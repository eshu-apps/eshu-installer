# AI Model Integration Guide for ESHU

This document explains exactly where and how AI models (LLMs) are integrated into ESHU.

---

## Overview

ESHU uses Large Language Models (LLMs) to provide intelligent package search, ranking, error analysis, and recommendations. The LLM integration is:
- **Optional** - ESHU works without LLM (falls back to basic search)
- **Provider-agnostic** - Supports Anthropic Claude, OpenAI, and Ollama (local)
- **Usage-limited in free tier** - 10 queries/day for free users, unlimited for premium

---

## 1. LLM Engine Core (`src/eshu/llm_engine.py`)

### Location: `src/eshu/llm_engine.py:10-461`

The `LLMEngine` class is the central component for all AI functionality.

### Initialization

**File:** `src/eshu/llm_engine.py:13-40`

```python
class LLMEngine:
    def __init__(self, config: ESHUConfig):
        self.config = config
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate LLM client"""
        if self.config.llm_provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)

        elif self.config.llm_provider == "openai":
            import openai
            self.client = openai.OpenAI(api_key=self.config.openai_api_key)

        elif self.config.llm_provider == "ollama":
            import openai
            self.client = openai.OpenAI(
                base_url=self.config.ollama_endpoint,  # http://localhost:11434
                api_key="ollama"  # Ollama doesn't need a real key
            )
```

**How it works:**
- Reads provider from config (default: "anthropic")
- Loads appropriate API key from config or environment variables
- For Ollama: Uses OpenAI-compatible API with local endpoint

---

## 2. Five AI-Powered Features

### Feature 1: Query Interpretation

**File:** `src/eshu/llm_engine.py:49-113`
**Used in:** `src/eshu/cli_enhanced.py:344-347`

**What it does:**
Converts natural language queries into structured search terms.

**Example:**
```
User types: "a terminal emulator for wayland"
LLM returns: {
  "search_terms": ["kitty", "alacritty", "foot"],
  "preferred_manager": null,
  "intent": "install",
  "requirements": ["wayland-compatible"]
}
```

**Code:**
```python
# cli_enhanced.py:344-347
if can_use_llm:
    console.print(f"🤖 Interpreting query: {query}")
    interpretation = llm.interpret_query(query, profile)
    search_terms = interpretation.get("search_terms", [query])
```

**Fallback:**
If LLM fails, uses the raw query as search term.

---

### Feature 2: Result Ranking & Recommendations (Premium)

**File:** `src/eshu/llm_engine.py:115-267`
**Used in:** `src/eshu/cli_enhanced.py:373-377`

**What it does:**
Analyzes search results and recommends the best package based on:
- User's distro (Arch, Debian, etc.)
- Hardware (GPU, CPU)
- Package manager priority
- Community warnings

**Example:**
```
User searches: "firefox"
Results: 362 packages (firefox-pacman, firefox-snap, firefox-flatpak...)

LLM analyzes and returns:
{
  "recommended_index": 0,  # firefox from pacman
  "explanation": "Official Arch package, best performance",
  "alternatives": [3, 5],  # flatpak and snap as backups
  "warnings": ["⚠️ Snap version may have sandbox issues"]
}
```

**Code:**
```python
# cli_enhanced.py:373-377
if can_use_llm and check_license_feature(license_mgr, "community_warnings", show_message=False):
    console.print("🤖 Analyzing results and checking for known issues...")
    recommended_results = llm.rank_and_recommend(query, ranked_results[:20], profile, check_community=True)
else:
    recommended_results = [(r, None) for r in ranked_results[:20]]
```

**Premium Check:**
Uses `community_warnings` feature flag (premium only).

**Fallback:**
Returns results as-is without recommendations.

---

### Feature 3: Lightweight Alternatives (Premium)

**File:** `src/eshu/llm_engine.py:269-293`
**Used in:** `src/eshu/cli_enhanced.py:394-399`

**What it does:**
Suggests lighter alternatives if system has < 4GB RAM.

**Example:**
```
User has 2GB RAM and searches: "chrome"
LLM suggests: {
  "name": "chromium",
  "reason": "Lighter alternative to Chrome, uses less RAM"
}
```

**Code:**
```python
# llm_engine.py:284-289
if ram_gb < 4:
    checker = self._get_community_checker()
    alternatives = checker.suggest_alternatives(package_name, reason="lightweight")
    if alternatives:
        return alternatives[0]
```

**Note:**
This actually uses the CommunityChecker, not direct LLM calls. It's a rule-based system with curated alternatives.

---

### Feature 4: Installation Plan Generation

**File:** `src/eshu/llm_engine.py:295-396`
**Used in:** `src/eshu/installer.py:16` (passed to installer)

**What it does:**
Generates step-by-step installation plans including:
- Commands to run
- Build system detection (make, cmake, cargo, etc.)
- Dependencies needed
- Post-install steps

**Example:**
```
Package: hyprland (AUR)
LLM generates: {
  "commands": ["yay -S hyprland"],
  "requires_build": true,
  "build_system": "meson",
  "dependencies": ["base-devel", "git"],
  "post_install": ["systemctl --user enable hyprland.service"],
  "notes": "May take 10-15 minutes to compile"
}
```

**Fallback:**
Uses `_generate_basic_install_plan()` which has hardcoded commands for each package manager.

---

### Feature 5: Error Analysis & Auto-Fix (Premium)

**File:** `src/eshu/llm_engine.py:398-460`
**Used in:** `src/eshu/installer.py:122-126`

**What it does:**
When installation fails, LLM analyzes the error output and suggests fixes.

**Example:**
```
Error: "error: failed to prepare transaction (could not satisfy dependencies)"
LLM analyzes and returns: {
  "error_type": "dependency",
  "diagnosis": "Missing base-devel package group",
  "solutions": [
    "Install base-devel package group",
    "Install missing dependencies manually"
  ],
  "commands": ["sudo pacman -S base-devel"]
}
```

**Code:**
```python
# installer.py:122-126
if critical:
    # Use LLM to analyze error and suggest fixes
    error_analysis = self.llm.handle_error(
        e.stderr if e.stderr else e.stdout,
        package,
        self.profile
    )
```

**Fallback:**
Returns generic error message: "Unable to analyze error".

---

## 3. Configuration (`src/eshu/config.py`)

### LLM Provider Settings

**File:** `src/eshu/config.py:13-23`

```python
class ESHUConfig(BaseModel):
    # LLM Provider settings
    llm_provider: str = "anthropic"  # or "openai", "ollama"
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    ollama_endpoint: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"

    # Model settings
    model_name: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.3
    max_tokens: int = 4096
```

### How Config is Loaded

**File:** `src/eshu/config.py:55-73`

Priority order:
1. **Config file** (if exists): `~/.config/eshu/config.json`
2. **Environment variables**: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`
3. **Defaults**: Falls back to defaults above

**Example config file:**
```json
{
  "llm_provider": "anthropic",
  "model_name": "claude-3-5-sonnet-20241022",
  "temperature": 0.3,
  "max_tokens": 4096,
  "package_manager_priority": ["pacman", "yay", "apt", "flatpak"]
}
```

**Setting API keys:**
```bash
# Option 1: Environment variable
export ANTHROPIC_API_KEY="sk-ant-..."
eshu install hyprland

# Option 2: Config command
eshu config set-key
# Prompts for API key interactively

# Option 3: Manual config file edit
vim ~/.config/eshu/config.json
```

---

## 4. Usage Limits & License Checks

### Free Tier: 10 Queries/Day

**File:** `src/eshu/license_manager.py:189-223`

```python
def check_usage_limit(self, feature: str) -> tuple[bool, str]:
    """Check if usage limit reached for free tier"""
    license = self.get_license()

    if license.tier == "premium":
        return True, "Unlimited"  # Premium gets unlimited

    # Load usage data
    usage = self._load_usage()
    today = datetime.now().strftime("%Y-%m-%d")

    # Check limits
    limits = {
        "llm_queries": 10,      # 10 AI queries/day (free)
        "installs": 50,         # 50 installs/day (free)
        "searches": 100,        # 100 searches/day (free)
    }

    if usage[today]["llm_queries"] >= 10:
        return False, "Daily limit reached (10/10). Upgrade to Premium for unlimited access."

    # Increment usage
    usage[today]["llm_queries"] += 1
    self._save_usage(usage)

    return True, "5/10 used today"
```

### Where it's Checked

**File:** `src/eshu/cli_enhanced.py:311-314`

```python
# Check LLM usage limit
can_use_llm, llm_status = license_mgr.check_usage_limit("llm_queries")
if not can_use_llm:
    console.print(f"[yellow]{llm_status}[/yellow]")
    # Continue with basic search (no LLM)
```

**What happens when limit is reached:**
- Shows message: "Daily limit reached (10/10). Upgrade to Premium..."
- ESHU continues to work but uses basic search (no AI features)
- Searches still work across all package managers
- No query interpretation, no recommendations, no error analysis

---

## 5. Premium Features Using LLM

### Feature Flags

**File:** `src/eshu/license_manager.py:51-92`

```python
free_features = {
    "basic_llm": False,  # Limited to 10 queries/day
    "unlimited_llm": False,
    "community_warnings": False,  # Uses LLM for ranking
    "adaptive_error_fixing": False,  # Uses LLM for error analysis
}

premium_features = {
    "basic_llm": True,
    "unlimited_llm": True,
    "community_warnings": True,
    "adaptive_error_fixing": True,
}
```

### Premium LLM Features:

1. **Unlimited queries** (`unlimited_llm`)
   - No daily limit on AI queries

2. **Community warnings** (`community_warnings`)
   - Uses LLM to rank packages with hardware-specific warnings
   - Checks compatibility with your GPU/CPU

3. **Adaptive error fixing** (`adaptive_error_fixing`)
   - LLM analyzes errors and suggests fixes
   - Auto-retry with suggested commands

---

## 6. Where LLM is Called (Summary)

### In `install` Command:

**File:** `src/eshu/cli_enhanced.py:280-520`

1. **Line 311:** Check usage limit
   ```python
   can_use_llm, llm_status = license_mgr.check_usage_limit("llm_queries")
   ```

2. **Line 340:** Initialize LLM engine
   ```python
   llm = LLMEngine(config)
   ```

3. **Line 345:** Interpret query
   ```python
   interpretation = llm.interpret_query(query, profile)
   ```

4. **Line 375:** Rank and recommend
   ```python
   recommended_results = llm.rank_and_recommend(query, ranked_results[:20], profile)
   ```

5. **Line 395:** Suggest lightweight alternatives
   ```python
   alt = llm.suggest_lightweight_alternative(package.name, profile)
   ```

### In Package Installer:

**File:** `src/eshu/installer.py:16-127`

6. **Line 16:** Pass LLM to installer
   ```python
   def __init__(self, config: ESHUConfig, llm_engine: LLMEngine, system_profile: SystemProfile)
   ```

7. **Line 122:** Analyze errors
   ```python
   error_analysis = self.llm.handle_error(e.stderr, package, self.profile)
   ```

---

## 7. Supported LLM Providers

### Anthropic Claude (Default, Recommended)

**Setup:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
eshu config set-provider anthropic
```

**Models:**
- `claude-3-5-sonnet-20241022` (default)
- `claude-3-opus-20240229`
- `claude-3-haiku-20240307`

**Cost:**
- Input: $3/million tokens
- Output: $15/million tokens
- Typical query: ~1000 tokens = $0.003

**Pros:**
- Best accuracy for package recommendations
- Excellent error analysis
- Fast response times

---

### OpenAI GPT (Alternative)

**Setup:**
```bash
export OPENAI_API_KEY="sk-..."
eshu config set-provider openai
```

**Models:**
- `gpt-4` (recommended)
- `gpt-3.5-turbo` (cheaper, less accurate)

**Cost:**
- GPT-4: $30-60/million tokens
- GPT-3.5: $0.50-1.50/million tokens

**Pros:**
- Widely available
- Good performance

**Cons:**
- More expensive than Claude
- Slightly less accurate for Linux-specific queries

---

### Ollama (Local, Free)

**Setup:**
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Configure ESHU
eshu config set-provider ollama
```

**Models:**
- `llama3.1:8b` (recommended, default)
- `mistral:7b`
- `codellama:13b`

**Cost:**
- FREE (runs locally)
- Requires ~8GB RAM for 8B models
- Requires ~16GB RAM for 13B models

**Pros:**
- Completely free
- No API keys needed
- Privacy (data stays local)
- No internet required

**Cons:**
- Slower than cloud APIs
- Less accurate than Claude/GPT-4
- Requires powerful hardware
- Uses more RAM

---

## 8. Testing LLM Integration

### Test 1: Basic Query Interpretation

```bash
# Set up API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Test natural language query
eshu install "a terminal emulator for wayland"

# Expected output:
# 🤖 Interpreting query: a terminal emulator for wayland
# Search terms: kitty, alacritty, foot
```

### Test 2: Package Ranking

```bash
# Search with many results
eshu install firefox

# Expected output (premium):
# 🤖 Analyzing results and checking for known issues...
# ✓ RECOMMENDED: firefox from official Arch repositories
# Better performance than snap/flatpak versions
```

### Test 3: Error Analysis

```bash
# Try to install something that will fail
eshu install some-broken-aur-package

# Expected output (premium):
# ❌ Command failed with exit code 1
# 🔍 Error Analysis:
#    Type: dependency
#    Diagnosis: Missing build dependency 'base-devel'
# 💡 Suggested Solutions:
#    1. Install base-devel package group
# 🔧 Suggested Commands:
#    sudo pacman -S base-devel
# ❓ Try suggested fixes? [Y/n]
```

### Test 4: Usage Limits (Free Tier)

```bash
# Remove premium license (if activated)
rm ~/.cache/eshu/license.json

# Make 10 queries
for i in {1..10}; do eshu search firefox; done

# 11th query should show:
# Daily limit reached (10/10). Upgrade to Premium for unlimited access.
```

---

## 9. Disabling LLM (Offline Mode)

ESHU works perfectly fine without LLM. To disable:

### Option 1: Don't Set API Key
Just don't configure any API key. ESHU will fall back to basic search.

### Option 2: Remove API Key
```bash
eshu config show
# Edit ~/.config/eshu/config.json and remove API keys
```

### What Still Works Without LLM:
- ✅ Multi-manager package search
- ✅ Package installation
- ✅ System profiling
- ✅ Eshu's Path bundles (premium)
- ✅ Snapshots (premium)

### What Doesn't Work:
- ❌ Natural language query interpretation
- ❌ AI-powered package ranking
- ❌ Community warnings
- ❌ Error analysis and auto-fix
- ❌ Lightweight alternative suggestions

---

## 10. Costs & Usage

### Typical Usage Patterns:

**Light user (5 installs/day):**
- ~5 LLM queries/day
- ~5000 tokens/day
- **Anthropic cost:** $0.015/day = $0.45/month
- **OpenAI GPT-4:** $0.30/day = $9/month
- **Ollama:** FREE

**Heavy user (20 installs/day):**
- ~20 LLM queries/day
- ~20,000 tokens/day
- **Anthropic cost:** $0.06/day = $1.80/month
- **OpenAI GPT-4:** $1.20/day = $36/month
- **Ollama:** FREE

**Free tier (10 queries/day max):**
- ~10 LLM queries/day
- ~10,000 tokens/day
- **Anthropic cost:** $0.03/day = $0.90/month
- **OpenAI GPT-4:** $0.60/day = $18/month

### Recommendation:

For **end users**: Use Ollama (free, local)
For **premium users**: Use Anthropic Claude (best accuracy, reasonable cost)
For **power users**: Use OpenAI GPT-4 (if budget allows)

---

## 11. Privacy & Security

### What Data is Sent to LLM:

**Query interpretation:**
- User's search query
- System distro name
- Available package managers

**Result ranking:**
- Package names, versions, descriptions
- User's GPU/CPU type
- User's distro

**Error analysis:**
- Error output (up to 2000 characters)
- Package name
- Package manager used

### What is NOT Sent:

- ❌ User's email or license key
- ❌ Installed package list
- ❌ Full system info
- ❌ File paths or usernames
- ❌ Any personal data

### Privacy with Ollama:

With Ollama, **NOTHING** is sent to external servers. All AI processing happens locally on your machine.

---

## 12. Troubleshooting LLM Issues

### Issue: "Anthropic API key not configured"

**Solution:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Or
eshu config set-key
```

### Issue: "LLM interpretation error"

**Cause:** API key invalid or network issue

**Solution:**
- Check API key is correct
- Check internet connection
- ESHU falls back to basic search automatically

### Issue: Ollama not responding

**Solution:**
```bash
# Start Ollama service
ollama serve

# Check if model is downloaded
ollama list

# Pull model if missing
ollama pull llama3.1:8b
```

### Issue: "Daily limit reached"

**Solution:**
- Upgrade to Premium for unlimited queries
- Or wait until tomorrow (resets at midnight)
- Or use basic search (still works without LLM)

---

## Summary

### LLM Integration Points:

| Feature | File | Line | Free | Premium | Fallback |
|---------|------|------|------|---------|----------|
| Query interpretation | `llm_engine.py` | 49-113 | ✓ (10/day) | ✓ Unlimited | Raw query |
| Package ranking | `llm_engine.py` | 115-267 | ❌ | ✓ | As-is ranking |
| Lightweight suggestions | `llm_engine.py` | 269-293 | ❌ | ✓ | None |
| Install plan | `llm_engine.py` | 295-396 | ✓ (10/day) | ✓ Unlimited | Basic plan |
| Error analysis | `llm_engine.py` | 398-460 | ❌ | ✓ | Generic error |

### LLM Providers:

| Provider | Cost | Accuracy | Speed | Privacy |
|----------|------|----------|-------|---------|
| **Anthropic Claude** | $0.003/query | ⭐⭐⭐⭐⭐ | Fast | Cloud |
| **OpenAI GPT-4** | $0.06/query | ⭐⭐⭐⭐ | Fast | Cloud |
| **Ollama (local)** | FREE | ⭐⭐⭐ | Slower | Local |

**Recommended:** Anthropic Claude for best accuracy, Ollama for privacy/cost.

---

**For more info:** See `QUICKSTART.md` for LLM setup guide.

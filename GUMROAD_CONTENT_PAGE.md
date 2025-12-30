# Gumroad Content Page

This is the content buyers see AFTER purchasing ESHU Premium. Copy this into Gumroad's "Content" section.

---

## Copy-Paste This Into Gumroad Content Page:

```markdown
# Welcome to ESHU Premium! 🎉

Thank you for upgrading! You now have access to all premium features including **Eshu's Path** curated bundles, unlimited AI queries, automatic snapshots, and more.

---

## Your License Key

**{license_key}**

⚠️ **Save this key!** You'll need it to activate ESHU Premium on your system.

---

## Quick Start (5 minutes)

### Step 1: Install ESHU

Open your terminal and run:

```bash
# Clone the repository
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer

# Install ESHU
pip install -e .
```

**Alternative installation methods:**
```bash
# Using pipx (recommended for isolation)
pipx install git+https://github.com/eshu-apps/eshu-installer.git

# Or download and install locally
pip install --user -e .
```

---

### Step 2: Activate Your License

```bash
eshu license-cmd activate {license_key}
```

You should see:
```
✓ License activated successfully!
✓ ESHU Premium features unlocked
```

---

### Step 3: Configure LLM (Optional but Recommended)

ESHU works without AI, but premium AI features are amazing!

**Option 1: Anthropic Claude (Recommended)**
```bash
export ANTHROPIC_API_KEY="your-api-key"
eshu config set-provider anthropic
```

**Option 2: Ollama (Free, Local)**
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Configure ESHU
eshu config set-provider ollama
```

**Option 3: OpenAI**
```bash
export OPENAI_API_KEY="your-api-key"
eshu config set-provider openai
```

Don't have API keys? See the [AI Setup Guide](https://github.com/eshu-apps/eshu-installer/blob/main/AI_INTEGRATION_GUIDE.md)

---

### Step 4: Try It Out!

```bash
# Try Eshu's Path (Premium Feature!)
eshu install hyprland

# You'll see:
# 📦 Eshu's Path Available!
# Complete Hyprland Setup
# Includes 15 packages: hyprland, kitty, wofi, waybar, mako...
# Install complete bundle? [Y/n]
```

**Other commands to try:**
```bash
# Search for packages
eshu search firefox

# Find bloat (Premium)
eshu cleanup

# Create a snapshot (Premium)
eshu snapshot create

# Check your license status
eshu license-cmd status
```

---

## Premium Features You Now Have

### 📦 Eshu's Path - Curated Bundles
Install complete setups in one command:
- **Hyprland** - Full Wayland ecosystem (15 packages)
- **NVIDIA Proprietary** - Complete driver stack (8 packages)
- **Rust Development** - Full toolchain (9 packages)
- **Linux Gaming** - Steam + Proton + Wine (11 packages)
- **10+ more curated paths!**

```bash
eshu install hyprland    # Get the full bundle!
eshu install "nvidia proprietary"
eshu install "rust development"
```

### 🤖 Unlimited AI Queries
- Natural language package search
- Intelligent recommendations
- Hardware compatibility warnings
- No daily limits!

### 📸 Time Machine - System Snapshots
- Automatic snapshots before installations
- One-click rollback if something breaks
- Never worry about breaking your system

```bash
eshu snapshot list       # View all snapshots
eshu snapshot create     # Create manual snapshot
eshu snapshot restore <id>  # Rollback
```

### 🧹 Smart Bloat Analyzer
- Find orphaned packages
- Detect duplicates across package managers
- Identify large unused packages
- Reclaim disk space

```bash
eshu cleanup            # Dry run (shows what would be removed)
eshu cleanup --execute  # Actually remove bloat
```

### ⚠️ Community Hardware Warnings
- NVIDIA/AMD GPU compatibility alerts
- CPU-specific optimizations
- Known issue detection
- Automatic workaround suggestions

### 💡 Lightweight Alternatives
- AI suggests lighter packages when RAM < 4GB
- Perfect for older hardware
- Optimized for your system specs

### 🎯 Priority Support
- 24-hour response time
- Direct access to developers
- Feature requests prioritized

---

## Documentation & Resources

### Quick Links
- 📖 [Main Documentation](https://github.com/eshu-apps/eshu-installer/blob/main/README.md)
- 🚀 [Quick Start Guide](https://github.com/eshu-apps/eshu-installer/blob/main/QUICKSTART.md)
- 🤖 [AI Integration Guide](https://github.com/eshu-apps/eshu-installer/blob/main/AI_INTEGRATION_GUIDE.md)
- 📦 [Eshu's Path Feature](https://github.com/eshu-apps/eshu-installer/blob/main/ESHUS_PATH_FEATURE.md)
- 📝 [Command Reference](https://github.com/eshu-apps/eshu-installer/blob/main/ESHU_QUICK_REFERENCE.md)

### Video Tutorials (Coming Soon)
- Installation walkthrough
- Eshu's Path demo
- Advanced features

---

## Supported Distributions

ESHU works on **all major Linux distributions:**

✅ **Arch Linux** (full support)
✅ **Manjaro** (full support)
✅ **EndeavourOS** (full support)
✅ **Debian/Ubuntu** (full support)
✅ **Fedora** (in progress)
✅ **Pop!_OS** (full support)
✅ **Linux Mint** (full support)
✅ Any distro with Python 3.9+

---

## Supported Package Managers

ESHU searches across ALL of these simultaneously:

| Manager | Status | Size Info |
|---------|--------|-----------|
| **pacman** (Arch) | ✅ Full support | ✅ |
| **yay** (AUR) | ✅ Full support | ❌ |
| **paru** (AUR) | ✅ Full support | ❌ |
| **apt** (Debian/Ubuntu) | ✅ Full support | ❌ |
| **flatpak** | ✅ Full support | ✅ |
| **snap** | ✅ Full support | ❌ |
| **cargo** (Rust) | ✅ Full support | ❌ |
| **npm** (Node.js) | ✅ Full support | ❌ |
| **pip** (Python) | ✅ Full support | ❌ |

---

## Troubleshooting

### Issue: Command not found after installation

**Solution:**
```bash
# Make sure pip bin directory is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Add to ~/.bashrc or ~/.zshrc to make permanent
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Or reinstall with pipx
pipx install git+https://github.com/eshu-apps/eshu-installer.git
```

### Issue: License activation failed

**Solution:**
```bash
# Make sure you copied the full license key
eshu license-cmd activate ESHU-XXXX-XXXX-XXXX-XXXX

# Check license status
eshu license-cmd status

# If still having issues, contact support
```

### Issue: LLM API key not working

**Solution:**
```bash
# Check current config
eshu config show

# Set API key manually
eshu config set-key

# Or use environment variable
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Issue: Permission denied

**Solution:**
```bash
# ESHU needs sudo for system package managers
# Make sure your user is in sudoers

# For AUR helpers (yay/paru), run as regular user (NOT sudo)
eshu install package-name
```

---

## Support & Community

### Need Help?

**📧 Email Support:** support@eshu-installer.com
- Response time: 24 hours (premium users)
- Include your license key and error output

**💬 GitHub Issues:** https://github.com/eshu-apps/eshu-installer/issues
- Bug reports
- Feature requests
- Community discussion

**📖 Documentation:** https://github.com/eshu-apps/eshu-installer
- Full documentation
- Troubleshooting guides
- Examples and tutorials

---

## Share Your Experience!

Love ESHU? Help spread the word:

**Tweet about it:**
```
Just tried @eshu_apps Premium and installed a complete Hyprland setup with ONE command. 🤯

Eshu's Path is a game-changer for Linux package management!

https://eshu-apps.gumroad.com/l/eshu-premium
```

**Leave a review:**
- Star the repo: https://github.com/eshu-apps/eshu-installer
- Share on Reddit: r/linux, r/archlinux, r/unixporn
- Write a blog post

We read every piece of feedback! 💙

---

## Your Subscription

**Plan:** ESHU Premium ($9.99/month)
**Status:** Active
**Renewal:** Automatic (cancel anytime from your Gumroad Library)

**To cancel:**
1. Go to https://gumroad.com/library
2. Find "ESHU Premium"
3. Click "Cancel subscription"
4. You'll keep access until the end of your billing period

**Refund policy:** 14-day money-back guarantee. Email support@eshu-installer.com if you're not satisfied.

---

## Updates & Changelog

Your premium subscription includes **free updates for life**!

**Recent updates:**
- ✨ **v0.3.0** - Eshu's Path curated bundles (NEW!)
- 🎨 Improved UX and table text wrapping
- 🐛 Fixed premium prompt placement
- 📚 Comprehensive documentation

**Coming soon:**
- More curated paths (Desktop environments, server stacks)
- GUI interface
- Plugin system
- More package manager support

Follow updates: https://github.com/eshu-apps/eshu-installer/releases

---

## Examples to Try

### Example 1: Install Hyprland Ecosystem

```bash
eshu install hyprland

# ESHU will offer the complete bundle:
# 📦 Eshu's Path Available!
# Complete Hyprland Setup
# Includes 15 packages: hyprland, kitty, wofi, waybar, mako...
```

### Example 2: Set Up Rust Development

```bash
eshu install "rust development"

# Gets you:
# - rustc, cargo, rust-analyzer
# - clippy, rustfmt
# - cargo-watch, cargo-audit
# Complete toolchain in one command!
```

### Example 3: Gaming Setup

```bash
eshu install "linux gaming"

# Installs:
# - Steam, Proton
# - Wine, Lutris
# - Performance tools
# Everything you need for gaming on Linux!
```

### Example 4: Clean Up Your System

```bash
# Find bloat
eshu cleanup

# Shows:
# 🧹 Found 234MB of orphaned packages
# 🗑️  5 duplicate packages across managers
# 💾 1.2GB of unused packages

# Remove it
eshu cleanup --execute
```

---

## Tips & Tricks

### Tip 1: Use Eshu's Path for Everything
Instead of googling "what packages do I need for X", just try:
```bash
eshu install X
```

If there's a curated path, ESHU will suggest it!

### Tip 2: Create Snapshots Before Major Changes
```bash
eshu snapshot create
eshu install some-risky-package
# If it breaks, rollback:
eshu snapshot restore <id>
```

### Tip 3: Use Natural Language
ESHU understands context:
```bash
eshu install "a fast terminal for wayland"
# AI interprets → suggests kitty, alacritty, foot
```

### Tip 4: Check for Bloat Regularly
```bash
# Weekly cleanup
eshu cleanup --execute
# Can reclaim gigabytes!
```

### Tip 5: Use Ollama for Free AI
Don't want to pay for API keys? Use Ollama (local, free):
```bash
ollama pull llama3.1:8b
eshu config set-provider ollama
# Unlimited AI queries, no API costs!
```

---

## Thank You! 🙏

Thank you for supporting ESHU Premium! Your subscription helps us:
- 🚀 Build new features
- 📚 Improve documentation
- 🐛 Fix bugs faster
- 💡 Create more curated paths

Questions? Email support@eshu-installer.com

Happy installing! 🎉

---

**ESHU Premium** - One command for every package. AI-powered universal Linux installer.

https://github.com/eshu-apps/eshu-installer
```

---

## Gumroad Setup Instructions

### Where to Add This Content:

1. **Log into Gumroad**
2. **Go to your product** (ESHU Premium)
3. **Click "Edit product"**
4. **Scroll to "Content" section**
5. **Paste the markdown above** into the content editor
6. **Enable "Use Markdown"** toggle (if available)
7. **Click "Save"**

### What Gumroad Auto-Adds:

Gumroad will automatically insert:
- `{license_key}` → Actual license key
- Purchase date
- Customer email
- Download button (if you attach files)

### Optional: Attach Files

You can also attach these files for easy download:

**To attach:**
1. Create a ZIP file with:
   - `README.md`
   - `QUICKSTART.md`
   - `AI_INTEGRATION_GUIDE.md`
   - `ESHU_QUICK_REFERENCE.md`

2. Upload to Gumroad:
   - Product → Edit → Files
   - Click "Add file"
   - Upload the ZIP
   - Customers can download after purchase

**Note:** Not necessary since everything is on GitHub, but it's a nice touch!

---

## Content Page Best Practices

### ✅ DO:
- Include clear installation instructions
- Show example commands
- Provide troubleshooting section
- Link to documentation
- Include support email
- Show license key prominently
- Explain all premium features

### ❌ DON'T:
- Make it too long (but this length is fine)
- Forget to test all links
- Hide the license key
- Skip troubleshooting
- Forget support contact info

---

## Preview Your Content Page

After pasting:
1. Click "Preview" in Gumroad
2. Check that all markdown renders correctly
3. Test all links
4. Make a test purchase to see customer experience
5. Adjust formatting if needed

---

**This content page is ready to copy-paste directly into Gumroad!**

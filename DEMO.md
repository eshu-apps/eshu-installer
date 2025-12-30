# ESHU Demo & Usage Guide

## Quick Start

### 1. Installation

```bash
cd ~/eshu-installer
./install.sh
```

Or manual installation:

```bash
pip install -e .
export ANTHROPIC_API_KEY="your-key-here"
eshu config set-provider anthropic
```

### 2. First Run - System Profile

```bash
# Scan your system
eshu profile

# Output:
# ╭────────────────────────────────────────────── System Profile ──────────────────────────────────────────────╮
# │ Distribution: arch unknown                                                                                 │
# │ Kernel: 6.17.10                                                                                            │
# │ Architecture: x86_64                                                                                       │
# │ Available Package Managers: pacman, yay, cargo, npm, pip3                                                  │
# │ Installed Packages: 1234                                                                                   │
# │ Profile Updated: 2024-01-15T10:30:00                                                                       │
# ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### 3. Search for Packages

```bash
# Search across ALL package managers at once
eshu search hyprland

# Output shows results from pacman, AUR, cargo, npm, etc.
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
# ┃ Package                 ┃ Version                 ┃ Manager ┃ Repository ┃ Description            ┃ Status ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
# │ hyprland                │ 0.35.0                  │ pacman  │ extra      │ Dynamic tiling Wayland │        │
# │ hyprland-git            │ 0.35.0.r1               │ yay     │ aur        │ Development version    │        │
```

### 4. Install with AI Assistance

```bash
# Natural language installation
eshu install hyprland

# The AI will:
# 1. Interpret your query
# 2. Search all package managers
# 3. Rank results by relevance
# 4. Recommend the best option
# 5. Generate installation plan
# 6. Handle errors adaptively
```

## Real-World Examples

### Example 1: Installing Hyprland on Arch

```bash
$ eshu install hyprland

🔍 Scanning system...
System: arch unknown (x86_64)
Available managers: pacman, yay, cargo, npm, pip3

🤖 Interpreting query: hyprland
Search terms: hyprland

🔎 Searching for 'hyprland'...

📦 Search Reshults:

#  Package              Version    Manager  Repository  Status
1  hyprland            0.35.0     pacman   extra       
2  hyprland-git        0.35.0.r1  yay      aur         
3  hyprland-protocols  0.2        pacman   extra       

✓ RECOMMENDED: hyprland from official Arch repositories is the stable release, 
recommended for most users. The AUR version (hyprland-git) is the development version.

Description: A dynamic tiling Wayland compositor that doesn't sacrifice on its looks

Select package number to install (0 to cancel) [1]: 1

📦 Installing hyprland via pacman...

📋 Installation Plan:
   Commands: sudo pacman -S hyprland
   ℹ️  Note: Standard installation for pacman

❓ Proceed with installation? [Y/n]: y

▶ Executing: sudo pacman -S hyprland
✓ Command completed successfully

✓ Successfully installed hyprland!
🔍 Verifying installation of hyprland...
✓ hyprland is available in PATH
```

### Example 2: Installing from AUR with Build Issues

```bash
$ eshu install some-aur-package

[... search and selection ...]

📦 Installing some-aur-package via yay...

📋 Installation Plan:
   Commands: yay -S some-aur-package
   ⚙️  Requires build: true
   ℹ️  Note: AUR package, will be built from source

▶ Executing: yay -S some-aur-package

❌ Command failed with exit code 1

🔍 Error Analysis:
   Type: dependency
   Diagnosis: Missing build dependency 'base-devel' package group

💡 Suggested Solutions:
   1. Install base-devel package group which contains essential build tools
   2. Ensure all build dependencies are installed
   3. Check PKGBUILD for additional requirements

🔧 Suggested Commands:
   sudo pacman -S base-devel

❓ Try suggested fixes? [Y/n]: y

▶ Executing: sudo pacman -S base-devel
✓ Command completed successfully

▶ Retrying: yay -S some-aur-package
✓ Command completed successfully

✓ Successfully installed some-aur-package!
```

### Example 3: Cross-Platform Package Search

```bash
$ eshu search "terminal emulator"

🤖 Interpreting query: terminal emulator
Search terms: alacritty, kitty, wezterm, foot

🔎 Searching for 'alacritty'...
🔎 Searching for 'kitty'...
🔎 Searching for 'wezterm'...
🔎 Searching for 'foot'...

📦 Search Reshults:

#  Package              Version    Manager  Repository  Status
1  alacritty           0.13.1     pacman   extra       ✓ Installed
2  kitty               0.32.0     pacman   extra       
3  wezterm             20240203   cargo    crates.io   
4  foot                1.16.2     pacman   extra       
5  alacritty           0.13.1     flatpak  flathub     
6  kitty               0.32.0     snap     snapcraft   

✓ RECOMMENDED: alacritty from pacman is already installed. 
For Wayland-native alternatives, consider 'foot' or 'kitty'.

Description: A cross-platform, GPU-accelerated terminal emulator
```

### Example 4: Installing Development Tools

```bash
$ eshu install "rust development environment"

🤖 Interpreting query: rust development environment
Search terms: rust, cargo, rustup, rust-analyzer

🔎 Searching...

📦 Search Reshults:

#  Package              Version    Manager  Repository  Status
1  rust                1.75.0     pacman   extra       
2  rustup              1.26.0     pacman   extra       
3  rust-analyzer       2024.01    pacman   extra       
4  cargo               1.75.0     pacman   extra       

✓ RECOMMENDED: Install 'rustup' which provides the complete Rust toolchain 
management system. It includes rust, cargo, and allows easy version switching.

Description: The Rust toolchain installer

Select package number to install (0 to cancel) [2]: 2

📦 Installing rustup via pacman...

📋 Installation Plan:
   Commands: sudo pacman -S rustup
   Post-install: rustup default stable
   ℹ️  Note: After installation, run 'rustup default stable' to install the stable toolchain

[... installation proceeds ...]

✓ Successfully installed rustup!

🔧 Running post-install steps...
▶ Executing: rustup default stable
✓ Command completed successfully
```

### Example 5: Handling Multiple Package Managers

```bash
$ eshu install neovim

🔎 Searching for 'neovim'...

📦 Search Reshults:

#  Package              Version    Manager  Repository  Status
1  neovim              0.9.5      pacman   extra       
2  neovim              0.9.5      flatpak  flathub     
3  neovim              0.9.5      snap     snapcraft   
4  neovim              0.9.5      cargo    crates.io   
5  neovim              5.4.0      npm      npmjs       

✓ RECOMMENDED: neovim from pacman (native package) is preferred over 
containerized versions (flatpak/snap) for better system integration.

Description: Vim-fork focused on extensibility and usability

Select package number to install (0 to cancel) [1]: 1
```

## Advanced Features

### Auto-Confirm Mode

```bash
# Skip all prompts, use defaults
eshu install -y package-name
```

### Force Profile Refresh

```bash
# Refresh system cache before search
eshu install -r package-name
```

### View Installed Packages

```bash
# Show all installed packages
eshu profile --packages

# Output:
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
# ┃ Package                 ┃ Version                 ┃ Manager ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
# │ hyprland                │ 0.35.0                  │ pacman  │
# │ neovim                  │ 0.9.5                   │ pacman  │
# │ rust                    │ 1.75.0                  │ pacman  │
# ... and 1231 more
```

### Configuration Management

```bash
# Show current configuration
eshu config show

# Set API key
eshu config set-key

# Change LLM provider
eshu config set-provider ollama

# Use local Ollama (free, no API key needed)
eshu config set-provider ollama
# Then: ollama pull llama3.1:8b
```

## Systemd Service

Enable automatic system profiling at boot:

```bash
# Install service
sudo cp systemd/eshu-profiler.* /etc/systemd/system/
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable --now eshu-profiler.timer

# Check status
sudo systemctl status eshu-profiler.timer

# View logs
journalctl -u eshu-profiler.service
```

The service will:
- Run 2 minutes after boot
- Update system profile daily
- Cache results for fast queries

## Configuration File

Location: `~/.config/eshu/config.json`

```json
{
  "llm_provider": "anthropic",
  "model_name": "claude-3-5-sonnet-20241022",
  "temperature": 0.3,
  "package_manager_priority": [
    "pacman",
    "yay",
    "paru",
    "apt",
    "flatpak",
    "snap",
    "cargo",
    "npm",
    "pip"
  ],
  "cache_dir": "/var/cache/eshu",
  "build_dir": "/tmp/eshu-builds",
  "auto_confirm_deps": false,
  "prefer_native": true,
  "enable_aur": true,
  "parallel_jobs": 0
}
```

## Tips & Tricks

### 1. Use Natural Language

```bash
# Instead of remembering package names:
eshu install "wayland compositor"
eshu install "pdf viewer"
eshu install "screenshot tool"
```

### 2. Compare Package Managers

```bash
# See the same package across different managers
eshu search firefox
# Shows: pacman, flatpak, snap versions
```

### 3. Check Before Installing

```bash
# Search first to see options
eshu search hyprland

# Then install specific one
eshu install hyprland
```

### 4. Use Ollama for Free

```bash
# No API costs, runs locally
ollama pull llama3.1:8b
eshu config set-provider ollama

# Now use ESHU without API keys
eshu install anything
```

### 5. Batch Operations

```bash
# Install multiple packages
for pkg in neovim tmux git; do
    eshu install -y $pkg
done
```

## Troubleshooting

### Issue: "API key not configured"

```bash
# Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."
eshu config set-key

# Or use Ollama (free)
eshu config set-provider ollama
```

### Issue: "Permission denied: /var/cache/eshu"

```bash
# Create cache directory
sudo mkdir -p /var/cache/eshu
sudo chmod 755 /var/cache/eshu
```

### Issue: "Package not found"

```bash
# Refresh system profile
eshu profile --refresh

# Try different search terms
eshu search "alternative name"
```

### Issue: Build failures

ESHU will automatically:
1. Detect the error type
2. Suggest fixes
3. Offer to apply them

Just answer "y" when prompted!

## Performance

- **First run**: ~5-10 seconds (system scan)
- **Cached runs**: <1 second
- **Search**: 2-5 seconds (parallel across all managers)
- **LLM analysis**: 1-3 seconds

## Supported Distributions

- ✅ Arch Linux (pacman, yay, paru)
- ✅ Debian/Ubuntu (apt)
- ✅ Fedora (dnf) - partial
- ✅ Any distro with flatpak/snap
- ✅ Universal: cargo, npm, pip

## Next Steps

1. **Try it**: `eshu install hyprland`
2. **Explore**: `eshu search "your favorite app"`
3. **Configure**: `eshu config show`
4. **Automate**: Enable systemd service
5. **Contribute**: Add more package managers!

## Why ESHU?

**Before ESHU:**
```bash
# Which package manager?
pacman -Ss hyprland  # Not found
yay -Ss hyprland     # Found in AUR
# Install
yay -S hyprland
# Build fails - missing dependencies
# Google error message
# Install base-devel
sudo pacman -S base-devel
# Try again
yay -S hyprland
# Success!
```

**With ESHU:**
```bash
eshu install hyprland
# AI finds it, recommends best option, handles errors
# Done!
```

---

**ESHU** - One command for every package. AI-powered universal Linux installer.. 🚀

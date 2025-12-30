<div align="center">

<img src="assets/logo.png" alt="ESHU Logo" width="300"/>

# ESHU

### AI-Driven Universal Package Installer for Linux

> **One command for every package. AI-powered universal Linux installer.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.3.0-green.svg)](https://github.com/eshu-apps/eshu-installer/releases)
[![Premium](https://img.shields.io/badge/premium-$4.99%2Fmonth-gold.svg)](https://eshu-installer.com/upgrade)

</div>

---

**ESHU** is an intelligent, AI-powered package installer that unifies all Linux package managers under a single natural language interface. No more remembering whether to use `pacman`, `apt`, `yay`, `cargo`, `npm`, or any other package manager - just tell ESHU what you want to install.

## ✨ Features

🤖 **AI-Powered Intelligence**
- Natural language package queries
- Intelligent package ranking and recommendations
- Adaptive error handling with suggested fixes
- Context-aware installation plans

🔍 **Universal Package Search**
- Searches across all available package managers simultaneously
- Supports: pacman, yay, paru, apt, flatpak, snap, cargo, npm, pip, and more
- Unified result ranking and deduplication
- Paginated results with `--all` flag

⚙️ **Adaptive Installation**
- Automatically detects best installation method
- Handles build systems: make, cmake, cargo, meson, etc.
- Intelligent dependency resolution
- Real-time error analysis and recovery

📊 **System Profiling**
- Scans installed packages and dependencies at boot
- Caches system state for fast queries
- Tracks available package managers
- Systemd service integration

📸 **Time Machine (Premium)**
- Automatic snapshots before installations
- One-click rollback if something breaks
- Supports Timeshift and Btrfs

⚠️ **Community Warnings (Premium)**
- Hardware-specific compatibility alerts
- Known issue detection
- Automatic workaround suggestions

🧹 **Smart Cleanup (Premium)**
- Find and remove orphaned packages
- Detect duplicate packages
- Identify large unused packages
- Calculate reclaimable space

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer

# Install with pip
pip install -e .
```

### Basic Usage

```bash
# Search for packages
eshu search firefox

# Install packages
eshu install hyprland

# View system profile
eshu profile

# Find bloat
eshu cleanup
```

### Configure LLM (Optional for AI features)

```bash
# Option 1: Anthropic Claude (Recommended)
export ANTHROPIC_API_KEY="your-api-key"
eshu config set-provider anthropic

# Option 2: Ollama (Free, Local)
ollama pull llama3.1:8b
eshu config set-provider ollama
```

## 📦 Installation

### Prerequisites

```bash
# On Arch Linux
sudo pacman -S python python-pip git

# On Debian/Ubuntu
sudo apt install python3 python3-pip git
```

### Install ESHU

```bash
# Clone repository
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer

# Install with pip (recommended)
pip install -e .

# Or install system-wide
sudo pip install .
```

### Configure LLM Provider

ESHU supports multiple LLM providers:

**Option 1: Anthropic Claude (Recommended)**
```bash
export ANTHROPIC_API_KEY="your-api-key"
eshu config set-provider anthropic
```

**Option 2: OpenAI**
```bash
export OPENAI_API_KEY="your-api-key"
eshu config set-provider openai
```

**Option 3: Ollama (Local, Free)**
```bash
# Install Ollama first: https://ollama.ai
ollama pull llama3.1:8b
eshu config set-provider ollama
```

### Enable System Profiler Service (Optional)

```bash
# Copy systemd units
sudo cp systemd/eshu-profiler.* /etc/systemd/system/

# Enable and start
sudo systemctl enable --now eshu-profiler.timer

# Check status
sudo systemctl status eshu-profiler.timer
```

## 💻 Usage

### Install Packages

```bash
# Natural language queries
eshu install hyprland
eshu install "a terminal emulator for wayland"
eshu install "rust compiler"

# Auto-confirm installation
eshu install -y neovim

# Skip snapshot creation
eshu install --no-snapshot firefox
```

### Search Packages

```bash
# Search across all package managers
eshu search hyprland

# View all results with pagination
eshu search firefox --all
# Press 'n' for next, 'p' for previous, '#' to select

# Search specific manager
eshu search --manager pacman hyprland
```

### System Maintenance

```bash
# View system profile
eshu profile

# Find bloat (Premium)
eshu cleanup                    # Dry run
eshu cleanup --execute          # Actually remove

# Manage snapshots (Premium)
eshu snapshot list              # View snapshots
eshu snapshot create            # Create snapshot
eshu snapshot restore <id>      # Restore snapshot
```

### Configuration

```bash
# Show current configuration
eshu config show

# Set API key
eshu config set-key

# Change LLM provider
eshu config set-provider ollama
```

### License Management

```bash
# Check license status
eshu license-cmd status

# Activate premium
eshu license-cmd activate YOUR-LICENSE-KEY

# View usage
eshu license-cmd usage
```

## 📚 Examples

### Example 1: Install Hyprland

```bash
$ eshu install hyprland

🔍 Scanning system...
System: arch unknown (x86_64)
Available managers: pacman, yay, cargo, npm, pip3

🤖 Interpreting query: hyprland
Search terms: hyprland

🔎 Searching for 'hyprland'...

📦 Search Results:

┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┓
┃ Package          ┃ Version   ┃ Manager┃ Size    ┃ OS     ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━┩
│ hyprland         │ 0.35.0    │ pacman │ 12.5 MB │ 🔷 Arch│
│ hyprland-git     │ 0.35.0.r1 │ yay    │ N/A     │ 🔷 Arch│
└──────────────────┴───────────┴────────┴─────────┴────────┘

✓ RECOMMENDED: hyprland from official Arch repositories

Select package number to install (0 to cancel) [1]: 1

📸 Creating snapshot before installation...
✓ Snapshot created: snapshot_20231215_143022

📦 Installing hyprland via pacman...
✓ Successfully installed hyprland!
```

### Example 2: Search with Pagination

```bash
$ eshu search firefox --all

Found 362 packages:

┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┓
┃ Package          ┃ Version   ┃ Manager┃ Size    ┃ OS     ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━┩
│ firefox          │ 131.0     │ pacman │ 268.9 MB│ 🔷 Arch│
│ firefox          │ 131.0     │ snap   │ N/A     │ 🌐 All │
│ firefox-esr      │ 128.0     │ apt    │ N/A     │ 🔴 Deb │
└──────────────────┴───────────┴────────┴─────────┴────────┘

Showing 1-15 of 362 results
[n]ext | [p]revious | [#]select | [q]uit: 
```

### Example 3: Handle Build Errors

```bash
$ eshu install some-aur-package

[... installation starts ...]

❌ Command failed with exit code 1

🔍 Error Analysis:
   Type: dependency
   Diagnosis: Missing build dependency 'base-devel'

💡 Suggested Solutions:
   1. Install base-devel package group
   2. Install missing dependencies manually

🔧 Suggested Commands:
   sudo pacman -S base-devel

❓ Try suggested fixes? [Y/n]: y

▶ Executing: sudo pacman -S base-devel
✓ Command completed successfully
✓ Retrying installation...
✓ Successfully installed!
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         ESHU CLI                             │
│                    (Natural Language)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     LLM Engine                               │
│  • Query Interpretation  • Result Ranking                    │
│  • Install Planning      • Error Analysis                    │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   System    │  │   Package   │  │  Package    │
│  Profiler   │  │  Searcher   │  │  Installer  │
└─────────────┘  └─────────────┘  └─────────────┘
         │               │               │
         ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│              Package Manager Abstraction Layer               │
│  pacman │ yay │ apt │ flatpak │ snap │ cargo │ npm │ pip    │
└─────────────────────────────────────────────────────────────┘
```

## ⚙️ Configuration

Configuration file location:
- User: `~/.config/eshu/config.json`
- System: `/etc/eshu/config.json`

Example configuration:

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
  "enable_aur": true
}
```

## 📦 Supported Package Managers

| Manager  | Status | Features                          | Size Info |
|----------|--------|-----------------------------------|-----------|
| pacman   | ✅     | Full support                      | ✅        |
| yay      | ✅     | AUR support, build handling       | ❌        |
| paru     | ✅     | AUR support, build handling       | ❌        |
| apt      | ✅     | Full support                      | ❌        |
| flatpak  | ✅     | Containerized apps                | ✅        |
| snap     | ✅     | Containerized apps                | ❌        |
| cargo    | ✅     | Rust packages, build support      | ❌        |
| npm      | ✅     | Node.js packages                  | ❌        |
| pip      | ✅     | Python packages (PyPI API)        | ❌        |
| dnf      | 🚧     | Planned                           | -         |
| zypper   | 🚧     | Planned                           | -         |

## 💎 Free vs Premium

### Free Tier
- ✅ Multi-manager package search
- ✅ Basic installation
- ✅ System profiling
- ✅ 10 AI queries/day
- ✅ All package managers

### Premium ($4.99/month)
- ✅ **Everything in Free**
- ✅ Unlimited AI queries
- ✅ Automatic snapshots & rollback
- ✅ Community hardware warnings
- ✅ Smart bloat finder
- ✅ Lightweight suggestions
- ✅ Priority support

[**Upgrade to Premium →**](https://eshu-installer.com/upgrade)

## 🔧 Troubleshooting

### LLM API Key Issues

```bash
# Check if key is set
eshu config show

# Set key manually
eshu config set-key

# Or use environment variable
export ANTHROPIC_API_KEY="your-key"
```

### Cache Issues

```bash
# Clear cache
sudo rm -rf ~/.cache/eshu/*

# Rebuild profile
eshu profile --refresh
```

### Permission Issues

```bash
# ESHU needs sudo for system package managers
# Make sure your user is in sudoers

# For AUR helpers (yay/paru), run as regular user
eshu install package-name
```

### No Search Results

```bash
# Check available package managers
eshu profile

# Make sure repositories are configured
# For snap:
sudo snap install core

# For flatpak:
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Additional package manager support (dnf, zypper, etc.)
- [ ] Better build system detection
- [ ] Package conflict resolution
- [ ] GUI interface
- [ ] Plugin system
- [ ] More size information for package managers

## 📄 License

MIT License - see LICENSE file

## 🙏 Credits

Built with:
- [Anthropic Claude](https://anthropic.com) - AI intelligence
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Pydantic](https://pydantic.dev/) - Configuration management

## 📚 Documentation

- **QUICKSTART.md** - 5-minute setup guide
- **DEMO.md** - Real-world usage examples
- **ARCHITECTURE.md** - Technical implementation details
- **GITHUB_DEPLOYMENT_GUIDE.md** - Launch instructions
- **ESHU_QUICK_REFERENCE.md** - Command reference card

---

**ESHU** - One command for every package. AI-powered universal Linux installer. 🚀

*For detailed documentation, see the docs/ directory*

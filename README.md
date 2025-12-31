<div align="center">

# 🚀 ESHU

### Universal Package Installer for Linux

> **One command for every package. Stop juggling package managers.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.3.0-green.svg)](https://github.com/eshu-apps/eshu-installer/releases)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

<a href="https://eshu-apps.gumroad.com/l/eshu-premium"><img src="https://img.shields.io/badge/Premium-$9.99%2Fmonth-gold.svg?style=for-the-badge" alt="Upgrade to Premium"></a>

</div>

---

## 🎯 What is ESHU?

**ESHU** unifies **all** Linux package managers under a single interface. No more remembering different commands for pacman, apt, yay, flatpak, snap, cargo, npm, and pip.

### Stop This:

```bash
# Which package manager has firefox?
apt search firefox
snap search firefox
flatpak search firefox
yay -Ss firefox

# Which one should I use? Which is best?
# Let me check Reddit... *30 minutes later*
```

### Do This Instead:

```bash
eshu install firefox
# ✓ Searches across ALL package managers
# ✓ Shows best option for your system
# ✓ One command. Done.
```

---

## ✨ Features

- 🔍 **Universal Search** - Search across pacman, yay, apt, flatpak, snap, cargo, npm, pip simultaneously
- ⚡ **Smart Installation** - Automatically picks the best package manager for your system
- 🤖 **AI-Powered** (Optional) - Natural language queries and intelligent recommendations
- 📦 **Eshu's Path** (Premium) - Curated package bundles for complete setups
- 📸 **Time Machine** (Premium) - Automatic snapshots before installations
- 🧹 **Smart Cleanup** (Premium) - Find and remove bloat

---

## 🚀 Quick Install

```bash
# Clone the repository
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer

# Run the installer (handles everything automatically)
./install-eshu.sh
```

That's it! The installer will:
- ✅ Create a Python virtual environment (no system pollution)
- ✅ Install all dependencies
- ✅ Create the `eshu` command in `~/.local/bin`
- ✅ Test the installation

### Add to PATH (if needed)

If `~/.local/bin` isn't in your PATH, add this to your shell config:

**Bash** (`~/.bashrc`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Fish** (`~/.config/fish/config.fish`):
```fish
set -gx PATH $HOME/.local/bin $PATH
```

Then reload: `source ~/.bashrc` or restart your terminal.

---

## 💻 Usage

### Basic Commands

```bash
# Search for packages
eshu search firefox

# Install packages
eshu install hyprland

# View system profile
eshu profile

# Find bloat (Premium)
eshu cleanup
```

### AI Features (Optional)

**ESHU works perfectly without AI!** But if you want AI-powered package ranking:

**Option 1: Ollama (FREE, runs locally)**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
eshu config set-provider ollama
```

**Option 2: Anthropic Claude (best results, paid API)**
```bash
export ANTHROPIC_API_KEY="your-api-key"
eshu config set-provider anthropic
```

---

## 📦 Supported Package Managers

| Manager  | Search | Install | Notes |
|----------|--------|---------|-------|
| pacman   | ✅     | ✅      | Arch Linux official repos |
| yay      | ✅     | ✅      | AUR helper |
| paru     | ✅     | ✅      | AUR helper |
| apt      | ✅     | ✅      | Debian/Ubuntu |
| flatpak  | ✅     | ✅      | Universal apps |
| snap     | ✅     | ✅      | Universal apps |
| cargo    | ✅     | ✅      | Rust packages |
| npm      | ✅     | ✅      | Node.js packages |
| pip      | ✅     | ✅      | Python packages |

---

## 💎 Free vs Premium

### Free Tier
- ✅ Multi-manager package search
- ✅ Basic installation
- ✅ System profiling
- ✅ 10 AI queries/day
- ✅ All package managers

### Premium ($9.99/month)
- ✅ **Everything in Free**
- ✅ **📦 Eshu's Path** - Curated package bundles
- ✅ Unlimited AI queries
- ✅ Automatic snapshots & rollback
- ✅ Community hardware warnings
- ✅ Smart bloat finder
- ✅ Priority support

[**Upgrade to Premium →**](https://eshu-apps.gumroad.com/l/eshu-premium)

---

## 🔧 Troubleshooting

### Command not found

Make sure `~/.local/bin` is in your PATH (see installation instructions above).

### Python version issues

ESHU requires Python 3.9+. Check your version:
```bash
python3 --version
```

On Arch: `sudo pacman -S python python-pip`
On Debian/Ubuntu: `sudo apt install python3 python3-pip`

### Reinstall

```bash
cd eshu-installer
./install-eshu.sh
# Choose 'y' when asked to reinstall
```

### Uninstall

```bash
rm -rf ~/.local/share/eshu
rm ~/.local/bin/eshu
```

---

## 📚 Documentation

- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Command cheat sheet
- **[Architecture](docs/ARCHITECTURE.md)** - How ESHU works
- **[Contributing](docs/CONTRIBUTING.md)** - Help improve ESHU

---

## ❓ FAQ

### Why not just learn the package managers?

**Time.** Learning all package managers takes weeks. ESHU works in 5 minutes.

Plus, even experts forget syntax:
- Is it `apt search` or `apt-cache search`?
- `pacman -Ss` or `pacman -S`?
- `yay -S` or `yay -Ss`?

ESHU unifies everything. One command to rule them all.

### How is this different from Nix?

**Nix** is a whole ecosystem requiring you to adopt Nix package management.

**ESHU** works with your **existing** setup:
- ✓ Uses pacman/apt/yay you already have
- ✓ No system rewrites
- ✓ Just a thin layer on top
- ✓ Install it, use it, done

### Does this work on Debian/Ubuntu?

**Yes!** ESHU works on **any** Linux distro with Python 3.9+:
- Arch/Manjaro/EndeavourOS ✓
- Debian/Ubuntu/Pop!_OS ✓
- Fedora ✓

ESHU detects your distro and uses the appropriate package managers automatically.

### What data is collected?

**Zero.** ESHU is fully offline. No telemetry, no analytics, no phone-home.

With AI features:
- LLM queries are sent to the API you choose (Anthropic/OpenAI/Ollama)
- Only package names and error messages are sent
- No personal data, no usage tracking

Use Ollama for 100% local AI processing if privacy is critical.

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Credits

Built with:
- [Anthropic Claude](https://anthropic.com) - AI intelligence
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting

---

<div align="center">

**ESHU** - One command for every package. 🚀

[GitHub](https://github.com/eshu-apps/eshu-installer) • [Premium](https://eshu-apps.gumroad.com/l/eshu-premium) • [Docs](docs/)

</div>

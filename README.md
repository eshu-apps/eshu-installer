<div align="center">

<img src="assets/horizontal.png" alt="ESHU - Universal Package Manager for Linux" width="800">

### Universal Package Manager for Linux

> **One command for every package. Stop the madness.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0-green.svg)](https://github.com/eshu-apps/eshu-installer/releases)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Website](https://img.shields.io/badge/🌐-eshu--apps.com-blue)](https://eshu-apps.com)

<a href="https://eshuapps.gumroad.com/l/eshu-premium"><img src="https://img.shields.io/badge/Premium-$9.99%2Fmonth-gold.svg?style=for-the-badge" alt="Upgrade to Premium"></a>
<a href="https://gumroad.com/l/eshu-donate"><img src="https://img.shields.io/badge/💝-Donate-ff69b4.svg?style=for-the-badge" alt="Donate"></a>

</div>

---

## 😭 The Problem: Package Manager Hell

> **These are the nightmares we're replacing with ESHU** ⬇️

<details>
<summary><b>❌ NVIDIA Driver Hell</b> (click to expand horror story)</summary>

<br>

```bash
# Spent 3 hours on Reddit...
sudo pacman -S nvidia nvidia-utils
# Breaks Wayland

sudo apt install nvidia-driver-535
# Wrong version for your card

yay -S nvidia-dkms
# Kernel mismatch

# Finally works, then:
sudo pacman -Syu
# System won't boot 💀
```

</details>

<details>
<summary><b>❌ AUR/Pacman Confusion</b></summary>

<br>

```bash
pacman -Ss hyprland
# Not found

yay -Ss hyprland
# Found! But which repo?

# Is it aur/hyprland or extra/hyprland?
# Do I use pacman or yay?
# What about paru?
# *existential crisis*
```

</details>

<details>
<summary><b>❌ Fedora Silverblue Hell</b></summary>

<br>

```bash
# Wait, is this rpm-ostree or dnf?
rpm-ostree install nvidia-driver
# Error: can't layer this package

dnf install nvidia-driver
# Error: read-only filesystem

flatpak install nvidia-driver
# Error: not available

# 2 hours later, still no NVIDIA drivers 😤
```

</details>

---

## ✨ The Solution: ESHU

### NVIDIA Driver Hell
```bash
# Spent 3 hours on Reddit...
sudo pacman -S nvidia nvidia-utils
# Breaks Wayland

sudo apt install nvidia-driver-535
# Wrong version for your card

yay -S nvidia-dkms
# Kernel mismatch

# Finally works, then:
sudo pacman -Syu
# System won't boot 💀
```


```bash
eshu install nvidia

🤖 AI analyzing your system...
✓ Detected: Arch Linux, RTX 3080, Wayland

📦 Installing Complete NVIDIA Setup:
  • nvidia-dkms (for kernel compatibility)
  • nvidia-utils (OpenGL/Vulkan)
  • lib32-nvidia-utils (32-bit support)
  • nvidia-settings (control panel)
  • egl-wayland (Wayland support)

✓ All installed! Wayland configured automatically.
Reboot to activate. ✨
```

```bash
eshu install hyprland

🤖 Found cached bundle (234 uses, 96% success rate)

📦 Complete Wayland Desktop Environment:
  • hyprland (compositor)
  • waybar (status bar)
  • wofi (app launcher)
  • mako (notifications)
  • grim + slurp (screenshots)
  • wl-clipboard (clipboard)
  • All configured to work together!

Install complete bundle? [Y/n] █
```

**One command. No confusion. No broken systems.** 🚀

---

## 🎯 What is ESHU?

**ESHU** unifies **ALL** Linux package managers into one intelligent interface:

<div align="center">

```
┌─────────────────────────────────────────────┐
│           📦 ESHU UNIVERSAL API             │
├─────────────────────────────────────────────┤
│  One command searches:                      │
│  • pacman   • yay      • paru    • apt      │
│  • flatpak  • snap     • cargo   • npm      │
│  • pip      • GitHub repos (NEW!)           │
│                                             │
│  🤖 AI ranks results for YOUR system       │
│  📦 Suggests complete package bundles       │
│  🔧 Auto-fixes errors during installation   │
│  📊 Learns from your usage patterns         │
└─────────────────────────────────────────────┘
```

</div>

**Works on:** Arch • Debian • Ubuntu • Fedora • Any Linux with Python 3.9+

---

## ⚡ Features

### 🔍 **Universal Search**
- Search 9+ package managers + GitHub repos simultaneously
- AI ranks results based on your hardware and distro
- Shows which packages are already installed
- See size, version, and repo info instantly

### 📦 **Eshu's Path - Smart Bundles** *(Premium)*
- AI generates complete package setups
- Cached locally for instant reuse
- Community-driven knowledge base
- **Example:** Install Hyprland → get entire Wayland ecosystem (15 packages)

### 🤖 **AI-Powered Intelligence** *(Optional)*
- Natural language queries: "install a video editor"
- Automatic error diagnosis and fixes
- Hardware compatibility warnings
- Suggests lightweight alternatives on low-RAM systems

### 🔧 **System Maintenance** *(Premium)*
```bash
eshu maintain

🔄 Updating: pacman, yay, flatpak, npm, pip...
✓ 23 packages updated

🧹 Cleaning caches and orphans...
✓ 680MB disk space freed

System is healthy! ✨
```
**One command updates EVERYTHING.** No more update scripts!

### 📊 **Usage Analytics** *(Privacy-Respecting)*
- Track which package managers you use most
- See your most-searched packages
- Monitor install success rates
- **Zero PII collected** - completely anonymous

### 💬 **Interactive Mode**
```bash
eshu install

╔═══════════════════════════════════════╗
║  ESHU - Universal Package Installer   ║
╚═══════════════════════════════════════╝

What would you like to install?
> nvidia drivers for gaming

🤖 AI understanding query...
📦 Found NVIDIA gaming setup bundle...
```

---

## 🚀 Installation

### One-Line Install (Recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/eshu-apps/eshu-installer/main/install-eshu.sh | bash
```

### Manual Install
```bash
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer
./install-eshu.sh
```

**That's it!** The installer:
- ✅ Creates isolated Python environment (no system pollution)
- ✅ Installs dependencies automatically
- ✅ Creates `eshu` command in `~/.local/bin`
- ✅ Runs setup wizard

### 🔄 Updating

Keep eshu up-to-date with the latest features and fixes:

```bash
# One command to update everything
eshu update
```

This will:
- ✅ Check for new updates
- ✅ Download latest code from GitHub
- ✅ Reinstall dependencies automatically
- ✅ Show recent changes

**If update fails, just reinstall:**
```bash
curl -fsSL https://raw.githubusercontent.com/eshu-apps/eshu-installer/main/install-eshu.sh | bash
```

---

## 💻 Quick Start

```bash
# Search for packages
eshu search firefox

# Install packages (single or multiple)
eshu install firefox
eshu install firefox chrome vlc

# Interactive mode (no arguments)
eshu install
eshu search

# System maintenance (Premium)
eshu maintain

# View your usage stats
eshu stats
```

### Add AI Features (Optional)

**ESHU works great without AI!** But for intelligent bundles and error handling:

```bash
# Option 1: Ollama (FREE, runs locally)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
eshu config set-provider ollama

# Option 2: Anthropic Claude (best results, paid API)
export ANTHROPIC_API_KEY="your-key"
eshu config set-provider anthropic
```

**Free tier:** 10 AI queries/day
**Premium:** Unlimited AI + bundles + maintenance → [$9.99/month](https://eshuapps.gumroad.com/l/eshu-premium)

---

## 📦 Supported Package Managers

| Manager | Search | Install | Update | Notes |
|---------|--------|---------|--------|-------|
| pacman | ✅ | ✅ | ✅ | Arch official repos |
| yay | ✅ | ✅ | ✅ | AUR helper |
| paru | ✅ | ✅ | ✅ | AUR helper |
| apt | ✅ | ✅ | ✅ | Debian/Ubuntu |
| flatpak | ✅ | ✅ | ✅ | Universal apps |
| snap | ✅ | ✅ | ✅ | Universal apps |
| cargo | ✅ | ✅ | ✅ | Rust packages |
| npm | ✅ | ✅ | ✅ | Node.js packages |
| pip | ✅ | ✅ | ✅ | Python packages |
| **GitHub** | ✅ | 🚧 | - | **NEW!** Repos with releases |

---

## 💎 Free vs Premium

<div align="center">

| Feature | Free | Premium |
|---------|------|---------|
| Multi-manager search | ✅ | ✅ |
| GitHub repo search | ✅ | ✅ |
| Basic installation | ✅ | ✅ |
| AI queries/day | 10 | ∞ |
| **Eshu's Path Bundles** | Teasers | ✅ |
| **System Maintenance** | ❌ | ✅ |
| **Auto Snapshots** | ❌ | ✅ |
| **Community Warnings** | ❌ | ✅ |
| **Cloud Bundle Sync** | ❌ | ✅ |
| **Priority Support** | ❌ | ✅ |

[**🚀 Upgrade to Premium**](https://eshuapps.gumroad.com/l/eshu-premium) | [💝 Donate](https://gumroad.com/l/eshu-donate)

</div>

---

## 🎯 Real-World Examples

### Example 1: Install Complete Hyprland Setup

```bash
$ eshu install hyprland

🤖 Checking bundle cache...
✓ Found cached bundle (used 234 times, 96% success rate)

📦 Eshu's Path: Complete Hyprland Setup

Includes 15 packages:
  • hyprland (Wayland compositor)
  • waybar (status bar)
  • wofi (app launcher)
  • mako (notifications)
  • grim, slurp (screenshots)
  • wl-clipboard (clipboard utilities)
  • swaylock, swayidle (screen locking)
  • pipewire, wireplumber (audio)
  • brightnessctl (brightness control)

Install complete bundle? [Y/n] y

✓ All 15 packages installed successfully!
✓ Hyprland is ready to use!
```

### Example 2: Fix NVIDIA on Arch

```bash
$ eshu install nvidia

🤖 AI analyzing system...
  • Detected: Arch Linux (rolling)
  • GPU: NVIDIA RTX 3080
  • Kernel: 6.6.7-arch1-1
  • Display: Wayland

⚠️  Community Warning:
   NVIDIA + Wayland on kernel 6.6 may have flickering.
   Workaround available.

📦 Complete NVIDIA Setup Bundle:
  • nvidia-dkms (kernel-independent)
  • nvidia-utils, lib32-nvidia-utils
  • nvidia-settings
  • egl-wayland (Wayland support)

Apply flickering workaround? [Y/n] y

✓ NVIDIA drivers installed
✓ Wayland configured
✓ Workaround applied

Reboot to activate. Run 'nvidia-smi' to verify.
```

### Example 3: System Maintenance (Premium)

```bash
$ eshu maintain

🔧 ESHU System Maintenance

🔄 Updating package managers...
  ✓ pacman: 18 packages updated
  ✓ yay: 5 AUR packages updated
  ✓ flatpak: 3 apps updated
  ✓ npm: 2 global packages updated

🧹 Cleaning caches and orphans...
  ✓ pacman: Removed 520MB cache
  ✓ apt: Removed 2 orphaned packages
  ✓ flatpak: Removed 3 unused runtimes

📊 Summary:
  28 packages updated
  680MB disk space freed
  0 errors

✓ System is healthy! ✨
```

---

## ❓ FAQ

### "Why not just use [package manager]?"

Because **you use multiple package managers**, whether you know it or not:

- System packages (pacman/apt)
- AUR (yay/paru)
- Flatpaks for GUI apps
- npm for Node tools
- pip for Python tools
- cargo for Rust tools

ESHU unifies them all. **One search. One install. Done.**

### "How is this different from Nix/Guix?"

**Nix/Guix** replace your entire package management system.

**ESHU** works **with** your existing setup:
- ✅ Uses the package managers you already have
- ✅ No system rewrites required
- ✅ Install it, use it, done
- ✅ Can be removed without breaking anything

Think of ESHU as a "universal remote" for package managers.

### "What about security/privacy?"

**Analytics:**
- Completely opt-in (enabled by default, easily disabled)
- **Zero personal data** collected (no names, emails, IPs)
- Only tracks package names, managers used, error types
- Stored locally first, cloud sync optional (Premium)
- Disable: `eshu config set analytics_enabled false`

**AI Features:**
- Queries sent to your chosen provider (Anthropic/OpenAI/Ollama)
- Only package names and error messages sent
- Use Ollama for 100% local processing

**Code:**
- Fully open source (MIT license)
- No telemetry or phone-home
- No tracking pixels or analytics scripts

---

## 🗺️ Roadmap

### v0.4.0 (Current)
- [x] Bundle database and caching
- [x] Usage analytics (privacy-respecting)
- [x] System maintenance command
- [x] GitHub repo search
- [x] Interactive CLI mode

### v0.5.0 (Next - Q1 2025)
- [ ] Cloud bundle sync (Premium)
- [ ] Bundle marketplace
- [ ] Smart install source switching
- [ ] Auto-build assistance for GitHub repos
- [ ] GUI interface (Electron or Tauri)

### v1.0.0 (Q2 2025)
- [ ] Plugin system
- [ ] Custom bundle creation
- [ ] Multi-machine sync
- [ ] Enterprise features
- [ ] Production-ready stability

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional package manager support
- More curated Eshu's Path bundles
- Better error handling
- GUI interface
- Documentation improvements

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Credits

Built with:
- [Anthropic Claude](https://anthropic.com) - AI intelligence
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Pydantic](https://pydantic.dev/) - Configuration management

---

## 📚 Documentation

- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Command cheat sheet
- **[Advanced Features](ADVANCED_FEATURES.md)** - Deep dive into v0.4.0 features
- **[Privacy Policy](PRIVACY.md)** - What we collect (and don't)
- **[Architecture](ARCHITECTURE.md)** - How ESHU works

---

## 📞 Support & Contact

- 🌐 **Website**: [eshu-apps.com](https://eshu-apps.com)
- 📧 **Support**: support@eshu-apps.com
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/eshu-apps/eshu-installer/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/eshu-apps/eshu-installer/discussions)
- 💝 **Donate**: [Support the Project](https://gumroad.com/l/eshu-donate)

---

<div align="center">

**ESHU v0.4.0** - One command for every package. 🚀

**Stop juggling package managers. Start using ESHU.**

[Website](https://eshu-apps.com) • [Get Started](https://github.com/eshu-apps/eshu-installer) • [Premium](https://eshuapps.gumroad.com/l/eshu-premium) • [Donate](https://gumroad.com/l/eshu-donate)

---

*Made with ❤️ for the Linux community*

</div>

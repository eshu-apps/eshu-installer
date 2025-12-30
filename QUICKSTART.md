# ESHU Quick Start Guide

## 5-Minute Setup

### 1. Install ESHU

```bash
cd ~/eshu-installer
./install.sh
```

Or manually:

```bash
pip install -e .
```

### 2. Configure LLM Provider

**Option A: Anthropic Claude (Best Quality)**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
eshu config set-provider anthropic
```

**Option B: OpenAI GPT**
```bash
export OPENAI_API_KEY="sk-your-key-here"
eshu config set-provider openai
```

**Option C: Ollama (Free, Local)**
```bash
# Install Ollama first: https://ollama.ai
ollama pull llama3.1:8b
eshu config set-provider ollama
```

### 3. Test It

```bash
# Search for a package
eshu search firefox

# Install something
eshu install neovim
```

## Common Commands

```bash
# Install packages
eshu install hyprland
eshu install "terminal emulator"
eshu install -y package-name          # Auto-confirm

# Search packages
eshu search firefox
eshu search "pdf viewer"

# System info
eshu profile
eshu profile --packages               # Show installed packages
eshu profile --refresh                # Force refresh

# Configuration
eshu config show
eshu config set-key
eshu config set-provider ollama

# Help
eshu --help
eshu install --help
```

## Examples

### Install Hyprland
```bash
$ eshu install hyprland
# AI finds best option, installs it
```

### Search Across All Package Managers
```bash
$ eshu search neovim
# Shows results from pacman, apt, flatpak, snap, cargo, npm, pip
```

### Handle Build Errors Automatically
```bash
$ eshu install some-aur-package
# If build fails, AI suggests fixes and applies them
```

## Configuration

Edit `~/.config/eshu/config.json`:

```json
{
  "llm_provider": "anthropic",
  "package_manager_priority": ["pacman", "yay", "apt"],
  "prefer_native": true,
  "auto_confirm_deps": false
}
```

## Systemd Service (Optional)

Auto-scan system at boot:

```bash
sudo cp systemd/eshu-profiler.* /etc/systemd/system/
sudo systemctl enable --now eshu-profiler.timer
```

## Troubleshooting

### "API key not configured"
```bash
export ANTHROPIC_API_KEY="your-key"
eshu config set-key
```

### "Permission denied"
```bash
sudo mkdir -p /var/cache/eshu
sudo chmod 755 /var/cache/eshu
```

### Package not found
```bash
eshu profile --refresh
eshu search "alternative name"
```

## Tips

1. **Use natural language**: `eshu install "wayland compositor"`
2. **Check before installing**: `eshu search package-name`
3. **Use Ollama for free**: No API costs, runs locally
4. **Enable systemd service**: Faster queries with cached profile

## Next Steps

- Read [DEMO.md](DEMO.md) for detailed examples
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Check [README.md](README.md) for full documentation

---

**ESHU** - One command for all package managers. 🚀

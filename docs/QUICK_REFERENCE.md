# ESHU Quick Reference

## Installation

```bash
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer
./install-eshu.sh
```

## Basic Commands

### Search
```bash
eshu search <package>          # Search all package managers
eshu search --manager pacman <package>  # Search specific manager
eshu search --all <package>    # Show all results with pagination
```

### Install
```bash
eshu install <package>         # Install package
eshu install -y <package>      # Auto-confirm
eshu install --no-snapshot <package>  # Skip snapshot (Premium)
```

### System Info
```bash
eshu profile                   # Show system info
eshu profile --refresh         # Rebuild profile cache
```

### Cleanup (Premium)
```bash
eshu cleanup                   # Show what can be removed
eshu cleanup --execute         # Actually remove packages
```

### Configuration
```bash
eshu config show               # Show current config
eshu config set-provider ollama  # Set LLM provider
eshu config set-key            # Set API key
```

### License (Premium)
```bash
eshu license-cmd status        # Check license status
eshu license-cmd activate <key>  # Activate premium
eshu license-cmd usage         # View usage stats
```

## AI Providers

### Ollama (Free, Local)
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
eshu config set-provider ollama
```

### Anthropic Claude
```bash
export ANTHROPIC_API_KEY="your-key"
eshu config set-provider anthropic
```

### OpenAI
```bash
export OPENAI_API_KEY="your-key"
eshu config set-provider openai
```

## Package Managers

| Command | Manager | Notes |
|---------|---------|-------|
| `pacman` | Arch official | Native packages |
| `yay` | AUR | Community packages |
| `paru` | AUR | Alternative AUR helper |
| `apt` | Debian/Ubuntu | System packages |
| `flatpak` | Universal | Sandboxed apps |
| `snap` | Universal | Canonical's format |
| `cargo` | Rust | Rust crates |
| `npm` | Node.js | JavaScript packages |
| `pip` | Python | Python packages |

## Examples

### Install Hyprland
```bash
eshu install hyprland
# Searches pacman, yay, flatpak, etc.
# Shows best option for your system
```

### Search for Firefox
```bash
eshu search firefox --all
# Shows all available versions
# Navigate with n/p/q
```

### Find Bloat
```bash
eshu cleanup
# Shows orphaned packages
# Shows large unused packages
# Calculates reclaimable space
```

## Troubleshooting

### Command not found
```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Reinstall
```bash
cd eshu-installer
./install-eshu.sh
# Choose 'y' to reinstall
```

### Clear cache
```bash
rm -rf ~/.cache/eshu
eshu profile --refresh
```

## Configuration File

Location: `~/.config/eshu/config.json`

```json
{
  "llm_provider": "ollama",
  "model_name": "llama3.1:8b",
  "temperature": 0.3,
  "package_manager_priority": [
    "pacman",
    "yay",
    "flatpak",
    "snap"
  ]
}
```

## Premium Features

- 📦 **Eshu's Path** - Curated package bundles
- 📸 **Time Machine** - Automatic snapshots
- ⚠️ **Community Warnings** - Hardware compatibility alerts
- 🧹 **Smart Cleanup** - Advanced bloat detection
- 🤖 **Unlimited AI** - No query limits

[Upgrade to Premium →](https://eshuapps.gumroad.com/l/eshu-premium)

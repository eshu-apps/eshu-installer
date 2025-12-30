# 🚀 ESHU Quick Reference Card

**ESHU** - One command for every package. AI-powered universal Linux installer.

---

## 📦 Basic Commands

### **Search**
```bash
eshu search <package>           # Search all package managers
eshu search firefox --all       # Show all results with pagination
```

### **Install**
```bash
eshu install <package>          # AI-powered installation
eshu install <pkg> --no-snapshot  # Skip snapshot creation
```

### **System Info**
```bash
eshu profile                    # View system profile
eshu version                    # Show ESHU version
```

---

## 🧹 Cleanup & Maintenance

### **Find Bloat**
```bash
eshu cleanup                    # Find unused packages (dry run)
eshu cleanup --execute          # Actually remove bloat
eshu cleanup --days 60          # Custom threshold
```

### **Snapshots**
```bash
eshu snapshot list              # View all snapshots
eshu snapshot create            # Create manual snapshot
eshu snapshot restore <id>      # Restore snapshot
eshu snapshot delete <id>       # Delete snapshot
```

---

## ⚙️ Configuration

### **LLM Setup**
```bash
eshu config show                # View current config
eshu config set-provider anthropic  # Use Claude
eshu config set-provider openai     # Use GPT
eshu config set-provider ollama     # Use local LLM
```

### **API Keys**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
```

---

## 🔒 License Management

### **Free Tier**
- Basic features
- 10 AI queries/day
- All package managers

### **Premium ($4.99/month)**
- Unlimited AI queries
- Snapshots & rollback
- Community warnings
- Bloat finder
- Priority support

### **Commands**
```bash
eshu license-cmd status         # Check license
eshu license-cmd activate <key> # Activate premium
eshu license-cmd usage          # View usage stats
```

---

## 🎯 Common Use Cases

### **Install Development Tools**
```bash
eshu install neovim
eshu install "python development tools"
eshu install docker
```

### **Install Desktop Apps**
```bash
eshu install firefox
eshu install "video editor"
eshu install discord
```

### **System Maintenance**
```bash
eshu cleanup                    # Find bloat
eshu snapshot create            # Backup before changes
eshu profile                    # Check system status
```

---

## 🔍 Search Tips

### **Exact Match**
```bash
eshu search firefox             # Finds Firefox browser
```

### **Natural Language**
```bash
eshu install "terminal emulator"
eshu install "screenshot tool"
eshu install "video player"
```

### **View All Results**
```bash
eshu search firefox --all       # Paginated results
# Press 'n' for next, 'p' for previous, '#' to select
```

---

## 🎨 Result Display

### **Columns**
- **Package** - Package name
- **Version** - Version number
- **Manager** - Package manager (pacman, apt, flatpak, etc.)
- **Size** - Installation size
- **OS** - Optimized for (🔷 Arch, 🔴 Debian, 🌐 All)
- **Description** - Package description

### **Indicators**
- ✓ - Already installed
- 🔷 - Arch Linux optimized
- 🔴 - Debian/Ubuntu optimized
- 🌐 - Universal (all distros)

---

## 🛡️ Safety Features

### **Automatic Snapshots**
- Created before each installation
- Keeps last 10 snapshots
- One-click rollback

### **Community Warnings**
- Hardware compatibility checks
- Known issue alerts
- Workaround suggestions

### **Sandbox Recommendations**
- Flatpak for browsers (security)
- Native for dev tools (performance)

---

## 📊 Supported Package Managers

| Manager | Status | Features |
|---------|--------|----------|
| pacman  | ✅ | Native Arch, size info |
| yay     | ✅ | AUR support |
| paru    | ✅ | AUR support |
| apt     | ✅ | Debian/Ubuntu |
| flatpak | ✅ | Sandboxed apps, size info |
| snap    | ✅ | Canonical apps |
| cargo   | ✅ | Rust packages |
| npm     | ✅ | Node.js packages |
| pip     | ✅ | Python packages |

---

## 🔧 Troubleshooting

### **Command Not Found**
```bash
which eshu                      # Check if installed
pip install -e /home/brax/eshu-installer
```

### **No Results Found**
```bash
eshu config show                # Check package managers
# Make sure package managers are installed
```

### **LLM Not Working**
```bash
# Check API key
echo $ANTHROPIC_API_KEY
# Or use free local LLM
eshu config set-provider ollama
```

### **License Issues**
```bash
eshu license-cmd status         # Check status
eshu license-cmd usage          # Check quota
```

---

## 📚 Documentation

- **README.md** - Complete feature documentation
- **QUICKSTART.md** - 5-minute setup guide
- **DEMO.md** - Real-world examples
- **GITHUB_DEPLOYMENT_GUIDE.md** - Launch instructions
- **START_HERE.md** - Quick launch guide

---

## 🌐 Links

- **GitHub:** https://github.com/yourusername/eshu-installer
- **Upgrade:** https://eshu-installer.com/upgrade
- **Docs:** https://github.com/yourusername/eshu-installer/blob/main/README.md
- **Issues:** https://github.com/yourusername/eshu-installer/issues

---

## 💡 Pro Tips

1. **Use `--all` flag** to see all search results
2. **Create snapshots** before major installations
3. **Run cleanup monthly** to free up space
4. **Use natural language** for better AI results
5. **Check community warnings** for hardware-specific issues

---

## 🎉 Quick Start

```bash
# 1. Search for a package
eshu search firefox

# 2. Install it
eshu install firefox

# 3. Check your system
eshu profile

# 4. Find bloat
eshu cleanup

# 5. Create a backup
eshu snapshot create
```

---

**ESHU v0.3.0** - One command for every package. 🚀

*For detailed documentation, see README.md*

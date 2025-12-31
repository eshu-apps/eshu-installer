# ESHU Installation Guide

## Quick Install (Recommended)

### One-Line Install
```bash
curl -fsSL https://raw.githubusercontent.com/eshu-apps/eshu-installer/main/install-eshu.sh | bash
```

### Manual Install
```bash
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer
./install-eshu.sh
```

## What the Installer Does

The installer automatically:
1. ✅ Checks for Python 3.9+ and pip
2. ✅ Creates an isolated virtual environment at `~/.local/share/eshu/venv`
3. ✅ Installs all dependencies
4. ✅ Creates the `eshu` command wrapper at `~/.local/bin/eshu`
5. ✅ Tests the installation

## Post-Installation

### Add to PATH (if needed)

If you see "command not found" after installation, add `~/.local/bin` to your PATH:

**Bash** (`~/.bashrc`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Fish** (`~/.config/fish/config.fish`):
```fish
set -gx PATH $HOME/.local/bin $PATH
```

**Zsh** (`~/.zshrc`):
```zsh
export PATH="$HOME/.local/bin:$PATH"
```

Then reload: `source ~/.bashrc` or restart your terminal.

### Verify Installation

```bash
eshu --help
eshu profile
```

## Manual Installation (Advanced)

If you prefer to install manually:

```bash
# Clone the repository
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer

# Create virtual environment
python3 -m venv ~/.local/share/eshu/venv

# Activate virtual environment
source ~/.local/share/eshu/venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install ESHU in editable mode
pip install -e .

# Create wrapper script
mkdir -p ~/.local/bin
cat > ~/.local/bin/eshu << 'EOF'
#!/usr/bin/env bash
VENV_DIR="$HOME/.local/share/eshu/venv"
source "$VENV_DIR/bin/activate"
exec python -m eshu.cli_enhanced "$@"
EOF

# Make executable
chmod +x ~/.local/bin/eshu

# Test
eshu --help
```

## Troubleshooting

### Python Version Issues

ESHU requires Python 3.9 or higher. Check your version:
```bash
python3 --version
```

**Install Python:**
- **Arch Linux**: `sudo pacman -S python python-pip`
- **Debian/Ubuntu**: `sudo apt install python3 python3-pip python3-venv`
- **Fedora**: `sudo dnf install python3 python3-pip`
- **openSUSE**: `sudo zypper install python3 python3-pip`

### Command Not Found

Make sure `~/.local/bin` is in your PATH (see "Add to PATH" above).

### Permission Errors

Never run the installer with `sudo`. ESHU installs to your home directory and will ask for sudo when needed.

### Reinstall

```bash
cd eshu-installer
./install-eshu.sh
# Choose 'y' when asked to reinstall
```

### Clean Uninstall

```bash
rm -rf ~/.local/share/eshu
rm ~/.local/bin/eshu
```

## Virtual Environment Explained

ESHU uses a Python virtual environment to:
- ✅ Avoid conflicts with system Python packages
- ✅ Keep your system clean
- ✅ Allow easy updates and uninstallation
- ✅ Follow Python best practices

The wrapper script at `~/.local/bin/eshu` automatically activates the virtual environment, so you just run `eshu` like any other command.

## Updating ESHU

```bash
cd eshu-installer
git pull origin main
./install-eshu.sh
# Choose 'y' to reinstall with updates
```

## Alternative: pipx Installation (Not Recommended)

While you *can* use pipx, the custom installer is recommended because:
- It handles the virtual environment setup automatically
- It creates a proper wrapper script
- It tests the installation
- It provides better error messages

If you still want to use pipx:
```bash
pipx install git+https://github.com/eshu-apps/eshu-installer.git
```

## Getting Help

- **Documentation**: https://github.com/eshu-apps/eshu-installer
- **Issues**: https://github.com/eshu-apps/eshu-installer/issues
- **Premium Support**: https://eshu-apps.gumroad.com/l/eshu-premium

# Installation Methods

ESHU offers multiple installation methods to suit different security preferences and use cases.

## Method 1: Quick Install (curl | bash)

**Best for:** Quick testing and development

```bash
curl -sSL https://raw.githubusercontent.com/eshu-apps/eshu-installer/main/install-eshu.sh | bash
```

**Security Note:** This method is convenient but requires trusting the installation script. For production use, we recommend using pre-built packages or building from source.

## Method 2: Pre-built Packages (Recommended for Production)

**Best for:** Production systems and security-conscious users

### Debian/Ubuntu (.deb)

```bash
# Download latest release
wget https://github.com/eshu-apps/eshu-installer/releases/latest/download/eshu.deb

# Verify checksum (optional but recommended)
wget https://github.com/eshu-apps/eshu-installer/releases/latest/download/eshu.deb.sha256
sha256sum -c eshu.deb.sha256

# Install
sudo dpkg -i eshu.deb
sudo apt-get install -f  # Fix dependencies if needed
```

### Fedora/RHEL/CentOS (.rpm)

```bash
# Download latest release
wget https://github.com/eshu-apps/eshu-installer/releases/latest/download/eshu.rpm

# Verify checksum (optional but recommended)
wget https://github.com/eshu-apps/eshu-installer/releases/latest/download/eshu.rpm.sha256
sha256sum -c eshu.rpm.sha256

# Install
sudo dnf install eshu.rpm
# or on older systems:
sudo yum install eshu.rpm
```

### Arch Linux (AUR)

```bash
# Using yay
yay -S eshu

# Using paru
paru -S eshu

# Manual from AUR
git clone https://aur.archlinux.org/eshu.git
cd eshu
makepkg -si
```

## Method 3: From Source

**Best for:** Developers and auditing the code

```bash
# Clone repository
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer

# Inspect the code (recommended!)
cat install-eshu.sh
ls -la src/

# Install dependencies
pip install -r requirements.txt

# Install
pip install -e .

# Or build wheel
python -m build
pip install dist/*.whl
```

## Method 4: Python Package (PyPI)

**Best for:** Python developers and virtual environments

```bash
# Install from PyPI
pip install eshu

# Or in a virtual environment
python -m venv eshu-env
source eshu-env/bin/activate
pip install eshu
```

## Verification

### Verify Installation

```bash
# Check version
eshu --version

# Check installation
which eshu

# Run system check
eshu status
```

### Verify Package Signatures (For .deb/.rpm)

All releases are signed with our GPG key.

```bash
# Import GPG key
wget -O- https://eshu-apps.com/gpg-key.asc | gpg --import

# Verify signature
gpg --verify eshu.deb.sig eshu.deb
```

## Security Best Practices

1. **Always verify checksums** for downloaded packages
2. **Inspect installation scripts** before running them
3. **Use package managers** when possible (apt, dnf, pacman)
4. **Check GitHub releases** for version history
5. **Review the source code** - it's open source!

## Uninstallation

### If installed via package manager:

```bash
# Debian/Ubuntu
sudo apt remove eshu

# Fedora/RHEL
sudo dnf remove eshu

# Arch
sudo pacman -R eshu
```

### If installed via pip:

```bash
pip uninstall eshu
```

### Clean up cache and config:

```bash
rm -rf ~/.cache/eshu
rm -rf ~/.config/eshu
```

## Updating

### Package manager:

```bash
# Debian/Ubuntu
sudo apt update && sudo apt upgrade eshu

# Fedora/RHEL
sudo dnf update eshu

# Arch
sudo pacman -Syu eshu
```

### pip:

```bash
pip install --upgrade eshu
```

## Troubleshooting

### Permission denied

If you get permission errors:
```bash
# Make sure you have sudo access
sudo eshu status

# Or install in user directory
pip install --user eshu
```

### Command not found

If `eshu` is not found after installation:
```bash
# Add to PATH (for pip --user installs)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Dependency issues

If you have dependency conflicts:
```bash
# Use a virtual environment
python -m venv eshu-env
source eshu-env/bin/activate
pip install eshu
```

## Getting Help

- 📖 Documentation: https://github.com/eshu-apps/eshu-installer
- 🐛 Issues: https://github.com/eshu-apps/eshu-installer/issues
- 💬 Discussions: https://github.com/eshu-apps/eshu-installer/discussions
- 📧 Email: support@eshu-apps.com

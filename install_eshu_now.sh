#!/bin/bash
# Quick installer for Eshu on Arch Linux
# Handles pipx installation and Eshu setup

set -e

echo "🚀 Installing ESHU on your system..."
echo ""

# Check if pipx is installed
if ! command -v pipx &> /dev/null; then
    echo "📦 Installing python-pipx..."
    sudo pacman -S --noconfirm python-pipx
    echo "✅ pipx installed"
    echo ""
fi

# Ensure pipx is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "⚠️  Adding ~/.local/bin to PATH for this session..."
    export PATH="$HOME/.local/bin:$PATH"
    echo ""
fi

# Install Eshu with pipx
echo "📦 Installing ESHU with pipx..."
pipx install -e /home/hermes/Templates/eshu-installer

echo ""
echo "✅ ESHU installed successfully!"
echo ""

# Test installation
echo "🧪 Testing installation..."
eshu --version 2>/dev/null || eshu --help | head -5

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 ESHU is ready to use!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Try these commands:"
echo "  eshu --help"
echo "  eshu profile"
echo "  eshu search firefox"
echo "  eshu license-cmd status"
echo ""
echo "To test premium features:"
echo "  eshu snapshot list    ← Should show premium prompt"
echo "  eshu cleanup          ← Should show premium prompt"
echo ""
echo "⚠️  IMPORTANT: Add this to your ~/.bashrc or ~/.zshrc:"
echo '    export PATH="$HOME/.local/bin:$PATH"'
echo ""

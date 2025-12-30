#!/bin/bash
# ESHU Installer Script

set -e

echo "🚀 Installing ESHU - AI-Driven Universal Package Installer"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "Install it with: sudo pacman -S python (Arch) or sudo apt install python3 (Debian/Ubuntu)"
    exit 1
fi

# Check for pip
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not installed"
    echo "Install it with: sudo pacman -S python-pip (Arch) or sudo apt install python3-pip (Debian/Ubuntu)"
    exit 1
fi

# Determine pip command
PIP_CMD="pip3"
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
fi

# Install ESHU
echo "📦 Installing ESHU package..."
$PIP_CMD install --user -e .

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "⚠️  Warning: ~/.local/bin is not in your PATH"
    echo "Add this to your shell configuration (~/.bashrc, ~/.zshrc, or ~/.config/fish/config.fish):"
    echo ""
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

# Prompt for LLM configuration
echo ""
echo "🤖 LLM Configuration"
echo "ESHU requires an LLM provider for intelligent package management."
echo ""
echo "Choose a provider:"
echo "  1) Anthropic Claude (recommended, requires API key)"
echo "  2) OpenAI GPT (requires API key)"
echo "  3) Ollama (local, free, requires Ollama installation)"
echo "  4) Skip for now"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        read -p "Enter Anthropic API key: " api_key
        export ANTHROPIC_API_KEY="$api_key"
        ~/.local/bin/eshu config set-provider anthropic
        ~/.local/bin/eshu config set-key "$api_key"
        echo "✓ Anthropic configured"
        ;;
    2)
        read -p "Enter OpenAI API key: " api_key
        export OPENAI_API_KEY="$api_key"
        ~/.local/bin/eshu config set-provider openai
        ~/.local/bin/eshu config set-key "$api_key"
        echo "✓ OpenAI configured"
        ;;
    3)
        if ! command -v ollama &> /dev/null; then
            echo "⚠️  Ollama not found. Install from: https://ollama.ai"
            echo "After installing Ollama, run: eshu config set-provider ollama"
        else
            ~/.local/bin/eshu config set-provider ollama
            echo "✓ Ollama configured"
        fi
        ;;
    4)
        echo "⚠️  Skipping LLM configuration. Run 'eshu config set-provider' later."
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

# Offer to install systemd service
echo ""
read -p "Install systemd service for automatic system profiling? [y/N]: " install_service

if [[ $install_service =~ ^[Yy]$ ]]; then
    sudo cp systemd/eshu-profiler.service /etc/systemd/system/
    sudo cp systemd/eshu-profiler.timer /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable --now eshu-profiler.timer
    echo "✓ Systemd service installed and enabled"
fi

# Create cache directory
sudo mkdir -p /var/cache/eshu
sudo chmod 755 /var/cache/eshu

echo ""
echo "✅ ESHU installation complete!"
echo ""
echo "Try it out:"
echo "  eshu install hyprland"
echo "  eshu search firefox"
echo "  eshu profile"
echo ""
echo "For help: eshu --help"

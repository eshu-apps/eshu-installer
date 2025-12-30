#!/bin/bash
# ESHU Post-Installation Setup Wizard
# Run this after installing Eshu to configure LLM and systemd service

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 ESHU Setup Wizard"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Let's configure ESHU for optimal performance!"
echo ""

# Check if eshu is installed
if ! command -v eshu &> /dev/null; then
    echo "❌ Error: eshu command not found"
    echo ""
    echo "Please install Eshu first:"
    echo "  cd /home/hermes/Templates/eshu-installer"
    echo "  ./fix_and_install.sh"
    exit 1
fi

# Show current status
echo "📋 Current Status:"
eshu license-cmd status 2>/dev/null || echo "License: Free Tier"
echo ""

# LLM Configuration
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 Step 1: LLM Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "ESHU uses AI to provide intelligent package recommendations."
echo "Choose your LLM provider:"
echo ""
echo "  1) Anthropic Claude (recommended, requires API key)"
echo "     Get free key at: https://console.anthropic.com/"
echo ""
echo "  2) OpenAI GPT (requires API key)"
echo "     Get key at: https://platform.openai.com/api-keys"
echo ""
echo "  3) Ollama (local, free, requires Ollama installation)"
echo "     Install from: https://ollama.ai"
echo ""
echo "  4) Skip for now (basic search only, no AI features)"
echo ""
read -p "Enter choice [1-4]: " llm_choice

case $llm_choice in
    1)
        echo ""
        echo "📝 Anthropic Claude Setup"
        echo ""
        echo "Get your API key from: https://console.anthropic.com/"
        echo "(Free tier: 5000 tokens/month)"
        echo ""
        read -p "Enter your Anthropic API key: " api_key

        if [[ -z "$api_key" ]]; then
            echo "⚠️  No key entered, skipping..."
        else
            export ANTHROPIC_API_KEY="$api_key"
            eshu config set-provider anthropic
            eshu config set-key "$api_key"
            echo "✅ Anthropic Claude configured!"
        fi
        ;;
    2)
        echo ""
        echo "📝 OpenAI GPT Setup"
        echo ""
        echo "Get your API key from: https://platform.openai.com/api-keys"
        echo ""
        read -p "Enter your OpenAI API key: " api_key

        if [[ -z "$api_key" ]]; then
            echo "⚠️  No key entered, skipping..."
        else
            export OPENAI_API_KEY="$api_key"
            eshu config set-provider openai
            eshu config set-key "$api_key"
            echo "✅ OpenAI GPT configured!"
        fi
        ;;
    3)
        echo ""
        if ! command -v ollama &> /dev/null; then
            echo "⚠️  Ollama not found!"
            echo ""
            echo "Install Ollama:"
            echo "  1. Visit: https://ollama.ai"
            echo "  2. Download and install"
            echo "  3. Run: ollama pull llama3.1:8b"
            echo "  4. Run this setup again"
            echo ""
        else
            eshu config set-provider ollama
            echo "✅ Ollama configured!"
            echo ""
            echo "💡 Make sure you've pulled a model:"
            echo "   ollama pull llama3.1:8b"
        fi
        ;;
    4)
        echo ""
        echo "⏩ Skipping LLM configuration"
        echo ""
        echo "You can set it up later with:"
        echo "  eshu config set-provider <anthropic|openai|ollama>"
        ;;
    *)
        echo "Invalid choice, skipping..."
        ;;
esac

echo ""

# Systemd Service
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚙️  Step 2: System Profiling Service (Optional)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Install systemd service for automatic system profiling?"
echo ""
echo "Benefits:"
echo "  ✅ Faster package searches (pre-cached system info)"
echo "  ✅ Automatic updates on boot"
echo "  ✅ Tracks package changes"
echo ""
echo "Note: Requires sudo for systemd service installation"
echo ""
read -p "Install systemd service? [y/N]: " install_service

if [[ $install_service =~ ^[Yy]$ ]]; then
    echo ""
    echo "📦 Installing systemd service..."

    SERVICE_DIR="/home/hermes/Templates/eshu-installer/systemd"

    if [[ ! -f "$SERVICE_DIR/eshu-profiler.service" ]]; then
        echo "❌ Service files not found in: $SERVICE_DIR"
    else
        sudo cp "$SERVICE_DIR/eshu-profiler.service" /etc/systemd/system/
        sudo cp "$SERVICE_DIR/eshu-profiler.timer" /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable --now eshu-profiler.timer
        echo "✅ Systemd service installed and enabled!"
        echo ""
        echo "Check status: sudo systemctl status eshu-profiler.timer"
    fi
else
    echo "⏩ Skipping systemd service installation"
fi

echo ""

# Show final status
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 ESHU is ready to use!"
echo ""
echo "Try these commands:"
echo "  eshu search firefox       # Search for packages"
echo "  eshu install hyprland     # Install with AI assistance"
echo "  eshu profile              # View system information"
echo "  eshu license-cmd status   # Check license status"
echo ""
echo "Premium features (upgrade to unlock):"
echo "  eshu snapshot list        # System snapshots & rollback"
echo "  eshu cleanup              # Find and remove bloat"
echo ""
echo "Configuration:"
echo "  eshu config show          # View current config"
echo "  eshu --help               # Full command list"
echo ""
echo "Need help? Check: https://github.com/eshu-apps/eshu-installer"
echo ""

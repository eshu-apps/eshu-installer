#!/bin/bash
# Fix installation issues and install Eshu properly

set -e

echo "🔧 Fixing Eshu installation issues..."
echo ""

# Clean up root-owned build artifacts
echo "1. Cleaning up build artifacts (requires sudo)..."
sudo rm -rf src/*.egg-info build/ dist/ *.egg-info 2>/dev/null || true
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "   ✅ Build artifacts cleaned"
echo ""

# Show what we fixed
echo "2. Fixed dependencies in pyproject.toml:"
echo "   ✅ Added psutil>=5.9.0 (was missing - caused import errors)"
echo ""

# Remove any failed pipx installations
echo "3. Cleaning previous pipx attempts..."
pipx uninstall eshu-installer 2>/dev/null || true
echo "   ✅ Cleaned"
echo ""

# Install with pipx
echo "4. Installing Eshu with pipx..."
pipx install -e /home/hermes/Templates/eshu-installer

echo ""
echo "5. Verifying installation..."

# Check if eshu is available
if command -v eshu &> /dev/null; then
    echo "   ✅ eshu command is available!"
    echo ""

    # Show version
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    eshu --help | head -10
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🎉 ESHU IS INSTALLED!"
    echo ""

    # Ask if user wants to run setup wizard
    read -p "Run setup wizard to configure LLM and systemd service? [Y/n]: " run_setup

    if [[ "$run_setup" =~ ^[Yy]?$ ]] || [[ -z "$run_setup" ]]; then
        echo ""
        eshu setup
    else
        echo ""
        echo "⏩ Skipping setup. Run 'eshu setup' anytime to configure."
        echo ""
        echo "Test it:"
        echo "  eshu license-cmd status    ← Check free tier status"
        echo "  eshu snapshot list         ← Should prompt for Premium"
        echo "  eshu cleanup               ← Should prompt for Premium"
        echo "  eshu search firefox        ← Should work (free tier)"
        echo ""
    fi
else
    echo "   ⚠️  eshu not in PATH"
    echo ""
    echo "Add to your ~/.bashrc or ~/.zshrc:"
    echo '   export PATH="$HOME/.local/bin:$PATH"'
    echo ""
    echo "Then run: source ~/.bashrc  (or source ~/.zshrc)"
fi

#!/bin/bash
# Quick update script for Eshu - reinstalls with latest changes

echo "🔄 Updating ESHU to latest version..."
echo ""

# Uninstall old version
echo "1. Removing old version..."
pipx uninstall eshu-installer 2>/dev/null || echo "   (No previous installation found)"

# Reinstall
echo ""
echo "2. Installing latest version..."
pipx install -e /home/hermes/Templates/eshu-installer

echo ""
echo "✅ ESHU updated!"
echo ""

# Show new help with setup command
echo "📋 New commands available:"
eshu --help | grep -E "setup|Commands" -A 10

echo ""
echo "🎉 Try the new setup wizard:"
echo "   eshu setup"
echo ""

#!/bin/bash
# ESHU Installer Demo Recording Script
# This automates a screen recording showing off ESHU's best features

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Install required tools if not present
if ! command -v asciinema &> /dev/null; then
    echo -e "${YELLOW}Installing asciinema for terminal recording...${NC}"
    sudo pacman -S asciinema --noconfirm || sudo apt install asciinema -y
fi

if ! command -v expect &> /dev/null; then
    echo -e "${YELLOW}Installing expect for automation...${NC}"
    sudo pacman -S expect --noconfirm || sudo apt install expect -y
fi

# Create the demo script
cat > /tmp/eshu-demo.exp << 'EOF'
#!/usr/bin/expect -f

set timeout -1
set send_human {0.05 0.1 0.5 0.01 0.2}

# Start recording
spawn asciinema rec --overwrite /tmp/eshu-demo.cast

# Wait for shell prompt
sleep 2

# === SCENE 1: Welcome & Quick Search (FREE) ===
send -h "# Welcome to ESHU - The Universal Package Installer\r"
sleep 2
send -h "# Let's search for Firefox across ALL package managers\r"
sleep 1
send -h "eshu search firefox\r"
sleep 5

# === SCENE 2: AI-Powered Natural Language (FREE with 10/day limit) ===
send -h "\r\r"
send -h "# Ask in plain English - AI understands what you want!\r"
sleep 1
send -h "eshu chat install a video editor\r"
sleep 8

# === SCENE 3: Ghost Mode - Try Before Installing (FREE!) ===
send -h "\r\r"
send -h "# 👻 Ghost Mode: Try packages without installing!\r"
sleep 1
send -h "eshu try gimp\r"
sleep 3
send -h "# Ghost Mode creates isolated environment\r"
sleep 2
send -h "# Test the app, then keep it or delete it!\r"
sleep 2
send -h "exit\r"
sleep 2

# === SCENE 4: System Profile (FREE) ===
send -h "\r\r"
send -h "# Check your system profile\r"
sleep 1
send -h "eshu profile\r"
sleep 4

# === SCENE 5: Premium Features Preview ===
send -h "\r\r"
send -h "# 💎 PREMIUM FEATURES:\r"
sleep 1
send -h "# • Eshu's Path - Curated package bundles (gaming, dev, media)\r"
sleep 2
send -h "eshu path show gaming\r"
sleep 4

send -h "\r\r"
send -h "# • Time Machine - Snapshot & rollback broken installs\r"
sleep 2
send -h "eshu snapshot create before-upgrade\r"
sleep 3

send -h "\r\r"
send -h "# • Smart Bloat Analyzer - Find & remove junk\r"
sleep 2
send -h "eshu bloat\r"
sleep 4

send -h "\r\r"
send -h "# • Unlimited AI Queries - No daily limits!\r"
sleep 2
send -h "# FREE: 10 AI queries/day | PREMIUM: Unlimited\r"
sleep 3

# === FINALE ===
send -h "\r\r"
send -h "# Get ESHU: paru -S eshu-installer\r"
sleep 2
send -h "# Visit: https://eshu-apps.com\r"
sleep 2
send -h "\r"

# End recording
send "\x04"
sleep 2

EOF

chmod +x /tmp/eshu-demo.exp

# Run the demo
echo -e "${GREEN}Starting ESHU demo recording...${NC}"
echo -e "${BLUE}The demo will run automatically and create: /tmp/eshu-demo.cast${NC}"
echo ""

/tmp/eshu-demo.exp

# Convert to GIF (optional, requires agg or asciinema-player)
if command -v agg &> /dev/null; then
    echo -e "${GREEN}Converting to GIF...${NC}"
    agg /tmp/eshu-demo.cast /tmp/eshu-demo.gif --speed 1.5
    echo -e "${GREEN}GIF created: /tmp/eshu-demo.gif${NC}"
fi

# Upload to asciinema (optional)
echo -e "${YELLOW}Upload recording to asciinema.org? (y/n)${NC}"
read -r response
if [[ "$response" == "y" ]]; then
    asciinema upload /tmp/eshu-demo.cast
fi

echo -e "${GREEN}Demo complete!${NC}"
echo -e "${BLUE}Recording saved to: /tmp/eshu-demo.cast${NC}"
echo -e "${BLUE}View with: asciinema play /tmp/eshu-demo.cast${NC}"

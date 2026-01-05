#!/bin/bash
# ESHU v0.4.0 Marketing Campaign - Automated Launch Script
# Run: ./marketing/launch_campaign.sh

set -e

REPO_URL="https://github.com/eshu-apps/eshu-installer"
PREMIUM_URL="https://eshu-apps.gumroad.com/l/eshu-premium"
VERSION="0.4.0"

echo "═══════════════════════════════════════════════════════════"
echo "  ESHU v${VERSION} - Marketing Campaign Launcher"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if credentials exist
if [ ! -f marketing/credentials.env ]; then
    echo "⚠️  Creating credentials template..."
    cat > marketing/credentials.env << 'EOF'
# Social Media Credentials (fill these in)
REDDIT_USERNAME=""
REDDIT_PASSWORD=""
REDDIT_CLIENT_ID=""
REDDIT_CLIENT_SECRET=""

TWITTER_API_KEY=""
TWITTER_API_SECRET=""
TWITTER_ACCESS_TOKEN=""
TWITTER_ACCESS_SECRET=""

MASTODON_INSTANCE="https://fosstodon.org"
MASTODON_ACCESS_TOKEN=""

HACKERNEWS_USERNAME=""
HACKERNEWS_PASSWORD=""

# Email for blog submissions
CONTACT_EMAIL=""
EOF
    echo "✓ Created marketing/credentials.env"
    echo ""
    echo "📝 Please edit marketing/credentials.env and add your credentials"
    echo "   Then run this script again."
    exit 0
fi

source marketing/credentials.env

# Menu
echo "Choose campaign to run:"
echo ""
echo "  1. Reddit Campaign (r/linux, r/archlinux, r/selfhosted, etc.)"
echo "  2. Hacker News Submission"
echo "  3. Twitter/X Thread"
echo "  4. Mastodon Thread"
echo "  5. Submit to Package Repos (AUR, brew, etc.)"
echo "  6. Blog/Media Outreach"
echo "  7. Full Launch (ALL OF THE ABOVE)"
echo ""
read -p "Choice [1-7]: " choice

case $choice in
    1) ./marketing/reddit_campaign.py ;;
    2) ./marketing/hackernews_submit.py ;;
    3) ./marketing/twitter_campaign.py ;;
    4) ./marketing/mastodon_campaign.py ;;
    5) ./marketing/repo_submissions.sh ;;
    6) ./marketing/media_outreach.py ;;
    7)
        echo "🚀 FULL LAUNCH INITIATED"
        ./marketing/reddit_campaign.py
        ./marketing/hackernews_submit.py
        ./marketing/twitter_campaign.py
        ./marketing/mastodon_campaign.py
        ./marketing/repo_submissions.sh
        ./marketing/media_outreach.py
        echo "✓ Full campaign complete!"
        ;;
    *) echo "Invalid choice"; exit 1 ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Campaign Complete!"
echo "═══════════════════════════════════════════════════════════"

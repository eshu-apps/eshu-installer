#!/bin/bash
# Quick script to update payment URLs after setting up Gumroad

echo "🔧 ESHU Payment URL Updater"
echo "=========================="
echo ""

# Prompt for Gumroad URL
read -p "Enter your Gumroad product URL (e.g., gumroad.com/l/eshu-premium): " GUMROAD_URL

# Validate input
if [[ -z "$GUMROAD_URL" ]]; then
    echo "❌ Error: URL cannot be empty"
    exit 1
fi

# Add https:// if not present
if [[ ! "$GUMROAD_URL" =~ ^https?:// ]]; then
    GUMROAD_URL="https://$GUMROAD_URL"
fi

echo ""
echo "📝 Updating files with: $GUMROAD_URL"
echo ""

# Update license_manager.py
echo "Updating src/eshu/license_manager.py..."
sed -i "s|https://your-payment-page.com/eshu-premium|$GUMROAD_URL|g" src/eshu/license_manager.py

# Update setup.py
echo "Updating setup.py..."
sed -i "s|https://eshu-installer.com/upgrade|$GUMROAD_URL|g" setup.py

# Update pyproject.toml
echo "Updating pyproject.toml..."
sed -i "s|https://eshu-installer.com/upgrade|$GUMROAD_URL|g" pyproject.toml

echo ""
echo "✅ All files updated!"
echo ""
echo "📋 Changed files:"
git diff --name-only

echo ""
echo "🔍 Preview changes:"
echo ""
echo "--- license_manager.py ---"
grep -n "get_upgrade_url" -A 3 src/eshu/license_manager.py | grep "return"
echo ""
echo "--- setup.py ---"
grep "Upgrade to Premium" setup.py
echo ""
echo "--- pyproject.toml ---"
grep "Upgrade to Premium" pyproject.toml

echo ""
read -p "✓ Commit these changes? [Y/n]: " COMMIT

if [[ "$COMMIT" =~ ^[Yy]$ ]] || [[ -z "$COMMIT" ]]; then
    git add src/eshu/license_manager.py setup.py pyproject.toml
    git commit -m "Add Gumroad payment integration

- Updated upgrade URLs to: $GUMROAD_URL
- Users can now purchase ESHU Premium subscriptions
- Revenue-ready for launch 💰"

    echo ""
    echo "✅ Changes committed!"
    echo ""
    echo "📤 Ready to push to GitHub with:"
    echo "   git push origin master"
else
    echo ""
    echo "⏸️  Changes staged but not committed"
    echo "   Review with: git diff"
    echo "   Commit with: git commit -m 'Add payment integration'"
fi

echo ""
echo "🎉 Payment integration complete!"
echo ""

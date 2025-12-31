#!/usr/bin/env bash
#
# Cleanup script to remove unnecessary files before GitHub push
#

set -e

echo "🧹 Cleaning up ESHU repository..."

# Remove old markdown documentation files
echo "Removing old documentation files..."
rm -f AI_INTEGRATION_GUIDE.md
rm -f AI_POWERED_BUNDLES_REAL.md
rm -f ARCHITECTURE.md
rm -f CRITICAL_HANG_FIX.md
rm -f DEMO.md
rm -f DEPLOYMENT_INSTRUCTIONS.md
rm -f ESHU_PATH_INSTALLATION_FIX.md
rm -f ESHU_QUICK_REFERENCE.md
rm -f ESHUS_PATH_FEATURE.md
rm -f FREEMIUM_SETUP_GUIDE.md
rm -f GITHUB_DEPLOYMENT_GUIDE.md
rm -f GUMROAD_CONTENT_PAGE.md
rm -f GUMROAD_LICENSE_FIX.md
rm -f GUMROAD_SETUP_GUIDE.md
rm -f LAUNCH_POSTS.md
rm -f NEXT_STEPS.md
rm -f PERFORMANCE_ANALYSIS.md
rm -f PERFORMANCE_IMPROVEMENTS_IMPLEMENTED.md
rm -f QUICK_FIX.md
rm -f QUICKSTART.md
rm -f SETUP_PAYMENT_NOW.md
rm -f START_HERE.md

# Remove old installation scripts (keep only install-eshu.sh)
echo "Removing old installation scripts..."
rm -f fix_and_install.sh
rm -f install_eshu_now.sh
rm -f install.sh
rm -f setup_eshu.sh
rm -f update_eshu.sh
rm -f update_payment_url.sh

# Remove test files
echo "Removing test files..."
rm -f test_gumroad_license.py

# Remove build artifacts
echo "Removing build artifacts..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
rm -rf src/*.egg-info/

# Remove any zip files
echo "Removing zip files..."
rm -f *.zip

echo "✓ Cleanup complete!"
echo ""
echo "Repository is now clean and ready for GitHub."
echo "Files kept:"
echo "  - README.md (new clean version)"
echo "  - install-eshu.sh (user-friendly installer)"
echo "  - docs/ (organized documentation)"
echo "  - src/ (source code)"
echo "  - pyproject.toml, setup.py (build files)"
echo "  - LICENSE, .gitignore"

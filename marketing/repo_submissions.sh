#!/bin/bash
# Submit ESHU to package repositories

echo "═══════════════════════════════════════════════════════════"
echo "  ESHU Package Repository Submissions"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. AUR (Arch User Repository)
echo "📦 1. AUR Submission"
echo "   Manual steps:"
echo "   1. Create PKGBUILD:"
echo "      cd /tmp && git clone ssh://aur@aur.archlinux.org/eshu.git"
echo "      # Add PKGBUILD (template in marketing/pkgbuild/PKGBUILD)"
echo "      makepkg --printsrcinfo > .SRCINFO"
echo "      git add PKGBUILD .SRCINFO"
echo "      git commit -m 'Initial commit: ESHU v0.4.0'"
echo "      git push"
echo ""

# 2. Homebrew
echo "📦 2. Homebrew (macOS/Linux)"
echo "   Fork: https://github.com/Homebrew/homebrew-core"
echo "   Create formula: Formula/eshu.rb"
echo "   PR: https://github.com/Homebrew/homebrew-core/pulls"
echo ""

# 3. Snapcraft
echo "📦 3. Snapcraft"
echo "   Already have snapcraft.yaml"
echo "   Run: snapcraft"
echo "   Upload: snapcraft upload eshu_0.4.0_amd64.snap --release=stable"
echo ""

# 4. PyPI
echo "📦 4. PyPI (Python Package Index)"
echo "   Run:"
echo "     python3 -m build"
echo "     python3 -m twine upload dist/*"
echo ""

# 5. Flathub
echo "📦 5. Flathub"
echo "   Fork: https://github.com/flathub/flathub"
echo "   Create: com.eshu.installer.yml"
echo "   PR: Submit to Flathub"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "  Templates available in marketing/pkgbuild/"
echo "═══════════════════════════════════════════════════════════"

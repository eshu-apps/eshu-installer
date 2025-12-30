# Gumroad Setup Guide for ESHU Premium

This guide provides plug-and-play text for setting up ESHU Premium on Gumroad.

---

## Product Details

### Product Name
```
ESHU Premium - AI-Powered Linux Package Installer
```

### Short Description (160 characters max)
```
One command for every package. AI-powered universal Linux installer with curated bundles, snapshots, and unlimited queries. $9.99/month.
```

### Product URL Slug
```
eshu-premium
```

**Your Gumroad URL will be:** `https://eshu-apps.gumroad.com/l/eshu-premium`

---

## Full Product Description

### Main Description (Copy this into Gumroad)

```markdown
# ESHU Premium - The Ultimate Linux Package Manager

**One command for every package. AI-powered universal installer that just works.**

ESHU is an intelligent package installer that unifies ALL Linux package managers under a single natural language interface. No more remembering whether to use `pacman`, `apt`, `yay`, `cargo`, `npm`, or any other package manager - just tell ESHU what you want.

---

## What's Included in Premium?

### 📦 Eshu's Path - Curated Package Bundles (NEW!)
The killer feature that saves you HOURS:

- **Installing Hyprland?** Get the complete Wayland ecosystem (15 packages) in one command
- **NVIDIA drivers?** Get the full proprietary stack automatically
- **Rust development?** Get the complete toolchain
- **10+ curated paths** for common setups

**No more researching what packages you need. No more missing dependencies. No more broken setups.**

### 🤖 Unlimited AI Queries
- **Free tier:** 10 AI queries/day
- **Premium:** Unlimited intelligent recommendations
- Natural language package search
- Smart error analysis and auto-fixing

### 📸 Time Machine - System Snapshots
- Automatic snapshots before every installation
- One-click rollback if something breaks
- Never worry about breaking your system again
- Supports Timeshift and Btrfs

### 🧹 Smart Bloat Analyzer
- Find and remove orphaned packages
- Detect duplicate installations across package managers
- Identify large unused packages
- Reclaim gigabytes of disk space

### ⚠️ Community Hardware Warnings
- Hardware-specific compatibility alerts
- Known issue detection before installation
- Automatic workaround suggestions
- Learn from the community's experience

### 💡 Lightweight Alternatives
- AI suggests lighter packages when you're low on RAM
- Optimized recommendations for your system specs
- Perfect for older hardware or minimal setups

### 🎯 Priority Support
- 24-hour response time
- Direct access to developers
- Feature requests prioritized
- Help with complex setups

---

## Why ESHU Premium?

### Before ESHU:
```bash
# You want Hyprland...
pacman -S hyprland  # OK, installed
hyprctl  # ERROR: no terminal!
# *searches Google for "wayland terminal"*
pacman -S kitty
# *launches Hyprland, can't open apps*
# *searches for "wayland launcher"*
pacman -S wofi
# *no notifications*
# *no screenshots*
# ... 2 hours later, still missing things
```

### With ESHU Premium:
```bash
eshu install hyprland

📦 Eshu's Path Available!
Complete Hyprland Setup

Includes 15 packages: hyprland, kitty, wofi, waybar,
mako, grim, slurp, wl-clipboard, swaylock, swayidle,
xdg-desktop-portal-hyprland, polkit-gnome, pipewire,
wireplumber, brightnessctl

Install complete bundle? [Y/n] y

✅ Done! Complete working setup in one command.
```

**That's the power of Eshu's Path.**

---

## Perfect For:

✅ **Arch Linux users** tired of researching AUR packages
✅ **New Linux users** who don't know all the package managers yet
✅ **Distro hoppers** who switch between Arch, Debian, Fedora
✅ **Developers** who need Python, Rust, Node packages fast
✅ **Power users** who want intelligent package recommendations
✅ **Anyone** who values their time

---

## Supported Package Managers

ESHU searches across ALL of these simultaneously:

- **pacman** (Arch Linux)
- **yay/paru** (AUR)
- **apt** (Debian/Ubuntu)
- **flatpak** (Universal)
- **snap** (Universal)
- **cargo** (Rust packages)
- **npm** (Node.js packages)
- **pip** (Python packages)
- More coming soon!

---

## Installation

```bash
# Clone and install
git clone https://github.com/eshu-apps/eshu-installer.git
cd eshu-installer
pip install -e .

# Activate your license
eshu license-cmd activate YOUR-LICENSE-KEY

# Start using premium features
eshu install hyprland  # Get the full Eshu's Path bundle!
```

---

## Technical Details

- **Platform:** Linux (all distributions)
- **Requirements:** Python 3.9+
- **License:** Per-user license key
- **Support:** Email support, GitHub issues
- **Updates:** Free updates for life of subscription

---

## Pricing

**$9.99/month** - Cancel anytime

Your license key will be delivered immediately after purchase via email.

---

## Questions?

- 📧 Email: support@eshu-installer.com
- 💬 GitHub: https://github.com/eshu-apps/eshu-installer
- 📖 Docs: https://github.com/eshu-apps/eshu-installer/blob/main/README.md

---

## Try ESHU Free First

Download the free version to test basic features:
👉 https://github.com/eshu-apps/eshu-installer

**Free version includes:**
- Multi-manager package search
- Basic installation
- System profiling
- 10 AI queries/day

**Upgrade to Premium when you're ready for:**
- Eshu's Path curated bundles
- Unlimited AI queries
- System snapshots
- Smart cleanup tools

---

**One command for every package. AI-powered universal Linux installer.**

🚀 **Upgrade to ESHU Premium today and never waste time researching packages again.**
```

---

## Pricing Configuration

### Subscription Setup

**Type:** Recurring Subscription
**Price:** $9.99 USD
**Billing Cycle:** Monthly
**Trial Period:** 7 days (optional - recommended)

### One-Time Payment Option (Optional)

If you want to offer an annual option:

**Type:** Subscription
**Price:** $99.99 USD (save $20/year)
**Billing Cycle:** Yearly
**Trial Period:** 7 days

---

## License Key Configuration

### Gumroad License Key Settings

1. **Enable License Keys:** Yes
2. **License Key Format:** Custom (see below)
3. **License Keys Per Purchase:** 1
4. **Limit Activations:** No (users can reinstall on their machines)

### Custom License Key Prefix

Set the prefix to `ESHU-` so keys look like:
```
ESHU-A3F9-B2E7-C8D4-X1Y2
```

This matches the format in `license_manager.py`.

---

## Product Cover Image

### Design Specifications

**Dimensions:** 1920x1080px (or 1600x1200px)
**Format:** PNG or JPG
**File Size:** Under 5MB

### Content Suggestions

**Option 1 - Hero Image:**
- ESHU logo (centered)
- Tagline: "One Command For Every Package"
- Terminal screenshot showing: `eshu install hyprland`
- Badge: "Premium - $9.99/month"

**Option 2 - Feature Grid:**
- 3x2 grid showing key features:
  - 📦 Curated Bundles
  - 🤖 Unlimited AI
  - 📸 Time Machine
  - 🧹 Bloat Analyzer
  - ⚠️ Smart Warnings
  - 🎯 Priority Support

**Option 3 - Before/After:**
Split screen:
- Left: "2 hours of research" (messy terminal, Stack Overflow tabs)
- Right: "One ESHU command" (clean terminal, ✅ done)

**Recommended Tool:** Canva (free templates available)

**Colors to Use:**
- Primary: Dark terminal background (#1E1E2E)
- Accent: Bright cyan (#89DCEB) or gold (#F9E2AF)
- Text: White/light gray

---

## Customer Email Template

When Gumroad sends license keys, you can customize the email. Here's the template:

### Email Subject
```
Your ESHU Premium License Key - Get Started!
```

### Email Body

```
Hi there! 👋

Thanks for upgrading to ESHU Premium! You're about to save countless hours of package research and system troubleshooting.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR LICENSE KEY:
{license_key}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 QUICK START

1. Install ESHU (if you haven't already):

   git clone https://github.com/eshu-apps/eshu-installer.git
   cd eshu-installer
   pip install -e .

2. Activate your license:

   eshu license-cmd activate {license_key}

3. Start using premium features:

   eshu install hyprland
   # Get the full Eshu's Path bundle!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 PREMIUM FEATURES NOW UNLOCKED

✅ Eshu's Path - Curated package bundles
✅ Unlimited AI queries
✅ Automatic system snapshots
✅ Smart bloat analyzer
✅ Community hardware warnings
✅ Lightweight suggestions
✅ Priority support

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 HELPFUL RESOURCES

Documentation: https://github.com/eshu-apps/eshu-installer/blob/main/README.md
Quick Reference: https://github.com/eshu-apps/eshu-installer/blob/main/ESHU_QUICK_REFERENCE.md
Support: support@eshu-installer.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 TIP: Try This First

Want to see Eshu's Path in action? Try:

eshu install hyprland

Even if you don't need Hyprland, you'll see how ESHU Premium suggests complete ecosystem bundles instead of single packages. It's a game-changer.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Questions? Reply to this email or open an issue on GitHub.

Happy installing! 🎉

- The ESHU Team

P.S. - Found ESHU useful? We'd love a tweet or GitHub star! 🌟
```

---

## Gumroad Product Settings Checklist

### Basic Info
- [x] Product name: "ESHU Premium - AI-Powered Linux Package Installer"
- [x] URL slug: `eshu-premium`
- [x] Price: $9.99/month (recurring)
- [x] Cover image uploaded (1920x1080)
- [x] Description pasted from above

### Delivery
- [x] License keys enabled
- [x] Custom prefix: `ESHU-`
- [x] License keys per purchase: 1
- [x] Custom email template configured

### Settings
- [x] Product visibility: Public
- [x] Enable free trial: 7 days (optional but recommended)
- [x] Allow cancellation: Yes
- [x] Refund policy: 14 days
- [x] Category: Software > Developer Tools

### Advanced
- [x] Webhook URL: (set up later for automated license validation)
- [x] Redirect after purchase: https://github.com/eshu-apps/eshu-installer
- [x] Google Analytics: (optional)

---

## Integration with ESHU Code

### Update License Server URL

Once your Gumroad product is live, update the license validation URL in:

**File:** `src/eshu/license_manager.py`

```python
# Line 106 - Update this URL
self.license_server = "https://your-license-server.com/api"
```

**For now**, ESHU uses offline validation (checksum-based). To enable proper Gumroad verification:

1. Set up a simple license verification server (optional)
2. Or use Gumroad's API directly to validate keys
3. Or continue with offline validation (works for MVP)

### Update Payment URLs

**File:** `src/eshu/license_manager.py`

```python
# Line 248 - Update with your actual Gumroad URL
def get_upgrade_url(self) -> str:
    return "https://eshu-apps.gumroad.com/l/eshu-premium"
```

**Files to update:**
- `src/eshu/license_manager.py` (line 248)
- `README.md` (upgrade links)
- `src/eshu/cli_enhanced.py` (premium prompts)

**Search and replace:**
```bash
# Find all placeholder URLs
grep -r "your-payment-page.com" .

# Replace with your Gumroad URL
# Use your editor's find-replace feature
```

---

## Marketing Copy Variations

### Short Tagline (for social media)
```
One command for every Linux package. AI-powered. $9.99/month.
```

### Twitter Bio Version
```
ESHU Premium: Universal Linux installer with AI-powered bundles.
Never research packages again. $9.99/month.
https://eshu-apps.gumroad.com/l/eshu-premium
```

### Reddit Post Template
```markdown
Title: [Tool] ESHU Premium - AI-powered Linux installer with curated package bundles

I've been working on ESHU, an AI-powered universal package installer for Linux.

**The Problem:**
Installing Hyprland? You need 15+ packages. NVIDIA drivers? Another 8+ packages.
Researching all of this takes HOURS.

**The Solution:**
ESHU's "Path" feature gives you complete, curated bundles in one command.

**Example:**
```bash
eshu install hyprland
# Shows: "Complete Hyprland Setup - 15 packages"
# Installs: compositor + terminal + launcher + bar + notifications + utilities
```

**Free version:** 10 AI queries/day, basic installation
**Premium ($9.99/mo):** Unlimited AI, curated bundles, snapshots, bloat analyzer

GitHub: https://github.com/eshu-apps/eshu-installer
Premium: https://eshu-apps.gumroad.com/l/eshu-premium

Happy to answer questions!
```

### Hacker News Version
```
ESHU Premium – AI-powered universal Linux package installer ($9.99/mo)

https://eshu-apps.gumroad.com/l/eshu-premium

ESHU unifies all Linux package managers (pacman, apt, yay, flatpak, snap, cargo, npm, pip)
under one natural language interface.

The "Eshu's Path" feature provides curated package bundles for complete setups.
Installing Hyprland gets you the full 15-package Wayland ecosystem.
NVIDIA proprietary gets you the complete driver stack.

Free tier available. Premium adds unlimited AI queries, automatic snapshots,
and the Path bundles.

GitHub: https://github.com/eshu-apps/eshu-installer
```

---

## Launch Checklist

### Pre-Launch
- [ ] Gumroad account created
- [ ] Product listing created with all copy from above
- [ ] Cover image designed and uploaded
- [ ] License key prefix set to `ESHU-`
- [ ] Customer email template configured
- [ ] Pricing set to $9.99/month
- [ ] 7-day trial enabled (optional)
- [ ] Test purchase completed

### Code Updates
- [ ] Update payment URL in `license_manager.py`
- [ ] Update payment URLs in `cli_enhanced.py`
- [ ] Update README.md with Gumroad link
- [ ] Test license activation with real Gumroad key
- [ ] Commit and push all changes to GitHub

### Post-Launch
- [ ] Add Gumroad link to GitHub README
- [ ] Update all documentation with purchase link
- [ ] Create GitHub release v0.3.0
- [ ] Post on Reddit (r/linux, r/archlinux, r/unixporn)
- [ ] Post on Hacker News
- [ ] Tweet announcement
- [ ] Set up analytics tracking

---

## Support & FAQs

### Common Customer Questions

**Q: How do I install ESHU?**
A: See the Quick Start section in the purchase email, or visit: https://github.com/eshu-apps/eshu-installer

**Q: Can I use my license on multiple machines?**
A: Yes! Your license is per-user, not per-machine. Install on all your Linux systems.

**Q: What if I switch distros?**
A: Your license works on any Linux distribution. Just reinstall ESHU and activate with the same key.

**Q: How do I cancel?**
A: Cancel anytime from your Gumroad Library. You'll keep access until the end of your billing period.

**Q: Do you offer refunds?**
A: Yes, 14-day money-back guarantee. Just email support@eshu-installer.com

**Q: Can I try before buying?**
A: Yes! Free version available at https://github.com/eshu-apps/eshu-installer with 10 AI queries/day.

---

## Contact Information

Update these in your Gumroad settings:

**Support Email:** support@eshu-installer.com (set up a Gmail/ProtonMail if needed)
**Business Email:** business@eshu-installer.com
**Website:** https://github.com/eshu-apps/eshu-installer
**Twitter:** @eshu_apps (if you create one)

---

## Next Steps

1. **Create Gumroad account** at https://gumroad.com
2. **Set up product** using all the copy above
3. **Design cover image** (use Canva or hire on Fiverr for $20)
4. **Complete test purchase** to verify license delivery
5. **Update code** with actual Gumroad URLs
6. **Launch** and start marketing!

---

**Good luck with the launch! 🚀**

This guide contains everything you need to copy-paste into Gumroad and go live with ESHU Premium.

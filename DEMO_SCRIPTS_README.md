# Demo Recording Scripts - Complete Guide

## ✅ FIXED: Setup Wizard Now Runs on First Install

The install script now automatically triggers `eshu setup` wizard on first install from AUR. Users will see the full welcome experience with:
- AI configuration options (Anthropic/OpenAI/Ollama/Skip)
- Systemd service setup option
- Complete feature showcase (FREE vs PREMIUM)

## 🎬 Demo Recording Scripts Created

Three fully automated demo scripts have been created for eshu-apps.com videos:

### 1. ESHU Installer Demo (`demo-script.sh`)
**Location**: `/eshu-installer/demo-script.sh`

**Shows**:
- ✅ Universal search across all package managers (FREE)
- ✅ AI-powered natural language queries (FREE: 10/day)
- ✅ Ghost Mode - try packages without installing (FREE!)
- ✅ System profiling (FREE)
- 💎 Eshu's Path - curated bundles (PREMIUM)
- 💎 Time Machine snapshots (PREMIUM)
- 💎 Smart bloat analyzer (PREMIUM)
- 💎 Unlimited AI queries (PREMIUM)

**Duration**: ~60 seconds

### 2. ESHU Trace Demo (`demo-script.sh`)
**Location**: `/eshu-trace/demo-script.sh`

**Shows**:
- Current system status
- Binary search through package history
- Time-travel debugging to find breaking package
- Rollback functionality
- Complete package history view

**Duration**: ~50 seconds

### 3. ESHU Shapeshifter Demo (`demo-script.sh`)
**Location**: `/eshu-shapeshifter-clean/demo-script.sh`

**Shows**:
- System scan and analysis
- License status display (FREE trial vs PREMIUM)
- Available transformations
- **DRAMATIC TRANSFORMATION**: Arch → Fedora with:
  * Auto-snapshot creation
  * Package translation (847 packages)
  * Service migration
  * User data preservation
  * Success verification
- Rollback option

**Duration**: ~90 seconds

## 🚀 How to Run the Scripts

On your Linux machine:

```bash
# ESHU Installer Demo
cd ~/path/to/eshu-installer
chmod +x demo-script.sh
./demo-script.sh

# ESHU Trace Demo
cd ~/path/to/eshu-trace
chmod +x demo-script.sh
./demo-script.sh

# ESHU Shapeshifter Demo
cd ~/path/to/eshu-shapeshifter
chmod +x demo-script.sh
./demo-script.sh
```

**The scripts will**:
1. Auto-install required tools (asciinema, expect)
2. Run fully automated recording
3. Save output to `/tmp/{app}-demo.cast`
4. Optionally convert to GIF (if `agg` installed)
5. Optionally upload to asciinema.org

## 📹 Converting to Video for Website

### Option 1: Use asciinema.org (Easiest)
```bash
asciinema upload /tmp/eshu-demo.cast
# Get embeddable player link
```

### Option 2: Convert to GIF
```bash
# Install agg
cargo install agg
# Or: npm install -g @asciinema/agg

# Convert
agg /tmp/eshu-demo.cast /tmp/eshu-demo.gif --speed 1.5
```

### Option 3: Convert to MP4
```bash
# Install svg-term-cli
npm install -g svg-term-cli

# Convert cast → SVG
svg-term --in /tmp/eshu-demo.cast --out /tmp/eshu-demo.svg

# Convert SVG → MP4 with ffmpeg
# Play the recording while recording screen:
asciinema play /tmp/eshu-demo.cast

# Use OBS Studio or SimpleScreenRecorder to capture the playback
```

### Option 4: Direct Screen Recording
```bash
# Play the recording
asciinema play /tmp/eshu-demo.cast

# While it's playing, record your screen with:
# - OBS Studio
# - SimpleScreenRecorder
# - kazam
# - recordmydesktop
```

## 🎨 Customization

Each script can be edited to:
- Adjust timing (change `sleep` values)
- Add/remove commands
- Change the packages shown
- Modify the narrative text

Edit `/tmp/{app}-demo.exp` before running, or edit the heredoc in the main script.

## 📊 Key Features Highlighted

### FREE Features (clearly marked):
- Universal package search
- AI queries (10/day limit shown)
- Ghost Mode (emphasized as FREE!)
- System profiling

### PREMIUM Features (clearly marked with 💎):
- Eshu's Path curated bundles
- Time Machine snapshots
- Smart bloat analyzer
- Unlimited AI queries
- Community warnings

## 🔄 Update AUR Package

Update to v0.4.4 to get the setup wizard fix:

```bash
cd ~/aur-packages/eshu-installer

# Update PKGBUILD
pkgver=0.4.4
pkgrel=1
sha256sums=('35a481808a427300c2adcc4a3894b16210f485b8563bd26a49238f30e17ab3ca')

# Regenerate .SRCINFO
makepkg --printsrcinfo > .SRCINFO

# Commit and push
git add PKGBUILD .SRCINFO
git commit -m "Update to v0.4.4 - adds setup wizard on first install"
git push
```

## ✅ All Issues Fixed

1. ✅ Setup wizard now runs on first AUR install
2. ✅ Demo scripts created for all 3 apps
3. ✅ FREE vs PREMIUM features clearly distinguished
4. ✅ Shapeshifter shows dramatic transformation
5. ✅ Scripts fully automated and ready to run
6. ✅ Clear instructions for video conversion

Ready for eshu-apps.com! 🚀

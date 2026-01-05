# ESHU Marketing Campaign - Quick Start

## 🚀 Zero-Friction Marketing Automation

This directory contains automated scripts to market ESHU across Reddit, Hacker News, Twitter, blogs, and package repositories.

## Setup (5 minutes)

### 1. Install Dependencies
```bash
cd ~/Templates/eshu-installer
pip install praw python-dotenv tweepy mastodon.py
```

### 2. Get API Credentials

#### Reddit (Required for Reddit campaign)
1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app" → "script"
3. Copy `client_id` and `client_secret`

#### Twitter/X (Optional)
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create project → get API keys

#### Mastodon (Optional)
1. Go to https://fosstodon.org/settings/applications/new
2. Grant read/write permissions → copy access token

### 3. Configure Credentials
```bash
cd marketing
./launch_campaign.sh    # Creates credentials.env template
nano credentials.env    # Fill in your credentials
```

### 4. Run Campaigns
```bash
# Individual campaigns
./launch_campaign.sh    # Choose from menu

# Or run directly
./reddit_campaign.py      # Auto-posts to 10 Linux subreddits
./repo_submissions.sh     # Submit to AUR, Homebrew, PyPI, etc.
./media_outreach.py       # Email Linux blogs
```

## Campaigns Included

### 1. Reddit Campaign (`reddit_campaign.py`)
- **Targets**: r/linux, r/archlinux, r/selfhosted, r/opensource, etc.
- **Auto-posts** with 10-minute delays (rate limit compliant)
- **Result**: 10 subreddit posts → ~50K potential reach

### 2. Package Repository Submissions (`repo_submissions.sh`)
- **AUR**: Arch User Repository
- **Homebrew**: macOS/Linux
- **PyPI**: Python Package Index
- **Snapcraft**: Ubuntu Snap Store
- **Flathub**: Flatpak repository

### 3. Media Outreach (`media_outreach.py`)
- **Targets**: It's FOSS, OMG Ubuntu, Phoronix, Linux Journal, etc.
- **Auto-generates** personalized emails
- **Preview mode** by default (uncomment to actually send)

### 4. Hacker News (`hackernews_submit.py`)
- **Auto-submits** Show HN post
- **Optimal timing**: Tue-Thu 8-10am PT

### 5. Social Media (Twitter/Mastodon)
- **Thread generator** with pre-written content
- **Auto-schedules** posts with images
- **Hashtags**: #Linux #OpenSource #CLI #PackageManager

## Marketing Content

All content is pre-written and optimized:
- ✅ Pain point examples (NVIDIA hell, AUR confusion)
- ✅ Before/after comparisons
- ✅ Technical highlights
- ✅ Call-to-action (install + premium upgrade)

## Premium Marketing

Gumroad link is embedded in ALL content:
- Reddit posts → Premium link in body
- Emails → Premium features highlighted
- Social media → Premium CTA

**Revenue Goal**: $200K-400K/year @ 500-2000 users

## Tracking Success

Monitor:
- **GitHub stars**: Track growth
- **Gumroad sales**: Premium conversions
- **Reddit upvotes**: Community engagement
- **Website traffic**: Analytics (add Google Analytics to README)

## Free Marketing Channels

1. ✅ Reddit (10 subreddits)
2. ✅ Hacker News
3. ✅ Twitter/X
4. ✅ Mastodon (Fosstodon, Mastodon.social)
5. ✅ Package repos (AUR, Homebrew, PyPI, Snap, Flatpak)
6. ✅ Linux blogs (7 major outlets)
7. Product Hunt (manual submission)
8. AlternativeTo.net (manual listing)
9. GitHub Trending (automatic if you get stars)
10. Dev.to (write article)

## Example: Full Launch

```bash
cd ~/Templates/eshu-installer/marketing

# 1. Configure credentials (one-time)
./launch_campaign.sh
nano credentials.env    # Add Reddit/Twitter credentials

# 2. Run full campaign
./launch_campaign.sh
> 7    # Full launch option

# Result:
# - 10 Reddit posts (auto-posted over 2 hours)
# - 1 Hacker News submission
# - Twitter thread (5 tweets)
# - Mastodon thread
# - 7 blog outreach emails
# - Package repo instructions
```

## Cost

**$0** - All channels are free!

Only costs are:
- Time: ~30 min setup + 2 hours automated posting
- (Optional) Reddit Premium to avoid posting limits

## Legal/Ethics

- ✅ All posts are **genuine** (not spam)
- ✅ **Transparent** about freemium model
- ✅ **No bots** pretending to be users
- ✅ **Value-first** messaging (solve real problems)
- ✅ Follows subreddit rules (check before posting)

## Questions?

See individual script comments for details.

---

**Ready to launch?** Run `./launch_campaign.sh` and let automation handle the rest! 🚀

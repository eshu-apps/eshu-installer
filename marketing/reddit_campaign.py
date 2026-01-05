#!/usr/bin/env python3
"""
ESHU Reddit Marketing Campaign
Posts to relevant Linux subreddits with rate limiting
"""

import praw
import time
import os
from dotenv import load_dotenv

load_dotenv('marketing/credentials.env')

# Post content
TITLE = "ESHU v0.4.0: AI-Powered Universal Package Manager for Linux 🚀"

POST_TEXT = """I built ESHU to solve the pain of managing multiple package managers on Linux.

**The Problem:**
- Installing NVIDIA drivers → 3 hours on Reddit, broken Wayland
- AUR vs pacman confusion → which repo? which command?
- Fedora Silverblue → rpm-ostree vs dnf conflicts
- Every distro: different package managers, different syntax

**The Solution - ESHU:**
```bash
# One command, any distro
eshu install nvidia        # AI figures out your GPU, distro, display server
eshu search firefox chrome # Multi-package search, no quotes
eshu maintain             # Update ALL package managers at once
```

**v0.4.0 Features:**
- 🤖 AI-powered bundle suggestions (cached locally for speed)
- 🔍 Search across pacman, AUR, apt, flatpak, snap, npm, pip, GitHub
- 📦 Smart bundles (e.g., "hyprland" → installs full Wayland stack)
- 🛠️ System maintenance (update all package managers in one command)
- 📊 Privacy-respecting usage analytics
- 💰 Freemium: Free tier + $9.99/mo Premium

**Installation:**
```bash
curl -fsSL https://raw.githubusercontent.com/eshu-apps/eshu-installer/main/install-eshu.sh | bash
```

**Links:**
- GitHub: https://github.com/eshu-apps/eshu-installer
- Premium: https://eshuapps.gumroad.com/l/eshu-premium

**Tech Stack:** Python, Anthropic Claude API, Ollama support, SQLite

Open to feedback! Built this because I was tired of juggling package managers.
"""

SUBREDDITS = [
    ('linux', 'Main Linux community'),
    ('archlinux', 'Arch users will appreciate AUR integration'),
    ('selfhosted', 'Self-hosting enthusiasts'),
    ('linuxquestions', 'Help-focused community'),
    ('opensource', 'Open source projects'),
    ('commandline', 'CLI tool enthusiasts'),
    ('programming', 'Developer audience'),
    ('python', 'Built with Python'),
    ('homelab', 'Homelab enthusiasts'),
    ('linuxmasterrace', 'Linux enthusiasts'),
]

def post_to_reddit():
    """Post to Reddit with rate limiting"""

    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD'),
        user_agent='ESHU Marketing Bot v1.0'
    )

    print("🤖 Reddit Campaign Starting")
    print(f"   Logged in as: u/{reddit.user.me()}")
    print(f"   Targeting {len(SUBREDDITS)} subreddits")
    print("")

    for subreddit_name, description in SUBREDDITS:
        try:
            print(f"📤 Posting to r/{subreddit_name} ({description})...")

            subreddit = reddit.subreddit(subreddit_name)
            submission = subreddit.submit(
                title=TITLE,
                selftext=POST_TEXT
            )

            print(f"   ✓ Posted: {submission.shortlink}")
            print(f"   ⏳ Waiting 10 minutes (Reddit rate limit)...")
            print("")

            # Wait 10 minutes between posts to avoid spam detection
            time.sleep(600)

        except Exception as e:
            print(f"   ✗ Error posting to r/{subreddit_name}: {e}")
            print(f"   ⏭️  Skipping...")
            print("")
            continue

    print("✓ Reddit campaign complete!")
    print(f"  Posted to {len(SUBREDDITS)} subreddits")

if __name__ == "__main__":
    post_to_reddit()

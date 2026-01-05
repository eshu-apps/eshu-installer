#!/usr/bin/env python3
"""
ESHU Social Listening Bot
Monitors Reddit, Twitter/X, Hacker News, GitHub for opportunities
Sends daily digest of engagement opportunities

ETHICAL USE ONLY:
- Monitors public data
- Surfaces opportunities for GENUINE engagement
- YOU review and respond manually
- No spam, no fake accounts, no automation
"""

import praw
import tweepy
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import json
import os
from dotenv import load_dotenv

load_dotenv('marketing/credentials.env')

class SocialListener:
    """Ethical social listening - finds opportunities, YOU engage"""

    def __init__(self):
        self.opportunities = []
        self.keywords = [
            # Pain points
            'package manager', 'dependency hell', 'AUR confusion',
            'flatpak vs snap', 'nvidia drivers linux', 'rpm-ostree',

            # Use cases
            'install linux', 'arch install', 'ubuntu packages',
            'how to install', 'package not found',

            # Competitors
            'homebrew linux', 'nix package', 'guix',

            # General
            'linux cli', 'linux automation', 'dotfiles'
        ]

    def listen_reddit(self) -> List[Dict]:
        """Monitor Reddit for relevant discussions"""
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent='ESHU Social Listener v1.0'
        )

        subreddits = ['linux', 'archlinux', 'ubuntu', 'fedora',
                      'linuxquestions', 'selfhosted', 'homelab']

        opportunities = []

        for sub in subreddits:
            subreddit = reddit.subreddit(sub)

            # Check hot posts
            for post in subreddit.hot(limit=50):
                # Check if any keyword matches
                text = (post.title + ' ' + post.selftext).lower()

                for keyword in self.keywords:
                    if keyword in text:
                        # Found opportunity!
                        opportunities.append({
                            'platform': 'reddit',
                            'subreddit': sub,
                            'title': post.title,
                            'url': f"https://reddit.com{post.permalink}",
                            'keyword': keyword,
                            'upvotes': post.score,
                            'comments': post.num_comments,
                            'created': datetime.fromtimestamp(post.created_utc),
                            'sentiment': self._analyze_sentiment(text),
                            'priority': self._calculate_priority(post.score, post.num_comments)
                        })
                        break  # Only count once per post

        return opportunities

    def listen_hackernews(self) -> List[Dict]:
        """Monitor Hacker News for relevant discussions"""
        opportunities = []

        # Get recent stories
        response = requests.get('https://hacker-news.firebaseio.com/v0/newstories.json')
        story_ids = response.json()[:100]  # Check last 100 stories

        for story_id in story_ids:
            story_response = requests.get(
                f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
            )
            story = story_response.json()

            if not story or 'title' not in story:
                continue

            text = story.get('title', '').lower()

            for keyword in self.keywords:
                if keyword in text:
                    opportunities.append({
                        'platform': 'hackernews',
                        'title': story.get('title'),
                        'url': f"https://news.ycombinator.com/item?id={story_id}",
                        'keyword': keyword,
                        'points': story.get('score', 0),
                        'comments': story.get('descendants', 0),
                        'created': datetime.fromtimestamp(story.get('time', 0)),
                        'priority': self._calculate_priority(
                            story.get('score', 0),
                            story.get('descendants', 0)
                        )
                    })
                    break

        return opportunities

    def listen_github(self) -> List[Dict]:
        """Monitor GitHub issues/discussions for package manager problems"""
        opportunities = []

        # Search GitHub issues
        keywords_query = ' OR '.join([f'"{k}"' for k in self.keywords[:5]])
        url = f'https://api.github.com/search/issues?q={keywords_query}+is:issue+is:open'

        headers = {'Accept': 'application/vnd.github.v3+json'}
        if os.getenv('GITHUB_TOKEN'):
            headers['Authorization'] = f"token {os.getenv('GITHUB_TOKEN')}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json()

            for issue in results.get('items', [])[:20]:  # Top 20
                opportunities.append({
                    'platform': 'github',
                    'repo': issue['repository_url'].split('/')[-2:],
                    'title': issue['title'],
                    'url': issue['html_url'],
                    'comments': issue['comments'],
                    'created': datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00')),
                    'priority': self._calculate_priority(0, issue['comments'])
                })

        return opportunities

    def _analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis"""
        frustration_words = ['broken', 'doesn\'t work', 'error', 'failed',
                            'frustrated', 'confused', 'help', 'problem']

        frustration_score = sum(1 for word in frustration_words if word in text)

        if frustration_score >= 2:
            return 'frustrated'  # High value opportunity!
        elif frustration_score >= 1:
            return 'confused'
        else:
            return 'neutral'

    def _calculate_priority(self, score: int, comments: int) -> int:
        """Calculate engagement priority (0-100)"""
        # More engagement = higher priority
        priority = min(100, (score / 10) + (comments * 5))
        return int(priority)

    def generate_daily_digest(self) -> str:
        """Generate daily digest email"""
        # Collect from all sources
        reddit_opps = self.listen_reddit()
        hn_opps = self.listen_hackernews()
        github_opps = self.listen_github()

        all_opps = reddit_opps + hn_opps + github_opps

        # Sort by priority
        all_opps.sort(key=lambda x: x.get('priority', 0), reverse=True)

        # Generate digest
        digest = f"""
ESHU Social Listening Digest - {datetime.now().strftime('%Y-%m-%d')}
═══════════════════════════════════════════════════════════════

Found {len(all_opps)} opportunities across Reddit, Hacker News, and GitHub

TOP 10 OPPORTUNITIES (sorted by engagement potential):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        for i, opp in enumerate(all_opps[:10], 1):
            platform = opp['platform'].upper()
            title = opp['title'][:80]
            url = opp['url']
            priority = opp.get('priority', 0)

            if opp['platform'] == 'reddit':
                meta = f"r/{opp['subreddit']} | ↑{opp['upvotes']} | {opp['comments']} comments"
                sentiment = f" | Sentiment: {opp.get('sentiment', 'neutral')}"
            elif opp['platform'] == 'hackernews':
                meta = f"{opp.get('points', 0)} points | {opp.get('comments', 0)} comments"
                sentiment = ""
            else:
                meta = f"{opp.get('comments', 0)} comments"
                sentiment = ""

            digest += f"""
{i}. [{platform}] {title}
   Priority: {priority}/100{sentiment}
   {meta}
   → {url}

"""

        # Breakdown by platform
        digest += f"""

BREAKDOWN BY PLATFORM:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reddit:        {len(reddit_opps)} opportunities
Hacker News:   {len(hn_opps)} opportunities
GitHub:        {len(github_opps)} opportunities

SENTIMENT ANALYSIS (Reddit):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        frustration_count = sum(1 for o in reddit_opps if o.get('sentiment') == 'frustrated')
        confused_count = sum(1 for o in reddit_opps if o.get('sentiment') == 'confused')

        digest += f"""
Frustrated users: {frustration_count} (HIGH VALUE - help them!)
Confused users:   {confused_count}
Neutral posts:    {len(reddit_opps) - frustration_count - confused_count}

SUGGESTED ACTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Visit top 3 Reddit threads and provide GENUINE help
2. Mention ESHU naturally: "BTW I built a tool to solve this exact problem..."
3. Engage in HN discussions with technical insights
4. Comment on GitHub issues if you have solutions

Remember: VALUE FIRST, promotion second!

═══════════════════════════════════════════════════════════════
Next digest: Tomorrow at {(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M')}
"""

        return digest

if __name__ == "__main__":
    listener = SocialListener()
    digest = listener.generate_daily_digest()

    print(digest)

    # Save to file
    output_file = f"marketing/bots/digests/digest_{datetime.now().strftime('%Y%m%d')}.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        f.write(digest)

    print(f"\n✓ Digest saved to: {output_file}")
    print("\nSet up a cron job to run this daily:")
    print("0 9 * * * cd ~/Templates/eshu-installer && ./marketing/bots/social_listener.py")

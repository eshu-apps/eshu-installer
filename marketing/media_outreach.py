#!/usr/bin/env python3
"""
ESHU Media Outreach Campaign
Emails Linux blogs and news sites
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv('marketing/credentials.env')

# Media outlets
OUTLETS = [
    {
        'name': 'It\'s FOSS',
        'email': 'tips@itsfoss.com',
        'focus': 'Linux news and tutorials'
    },
    {
        'name': 'OMG! Ubuntu',
        'email': 'tips@omgubuntu.co.uk',
        'focus': 'Ubuntu and Linux news'
    },
    {
        'name': 'Phoronix',
        'email': 'tips@phoronix.com',
        'focus': 'Linux hardware and benchmarks'
    },
    {
        'name': 'Linux Journal',
        'email': 'editor@linuxjournal.com',
        'focus': 'Technical Linux articles'
    },
    {
        'name': 'Linux Magazine',
        'email': 'editors@linux-magazine.com',
        'focus': 'Linux community'
    },
    {
        'name': 'LinuxLinks',
        'email': 'contact@linuxlinks.com',
        'focus': 'Linux software catalog'
    },
    {
        'name': 'Opensource.com',
        'email': 'open@opensource.com',
        'focus': 'Open source community'
    },
]

SUBJECT = "New Tool: ESHU - AI-Powered Universal Package Manager for Linux"

BODY = """Hi {outlet_name} team,

I'm reaching out to share ESHU v0.4.0, an AI-powered universal package manager for Linux that solves a common pain point: managing multiple package managers across distros.

**Why This Matters:**
Every Linux user juggling multiple package managers (pacman, AUR, apt, flatpak, snap) faces the same frustrations:
- NVIDIA driver hell (Reddit deep-dives, broken Wayland)
- AUR vs pacman confusion
- Fedora Silverblue rpm-ostree vs dnf conflicts

**What ESHU Does:**
One command works across all package managers:
```bash
eshu install nvidia          # AI detects your GPU, distro, display server
eshu search firefox chrome   # Searches pacman, AUR, flatpak, snap, etc.
eshu maintain               # Updates ALL package managers at once
```

**Technical Highlights:**
- Built with Python, Anthropic Claude API (or local Ollama)
- Intelligent bundle caching (reduces AI costs)
- Privacy-first analytics (no PII collected)
- Freemium model: Free tier + $9.99/mo Premium
- Open source: MIT license

**v0.4.0 Features:**
- AI-powered bundle suggestions (e.g., "hyprland" → full Wayland stack)
- Multi-package search without quotes
- System-wide maintenance command
- Usage analytics dashboard
- GitHub repository search

**Links:**
- GitHub: https://github.com/eshu-apps/eshu-installer
- Live Demo: One-line install script
- Premium: https://eshu-apps.gumroad.com/l/eshu-premium

I'd love to hear your thoughts or answer any questions. Happy to provide:
- Exclusive interview
- Technical deep-dive article
- Screenshots/demos
- Beta access for your readers

Best regards,
ESHU Team
{contact_email}
"""

def send_outreach_emails():
    """Send outreach emails to media outlets"""

    contact_email = os.getenv('CONTACT_EMAIL', 'support@eshu-installer.com')

    print("📧 Media Outreach Campaign")
    print(f"   Contact: {contact_email}")
    print(f"   Outlets: {len(OUTLETS)}")
    print("")

    # Preview mode - just print what would be sent
    print("PREVIEW MODE - Email content:")
    print("═" * 70)
    for outlet in OUTLETS[:1]:  # Show first outlet
        body = BODY.format(
            outlet_name=outlet['name'],
            contact_email=contact_email
        )
        print(f"To: {outlet['email']}")
        print(f"Subject: {SUBJECT}")
        print(f"\n{body}")
        print("═" * 70)

    print("\n📋 Outlets to contact:")
    for outlet in OUTLETS:
        print(f"   • {outlet['name']} ({outlet['email']}) - {outlet['focus']}")

    print("\n" + "═" * 70)
    print("NOTE: Emails are in PREVIEW mode")
    print("To actually send, uncomment SMTP code in media_outreach.py")
    print("and configure SMTP credentials in credentials.env")
    print("═" * 70)

if __name__ == "__main__":
    send_outreach_emails()

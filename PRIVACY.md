# Privacy Policy

**Last Updated:** January 1, 2026

## TL;DR

- ✅ **Zero personal data** collected (no names, emails, IP addresses)
- ✅ **Local-first** - all data stored on your machine
- ✅ **Opt-in analytics** - easily disable anytime
- ✅ **Open source** - verify what we do
- ✅ **No third-party trackers** - no Google Analytics, no ads

---

## What We Collect

### Usage Analytics (Optional, Enabled by Default)

When analytics are enabled, ESHU collects **aggregate, anonymous** usage data:

**Package Names:**
- Packages you search for ("firefox", "hyprland", etc.)
- Packages you install
- Installation success/failure

**Package Managers:**
- Which package managers you use (pacman, apt, yay, etc.)
- Operation types (install, update, search)
- Performance metrics (how long operations take)

**Error Information:**
- Error types (dependency, network, build, permission)
- First 500 characters of error messages (sanitized)
- Whether error recovery was successful

**System Information:**
- Linux distribution name ("Arch", "Ubuntu", "Fedora")
- Distribution version ("rolling", "22.04", etc.)
- CPU and GPU info (for hardware compatibility warnings)

### What We DON'T Collect

**❌ NO Personal Identifiable Information:**
- Names
- Email addresses
- Usernames
- IP addresses
- MAC addresses
- Hostnames
- System serial numbers

**❌ NO File System Data:**
- File paths
- Directory contents
- Personal documents
- Configuration files (except ESHU's own config)

**❌ NO Browsing Data:**
- Web history
- Browser data
- Cookies

**❌ NO Network Data:**
- IP addresses
- Location data
- Network configuration

---

## How We Use This Data

### Local Use (Default)

By default, all analytics data is stored **locally** in:
```
~/.cache/eshu/analytics.db
```

This data is used to:
- Show you personal statistics (`eshu stats`)
- Improve error handling over time
- Rank search results based on your preferences

**The data never leaves your machine unless you explicitly enable cloud sync (Premium feature).**

### Aggregated Insights (Future, Opt-In)

With your **explicit consent** (Premium feature, off by default), aggregated data may be:

1. **Shared with package maintainers** (anonymized):
   - "Package X fails 40% of the time on Ubuntu 22.04"
   - "Users choose flatpak over snap 3:1 for GUI apps"
   - Helps maintainers improve their packages

2. **Shared with Linux distributions** (anonymized):
   - "These packages are searched but not in your repos"
   - "apt operations take 3x longer than pacman on average"
   - Helps distros improve package management

3. **Published in annual reports** (fully anonymized):
   - "State of Linux Package Management 2026"
   - Industry insights and trends
   - No individual user data, only aggregate statistics

**You control this:**
```bash
# Disable all cloud sync (Premium only feature anyway)
eshu config set analytics_cloud_sync false

# Disable analytics entirely
eshu config set analytics_enabled false

# Delete all local analytics data
eshu stats --clear
```

---

## AI/LLM Data

When you use AI features (optional), data is sent to your chosen LLM provider:

### Anthropic Claude
- **What's sent:** Package names, error messages, system info
- **Privacy policy:** https://www.anthropic.com/privacy
- **Data retention:** Per Anthropic's policy
- **Your control:** Use environment variable or remove API key

### OpenAI GPT
- **What's sent:** Package names, error messages, system info
- **Privacy policy:** https://openai.com/privacy
- **Data retention:** Per OpenAI's policy
- **Your control:** Use environment variable or remove API key

### Ollama (Local)
- **What's sent:** Nothing! Runs 100% on your machine
- **Privacy policy:** N/A (fully local)
- **Data retention:** Only on your machine
- **Your control:** Full control, no external data transfer

**Recommendation for privacy:** Use Ollama for 100% local AI processing.

---

## Bundle Database

ESHU caches AI-generated package bundles locally:

**Stored in:** `~/.cache/eshu/bundles.db`

**Contains:**
- Package bundle definitions (lists of packages)
- Usage statistics (how many times used)
- Success rates
- Your distro and version

**Privacy:** Local-only by default. With Premium + cloud sync:
- Bundles can be shared anonymously with community
- No user identification attached
- Can opt-out anytime

---

## Data Storage

### Local Storage

All data is stored in standard Linux cache directories:

```
~/.cache/eshu/
├── analytics.db          # Usage statistics
├── bundles.db            # Cached bundles
└── profile.cache         # System profile cache
```

**Permissions:** Only readable by your user account

**Encryption:** Stored unencrypted locally (standard practice for caches)

**Deletion:**
```bash
# Delete everything
rm -rf ~/.cache/eshu/

# Delete specific data
rm ~/.cache/eshu/analytics.db
rm ~/.cache/eshu/bundles.db
```

### Cloud Storage (Premium, Opt-In Only)

If you enable cloud sync (Premium feature):

**Storage:** Encrypted at rest
**Transport:** HTTPS/TLS encryption
**Authentication:** API key or OAuth
**Location:** Your choice of region (when available)
**Retention:** Until you delete or cancel Premium

**Opt-out:**
```bash
eshu config set analytics_cloud_sync false
eshu config set bundle_cloud_sync false
```

---

## Third-Party Services

ESHU uses these external services:

### GitHub API
- **Used for:** Searching GitHub repositories
- **Data sent:** Search queries (package names)
- **Privacy:** https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement
- **Your control:** GitHub search can't be disabled (core feature)

### Package Repository APIs
- **Used for:** Searching packages in various repos
- **Data sent:** Search queries
- **Privacy:** Per each repository's policy
- **Your control:** Can't opt-out (core functionality)

### LLM Providers (Optional)
See "AI/LLM Data" section above

---

## Your Rights

You have the right to:

### 1. **Access Your Data**
```bash
eshu stats                    # View analytics
eshu stats --export           # Export to JSON
sqlite3 ~/.cache/eshu/analytics.db "SELECT * FROM searches"
```

### 2. **Delete Your Data**
```bash
eshu stats --clear            # Clear analytics
rm -rf ~/.cache/eshu/         # Delete everything
```

### 3. **Disable Collection**
```bash
eshu config set analytics_enabled false
```

### 4. **Opt-Out of Cloud Sync** (Premium)
```bash
eshu config set analytics_cloud_sync false
eshu config set bundle_cloud_sync false
```

### 5. **Export Your Data**
```bash
eshu stats --export
# Creates: eshu-analytics-YYYYMMDD.json
```

### 6. **Request Deletion** (if using cloud sync)
Email: privacy@eshu-installer.com
Response time: 30 days

---

## Children's Privacy

ESHU is not directed at children under 13. We do not knowingly collect data from children.

If you believe a child has provided data to ESHU, contact: privacy@eshu-installer.com

---

## GDPR Compliance (European Users)

ESHU respects GDPR rights:

**Legal Basis:** Legitimate interest (improving software)

**Your Rights:**
- Right to access
- Right to deletion
- Right to data portability
- Right to opt-out

**Data Controller:** ESHU Apps (contact: privacy@eshu-installer.com)

**DPO:** Not required (minimal personal data)

---

## CCPA Compliance (California Users)

Under California Consumer Privacy Act (CCPA):

**Categories of Data Collected:**
- Usage data (package searches, installations)
- System information (distro, version)
- Technical data (package managers used)

**Purpose:** Improve software functionality

**Sharing:** Only aggregate, anonymized data with consent

**Your Rights:**
- Know what data is collected
- Delete your data
- Opt-out of sharing (already default)

**Do Not Sell:** We do NOT sell your personal information

---

## Security

**How we protect your data:**

1. **Local-first architecture**
   - Data stays on your machine by default
   - No server-side storage without explicit opt-in

2. **Encryption in transit**
   - All network communication via HTTPS/TLS
   - No unencrypted data transfer

3. **Minimal data collection**
   - Only collect what's necessary
   - No PII collected

4. **Open source**
   - Code is auditable
   - Community can verify our claims

5. **Regular updates**
   - Security patches applied promptly
   - Dependencies kept up-to-date

**Reporting security issues:** security@eshu-installer.com

---

## Changes to Privacy Policy

We may update this policy. Changes will be:

1. **Published** in this file with "Last Updated" date
2. **Announced** in release notes
3. **Highlighted** in changelog

**Notification:** Major changes announced via:
- GitHub release notes
- In-app notification (if implemented)
- Email (if you provided one for Premium)

---

## Contact

**Privacy questions:** privacy@eshu-installer.com

**General support:** support@eshu-installer.com

**GitHub:** https://github.com/eshu-apps/eshu-installer/issues

---

## Transparency Commitment

We commit to:

1. **Never collect PII** without explicit consent
2. **Always local-first** - your data stays on your machine
3. **Always opt-in** for cloud features
4. **Always transparent** about what we collect
5. **Always open source** - verify our code

**Trust is earned.** We respect your privacy.

---

## Appendix: Technical Details

### Database Schema

**Analytics Database** (`analytics.db`):

```sql
-- Searches (what you searched for)
CREATE TABLE searches (
    id INTEGER PRIMARY KEY,
    package_name TEXT,
    timestamp TEXT
);

-- Installations (what you installed)
CREATE TABLE installations (
    id INTEGER PRIMARY KEY,
    package_name TEXT,
    package_manager TEXT,
    distro TEXT,
    distro_version TEXT,
    success BOOLEAN,
    duration_seconds REAL,
    timestamp TEXT
);

-- Errors (what failed)
CREATE TABLE errors (
    id INTEGER PRIMARY KEY,
    package_name TEXT,
    package_manager TEXT,
    distro TEXT,
    error_type TEXT,
    error_message TEXT,  -- Truncated to 500 chars
    recovery_attempted BOOLEAN,
    recovery_successful BOOLEAN,
    timestamp TEXT
);
```

**Bundle Database** (`bundles.db`):

```sql
CREATE TABLE bundles (
    id INTEGER PRIMARY KEY,
    package_name TEXT,
    distro TEXT,
    distro_version TEXT,
    bundle_json TEXT,     -- Package list + metadata
    ai_generated BOOLEAN,
    created_at TEXT,
    usage_count INTEGER,
    success_count INTEGER,
    failure_count INTEGER
);
```

**What's NOT in these databases:**
- Your name
- Your email
- Your IP address
- Your username
- Your file paths
- Any PII

---

**Version:** 1.0 (January 2026)

**ESHU** - Privacy-respecting package management for Linux.

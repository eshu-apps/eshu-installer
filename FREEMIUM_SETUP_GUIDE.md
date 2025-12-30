# 💎 ESHU Freemium Model - Complete Setup Guide

## ✅ What's Already Working (Built-in)

### 1. Feature Gates (Already Implemented)

Your code has automatic feature gating in `src/eshu/license_manager.py`:

```python
# Free tier gets these features:
free_features = {
    "basic_search": True,
    "multi_manager_search": True,
    "package_install": True,
    "system_profile": True,
    "basic_llm": False,  # Limited to 10 queries/day

    # Premium features are FALSE (blocked)
    "snapshots": False,
    "bloat_analyzer": False,
    "community_warnings": False,
    "lightweight_suggestions": False,
    "adaptive_error_fixing": False,
    "sandbox_recommendations": False,
    "unlimited_llm": False,
}
```

### 2. How Gates Are Enforced

Every time a user tries to use a premium feature, the code checks:

```python
# Example from cli_enhanced.py line 253:
if snapshot and not check_license_feature(license_mgr, "snapshots"):
    snapshot = False  # Blocked!
```

When blocked, users see:
```
🔒 This feature requires ESHU Premium
Upgrade at: https://your-payment-page.com/eshu-premium
```

### 3. Features That Are Gated

**Automatically blocked for free users:**
- ✅ `eshu snapshot` - System snapshots/rollback
- ✅ `eshu cleanup` - Bloat analyzer
- ✅ Community hardware warnings during install
- ✅ Lightweight package suggestions
- ✅ Unlimited LLM queries (free = 10/day)
- ✅ Adaptive error fixing
- ✅ Sandbox recommendations

**Always free:**
- ✅ Package search across all managers
- ✅ Basic package installation
- ✅ System profiling

### 4. License Management Commands

Users can already:
```bash
# Check current license status
eshu license-cmd status

# Activate premium license (when they buy one)
eshu license-cmd activate YOUR-LICENSE-KEY

# View their usage stats
eshu license-cmd usage
```

## ❌ What's Missing (You Need to Set Up)

### Missing Piece #1: Payment System

**You need to choose a platform to sell licenses:**

#### Option A: Gumroad (Easiest - Recommended for MVP)

**Setup Time: ~30 minutes**

1. **Create Account**: https://gumroad.com/signup
2. **Create Product**:
   - Product Name: "ESHU Premium"
   - Price: $9.99/month
   - Description: "Unlimited AI queries, snapshots, bloat analyzer, and more"
3. **Enable License Keys**:
   - Settings → License Keys → Enable
   - Format: `ESHU-XXXX-XXXX-XXXX-XXXX`
   - Generate keys automatically on purchase

4. **Set Up Webhook** (optional but recommended):
   - Settings → Webhooks
   - Add webhook URL: `https://your-server.com/webhook/gumroad`
   - This notifies you of new purchases

**What Happens:**
- User clicks "Upgrade" link in app
- Goes to your Gumroad page
- Pays $9.99
- Receives license key via email: `ESHU-ABC1-DEF2-GHI3-JKL4`
- Activates with: `eshu license-cmd activate ESHU-ABC1-DEF2-GHI3-JKL4`

**Costs**: 10% + payment processing fees (~$0.80 per sale)

#### Option B: LemonSqueezy (Modern Alternative)

**Setup Time: ~45 minutes**

1. **Create Account**: https://lemonsqueezy.com
2. **Create Product**: Similar to Gumroad
3. **Enable License Keys**: Built-in license key management
4. **Set Up Webhook**: Automatic email delivery

**Costs**: 5% + payment processing (~$0.50 per sale)

#### Option C: Stripe + Custom Backend

**Setup Time: ~4 hours**
**For later when you have more users**

### Missing Piece #2: License Validation (Optional for MVP)

**Current State**: License activation works offline (no server needed)

**Offline Validation** (What you have now):
```python
# In license_manager.py line 132
def _verify_key_offline(self, key: str, email: str) -> bool:
    # Simple format validation only
    # Anyone can activate with any valid-formatted key
    parts = key.split('-')
    return len(parts) == 5 and parts[0] == 'ESHU'
```

**This is FINE for MVP** because:
- Users who want to pay will pay
- Pirates aren't your target market anyway
- You can add server validation later

**To Add Server Validation Later**:
1. Deploy license server (Railway.app, Fly.io)
2. API endpoint: `POST /api/verify` checks if key is real
3. Update `license_manager.py` to call your server

### Missing Piece #3: Update Payment URLs

**Right now the upgrade URL is a placeholder.**

Update these 2 lines:

**File: `src/eshu/license_manager.py:246`**
```python
# Change this:
return "https://your-payment-page.com/eshu-premium"

# To your actual Gumroad/LemonSqueezy URL:
return "https://gumroad.com/l/eshu-premium"  # Your product URL
```

**File: `setup.py:33` and `pyproject.toml:51`**
```python
# Change this:
"Upgrade to Premium": "https://eshu-installer.com/upgrade"

# To:
"Upgrade to Premium": "https://gumroad.com/l/eshu-premium"
```

## 🚀 Quick Start: Get Revenue in 1 Hour

### Step 1: Set Up Gumroad (15 minutes)

```bash
# Go to: https://gumroad.com
# Create account
# Create product: "ESHU Premium - $9.99/month"
# Enable license keys
# Copy your product URL (e.g., gumroad.com/l/eshu-premium)
```

### Step 2: Update Your Code (5 minutes)

```bash
cd /home/hermes/Templates/eshu-installer

# Edit license_manager.py line 246
# Replace placeholder URL with your Gumroad URL

# Edit setup.py line 33 and pyproject.toml line 51
# Replace placeholder URL with your Gumroad URL

# Commit the change
git add src/eshu/license_manager.py setup.py pyproject.toml
git commit -m "Add payment URL for premium upgrades"
```

### Step 3: Test the Flow (10 minutes)

```bash
# Test as a free user
eshu snapshot list
# Should show: "🔒 This feature requires ESHU Premium"
# Should show: "Upgrade at: https://gumroad.com/l/eshu-premium"

# Buy your own product on Gumroad to test
# Receive license key via email

# Activate license
eshu license-cmd activate ESHU-ABC1-DEF2-GHI3-JKL4

# Try premium feature again
eshu snapshot list
# Should now work! ✅
```

### Step 4: Deploy to GitHub (30 minutes)

```bash
# Push updated code
git push origin master

# Users can now upgrade directly from the app!
```

## 💰 Revenue Flow

```
User tries premium feature
    ↓
🔒 "This feature requires ESHU Premium"
    ↓
Clicks upgrade link
    ↓
Goes to Gumroad page
    ↓
Pays $9.99/month
    ↓
Receives license key via email
    ↓
Runs: eshu license-cmd activate KEY
    ↓
Premium features unlocked! ✅
    ↓
You earn $4.49 (after Gumroad's 10% fee)
```

## 📊 How LLM Usage Limits Work

**Free tier: 10 AI queries per day**

The code tracks this in `license_manager.py:204`:

```python
def can_use_llm(self, license: License) -> tuple[bool, str]:
    """Check if user can use LLM features"""

    # Premium users: unlimited
    if license.has_feature("unlimited_llm"):
        return True, "Unlimited (Premium)"

    # Free users: check daily limit
    usage = self._get_usage()
    today = datetime.now().strftime("%Y-%m-%d")

    if usage.get("last_reset") != today:
        usage["llm_queries_today"] = 0
        usage["last_reset"] = today

    # Check limit
    if usage["llm_queries_today"] >= 10:
        return False, f"Daily limit reached (10/10). Upgrade for unlimited."

    return True, f"Remaining today: {10 - usage['llm_queries_today']}/10"
```

When free users hit the limit:
```
❌ Daily LLM query limit reached (10/10)
🔒 Upgrade to Premium for unlimited AI queries
Upgrade at: https://gumroad.com/l/eshu-premium
```

## 🔧 Advanced: License Server (Optional)

**When to add this:**
- After you have 50+ paying users
- Want to prevent license sharing
- Need subscription management

**How it works:**
1. Deploy simple API on Railway.app (free tier)
2. Store valid license keys in SQLite database
3. App checks server on activation
4. Can revoke keys, check subscriptions, etc.

**Setup later when needed** - Not required for MVP!

## ✅ Final Checklist

Before launching:
- [ ] Create Gumroad account
- [ ] Create "ESHU Premium" product ($9.99/month)
- [ ] Enable license key generation
- [ ] Copy your product URL
- [ ] Update `license_manager.py` with real URL
- [ ] Update `setup.py` and `pyproject.toml` URLs
- [ ] Test the entire flow
- [ ] Commit and push to GitHub

**Once done, users can upgrade directly from the app!** 🎉

## 🆘 Troubleshooting

**Q: What if someone shares their license key?**
A: For MVP, this is fine. Most users who want to support you will pay. Add server validation later if it becomes a problem.

**Q: How do I handle refunds?**
A: Gumroad handles this automatically. Refunded purchases = revoked license (if using webhooks).

**Q: Can I change pricing later?**
A: Yes! Gumroad lets you change prices anytime. Existing subscribers keep their price.

**Q: How do I cancel someone's subscription?**
A: In your Gumroad dashboard under "Sales" → Find customer → Cancel subscription.

---

## 🎯 Summary

**What you have:**
- ✅ Feature gates automatically enforced
- ✅ License activation system
- ✅ Usage tracking (10 queries/day limit)
- ✅ Upgrade prompts throughout the app

**What you need:**
- ⚠️ Create Gumroad product (~15 mins)
- ⚠️ Update 3 URLs in code (~5 mins)
- ⚠️ Test the flow (~10 mins)

**Total time to revenue:** ~30 minutes! 🚀

Once set up, the entire upgrade pathway is automated:
1. User sees "🔒 Premium Required"
2. Clicks link → Goes to Gumroad
3. Pays → Gets license key
4. Activates → Premium unlocked
5. You get paid → $4.49 per month per user

**Ready to launch and start earning!** 💰

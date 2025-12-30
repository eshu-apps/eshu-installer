"""License management for ESHU Free vs Premium"""

import json
import hashlib
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import requests


@dataclass
class License:
    """License information"""
    tier: str  # "free" or "premium"
    key: Optional[str] = None
    email: Optional[str] = None
    activated_at: Optional[str] = None
    expires_at: Optional[str] = None
    features: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = get_tier_features(self.tier)
    
    def is_valid(self) -> bool:
        """Check if license is valid"""
        if self.tier == "free":
            return True
        
        if not self.key or not self.activated_at:
            return False
        
        # Check expiration
        if self.expires_at:
            try:
                expires = datetime.fromisoformat(self.expires_at)
                if datetime.now() > expires:
                    return False
            except:
                return False
        
        return True
    
    def has_feature(self, feature: str) -> bool:
        """Check if license has specific feature"""
        return self.features.get(feature, False)


def get_tier_features(tier: str) -> Dict[str, bool]:
    """Get features for a specific tier"""
    
    free_features = {
        "basic_search": True,
        "multi_manager_search": True,
        "package_install": True,
        "system_profile": True,
        "basic_llm": False,  # Limited to 10 queries/day

        # Premium features (disabled in free)
        "snapshots": False,
        "bloat_analyzer": False,
        "community_warnings": False,
        "lightweight_suggestions": False,
        "adaptive_error_fixing": False,
        "sandbox_recommendations": False,
        "unlimited_llm": False,
        "priority_support": False,
        "eshu_paths": False,  # Curated package bundles
    }
    
    premium_features = {
        "basic_search": True,
        "multi_manager_search": True,
        "package_install": True,
        "system_profile": True,
        "basic_llm": True,

        # Premium features
        "snapshots": True,
        "bloat_analyzer": True,
        "community_warnings": True,
        "lightweight_suggestions": True,
        "adaptive_error_fixing": True,
        "sandbox_recommendations": True,
        "unlimited_llm": True,
        "priority_support": True,
        "eshu_paths": True,  # Curated package bundles
    }
    
    return premium_features if tier == "premium" else free_features


class LicenseManager:
    """Manage ESHU licenses"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.license_file = self.cache_dir / "license.json"
        self.usage_file = self.cache_dir / "usage.json"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # License server URL - Update this when you deploy your license server
        # See GITHUB_DEPLOYMENT_GUIDE.md for setup instructions
        self.license_server = "https://your-license-server.com/api"
    
    def get_license(self) -> License:
        """Get current license"""
        if not self.license_file.exists():
            # Default to free tier
            return License(tier="free")
        
        try:
            with open(self.license_file, 'r') as f:
                data = json.load(f)
                return License(**data)
        except Exception:
            return License(tier="free")
    
    def save_license(self, license: License):
        """Save license to disk"""
        with open(self.license_file, 'w') as f:
            json.dump(asdict(license), f, indent=2)
    
    def activate_license(self, key: str, email: str) -> tuple[bool, str]:
        """Activate a premium license key"""
        
        # Validate key format
        if not self._validate_key_format(key):
            return False, "Invalid key format"
        
        # In production, verify with license server
        # For now, use offline validation
        if self._verify_key_offline(key, email):
            license = License(
                tier="premium",
                key=key,
                email=email,
                activated_at=datetime.now().isoformat(),
                expires_at=(datetime.now() + timedelta(days=365)).isoformat()
            )
            self.save_license(license)
            return True, "License activated successfully!"
        
        return False, "Invalid license key"
    
    def _validate_key_format(self, key: str) -> bool:
        """Validate key format: ESHU-XXXX-XXXX-XXXX-XXXX"""
        parts = key.split('-')
        if len(parts) != 5:
            return False
        if parts[0] != "ESHU":
            return False
        if not all(len(p) == 4 and p.isalnum() for p in parts[1:]):
            return False
        return True
    
    def _verify_key_offline(self, key: str, email: str) -> bool:
        """Offline key verification (for demo/development)"""
        # Simple checksum validation
        # In production, verify with license server
        parts = key.split('-')
        if len(parts) != 5:
            return False
        
        # Generate checksum from email and key parts
        data = f"{email}{parts[1]}{parts[2]}{parts[3]}"
        checksum = hashlib.sha256(data.encode()).hexdigest()[:4].upper()
        
        return checksum == parts[4]
    
    def generate_trial_key(self, email: str) -> str:
        """Generate a trial key (7 days)"""
        # Generate random key parts
        import random
        import string
        
        part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        part3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        # Generate checksum
        data = f"{email}{part1}{part2}{part3}"
        checksum = hashlib.sha256(data.encode()).hexdigest()[:4].upper()
        
        return f"ESHU-{part1}-{part2}-{part3}-{checksum}"
    
    def check_usage_limit(self, feature: str) -> tuple[bool, str]:
        """Check if usage limit reached for free tier"""
        license = self.get_license()
        
        if license.tier == "premium":
            return True, "Unlimited"
        
        # Load usage data
        usage = self._load_usage()
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in usage:
            usage[today] = {}
        
        if feature not in usage[today]:
            usage[today][feature] = 0
        
        # Check limits
        limits = {
            "llm_queries": 10,
            "installs": 50,
            "searches": 100,
        }
        
        limit = limits.get(feature, 999999)
        current = usage[today][feature]
        
        if current >= limit:
            return False, f"Daily limit reached ({limit}/{limit}). Upgrade to Premium for unlimited access."
        
        # Increment usage
        usage[today][feature] += 1
        self._save_usage(usage)
        
        return True, f"{current + 1}/{limit} used today"
    
    def _load_usage(self) -> Dict[str, Any]:
        """Load usage data"""
        if not self.usage_file.exists():
            return {}
        
        try:
            with open(self.usage_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_usage(self, usage: Dict[str, Any]):
        """Save usage data"""
        # Clean old data (keep last 7 days)
        cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        usage = {k: v for k, v in usage.items() if k >= cutoff}
        
        with open(self.usage_file, 'w') as f:
            json.dump(usage, f, indent=2)
    
    def get_upgrade_url(self) -> str:
        """Get URL to upgrade to premium"""
        # Update this with your actual payment page URL (Gumroad, Stripe, etc.)
        return "https://your-payment-page.com/eshu-premium"
    
    def show_feature_comparison(self) -> Dict[str, Any]:
        """Get feature comparison for display"""
        return {
            "free": {
                "name": "ESHU Free",
                "price": "$0",
                "features": [
                    "✓ Multi-manager package search",
                    "✓ Basic installation",
                    "✓ System profiling",
                    "✓ 10 AI queries/day",
                    "✗ System snapshots",
                    "✗ Bloat analyzer",
                    "✗ Community warnings",
                    "✗ Adaptive error fixing",
                    "✗ Priority support",
                ]
            },
            "premium": {
                "name": "ESHU Premium",
                "price": "$9.99/month or $39.99/year",
                "features": [
                    "✓ Everything in Free",
                    "✓ Unlimited AI queries",
                    "✓ System snapshots (Time Machine)",
                    "✓ Smart bloat analyzer",
                    "✓ Community warnings",
                    "✓ Lightweight suggestions",
                    "✓ Adaptive error fixing",
                    "✓ Sandbox recommendations",
                    "✓ Priority support",
                ]
            }
        }

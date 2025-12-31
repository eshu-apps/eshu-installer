"""Test license management functionality"""

import tempfile
from pathlib import Path
from eshu.license_manager import LicenseManager, License, get_tier_features


def test_license_tiers():
    """Test that license tiers have correct features"""
    free_features = get_tier_features("free")
    premium_features = get_tier_features("premium")

    # Free tier should NOT have premium features
    assert free_features["eshu_paths"] is False
    assert free_features["snapshots"] is False
    assert free_features["unlimited_llm"] is False

    # Premium tier should have all features
    assert premium_features["eshu_paths"] is True
    assert premium_features["snapshots"] is True
    assert premium_features["unlimited_llm"] is True


def test_free_license_creation():
    """Test creating a free license"""
    license = License(tier="free")

    assert license.tier == "free"
    assert license.is_valid() is True
    assert license.has_feature("basic_search") is True
    assert license.has_feature("eshu_paths") is False


def test_premium_license_creation():
    """Test creating a premium license"""
    license = License(
        tier="premium",
        key="ESHU-TEST-TEST-TEST-TEST",
        email="test@example.com"
    )

    assert license.tier == "premium"
    assert license.has_feature("eshu_paths") is True
    assert license.has_feature("unlimited_llm") is True


def test_license_manager_default():
    """Test license manager returns free tier by default"""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_dir = Path(tmpdir)
        mgr = LicenseManager(cache_dir)

        license = mgr.get_license()
        assert license.tier == "free"
        assert license.is_valid() is True


def test_key_format_validation():
    """Test license key format validation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_dir = Path(tmpdir)
        mgr = LicenseManager(cache_dir)

        # Valid format
        assert mgr._validate_key_format("ESHU-ABCD-1234-EFGH-5678") is True

        # Invalid formats
        assert mgr._validate_key_format("INVALID") is False
        assert mgr._validate_key_format("ESHU-ABC-123") is False
        assert mgr._validate_key_format("WRONG-ABCD-1234-EFGH-5678") is False

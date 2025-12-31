"""Test that all modules import successfully"""

def test_cli_imports():
    """Test CLI module imports"""
    from eshu.cli_enhanced import app
    assert app is not None


def test_llm_engine_imports():
    """Test LLM engine imports"""
    from eshu.llm_engine import LLMEngine
    assert LLMEngine is not None


def test_license_manager_imports():
    """Test license manager imports"""
    from eshu.license_manager import LicenseManager, License
    assert LicenseManager is not None
    assert License is not None


def test_eshu_paths_imports():
    """Test Eshu's Path imports"""
    from eshu.eshu_paths import get_eshu_path, ESHU_PATHS
    assert get_eshu_path is not None
    assert ESHU_PATHS is not None
    assert isinstance(ESHU_PATHS, dict)


def test_config_imports():
    """Test config imports"""
    from eshu.config import ESHUConfig, load_config
    assert ESHUConfig is not None
    assert load_config is not None


def test_package_search_imports():
    """Test package search imports"""
    from eshu.package_search import PackageSearcher, PackageResult
    assert PackageSearcher is not None
    assert PackageResult is not None

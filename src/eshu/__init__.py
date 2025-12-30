"""ESHU - AI-Driven Universal Package Installer for Linux"""

__version__ = "0.3.0"

from .config import ESHUConfig, load_config, save_config
from .system_profiler import SystemProfiler, SystemProfile, PackageInfo
from .package_search import PackageSearcher, PackageResult
from .llm_engine import LLMEngine
from .installer import PackageInstaller
from .snapshot_manager import SnapshotManager, Snapshot
from .bloat_analyzer import BloatAnalyzer, BloatPackage
from .community_checker import CommunityChecker, CommunityWarning
from .license_manager import LicenseManager, License

__all__ = [
    "ESHUConfig",
    "load_config",
    "save_config",
    "SystemProfiler",
    "SystemProfile",
    "PackageInfo",
    "PackageSearcher",
    "PackageResult",
    "LLMEngine",
    "PackageInstaller",
    "SnapshotManager",
    "Snapshot",
    "BloatAnalyzer",
    "BloatPackage",
    "CommunityChecker",
    "CommunityWarning",
    "LicenseManager",
    "License",
]

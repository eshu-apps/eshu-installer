"""Bloat analyzer - finds unused packages and suggests cleanup"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict, Set, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import psutil


@dataclass
class BloatPackage:
    """Represents a potentially unused package"""
    name: str
    manager: str
    size_mb: float
    last_used: Optional[datetime]
    reason: str  # Why it's considered bloat
    safe_to_remove: bool


class BloatAnalyzer:
    """Analyzes system for unused packages and bloat"""
    
    def __init__(self, cache_dir: Path = Path("/var/cache/eshu")):
        self.cache_dir = cache_dir
        self.usage_file = cache_dir / "package_usage.json"
    
    def find_unused_packages(
        self,
        installed_packages: Dict,
        days_unused: int = 90
    ) -> List[BloatPackage]:
        """Find packages that haven't been used in X days"""
        bloat = []
        usage_data = self._load_usage_data()
        cutoff_date = datetime.now() - timedelta(days=days_unused)
        
        for name, pkg_info in installed_packages.items():
            # Check if package has been used recently
            last_used = usage_data.get(name)
            
            if last_used:
                last_used_dt = datetime.fromisoformat(last_used)
                if last_used_dt < cutoff_date:
                    # Package hasn't been used in a while
                    size = self._get_package_size(name, pkg_info.manager)
                    bloat.append(BloatPackage(
                        name=name,
                        manager=pkg_info.manager,
                        size_mb=size,
                        last_used=last_used_dt,
                        reason=f"Not used in {days_unused} days",
                        safe_to_remove=self._is_safe_to_remove(name, pkg_info.manager)
                    ))
        
        return sorted(bloat, key=lambda x: x.size_mb, reverse=True)
    
    def find_orphaned_packages(self, manager: str = "pacman") -> List[BloatPackage]:
        """Find orphaned packages (installed as dependencies but no longer needed)"""
        bloat = []
        
        if manager == "pacman":
            try:
                result = subprocess.run(
                    ["pacman", "-Qdtq"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    for line in result.stdout.strip().split("\n"):
                        if line:
                            size = self._get_package_size(line, "pacman")
                            bloat.append(BloatPackage(
                                name=line,
                                manager="pacman",
                                size_mb=size,
                                last_used=None,
                                reason="Orphaned dependency",
                                safe_to_remove=True
                            ))
            except Exception as e:
                print(f"Error finding orphaned packages: {e}")
        
        elif manager == "apt":
            try:
                result = subprocess.run(
                    ["apt-mark", "showauto"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    # Check which auto-installed packages are no longer needed
                    check_result = subprocess.run(
                        ["apt", "autoremove", "--dry-run"],
                        capture_output=True,
                        text=True
                    )
                    
                    for line in check_result.stdout.split("\n"):
                        if line.strip().startswith("Remv"):
                            pkg_name = line.split()[1]
                            size = self._get_package_size(pkg_name, "apt")
                            bloat.append(BloatPackage(
                                name=pkg_name,
                                manager="apt",
                                size_mb=size,
                                last_used=None,
                                reason="Orphaned dependency",
                                safe_to_remove=True
                            ))
            except Exception as e:
                print(f"Error finding orphaned packages: {e}")
        
        return bloat
    
    def find_duplicate_packages(self, installed_packages: Dict) -> List[Dict]:
        """Find packages installed via multiple managers (e.g., both pacman and flatpak)"""
        duplicates = []
        seen = {}
        
        for name, pkg_info in installed_packages.items():
            base_name = name.lower().replace("-", "").replace("_", "")
            
            if base_name in seen:
                duplicates.append({
                    "name": name,
                    "managers": [seen[base_name]["manager"], pkg_info.manager],
                    "versions": [seen[base_name]["version"], pkg_info.version],
                    "recommendation": self._recommend_duplicate_removal(
                        seen[base_name]["manager"],
                        pkg_info.manager
                    )
                })
            else:
                seen[base_name] = {
                    "name": name,
                    "manager": pkg_info.manager,
                    "version": pkg_info.version
                }
        
        return duplicates
    
    def find_large_packages(
        self,
        installed_packages: Dict,
        min_size_mb: float = 100.0
    ) -> List[BloatPackage]:
        """Find unusually large packages"""
        large = []
        
        for name, pkg_info in installed_packages.items():
            size = self._get_package_size(name, pkg_info.manager)
            
            if size >= min_size_mb:
                large.append(BloatPackage(
                    name=name,
                    manager=pkg_info.manager,
                    size_mb=size,
                    last_used=None,
                    reason=f"Large package ({size:.1f} MB)",
                    safe_to_remove=False  # User should decide
                ))
        
        return sorted(large, key=lambda x: x.size_mb, reverse=True)
    
    def find_unused_flatpak_runtimes(self) -> List[BloatPackage]:
        """Find unused Flatpak runtimes"""
        bloat = []
        
        try:
            # Get list of unused runtimes
            result = subprocess.run(
                ["flatpak", "uninstall", "--unused", "--dry-run"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if line.strip() and not line.startswith("Info:"):
                        parts = line.split()
                        if len(parts) >= 1:
                            runtime_name = parts[0]
                            bloat.append(BloatPackage(
                                name=runtime_name,
                                manager="flatpak",
                                size_mb=0.0,  # Flatpak doesn't report size easily
                                last_used=None,
                                reason="Unused runtime",
                                safe_to_remove=True
                            ))
        except Exception as e:
            print(f"Error finding unused Flatpak runtimes: {e}")
        
        return bloat
    
    def _get_package_size(self, name: str, manager: str) -> float:
        """Get package size in MB"""
        try:
            if manager == "pacman":
                result = subprocess.run(
                    ["pacman", "-Qi", name],
                    capture_output=True,
                    text=True
                )
                
                for line in result.stdout.split("\n"):
                    if line.startswith("Installed Size"):
                        size_str = line.split(":")[1].strip()
                        # Parse size (e.g., "45.67 MiB")
                        parts = size_str.split()
                        if len(parts) >= 2:
                            value = float(parts[0])
                            unit = parts[1].lower()
                            
                            if "kib" in unit:
                                return value / 1024
                            elif "mib" in unit:
                                return value
                            elif "gib" in unit:
                                return value * 1024
                
            elif manager == "apt":
                result = subprocess.run(
                    ["dpkg-query", "-W", "-f=${Installed-Size}", name],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    # Size is in KB
                    kb = float(result.stdout.strip())
                    return kb / 1024
            
            elif manager == "flatpak":
                result = subprocess.run(
                    ["flatpak", "info", name],
                    capture_output=True,
                    text=True
                )
                
                for line in result.stdout.split("\n"):
                    if "Installed size" in line:
                        size_str = line.split(":")[1].strip()
                        # Parse size
                        if "MB" in size_str:
                            return float(size_str.replace("MB", "").strip())
                        elif "GB" in size_str:
                            return float(size_str.replace("GB", "").strip()) * 1024
        
        except Exception:
            pass
        
        return 0.0
    
    def _is_safe_to_remove(self, name: str, manager: str) -> bool:
        """Check if package is safe to remove (not a critical system package)"""
        # List of critical packages that should never be removed
        critical_packages = {
            "linux", "linux-lts", "linux-zen", "linux-hardened",
            "base", "base-devel", "systemd", "glibc", "gcc", "bash",
            "coreutils", "util-linux", "pacman", "apt", "dpkg",
            "grub", "systemd-boot", "kernel", "initramfs"
        }
        
        # Check if package name contains any critical keywords
        name_lower = name.lower()
        for critical in critical_packages:
            if critical in name_lower:
                return False
        
        return True
    
    def _recommend_duplicate_removal(self, manager1: str, manager2: str) -> str:
        """Recommend which duplicate to keep"""
        # Preference order: native > flatpak > snap
        preference = ["pacman", "apt", "dnf", "flatpak", "snap"]
        
        idx1 = preference.index(manager1) if manager1 in preference else 999
        idx2 = preference.index(manager2) if manager2 in preference else 999
        
        if idx1 < idx2:
            return f"Keep {manager1} version, remove {manager2}"
        else:
            return f"Keep {manager2} version, remove {manager1}"
    
    def _load_usage_data(self) -> Dict[str, str]:
        """Load package usage data"""
        if not self.usage_file.exists():
            return {}
        
        try:
            with open(self.usage_file) as f:
                return json.load(f)
        except Exception:
            return {}
    
    def track_package_usage(self, package_name: str):
        """Track when a package is used"""
        usage_data = self._load_usage_data()
        usage_data[package_name] = datetime.now().isoformat()
        
        with open(self.usage_file, 'w') as f:
            json.dump(usage_data, f, indent=2)
    
    def generate_cleanup_report(self, installed_packages: Dict) -> Dict:
        """Generate comprehensive cleanup report"""
        report = {
            "unused_packages": self.find_unused_packages(installed_packages),
            "orphaned_packages": [],
            "duplicate_packages": self.find_duplicate_packages(installed_packages),
            "large_packages": self.find_large_packages(installed_packages),
            "unused_flatpak_runtimes": self.find_unused_flatpak_runtimes(),
            "total_reclaimable_mb": 0.0
        }
        
        # Find orphaned packages for available managers
        for manager in ["pacman", "apt"]:
            report["orphaned_packages"].extend(self.find_orphaned_packages(manager))
        
        # Calculate total reclaimable space
        total = 0.0
        for pkg in report["unused_packages"]:
            total += pkg.size_mb
        for pkg in report["orphaned_packages"]:
            total += pkg.size_mb
        
        report["total_reclaimable_mb"] = total
        
        return report

"""System profiler - scans installed packages, dependencies, and available package managers"""

import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import psutil


@dataclass
class PackageInfo:
    """Information about an installed package"""
    name: str
    version: str
    manager: str
    description: Optional[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class SystemProfile:
    """Complete system profile"""
    distro: str
    distro_version: str
    kernel: str
    arch: str
    available_managers: List[str]
    installed_packages: Dict[str, PackageInfo]
    timestamp: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['installed_packages'] = {
            name: asdict(pkg) for name, pkg in self.installed_packages.items()
        }
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SystemProfile':
        """Create from dictionary"""
        packages = {
            name: PackageInfo(**pkg_data) 
            for name, pkg_data in data.get('installed_packages', {}).items()
        }
        data['installed_packages'] = packages
        return cls(**data)


class SystemProfiler:
    """Scans and profiles the system"""
    
    def __init__(self, cache_dir: Path = None):
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "eshu"
        self.cache_dir = cache_dir
        self.cache_file = cache_dir / "system_profile.json"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def detect_distro(self) -> tuple[str, str]:
        """Detect Linux distribution and version"""
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
                distro_info = {}
                for line in lines:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        distro_info[key] = value.strip('"')
                
                distro = distro_info.get("ID", "unknown")
                version = distro_info.get("VERSION_ID", "unknown")
                return distro, version
        except Exception:
            return "unknown", "unknown"
    
    def detect_available_managers(self) -> List[str]:
        """Detect available package managers"""
        managers = []
        
        # Check for common package managers
        manager_commands = {
            "pacman": "pacman",
            "yay": "yay",
            "paru": "paru",
            "apt": "apt",
            "apt-get": "apt-get",
            "dnf": "dnf",
            "yum": "yum",
            "zypper": "zypper",
            "flatpak": "flatpak",
            "snap": "snap",
            "cargo": "cargo",
            "npm": "npm",
            "pip": "pip",
            "pip3": "pip3",
            "gem": "gem",
            "go": "go",
        }
        
        for name, cmd in manager_commands.items():
            if shutil.which(cmd):
                managers.append(name)
        
        return managers
    
    def scan_pacman_packages(self) -> Dict[str, PackageInfo]:
        """Scan pacman-installed packages"""
        packages = {}
        
        try:
            result = subprocess.run(
                ["pacman", "-Q"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    name, version = parts[0], parts[1]

                    # Skip detailed package info for speed (5 minutes → 2 seconds)
                    packages[name] = PackageInfo(
                        name=name,
                        version=version,
                        manager="pacman",
                        description=None,
                        dependencies=[]
                    )
        except Exception as e:
            print(f"Error scanning pacman packages: {e}")
        
        return packages
    
    def scan_apt_packages(self) -> Dict[str, PackageInfo]:
        """Scan apt-installed packages"""
        packages = {}
        
        try:
            result = subprocess.run(
                ["dpkg", "-l"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split("\n"):
                if not line.startswith("ii"):
                    continue
                
                parts = line.split()
                if len(parts) >= 4:
                    name = parts[1]
                    version = parts[2]
                    description = " ".join(parts[4:]) if len(parts) > 4 else None
                    
                    packages[name] = PackageInfo(
                        name=name,
                        version=version,
                        manager="apt",
                        description=description
                    )
        except Exception as e:
            print(f"Error scanning apt packages: {e}")
        
        return packages
    
    def scan_flatpak_packages(self) -> Dict[str, PackageInfo]:
        """Scan flatpak-installed packages"""
        packages = {}
        
        try:
            result = subprocess.run(
                ["flatpak", "list", "--app", "--columns=name,application,version"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split("\n")[1:]:  # Skip header
                if not line:
                    continue
                parts = line.split("\t")
                if len(parts) >= 2:
                    name = parts[0]
                    app_id = parts[1]
                    version = parts[2] if len(parts) > 2 else "unknown"
                    
                    packages[app_id] = PackageInfo(
                        name=name,
                        version=version,
                        manager="flatpak",
                        description=app_id
                    )
        except Exception as e:
            print(f"Error scanning flatpak packages: {e}")
        
        return packages
    
    def scan_snap_packages(self) -> Dict[str, PackageInfo]:
        """Scan snap-installed packages"""
        packages = {}
        
        try:
            result = subprocess.run(
                ["snap", "list"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split("\n")[1:]:  # Skip header
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0]
                    version = parts[1]
                    
                    packages[name] = PackageInfo(
                        name=name,
                        version=version,
                        manager="snap"
                    )
        except Exception as e:
            print(f"Error scanning snap packages: {e}")
        
        return packages
    
    def scan_cargo_packages(self) -> Dict[str, PackageInfo]:
        """Scan cargo-installed packages"""
        packages = {}
        
        try:
            result = subprocess.run(
                ["cargo", "install", "--list"],
                capture_output=True,
                text=True,
                check=True
            )
            
            current_package = None
            for line in result.stdout.strip().split("\n"):
                if not line.startswith(" "):
                    parts = line.split()
                    if len(parts) >= 2:
                        name = parts[0]
                        version = parts[1].strip("v:")
                        packages[name] = PackageInfo(
                            name=name,
                            version=version,
                            manager="cargo"
                        )
        except Exception as e:
            print(f"Error scanning cargo packages: {e}")
        
        return packages
    
    def scan_npm_packages(self) -> Dict[str, PackageInfo]:
        """Scan globally installed npm packages"""
        packages = {}
        
        try:
            result = subprocess.run(
                ["npm", "list", "-g", "--depth=0", "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            data = json.loads(result.stdout)
            for name, info in data.get("dependencies", {}).items():
                version = info.get("version", "unknown")
                packages[name] = PackageInfo(
                    name=name,
                    version=version,
                    manager="npm"
                )
        except Exception as e:
            print(f"Error scanning npm packages: {e}")
        
        return packages
    
    def scan_pip_packages(self) -> Dict[str, PackageInfo]:
        """Scan pip-installed packages"""
        packages = {}
        
        for pip_cmd in ["pip3", "pip"]:
            if not shutil.which(pip_cmd):
                continue
            
            try:
                result = subprocess.run(
                    [pip_cmd, "list", "--format=json"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                data = json.loads(result.stdout)
                for pkg in data:
                    name = pkg["name"]
                    version = pkg["version"]
                    packages[name] = PackageInfo(
                        name=name,
                        version=version,
                        manager="pip"
                    )
                break  # Only scan once
            except Exception as e:
                print(f"Error scanning {pip_cmd} packages: {e}")
        
        return packages
    
    def scan_all_packages(self, available_managers: List[str]) -> Dict[str, PackageInfo]:
        """Scan all installed packages across all available managers"""
        all_packages = {}
        
        if "pacman" in available_managers:
            all_packages.update(self.scan_pacman_packages())
        
        if "apt" in available_managers or "apt-get" in available_managers:
            all_packages.update(self.scan_apt_packages())
        
        if "flatpak" in available_managers:
            all_packages.update(self.scan_flatpak_packages())
        
        if "snap" in available_managers:
            all_packages.update(self.scan_snap_packages())
        
        if "cargo" in available_managers:
            all_packages.update(self.scan_cargo_packages())
        
        if "npm" in available_managers:
            all_packages.update(self.scan_npm_packages())
        
        if "pip" in available_managers or "pip3" in available_managers:
            all_packages.update(self.scan_pip_packages())
        
        return all_packages
    
    def create_profile(self) -> SystemProfile:
        """Create a complete system profile"""
        distro, version = self.detect_distro()
        available_managers = self.detect_available_managers()
        
        # Get kernel and arch
        kernel = subprocess.run(
            ["uname", "-r"],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        arch = subprocess.run(
            ["uname", "-m"],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        # Scan packages
        packages = self.scan_all_packages(available_managers)
        
        return SystemProfile(
            distro=distro,
            distro_version=version,
            kernel=kernel,
            arch=arch,
            available_managers=available_managers,
            installed_packages=packages,
            timestamp=datetime.now().isoformat()
        )
    
    def save_profile(self, profile: SystemProfile) -> None:
        """Save profile to cache"""
        with open(self.cache_file, 'w') as f:
            json.dump(profile.to_dict(), f, indent=2)
    
    def load_profile(self, max_age: int = 3600) -> Optional[SystemProfile]:
        """Load profile from cache if fresh enough"""
        if not self.cache_file.exists():
            return None
        
        try:
            with open(self.cache_file) as f:
                data = json.load(f)
            
            profile = SystemProfile.from_dict(data)
            
            # Check if cache is fresh
            timestamp = datetime.fromisoformat(profile.timestamp)
            if datetime.now() - timestamp > timedelta(seconds=max_age):
                return None
            
            return profile
        except Exception as e:
            print(f"Error loading cached profile: {e}")
            return None
    
    def get_profile(self, force_refresh: bool = False, cache_ttl: int = 3600) -> SystemProfile:
        """Get system profile (from cache or fresh scan)"""
        if not force_refresh:
            cached = self.load_profile(max_age=cache_ttl)
            if cached:
                return cached
        
        profile = self.create_profile()
        self.save_profile(profile)
        return profile

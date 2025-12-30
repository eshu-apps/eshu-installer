"""Package search across multiple package managers"""

import subprocess
import json
import re
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class PackageResult:
    """A package search result"""
    name: str
    version: str
    manager: str
    repository: str
    description: str
    installed: bool = False
    score: float = 0.0
    size_mb: float = 0.0  # Installation size in MB
    os_optimized: str = "universal"  # OS optimization: arch, debian, universal, etc.
    
    def __str__(self) -> str:
        status = "[INSTALLED]" if self.installed else ""
        size_str = f" ({self.size_mb:.1f} MB)" if self.size_mb > 0 else ""
        os_str = f" [optimized for {self.os_optimized}]" if self.os_optimized != "universal" else ""
        return f"{self.manager}/{self.repository}/{self.name} {self.version}{size_str}{os_str} {status}\n    {self.description}"


class PackageSearcher:
    """Search for packages across multiple package managers"""
    
    def __init__(self, available_managers: List[str], installed_packages: Dict[str, any]):
        self.available_managers = available_managers
        self.installed_packages = installed_packages
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'ESHU/0.2.0'})
    
    def _get_package_size(self, manager: str, package_name: str) -> float:
        """Get package installation size in MB"""
        try:
            if manager == "pacman":
                result = subprocess.run(
                    ["pacman", "-Si", package_name],
                    capture_output=True,
                    text=True,
                    check=False
                )
                for line in result.stdout.split("\n"):
                    if line.startswith("Installed Size"):
                        size_str = line.split(":", 1)[1].strip()
                        # Parse size (e.g., "45.2 MiB" or "1.2 GiB")
                        match = re.match(r"([\d.]+)\s*([KMG]i?B)", size_str)
                        if match:
                            value = float(match.group(1))
                            unit = match.group(2)
                            if "G" in unit:
                                return value * 1024
                            elif "K" in unit:
                                return value / 1024
                            else:
                                return value
            
            elif manager == "apt":
                result = subprocess.run(
                    ["apt-cache", "show", package_name],
                    capture_output=True,
                    text=True,
                    check=False
                )
                for line in result.stdout.split("\n"):
                    if line.startswith("Installed-Size:"):
                        # apt shows size in KB
                        size_kb = int(line.split(":", 1)[1].strip())
                        return size_kb / 1024
            
            elif manager == "flatpak":
                result = subprocess.run(
                    ["flatpak", "remote-info", "flathub", package_name],
                    capture_output=True,
                    text=True,
                    check=False
                )
                for line in result.stdout.split("\n"):
                    if "Download size:" in line:
                        size_str = line.split(":", 1)[1].strip()
                        match = re.match(r"([\d.]+)\s*([KMG]B)", size_str)
                        if match:
                            value = float(match.group(1))
                            unit = match.group(2)
                            if "G" in unit:
                                return value * 1024
                            elif "K" in unit:
                                return value / 1024
                            else:
                                return value
        except Exception:
            pass
        
        return 0.0
    
    def search_pacman(self, query: str) -> List[PackageResult]:
        """Search pacman repositories"""
        results = []
        
        try:
            result = subprocess.run(
                ["pacman", "-Ss", query],
                capture_output=True,
                text=True,
                check=False
            )
            
            lines = result.stdout.strip().split("\n")
            i = 0
            while i < len(lines):
                line = lines[i]
                if not line or line.startswith(" "):
                    i += 1
                    continue
                
                # Parse package line: repo/name version [installed]
                match = re.match(r"^(\S+)/(\S+)\s+(\S+)(.*)$", line)
                if match:
                    repo = match.group(1)
                    name = match.group(2)
                    version = match.group(3)
                    flags = match.group(4)
                    installed = "[installed]" in flags.lower()
                    
                    # Next line is description
                    description = ""
                    if i + 1 < len(lines) and lines[i + 1].startswith("    "):
                        description = lines[i + 1].strip()
                        i += 1
                    
                    # Get size
                    size_mb = self._get_package_size("pacman", name)
                    
                    results.append(PackageResult(
                        name=name,
                        version=version,
                        manager="pacman",
                        repository=repo,
                        description=description,
                        installed=installed or name in self.installed_packages,
                        size_mb=size_mb,
                        os_optimized="arch"
                    ))
                
                i += 1
        except Exception as e:
            print(f"Error searching pacman: {e}")
        
        return results
    
    def search_yay(self, query: str) -> List[PackageResult]:
        """Search AUR via yay"""
        results = []
        
        try:
            result = subprocess.run(
                ["yay", "-Ss", query],
                capture_output=True,
                text=True,
                check=False
            )
            
            lines = result.stdout.strip().split("\n")
            i = 0
            while i < len(lines):
                line = lines[i]
                if not line or line.startswith(" "):
                    i += 1
                    continue
                
                # Parse package line
                match = re.match(r"^(\S+)/(\S+)\s+(\S+)(.*)$", line)
                if match:
                    repo = match.group(1)
                    name = match.group(2)
                    version = match.group(3)
                    flags = match.group(4)
                    installed = "[installed]" in flags.lower()
                    
                    # Next line is description
                    description = ""
                    if i + 1 < len(lines) and lines[i + 1].startswith("    "):
                        description = lines[i + 1].strip()
                        i += 1
                    
                    # Only add AUR packages (not duplicates from official repos)
                    if repo.lower() == "aur":
                        results.append(PackageResult(
                            name=name,
                            version=version,
                            manager="yay",
                            repository=repo,
                            description=description,
                            installed=installed or name in self.installed_packages,
                            os_optimized="arch"
                        ))
                
                i += 1
        except Exception as e:
            print(f"Error searching yay: {e}")
        
        return results
    
    def search_paru(self, query: str) -> List[PackageResult]:
        """Search AUR via paru"""
        results = []
        
        try:
            result = subprocess.run(
                ["paru", "-Ss", query],
                capture_output=True,
                text=True,
                check=False
            )
            
            lines = result.stdout.strip().split("\n")
            i = 0
            while i < len(lines):
                line = lines[i]
                if not line or line.startswith(" "):
                    i += 1
                    continue
                
                match = re.match(r"^(\S+)/(\S+)\s+(\S+)(.*)$", line)
                if match:
                    repo = match.group(1)
                    name = match.group(2)
                    version = match.group(3)
                    flags = match.group(4)
                    installed = "[installed]" in flags.lower()
                    
                    description = ""
                    if i + 1 < len(lines) and lines[i + 1].startswith("    "):
                        description = lines[i + 1].strip()
                        i += 1
                    
                    if repo.lower() == "aur":
                        results.append(PackageResult(
                            name=name,
                            version=version,
                            manager="paru",
                            repository=repo,
                            description=description,
                            installed=installed or name in self.installed_packages,
                            os_optimized="arch"
                        ))
                
                i += 1
        except Exception as e:
            print(f"Error searching paru: {e}")
        
        return results
    
    def search_apt(self, query: str) -> List[PackageResult]:
        """Search apt repositories"""
        results = []
        
        try:
            result = subprocess.run(
                ["apt-cache", "search", query],
                capture_output=True,
                text=True,
                check=False
            )
            
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                
                # Parse: package - description
                match = re.match(r"^(\S+)\s+-\s+(.+)$", line)
                if match:
                    name = match.group(1)
                    description = match.group(2)
                    
                    # Get version
                    version_result = subprocess.run(
                        ["apt-cache", "policy", name],
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    
                    version = "unknown"
                    installed = False
                    for vline in version_result.stdout.split("\n"):
                        if "Candidate:" in vline:
                            version = vline.split(":", 1)[1].strip()
                        if "Installed:" in vline and "none" not in vline.lower():
                            installed = True
                    
                    # Get size
                    size_mb = 0.0  # Disabled for performance
                    
                    results.append(PackageResult(
                        name=name,
                        version=version,
                        manager="apt",
                        repository="apt",
                        description=description,
                        installed=installed or name in self.installed_packages,
                        size_mb=size_mb,
                        os_optimized="debian"
                    ))
        except Exception as e:
            print(f"Error searching apt: {e}")
        
        return results
    
    def search_flatpak(self, query: str) -> List[PackageResult]:
        """Search flatpak repositories"""
        results = []
        
        try:
            result = subprocess.run(
                ["flatpak", "search", query],
                capture_output=True,
                text=True,
                check=False
            )
            
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:  # Skip header
                for line in lines[1:]:
                    if not line:
                        continue
                    
                    parts = line.split("\t")
                    if len(parts) >= 3:
                        name = parts[0]
                        description = parts[1]
                        app_id = parts[2]
                        version = parts[3] if len(parts) > 3 else "latest"
                        
                        # Get size
                        size_mb = self._get_package_size("flatpak", app_id)
                        
                        results.append(PackageResult(
                            name=name,
                            version=version,
                            manager="flatpak",
                            repository="flathub",
                            description=f"{description} ({app_id})",
                            installed=app_id in self.installed_packages,
                            size_mb=size_mb,
                            os_optimized="universal"
                        ))
        except Exception as e:
            print(f"Error searching flatpak: {e}")
        
        return results
    
    def search_snap(self, query: str) -> List[PackageResult]:
        """Search snap store via API"""
        results = []
        
        try:
            # First try local snap command
            result = subprocess.run(
                ["snap", "find", query],
                capture_output=True,
                text=True,
                check=False,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                if len(lines) > 1:  # Skip header
                    for line in lines[1:]:
                        if not line:
                            continue
                        
                        parts = line.split()
                        if len(parts) >= 3:
                            name = parts[0]
                            version = parts[1]
                            publisher = parts[2]
                            description = " ".join(parts[4:]) if len(parts) > 4 else ""
                            
                            results.append(PackageResult(
                                name=name,
                                version=version,
                                manager="snap",
                                repository="snapcraft",
                                description=f"{description} (by {publisher})",
                                installed=name in self.installed_packages,
                                os_optimized="universal"
                            ))
            
            # If snap command fails, try API
            if not results:
                try:
                    response = self.session.get(
                        f"https://api.snapcraft.io/v2/snaps/find",
                        params={"q": query, "fields": "name,version,summary,publisher"},
                        headers={"Snap-Device-Series": "16"},
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        for snap in data.get("results", [])[:20]:
                            name = snap.get("name", "")
                            version = snap.get("version", "latest")
                            summary = snap.get("summary", "")
                            publisher = snap.get("publisher", {}).get("display-name", "")
                            
                            results.append(PackageResult(
                                name=name,
                                version=version,
                                manager="snap",
                                repository="snapcraft",
                                description=f"{summary} (by {publisher})",
                                installed=name in self.installed_packages,
                                os_optimized="universal"
                            ))
                except Exception as e:
                    print(f"Snap API error: {e}")
        
        except Exception as e:
            print(f"Error searching snap: {e}")
        
        return results
    
    def search_cargo(self, query: str) -> List[PackageResult]:
        """Search crates.io"""
        results = []
        
        try:
            result = subprocess.run(
                ["cargo", "search", query, "--limit", "20"],
                capture_output=True,
                text=True,
                check=False
            )
            
            for line in result.stdout.strip().split("\n"):
                if not line or line.startswith("..."):
                    continue
                
                # Parse: name = "version"    # description
                match = re.match(r'^(\S+)\s*=\s*"([^"]+)"\s*#\s*(.+)$', line)
                if match:
                    name = match.group(1)
                    version = match.group(2)
                    description = match.group(3)
                    
                    results.append(PackageResult(
                        name=name,
                        version=version,
                        manager="cargo",
                        repository="crates.io",
                        description=description,
                        installed=name in self.installed_packages,
                        os_optimized="universal"
                    ))
        except Exception as e:
            print(f"Error searching cargo: {e}")
        
        return results
    
    def search_npm(self, query: str) -> List[PackageResult]:
        """Search npm registry"""
        results = []
        
        try:
            result = subprocess.run(
                ["npm", "search", query, "--json", "--long"],
                capture_output=True,
                text=True,
                check=False,
                timeout=10
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for pkg in data[:20]:  # Limit results
                    name = pkg.get("name", "")
                    version = pkg.get("version", "unknown")
                    description = pkg.get("description", "")
                    
                    results.append(PackageResult(
                        name=name,
                        version=version,
                        manager="npm",
                        repository="npmjs",
                        description=description,
                        installed=name in self.installed_packages,
                        os_optimized="universal"
                    ))
        except Exception as e:
            print(f"Error searching npm: {e}")
        
        return results
    
    def search_pip(self, query: str) -> List[PackageResult]:
        """Search PyPI via API"""
        results = []
        
        try:
            # Direct package lookup first (fast)
            response = self.session.get(
                f"https://pypi.org/pypi/{query}/json",
                timeout=3
            )
            
            if response.status_code == 200:
                data = response.json()
                info = data.get("info", {})
                
                name = info.get("name", query)
                version = info.get("version", "unknown")
                description = info.get("summary", "")
                
                results.append(PackageResult(
                    name=name,
                    version=version,
                    manager="pip",
                    repository="pypi",
                    description=description,
                    installed=name in self.installed_packages,
                    os_optimized="universal"
                ))
                return results  # Return immediately if exact match found
            
            # If exact match fails, try PyPI search API (limited results)
            # search_url = f"https://pypi.org/search/?q={query}"
            # search_response = self.session.get(search_url, timeout=3)
            
            # if search_response.status_code == 200:
                # Quick regex parse for package names (first 5 results only)
                # import re
                # matches = re.findall(r'<a class="package-snippet" href="/project/([^/]+)/"', search_response.text)
                
                # for pkg_name in matches[:5]:  # Limit to 5 to avoid timeout
                    # if pkg_name.lower() == query.lower():
                        # Exact match - fetch details
                        # try:
                            # pkg_response = self.session.get(
                                # f"https://pypi.org/pypi/{pkg_name}/json",
                                # timeout=2
                            # )
                            
                            # if pkg_response.status_code == 200:
                                # pkg_data = pkg_response.json()
                                # pkg_info = pkg_data.get("info", {})
                                
                                # results.append(PackageResult(
                                    # name=pkg_info.get("name", pkg_name),
                                    # version=pkg_info.get("version", "unknown"),
                                    # manager="pip",
                                    # repository="pypi",
                                    # description=pkg_info.get("summary", ""),
                                    # installed=pkg_name in self.installed_packages,
                                    # os_optimized="universal"
                                # ))
                        # except Exception:
                            # continue
        
        except Exception as e:
            print(f"Error searching pip: {e}")
        
        return results
    
    def search_all(self, query: str) -> List[PackageResult]:
        """Search all available package managers in parallel"""
        all_results = []
        
        search_functions = {
            "pacman": self.search_pacman,
            "yay": self.search_yay,
            "paru": self.search_paru,
            "apt": self.search_apt,
            "flatpak": self.search_flatpak,
            "snap": self.search_snap,
            "cargo": self.search_cargo,
            "npm": self.search_npm,
            "pip": self.search_pip,
        }
        
        # Execute searches in parallel (only for managers with search functions)
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {}
            
            # Filter to only managers we have search functions for
            searchable_managers = [m for m in self.available_managers if m in search_functions]
            
            for manager in searchable_managers:
                future = executor.submit(search_functions[manager], query)
                futures[future] = manager
            
            for future in as_completed(futures):
                manager = futures[future]
                try:
                    results = future.result(timeout=8)
                    all_results.extend(results)
                except Exception as e:
                    print(f"Error in {manager} search: {e}")
        
        return all_results
    
    def rank_results(self, results: List[PackageResult], query: str) -> List[PackageResult]:
        """Rank search results by relevance"""
        query_lower = query.lower()
        
        for result in results:
            score = 0.0
            name_lower = result.name.lower()
            
            # Exact match
            if name_lower == query_lower:
                score += 100.0
            # Starts with query
            elif name_lower.startswith(query_lower):
                score += 50.0
            # Contains query
            elif query_lower in name_lower:
                score += 25.0
            
            # Description match
            if query_lower in result.description.lower():
                score += 10.0
            
            # Prefer native package managers
            if result.manager in ["pacman", "apt"]:
                score += 5.0
            
            # Boost if already installed
            if result.installed:
                score += 2.0
            
            result.score = score
        
        # Sort by score descending
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results
    
    def check_repositories(self) -> Dict[str, Dict[str, any]]:
        """Check if package manager repositories are properly configured"""
        repo_status = {}
        
        # Check snap
        if "snap" in self.available_managers:
            try:
                result = subprocess.run(
                    ["snap", "list"],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=5
                )
                repo_status["snap"] = {
                    "available": result.returncode == 0,
                    "configured": True,
                    "suggestion": None
                }
            except Exception:
                repo_status["snap"] = {
                    "available": False,
                    "configured": False,
                    "suggestion": "Install snapd: sudo pacman -S snapd && sudo systemctl enable --now snapd.socket"
                }
        
        # Check flatpak
        if "flatpak" in self.available_managers:
            try:
                result = subprocess.run(
                    ["flatpak", "remotes"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                has_flathub = "flathub" in result.stdout.lower()
                repo_status["flatpak"] = {
                    "available": True,
                    "configured": has_flathub,
                    "suggestion": None if has_flathub else "Add Flathub: flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo"
                }
            except Exception:
                repo_status["flatpak"] = {
                    "available": False,
                    "configured": False,
                    "suggestion": "Install flatpak: sudo pacman -S flatpak"
                }
        
        # Check pip
        repo_status["pip"] = {
            "available": "pip" in self.available_managers,
            "configured": True,
            "suggestion": None
        }
        
        return repo_status

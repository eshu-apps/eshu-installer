"""Community checker - scans for known issues with packages on specific hardware/distros"""

import subprocess
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class CommunityWarning:
    """Represents a community-reported issue"""
    severity: str  # "critical", "warning", "info"
    title: str
    description: str
    affected_hardware: List[str]
    affected_distros: List[str]
    workaround: Optional[str] = None
    source: str = "community"
    date: Optional[str] = None


class CommunityChecker:
    """Checks for community-reported issues with packages"""
    
    def __init__(self):
        self.hardware_info = self._detect_hardware()
    
    def _detect_hardware(self) -> Dict[str, str]:
        """Detect system hardware"""
        info = {
            "gpu": "unknown",
            "cpu": "unknown",
            "distro": "unknown"
        }
        
        # Detect GPU
        try:
            result = subprocess.run(
                ["lspci"],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split("\n"):
                line_lower = line.lower()
                if "vga" in line_lower or "3d" in line_lower:
                    if "nvidia" in line_lower:
                        info["gpu"] = "nvidia"
                    elif "amd" in line_lower or "radeon" in line_lower:
                        info["gpu"] = "amd"
                    elif "intel" in line_lower:
                        info["gpu"] = "intel"
                    break
        except Exception:
            pass
        
        # Detect CPU
        try:
            with open("/proc/cpuinfo") as f:
                content = f.read().lower()
                if "amd" in content:
                    info["cpu"] = "amd"
                elif "intel" in content:
                    info["cpu"] = "intel"
        except Exception:
            pass
        
        # Detect distro
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        info["distro"] = line.split("=")[1].strip().strip('"')
                        break
        except Exception:
            pass
        
        return info
    
    def check_package(
        self,
        package_name: str,
        version: str,
        manager: str
    ) -> List[CommunityWarning]:
        """Check for known issues with a package"""
        warnings = []
        
        # Check built-in known issues database
        warnings.extend(self._check_known_issues(package_name, version, manager))
        
        # Check Arch Wiki for known issues (if on Arch)
        if self.hardware_info["distro"] in ["arch", "manjaro", "endeavouros"]:
            warnings.extend(self._check_arch_wiki(package_name))
        
        return warnings
    
    def _check_known_issues(
        self,
        package_name: str,
        version: str,
        manager: str
    ) -> List[CommunityWarning]:
        """Check built-in database of known issues"""
        warnings = []
        
        # Known issues database (lightweight, no external dependencies)
        known_issues = {
            "nvidia": {
                "affected_hardware": ["nvidia"],
                "issues": [
                    {
                        "severity": "warning",
                        "title": "NVIDIA driver compatibility",
                        "description": "Some NVIDIA driver versions have issues with Wayland compositors",
                        "workaround": "Use X11 session or wait for driver update"
                    }
                ]
            },
            "hyprland": {
                "affected_hardware": ["nvidia"],
                "issues": [
                    {
                        "severity": "warning",
                        "title": "Hyprland + NVIDIA issues",
                        "description": "Hyprland may have flickering or crashes on NVIDIA GPUs",
                        "workaround": "Enable nvidia-drm.modeset=1 in kernel parameters"
                    }
                ]
            },
            "wayland": {
                "affected_hardware": ["nvidia"],
                "issues": [
                    {
                        "severity": "info",
                        "title": "Wayland on NVIDIA",
                        "description": "Wayland support on NVIDIA requires driver version 495+",
                        "workaround": "Ensure you have the latest NVIDIA drivers"
                    }
                ]
            },
            "mesa": {
                "affected_hardware": ["amd", "intel"],
                "issues": [
                    {
                        "severity": "info",
                        "title": "Mesa updates",
                        "description": "Mesa updates can occasionally cause temporary graphics issues",
                        "workaround": "Keep a backup kernel/driver version"
                    }
                ]
            },
            "wine": {
                "affected_hardware": ["nvidia"],
                "issues": [
                    {
                        "severity": "info",
                        "title": "Wine + NVIDIA",
                        "description": "Some games may require nvidia-utils-beta for best performance",
                        "workaround": "Install nvidia-utils-beta if experiencing issues"
                    }
                ]
            }
        }
        
        # Check if package matches any known issues
        for pkg_pattern, issue_data in known_issues.items():
            if pkg_pattern.lower() in package_name.lower():
                # Check if user's hardware is affected
                affected_hw = issue_data.get("affected_hardware", [])
                
                is_affected = False
                for hw in affected_hw:
                    if hw == self.hardware_info["gpu"] or hw == self.hardware_info["cpu"]:
                        is_affected = True
                        break
                
                if is_affected or not affected_hw:
                    for issue in issue_data.get("issues", []):
                        warnings.append(CommunityWarning(
                            severity=issue["severity"],
                            title=issue["title"],
                            description=issue["description"],
                            affected_hardware=affected_hw,
                            affected_distros=[],
                            workaround=issue.get("workaround"),
                            source="known_issues"
                        ))
        
        return warnings
    
    def _check_arch_wiki(self, package_name: str) -> List[CommunityWarning]:
        """Check Arch Wiki for known issues (lightweight check)"""
        warnings = []
        
        # This is a placeholder for future implementation
        # Could use arch-wiki-docs package or web scraping
        # For now, return empty to keep it lightweight
        
        return warnings
    
    def check_system_compatibility(self, package_name: str) -> Dict[str, any]:
        """Check if package is compatible with current system"""
        compatibility = {
            "compatible": True,
            "warnings": [],
            "recommendations": []
        }
        
        # Check for known incompatibilities
        if package_name.lower() in ["hyprland", "sway", "wayfire"]:
            if self.hardware_info["gpu"] == "nvidia":
                compatibility["warnings"].append(
                    "Wayland compositors may have issues on NVIDIA hardware"
                )
                compatibility["recommendations"].append(
                    "Consider using X11-based desktop environment or ensure nvidia-drm.modeset=1"
                )
        
        if "cuda" in package_name.lower():
            if self.hardware_info["gpu"] != "nvidia":
                compatibility["compatible"] = False
                compatibility["warnings"].append(
                    "CUDA requires NVIDIA GPU"
                )
        
        if "rocm" in package_name.lower():
            if self.hardware_info["gpu"] != "amd":
                compatibility["compatible"] = False
                compatibility["warnings"].append(
                    "ROCm requires AMD GPU"
                )
        
        return compatibility
    
    def suggest_alternatives(
        self,
        package_name: str,
        reason: str = "compatibility"
    ) -> List[Dict[str, str]]:
        """Suggest alternative packages based on hardware/compatibility"""
        alternatives = []
        
        # Hardware-specific alternatives
        if self.hardware_info["gpu"] == "nvidia":
            if package_name in ["mesa", "mesa-git"]:
                alternatives.append({
                    "name": "nvidia",
                    "reason": "NVIDIA proprietary driver recommended for NVIDIA GPUs"
                })
        
        if self.hardware_info["gpu"] in ["amd", "intel"]:
            if package_name in ["nvidia", "nvidia-dkms"]:
                alternatives.append({
                    "name": "mesa",
                    "reason": "Mesa is the correct driver for AMD/Intel GPUs"
                })
        
        # Lightweight alternatives for low-end hardware
        lightweight_alternatives = {
            "libreoffice": [
                {"name": "abiword", "reason": "Lightweight word processor"},
                {"name": "gnumeric", "reason": "Lightweight spreadsheet"}
            ],
            "firefox": [
                {"name": "firefox-esr", "reason": "More stable, less resource-intensive"},
                {"name": "chromium", "reason": "Alternative browser"}
            ],
            "thunderbird": [
                {"name": "geary", "reason": "Lightweight email client"},
                {"name": "claws-mail", "reason": "Very lightweight email client"}
            ],
            "gimp": [
                {"name": "krita", "reason": "Lighter for digital painting"},
                {"name": "pinta", "reason": "Very lightweight image editor"}
            ]
        }
        
        if reason == "lightweight":
            for pkg, alts in lightweight_alternatives.items():
                if pkg in package_name.lower():
                    alternatives.extend(alts)
        
        return alternatives
    
    def get_hardware_info(self) -> Dict[str, str]:
        """Get detected hardware information"""
        return self.hardware_info.copy()

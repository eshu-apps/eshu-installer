"""Package name translation layer for cross-distro compatibility

Solves the "Rosetta Stone" problem where packages have different names across distros:
- libssl-dev (Debian) -> openssl-devel (Fedora) -> openssl (Arch)
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass


@dataclass
class PackageMapping:
    """Maps a package across different distributions"""
    canonical_name: str
    debian_names: List[str]
    fedora_names: List[str]
    arch_names: List[str]
    description: str


# Comprehensive package translation database
PACKAGE_TRANSLATIONS: List[PackageMapping] = [
    PackageMapping(
        canonical_name="openssl-dev",
        debian_names=["libssl-dev"],
        fedora_names=["openssl-devel"],
        arch_names=["openssl"],
        description="OpenSSL development headers"
    ),
    PackageMapping(
        canonical_name="python-dev",
        debian_names=["python3-dev", "python3.11-dev"],
        fedora_names=["python3-devel"],
        arch_names=["python"],
        description="Python development headers"
    ),
    PackageMapping(
        canonical_name="build-essential",
        debian_names=["build-essential"],
        fedora_names=["gcc", "gcc-c++", "make"],
        arch_names=["base-devel"],
        description="Basic build tools"
    ),
    PackageMapping(
        canonical_name="jpeg-dev",
        debian_names=["libjpeg-dev"],
        fedora_names=["libjpeg-turbo-devel"],
        arch_names=["libjpeg-turbo"],
        description="JPEG library development files"
    ),
    PackageMapping(
        canonical_name="png-dev",
        debian_names=["libpng-dev"],
        fedora_names=["libpng-devel"],
        arch_names=["libpng"],
        description="PNG library development files"
    ),
    PackageMapping(
        canonical_name="curl-dev",
        debian_names=["libcurl4-openssl-dev"],
        fedora_names=["libcurl-devel"],
        arch_names=["curl"],
        description="cURL development files"
    ),
    PackageMapping(
        canonical_name="xml2-dev",
        debian_names=["libxml2-dev"],
        fedora_names=["libxml2-devel"],
        arch_names=["libxml2"],
        description="XML library development files"
    ),
    PackageMapping(
        canonical_name="sqlite-dev",
        debian_names=["libsqlite3-dev"],
        fedora_names=["sqlite-devel"],
        arch_names=["sqlite"],
        description="SQLite development files"
    ),
    PackageMapping(
        canonical_name="ncurses-dev",
        debian_names=["libncurses-dev", "libncurses5-dev"],
        fedora_names=["ncurses-devel"],
        arch_names=["ncurses"],
        description="Terminal UI library development files"
    ),
    PackageMapping(
        canonical_name="readline-dev",
        debian_names=["libreadline-dev"],
        fedora_names=["readline-devel"],
        arch_names=["readline"],
        description="Readline library development files"
    ),
]


class PackageTranslator:
    """Translates package names across different Linux distributions"""

    def __init__(self):
        self.mappings = PACKAGE_TRANSLATIONS

        # Build reverse lookup indices for fast search
        self._debian_index: Dict[str, PackageMapping] = {}
        self._fedora_index: Dict[str, PackageMapping] = {}
        self._arch_index: Dict[str, PackageMapping] = {}

        for mapping in self.mappings:
            for name in mapping.debian_names:
                self._debian_index[name.lower()] = mapping
            for name in mapping.fedora_names:
                self._fedora_index[name.lower()] = mapping
            for name in mapping.arch_names:
                self._arch_index[name.lower()] = mapping

    def translate(
        self,
        package_name: str,
        from_distro: str,
        to_distro: str
    ) -> Optional[List[str]]:
        """
        Translate a package name from one distro to another

        Args:
            package_name: Original package name
            from_distro: Source distribution (debian, fedora, arch)
            to_distro: Target distribution (debian, fedora, arch)

        Returns:
            List of equivalent package names in target distro, or None if no mapping found
        """
        package_name_lower = package_name.lower()

        # Find the canonical mapping
        mapping = None
        if from_distro == "debian":
            mapping = self._debian_index.get(package_name_lower)
        elif from_distro == "fedora":
            mapping = self._fedora_index.get(package_name_lower)
        elif from_distro == "arch":
            mapping = self._arch_index.get(package_name_lower)

        if not mapping:
            return None

        # Get target names
        if to_distro == "debian":
            return mapping.debian_names
        elif to_distro == "fedora":
            return mapping.fedora_names
        elif to_distro == "arch":
            return mapping.arch_names

        return None

    def get_all_names(self, package_name: str) -> Set[str]:
        """Get all known names for a package across all distros"""
        package_name_lower = package_name.lower()

        # Check all indices
        mapping = (
            self._debian_index.get(package_name_lower) or
            self._fedora_index.get(package_name_lower) or
            self._arch_index.get(package_name_lower)
        )

        if not mapping:
            return {package_name}

        # Return all names
        all_names = set()
        all_names.update(mapping.debian_names)
        all_names.update(mapping.fedora_names)
        all_names.update(mapping.arch_names)

        return all_names

    def normalize_distro(self, distro: str) -> str:
        """Normalize distro name to standard form"""
        distro_lower = distro.lower()

        if distro_lower in ["ubuntu", "debian", "mint", "pop", "elementary"]:
            return "debian"
        elif distro_lower in ["fedora", "rhel", "centos", "rocky", "alma"]:
            return "fedora"
        elif distro_lower in ["arch", "manjaro", "endeavouros", "artix"]:
            return "arch"

        return distro_lower

    def suggest_search_terms(
        self,
        query: str,
        target_distro: str
    ) -> List[str]:
        """
        Given a user query, suggest all possible search terms across package naming conventions

        This enables "search-first" logic: try all known variations before failing
        """
        query_lower = query.lower()
        all_names = self.get_all_names(query)

        # Filter to target distro if possible
        normalized_distro = self.normalize_distro(target_distro)

        # Start with original query
        search_terms = [query]

        # Add all translated names
        search_terms.extend(all_names)

        # Remove duplicates while preserving order
        seen = set()
        unique_terms = []
        for term in search_terms:
            if term.lower() not in seen:
                seen.add(term.lower())
                unique_terms.append(term)

        return unique_terms

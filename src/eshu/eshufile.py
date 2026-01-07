"""Eshufile - Declarative System Sync

Enables users to:
1. Export current system state to a portable format: eshu export > system.eshu
2. Apply that state on any Linux distro: eshu apply system.eshu

The magic: Records INTENTS not package names, so it translates across distros:
- Ubuntu: { "editors": ["code"] } → apt install code
- Fedora: { "editors": ["code"] } → dnf install code
- Arch: { "editors": ["code"] } → pacman -S code

Makes system provisioning portable across any Linux distribution!
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm
import subprocess

from .package_translator import PackageTranslator
from .system_profiler import SystemProfiler

console = Console()


@dataclass
class PackageIntent:
    """Represents the INTENT behind installing a package, not just its name"""
    category: str  # editors, browsers, dev-tools, media, etc.
    name: str  # canonical/intent name
    description: str
    alternatives: List[str]  # Alternative packages that serve same purpose


@dataclass
class EshuFile:
    """Declarative system configuration file"""
    version: str = "1.0"
    created_at: str = ""
    created_on_distro: str = ""
    intents: Dict[str, List[str]] = None  # category -> list of package names
    packages: List[str] = None  # Raw package list (fallback)
    metadata: Dict[str, str] = None

    def __post_init__(self):
        if self.intents is None:
            self.intents = {}
        if self.packages is None:
            self.packages = []
        if self.metadata is None:
            self.metadata = {}


# Intent categories and their common packages
INTENT_CATEGORIES = {
    "editors": {
        "vscode": PackageIntent(
            category="editors",
            name="vscode",
            description="Visual Studio Code",
            alternatives=["code", "visual-studio-code-bin", "code-oss"]
        ),
        "vim": PackageIntent(
            category="editors",
            name="vim",
            description="Vi IMproved",
            alternatives=["vim", "neovim", "nvim"]
        ),
        "emacs": PackageIntent(
            category="editors",
            name="emacs",
            description="GNU Emacs",
            alternatives=["emacs", "emacs-nox"]
        ),
    },
    "browsers": {
        "firefox": PackageIntent(
            category="browsers",
            name="firefox",
            description="Mozilla Firefox",
            alternatives=["firefox", "firefox-esr"]
        ),
        "chrome": PackageIntent(
            category="browsers",
            name="chrome",
            description="Google Chrome",
            alternatives=["google-chrome", "google-chrome-stable", "chromium"]
        ),
    },
    "dev-tools": {
        "git": PackageIntent(
            category="dev-tools",
            name="git",
            description="Version control system",
            alternatives=["git"]
        ),
        "docker": PackageIntent(
            category="dev-tools",
            name="docker",
            description="Container platform",
            alternatives=["docker", "docker-ce", "docker.io"]
        ),
    },
    "media": {
        "vlc": PackageIntent(
            category="media",
            name="vlc",
            description="VLC media player",
            alternatives=["vlc"]
        ),
        "spotify": PackageIntent(
            category="media",
            name="spotify",
            description="Spotify music player",
            alternatives=["spotify", "spotify-client"]
        ),
    },
    "terminals": {
        "kitty": PackageIntent(
            category="terminals",
            name="kitty",
            description="Kitty terminal emulator",
            alternatives=["kitty"]
        ),
        "alacritty": PackageIntent(
            category="terminals",
            name="alacritty",
            description="Alacritty terminal emulator",
            alternatives=["alacritty"]
        ),
    }
}


class EshuFileManager:
    """Manages Eshufile creation and application"""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.translator = PackageTranslator()
        self.profiler = SystemProfiler(cache_dir)

    def export_system(
        self,
        output_path: Optional[Path] = None,
        include_intents: bool = True
    ) -> EshuFile:
        """
        Export current system packages to Eshufile

        Args:
            output_path: Where to save the Eshufile (default: stdout)
            include_intents: If True, categorize packages by intent (recommended)

        Returns:
            EshuFile object
        """

        console.print("\n[cyan]🔍 Scanning installed packages...[/cyan]")

        # Get system profile
        profile = self.profiler.get_profile()

        # Create Eshufile
        eshufile = EshuFile(
            version="1.0",
            created_at=datetime.now().isoformat(),
            created_on_distro=f"{profile.distro} {profile.distro_version}",
            metadata={
                "arch": profile.arch,
                "managers": ",".join(profile.available_managers)
            }
        )

        if include_intents:
            # Categorize packages by intent
            eshufile.intents = self._categorize_packages(profile.installed_packages)
        else:
            # Just list packages
            eshufile.packages = list(profile.installed_packages)

        # Save to file or stdout
        if output_path:
            self._save_eshufile(eshufile, output_path)
            console.print(f"\n[green]✓ Eshufile saved to {output_path}[/green]")
        else:
            # Print to stdout
            self._print_eshufile(eshufile)

        return eshufile

    def apply_eshufile(
        self,
        eshufile_path: Path,
        dry_run: bool = False,
        auto_confirm: bool = False
    ) -> bool:
        """
        Apply an Eshufile to the current system

        Args:
            eshufile_path: Path to Eshufile
            dry_run: If True, only show what would be installed
            auto_confirm: If True, don't ask for confirmation

        Returns:
            True if successful, False otherwise
        """

        console.print(f"\n[cyan]📖 Reading Eshufile from {eshufile_path}...[/cyan]")

        # Load Eshufile
        eshufile = self._load_eshufile(eshufile_path)
        if not eshufile:
            console.print("[red]✗ Failed to load Eshufile[/red]")
            return False

        # Get current system profile
        profile = self.profiler.get_profile()

        console.print(Panel(
            f"[bold]Source System:[/bold] {eshufile.created_on_distro}\n"
            f"[bold]Created:[/bold] {eshufile.created_at}\n"
            f"[bold]Target System:[/bold] {profile.distro} {profile.distro_version}",
            title="📦 Eshufile Application",
            border_style="cyan"
        ))

        # Translate packages to target distro
        if eshufile.intents:
            packages_to_install = self._translate_intents(eshufile.intents, profile.distro)
        else:
            packages_to_install = self._translate_packages(eshufile.packages, profile.distro)

        # Show plan
        console.print(f"\n[bold cyan]Installation Plan:[/bold cyan]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan")
        table.add_column("Packages", style="green")

        if eshufile.intents:
            for category, packages in packages_to_install.items():
                table.add_row(category, ", ".join(packages))
        else:
            table.add_row("packages", ", ".join(packages_to_install))

        console.print(table)

        total_packages = (
            sum(len(pkgs) for pkgs in packages_to_install.values())
            if isinstance(packages_to_install, dict)
            else len(packages_to_install)
        )

        console.print(f"\n[yellow]Total packages to install: {total_packages}[/yellow]")

        if dry_run:
            console.print("\n[dim]Dry run - no changes made[/dim]")
            return True

        # Confirm
        if not auto_confirm:
            if not Confirm.ask("\nProceed with installation?", default=True):
                console.print("[yellow]Installation cancelled[/yellow]")
                return False

        # Install packages
        console.print("\n[cyan]📦 Installing packages...[/cyan]\n")

        if isinstance(packages_to_install, dict):
            # Install by category
            for category, packages in packages_to_install.items():
                console.print(f"\n[bold]Installing {category}:[/bold]")
                if not self._install_packages(packages, profile):
                    console.print(f"[yellow]⚠ Some packages in {category} failed to install[/yellow]")
        else:
            # Install all at once
            if not self._install_packages(packages_to_install, profile):
                console.print("[yellow]⚠ Some packages failed to install[/yellow]")
                return False

        console.print("\n[green]✓ Eshufile applied successfully![/green]")
        return True

    def _categorize_packages(self, packages: Set[str]) -> Dict[str, List[str]]:
        """Categorize packages by intent"""

        categorized = {}

        for category, intents in INTENT_CATEGORIES.items():
            categorized[category] = []

            for intent_name, intent in intents.items():
                # Check if any alternative is installed
                for alt in intent.alternatives:
                    if alt.lower() in {p.lower() for p in packages}:
                        categorized[category].append(intent_name)
                        break

        # Add uncategorized packages
        categorized_packages = set()
        for category_packages in categorized.values():
            for pkg in category_packages:
                intent = self._find_intent(pkg)
                if intent:
                    categorized_packages.update(intent.alternatives)

        uncategorized = packages - categorized_packages
        if uncategorized:
            categorized["other"] = list(uncategorized)

        # Remove empty categories
        categorized = {k: v for k, v in categorized.items() if v}

        return categorized

    def _find_intent(self, package_name: str) -> Optional[PackageIntent]:
        """Find intent for a package name"""

        for category_intents in INTENT_CATEGORIES.values():
            for intent in category_intents.values():
                if package_name in intent.alternatives or package_name == intent.name:
                    return intent

        return None

    def _translate_intents(
        self,
        intents: Dict[str, List[str]],
        target_distro: str
    ) -> Dict[str, List[str]]:
        """Translate intents to target distro packages"""

        translated = {}

        for category, intent_names in intents.items():
            translated[category] = []

            for intent_name in intent_names:
                # Find the intent
                intent = None
                for cat_intents in INTENT_CATEGORIES.values():
                    if intent_name in cat_intents:
                        intent = cat_intents[intent_name]
                        break

                if intent:
                    # Use the first alternative (or could use LLM to pick best for distro)
                    package = intent.alternatives[0]
                    translated[category].append(package)
                else:
                    # Unknown intent, try translation
                    package_names = self.translator.suggest_search_terms(intent_name, target_distro)
                    if package_names:
                        translated[category].append(package_names[0])

        return translated

    def _translate_packages(
        self,
        packages: List[str],
        target_distro: str
    ) -> List[str]:
        """Translate raw package list to target distro"""

        translated = []

        for package in packages:
            # Try translation
            suggested = self.translator.suggest_search_terms(package, target_distro)
            translated.append(suggested[0] if suggested else package)

        return translated

    def _install_packages(self, packages: List[str], profile) -> bool:
        """Install packages using appropriate package manager"""

        if not packages:
            return True

        # Determine package manager
        if "pacman" in profile.available_managers:
            cmd = ["sudo", "pacman", "-S", "--needed", "--noconfirm"] + packages
        elif "yay" in profile.available_managers:
            cmd = ["yay", "-S", "--needed", "--noconfirm"] + packages
        elif "apt" in profile.available_managers:
            cmd = ["sudo", "apt", "install", "-y"] + packages
        elif "dnf" in profile.available_managers:
            cmd = ["sudo", "dnf", "install", "-y"] + packages
        else:
            console.print("[red]✗ No supported package manager found[/red]")
            return False

        console.print(f"[dim]Running: {' '.join(cmd)}[/dim]")

        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def _save_eshufile(self, eshufile: EshuFile, path: Path):
        """Save Eshufile to disk"""

        data = asdict(eshufile)

        if path.suffix in [".yaml", ".yml"]:
            with open(path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        else:
            # Default to JSON
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)

    def _load_eshufile(self, path: Path) -> Optional[EshuFile]:
        """Load Eshufile from disk"""

        try:
            with open(path, 'r') as f:
                if path.suffix in [".yaml", ".yml"]:
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)

            return EshuFile(**data)

        except Exception as e:
            console.print(f"[red]✗ Error loading Eshufile: {e}[/red]")
            return None

    def _print_eshufile(self, eshufile: EshuFile):
        """Print Eshufile to stdout"""

        data = asdict(eshufile)
        print(yaml.dump(data, default_flow_style=False, sort_keys=False))

"""System maintenance - update and clean all package managers (Premium feature)"""

import subprocess
from typing import Dict, List, Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

console = Console()


class SystemMaintainer:
    """Handles system-wide package manager maintenance"""

    def __init__(self, available_managers: List[str]):
        self.available_managers = available_managers
        self.results = {}

    def update_all(self) -> Dict[str, Dict]:
        """Update all available package managers"""
        results = {}

        # Pacman
        if "pacman" in self.available_managers:
            results["pacman"] = self._update_pacman()

        # Yay/Paru (AUR)
        if "yay" in self.available_managers:
            results["yay"] = self._update_yay()
        elif "paru" in self.available_managers:
            results["paru"] = self._update_paru()

        # Apt
        if "apt" in self.available_managers:
            results["apt"] = self._update_apt()

        # Flatpak
        if "flatpak" in self.available_managers:
            results["flatpak"] = self._update_flatpak()

        # Snap
        if "snap" in self.available_managers:
            results["snap"] = self._update_snap()

        # Cargo
        if "cargo" in self.available_managers:
            results["cargo"] = self._update_cargo()

        # NPM
        if "npm" in self.available_managers:
            results["npm"] = self._update_npm()

        # Pip
        if "pip" in self.available_managers or "pip3" in self.available_managers:
            results["pip"] = self._update_pip()

        self.results = results
        return results

    def clean_all(self) -> Dict[str, Dict]:
        """Clean caches and remove orphaned packages"""
        results = {}

        # Pacman
        if "pacman" in self.available_managers:
            results["pacman"] = self._clean_pacman()

        # Apt
        if "apt" in self.available_managers:
            results["apt"] = self._clean_apt()

        # Flatpak
        if "flatpak" in self.available_managers:
            results["flatpak"] = self._clean_flatpak()

        # Cargo
        if "cargo" in self.available_managers:
            results["cargo"] = self._clean_cargo()

        # NPM
        if "npm" in self.available_managers:
            results["npm"] = self._clean_npm()

        return results

    def _run_command(self, cmd: List[str], description: str) -> Tuple[bool, str]:
        """Run a maintenance command"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )

            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr

        except subprocess.TimeoutExpired:
            return False, "Command timed out after 10 minutes"
        except Exception as e:
            return False, str(e)

    # Update methods

    def _update_pacman(self) -> Dict:
        """Update pacman packages"""
        success, output = self._run_command(
            ["sudo", "pacman", "-Syu", "--noconfirm"],
            "Updating pacman packages"
        )

        # Count updated packages
        updated = output.count("upgrading") if success else 0

        return {
            "success": success,
            "updated": updated,
            "message": "Updated successfully" if success else "Update failed"
        }

    def _update_yay(self) -> Dict:
        """Update AUR packages via yay"""
        success, output = self._run_command(
            ["yay", "-Syu", "--noconfirm"],
            "Updating AUR packages (yay)"
        )

        updated = output.count("upgrading") if success else 0

        return {
            "success": success,
            "updated": updated,
            "message": "Updated successfully" if success else "Update failed"
        }

    def _update_paru(self) -> Dict:
        """Update AUR packages via paru"""
        success, output = self._run_command(
            ["paru", "-Syu", "--noconfirm"],
            "Updating AUR packages (paru)"
        )

        updated = output.count("upgrading") if success else 0

        return {
            "success": success,
            "updated": updated,
            "message": "Updated successfully" if success else "Update failed"
        }

    def _update_apt(self) -> Dict:
        """Update apt packages"""
        # Update package lists
        update_success, _ = self._run_command(
            ["sudo", "apt", "update"],
            "Updating apt package lists"
        )

        if not update_success:
            return {"success": False, "updated": 0, "message": "Failed to update package lists"}

        # Upgrade packages
        success, output = self._run_command(
            ["sudo", "apt", "upgrade", "-y"],
            "Upgrading apt packages"
        )

        # Count upgraded packages
        updated = output.count("upgraded") if success else 0

        return {
            "success": success,
            "updated": updated,
            "message": "Updated successfully" if success else "Update failed"
        }

    def _update_flatpak(self) -> Dict:
        """Update flatpak applications"""
        success, output = self._run_command(
            ["flatpak", "update", "-y"],
            "Updating flatpak applications"
        )

        # Count updated apps
        updated = output.count("updated") if success else 0

        return {
            "success": success,
            "updated": updated,
            "message": "Updated successfully" if success else "Update failed"
        }

    def _update_snap(self) -> Dict:
        """Update snap packages"""
        success, output = self._run_command(
            ["sudo", "snap", "refresh"],
            "Updating snap packages"
        )

        updated = output.count("refreshed") if success else 0

        return {
            "success": success,
            "updated": updated,
            "message": "Updated successfully" if success else "Update failed"
        }

    def _update_cargo(self) -> Dict:
        """Update cargo packages"""
        # First check if cargo-update is installed
        check_result = subprocess.run(
            ["cargo", "install-update", "--version"],
            capture_output=True
        )

        if check_result.returncode != 0:
            return {
                "success": False,
                "updated": 0,
                "message": "cargo-update not installed (cargo install cargo-update)"
            }

        success, output = self._run_command(
            ["cargo", "install-update", "-a"],
            "Updating cargo packages"
        )

        updated = output.count("updated") if success else 0

        return {
            "success": success,
            "updated": updated,
            "message": "Updated successfully" if success else "Update failed"
        }

    def _update_npm(self) -> Dict:
        """Update global npm packages"""
        success, output = self._run_command(
            ["npm", "update", "-g"],
            "Updating global npm packages"
        )

        # Count updates
        updated = output.count("changed") if success else 0

        return {
            "success": success,
            "updated": updated,
            "message": "Updated successfully" if success else "Update failed"
        }

    def _update_pip(self) -> Dict:
        """Update pip itself"""
        success, output = self._run_command(
            ["pip3", "install", "--upgrade", "pip"],
            "Updating pip"
        )

        return {
            "success": success,
            "updated": 1 if success and "successfully installed" in output.lower() else 0,
            "message": "Updated successfully" if success else "Update failed"
        }

    # Cleanup methods

    def _clean_pacman(self) -> Dict:
        """Clean pacman cache and remove orphans"""
        # Clean cache
        cache_success, _ = self._run_command(
            ["sudo", "pacman", "-Sc", "--noconfirm"],
            "Cleaning pacman cache"
        )

        # Remove orphaned packages
        orphan_success, orphan_output = self._run_command(
            ["sudo", "pacman", "-Rns", "--noconfirm", "$(pacman -Qtdq)"],
            "Removing orphaned packages"
        )

        removed = orphan_output.count("removing") if orphan_success else 0

        return {
            "success": cache_success,
            "removed": removed,
            "message": "Cleaned successfully" if cache_success else "Cleanup failed"
        }

    def _clean_apt(self) -> Dict:
        """Clean apt cache and remove orphans"""
        # Remove unused packages
        autoremove_success, autoremove_output = self._run_command(
            ["sudo", "apt", "autoremove", "-y"],
            "Removing unused apt packages"
        )

        # Clean cache
        clean_success, _ = self._run_command(
            ["sudo", "apt", "clean"],
            "Cleaning apt cache"
        )

        removed = autoremove_output.count("removed") if autoremove_success else 0

        return {
            "success": autoremove_success and clean_success,
            "removed": removed,
            "message": "Cleaned successfully" if clean_success else "Cleanup failed"
        }

    def _clean_flatpak(self) -> Dict:
        """Clean unused flatpak runtimes"""
        success, output = self._run_command(
            ["flatpak", "uninstall", "--unused", "-y"],
            "Removing unused flatpak runtimes"
        )

        removed = output.count("uninstalled") if success else 0

        return {
            "success": success,
            "removed": removed,
            "message": "Cleaned successfully" if success else "Cleanup failed"
        }

    def _clean_cargo(self) -> Dict:
        """Clean cargo cache"""
        success, output = self._run_command(
            ["cargo", "cache", "--autoclean"],
            "Cleaning cargo cache"
        )

        return {
            "success": success,
            "removed": 0,
            "message": "Cleaned successfully" if success else "cargo-cache not installed"
        }

    def _clean_npm(self) -> Dict:
        """Clean npm cache"""
        success, output = self._run_command(
            ["npm", "cache", "clean", "--force"],
            "Cleaning npm cache"
        )

        return {
            "success": success,
            "removed": 0,
            "message": "Cleaned successfully" if success else "Cleanup failed"
        }


def display_maintenance_results(update_results: Dict, clean_results: Dict):
    """Display maintenance results in a nice table"""

    # Update results
    if update_results:
        console.print("\n[bold cyan]📦 Package Updates[/bold cyan]\n")

        update_table = Table(show_header=True, header_style="bold magenta")
        update_table.add_column("Manager", style="cyan", width=15)
        update_table.add_column("Status", style="green", width=12)
        update_table.add_column("Updated", style="yellow", width=10)

        total_updated = 0
        for manager, result in update_results.items():
            status = "✓ Success" if result["success"] else "✗ Failed"
            update_table.add_row(
                manager,
                status,
                str(result["updated"])
            )
            total_updated += result["updated"]

        console.print(update_table)
        console.print(f"\n[green]✓ Total packages updated: {total_updated}[/green]")

    # Clean results
    if clean_results:
        console.print("\n[bold cyan]🧹 Cleanup Results[/bold cyan]\n")

        clean_table = Table(show_header=True, header_style="bold magenta")
        clean_table.add_column("Manager", style="cyan", width=15)
        clean_table.add_column("Status", style="green", width=12)
        clean_table.add_column("Removed", style="yellow", width=10)

        total_removed = 0
        for manager, result in clean_results.items():
            status = "✓ Success" if result["success"] else "✗ Failed"
            clean_table.add_row(
                manager,
                status,
                str(result["removed"])
            )
            total_removed += result["removed"]

        console.print(clean_table)
        console.print(f"\n[green]✓ Total items removed: {total_removed}[/green]")

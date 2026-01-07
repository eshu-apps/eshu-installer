"""Ghost Mode - Try packages in isolated environment without polluting the host system

Implements 'eshu try <package>' which:
1. Creates temporary isolated environment (podman/distrobox/flatpak)
2. Installs package in that environment
3. Launches the app
4. On close, asks "Keep or Discard?"
5. Cleans up if discarded

This solves "dependency hell" and keeps the host OS clean for one-time-use apps.
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel

console = Console()


@dataclass
class GhostEnvironment:
    """Represents a temporary package testing environment"""
    backend: str  # podman, distrobox, flatpak
    container_id: Optional[str]
    name: str
    package_name: str
    created: bool = False


class GhostMode:
    """Manages temporary package testing environments"""

    def __init__(self):
        self.backend = self._detect_backend()
        self.active_environments: List[GhostEnvironment] = []

    def _detect_backend(self) -> str:
        """Detect which container backend is available"""

        # Priority: distrobox > podman > flatpak
        if shutil.which("distrobox"):
            return "distrobox"
        elif shutil.which("podman"):
            return "podman"
        elif shutil.which("flatpak"):
            return "flatpak"
        else:
            return None

    def is_available(self) -> Tuple[bool, str]:
        """Check if Ghost Mode is available on this system"""

        if not self.backend:
            return False, (
                "Ghost Mode requires one of: distrobox, podman, or flatpak.\n"
                "Install with:\n"
                "  • Arch: sudo pacman -S distrobox\n"
                "  • Debian/Ubuntu: sudo apt install distrobox\n"
                "  • Fedora: sudo dnf install distrobox"
            )

        return True, f"Ghost Mode ready (using {self.backend})"

    def try_package(
        self,
        package_name: str,
        manager: Optional[str] = None,
        keep: bool = False
    ) -> bool:
        """
        Try a package in isolated environment

        Args:
            package_name: Name of package to try
            manager: Preferred package manager (optional)
            keep: If True, keep environment after exit

        Returns:
            True if successful, False otherwise
        """

        available, message = self.is_available()
        if not available:
            console.print(f"[red]✗ {message}[/red]")
            return False

        console.print(Panel(
            f"[bold]Ghost Mode[/bold]\n\n"
            f"Package: [cyan]{package_name}[/cyan]\n"
            f"Backend: [yellow]{self.backend}[/yellow]\n\n"
            f"[dim]This will create a temporary isolated environment\n"
            f"and install {package_name} without affecting your system.[/dim]",
            title="👻 Try Package",
            border_style="cyan"
        ))

        # Create environment
        env = self._create_environment(package_name)
        if not env or not env.created:
            console.print("[red]✗ Failed to create ghost environment[/red]")
            return False

        self.active_environments.append(env)

        try:
            # Install package in environment
            console.print(f"\n[yellow]📦 Installing {package_name} in ghost environment...[/yellow]")
            if not self._install_in_environment(env, package_name, manager):
                console.print("[red]✗ Installation failed[/red]")
                return False

            console.print(f"[green]✓ {package_name} installed in ghost environment[/green]")

            # Launch the application
            console.print(f"\n[cyan]🚀 Launching {package_name}...[/cyan]")
            console.print("[dim]Close the app when you're done testing[/dim]\n")

            self._launch_app(env, package_name)

            # Ask if user wants to keep it
            if not keep:
                keep = Confirm.ask(
                    f"\n[cyan]Keep {package_name}?[/cyan] (No = discard environment)",
                    default=False
                )

            if keep:
                console.print(f"\n[green]✓ Keeping {package_name}[/green]")
                console.print(f"[dim]Access with: {self._get_access_command(env, package_name)}[/dim]")
                console.print(f"[dim]Remove with: eshu ghost clean {env.name}[/dim]\n")
                return True
            else:
                console.print(f"\n[yellow]🧹 Discarding ghost environment...[/yellow]")
                self._cleanup_environment(env)
                console.print(f"[green]✓ Environment cleaned up[/green]\n")
                return True

        except KeyboardInterrupt:
            console.print(f"\n[yellow]Ghost mode interrupted[/yellow]")
            if not keep and Confirm.ask("Discard ghost environment?", default=True):
                self._cleanup_environment(env)
            return False

    def _create_environment(self, package_name: str) -> Optional[GhostEnvironment]:
        """Create an isolated environment for testing"""

        env_name = f"eshu-ghost-{package_name}"

        if self.backend == "distrobox":
            return self._create_distrobox(env_name, package_name)
        elif self.backend == "podman":
            return self._create_podman(env_name, package_name)
        elif self.backend == "flatpak":
            # Flatpak doesn't need container creation, packages are already isolated
            return GhostEnvironment(
                backend="flatpak",
                container_id=None,
                name=env_name,
                package_name=package_name,
                created=True
            )

        return None

    def _create_distrobox(self, name: str, package_name: str) -> Optional[GhostEnvironment]:
        """Create distrobox container"""

        try:
            console.print(f"[dim]Creating distrobox container '{name}'...[/dim]")

            # Create distrobox based on same distro as host
            result = subprocess.run(
                ["distrobox", "create", "--name", name, "--yes"],
                capture_output=True,
                text=True,
                check=True
            )

            return GhostEnvironment(
                backend="distrobox",
                container_id=name,
                name=name,
                package_name=package_name,
                created=True
            )

        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗ Failed to create distrobox: {e.stderr}[/red]")
            return None

    def _create_podman(self, name: str, package_name: str) -> Optional[GhostEnvironment]:
        """Create podman container"""

        try:
            console.print(f"[dim]Creating podman container '{name}'...[/dim]")

            # Use alpine for speed (can be configured)
            result = subprocess.run(
                [
                    "podman", "run", "-dit",
                    "--name", name,
                    "docker.io/library/alpine:latest",
                    "/bin/sh"
                ],
                capture_output=True,
                text=True,
                check=True
            )

            container_id = result.stdout.strip()

            return GhostEnvironment(
                backend="podman",
                container_id=container_id,
                name=name,
                package_name=package_name,
                created=True
            )

        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗ Failed to create podman container: {e.stderr}[/red]")
            return None

    def _install_in_environment(
        self,
        env: GhostEnvironment,
        package_name: str,
        manager: Optional[str] = None
    ) -> bool:
        """Install package inside the isolated environment"""

        if env.backend == "distrobox":
            # Distrobox supports native package managers
            try:
                subprocess.run(
                    ["distrobox", "enter", env.name, "--", "eshu", "install", package_name, "--yes"],
                    check=True
                )
                return True
            except subprocess.CalledProcessError:
                return False

        elif env.backend == "podman":
            # Install in podman container
            try:
                # Detect package manager in container
                subprocess.run(
                    ["podman", "exec", env.container_id, "apk", "add", package_name],
                    check=True
                )
                return True
            except subprocess.CalledProcessError:
                return False

        elif env.backend == "flatpak":
            # Install as flatpak (already isolated)
            try:
                subprocess.run(
                    ["flatpak", "install", "--user", "-y", package_name],
                    check=True
                )
                return True
            except subprocess.CalledProcessError:
                return False

        return False

    def _launch_app(self, env: GhostEnvironment, package_name: str):
        """Launch the application from the ghost environment"""

        if env.backend == "distrobox":
            subprocess.run(
                ["distrobox", "enter", env.name, "--", package_name],
                check=False  # Don't fail if app exits normally
            )

        elif env.backend == "podman":
            # Need X11 forwarding for GUI apps
            subprocess.run(
                [
                    "podman", "exec", "-it",
                    "-e", "DISPLAY",
                    env.container_id,
                    package_name
                ],
                check=False
            )

        elif env.backend == "flatpak":
            subprocess.run(
                ["flatpak", "run", package_name],
                check=False
            )

    def _get_access_command(self, env: GhostEnvironment, package_name: str) -> str:
        """Get command to access the ghost environment later"""

        if env.backend == "distrobox":
            return f"distrobox enter {env.name} -- {package_name}"
        elif env.backend == "podman":
            return f"podman exec -it {env.container_id} {package_name}"
        elif env.backend == "flatpak":
            return f"flatpak run {package_name}"

        return ""

    def _cleanup_environment(self, env: GhostEnvironment):
        """Clean up and remove ghost environment"""

        if env.backend == "distrobox":
            try:
                subprocess.run(
                    ["distrobox", "rm", "-f", env.name],
                    capture_output=True,
                    check=True
                )
            except subprocess.CalledProcessError:
                pass

        elif env.backend == "podman":
            try:
                subprocess.run(
                    ["podman", "rm", "-f", env.container_id],
                    capture_output=True,
                    check=True
                )
            except subprocess.CalledProcessError:
                pass

        elif env.backend == "flatpak":
            try:
                subprocess.run(
                    ["flatpak", "uninstall", "--user", "-y", env.package_name],
                    capture_output=True,
                    check=True
                )
            except subprocess.CalledProcessError:
                pass

        # Remove from active list
        if env in self.active_environments:
            self.active_environments.remove(env)

    def list_environments(self) -> List[GhostEnvironment]:
        """List all active ghost environments"""

        environments = []

        # Check distrobox
        if shutil.which("distrobox"):
            try:
                result = subprocess.run(
                    ["distrobox", "list", "--no-color"],
                    capture_output=True,
                    text=True,
                    check=True
                )

                for line in result.stdout.split("\n"):
                    if "eshu-ghost-" in line:
                        parts = line.split()
                        if parts:
                            name = parts[1]
                            package = name.replace("eshu-ghost-", "")
                            environments.append(GhostEnvironment(
                                backend="distrobox",
                                container_id=name,
                                name=name,
                                package_name=package,
                                created=True
                            ))
            except subprocess.CalledProcessError:
                pass

        # Check podman
        if shutil.which("podman"):
            try:
                result = subprocess.run(
                    ["podman", "ps", "-a", "--filter", "name=eshu-ghost-", "--format", "{{.Names}}"],
                    capture_output=True,
                    text=True,
                    check=True
                )

                for line in result.stdout.strip().split("\n"):
                    if line and "eshu-ghost-" in line:
                        package = line.replace("eshu-ghost-", "")
                        environments.append(GhostEnvironment(
                            backend="podman",
                            container_id=line,
                            name=line,
                            package_name=package,
                            created=True
                        ))
            except subprocess.CalledProcessError:
                pass

        return environments

    def cleanup_all(self):
        """Clean up all ghost environments"""

        envs = self.list_environments()

        if not envs:
            console.print("[yellow]No ghost environments found[/yellow]")
            return

        console.print(f"\n[yellow]Found {len(envs)} ghost environment(s):[/yellow]")
        for env in envs:
            console.print(f"  • {env.name} ({env.backend})")

        if Confirm.ask("\nRemove all ghost environments?", default=False):
            for env in envs:
                console.print(f"[dim]Removing {env.name}...[/dim]")
                self._cleanup_environment(env)

            console.print(f"\n[green]✓ Cleaned up {len(envs)} ghost environment(s)[/green]")

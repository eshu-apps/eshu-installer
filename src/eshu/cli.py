"""Command-line interface for ESHU"""

import sys
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from rich.text import Text

from .config import ESHUConfig, load_config, save_config, get_config_path
from .system_profiler import SystemProfiler
from .package_search import PackageSearcher
from .llm_engine import LLMEngine
from .installer import PackageInstaller

app = typer.Typer(
    name="eshu",
    help="ESHU - AI-Driven Universal Package Installer for Linux",
    add_completion=True
)
console = Console()


@app.command()
def install(
    query: str = typer.Argument(..., help="Package name or natural language query"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Auto-confirm installation"),
    refresh: bool = typer.Option(False, "--refresh", "-r", help="Refresh system profile cache"),
    manager: Optional[str] = typer.Option(None, "--manager", "-m", help="Prefer specific package manager"),
    snapshot: bool = typer.Option(True, "--snapshot/--no-snapshot", help="Create system snapshot before install"),
):
    """Install a package using AI-driven search and installation"""
    
    try:
        # Load configuration
        config = load_config()
        
        # Check if LLM is configured
        if config.llm_provider == "anthropic" and not config.anthropic_api_key:
            console.print("[red]❌ Anthropic API key not configured[/red]")
            console.print("Set ANTHROPIC_API_KEY environment variable or run: eshu config set-key")
            sys.exit(1)
        
        # Initialize system profiler
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("🔍 Scanning system...", total=None)
            profiler = SystemProfiler(cache_dir=config.cache_dir)
            profile = profiler.get_profile(force_refresh=refresh, cache_ttl=config.profile_cache_ttl)
            progress.update(task, completed=True)
        
        console.print(f"\n[cyan]System:[/cyan] {profile.distro} {profile.distro_version} ({profile.arch})")
        console.print(f"[cyan]Available managers:[/cyan] {', '.join(profile.available_managers)}\n")
        
        # Check repository configuration
        searcher = PackageSearcher(profile.available_managers, profile.installed_packages)
        repo_status = searcher.check_repositories()
        
        # Show repository suggestions if needed
        for manager, status in repo_status.items():
            if not status["configured"] and status["suggestion"]:
                console.print(f"[yellow]💡 {status['suggestion']}[/yellow]")
        
        # Initialize LLM engine
        llm = LLMEngine(config)
        
        # Interpret query
        console.print(f"\n[yellow]🤖 Interpreting query:[/yellow] {query}")
        interpretation = llm.interpret_query(query, profile)
        
        search_terms = interpretation.get("search_terms", [query])
        console.print(f"[cyan]Search terms:[/cyan] {', '.join(search_terms)}\n")
        
        # Search for packages
        all_results = []
        for term in search_terms:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"🔎 Searching for '{term}'...", total=None)
                results = searcher.search_all(term)
                progress.update(task, completed=True)
            
            all_results.extend(results)
        
        if not all_results:
            console.print(f"[red]❌ No packages found for '{query}'[/red]")
            sys.exit(1)
        
        # Rank results
        ranked_results = searcher.rank_results(all_results, query)
        
        # Get LLM recommendations (with community warnings)
        console.print("\n[yellow]🤖 Analyzing results and checking for known issues...[/yellow]")
        recommended_results = llm.rank_and_recommend(query, ranked_results[:20], profile, check_community=True)
        
        # Display results with enhanced formatting
        console.print("\n[bold cyan]📦 Search Results:[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Package", style="cyan", width=20)
        table.add_column("Version", style="green", width=12)
        table.add_column("Manager", style="yellow", width=10)
        table.add_column("Size", style="blue", width=10)
        table.add_column("OS", style="magenta", width=10)
        table.add_column("Description", style="white", width=50)
        
        display_results = recommended_results[:15]  # Show top 15
        
        for i, (result, recommendation) in enumerate(display_results, 1):
            # Format size
            size_str = f"{result.size_mb:.1f} MB" if result.size_mb > 0 else "N/A"
            
            # Format OS optimization with emoji
            os_emoji = {
                "arch": "🔷 Arch",
                "debian": "🔴 Debian",
                "universal": "🌐 All"
            }
            os_str = os_emoji.get(result.os_optimized, result.os_optimized)
            
            # Color-code description based on status
            desc_text = Text(result.description[:50] + "..." if len(result.description) > 50 else result.description)
            if result.installed:
                desc_text.stylize("dim italic")
            
            # Add status indicator to package name
            pkg_name = f"{'✓ ' if result.installed else ''}{result.name}"
            
            table.add_row(
                str(i),
                pkg_name,
                result.version,
                result.manager,
                size_str,
                os_str,
                desc_text
            )
        
        console.print(table)
        
        # Show top recommendation
        if recommended_results:
            top_result, top_rec = recommended_results[0]
            if top_rec:
                console.print(f"\n[green]✨ {top_rec}[/green]")
            
            # Check for lightweight alternative
            alt = llm.suggest_lightweight_alternative(top_result.name, profile)
            if alt:
                console.print(f"\n[yellow]💡 Lightweight alternative:[/yellow] {alt['name']} - {alt['reason']}")
            
            # Show full description with better formatting
            console.print(f"\n[bold cyan]Package Details:[/bold cyan]")
            console.print(Panel(
                f"[bold]{top_result.name}[/bold] v{top_result.version}\n\n"
                f"{top_result.description}\n\n"
                f"[dim]Manager: {top_result.manager} | Repository: {top_result.repository} | "
                f"Size: {top_result.size_mb:.1f} MB | Optimized for: {top_result.os_optimized}[/dim]",
                border_style="cyan"
            ))
        
        # Prompt for selection
        if yes:
            selection = 1
        else:
            try:
                selection = typer.prompt(
                    "Select package number to install (0 to cancel)",
                    type=int,
                    default=1
                )
            except (KeyboardInterrupt, EOFError):
                console.print("\n[yellow]Installation cancelled[/yellow]")
                sys.exit(0)
        
        if selection == 0:
            console.print("[yellow]Installation cancelled[/yellow]")
            sys.exit(0)
        
        if selection < 1 or selection > len(display_results):
            console.print("[red]Invalid selection[/red]")
            sys.exit(1)
        
        # Install selected package
        selected_package, _ = display_results[selection - 1]
        
        # Create snapshot if enabled
        if snapshot:
            from .snapshot_manager import SnapshotManager
            snap_mgr = SnapshotManager(cache_dir=config.cache_dir)
            
            if snap_mgr.is_available():
                console.print(f"\n[yellow]📸 Creating system snapshot...[/yellow]")
                snap = snap_mgr.create_snapshot(f"Before installing {selected_package.name}")
                if snap:
                    console.print(f"[green]✓ Snapshot created: {snap.id}[/green]")
                else:
                    console.print("[yellow]⚠️  Snapshot creation failed, continuing anyway...[/yellow]")
            else:
                console.print("[dim]ℹ️  Snapshots not available (install Timeshift or use Btrfs)[/dim]")
        
        installer = PackageInstaller(config, llm, profile)
        success = installer.install(selected_package, auto_confirm=yes)
        
        if success:
            console.print(f"\n[green]✓ Successfully installed {selected_package.name}![/green]")
            installer.verify_installation(selected_package)
        else:
            console.print(f"\n[red]❌ Failed to install {selected_package.name}[/red]")
            
            # Offer to restore snapshot
            if snapshot:
                from .snapshot_manager import SnapshotManager
                snap_mgr = SnapshotManager(cache_dir=config.cache_dir)
                snapshots = snap_mgr.list_snapshots()
                
                if snapshots and not yes:
                    if Confirm.ask("Would you like to restore the pre-install snapshot?"):
                        console.print("[yellow]⚠️  Snapshot restoration requires manual steps[/yellow]")
                        console.print(f"Run: eshu snapshot restore {snapshots[-1].id}")
            
            sys.exit(1)
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        if "--debug" in sys.argv:
            raise
        sys.exit(1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Package name to search for"),
    all_managers: bool = typer.Option(True, "--all", "-a", help="Search all package managers"),
    manager: Optional[str] = typer.Option(None, "--manager", "-m", help="Search specific manager only"),
):
    """Search for packages across all package managers"""
    
    try:
        config = load_config()
        profiler = SystemProfiler(cache_dir=config.cache_dir)
        profile = profiler.get_profile(cache_ttl=config.profile_cache_ttl)
        
        searcher = PackageSearcher(profile.available_managers, profile.installed_packages)
        
        # Check repository configuration
        repo_status = searcher.check_repositories()
        for manager_name, status in repo_status.items():
            if not status["configured"] and status["suggestion"]:
                console.print(f"[yellow]💡 {status['suggestion']}[/yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"🔎 Searching for '{query}'...", total=None)
            results = searcher.search_all(query)
            progress.update(task, completed=True)
        
        if not results:
            console.print(f"[red]No packages found for '{query}'[/red]")
            sys.exit(1)
        
        ranked_results = searcher.rank_results(results, query)
        
        # Display results with enhanced formatting
        console.print(f"\n[bold cyan]Found {len(ranked_results)} packages:[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("Package", style="cyan", width=20)
        table.add_column("Version", style="green", width=12)
        table.add_column("Manager", style="yellow", width=10)
        table.add_column("Size", style="blue", width=10)
        table.add_column("OS", style="magenta", width=10)
        table.add_column("Description", style="white", width=50)
        
        for result in ranked_results[:30]:
            # Format size
            size_str = f"{result.size_mb:.1f} MB" if result.size_mb > 0 else "N/A"
            
            # Format OS optimization
            os_emoji = {
                "arch": "🔷 Arch",
                "debian": "🔴 Debian",
                "universal": "🌐 All"
            }
            os_str = os_emoji.get(result.os_optimized, result.os_optimized)
            
            # Color-code description
            desc_text = Text(result.description[:50] + "..." if len(result.description) > 50 else result.description)
            if result.installed:
                desc_text.stylize("dim italic")
            
            # Add status to package name
            pkg_name = f"{'✓ ' if result.installed else ''}{result.name}"
            
            table.add_row(
                pkg_name,
                result.version,
                result.manager,
                size_str,
                os_str,
                desc_text
            )
        
        console.print(table)
        
        if len(ranked_results) > 30:
            console.print(f"\n[dim]... and {len(ranked_results) - 30} more results[/dim]")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@app.command()
def profile(
    refresh: bool = typer.Option(False, "--refresh", "-r", help="Force refresh system profile"),
    show_packages: bool = typer.Option(False, "--packages", "-p", help="Show installed packages"),
):
    """Display system profile information"""
    
    try:
        config = load_config()
        profiler = SystemProfiler(cache_dir=config.cache_dir)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("🔍 Scanning system...", total=None)
            sys_profile = profiler.get_profile(force_refresh=refresh, cache_ttl=config.profile_cache_ttl)
            progress.update(task, completed=True)
        
        # Display system info
        info_panel = f"""[cyan]Distribution:[/cyan] {sys_profile.distro} {sys_profile.distro_version}
[cyan]Kernel:[/cyan] {sys_profile.kernel}
[cyan]Architecture:[/cyan] {sys_profile.arch}
[cyan]Available Package Managers:[/cyan] {', '.join(sys_profile.available_managers)}
[cyan]Installed Packages:[/cyan] {len(sys_profile.installed_packages)}
[cyan]Profile Updated:[/cyan] {sys_profile.timestamp}"""
        
        console.print(Panel(info_panel, title="[bold]System Profile[/bold]", border_style="cyan"))
        
        if show_packages:
            console.print(f"\n[bold cyan]Installed Packages ({len(sys_profile.installed_packages)}):[/bold cyan]\n")
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Package", style="cyan")
            table.add_column("Version", style="green")
            table.add_column("Manager", style="yellow")
            
            for name, pkg in list(sys_profile.installed_packages.items())[:50]:
                table.add_row(pkg.name, pkg.version, pkg.manager)
            
            console.print(table)
            
            if len(sys_profile.installed_packages) > 50:
                console.print(f"\n[dim]... and {len(sys_profile.installed_packages) - 50} more[/dim]")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@app.command()
def cleanup(
    dry_run: bool = typer.Option(True, "--dry-run/--execute", help="Show what would be removed without removing"),
    unused_days: int = typer.Option(90, "--days", "-d", help="Consider packages unused after N days"),
):
    """Find and remove unused packages and bloat"""
    
    try:
        config = load_config()
        profiler = SystemProfiler(cache_dir=config.cache_dir)
        profile = profiler.get_profile()
        
        from .bloat_analyzer import BloatAnalyzer
        analyzer = BloatAnalyzer(cache_dir=config.cache_dir)
        
        console.print("[yellow]🔍 Analyzing system for bloat...[/yellow]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Scanning...", total=None)
            report = analyzer.generate_cleanup_report(profile.installed_packages)
            progress.update(task, completed=True)
        
        # Display orphaned packages
        if report["orphaned_packages"]:
            console.print(f"\n[bold cyan]🗑️  Orphaned Packages ({len(report['orphaned_packages'])}):[/bold cyan]")
            table = Table(show_header=True)
            table.add_column("Package", style="cyan")
            table.add_column("Manager", style="yellow")
            table.add_column("Size", style="green")
            
            for pkg in report["orphaned_packages"][:20]:
                table.add_row(pkg.name, pkg.manager, f"{pkg.size_mb:.1f} MB")
            
            console.print(table)
        
        # Display duplicate packages
        if report["duplicate_packages"]:
            console.print(f"\n[bold cyan]📦 Duplicate Packages ({len(report['duplicate_packages'])}):[/bold cyan]")
            table = Table(show_header=True)
            table.add_column("Package", style="cyan")
            table.add_column("Managers", style="yellow")
            table.add_column("Recommendation", style="green")
            
            for dup in report["duplicate_packages"][:10]:
                table.add_row(
                    dup["name"],
                    ", ".join(dup["managers"]),
                    dup["recommendation"]
                )
            
            console.print(table)
        
        # Display large packages
        if report["large_packages"]:
            console.print(f"\n[bold cyan]💾 Large Packages ({len(report['large_packages'])}):[/bold cyan]")
            table = Table(show_header=True)
            table.add_column("Package", style="cyan")
            table.add_column("Manager", style="yellow")
            table.add_column("Size", style="green")
            
            for pkg in report["large_packages"][:10]:
                table.add_row(pkg.name, pkg.manager, f"{pkg.size_mb:.1f} MB")
            
            console.print(table)
        
        # Summary
        console.print(f"\n[bold green]💡 Total Reclaimable Space: {report['total_reclaimable_mb']:.1f} MB[/bold green]")
        
        if dry_run:
            console.print("\n[yellow]ℹ️  This was a dry run. Use --execute to actually remove packages.[/yellow]")
        else:
            if Confirm.ask("\nProceed with cleanup?"):
                console.print("[yellow]🧹 Cleaning up...[/yellow]")
                # TODO: Implement actual cleanup
                console.print("[green]✓ Cleanup complete![/green]")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@app.command()
def snapshot(
    action: str = typer.Argument(..., help="Action: list, create, restore, delete"),
    snapshot_id: Optional[str] = typer.Argument(None, help="Snapshot ID for restore/delete"),
):
    """Manage system snapshots"""
    
    try:
        config = load_config()
        from .snapshot_manager import SnapshotManager
        snap_mgr = SnapshotManager(cache_dir=config.cache_dir)
        
        if not snap_mgr.is_available():
            console.print("[red]❌ Snapshots not available[/red]")
            console.print("Install Timeshift or use a Btrfs filesystem")
            sys.exit(1)
        
        if action == "list":
            snapshots = snap_mgr.list_snapshots()
            
            if not snapshots:
                console.print("[yellow]No snapshots found[/yellow]")
                return
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan")
            table.add_column("Date", style="green")
            table.add_column("Description", style="white")
            table.add_column("Backend", style="yellow")
            
            for snap in snapshots:
                table.add_row(
                    snap.id,
                    snap.timestamp,
                    snap.description,
                    snap.backend
                )
            
            console.print(f"\n[bold cyan]System Snapshots ({len(snapshots)}):[/bold cyan]\n")
            console.print(table)
        
        elif action == "create":
            description = typer.prompt("Snapshot description", default="Manual snapshot")
            console.print("[yellow]📸 Creating snapshot...[/yellow]")
            snap = snap_mgr.create_snapshot(description)
            
            if snap:
                console.print(f"[green]✓ Snapshot created: {snap.id}[/green]")
            else:
                console.print("[red]❌ Failed to create snapshot[/red]")
        
        elif action == "restore":
            if not snapshot_id:
                console.print("[red]Snapshot ID required for restore[/red]")
                sys.exit(1)
            
            console.print(f"[yellow]⚠️  Restoring snapshot {snapshot_id}...[/yellow]")
            success = snap_mgr.restore_snapshot(snapshot_id)
            
            if success:
                console.print("[green]✓ Snapshot restored[/green]")
            else:
                console.print("[red]❌ Failed to restore snapshot[/red]")
        
        elif action == "delete":
            if not snapshot_id:
                console.print("[red]Snapshot ID required for delete[/red]")
                sys.exit(1)
            
            if Confirm.ask(f"Delete snapshot {snapshot_id}?"):
                success = snap_mgr.delete_snapshot(snapshot_id)
                
                if success:
                    console.print("[green]✓ Snapshot deleted[/green]")
                else:
                    console.print("[red]❌ Failed to delete snapshot[/red]")
        
        else:
            console.print(f"[red]Unknown action: {action}[/red]")
            console.print("Available actions: list, create, restore, delete")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@app.command("config")
def config_cmd(
    action: str = typer.Argument(..., help="Action: show, set-key, set-provider"),
    value: Optional[str] = typer.Argument(None, help="Value for set actions"),
):
    """Configure ESHU settings"""
    
    try:
        config = load_config()
        
        if action == "show":
            console.print(Panel(
                f"""[cyan]LLM Provider:[/cyan] {config.llm_provider}
[cyan]Model:[/cyan] {config.model_name}
[cyan]API Key Set:[/cyan] {'Yes' if config.anthropic_api_key or config.openai_api_key else 'No'}
[cyan]Cache Directory:[/cyan] {config.cache_dir}
[cyan]Build Directory:[/cyan] {config.build_dir}
[cyan]Package Manager Priority:[/cyan] {', '.join(config.package_manager_priority)}
[cyan]Config File:[/cyan] {get_config_path()}""",
                title="[bold]ESHU Configuration[/bold]",
                border_style="cyan"
            ))
        
        elif action == "set-key":
            if not value:
                value = typer.prompt("Enter API key", hide_input=True)
            
            if config.llm_provider == "anthropic":
                config.anthropic_api_key = value
            elif config.llm_provider == "openai":
                config.openai_api_key = value
            
            save_config(config)
            console.print(f"[green]✓ API key saved for {config.llm_provider}[/green]")
        
        elif action == "set-provider":
            if not value:
                value = typer.prompt("Enter provider (anthropic/openai/ollama)")
            
            if value not in ["anthropic", "openai", "ollama"]:
                console.print("[red]Invalid provider. Choose: anthropic, openai, or ollama[/red]")
                sys.exit(1)
            
            config.llm_provider = value
            
            if value == "anthropic":
                config.model_name = "claude-3-5-sonnet-20241022"
            elif value == "openai":
                config.model_name = "gpt-4-turbo-preview"
            
            save_config(config)
            console.print(f"[green]✓ LLM provider set to {value}[/green]")
        
        else:
            console.print(f"[red]Unknown action: {action}[/red]")
            console.print("Available actions: show, set-key, set-provider")
            sys.exit(1)
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@app.command()
def version():
    """Show ESHU version"""
    from . import __version__
    console.print(f"[cyan]ESHU version {__version__}[/cyan]")


if __name__ == "__main__":
    app()

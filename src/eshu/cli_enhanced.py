"""Enhanced CLI with pagination and license management"""

import sys
from pathlib import Path
from typing import Optional, List, Tuple
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.text import Text
from rich.columns import Columns

from .config import ESHUConfig, load_config, save_config, get_config_path
from .system_profiler import SystemProfiler
from .package_search import PackageSearcher, PackageResult
from .llm_engine import LLMEngine
from .installer import PackageInstaller
from .license_manager import LicenseManager, License

app = typer.Typer(
    name="eshu",
    help="ESHU - AI-Driven Universal Package Installer for Linux",
    add_completion=True
)
console = Console()


def check_license_feature(license_mgr: LicenseManager, feature: str) -> bool:
    """Check if license allows feature and show upgrade message if not"""
    license = license_mgr.get_license()
    
    if not license.has_feature(feature):
        console.print(f"\n[yellow]🔒 This feature requires ESHU Premium[/yellow]")
        console.print(f"[dim]Upgrade at: {license_mgr.get_upgrade_url()}[/dim]\n")
        return False
    
    return True


def display_paginated_results(
    results: List[Tuple[PackageResult, Optional[str]]],
    page_size: int = 15
) -> Optional[Tuple[PackageResult, Optional[str]]]:
    """Display results with pagination and return selected package"""
    
    total_pages = (len(results) + page_size - 1) // page_size
    current_page = 0
    
    while True:
        # Calculate page bounds
        start_idx = current_page * page_size
        end_idx = min(start_idx + page_size, len(results))
        page_results = results[start_idx:end_idx]
        
        # Clear screen and show results
        console.clear()
        console.print(f"\n[bold cyan]📦 Search Results (Page {current_page + 1}/{total_pages}):[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("#", style="dim", width=4)
        table.add_column("Package", style="cyan", width=20)
        table.add_column("Version", style="green", width=12)
        table.add_column("Manager", style="yellow", width=10)
        table.add_column("Size", style="blue", width=10)
        table.add_column("OS", style="magenta", width=10)
        table.add_column("Description", style="white", width=50)
        
        for i, (result, recommendation) in enumerate(page_results, start=start_idx + 1):
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
        
        # Show navigation options
        nav_options = []
        if current_page > 0:
            nav_options.append("[cyan]p[/cyan]=Previous")
        if current_page < total_pages - 1:
            nav_options.append("[cyan]n[/cyan]=Next")
        nav_options.extend(["[cyan]#[/cyan]=Select", "[cyan]q[/cyan]=Quit"])
        
        console.print(f"\n[dim]Navigation: {' | '.join(nav_options)}[/dim]")
        console.print(f"[dim]Showing {start_idx + 1}-{end_idx} of {len(results)} results[/dim]\n")
        
        # Get user input
        choice = Prompt.ask("Enter choice", default="1")
        
        if choice.lower() == 'q':
            return None
        elif choice.lower() == 'n' and current_page < total_pages - 1:
            current_page += 1
        elif choice.lower() == 'p' and current_page > 0:
            current_page -= 1
        elif choice.isdigit():
            selection = int(choice)
            if 1 <= selection <= len(results):
                return results[selection - 1]
            else:
                console.print("[red]Invalid selection[/red]")
                console.input("Press Enter to continue...")
        else:
            console.print("[red]Invalid choice[/red]")
            console.input("Press Enter to continue...")


@app.command()
def search(
    query: str = typer.Argument(..., help="Package name to search for"),
    all_results: bool = typer.Option(False, "--all", "-a", help="Show all results with pagination"),
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
        
        # Convert to tuple format for pagination
        results_with_rec = [(r, None) for r in ranked_results]
        
        if all_results:
            # Show paginated results
            selected = display_paginated_results(results_with_rec)
            if selected:
                result, _ = selected
                console.print(f"\n[green]Selected: {result.name}[/green]")
                console.print(f"To install: [cyan]eshu install {result.name}[/cyan]")
        else:
            # Show first 30 results
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
                remaining = len(ranked_results) - 30
                console.print(f"\n[yellow]... and {remaining} more results[/yellow]")
                console.print(f"[dim]Use [cyan]eshu search '{query}' --all[/cyan] to view all results with pagination[/dim]")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


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
        # Load configuration and license
        config = load_config()
        license_mgr = LicenseManager(cache_dir=config.cache_dir)
        license = license_mgr.get_license()
        
        # Show license tier
        console.print(f"[dim]ESHU {license.tier.title()}[/dim]")
        
        # Check snapshot feature
        if snapshot and not check_license_feature(license_mgr, "snapshots"):
            snapshot = False
        
        # Check LLM usage limit
        can_use_llm, llm_status = license_mgr.check_usage_limit("llm_queries")
        if not can_use_llm:
            console.print(f"[yellow]{llm_status}[/yellow]")
            # Continue with basic search
        
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
        
        # Interpret query (if LLM available)
        if can_use_llm:
            console.print(f"\n[yellow]🤖 Interpreting query:[/yellow] {query}")
            interpretation = llm.interpret_query(query, profile)
            search_terms = interpretation.get("search_terms", [query])
            console.print(f"[cyan]Search terms:[/cyan] {', '.join(search_terms)}\n")
        else:
            search_terms = [query]
        
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
        
        # Get LLM recommendations (if available and premium)
        if can_use_llm and check_license_feature(license_mgr, "community_warnings"):
            console.print("\n[yellow]🤖 Analyzing results and checking for known issues...[/yellow]")
            recommended_results = llm.rank_and_recommend(query, ranked_results[:20], profile, check_community=True)
        else:
            recommended_results = [(r, None) for r in ranked_results[:20]]
        
        # Display results with pagination
        selected = display_paginated_results(recommended_results)
        
        if not selected:
            console.print("[yellow]Installation cancelled[/yellow]")
            sys.exit(0)
        
        selected_package, recommendation = selected
        
        # Show recommendation if available
        if recommendation:
            console.print(f"\n[green]✨ {recommendation}[/green]")
        
        # Check for lightweight alternative (premium feature)
        if check_license_feature(license_mgr, "lightweight_suggestions"):
            alt = llm.suggest_lightweight_alternative(selected_package.name, profile)
            if alt:
                console.print(f"\n[yellow]💡 Lightweight alternative:[/yellow] {alt['name']} - {alt['reason']}")
        
        # Show full description
        console.print(f"\n[bold cyan]Package Details:[/bold cyan]")
        console.print(Panel(
            f"[bold]{selected_package.name}[/bold] v{selected_package.version}\n\n"
            f"{selected_package.description}\n\n"
            f"[dim]Manager: {selected_package.manager} | Repository: {selected_package.repository} | "
            f"Size: {selected_package.size_mb:.1f} MB | Optimized for: {selected_package.os_optimized}[/dim]",
            border_style="cyan"
        ))
        
        # Confirm installation
        if not yes:
            if not Confirm.ask(f"\nInstall {selected_package.name}?"):
                console.print("[yellow]Installation cancelled[/yellow]")
                sys.exit(0)
        
        # Create snapshot if enabled (premium feature)
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
        
        # Install package
        installer = PackageInstaller(config, llm, profile)
        success = installer.install(selected_package, auto_confirm=yes)
        
        if success:
            console.print(f"\n[green]✓ Successfully installed {selected_package.name}![/green]")
            installer.verify_installation(selected_package)
        else:
            console.print(f"\n[red]❌ Failed to install {selected_package.name}[/red]")
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
def license_cmd(
    action: str = typer.Argument(..., help="Action: show, activate, upgrade, trial"),
    key: Optional[str] = typer.Argument(None, help="License key for activation"),
):
    """Manage ESHU license"""
    
    try:
        config = load_config()
        license_mgr = LicenseManager(cache_dir=config.cache_dir)
        
        if action == "show":
            license = license_mgr.get_license()
            comparison = license_mgr.show_feature_comparison()
            
            # Show current license
            console.print(Panel(
                f"""[cyan]Tier:[/cyan] {license.tier.title()}
[cyan]Status:[/cyan] {'✓ Active' if license.is_valid() else '✗ Inactive'}
[cyan]Email:[/cyan] {license.email or 'N/A'}
[cyan]Activated:[/cyan] {license.activated_at or 'N/A'}
[cyan]Expires:[/cyan] {license.expires_at or 'Never'}""",
                title="[bold]Current License[/bold]",
                border_style="cyan"
            ))
            
            # Show feature comparison
            console.print("\n[bold cyan]Feature Comparison:[/bold cyan]\n")
            
            free_panel = Panel(
                "\n".join(comparison["free"]["features"]),
                title=f"[bold]{comparison['free']['name']}[/bold]",
                subtitle=comparison["free"]["price"],
                border_style="dim"
            )
            
            premium_panel = Panel(
                "\n".join(comparison["premium"]["features"]),
                title=f"[bold]{comparison['premium']['name']}[/bold]",
                subtitle=comparison["premium"]["price"],
                border_style="green"
            )
            
            console.print(Columns([free_panel, premium_panel]))
            
            if license.tier == "free":
                console.print(f"\n[yellow]💎 Upgrade to Premium:[/yellow] {license_mgr.get_upgrade_url()}")
        
        elif action == "activate":
            if not key:
                key = Prompt.ask("Enter license key")
            
            email = Prompt.ask("Enter email address")
            
            console.print("[yellow]Activating license...[/yellow]")
            success, message = license_mgr.activate_license(key, email)
            
            if success:
                console.print(f"[green]✓ {message}[/green]")
                console.print("[cyan]Thank you for supporting ESHU![/cyan]")
            else:
                console.print(f"[red]✗ {message}[/red]")
        
        elif action == "trial":
            email = Prompt.ask("Enter email address for trial")
            
            trial_key = license_mgr.generate_trial_key(email)
            console.print(f"\n[green]✓ Trial key generated:[/green] {trial_key}")
            console.print("[yellow]This is a 7-day trial key. Activate it with:[/yellow]")
            console.print(f"[cyan]eshu license activate {trial_key}[/cyan]\n")
        
        elif action == "upgrade":
            console.print(f"\n[bold cyan]Upgrade to ESHU Premium[/bold cyan]\n")
            console.print("Visit: [cyan]https://eshu-installer.com/upgrade[/cyan]")
            console.print("\n[green]Benefits:[/green]")
            console.print("  • Unlimited AI queries")
            console.print("  • System snapshots (Time Machine)")
            console.print("  • Smart bloat analyzer")
            console.print("  • Community warnings")
            console.print("  • Adaptive error fixing")
            console.print("  • Priority support")
            console.print("\n[yellow]Pricing:[/yellow]")
            console.print("  • $4.99/month")
            console.print("  • $39.99/year (save 33%)")
        
        else:
            console.print(f"[red]Unknown action: {action}[/red]")
            console.print("Available actions: show, activate, upgrade, trial")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


# Import remaining commands from original CLI
from .cli import profile, cleanup, snapshot, config_cmd, version

# Register them
app.command()(profile)
app.command()(cleanup)
app.command()(snapshot)
app.command("config")(config_cmd)
app.command()(version)


if __name__ == "__main__":
    app()

"""Enhanced CLI with pagination and license management"""

import sys
import subprocess
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
from .eshu_paths import get_eshu_path, suggest_eshu_path_with_llm, ESHU_PATHS
from .cache import SimpleCache

app = typer.Typer(
    name="eshu",
    help="ESHU - AI-Driven Universal Package Installer for Linux",
    add_completion=False,  # Disable confusing shell completion prompts
    rich_markup_mode="rich"
)
console = Console()


def is_simple_query(query: str) -> bool:
    """
    Check if query is a simple package name (doesn't need LLM interpretation)

    Examples of simple queries:
        - "firefox" -> True
        - "python3" -> True
        - "docker-compose" -> True
        - "a web browser" -> False
        - "something for editing videos" -> False
    """
    # Remove common separators
    clean_query = query.lower().replace('-', '').replace('_', '').replace('.', '')

    # If it's alphanumeric and short, it's likely a package name
    if clean_query.isalnum() and len(query.split()) == 1:
        return True

    # If it contains common natural language words, needs interpretation
    natural_language_words = ['a', 'an', 'the', 'for', 'to', 'with', 'that', 'like', 'similar']
    query_words = query.lower().split()

    if any(word in natural_language_words for word in query_words):
        return False

    # If multiple words but looks like a package name (e.g., "visual studio code")
    if len(query_words) <= 3 and all(word.replace('-', '').isalnum() for word in query_words):
        return True

    return False


def check_license_feature(license_mgr: LicenseManager, feature: str, show_message: bool = True) -> bool:
    """Check if license allows feature and optionally show upgrade message"""
    license = license_mgr.get_license()

    if not license.has_feature(feature):
        if show_message:
            # Clear message about WHAT is premium
            feature_names = {
                "snapshots": "System Snapshots & Rollback",
                "bloat_analyzer": "Smart Bloat Analyzer",
                "community_warnings": "AI-Powered Hardware Warnings",
                "lightweight_suggestions": "Lightweight Package Suggestions",
                "unlimited_llm": "Unlimited AI Queries",
                "eshu_paths": "Eshu's Path - Curated Package Bundles"
            }
            feature_name = feature_names.get(feature, feature.replace("_", " ").title())

            console.print(f"\n[yellow]🔒 '{feature_name}' is a Premium feature[/yellow]")
            console.print(f"[dim]Upgrade: {license_mgr.get_upgrade_url()} | Donate: https://github.com/sponsors/eshu-apps[/dim]\n")
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
        table.add_column("Package", style="cyan", width=20, no_wrap=False)
        table.add_column("Version", style="green", width=12)
        table.add_column("Manager", style="yellow", width=10)
        table.add_column("Size", style="blue", width=10)
        table.add_column("OS", style="magenta", width=10)
        table.add_column("Description", style="white", no_wrap=False, overflow="fold")
        
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
            
            # Color-code description based on status (no truncation)
            desc_text = Text(result.description)
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
    query: Optional[str] = typer.Argument(None, help="Package name to search for"),
    all_results: bool = typer.Option(False, "--all", "-a", help="Show all results with pagination"),
    manager: Optional[str] = typer.Option(None, "--manager", "-m", help="Search specific manager only"),
):
    """Search for packages across all package managers

    Examples:
        eshu search                    # Interactive mode - prompts for search
        eshu search firefox            # Search for firefox
        eshu search "web browser"      # Natural language search
        eshu search firefox --all      # Show all results with pagination
    """

    try:
        # Interactive mode - prompt for search if not provided
        if not query:
            console.print("\n[bold cyan]╔═══════════════════════════════════════════════════════════╗[/bold cyan]")
            console.print("[bold cyan]║              ESHU - Universal Package Search             ║[/bold cyan]")
            console.print("[bold cyan]╚═══════════════════════════════════════════════════════════╝[/bold cyan]\n")

            query = Prompt.ask(
                "[cyan]What package are you looking for?[/cyan]\n[dim]  (Package name or description)[/dim]",
                default=""
            )

            if not query or query.strip() == "":
                console.print("[yellow]No search query provided. Exiting.[/yellow]")
                sys.exit(0)

            query = query.strip()

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
    packages: Optional[List[str]] = typer.Argument(None, help="Package name(s) to install (space-separated)"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Auto-confirm installation"),
    refresh: bool = typer.Option(False, "--refresh", "-r", help="Refresh system profile cache"),
    manager: Optional[str] = typer.Option(None, "--manager", "-m", help="Prefer specific package manager"),
    snapshot: bool = typer.Option(False, "--snapshot", help="Create system snapshot before install"),
    fast: bool = typer.Option(False, "--fast", "-f", help="Fast mode: skip all AI features for instant results"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip cache, force fresh search"),
):
    """Install one or more packages using AI-driven search

    Examples:
        eshu install                            # Interactive mode - prompts for package
        eshu install firefox                    # Install single package
        eshu install firefox chrome vlc         # Install multiple packages
        eshu install firefox --fast             # Ultra-fast mode (no AI)
        eshu install firefox --snapshot         # With snapshot (Premium)
    """

    try:
        # Interactive mode - prompt for package if not provided
        if not packages:
            console.print("\n[bold cyan]╔═══════════════════════════════════════════════════════════╗[/bold cyan]")
            console.print("[bold cyan]║           ESHU - Universal Package Installer             ║[/bold cyan]")
            console.print("[bold cyan]╚═══════════════════════════════════════════════════════════╝[/bold cyan]\n")

            package_input = Prompt.ask(
                "[cyan]What would you like to install?[/cyan]\n[dim]  (Package name, multiple packages, or natural language)[/dim]",
                default=""
            )

            if not package_input or package_input.strip() == "":
                console.print("[yellow]No package specified. Exiting.[/yellow]")
                sys.exit(0)

            # Split input into packages (handles both space-separated and single packages)
            packages = package_input.strip().split()

        # Load configuration and license
        config = load_config()
        license_mgr = LicenseManager(cache_dir=config.cache_dir)
        license = license_mgr.get_license()

        # Initialize system profiler (needed for AI bundle suggestions)
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("🔍 Scanning system...", total=None)
            profiler = SystemProfiler(cache_dir=config.cache_dir)
            profile = profiler.get_profile(force_refresh=refresh, cache_ttl=config.profile_cache_ttl)
            progress.update(task, completed=True)

        # Initialize LLM engine for AI features
        llm = LLMEngine(config)

        # Get the primary package query (for Eshu's Path check)
        primary_package = packages[0]

        # Check for Eshu's Path - PREMIUM FEATURE (now with AI!)
        eshu_path_data = None
        if check_license_feature(license_mgr, "eshu_paths", show_message=False):
            # Premium user - use AI-powered bundle suggestion
            console.print(f"\n[dim]🤖 AI is analyzing if '{primary_package}' needs companion packages...[/dim]")
            eshu_path_data = suggest_eshu_path_with_llm(primary_package, llm, profile)
        else:
            # Free user - only show predefined paths as teasers
            eshu_path_obj = get_eshu_path(primary_package)
            if eshu_path_obj:
                eshu_path_data = {
                    "name": eshu_path_obj.name,
                    "description": eshu_path_obj.description,
                    "packages": eshu_path_obj.packages,
                    "reasoning": eshu_path_obj.reasoning,
                    "source": "curated"
                }

        if eshu_path_data:
            if check_license_feature(license_mgr, "eshu_paths", show_message=False):
                # Premium user - show Eshu's Path option
                source_badge = "🤖 AI-Generated" if eshu_path_data.get("source") == "ai-generated" else "📦 Curated"
                console.print(f"\n[bold cyan]{source_badge} Eshu's Path Available![/bold cyan]")
                console.print(Panel(
                    f"[bold]{eshu_path_data['name']}[/bold]\n\n"
                    f"{eshu_path_data['description']}\n\n"
                    f"[green]Includes {len(eshu_path_data['packages'])} packages:[/green]\n"
                    f"{', '.join(eshu_path_data['packages'][:5])}{'...' if len(eshu_path_data['packages']) > 5 else ''}\n\n"
                    f"[dim]{eshu_path_data['reasoning']}[/dim]",
                    title="🎯 Complete Setup",
                    border_style="cyan"
                ))

                if Confirm.ask("\nInstall the complete Eshu's Path bundle?", default=True):
                    console.print(f"\n[green]✨ Installing {len(eshu_path_data['packages'])} packages from Eshu's Path...[/green]\n")

                    # Show package list
                    for pkg in eshu_path_data['packages']:
                        console.print(f"  • {pkg}")
                    console.print()

                    # Determine best package manager and install command
                    install_cmd = None
                    if "pacman" in profile.available_managers:
                        install_cmd = ["sudo", "pacman", "-S", "--needed"] + eshu_path_data['packages']
                    elif "yay" in profile.available_managers:
                        install_cmd = ["yay", "-S", "--needed"] + eshu_path_data['packages']
                    elif "paru" in profile.available_managers:
                        install_cmd = ["paru", "-S", "--needed"] + eshu_path_data['packages']
                    elif "apt" in profile.available_managers:
                        install_cmd = ["sudo", "apt", "install", "-y"] + eshu_path_data['packages']
                    elif "dnf" in profile.available_managers:
                        install_cmd = ["sudo", "dnf", "install", "-y"] + eshu_path_data['packages']
                    else:
                        console.print("[red]✗ No supported package manager found![/red]")
                        console.print(f"[yellow]Install manually: {' '.join(eshu_path_data['packages'])}[/yellow]\n")
                        return

                    # Show the command
                    console.print(f"[cyan]▶ Running:[/cyan] {' '.join(install_cmd)}\n")

                    # Execute installation
                    try:
                        result = subprocess.run(
                            install_cmd,
                            check=True,
                            text=True
                        )
                        console.print(f"\n[green]✓ Successfully installed {len(eshu_path_data['packages'])} packages from Eshu's Path![/green]")
                        console.print(f"[dim]{eshu_path_data['name']} is now ready to use![/dim]\n")
                        return
                    except subprocess.CalledProcessError as e:
                        console.print(f"\n[red]✗ Installation failed![/red]")
                        console.print(f"[yellow]Some packages may have installed successfully. Check the output above.[/yellow]\n")
                        return
                    except KeyboardInterrupt:
                        console.print(f"\n[yellow]Installation cancelled by user.[/yellow]\n")
                        return
            else:
                # Free user - show teaser
                console.print(f"\n[bold cyan]💎 Eshu's Path Available (Premium)[/bold cyan]")
                console.print(Panel(
                    f"[bold]{eshu_path_data['name']}[/bold]\n\n"
                    f"Complete setup with {len(eshu_path_data['packages'])} curated packages:\n"
                    f"{', '.join(eshu_path_data['packages'][:3])}...\n\n"
                    f"[yellow]🔒 Unlock Eshu's Path with Premium[/yellow]\n"
                    f"[dim]Get complete, tested package bundles for instant setups\n"
                    f"Upgrade: {license_mgr.get_upgrade_url()} | Donate: https://github.com/sponsors/eshu-apps[/dim]",
                    title="🚀 Complete Setup (Premium)",
                    border_style="yellow"
                ))
                if not Confirm.ask("\nContinue with single package install?", default=True):
                    return

        # Show license tier
        console.print(f"\n[cyan]System:[/cyan] {profile.distro} {profile.distro_version} ({profile.arch})")
        console.print(f"[cyan]Available managers:[/cyan] {', '.join(profile.available_managers)}")
        console.print(f"[dim]ESHU {license.tier.title()}[/dim]\n")

        # Check snapshot feature
        if snapshot and not check_license_feature(license_mgr, "snapshots"):
            snapshot = False

        # Check LLM usage limit
        can_use_llm, llm_status = license_mgr.check_usage_limit("llm_queries")
        if not can_use_llm:
            console.print(f"[yellow]{llm_status}[/yellow]")
            # Continue with basic search

        # Check repository configuration
        searcher = PackageSearcher(profile.available_managers, profile.installed_packages)
        repo_status = searcher.check_repositories()

        # Show repository suggestions if needed
        for manager, status in repo_status.items():
            if not status["configured"] and status["suggestion"]:
                console.print(f"[yellow]💡 {status['suggestion']}[/yellow]")
        

        # Handle multiple packages
        if len(packages) > 1:
            console.print(f"\n[bold cyan]📦 Installing {len(packages)} packages:[/bold cyan]")
            for pkg in packages:
                console.print(f"  • {pkg}")
            console.print()
            
            if not yes and not Confirm.ask(f"\nInstall all {len(packages)} packages?"):
                console.print("[yellow]Installation cancelled[/yellow]")
                sys.exit(0)
            
            # Install each package
            success_count = 0
            failed_packages = []
            
            for i, pkg in enumerate(packages, 1):
                console.print(f"\n[bold cyan]═══ Package {i}/{len(packages)}: {pkg} ═══[/bold cyan]\n")
                
                try:
                    # Recursive call for each package
                    subprocess.run(
                        ["eshu", "install", pkg] + (["--yes"] if yes else []) + (["--fast"] if fast else []),
                        check=True
                    )
                    success_count += 1
                except subprocess.CalledProcessError:
                    failed_packages.append(pkg)
                    console.print(f"[red]✗ Failed to install {pkg}[/red]")
                    if not Confirm.ask("Continue with remaining packages?", default=True):
                        break
            
            # Summary
            console.print(f"\n[bold cyan]═══ Installation Summary ═══[/bold cyan]")
            console.print(f"[green]✓ Successful:[/green] {success_count}/{len(packages)}")
            if failed_packages:
                console.print(f"[red]✗ Failed:[/red] {', '.join(failed_packages)}")
            
            sys.exit(0 if not failed_packages else 1)
        
        # Single package installation (original flow)
        query = packages[0]
        
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
        
        # Get LLM recommendations (if available and premium) - silently check
        if can_use_llm and check_license_feature(license_mgr, "community_warnings", show_message=False):
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
        
        # Check for lightweight alternative (premium feature) - show after selection
        if check_license_feature(license_mgr, "lightweight_suggestions", show_message=False):
            alt = llm.suggest_lightweight_alternative(selected_package.name, profile)
            if alt:
                console.print(f"\n[yellow]💡 Lightweight alternative:[/yellow] {alt['name']} - {alt['reason']}")
        elif can_use_llm:
            # Show upgrade prompt contextually
            console.print(f"\n[dim]💡 Want AI-powered lightweight suggestions? Upgrade to Premium![/dim]")
            console.print(f"[dim]   {license_mgr.get_upgrade_url()} | https://github.com/sponsors/eshu-apps[/dim]")
        
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
                console.print(f"[cyan]💝 Support Development:[/cyan] https://github.com/sponsors/eshu-apps")
        
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
            console.print(f"\n[bold cyan]💎 Upgrade to ESHU Premium[/bold cyan]\n")
            console.print("Visit: [cyan]https://eshu-installer.com/upgrade[/cyan]")
            console.print("\n[green]✨ Premium Benefits:[/green]")
            console.print("  • 📦 Eshu's Path - Curated package bundles for complete setups")
            console.print("  • 🤖 Unlimited AI queries (Free: 10/day)")
            console.print("  • 📸 System snapshots (Time Machine for Linux)")
            console.print("  • 🧹 Smart bloat analyzer")
            console.print("  • ⚠️  Community hardware warnings")
            console.print("  • 💡 Lightweight package suggestions")
            console.print("  • 🔧 Adaptive error fixing")
            console.print("  • 🎯 Priority support")
            console.print("\n[yellow]💰 Pricing:[/yellow]")
            console.print("  • $9.99/month")
            console.print("  • $39.99/year (save 33%)")
            console.print("\n[cyan]💝 Just want to support? Donate:[/cyan]")
            console.print("   https://github.com/sponsors/eshu-apps")
            console.print("   Every contribution helps keep ESHU free!")
        
        else:
            console.print(f"[red]Unknown action: {action}[/red]")
            console.print("Available actions: show, activate, upgrade, trial")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@app.command()
def donate():
    """Support ESHU development with a donation"""
    console.print("\n[bold cyan]💝 Support ESHU Development[/bold cyan]\n")
    console.print("ESHU is free and open source. Your support helps keep it that way!\n")
    console.print("[green]Ways to support:[/green]")
    console.print("  💝 GitHub Sponsors: https://github.com/sponsors/eshu-apps")
    console.print("  💎 Upgrade to Premium: $9.99/month (https://eshu-installer.com/upgrade)")
    console.print("  ⭐ Star on GitHub: https://github.com/eshu-apps/eshu-installer")
    console.print("  📣 Share with friends")
    console.print("\n[yellow]Every contribution matters![/yellow]")
    console.print("[dim]Even $1 helps cover server costs and keeps development active.[/dim]\n")


@app.command()
def setup():
    """Run interactive setup wizard to configure ESHU"""
    import subprocess

    console.print("\n[bold cyan]🚀 ESHU Setup Wizard[/bold cyan]\n")

    # LLM Configuration
    console.print("[bold]🤖 Step 1: LLM Configuration[/bold]")
    console.print("\nESHU uses AI for intelligent package recommendations.")
    console.print("\nChoose your LLM provider:")
    console.print("  [cyan]1[/cyan]) Anthropic Claude (recommended, requires API key)")
    console.print("     Get free key at: https://console.anthropic.com/")
    console.print("  [cyan]2[/cyan]) OpenAI GPT (requires API key)")
    console.print("     Get key at: https://platform.openai.com/api-keys")
    console.print("  [cyan]3[/cyan]) Ollama (local, free, requires Ollama)")
    console.print("     Install from: https://ollama.ai")
    console.print("  [cyan]4[/cyan]) Skip for now\n")

    choice = Prompt.ask("Enter choice", choices=["1", "2", "3", "4"], default="4")

    if choice == "1":
        console.print("\n[bold]📝 Anthropic Claude Setup[/bold]")
        console.print("Get your API key from: https://console.anthropic.com/")
        api_key = Prompt.ask("Enter your Anthropic API key", password=True)
        if api_key:
            subprocess.run(["eshu", "config", "set-provider", "anthropic"], check=False)
            subprocess.run(["eshu", "config", "set-key", api_key], check=False)
            console.print("[green]✅ Anthropic Claude configured![/green]")
    elif choice == "2":
        console.print("\n[bold]📝 OpenAI GPT Setup[/bold]")
        console.print("Get your API key from: https://platform.openai.com/api-keys")
        api_key = Prompt.ask("Enter your OpenAI API key", password=True)
        if api_key:
            subprocess.run(["eshu", "config", "set-provider", "openai"], check=False)
            subprocess.run(["eshu", "config", "set-key", api_key], check=False)
            console.print("[green]✅ OpenAI GPT configured![/green]")
    elif choice == "3":
        subprocess.run(["eshu", "config", "set-provider", "ollama"], check=False)
        console.print("[green]✅ Ollama configured![/green]")
        console.print("[dim]💡 Make sure you've pulled a model: ollama pull llama3.1:8b[/dim]")
    else:
        console.print("[yellow]⏩ Skipping LLM configuration[/yellow]")

    # Systemd Service
    console.print("\n[bold]⚙️  Step 2: System Profiling Service (Optional)[/bold]")
    console.print("\nInstall systemd service for automatic system profiling?")
    console.print("Benefits:")
    console.print("  ✅ Faster package searches (pre-cached system info)")
    console.print("  ✅ Automatic updates on boot")

    if Confirm.ask("\nInstall systemd service?", default=False):
        try:
            from pathlib import Path
            # Look for systemd files
            install_dir = Path(__file__).parent.parent.parent
            service_dir = install_dir / "systemd"

            if service_dir.exists():
                subprocess.run([
                    "sudo", "cp",
                    str(service_dir / "eshu-profiler.service"),
                    "/etc/systemd/system/"
                ], check=True)
                subprocess.run([
                    "sudo", "cp",
                    str(service_dir / "eshu-profiler.timer"),
                    "/etc/systemd/system/"
                ], check=True)
                subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
                subprocess.run(["sudo", "systemctl", "enable", "--now", "eshu-profiler.timer"], check=True)
                console.print("[green]✅ Systemd service installed and enabled![/green]")
            else:
                console.print("[yellow]⚠️  Systemd service files not found[/yellow]")
        except subprocess.CalledProcessError:
            console.print("[red]❌ Failed to install systemd service (requires sudo)[/red]")
    else:
        console.print("[yellow]⏩ Skipping systemd service[/yellow]")

    # Summary
    console.print("\n[bold green]✅ Setup Complete![/bold green]")
    console.print("\n[cyan]Try these commands:[/cyan]")
    console.print("  eshu search firefox")
    console.print("  eshu install hyprland")
    console.print("  eshu profile")
    console.print("  eshu license-cmd status")
    console.print("\n[dim]Run 'eshu --help' for full command list[/dim]\n")


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

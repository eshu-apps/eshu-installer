#!/usr/bin/env python3
"""
Fix script to update cli_enhanced.py for:
1. Multiple package installation support
2. Remove premium blocking for basic installation
"""

import re
from pathlib import Path

def fix_cli_enhanced():
    cli_file = Path("src/eshu/cli_enhanced.py")
    
    if not cli_file.exists():
        print(f"Error: {cli_file} not found")
        return False
    
    content = cli_file.read_text()
    
    # Fix 1: Change install function signature to accept multiple packages
    old_signature = r'def install\(\s*query: str = typer\.Argument\(\.\.\., help="Package name or natural language query"\),'
    new_signature = 'def install(\n    packages: List[str] = typer.Argument(..., help="Package name(s) to install (space-separated)"),'
    
    content = re.sub(old_signature, new_signature, content)
    
    # Fix 2: Change snapshot default from True to False (opt-in)
    old_snapshot = r'snapshot: bool = typer\.Option\(True, "--snapshot/--no-snapshot"'
    new_snapshot = 'snapshot: bool = typer.Option(False, "--snapshot"'
    
    content = re.sub(old_snapshot, new_snapshot, content)
    
    # Fix 3: Update docstring
    old_docstring = '''    """Install a package using AI-driven search and installation

    Examples:
        eshu install firefox              # Full AI-powered experience
        eshu install firefox --fast       # Ultra-fast mode (no AI)
        eshu install firefox --no-cache   # Force fresh search
    """'''
    
    new_docstring = '''    """Install one or more packages using AI-driven search

    Examples:
        eshu install firefox                    # Install single package
        eshu install firefox chrome vlc         # Install multiple packages
        eshu install firefox --fast             # Ultra-fast mode (no AI)
        eshu install firefox --snapshot         # With snapshot (Premium)
    """'''
    
    content = content.replace(old_docstring, new_docstring)
    
    # Fix 4: Add multiple package handling logic after the license check
    # Find the line where we start searching for packages
    search_marker = '        # Interpret query (if LLM available)'
    
    if search_marker in content:
        # Insert multiple package handling before the search
        multi_package_code = '''
        # Handle multiple packages
        if len(packages) > 1:
            console.print(f"\\n[bold cyan]📦 Installing {len(packages)} packages:[/bold cyan]")
            for pkg in packages:
                console.print(f"  • {pkg}")
            console.print()
            
            if not yes and not Confirm.ask(f"\\nInstall all {len(packages)} packages?"):
                console.print("[yellow]Installation cancelled[/yellow]")
                sys.exit(0)
            
            # Install each package
            success_count = 0
            failed_packages = []
            
            for i, pkg in enumerate(packages, 1):
                console.print(f"\\n[bold cyan]═══ Package {i}/{len(packages)}: {pkg} ═══[/bold cyan]\\n")
                
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
            console.print(f"\\n[bold cyan]═══ Installation Summary ═══[/bold cyan]")
            console.print(f"[green]✓ Successful:[/green] {success_count}/{len(packages)}")
            if failed_packages:
                console.print(f"[red]✗ Failed:[/red] {', '.join(failed_packages)}")
            
            sys.exit(0 if not failed_packages else 1)
        
        # Single package installation (original flow)
        query = packages[0]
        
'''
        content = content.replace(search_marker, multi_package_code + search_marker)
    
    # Write the fixed content
    cli_file.write_text(content)
    print(f"✓ Fixed {cli_file}")
    return True

if __name__ == "__main__":
    if fix_cli_enhanced():
        print("\\n✅ All fixes applied successfully!")
        print("\\nNext steps:")
        print("  1. Review changes: git diff src/eshu/cli_enhanced.py")
        print("  2. Test: eshu install firefox chrome")
        print("  3. Commit: git add . && git commit -m 'Fix: Add multiple package install support'")
    else:
        print("\\n❌ Fix failed!")

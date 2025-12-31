"""Package installer with adaptive error handling"""

import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from .package_search import PackageResult
from .llm_engine import LLMEngine
from .system_profiler import SystemProfile
from .config import ESHUConfig


class PackageInstaller:
    """Handles package installation with adaptive error handling"""
    
    def __init__(self, config: ESHUConfig, llm_engine: LLMEngine, system_profile: SystemProfile):
        self.config = config
        self.llm = llm_engine
        self.profile = system_profile
        self.build_dir = config.build_dir
        self.build_dir.mkdir(parents=True, exist_ok=True)
    
    def install(self, package: PackageResult, auto_confirm: bool = False) -> bool:
        """
        Install a package with adaptive error handling
        Returns True if successful, False otherwise
        """
        
        print(f"\n📦 Installing {package.name} via {package.manager}...")
        
        # Generate installation plan
        plan = self.llm.generate_install_plan(package, self.profile)
        
        print(f"\n📋 Installation Plan:")
        print(f"   Commands: {' && '.join(plan['commands'])}")
        if plan['requires_build']:
            print(f"   ⚙️  Requires build: {plan['build_system']}")
        if plan['dependencies']:
            print(f"   📦 Dependencies: {', '.join(plan['dependencies'])}")
        if plan['notes']:
            print(f"   ℹ️  Note: {plan['notes']}")
        
        if not auto_confirm:
            response = input("\n❓ Proceed with installation? [Y/n]: ")
            if response.lower() in ['n', 'no']:
                print("❌ Installation cancelled")
                return False
        
        # Install dependencies first
        if plan['dependencies'] and not self._install_dependencies(plan['dependencies']):
            print("❌ Failed to install dependencies")
            return False
        
        # Execute installation commands
        success = self._execute_commands(plan['commands'], package)
        
        if success and plan['post_install']:
            print("\n🔧 Running post-install steps...")
            self._execute_commands(plan['post_install'], package, critical=False)
        
        return success
    
    def _install_dependencies(self, dependencies: List[str]) -> bool:
        """Install package dependencies"""
        print(f"\n📦 Installing dependencies: {', '.join(dependencies)}")
        
        # Determine which package manager to use for dependencies
        if "pacman" in self.profile.available_managers:
            cmd = ["sudo", "pacman", "-S", "--needed", "--noconfirm"] + dependencies
        elif "apt" in self.profile.available_managers:
            cmd = ["sudo", "apt", "install", "-y"] + dependencies
        else:
            print("⚠️  Unable to determine package manager for dependencies")
            return True  # Continue anyway
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✓ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Dependency installation failed: {e}")
            return False
    
    def _execute_commands(
        self,
        commands: List[str],
        package: PackageResult,
        critical: bool = True
    ) -> bool:
        """Execute a list of commands"""
        
        for cmd in commands:
            print(f"\n▶ Executing: {cmd}")
            
            try:
                # Parse command
                if isinstance(cmd, str):
                    cmd_parts = cmd.split()
                else:
                    cmd_parts = cmd
                
                # Determine if this is an interactive command
                interactive_managers = ['yay', 'paru', 'pacman', 'apt', 'dnf', 'zypper']
                is_interactive = any(mgr in cmd_parts[0] for mgr in interactive_managers)

                # Execute with proper I/O handling
                if is_interactive:
                    # Let user interact directly with the command
                    result = subprocess.run(
                        cmd_parts,
                        check=True,
                        timeout=300,  # 5 minute timeout
                        cwd=str(self.build_dir) if "make" in cmd or "cmake" in cmd else None
                    )
                else:
                    # Capture output for non-interactive commands
                    result = subprocess.run(
                        cmd_parts,
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=300,  # 5 minute timeout
                        cwd=str(self.build_dir) if "make" in cmd or "cmake" in cmd else None
                    )

                    # Show output if verbose
                    if result.stdout:
                        print(result.stdout)

                print(f"✓ Command completed successfully")
            
            except subprocess.TimeoutExpired:
                print(f"❌ Command timed out after 5 minutes")
                if critical:
                    return False
                continue

            except subprocess.CalledProcessError as e:
                print(f"❌ Command failed with exit code {e.returncode}")
                
                if critical:
                    # Use LLM to analyze error and suggest fixes
                    error_analysis = self.llm.handle_error(
                        e.stderr if e.stderr else e.stdout,
                        package,
                        self.profile
                    )
                    
                    print(f"\n🔍 Error Analysis:")
                    print(f"   Type: {error_analysis['error_type']}")
                    print(f"   Diagnosis: {error_analysis['diagnosis']}")
                    
                    if error_analysis['solutions']:
                        print(f"\n💡 Suggested Solutions:")
                        for i, solution in enumerate(error_analysis['solutions'], 1):
                            print(f"   {i}. {solution}")
                    
                    if error_analysis['commands']:
                        print(f"\n🔧 Suggested Commands:")
                        for fix_cmd in error_analysis['commands']:
                            print(f"   {fix_cmd}")
                        
                        response = input("\n❓ Try suggested fixes? [Y/n]: ")
                        if response.lower() not in ['n', 'no']:
                            return self._execute_commands(
                                error_analysis['commands'],
                                package,
                                critical=False
                            )
                    
                    return False
                else:
                    print("⚠️  Non-critical command failed, continuing...")
        
        return True
    
    def build_from_source(
        self,
        package: PackageResult,
        source_url: str,
        build_system: str = "make"
    ) -> bool:
        """Build and install package from source"""
        
        print(f"\n🔨 Building {package.name} from source...")
        
        # Create build directory
        pkg_build_dir = self.build_dir / package.name
        pkg_build_dir.mkdir(parents=True, exist_ok=True)
        
        # Clone/download source
        print(f"📥 Downloading source from {source_url}")
        
        if source_url.endswith(".git") or "github.com" in source_url:
            # Git clone
            cmd = ["git", "clone", source_url, str(pkg_build_dir)]
        else:
            # Download and extract
            cmd = ["wget", "-O", str(pkg_build_dir / "source.tar.gz"), source_url]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to download source: {e}")
            return False
        
        # Determine build commands based on build system
        if build_system == "make":
            build_commands = [
                "./configure",
                f"make -j{self.config.parallel_jobs if self.config.parallel_jobs > 0 else '$(nproc)'}",
                "sudo make install"
            ]
        elif build_system == "cmake":
            build_commands = [
                "mkdir -p build && cd build",
                "cmake ..",
                f"make -j{self.config.parallel_jobs if self.config.parallel_jobs > 0 else '$(nproc)'}",
                "sudo make install"
            ]
        elif build_system == "cargo":
            build_commands = [
                "cargo build --release",
                "cargo install --path ."
            ]
        elif build_system == "meson":
            build_commands = [
                "meson setup build",
                "meson compile -C build",
                "sudo meson install -C build"
            ]
        else:
            print(f"❌ Unknown build system: {build_system}")
            return False
        
        # Execute build
        return self._execute_commands(build_commands, package)
    
    def verify_installation(self, package: PackageResult) -> bool:
        """Verify that package was installed successfully"""
        
        print(f"\n🔍 Verifying installation of {package.name}...")
        
        # Check if command exists
        if shutil.which(package.name):
            print(f"✓ {package.name} is available in PATH")
            return True
        
        # Check package manager
        if package.manager == "pacman":
            result = subprocess.run(
                ["pacman", "-Q", package.name],
                capture_output=True,
                check=False
            )
            if result.returncode == 0:
                print(f"✓ {package.name} is installed via pacman")
                return True
        
        elif package.manager == "apt":
            result = subprocess.run(
                ["dpkg", "-l", package.name],
                capture_output=True,
                check=False
            )
            if result.returncode == 0:
                print(f"✓ {package.name} is installed via apt")
                return True
        
        elif package.manager == "flatpak":
            result = subprocess.run(
                ["flatpak", "list", "--app"],
                capture_output=True,
                text=True,
                check=False
            )
            if package.name in result.stdout:
                print(f"✓ {package.name} is installed via flatpak")
                return True
        
        print(f"⚠️  Could not verify installation of {package.name}")
        return False

"""Eshu's Path - Curated package bundles for complete setups"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class EshuPath:
    """A curated bundle of packages for a complete setup"""
    name: str
    description: str
    packages: List[str]
    category: str
    reasoning: str
    install_order: Optional[List[str]] = None  # If order matters


# Curated paths for common setups
ESHU_PATHS: Dict[str, EshuPath] = {
    # Wayland Compositors
    "hyprland": EshuPath(
        name="Complete Hyprland Setup",
        description="Full Wayland compositor setup with essential tools",
        category="wayland-compositor",
        reasoning="Hyprland needs a complete ecosystem to be usable. This includes terminal, launcher, bar, notifications, and utilities.",
        packages=[
            "hyprland",           # The compositor
            "kitty",              # Terminal emulator (Wayland-native)
            "wofi",               # Application launcher
            "waybar",             # Status bar
            "mako",               # Notification daemon
            "grim",               # Screenshot tool
            "slurp",              # Screen area selector
            "wl-clipboard",       # Clipboard utilities
            "swaylock",           # Screen locker
            "swayidle",           # Idle manager
            "xdg-desktop-portal-hyprland",  # Portal for screen sharing
            "polkit-gnome",       # Authentication agent
            "pipewire",           # Audio server
            "wireplumber",        # Pipewire session manager
            "brightnessctl",      # Brightness control
        ],
        install_order=[
            "pipewire", "wireplumber",  # Audio first
            "hyprland",                  # Then compositor
            # Rest can be parallel
        ]
    ),

    "niri": EshuPath(
        name="Complete Niri Setup",
        description="Scrollable-tiling Wayland compositor with essential tools",
        category="wayland-compositor",
        reasoning="Niri is a unique scrollable tiling compositor. This bundle includes everything for a complete workflow.",
        packages=[
            "niri",
            "foot",               # Lightweight terminal
            "fuzzel",             # App launcher
            "waybar",             # Status bar
            "mako",               # Notifications
            "grim",
            "slurp",
            "wl-clipboard",
            "swaylock",
            "swayidle",
            "pipewire",
            "wireplumber",
            "brightnessctl",
        ]
    ),

    "sway": EshuPath(
        name="Complete Sway Setup",
        description="i3-compatible Wayland compositor with full toolset",
        category="wayland-compositor",
        reasoning="Sway replicates i3 for Wayland. This bundle mirrors a typical i3 workflow.",
        packages=[
            "sway",
            "foot",
            "wofi",
            "waybar",
            "mako",
            "grim",
            "slurp",
            "wl-clipboard",
            "swaylock",
            "swayidle",
            "xdg-desktop-portal-wlr",
            "pipewire",
            "wireplumber",
        ]
    ),

    # NVIDIA Drivers
    "nvidia": EshuPath(
        name="Complete NVIDIA Proprietary Setup",
        description="Full NVIDIA driver stack with utilities and support",
        category="graphics-driver",
        reasoning="NVIDIA drivers need the full stack for proper functionality including CUDA, OpenGL, and Wayland support.",
        packages=[
            "nvidia",                    # Main driver
            "nvidia-utils",              # Utilities
            "nvidia-settings",           # Control panel
            "lib32-nvidia-utils",        # 32-bit support (gaming)
            "opencl-nvidia",             # OpenCL support
            "cuda",                      # CUDA toolkit
            "libva-nvidia-driver",       # VA-API support
            "egl-wayland",               # Wayland support
        ]
    ),

    "nvidia-open": EshuPath(
        name="NVIDIA Open Kernel Modules Setup",
        description="Open-source NVIDIA drivers (RTX 2000+)",
        category="graphics-driver",
        reasoning="For RTX 2000 series and newer, the open kernel modules offer better Wayland support.",
        packages=[
            "nvidia-open",
            "nvidia-utils",
            "nvidia-settings",
            "lib32-nvidia-utils",
            "egl-wayland",
        ]
    ),

    # Development Environments
    "rust-dev": EshuPath(
        name="Complete Rust Development Environment",
        description="Full Rust toolchain with common utilities",
        category="development",
        reasoning="Beyond rustc, you need tooling for a productive Rust workflow.",
        packages=[
            "rust",
            "rust-analyzer",      # LSP server
            "cargo",
            "cargo-watch",        # Auto-recompile
            "cargo-edit",         # cargo add/rm
            "cargo-nextest",      # Better test runner
            "rustfmt",
            "clippy",
            "mold",               # Faster linker
        ]
    ),

    "python-dev": EshuPath(
        name="Complete Python Development Environment",
        description="Modern Python setup with tooling",
        category="development",
        reasoning="Modern Python development needs more than just python - virtual environments, linting, formatting, etc.",
        packages=[
            "python",
            "python-pip",
            "python-virtualenv",
            "python-pipenv",
            "python-poetry",
            "ruff",               # Fast linter/formatter
            "pyright",            # Type checker
            "ipython",            # Better REPL
        ]
    ),

    # Gaming
    "gaming-linux": EshuPath(
        name="Complete Linux Gaming Setup",
        description="Steam, Proton, and all essentials for gaming on Linux",
        category="gaming",
        reasoning="Linux gaming requires Steam, compatibility layers, and performance tools.",
        packages=[
            "steam",
            "wine",
            "wine-staging",
            "winetricks",
            "lutris",
            "gamemode",           # Performance mode
            "mangohud",           # Performance overlay
            "lib32-vulkan-icd-loader",
            "lib32-mesa",
            "lib32-nvidia-utils",  # If NVIDIA
            "gamescope",          # Compositor for games
        ]
    ),

    # Content Creation
    "video-editing": EshuPath(
        name="Complete Video Editing Suite",
        description="Professional video editing and production tools",
        category="content-creation",
        reasoning="Video editing needs the editor plus codecs, effects, and utilities.",
        packages=[
            "kdenlive",           # Video editor
            "davinci-resolve",    # Professional editor
            "ffmpeg",
            "obs-studio",         # Recording/streaming
            "audacity",           # Audio editing
            "gimp",               # Image editing
            "inkscape",           # Vector graphics
            "blender",            # 3D/VFX
        ]
    ),
}


def get_eshu_path(package_name: str) -> Optional[EshuPath]:
    """Get curated path for a package if available"""
    # Direct match
    if package_name.lower() in ESHU_PATHS:
        return ESHU_PATHS[package_name.lower()]

    # Fuzzy matching for common variations
    fuzzy_matches = {
        "nvidia-driver": "nvidia",
        "nvidia-proprietary": "nvidia",
        "nvidia-drivers": "nvidia",
        "rust-toolchain": "rust-dev",
        "python3": "python-dev",
        "steam-gaming": "gaming-linux",
        "linux-gaming": "gaming-linux",
    }

    if package_name.lower() in fuzzy_matches:
        return ESHU_PATHS[fuzzy_matches[package_name.lower()]]

    return None


def suggest_eshu_path_with_llm(package_name: str, llm_engine) -> Optional[Dict]:
    """Use LLM to suggest a curated package bundle (Premium feature)"""

    # Check if we have a predefined path first
    predefined = get_eshu_path(package_name)
    if predefined:
        return {
            "name": predefined.name,
            "description": predefined.description,
            "packages": predefined.packages,
            "reasoning": predefined.reasoning,
            "source": "curated"
        }

    # For packages without predefined paths, use LLM to suggest
    # This could analyze the package and suggest complementary tools
    # TODO: Implement LLM-based suggestion

    return None


def get_all_categories() -> List[str]:
    """Get all available path categories"""
    return list(set(path.category for path in ESHU_PATHS.values()))


def get_paths_by_category(category: str) -> List[EshuPath]:
    """Get all paths in a category"""
    return [path for path in ESHU_PATHS.values() if path.category == category]

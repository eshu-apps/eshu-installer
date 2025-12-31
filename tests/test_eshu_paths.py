"""Test Eshu's Path curated bundles"""

from eshu.eshu_paths import get_eshu_path, ESHU_PATHS, EshuPath


def test_eshu_paths_loaded():
    """Test that Eshu's Path bundles are loaded"""
    assert len(ESHU_PATHS) > 0
    assert "hyprland" in ESHU_PATHS


def test_get_hyprland_path():
    """Test getting Hyprland path"""
    path = get_eshu_path("hyprland")

    assert path is not None
    assert isinstance(path, EshuPath)
    assert "Hyprland" in path.name
    assert len(path.packages) > 10  # Should have 15+ packages


def test_get_nvidia_path():
    """Test getting NVIDIA proprietary path"""
    path = get_eshu_path("nvidia proprietary")

    assert path is not None
    assert "NVIDIA" in path.name or "nvidia" in path.name
    assert len(path.packages) > 5  # Should have 8+ packages


def test_get_nonexistent_path():
    """Test getting a path that doesn't exist"""
    path = get_eshu_path("nonexistent-package-12345")
    assert path is None


def test_path_has_required_fields():
    """Test that all paths have required fields"""
    for key, path in ESHU_PATHS.items():
        assert path.name
        assert path.description
        assert path.packages
        assert len(path.packages) > 0
        assert path.category
        assert path.reasoning


def test_hyprland_complete_bundle():
    """Test Hyprland has all essential packages"""
    path = get_eshu_path("hyprland")
    packages = path.packages

    # Essential Hyprland packages
    assert "hyprland" in packages
    assert "kitty" in packages or "alacritty" in packages  # Terminal
    assert "wofi" in packages or "rofi" in packages  # Launcher
    assert "waybar" in packages  # Status bar
    assert "mako" in packages  # Notifications

"""Configuration management for ESHU"""

import json
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class ESHUConfig(BaseModel):
    """ESHU configuration model"""
    
    # LLM Provider settings
    llm_provider: str = Field(default="anthropic", description="LLM provider: anthropic, openai, or ollama")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    ollama_endpoint: str = Field(default="http://localhost:11434", description="Ollama endpoint")
    ollama_model: str = Field(default="llama3.1:8b", description="Ollama model name")
    
    # Model settings
    model_name: str = Field(default="claude-3-5-sonnet-20241022", description="Model to use")
    temperature: float = Field(default=0.3, description="LLM temperature")
    max_tokens: int = Field(default=4096, description="Max tokens for response")
    
    # Package manager preferences (priority order)
    package_manager_priority: list[str] = Field(
        default=["pacman", "yay", "paru", "apt", "flatpak", "snap", "cargo", "npm", "pip", "aur"],
        description="Priority order for package managers"
    )
    default_package_manager: Optional[str] = Field(
        default=None,
        description="Default/primary package manager for system updates (e.g., 'pacman', 'apt')"
    )

    # System profiler settings
    cache_dir: Path = Field(default=Path.home() / ".cache" / "eshu", description="Cache directory")
    profile_cache_ttl: int = Field(default=3600, description="System profile cache TTL in seconds")

    # Analytics settings (privacy-respecting)
    analytics_enabled: bool = Field(default=True, description="Enable privacy-respecting analytics")
    analytics_db_path: Path = Field(
        default=Path.home() / ".cache" / "eshu" / "analytics.db",
        description="Analytics database path"
    )

    # Bundle database settings
    bundle_db_path: Path = Field(
        default=Path.home() / ".cache" / "eshu" / "bundles.db",
        description="Bundle cache database path"
    )

    # Installation preferences
    auto_confirm_deps: bool = Field(default=False, description="Auto-confirm dependency installation")
    prefer_native: bool = Field(default=True, description="Prefer native packages over containerized")
    enable_aur: bool = Field(default=True, description="Enable AUR support on Arch")

    # Build settings
    build_dir: Path = Field(default=Path("/tmp/eshu-builds"), description="Temporary build directory")
    parallel_jobs: int = Field(default=0, description="Parallel build jobs (0=auto)")
    
    class Config:
        env_prefix = "ESHU_"


def get_config_path() -> Path:
    """Get configuration file path"""
    if os.geteuid() == 0:
        return Path("/etc/eshu/config.json")
    return Path.home() / ".config" / "eshu" / "config.json"


def load_config() -> ESHUConfig:
    """Load configuration from file or environment"""
    config_path = get_config_path()
    
    if config_path.exists():
        with open(config_path) as f:
            data = json.load(f)
            return ESHUConfig(**data)
    
    # Try to load from environment
    config = ESHUConfig()
    
    # Check for API keys in environment
    if api_key := os.getenv("ANTHROPIC_API_KEY"):
        config.anthropic_api_key = api_key
    if api_key := os.getenv("OPENAI_API_KEY"):
        config.openai_api_key = api_key
    
    return config


def save_config(config: ESHUConfig) -> None:
    """Save configuration to file"""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config.model_dump(), f, indent=2, default=str)

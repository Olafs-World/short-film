"""Configuration management."""

import os
from pathlib import Path
from typing import Optional

from .models import FilmConfig, FilmStyle, MusicVibe, VideoProvider


def load_api_keys() -> tuple[Optional[str], Optional[str]]:
    """Load API keys from environment.

    Returns:
        Tuple of (openai_key, gemini_key)
    """
    openai_key = os.environ.get("OPENAI_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    return openai_key, gemini_key


def get_output_dir(base_dir: Optional[Path] = None) -> Path:
    """Get output directory for film generation.

    Args:
        base_dir: Base directory (defaults to ./output)

    Returns:
        Path to output directory
    """
    if base_dir is None:
        base_dir = Path.cwd() / "output"

    base_dir = Path(base_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    return base_dir


def create_film_config(
    premise: str,
    style: str = "cinematic",
    music_vibe: str = "epic",
    provider: str = "openai",
    target_duration: float = 60.0,
) -> FilmConfig:
    """Create a film configuration.

    Args:
        premise: Film premise/description
        style: Film style
        music_vibe: Music vibe
        provider: Video generation provider
        target_duration: Target film duration in seconds

    Returns:
        FilmConfig instance
    """
    openai_key, gemini_key = load_api_keys()

    return FilmConfig(
        premise=premise,
        style=FilmStyle(style),
        music_vibe=MusicVibe(music_vibe),
        provider=VideoProvider(provider),
        target_duration=target_duration,
        openai_api_key=openai_key,
        gemini_api_key=gemini_key,
    )

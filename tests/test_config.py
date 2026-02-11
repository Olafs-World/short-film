"""Tests for configuration management."""


from short_film.config import create_film_config, get_output_dir, load_api_keys
from short_film.models import FilmStyle, MusicVibe, VideoProvider


def test_get_output_dir_default(tmp_path, monkeypatch):
    """Test default output directory creation."""
    monkeypatch.chdir(tmp_path)

    output_dir = get_output_dir()

    assert output_dir.exists()
    assert output_dir.name == "output"


def test_get_output_dir_custom(tmp_path):
    """Test custom output directory."""
    custom_dir = tmp_path / "custom_output"

    output_dir = get_output_dir(custom_dir)

    assert output_dir.exists()
    assert output_dir == custom_dir


def test_load_api_keys_from_env(monkeypatch):
    """Test loading API keys from environment."""
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini_key")

    openai_key, gemini_key = load_api_keys()

    assert openai_key == "test_openai_key"
    assert gemini_key == "test_gemini_key"


def test_load_api_keys_missing(monkeypatch):
    """Test loading API keys when not set."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    openai_key, gemini_key = load_api_keys()

    assert openai_key is None
    assert gemini_key is None


def test_create_film_config():
    """Test film config creation."""
    config = create_film_config(
        premise="Test premise",
        style="noir",
        music_vibe="dark",
        provider="gemini",
        target_duration=30.0,
    )

    assert config.premise == "Test premise"
    assert config.style == FilmStyle.NOIR
    assert config.music_vibe == MusicVibe.DARK
    assert config.provider == VideoProvider.GEMINI
    assert config.target_duration == 30.0

"""Tests for data models."""

from pathlib import Path

from short_film.models import (
    ClipStatus,
    FilmConfig,
    FilmState,
    FilmStyle,
    MusicVibe,
    VideoClip,
    VideoProvider,
)


def test_video_clip_creation():
    """Test VideoClip model creation."""
    clip = VideoClip(
        index=0,
        prompt="Test prompt",
        duration=10.0,
    )

    assert clip.index == 0
    assert clip.prompt == "Test prompt"
    assert clip.status == ClipStatus.PENDING
    assert clip.duration == 10.0


def test_film_config_creation():
    """Test FilmConfig model creation."""
    config = FilmConfig(
        premise="A test film",
        style=FilmStyle.CINEMATIC,
        music_vibe=MusicVibe.EPIC,
        provider=VideoProvider.OPENAI,
    )

    assert config.premise == "A test film"
    assert config.style == FilmStyle.CINEMATIC
    assert config.music_vibe == MusicVibe.EPIC
    assert config.target_duration == 60.0
    assert config.clip_duration == 10.0


def test_film_state_creation():
    """Test FilmState model creation."""
    config = FilmConfig(
        premise="Test",
        style=FilmStyle.ANIME,
        music_vibe=MusicVibe.UPBEAT,
    )

    state = FilmState(
        config=config,
        output_dir=Path("/tmp/test"),
    )

    assert state.config == config
    assert state.output_dir == Path("/tmp/test")
    assert state.completed is False
    assert len(state.clips) == 0


def test_enum_values():
    """Test enum values."""
    assert FilmStyle.CINEMATIC.value == "cinematic"
    assert MusicVibe.EPIC.value == "epic"
    assert VideoProvider.OPENAI.value == "openai"
    assert ClipStatus.COMPLETED.value == "completed"

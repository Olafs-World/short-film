"""Tests for state management."""

from pathlib import Path

import pytest
from short_film.models import FilmConfig, FilmState, FilmStyle, MusicVibe
from short_film.state import StateManager


def test_state_manager_save_and_load(tmp_path):
    """Test saving and loading state."""
    output_dir = tmp_path / "output"
    manager = StateManager(output_dir)
    
    config = FilmConfig(
        premise="Test film",
        style=FilmStyle.SCIFI,
        music_vibe=MusicVibe.SUSPENSEFUL,
    )
    
    state = FilmState(
        config=config,
        output_dir=output_dir,
    )
    
    # Save state
    manager.save(state)
    assert manager.state_file.exists()
    
    # Load state
    loaded_state = manager.load()
    assert loaded_state is not None
    assert loaded_state.config.premise == "Test film"
    assert loaded_state.config.style == FilmStyle.SCIFI


def test_state_manager_load_nonexistent(tmp_path):
    """Test loading when no state file exists."""
    output_dir = tmp_path / "output"
    manager = StateManager(output_dir)
    
    loaded_state = manager.load()
    assert loaded_state is None


def test_state_manager_clear(tmp_path):
    """Test clearing state."""
    output_dir = tmp_path / "output"
    manager = StateManager(output_dir)
    
    config = FilmConfig(
        premise="Test",
        style=FilmStyle.HORROR,
        music_vibe=MusicVibe.DARK,
    )
    
    state = FilmState(config=config, output_dir=output_dir)
    
    # Save and then clear
    manager.save(state)
    assert manager.state_file.exists()
    
    manager.clear()
    assert not manager.state_file.exists()

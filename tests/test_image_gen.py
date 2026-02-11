"""Tests for image generation."""

import pytest
from short_film.image_gen import create_image_prompt
from short_film.models import FilmStyle


def test_create_image_prompt_cinematic():
    """Test creating image prompt for cinematic style."""
    prompt = create_image_prompt("A space station", FilmStyle.CINEMATIC)
    
    assert "space station" in prompt.lower()
    assert "cinematic" in prompt.lower()


def test_create_image_prompt_noir():
    """Test creating image prompt for noir style."""
    prompt = create_image_prompt("A detective", FilmStyle.NOIR)
    
    assert "detective" in prompt.lower()
    assert "noir" in prompt.lower()
    assert "black and white" in prompt.lower()


def test_create_image_prompt_anime():
    """Test creating image prompt for anime style."""
    prompt = create_image_prompt("A hero", FilmStyle.ANIME)
    
    assert "hero" in prompt.lower()
    assert "anime" in prompt.lower()


@pytest.mark.integration
def test_generate_image_openai_integration(tmp_path):
    """Integration test for OpenAI image generation."""
    # This test requires a real API key and makes actual API calls
    # Skip in normal test runs
    pytest.skip("Integration test - requires API key and costs money")

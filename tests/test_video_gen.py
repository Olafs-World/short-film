"""Tests for video generation."""

import pytest
from short_film.video_gen import create_video_prompt


def test_create_video_prompt_first_clip():
    """Test creating prompt for first clip."""
    prompt = create_video_prompt("A robot explores", 0, 5)
    
    assert "robot explores" in prompt.lower()
    assert "opening" in prompt.lower()


def test_create_video_prompt_middle_clip():
    """Test creating prompt for middle clip."""
    prompt = create_video_prompt("A robot explores", 2, 5)
    
    assert "robot explores" in prompt.lower()
    assert "scene 3" in prompt.lower()


def test_create_video_prompt_final_clip():
    """Test creating prompt for final clip."""
    prompt = create_video_prompt("A robot explores", 4, 5)
    
    assert "robot explores" in prompt.lower()
    assert "final" in prompt.lower()


@pytest.mark.integration
def test_generate_video_openai_integration():
    """Integration test for OpenAI video generation."""
    # This test requires a real API key and Sora access
    pytest.skip("Integration test - requires Sora API access")


@pytest.mark.integration
def test_generate_video_gemini_integration():
    """Integration test for Gemini video generation."""
    # This test requires a real API key and Gemini video access
    pytest.skip("Integration test - requires Gemini video API")


@pytest.mark.integration
def test_extract_last_frame_integration(tmp_path):
    """Integration test for frame extraction."""
    # This test requires a real video file and opencv
    pytest.skip("Integration test - requires video file and opencv")

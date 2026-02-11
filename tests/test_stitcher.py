"""Tests for video stitching."""

import pytest

from short_film.stitcher import check_ffmpeg


def test_check_ffmpeg():
    """Test ffmpeg availability check."""
    # This will pass or fail depending on system
    result = check_ffmpeg()
    assert isinstance(result, bool)


@pytest.mark.integration
def test_stitch_videos_integration(tmp_path):
    """Integration test for video stitching."""
    # This test requires real video files and ffmpeg
    pytest.skip("Integration test - requires video files and ffmpeg")


@pytest.mark.integration
def test_stitch_videos_with_music_integration(tmp_path):
    """Integration test for video stitching with music."""
    # This test requires real video/audio files and ffmpeg
    pytest.skip("Integration test - requires media files and ffmpeg")

"""Video stitching with ffmpeg."""

import shutil
import subprocess
from pathlib import Path
from typing import Optional


def check_ffmpeg() -> bool:
    """Check if ffmpeg is installed.

    Returns:
        True if ffmpeg is available, False otherwise
    """
    return shutil.which("ffmpeg") is not None


def stitch_videos(
    video_paths: list[Path],
    output_path: Path,
    music_path: Optional[Path] = None,
) -> Path:
    """Stitch multiple video clips into a single film.

    Args:
        video_paths: List of video clip paths to stitch
        output_path: Output path for the final film
        music_path: Optional path to music/audio file to add

    Returns:
        Path to stitched video

    Raises:
        RuntimeError: If ffmpeg is not installed
        subprocess.CalledProcessError: If ffmpeg command fails
    """
    if not check_ffmpeg():
        raise RuntimeError(
            "ffmpeg is required for video stitching. "
            "Install with: sudo dnf install ffmpeg (Amazon Linux) "
            "or brew install ffmpeg (macOS) "
            "or apt install ffmpeg (Ubuntu)"
        )

    if not video_paths:
        raise ValueError("No video clips to stitch")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Create a temporary file list for ffmpeg concat
    concat_file = output_path.parent / "concat_list.txt"
    with open(concat_file, "w") as f:
        for video_path in video_paths:
            f.write(f"file '{video_path.absolute()}'\n")

    try:
        if music_path and music_path.exists():
            # Stitch with music
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-i", str(music_path),
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",  # Stop when shortest input ends
                "-y",  # Overwrite output file
                str(output_path),
            ]
        else:
            # Stitch without music
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-c", "copy",
                "-y",  # Overwrite output file
                str(output_path),
            ]

        subprocess.run(cmd, check=True, capture_output=True, text=True)

    finally:
        # Clean up concat file
        if concat_file.exists():
            concat_file.unlink()

    return output_path


def trim_video(
    input_path: Path,
    output_path: Path,
    duration: float,
) -> Path:
    """Trim a video to a specific duration.

    Args:
        input_path: Input video path
        output_path: Output video path
        duration: Target duration in seconds

    Returns:
        Path to trimmed video

    Raises:
        RuntimeError: If ffmpeg is not installed
        subprocess.CalledProcessError: If ffmpeg command fails
    """
    if not check_ffmpeg():
        raise RuntimeError("ffmpeg is required")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-t", str(duration),
        "-c", "copy",
        "-y",
        str(output_path),
    ]

    subprocess.run(cmd, check=True, capture_output=True, text=True)

    return output_path

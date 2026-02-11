"""Video generation with frame chaining."""

import time
from pathlib import Path
from typing import Optional

import google.generativeai as genai
from openai import OpenAI
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_exponential

from .models import FilmConfig, VideoClip, VideoProvider


def create_video_prompt(premise: str, clip_index: int, total_clips: int) -> str:
    """Create a video generation prompt for a specific clip.

    Args:
        premise: Overall film premise
        clip_index: Index of this clip (0-based)
        total_clips: Total number of clips

    Returns:
        Video generation prompt
    """
    if clip_index == 0:
        return f"{premise}. Opening scene, establishing shot. Smooth camera movement."
    elif clip_index == total_clips - 1:
        return f"{premise}. Final scene, resolution. Dramatic conclusion."
    else:
        progress = (clip_index / total_clips) * 100
        return f"{premise}. Continuing the story (scene {clip_index + 1}). Build tension and progression."


def extract_last_frame(video_path: Path, output_path: Path) -> Path:
    """Extract the last frame from a video file.

    Args:
        video_path: Path to video file
        output_path: Where to save the extracted frame

    Returns:
        Path to extracted frame

    Raises:
        ImportError: If opencv-python is not installed
        Exception: If frame extraction fails
    """
    try:
        import cv2
    except ImportError:
        raise ImportError(
            "opencv-python is required for frame extraction. "
            "Install with: uv add opencv-python"
        )

    cap = cv2.VideoCapture(str(video_path))
    
    # Get total frame count
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Set position to last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    
    # Read the frame
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise Exception(f"Failed to extract last frame from {video_path}")
    
    # Save the frame
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), frame)
    
    return output_path


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=8, max=60),
)
def generate_video_openai(
    prompt: str,
    api_key: str,
    output_path: Path,
    start_image_path: Optional[Path] = None,
    duration: float = 10.0,
) -> Path:
    """Generate a video using OpenAI Sora.

    Args:
        prompt: Video generation prompt
        api_key: OpenAI API key
        output_path: Where to save the generated video
        start_image_path: Optional starting image for image-to-video
        duration: Video duration in seconds

    Returns:
        Path to generated video

    Raises:
        Exception: If video generation fails
    """
    client = OpenAI(api_key=api_key)

    # Note: This uses the Sora API when available
    # For now, this is a placeholder that will work when Sora API is released
    try:
        if start_image_path:
            # Image-to-video generation
            with open(start_image_path, "rb") as img_file:
                response = client.videos.generate(
                    model="sora-1.0",
                    prompt=prompt,
                    image=img_file,
                    duration=duration,
                )
        else:
            # Text-to-video generation
            response = client.videos.generate(
                model="sora-1.0",
                prompt=prompt,
                duration=duration,
            )

        # Download video
        video_url = response.url
        import requests
        
        video_response = requests.get(video_url, timeout=300)
        video_response.raise_for_status()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(video_response.content)

        return output_path

    except Exception as e:
        # If Sora API is not available yet, provide helpful error
        if "not found" in str(e).lower() or "does not exist" in str(e).lower():
            raise Exception(
                "OpenAI Sora API is not yet available. "
                "Try using --provider gemini instead, or wait for Sora API release."
            ) from e
        raise


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=8, max=60),
)
def generate_video_gemini(
    prompt: str,
    api_key: str,
    output_path: Path,
    start_image_path: Optional[Path] = None,
    duration: float = 10.0,
) -> Path:
    """Generate a video using Google Gemini.

    Args:
        prompt: Video generation prompt
        api_key: Gemini API key
        output_path: Where to save the generated video
        start_image_path: Optional starting image
        duration: Video duration in seconds

    Returns:
        Path to generated video

    Raises:
        Exception: If video generation fails
    """
    genai.configure(api_key=api_key)
    
    # Note: This is a placeholder for Gemini video generation
    # Implementation depends on the actual Gemini video API when available
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # For now, Gemini video generation may not be fully available
        # This is a forward-compatible implementation
        response = model.generate_video(
            prompt=prompt,
            image_path=str(start_image_path) if start_image_path else None,
            duration=duration,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.video_data)

        return output_path

    except AttributeError:
        raise Exception(
            "Gemini video generation is not yet available in the API. "
            "Please check Google AI Studio for the latest API capabilities."
        )


def generate_clip(
    clip: VideoClip,
    config: FilmConfig,
    total_clips: int,
) -> VideoClip:
    """Generate a single video clip.

    Args:
        clip: Clip configuration
        config: Film configuration
        total_clips: Total number of clips in the film

    Returns:
        Updated clip with generation results

    Raises:
        ValueError: If required API key is missing
    """
    if config.provider == VideoProvider.OPENAI:
        if not config.openai_api_key:
            raise ValueError("OpenAI API key required")
        
        generate_fn = generate_video_openai
        api_key = config.openai_api_key
    else:
        if not config.gemini_api_key:
            raise ValueError("Gemini API key required")
        
        generate_fn = generate_video_gemini
        api_key = config.gemini_api_key

    try:
        output_path = generate_fn(
            prompt=clip.prompt,
            api_key=api_key,
            output_path=Path(clip.output_path),
            start_image_path=Path(clip.start_image_path) if clip.start_image_path else None,
            duration=clip.duration,
        )

        clip.output_path = output_path
        
        # Extract last frame for chaining to next clip
        if clip.index < total_clips - 1:
            last_frame_path = output_path.parent / f"clip_{clip.index}_last_frame.png"
            clip.last_frame_path = extract_last_frame(output_path, last_frame_path)

        return clip

    except Exception as e:
        clip.error = str(e)
        raise

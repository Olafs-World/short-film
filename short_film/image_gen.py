"""Image generation for starting frames."""

import base64
from io import BytesIO
from pathlib import Path
from typing import Optional

import requests
from openai import OpenAI
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_exponential

from .models import FilmConfig, FilmStyle


def create_image_prompt(premise: str, style: FilmStyle) -> str:
    """Create an image generation prompt from premise and style.

    Args:
        premise: Film premise
        style: Film style

    Returns:
        Image generation prompt
    """
    style_descriptions = {
        FilmStyle.CINEMATIC: "cinematic, dramatic lighting, film grain, anamorphic lens",
        FilmStyle.NOIR: "film noir, high contrast black and white, dramatic shadows",
        FilmStyle.ANIME: "anime style, vibrant colors, detailed illustration",
        FilmStyle.DOCUMENTARY: "documentary style, realistic, natural lighting",
        FilmStyle.SCIFI: "sci-fi, futuristic, neon lights, high tech",
        FilmStyle.FANTASY: "fantasy, magical, ethereal, dramatic",
        FilmStyle.HORROR: "horror, dark, ominous, unsettling atmosphere",
        FilmStyle.COMEDY: "bright, colorful, whimsical, fun",
    }

    style_desc = style_descriptions.get(style, "cinematic")
    return f"{premise}. {style_desc}. Opening shot, establishing scene. High quality, detailed."


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
)
def generate_image_openai(
    prompt: str,
    api_key: str,
    output_path: Path,
    size: str = "1024x1024",
) -> Path:
    """Generate an image using OpenAI DALL-E.

    Args:
        prompt: Image generation prompt
        api_key: OpenAI API key
        output_path: Where to save the generated image
        size: Image size

    Returns:
        Path to generated image

    Raises:
        Exception: If image generation fails
    """
    client = OpenAI(api_key=api_key)

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    
    # Download the image
    img_response = requests.get(image_url, timeout=30)
    img_response.raise_for_status()

    # Save the image
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_response.content)

    return output_path


def generate_starting_frame(
    config: FilmConfig,
    output_path: Path,
) -> Path:
    """Generate the starting frame for the film.

    Args:
        config: Film configuration
        output_path: Where to save the starting frame

    Returns:
        Path to generated starting frame

    Raises:
        ValueError: If API key is missing
        Exception: If generation fails
    """
    if not config.openai_api_key:
        raise ValueError("OpenAI API key required for image generation")

    prompt = create_image_prompt(config.premise, config.style)
    
    return generate_image_openai(
        prompt=prompt,
        api_key=config.openai_api_key,
        output_path=output_path,
    )

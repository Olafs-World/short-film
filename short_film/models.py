"""Data models for short-film."""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class FilmStyle(str, Enum):
    """Available film styles."""

    CINEMATIC = "cinematic"
    NOIR = "noir"
    ANIME = "anime"
    DOCUMENTARY = "documentary"
    SCIFI = "scifi"
    FANTASY = "fantasy"
    HORROR = "horror"
    COMEDY = "comedy"


class MusicVibe(str, Enum):
    """Available music vibes."""

    EPIC = "epic"
    SUSPENSEFUL = "suspenseful"
    CALM = "calm"
    UPBEAT = "upbeat"
    DARK = "dark"
    WHIMSICAL = "whimsical"
    NONE = "none"


class VideoProvider(str, Enum):
    """Available video generation providers."""

    OPENAI = "openai"
    GEMINI = "gemini"


class ClipStatus(str, Enum):
    """Status of a video clip."""

    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoClip(BaseModel):
    """Represents a single video clip in the film."""

    index: int
    status: ClipStatus = ClipStatus.PENDING
    prompt: str
    start_image_path: Optional[Path] = None
    output_path: Optional[Path] = None
    last_frame_path: Optional[Path] = None
    duration: float = Field(default=10.0, description="Duration in seconds")
    error: Optional[str] = None


class FilmConfig(BaseModel):
    """Configuration for a short film project."""

    premise: str
    style: FilmStyle
    music_vibe: MusicVibe
    target_duration: float = Field(default=60.0, description="Target film duration in seconds")
    clip_duration: float = Field(default=10.0, description="Duration per clip in seconds")
    provider: VideoProvider = VideoProvider.OPENAI
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None


class FilmState(BaseModel):
    """Current state of the film generation process."""

    model_config = {"arbitrary_types_allowed": True}

    config: FilmConfig
    output_dir: Path
    starting_frame_path: Optional[Path] = None
    clips: list[VideoClip] = Field(default_factory=list)
    final_video_path: Optional[Path] = None
    completed: bool = False

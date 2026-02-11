"""Main film generator orchestration."""

import math
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from .image_gen import generate_starting_frame
from .models import ClipStatus, FilmConfig, FilmState, VideoClip
from .state import StateManager
from .stitcher import stitch_videos
from .video_gen import create_video_prompt, generate_clip

console = Console()


class FilmGenerator:
    """Main film generation orchestrator."""

    def __init__(self, config: FilmConfig, output_dir: Path, resume: bool = True):
        """Initialize film generator.

        Args:
            config: Film configuration
            output_dir: Output directory for all generated files
            resume: Whether to resume from saved state
        """
        self.config = config
        self.output_dir = Path(output_dir)
        self.state_manager = StateManager(output_dir)
        
        # Try to load existing state if resuming
        if resume:
            existing_state = self.state_manager.load()
            if existing_state:
                console.print("🔄 Resuming from saved state", style="yellow")
                self.state = existing_state
                # Update config in case parameters changed
                self.state.config = config
            else:
                self.state = self._create_new_state()
        else:
            self.state = self._create_new_state()

    def _create_new_state(self) -> FilmState:
        """Create a new film state.

        Returns:
            Initialized FilmState
        """
        num_clips = math.ceil(self.config.target_duration / self.config.clip_duration)
        
        clips = [
            VideoClip(
                index=i,
                prompt="",  # Will be set during generation
                duration=self.config.clip_duration,
                output_path=self.output_dir / f"clip_{i}.mp4",
            )
            for i in range(num_clips)
        ]

        return FilmState(
            config=self.config,
            output_dir=self.output_dir,
            clips=clips,
        )

    def _save_state(self) -> None:
        """Save current state to disk."""
        self.state_manager.save(self.state)

    def generate(self) -> Path:
        """Generate the complete film.

        Returns:
            Path to final film

        Raises:
            Exception: If generation fails
        """
        console.print("🎬 Starting film generation", style="bold blue")
        console.print(f"📝 Premise: {self.config.premise}")
        console.print(f"🎨 Style: {self.config.style.value}")
        console.print(f"🎵 Music vibe: {self.config.music_vibe.value}")
        console.print(f"🎥 Provider: {self.config.provider.value}")
        console.print(f"⏱️  Target duration: {self.config.target_duration}s")
        console.print(f"📊 Clips: {len(self.state.clips)}")
        console.print()

        try:
            # Step 1: Generate starting frame
            if not self.state.starting_frame_path:
                self._generate_starting_frame()
                self._save_state()

            # Step 2: Generate video clips with chaining
            self._generate_clips()

            # Step 3: Stitch clips together
            final_video = self._stitch_clips()

            self.state.final_video_path = final_video
            self.state.completed = True
            self._save_state()

            console.print()
            console.print(f"✅ Film generation complete!", style="bold green")
            console.print(f"📹 Output: {final_video}")

            return final_video

        except Exception as e:
            console.print(f"❌ Error: {e}", style="bold red")
            self._save_state()
            raise

    def _generate_starting_frame(self) -> None:
        """Generate the starting frame."""
        console.print("🖼️  Generating starting frame...", style="cyan")
        
        output_path = self.output_dir / "starting_frame.png"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating image...", total=None)
            
            starting_frame = generate_starting_frame(self.config, output_path)
            self.state.starting_frame_path = starting_frame
            
            progress.update(task, completed=True)

        console.print(f"✓ Starting frame saved to {starting_frame}", style="green")

    def _generate_clips(self) -> None:
        """Generate all video clips with frame chaining."""
        console.print("🎥 Generating video clips...", style="cyan")
        
        total_clips = len(self.state.clips)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Generating clips...", total=total_clips)

            for i, clip in enumerate(self.state.clips):
                # Skip already completed clips
                if clip.status == ClipStatus.COMPLETED and clip.output_path and Path(clip.output_path).exists():
                    progress.advance(task)
                    continue

                # Update prompt if not set
                if not clip.prompt:
                    clip.prompt = create_video_prompt(
                        self.config.premise,
                        clip.index,
                        total_clips,
                    )

                # Set starting image
                if i == 0:
                    clip.start_image_path = self.state.starting_frame_path
                else:
                    # Use last frame from previous clip
                    prev_clip = self.state.clips[i - 1]
                    if prev_clip.last_frame_path:
                        clip.start_image_path = prev_clip.last_frame_path

                # Generate clip
                clip.status = ClipStatus.GENERATING
                progress.update(task, description=f"Generating clip {i + 1}/{total_clips}...")
                
                try:
                    updated_clip = generate_clip(clip, self.config, total_clips)
                    self.state.clips[i] = updated_clip
                    self.state.clips[i].status = ClipStatus.COMPLETED
                    
                except Exception as e:
                    self.state.clips[i].status = ClipStatus.FAILED
                    self.state.clips[i].error = str(e)
                    console.print(f"⚠️  Clip {i + 1} failed: {e}", style="yellow")
                    
                finally:
                    self._save_state()
                    progress.advance(task)

        # Check if all clips completed
        failed_clips = [c for c in self.state.clips if c.status == ClipStatus.FAILED]
        if failed_clips:
            console.print(f"⚠️  {len(failed_clips)} clips failed", style="yellow")
            for clip in failed_clips:
                console.print(f"  - Clip {clip.index + 1}: {clip.error}", style="dim")

    def _stitch_clips(self) -> Path:
        """Stitch all clips into final film."""
        console.print("🎞️  Stitching clips...", style="cyan")

        # Get all successfully generated clips
        completed_clips = [
            Path(clip.output_path)
            for clip in self.state.clips
            if clip.status == ClipStatus.COMPLETED and clip.output_path
        ]

        if not completed_clips:
            raise Exception("No completed clips to stitch")

        final_output = self.output_dir / "final_film.mp4"

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Stitching videos...", total=None)
            
            # TODO: Add music if music_vibe is not NONE
            # This would require sourcing/generating music which is out of scope for MVP
            final_video = stitch_videos(completed_clips, final_output)
            
            progress.update(task, completed=True)

        console.print(f"✓ Final film saved to {final_video}", style="green")
        
        return final_video

"""CLI interface for short-film."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

from . import __version__
from .config import create_film_config, get_output_dir
from .generator import FilmGenerator
from .models import FilmStyle, MusicVibe, VideoProvider

app = typer.Typer(
    name="short-film",
    help="Generate 60-second short films using AI video generation",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Print version and exit."""
    if value:
        console.print(f"short-film version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
):
    """Short Film - AI-powered 60-second film generator."""
    pass


@app.command()
def generate(
    premise: Optional[str] = typer.Option(
        None,
        "--premise",
        "-p",
        help="Film premise/description",
    ),
    style: str = typer.Option(
        "cinematic",
        "--style",
        "-s",
        help="Film style",
    ),
    music_vibe: str = typer.Option(
        "epic",
        "--music-vibe",
        "-m",
        help="Music vibe",
    ),
    provider: str = typer.Option(
        "openai",
        "--provider",
        help="Video generation provider (openai or gemini)",
    ),
    duration: float = typer.Option(
        60.0,
        "--duration",
        "-d",
        help="Target film duration in seconds",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory",
    ),
    interactive: bool = typer.Option(
        True,
        "--interactive/--no-interactive",
        help="Interactive mode",
    ),
    resume: bool = typer.Option(
        True,
        "--resume/--no-resume",
        help="Resume from saved state if available",
    ),
):
    """Generate a short film.

    Examples:
        # Interactive mode (default)
        short-film generate

        # Non-interactive with all options
        short-film generate -p "A lone astronaut discovers an alien artifact" \\
            --style scifi --music-vibe suspenseful --provider openai

        # Resume interrupted generation
        short-film generate --resume
    """
    # Interactive prompt flow
    if interactive and not premise:
        console.print("🎬 [bold blue]Welcome to Short Film Generator![/bold blue]")
        console.print()
        
        premise = _prompt_premise()
        style = _prompt_style()
        music_vibe = _prompt_music_vibe()
        
        console.print()
        _show_summary(premise, style, music_vibe, provider, duration)
        console.print()
        
        if not Confirm.ask("Ready to generate?", default=True):
            console.print("Cancelled.", style="yellow")
            raise typer.Exit()

    if not premise:
        console.print("❌ Premise is required. Use --premise or run in interactive mode.", style="red")
        raise typer.Exit(1)

    # Validate enums
    try:
        style_enum = FilmStyle(style)
        music_vibe_enum = MusicVibe(music_vibe)
        provider_enum = VideoProvider(provider)
    except ValueError as e:
        console.print(f"❌ Invalid option: {e}", style="red")
        raise typer.Exit(1)

    # Create config
    config = create_film_config(
        premise=premise,
        style=style,
        music_vibe=music_vibe,
        provider=provider,
        target_duration=duration,
    )

    # Get output directory
    if output_dir is None:
        output_dir = get_output_dir()
    else:
        output_dir = Path(output_dir)

    # Generate film
    try:
        generator = FilmGenerator(config, output_dir, resume=resume)
        final_video = generator.generate()
        
        console.print()
        console.print("🎉 [bold green]Success![/bold green]")
        console.print(f"Your film is ready: [cyan]{final_video}[/cyan]")

    except Exception as e:
        console.print(f"❌ [bold red]Generation failed:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def styles():
    """List available film styles."""
    table = Table(title="Available Film Styles", show_header=True)
    table.add_column("Style", style="cyan")
    table.add_column("Description", style="white")

    style_descriptions = {
        "cinematic": "Dramatic, film-like quality with professional cinematography",
        "noir": "Black and white, high contrast, dramatic shadows",
        "anime": "Japanese animation style with vibrant colors",
        "documentary": "Realistic, natural lighting, authentic feel",
        "scifi": "Futuristic, high-tech, neon-lit environments",
        "fantasy": "Magical, ethereal, fantastical elements",
        "horror": "Dark, ominous, unsettling atmosphere",
        "comedy": "Bright, colorful, lighthearted tone",
    }

    for style in FilmStyle:
        table.add_row(style.value, style_descriptions.get(style.value, ""))

    console.print(table)


@app.command()
def vibes():
    """List available music vibes."""
    table = Table(title="Available Music Vibes", show_header=True)
    table.add_column("Vibe", style="cyan")
    table.add_column("Description", style="white")

    vibe_descriptions = {
        "epic": "Grand, sweeping orchestral music",
        "suspenseful": "Tense, dramatic, keeps you on edge",
        "calm": "Peaceful, relaxing, ambient",
        "upbeat": "Energetic, positive, fun",
        "dark": "Ominous, foreboding, intense",
        "whimsical": "Playful, quirky, lighthearted",
        "none": "No music (video only)",
    }

    for vibe in MusicVibe:
        table.add_row(vibe.value, vibe_descriptions.get(vibe.value, ""))

    console.print(table)


def _prompt_premise() -> str:
    """Prompt for film premise."""
    console.print("📝 [bold]What's your film about?[/bold]")
    console.print("   Examples:")
    console.print("   • A lone astronaut discovers an alien artifact on Mars")
    console.print("   • Two robots fall in love in a post-apocalyptic city")
    console.print("   • A detective chases a mysterious figure through rain-soaked streets")
    console.print()
    
    premise = Prompt.ask("Film premise")
    return premise


def _prompt_style() -> str:
    """Prompt for film style."""
    console.print()
    console.print("🎨 [bold]Choose a film style[/bold]")
    
    styles = [s.value for s in FilmStyle]
    for i, style in enumerate(styles, 1):
        console.print(f"   {i}. {style}")
    
    console.print()
    choice = Prompt.ask(
        "Style",
        choices=styles + [str(i) for i in range(1, len(styles) + 1)],
        default="cinematic",
    )
    
    # Convert number to style if needed
    if choice.isdigit():
        return styles[int(choice) - 1]
    return choice


def _prompt_music_vibe() -> str:
    """Prompt for music vibe."""
    console.print()
    console.print("🎵 [bold]Choose a music vibe[/bold]")
    
    vibes = [v.value for v in MusicVibe]
    for i, vibe in enumerate(vibes, 1):
        console.print(f"   {i}. {vibe}")
    
    console.print()
    choice = Prompt.ask(
        "Music vibe",
        choices=vibes + [str(i) for i in range(1, len(vibes) + 1)],
        default="epic",
    )
    
    # Convert number to vibe if needed
    if choice.isdigit():
        return vibes[int(choice) - 1]
    return choice


def _show_summary(premise: str, style: str, music_vibe: str, provider: str, duration: float):
    """Show generation summary."""
    table = Table(title="Film Configuration", show_header=False, box=None)
    table.add_column("Key", style="cyan bold")
    table.add_column("Value", style="white")
    
    table.add_row("Premise", premise)
    table.add_row("Style", style)
    table.add_row("Music", music_vibe)
    table.add_row("Provider", provider)
    table.add_row("Duration", f"{duration}s")
    
    console.print(table)


if __name__ == "__main__":
    app()

---
name: short-film
description: Generate 60-second AI short films using OpenAI Sora or Google Gemini. Creates cinematic videos by chaining clips with last-frame-to-first-frame transitions. Interactive and non-interactive modes, 8 film styles (cinematic, noir, anime, documentary, sci-fi, fantasy, horror, comedy), 6 music vibes. Use for creating video content, storytelling, creative projects. Keywords - video generation, AI video, short film, Sora, Gemini, cinematic, video editing, frame chaining, movie maker
license: MIT
metadata:
  author: Olafs-World
  version: "0.1.0"
---

# Short Film

Generate 60-second AI short films using OpenAI Sora or Google Gemini with automatic frame chaining.

## Requirements

- Python 3.9+
- ffmpeg (for video stitching)
- OpenAI API key (for Sora) or Google Gemini API key

### Install ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Amazon Linux
sudo dnf install ffmpeg
```

## Quick Usage

### Interactive Mode (Recommended)

```bash
short-film generate
```

Guides you through:
1. Enter film premise
2. Choose visual style
3. Pick music vibe
4. Watch generation progress

### Non-Interactive Mode

```bash
short-film generate \
  --premise "A lone astronaut discovers an alien artifact on Mars" \
  --style scifi \
  --music-vibe suspenseful \
  --provider openai \
  --duration 60
```

### List Options

```bash
# Show all film styles
short-film styles

# Show all music vibes
short-film vibes
```

## Key Commands

| Command | Description |
|---------|-------------|
| `short-film generate` | Generate a new short film (interactive) |
| `short-film styles` | List available film styles |
| `short-film vibes` | List available music vibes |

## Generate Options

| Option | Description |
|--------|-------------|
| `--premise TEXT` | Film concept/premise (required in non-interactive) |
| `--style {cinematic,noir,anime,documentary,scifi,fantasy,horror,comedy}` | Visual style |
| `--music-vibe {epic,suspenseful,calm,upbeat,dark,whimsical,none}` | Music vibe |
| `--provider {openai,gemini}` | Video generation provider |
| `--duration INT` | Total duration in seconds (default: 60) |
| `--output PATH` | Custom output directory |
| `--resume` | Resume interrupted generation |
| `--no-interactive` | Disable interactive prompts |

## Film Styles

- **cinematic**: Dramatic, film-like quality with professional cinematography
- **noir**: Black and white, high contrast, dramatic shadows
- **anime**: Japanese animation style with vibrant colors
- **documentary**: Realistic, natural lighting, authentic feel
- **scifi**: Futuristic, high-tech, neon-lit environments
- **fantasy**: Magical, ethereal, fantastical elements
- **horror**: Dark, ominous, unsettling atmosphere
- **comedy**: Bright, colorful, lighthearted tone

## Music Vibes

- **epic**: Grand, sweeping orchestral music
- **suspenseful**: Tense, dramatic, keeps you on edge
- **calm**: Peaceful, relaxing, ambient
- **upbeat**: Energetic, positive, fun
- **dark**: Ominous, foreboding, intense
- **whimsical**: Playful, quirky, lighthearted
- **none**: No music (video only)

## How It Works

1. **Align on Premise**: Describe your short film concept
2. **Choose Style & Music**: Pick from cinematic styles and music vibes
3. **Generate Starting Frame**: AI creates the opening shot using DALL-E
4. **Chain Video Clips**: Each 10-second clip uses the previous clip's last frame as its first frame
5. **Stitch Together**: All clips are combined into a 60-second film

**The secret sauce**: Frame chaining creates smooth transitions and exceeds single-clip duration limits.

## Features

- **Multiple providers**: OpenAI Sora and Google Gemini support
- **8 film styles**: From cinematic to horror
- **6 music vibes**: Match the mood perfectly
- **Frame chaining**: Smooth transitions between clips
- **Resume support**: Continue interrupted generations
- **Progress tracking**: Beautiful progress bars and status updates
- **Interactive & non-interactive**: Conversational or config-driven

## Setup

Set API keys for your chosen provider:

```bash
# OpenAI (Sora)
export OPENAI_API_KEY="sk-..."

# Google Gemini
export GEMINI_API_KEY="..."
```

## Advanced Usage

### Resume Interrupted Generation

If generation is interrupted, resume from checkpoint:

```bash
short-film generate --resume
```

Progress is automatically saved after each step.

### Custom Output Directory

```bash
short-film generate \
  --premise "Your premise" \
  --output /path/to/output
```

## Use Cases

- Generate creative video content from text prompts
- Storytelling and narrative visualization
- Prototyping film ideas quickly
- Creating social media video content
- Educational videos with consistent visual style
- Art projects and experimental filmmaking
- Automated video content generation

## Tips

- Use interactive mode first to explore options
- Try different styles with the same premise for variety
- Frame chaining works best with coherent narratives
- Resume feature saves API costs on interruptions
- ffmpeg required for final video stitching
- Longer durations use more API credits (6 clips for 60s)

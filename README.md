# 🎬 Short Film

[![PyPI version](https://badge.fury.io/py/short-film.svg)](https://badge.fury.io/py/short-film)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate 60-second short films using AI video generation APIs. Creates cinematic videos by chaining clips together using last-frame-to-first-frame transitions.

## ✨ Features

- 🎥 **Multiple Video Providers**: OpenAI Sora and Google Gemini support
- 🎨 **8 Film Styles**: Cinematic, noir, anime, documentary, sci-fi, fantasy, horror, comedy
- 🎵 **Music Vibes**: Epic, suspenseful, calm, upbeat, dark, whimsical
- 🔗 **Frame Chaining**: Automatically chains clips by using the last frame as the first frame of the next clip
- 💾 **Resume Support**: Interrupted generations can be resumed from the last checkpoint
- 🎯 **Interactive & Non-interactive**: Use conversationally or with config files
- 📊 **Progress Tracking**: Beautiful progress bars and status updates

## 🚀 Quick Start

### Installation

```bash
# Using uv (recommended)
uv tool install short-film

# Using pipx
pipx install short-film

# Using pip
pip install short-film
```

### Usage

#### Interactive Mode (Recommended)

```bash
short-film generate
```

You'll be guided through the process:
1. Enter your film premise
2. Choose a visual style
3. Pick a music vibe
4. Watch as your film is generated!

#### Non-Interactive Mode

```bash
short-film generate \
  --premise "A lone astronaut discovers an alien artifact on Mars" \
  --style scifi \
  --music-vibe suspenseful \
  --provider openai \
  --duration 60
```

#### List Available Options

```bash
# Show all film styles
short-film styles

# Show all music vibes
short-film vibes
```

## 🎬 How It Works

1. **Align on Premise**: Describe your short film concept
2. **Choose Style & Music**: Pick from cinematic styles and music vibes
3. **Generate Starting Frame**: AI creates the opening shot using DALL-E
4. **Chain Video Clips**: Each 10-second clip uses the previous clip's last frame as its first frame
5. **Stitch Together**: All clips are combined into a 60-second film

**The secret sauce**: By chaining the last frame of each clip to the first frame of the next, we create smooth transitions and can exceed single-clip duration limits!

## 🔑 Setup

You'll need API keys for the video generation providers:

### OpenAI (Sora)

```bash
export OPENAI_API_KEY="sk-..."
```

### Google Gemini

```bash
export GEMINI_API_KEY="..."
```

## 📖 Advanced Usage

### Resume Interrupted Generation

If generation is interrupted, simply run the same command again:

```bash
short-film generate --resume
```

The tool automatically saves progress after each step and will continue from where it left off.

### Custom Output Directory

```bash
short-film generate \
  --premise "Your premise" \
  --output /path/to/output
```

### Disable Interactive Mode

```bash
short-film generate \
  --no-interactive \
  --premise "Your premise"
```

## 🎨 Film Styles

- **cinematic**: Dramatic, film-like quality with professional cinematography
- **noir**: Black and white, high contrast, dramatic shadows
- **anime**: Japanese animation style with vibrant colors
- **documentary**: Realistic, natural lighting, authentic feel
- **scifi**: Futuristic, high-tech, neon-lit environments
- **fantasy**: Magical, ethereal, fantastical elements
- **horror**: Dark, ominous, unsettling atmosphere
- **comedy**: Bright, colorful, lighthearted tone

## 🎵 Music Vibes

- **epic**: Grand, sweeping orchestral music
- **suspenseful**: Tense, dramatic, keeps you on edge
- **calm**: Peaceful, relaxing, ambient
- **upbeat**: Energetic, positive, fun
- **dark**: Ominous, foreboding, intense
- **whimsical**: Playful, quirky, lighthearted
- **none**: No music (video only)

## 🛠️ Requirements

- Python 3.9+
- ffmpeg (for video stitching)
- OpenAI API key (for Sora) or Google Gemini API key

### Installing ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Amazon Linux
sudo dnf install ffmpeg
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Credits

Built with:
- [OpenAI Sora](https://openai.com/sora) - AI video generation
- [Google Gemini](https://deepmind.google/technologies/gemini/) - Alternative video generation
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting

---

Made with ❤️ by [Aaron Levin](https://github.com/Olafs-World)

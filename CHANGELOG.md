# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-11

### Added
- Initial release of short-film CLI
- Support for OpenAI Sora and Google Gemini video generation
- 8 film styles (cinematic, noir, anime, documentary, scifi, fantasy, horror, comedy)
- 7 music vibes (epic, suspenseful, calm, upbeat, dark, whimsical, none)
- Interactive CLI flow with rich prompts
- Non-interactive mode with command-line options
- Frame chaining: last frame → first frame transitions between clips
- Resume/checkpoint support for interrupted generations
- Progress tracking with rich progress bars
- Image generation for starting frames using DALL-E
- Video stitching with ffmpeg
- Comprehensive test suite with unit and integration tests
- Beautiful terminal output with Rich library

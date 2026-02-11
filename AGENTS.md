# AGENTS.md - Developer Guide

This document contains instructions for AI agents and developers working on this project.

## Release Process

**⚠️ NEVER manually publish to PyPI!** Always use git tags - CI handles publishing automatically.

```bash
# 1. Update version in pyproject.toml
# Edit: version = "X.Y.Z"

# 2. Update CHANGELOG.md
# Add new version section with changes

# 3. Commit changes
git add -A
git commit -m "Bump version to X.Y.Z

Co-authored-by: olaf-s-app[bot] <259723076+olaf-s-app[bot]@users.noreply.github.com>"

# 4. Create and push tag
git tag vX.Y.Z
git push origin main
git push origin vX.Y.Z

# 5. CI automatically:
#    - Runs tests
#    - Builds package
#    - Publishes to PyPI
#    - Creates GitHub release
```

## Git Configuration

For commits to this repo:

```bash
git config user.name "Aaron Levin"
git config user.email "awlevin@comcast.net"
```

Always include co-author in commit messages:
```
Co-authored-by: olaf-s-app[bot] <259723076+olaf-s-app[bot]@users.noreply.github.com>
```

## Development

### Setup

```bash
# Clone repo
git clone https://github.com/Olafs-World/short-film.git
cd short-film

# Install dependencies
uv sync --all-extras --dev
```

### Running Tests

```bash
# Run unit tests only (fast)
uv run pytest -m "not integration"

# Run all tests including integration (requires API keys)
uv run pytest

# Run with coverage
uv run pytest --cov=short_film --cov-report=html
```

### Code Quality

```bash
# Run linter
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Local Testing

```bash
# Install in development mode
uv pip install -e .

# Run CLI
short-film --help
short-film styles
short-film vibes
```

## Code Style

- Use `ruff` for linting and formatting
- Line length: 100 characters
- Type hints encouraged but not required
- Docstrings for all public functions
- Keep functions focused and testable

## Testing Philosophy

- Unit tests should be fast and not require external services
- Mark integration tests with `@pytest.mark.integration`
- Integration tests can be skipped in CI (they cost money!)
- Aim for >80% coverage on unit tests

## Project Structure

```
short_film/
├── __init__.py          # Package metadata
├── cli.py              # CLI interface (Typer)
├── models.py           # Pydantic models
├── config.py           # Configuration management
├── state.py            # State/checkpoint management
├── image_gen.py        # DALL-E image generation
├── video_gen.py        # Video generation + frame chaining
├── stitcher.py         # ffmpeg video stitching
└── generator.py        # Main orchestrator

tests/
├── test_*.py           # Test files mirror source structure
└── conftest.py         # Shared fixtures (if needed)
```

## Key Principles

1. **Frame Chaining is Core**: The last-frame → first-frame chaining is what makes this tool special. Don't break it!

2. **Resume Must Work**: State management is critical. Users might lose connection or hit API limits.

3. **Great UX**: The CLI should be beautiful, informative, and forgiving. Use Rich for output.

4. **Handle Failures Gracefully**: APIs fail. Retry with exponential backoff. Save progress often.

5. **Production Quality**: This isn't a demo. Aaron is technical. Code quality matters.

## Future Enhancements

Ideas for v0.2.0+:

- [ ] Actual music generation/sourcing (currently music_vibe is just metadata)
- [ ] More video providers (Runway, Pika, etc.)
- [ ] Custom clip durations per clip
- [ ] Scene descriptions for each clip (more control)
- [ ] Prompt templates/presets
- [ ] Web UI
- [ ] Batch generation from CSV

"""State management for resume/checkpoint functionality."""

import json
from pathlib import Path
from typing import Optional

from .models import FilmState


class StateManager:
    """Manages persistent state for film generation."""

    def __init__(self, output_dir: Path):
        """Initialize state manager.

        Args:
            output_dir: Directory where state file will be stored
        """
        self.output_dir = Path(output_dir)
        self.state_file = self.output_dir / "state.json"

    def save(self, state: FilmState) -> None:
        """Save current state to disk.

        Args:
            state: Current film state
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Convert to dict with proper path serialization
        state_dict = state.model_dump(mode="json")

        with open(self.state_file, "w") as f:
            json.dump(state_dict, f, indent=2)

    def load(self) -> Optional[FilmState]:
        """Load state from disk.

        Returns:
            FilmState if state file exists, None otherwise
        """
        if not self.state_file.exists():
            return None

        with open(self.state_file, "r") as f:
            state_dict = json.load(f)

        return FilmState.model_validate(state_dict)

    def clear(self) -> None:
        """Clear saved state."""
        if self.state_file.exists():
            self.state_file.unlink()

"""Run a short non-interactive startup of the game and capture stdout logs.

This script patches Game.run to execute only a few frames so we get representative
structured logs (initialization, event dispatch, view opens, input logs) without
blocking indefinitely. The output is saved to docs/run_logs/sample_run.log.
"""

from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from decker_pygame.presentation.main import main


def short_run(self, max_frames: int = 5):
    """A short replacement for Game.run that steps the main loop a few times."""
    # Minimal loop that mirrors Game.run but bounded by frame count

    frame = 0
    while frame < max_frames and getattr(self, "is_running", True):
        # Simulate a tick without real clock dependence
        try:
            self.input_handler.handle_events()
        except Exception:
            # Don't let input handling stop the sample
            pass
        frame += 1


if __name__ == "__main__":
    out_dir = Path("docs/run_logs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "sample_run.log"

    # Patch Game.run with our short_run wrapper and capture stdout/stderr
    with open(out_path, "w", encoding="utf-8") as out_f:
        with redirect_stdout(out_f), redirect_stderr(out_f):
            with patch("decker_pygame.presentation.game.Game.run", new=short_run):
                # Run the composition root; plog writes to stdout by default
                main()

    # Informational message goes to the real stdout
    print(f"Sample run log written to {out_path}")

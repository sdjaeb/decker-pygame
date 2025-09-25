import json
import os
import subprocess
import sys
from pathlib import Path


def test_generate_sample_run_creates_log(tmp_path):
    """Run the sample-run script headless and assert the log file is created
    and parseable.

    This is a non-interactive smoke test intended for CI. It runs the
    existing script which patches Game.run to a short loop and writes
    stdout/stderr to docs/run_logs/sample_run.log. We force SDL into dummy
    mode for headless execution.
    """
    repo_root = Path(__file__).resolve().parents[2]
    script = repo_root / "scripts" / "generate_sample_run_log.py"
    out_log = repo_root / "docs" / "run_logs" / "sample_run.log"

    # Ensure old log does not interfere
    if out_log.exists():
        out_log.unlink()

    env = os.environ.copy()
    # Use the SDL dummy video driver so pygame doesn't require a display.
    env.setdefault("SDL_VIDEODRIVER", "dummy")
    # Ensure we use the same Python executable running pytest
    cmd = [sys.executable, str(script)]

    result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, f"script failed: {result.stderr}\n{result.stdout}"

    assert out_log.exists(), "Expected sample run log to be created"

    # Read the log and parse JSON entries. The sample_run.log may include
    # other textual lines; pick lines that look like JSON objects.
    entries = []
    with open(out_log, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            # Heuristics: JSON lines start with '{' and end with '}'
            if line.startswith("{") and line.endswith("}"):
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    # skip lines that are not pure JSON
                    continue

    assert entries, "No JSON log entries found in sample_run.log"

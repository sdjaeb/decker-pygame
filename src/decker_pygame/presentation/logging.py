"""Small presentation-layer logging helpers for human-reviewable stdout.

These are intentionally lightweight (print JSON to stdout) so CI and local runs
can be grepped and parsed. Keep dependencies minimal to avoid coupling.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any


def log(
    message: str, *, level: str = "INFO", category: str = "app", data: Any | None = None
) -> None:
    """Emit a structured log entry to stdout.

    Writes a small JSON object containing timestamp, level, category,
    message, and optional data. This is used across presentation code for
    human-reviewable and machine-parseable output during runs and tests.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "category": category,
        "message": message,
    }
    if data is not None:
        entry["data"] = data
    print(json.dumps(entry))

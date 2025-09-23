#!/usr/bin/env python3
"""Generate a report of all `# pragma: no cover` occurrences.

Writes a Markdown file to `docs/development/coverage_exceptions.md` with the
filename, line number, and surrounding context for each occurrence.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "development" / "coverage_exceptions.md"
PATTERN = re.compile(r"#\s*pragma:\s*no cover")


def scan_file(path: Path) -> list[tuple[int, str]]:
    """Return list of (lineno, line) for matches in a given file.

    This is resilient to encoding errors and returns an empty list on read
    failures.
    """
    hits: list[tuple[int, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return hits
    for i, line in enumerate(text.splitlines(), start=1):
        if PATTERN.search(line):
            hits.append((i, line.rstrip()))
    return hits


def gather() -> list[tuple[Path, int, str]]:
    """Walk the repository and collect pragma occurrences.

    Returns a list of tuples (relative_path, lineno, line).
    """
    results: list[tuple[Path, int, str]] = []
    for p in sorted(ROOT.rglob("*.py")):
        # ignore virtualenvs and docs build artifacts
        if "site-packages" in str(p) or "venv" in str(p) or "__pycache__" in str(p):
            continue
        file_hits = scan_file(p)
        for lineno, line in file_hits:
            results.append((p.relative_to(ROOT), lineno, line))
    return results


def render(results: list[tuple[Path, int, str]]) -> str:
    """Render the list of occurrences to Markdown text.

    The output groups each occurrence as a bullet with file and line context.
    """
    if not results:
        return "# Coverage exceptions\n\nNo `# pragma: no cover` occurrences found.\n"
    out = [
        "# Coverage exceptions\n",
        "The following `# pragma: no cover` occurrences were found:\n",
    ]
    for path, lineno, line in results:
        out.append(f"- **{path}**:{lineno}  \n  - `{line.strip()}`\n")
    return "\n".join(out)


def main() -> int:
    """Main entrypoint: generate the report and write it to disk."""
    results = gather()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(results), encoding="utf-8")
    print(f"Wrote coverage exceptions report to: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

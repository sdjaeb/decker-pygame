# How to run Decker (interactive) and capture logs

This document explains how to run the game locally and capture structured stdout logs for review.

Prerequisites
- Python 3.13+
- The project's virtualenv created via `uv venv` (see README)

Activate the venv

```bash
source .venv/bin/activate
```

Install dependencies (if not already done)

```bash
uv pip install -e ".[dev]"
```

Run the game (interactive)

```bash
decker
```

If you want a short non-interactive run that writes structured logs to `docs/run_logs/sample_run.log` (useful for auditing UI events and automations), run:

```bash
python3 scripts/generate_sample_run_log.py
```

This will run a short, bounded number of frames and write JSON log entries to `docs/run_logs/sample_run.log`.

Troubleshooting

- KeyError: 'dir' during startup
  - Cause: old `data/assets.json` entries using `file` shape. The code now supports both `file` and `dir`. If you edited `data/assets.json` manually and see issues, restore the repository version or use the `dir` form.

- Pygame display issues on headless CI
  - Use the test suite helpers and the DummyFont in `tests/conftest.py`. For CI, ensure SDL and Pygame are configured correctly (CI-specific steps vary by runner).

- No logs appear in `docs/run_logs/sample_run.log`
  - Check that the script ran without exceptions. The script will create the `docs/run_logs` directory and write to `sample_run.log`.

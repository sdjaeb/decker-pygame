# Run / Test Playbook

Purpose
-------
This playbook documents reproducible, non-interactive runs and checks for the
Decker Pygame project. It is both documentation and a living ledger of runs we
can execute locally or in CI to validate instrumentation, logging, and startup
integrations.

Layout
------
- Known-good flow: exact commands to exercise a short, auditable run.
- Expectations: what logs and artifacts should be produced.
- Troubleshooting notes for common startup failures.
- Ledger: timestamped entries of runs we've executed and what they proved.

Known-good flow (local)
-----------------------
1. Activate the virtualenv:

```bash
source .venv/bin/activate
```

2. Install dev deps (if necessary):

```bash
uv pip install -e ".[dev]"
```

3. Run the non-interactive sample run which writes structured logs to
   `docs/run_logs/sample_run.log`:

```bash
python3 scripts/generate_sample_run_log.py
```

4. Inspect the log (each line is usually a JSON entry):

```bash
sed -n '1,200p' docs/run_logs/sample_run.log
```

Known-good flow (CI-friendly)
-----------------------------
The same script can be executed in CI with SDL set to dummy:

```bash
SDL_VIDEODRIVER=dummy python3 scripts/generate_sample_run_log.py
```

Expectations
------------
- The script exits with return code 0.
- `docs/run_logs/sample_run.log` is created and contains one or more JSON log
  entries with `timestamp`, `level`, `category`, and `message` fields.

Troubleshooting
---------------
- KeyError: 'dir' — if observed, verify `data/assets.json` entries. The
  `AssetService` accepts both `file` (single image) and `dir` (directory of
  images). Prefer `file` for single images and `dir` for directories.
- Pygame display errors in CI — set `SDL_VIDEODRIVER=dummy` in the job's
  environment.

Ledger (entries)
-----------------

2025-09-24  — Added playbook and automation

- What: Implemented reliable sample-run capture and a CI-friendly integration
  test that runs the script headless and asserts the log contains JSON entries.
- Files added/changed:
  - `scripts/generate_sample_run_log.py` (redirect stdout/stderr to log)
  - `docs/run_instructions.md` (how-to)
  - `docs/run_playbook.md` (this file)
  - `tests/integration/test_sample_run.py` (headless integration test)
  - `docs/run_logs/sample_run.log` generated locally (not committed by default)

Status: committed to branch `feat/contract-loop` via an intermediate `run-audit` branch.

Next steps (ideas)
-------------------
- Expand the integration test to assert specific lifecycle messages.
- Add a CI job that runs the script and uploads `sample_run.log` as an artifact.
- Add a `scripts/compare_run_logs.py` helper to diff run logs and identify regressions.

Preserve release workflow
------------------------
When committing the run-audit changes (or any changes that will be merged into
`main`), preserve the existing release process: use Conventional Commits and
`commitizen` so the automated release tooling can correctly compute version
bumps and update the changelog. Typical flow:

```bash
# Stage changes
git add .
pre-commit run --all
cz commit
```

If you need to make a release after merging, use `cz bump --changelog` as
described in the project's README.

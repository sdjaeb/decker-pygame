# Docs & Repository Audit Checklist (2025-09-23)

This checklist was generated from a review of the repository's `docs/` and development notes. It is intended as a lightweight, actionable record of doc updates, CI alignment tasks, and low-risk follow-ups. No code changes are included here—this is documentation-only.

## High priority (blockers for contributors / CI)
- [ ] Validate CI and preflight instructions across `README.md`, `docs/development/*`, and `.github/workflows/*`:
  - Confirm the Python version used in CI and local `./scripts/preflight.sh` matches supported runtimes (project uses a `.venv/` with 3.13.x locally; CI examples currently show 3.11 in docs). Update docs or CI to align.
  - Ensure `scripts/generate_coverage_exceptions.py` output path and recommendation to fail CI on mismatches are accurate.

- [ ] Update `docs/development/coverage_exceptions.md` generation note to explain how to re-generate and when to accept changes (developer vs. maintainer review policy).

## Documentation accuracy and freshness
- [ ] Sync `README.md` and top-level docs to reflect current run instructions, including how to activate the project's venv (`.venv/`) and how to run the game for manual testing.
- [ ] Confirm examples in `docs/development/technical_learnings.txt` (e.g., `preflight` snippet, `functools.partial` notes) match the project's preferred workflows. Prefer documenting `scripts/preflight.sh` usage over shell snippets users must copy.
- [ ] Add a short “How to run the game locally” section: activate `.venv`, install deps (`pip install -e .`), and recommended runtime flags for headless testing (SDL env vars) and CI.

## Docs structure and discoverability
- [ ] Add an index in `docs/` or top-level `README.md` describing the purpose of `docs/architecture/`, `docs/development/`, and `docs/tech_debt/` so new contributors know where to look.
- [ ] Move or link transient files from `docs/tmp/` out of the main docs area or mark them clearly as drafts.

## Testing & coverage
- [ ] Document how to run the preflight locally: what it runs (pre-commit, ruff/format, mypy, pydoclint, pytest with coverage) and how `--cov-fail-under=100` affects contributors.
- [ ] Add a troubleshooting section for common local problems (example: `ModuleNotFoundError` unless `PYTHONPATH=src` or editable install is used; activating `.venv`).

## Architectural and technical-debt cross-checks
- [ ] Cross-reference `technical_debt.md` entries with code locations and tests. For each item, add an owning module/file and an approximate effort estimate (small/medium/large) for prioritization.
- [ ] Add a backlog item for integration harness documentation (see last section of `technical_debt.md`) and include a minimal example harness runnable by contributors.

## Low-hanging improvements (nice-to-have)
- [ ] Add `CONTRIBUTING.md` or extend `README.md` with repo conventions (coding style, test expectations, running formatters). Link to `pyproject.toml` and `pre-commit` config.
- [ ] Add a short developer checklist for common workflows: create feature branch, run `./scripts/preflight.sh`, update docs/technical_debt.md when adding `# pragma: no cover` exceptions.

## Next steps (suggested owners/actions)
- Assign a maintainer to own CI/doc updates and open a small PR to reconcile CI runtime and docs.
- Optionally extract this checklist to `docs/development/audit_checklist.md` (done) and track individual items as issues.
- Run the game locally and capture a short runbook listing missing runtime assets, env vars, and predictable failure modes (I can assist running this in your active environment when you're ready).

*Recorded on 2025-09-23.*

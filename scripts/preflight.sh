#!/usr/bin/env bash
set -euo pipefail

echo "Staging all changes..."
git add -A

echo "Generating coverage exceptions report..."
python3 scripts/generate_coverage_exceptions.py
# Stage the generated report so pre-commit can vet it if necessary
git add docs/development/coverage_exceptions.md || true

echo "Running pre-commit on staged files (fast path)..."
STAGED_FILES=$(git diff --name-only --cached || true)
if [ -n "${STAGED_FILES}" ]; then
  if ! pre-commit run --files ${STAGED_FILES}; then
    echo "Staged pre-commit hooks failed; running full pre-commit run to attempt auto-fixes..."
    if ! pre-commit run --all-files; then
      echo "pre-commit failed after full run. Showing git diff of automatic changes (if any):"
      git --no-pager diff || true
      echo "Please review and re-run preflight after fixing issues."
      exit 1
    fi
    git add -A
  fi
else
  echo "No staged files detected; running full pre-commit run..."
  if ! pre-commit run --all-files; then
    echo "pre-commit failed on full run. Showing git diff of automatic changes (if any):"
    git --no-pager diff || true
    exit 1
  fi
  git add -A
fi

echo "pre-commit passed. Running tests with coverage (enforce 100%)..."
# Fail if overall coverage is below 100
pytest --maxfail=1 --disable-warnings --cov=decker_pygame --cov-report=term-missing --cov-fail-under=100

echo "preflight completed successfully."

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.3.0] - 2025-07-01

### Feat

- **core**: ported remaining core models

### Fix

- **cicd**: fix github automation

### Feat

- **project**: better integrate pydantic
### Build
- **cicd**: Resolved multiple `mypy` and `ruff` issues within the CI/CD pipeline.
- **cicd**: Made the `.gitignore` file more comprehensive.
- **pre-commit**: Updated pre-commit hooks to remove warning messages.

## [v0.1.0] - 2025-06-29

### Feat
- **Project**: Established foundational project structure.
- **Core**: Added initial data models (`Character`, `Area`, `Contract`) and UI components (`AlarmBar`).
- **CI/CD**: Implemented a full CI/CD pipeline with GitHub Actions for automated testing, linting, and releases.
- **Tooling**: Integrated `commitizen` for conventional commits and `pre-commit` for local code quality checks.
### Docs
- Created initial project documentation (`README.md`, `architecture.md`, `porting_items.md`).
### Test
- Established the initial test suite using `pytest` and achieved 100% test coverage.
- Refactored asset loading and tests to be more dynamic.

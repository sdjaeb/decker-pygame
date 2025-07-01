# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.3.0 (2025-07-01)

### Feat

- **core**: ported remaining core models

### Fix

- **cicd**: fix github automation

## v0.1.0 (2025-06-30)

### Feat

- **project**: better integrate pydantic

## v0.2.0 (2025-06-29)

### Features

- **Core**: Established foundational data models (`Character`, `Area`, `Contract`) using Pydantic for runtime validation.
- **UI**: Added the `AlarmBar` component to display system alert levels.
- **CI/CD**: Implemented a full CI/CD pipeline with GitHub Actions for automated testing on pull requests and automated releases on merges to main.
- **Tooling**: Integrated `commitizen` for conventional commits and `pre-commit` for automated code quality checks (linting, formatting, testing).

### Bug Fixes

- **CI/CD**: Corrected the release workflow to ensure `commitizen` could find the project version and that the GitHub Actions bot had the correct permissions to push release commits and tags.
- **Linting**: Fixed various linting issues across the codebase.

### Documentation

- Created initial project documentation, including `README.md`, `architecture.md`, and `porting_items.md`.
- Updated `README.md` with detailed setup, development, and release instructions.

### Testing & Refactoring

- Established the initial test suite using `pytest` and achieved 100% test coverage.
- Refactored asset loading to dynamically load sprites from spritesheets and reorganized the asset directory structure.

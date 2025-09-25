# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.13.0 (2025-09-23)

### Feat

- **contracts**: Implement accept contract flow and state transition
- **ui**: Add 'Accept' button to ContractDataView
- **ui**: Make ContractDataView display selected contract details

### Fix

- **test**: stabilize test suite and resolve all quality checks

## v0.12.0 (2025-09-04)

### Feat

- **domain**: Add DiceService and complete porting phase

## v0.11.2 (2025-09-04)

## v0.11.1 (2025-09-04)

### Refactor

- **presentation**: Decouple all HomeState modal views from Game

## v0.11.0 (2025-09-01)

### Feat

- **engine**: Implement and integrate game state machine
- **engine**: Implement game state machine foundation

### Refactor

- **presentation**: Implement state machine and migrate view logic
- **presentation**: Migrate view management to concrete state classes
- **presentation**: Integrate ViewManager into Game class
- **engine**: Delegate main loop logic to state machine

## v0.10.0 (2025-08-18)

### Feat

- **ui**: Make ContractListView dynamic and interactive
- **matrix**: Populate MatrixRunView with live domain data

### Fix

- **testing**: Resolve test failures and coverage gaps

### Refactor

- **domain, tests**: Complete refactor from Host to System and harden UI tests

## v0.9.0 (2025-08-17)

### Feat

- **matrix**: Connect MatrixRunView to application service
- **presentation**: Complete MatrixRunView layout and stabilize tests
- Complete MatrixRunView UI layout with placeholders

### Fix

- **test**: Stabilize component tests and fix type errors

### Refactor

- **presentation**: Remove placeholder development borders

## v0.8.0 (2025-08-14)

### Feat

- **engine**: Implement DSFile entity and services
- **assets**: Implement data-driven AssetService

### Refactor

- **presentation**: Remove debug elements and streamline input

## v0.7.0 (2025-08-05)

### Docs

- Plan the final porting phase for the main application engine and the externalization of all game data.

## v0.6.0 (2025-08-05)

### Feat

- **projects**: Port Research & Development system, enabling players to research and build new software and chips.
- **ui**: Add `NewProjectView` and `ProjectDataView` for managing R&D.
- **ui**: Add reusable `ListView` component for displaying selectable lists.

### Fix

- **tests**: Refactor and harden tests for project-related callbacks in `test_game.py`.

## v0.5.0 (2025-07-11)

### Feat

- **ui**: Implement full deck management and refactor Game class
- **inventory**: Implement program transfer functionality
- **inventory**: Implement TransferView foundation and service logic
- **deck**: implement OrderView and re-ordering service
- **deck**: integrate DeckService and implement DeckView
- **deck**: introduce Deck aggregate and service
- **deck**: scaffold Deck Management views
- **architecture**: complete hexagonal architecture implementation
- **contracts**: lay foundation for contract system and harden tests
- **character**: implement interactive character data screen
- **game**: Add quit key and improve test suite robustness
- **components**: added build_view ui component

### Fix

- **tooling**: resolved a version conflict between git tags and the version in pyproject.toml

### Refactor

- **architecture**: make driving (application service) ports explicit
- **architecture**: make driven (repository) ports explicit

## [v0.4.0] - 2025-07-02

### Feat

- **project**: enhance the simple event service

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

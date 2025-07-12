# Decker-Pygame

![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A game development project built with the modern Pygame Community Edition.

## 📖 About the Project

This project is a modern Python port of the classic 2003 freeware Windows game, **Decker**. The goal is to recreate the original game's experience using modern development practices, a clean architecture, and the Pygame library.

- **Original Game Source:** [Decker on SourceForge](https://sourceforge.net/projects/decker/)
- **Playable Online Version:** [Decker (web port by @palparepa)](https://palparepa.github.io/decker/)

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended for environment and package management)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sdjaeb/decker-pygame.git
    cd decker-pygame
    ```

2.  **Create and activate a virtual environment using `uv`:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install the project and its development dependencies:**
    This command installs the project in "editable" mode (`-e`) and includes all development tools specified in `pyproject.toml`.
    ```bash
    uv pip install -e ".[dev]"
    ```

## 🧑‍💻 Development

This project is built on a foundation of modern software engineering principles to ensure it is robust, maintainable, and a pleasure to work on. For a deep dive into our architecture and development practices, please see our project documentation.

### Documentation

-   **[Architecture Overview](./docs/architecture.md):** The best starting point for understanding the project's structure.
-   **[Domain-Driven Design Guide](./docs/architecture/ddd_implementation_guide.md):** The rules and patterns we follow for DDD.
-   **[Hexagonal Architecture Guide](./docs/architecture/hexagonal_architecture.md):** How we use Ports & Adapters to isolate the core logic.
-   **[Project Roadmap](./docs/architecture/roadmap.md):** What features and enhancements are planned for the future.

### Project Philosophy & Architecture

Our architecture is designed to manage complexity and promote a clean separation of concerns.

-   **Domain-Driven Design (DDD):** We model the game's complex rules and logic at the very core of the application, isolated from technical details like databases or UI frameworks. This makes the business logic clear, explicit, and easy to test.

-   **Hexagonal Architecture (Ports & Adapters):** This pattern provides the structure for our DDD approach. The core application (the "hexagon") defines "ports" (interfaces) it needs to communicate with the outside world. The UI and persistence layers are "adapters" that plug into these ports. This makes the core independent and allows us to swap out external components easily.

-   **Event-Driven Foundation:** The system uses domain events to communicate significant state changes. This decouples components, allowing different parts of the application to react to events without being tightly bound to one another. This is a stepping stone towards our long-term goal of Event Sourcing.

### Quality & Automation

-   **100% Test Coverage:** We maintain a comprehensive test suite using `pytest` that covers every line of our application's logic. This provides a critical safety net, allowing for confident refactoring and rapid development.

-   **Automated Quality Checks:** We use `pre-commit` to run `ruff` (for linting and formatting) and our `pytest` suite before every commit. This ensures that all code pushed to the repository adheres to our quality standards.

-   **Continuous Integration & Delivery (CI/CD):** A GitHub Actions workflow automates the release process. When code is merged into `main`, it automatically calculates the next version number, updates the changelog, and creates a new release tag, ensuring a consistent and reliable release history.

### Pre-commit Hooks

We use `pre-commit` to automatically run linters, formatters, and tests before each commit. To set it up, run the following command after completing the installation steps:

```bash
pre-commit install
```

Now, `ruff` will automatically format your code and `pytest` will run the test suite on every commit, ensuring 100% test coverage is maintained.

### Committing Changes

This project follows the Conventional Commits specification. To help create compliant commit messages, we use `commitizen`.

Instead of `git commit`, use the following command:

```bash
cz commit
```

`commitizen` will prompt you through the process of creating a great commit message. The `pre-commit` hook will ensure that all commits adhere to this standard.

Before committing, the best practice for this workflow is to run the pre-commits before the cz commit - that way things aren't inadventently missed. It's fast and easy to run after every git add:

```bash
git add .
pre-commit run --all
```

### Development Mode

To enable development mode for rapid prototyping (e.g., giving the character extra starting credits), you can set an environment variable before running the game:

```bash
export DECKER_DEV_ENABLED=1
decker
```

This allows for temporary, config-driven changes without affecting test coverage.

#### What if a pre-commit hook fails?

If a hook fails (e.g., due to a linting error or a failing test), the commit will be aborted. However, your carefully crafted commit message is not lost.

1.  **Fix the issues** reported by the pre-commit hook in your code.
2.  **Stage the fixes** using `git add .`.
3.  **Commit again** using the standard `git commit` command:
    ```bash
    git commit
    ```
4.  Your text editor will open with your previous commit message already populated. Simply save and close the editor to finalize the commit.

### Automated Releases (CI/CD)

This project uses GitHub Actions to automate the release process. On every push to the `main` branch, a CI/CD workflow automatically:

1.  Determine the correct new version number based on your commit history (following Semantic Versioning).
2.  Update the version in `pyproject.toml`.
3.  Appends the latest changes to `CHANGELOG.md`.
4.  Commits the version change and changelog, and pushes it back to `main`.
5.  Creates a new git tag with the version number.

**Important:** After your pull request is merged, the `main` branch on GitHub will be updated with a new release commit. To keep your local repository in sync, you should:

```bash
# Switch to your local main branch
git checkout main

# Pull the latest changes, including the new release commit and tag
git pull
```

### Manual Release Process

This project uses `commitizen` to manage versioning and changelogs based on the Conventional Commits standard. When you are ready to create a new release, follow these steps:

1.  **Ensure you are on the `main` branch** and have pulled the latest changes.
2.  **Run the `commitizen` bump command:**
    ```bash
    cz bump --changelog
    ```
    This command will analyze your commit history, determine the correct version bump, update `pyproject.toml` and `CHANGELOG.md`, and create a new commit and tag.

3.  **Push the new commit and tag to GitHub:**
    ```bash
    git push --follow-tags
    ```
    This command pushes both your new release commit and its associated version tag to the remote repository.


### Running Tests Manually

To run the test suite manually at any time:

```bash
pytest
```

To run the test suite to review test coverage at any time:
```bash
pytest --cov=src/decker_pygame --cov-report=term-missing
```

## Asset Management

This project uses a structured `assets` directory. Game-ready assets are organized into subdirectories like `program_bmps/` and `sounds/`.

The `unused-assets/` directory contains the original, unsorted assets from the C++ project. As assets are integrated into the game, they should be moved from `unused-assets/` to the appropriate location within `assets/`.
```

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

This project uses a suite of modern Python tools to ensure code quality and consistency.

### Architecture

The codebase is structured following the principles of **Domain-Driven Design (DDD)** to ensure a clean separation of concerns and a focus on the core game logic.

- **[Implementation Guidelines](./docs/architecture/ddd_implementation_guide.md):** The rules and patterns we follow for DDD.
- **[DDD Concepts in Our Codebase](./docs/architecture/ddd_concepts.md):** A guide mapping DDD theory to specific files in this project.

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

This project uses GitHub Actions to automate the release process. On every merge to the `main` branch, a CI/CD workflow automatically:

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

### Running Tests Manually

To run the test suite manually at any time:

```bash
pytest
```

## Asset Management

This project uses a structured `assets` directory. Game-ready assets are organized into subdirectories like `program_bmps/` and `sounds/`.

The `unused-assets/` directory contains the original, unsorted assets from the C++ project. As assets are integrated into the game, they should be moved from `unused-assets/` to the appropriate location within `assets/`.
```

# Decker-Pygame

![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A game development project built with the modern Pygame Community Edition.

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
    uv pip install -e .[dev]
    ```

## 🧑‍💻 Development

This project uses a suite of modern Python tools to ensure code quality and consistency.

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

#### What if a pre-commit hook fails?

If a hook fails (e.g., due to a linting error or a failing test), the commit will be aborted. However, your carefully crafted commit message is not lost.

1.  **Fix the issues** reported by the pre-commit hook in your code.
2.  **Stage the fixes** using `git add .`.
3.  **Commit again** using the standard `git commit` command:
    ```bash
    git commit
    ```
4.  Your text editor will open with your previous commit message already populated. Simply save and close the editor to finalize the commit.

### Releasing a New Version

When you are ready to release a new version, `commitizen` can automatically:

1.  Determine the correct new version number based on your commit history (following Semantic Versioning).
2.  Update the version in `pyproject.toml`.
3.  Create a new `CHANGELOG.md` file or append the changes to the existing one.
4.  Commit the version change and changelog.
5.  Create a new git tag with the version number.

To do all of this, run the following command:

```bash
cz bump --changelog
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

# Decker-Pygame

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A game development project built with the modern Pygame Community Edition.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.11+
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

### Running Tests Manually

To run the test suite manually at any time:

```bash
pytest
```
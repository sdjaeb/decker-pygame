# Decker-Pygame

A modern Python port of the classic 2001 Cyberspace RPG, **Decker**, originally created by Shawn Overcash. This project aims to recreate the original game using Python 3.13+ and Pygame-CE, with modern development tools like `uv` and `ruff`.

## Original Project

The source code for the original C++/MFC project that this is based on is **DeckerSource_1_12**.

## Features (Planned)

*   Faithful recreation of the original gameplay mechanics.
*   Modernized codebase in Python with type hints.
*   Cross-platform compatibility thanks to Pygame.
*   UI and assets from the original game.

## Setup and Installation

This project uses `uv` for fast package management and virtual environments.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sdjaeb/decker-pygame.git
    cd decker-pygame
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:** For development (including the linter), install the `dev` extras:
    ```bash
    uv pip install -e ".[dev]"
    ```

## How to Run

Once the dependencies are installed, you can run the game using the script defined in `pyproject.toml`:

```bash
decker
```
# Architecture Overview

This document outlines the high-level architecture of the Decker-Pygame project, its core components, and the philosophy behind the port from the original C++ source.

## Project Structure

The project is organized into a `src/decker_pygame` directory, following modern Python packaging standards.

-   `src/decker_pygame/`: The main source code for the game.
    -   `model/`: Contains Pydantic data models (`Character`, `Area`, `Contract`, etc.) that represent the core game state. These are pure data structures with validation, containing no game logic.
    -   `components/`: Holds Pygame `Sprite` subclasses that represent visual UI elements (`ActiveBar`, `AlarmBar`, etc.). These components are responsible for their own rendering and state based on the game's data models.
    -   `game.py`: The central `Game` class, which manages the main game loop, event handling, state updates, and rendering orchestration.
    -   `settings.py`: Defines game-wide constants, configurations, and settings (e.g., screen dimensions, colors, asset paths).
    -   `asset_loader.py`: Utility functions for loading and processing game assets like images and spritesheets.
    -   `main.py`: The main entry point of the application.
-   `tests/`: Contains the `pytest` test suite, mirroring the structure of the `src` directory.
-   `assets/`: Contains all game assets, organized by type.
-   `docs/`: Project documentation, including this file.

## Porting Philosophy

The goal of this project is to create a modern, maintainable, and Pythonic port of the original Decker game. The process involves:

1.  **Identifying Core Concepts**: Analyzing the original C++ code (`.h` and `.cpp` files) to identify core data structures (like `CCharacter`, `CActiveBar`) and their responsibilities.
2.  **Modern Python Equivalents**: Translating these concepts into modern Python idioms.
    -   **Data Structures**: C++ structs and classes holding data are ported to Pydantic `BaseModel` classes for runtime validation and type safety.
    -   **UI Components**: C++ classes responsible for drawing (e.g., those with an `OnPaint` method) are ported to Pygame `Sprite` subclasses. Their `update()` and `image`/`rect` attributes handle the rendering logic.
    -   **Game Logic**: The central game loop and state management from the original `CMatrixView` or equivalent are being consolidated into the `Game` class.
3.  **Decoupling State and View**: A key architectural goal is to separate the game state (the Pydantic models) from the presentation (the Pygame components). The `Game` class will act as a controller, passing data from the models to the components for rendering.
4.  **Configuration over Hardcoding**: Values that were hardcoded in the C++ source (e.g., positions, sizes, colors) are being extracted into the `settings.py` file to make the game more configurable.

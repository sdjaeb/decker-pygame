# Issue: Data Directory Path is Relative to CWD

## Problem

Currently, the application's `data` directory, which stores all persistent game state (players, characters, etc.), is created relative to the **Current Working Directory (CWD)** from which the game is launched.

If you run `decker` from the project root, it creates `./data/`.
If you run it from `porting-state/`, it creates `porting-state/data/`.

This is unpredictable and not robust. The application's data storage should not depend on where the user happens to execute the command.

## Proposed Solution

The paths used to initialize the repositories in `presentation/main.py` should be made absolute. We should determine the project's root directory at runtime (e.g., by finding the location of `pyproject.toml` or by using the path of the `main.py` script) and construct an absolute path to the `data` directory from there.

This will ensure that the `data` folder is always created in a consistent, predictable location within the project structure, regardless of the CWD.

### Affected Components

-   `presentation/main.py`: The composition root where repositories are instantiated.
-   All `JsonFile*Repository` classes in the `infrastructure` layer: Their constructors will need to be updated to accept a base data path instead of hardcoding a relative one.

---

# Issue: Duplicated Logic in UI View Components

## Problem

Many of the UI view components (`CharDataView`, `DeckView`, `HomeView`, etc.) contain significant amounts of duplicated code:
1.  **Initialization:** The `__init__` methods all perform similar setup for creating a `pygame.Surface`, defining fonts and colors, and creating a `_components` group.
2.  **Event Handling:** The `handle_event` methods in each view contain nearly identical boilerplate logic to translate mouse coordinates to be relative to the view's `rect` before passing the event to child components.

This makes the views harder to maintain and introduces the risk of inconsistencies.

## Proposed Solution

Create a `BaseView` class that all other view components can inherit from.
-   The `BaseView` `__init__` method will handle the common setup of `self.image`, `self.rect`, fonts, and colors.
-   The `BaseView` will provide a standard `handle_event` implementation, removing this duplicated logic from all child classes.

### Affected Components

-   All classes in `src/decker_pygame/presentation/components/` that represent a full view/dialog (e.g., `HomeView`, `DeckView`, `CharDataView`, etc.).

---

# Issue: Game View Management is Brittle

## Problem

The `Game` class currently manages which view is active using a series of individual `Optional` attributes (e.g., `self.intro_view: IntroView | None`, `self.home_view: HomeView | None`). The logic for transitioning between views is scattered across various methods (`_continue_from_intro`, `_handle_character_creation`, etc.).

This approach is not scalable. As more views and game states are added, it will become increasingly complex and error-prone.

## Proposed Solution

Refactor the `Game` class to use a formal **State Machine**.
-   Define a `GameState` enum (e.g., `INTRO`, `NEW_CHAR`, `HOME`, `IN_GAME`).
-   The `Game` class will hold a single `current_state` attribute.
-   The main loop will delegate event handling, updates, and drawing to the `current_state` object.
-   State transitions will be handled explicitly, making the application flow clear and robust.

### Affected Components

-   `presentation/game.py`
-   `presentation/input_handler.py`

---

# Issue: Inconsistent Type Hinting Syntax

## Problem

Throughout the codebase, there is an inconsistent use of type hints for built-in collections. Some places may use the modern `list[int]` syntax, while others use the older `typing.List[int]`.

A previous commit reverted a change that standardized this, leaving the codebase in a mixed state. The project's `ruff` configuration (`UP007` is disabled) suggests a preference for the `typing` module's versions for consistency, possibly due to compatibility with older tools or libraries.

## Proposed Solution

Perform a codebase-wide audit and refactor all type hints for collections (`list`, `dict`, `tuple`, `Optional`, etc.) to use their counterparts from the `typing` module (e.g., `List`, `Dict`, `Tuple`, `Optional`). This will create a single, consistent style for type hinting across the project.

### Affected Components

-   Potentially all `.py` files in `src/`.

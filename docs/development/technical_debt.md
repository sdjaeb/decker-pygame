# Issue: Monolithic `Game` Class and Brittle View Management

## Problem

The `Game` class in `presentation/game.py` and its corresponding test file, `tests/presentation/test_game.py`, are becoming very large. The `Game` class is acting as a "god object" that manages every single view using a series of individual `Optional` attributes (e.g., `self.intro_view: IntroView | None`). The logic for transitioning between views is scattered across various methods, making it brittle and hard to follow.

This has several negative effects:
-   **High Cognitive Load:** It's difficult for developers to navigate and understand the flow of control.
-   **Maintenance Burden:** Adding new views or states requires modifying this central file, increasing the risk of introducing bugs.
-   **Tooling Performance:** Large files can slow down static analysis, linting, and even AI-assisted development.

## Proposed Solution

Refactor the `Game` class to use a formal **State Machine**.
-   Define a `GameState` enum (e.g., `INTRO`, `NEW_CHAR`, `HOME`, `IN_GAME`).
-   The `Game` class will hold a single `current_state` attribute.
-   The main loop will delegate event handling, updates, and drawing to the `current_state` object.
-   State transitions will be handled explicitly, making the application flow clear and robust.
-   Breaking the `Game` class into smaller, state-focused objects will naturally allow `test_game.py` to be split into smaller, more manageable test files (e.g., `test_home_state.py`, `test_shop_state.py`).

### Affected Components

-   `presentation/game.py`
-   `tests/presentation/test_game.py`
-   `presentation/input_handler.py`

---
# Issue: Hardcoded Shop Inventory

## Problem

The `ShopService` currently uses a hardcoded dictionary (`SHOP_INVENTORY`) to define the contents of all shops. This approach has several drawbacks:
- It violates our established repository pattern, where data persistence is handled by dedicated repository implementations in the `infrastructure` layer.
- It tightly couples the application service to a specific, static set of data.
- It makes it difficult to add new shops or modify shop inventories without changing application code.
- It prevents shop data from being persisted or modified dynamically during gameplay.

## Proposed Solution

1.  **Create a `ShopRepositoryInterface`** in the `ports` layer, defining methods like `get_by_name(name: str) -> Optional[Shop]` and `save(shop: Shop)`.
2.  **Implement a `JsonFileShopRepository`** in the `infrastructure` layer that reads shop data from dedicated JSON files.
3.  **Refactor `ShopService`** to be injected with a `ShopRepositoryInterface`. The service will now use the repository to fetch `Shop` aggregates instead of using the hardcoded dictionary.
4.  **Externalize the inventory data** into one or more JSON files in the `data/` directory.

This change will align the shop system with our established DDD and Hexagonal architecture, improving flexibility and maintainability.

### Affected Components
-   `application/shop_service.py`
-   `ports/repository_interfaces.py` (new `ShopRepositoryInterface`)
-   A new `infrastructure/json_shop_repository.py`.
---

# Issue: Data Directory Path is Relative to CWD

## Problem

Currently, the application's `data` directory, which stores all persistent game state (players, characters, etc.), is created relative to the **Current Working Directory (CWD)** from which the game is launched. This is unpredictable and not robust.

## Proposed Solution

The paths used to initialize the repositories in `presentation/main.py` should be made absolute. We should determine the project's root directory at runtime and construct an absolute path to the `data` directory from there. This will ensure that the `data` folder is always created in a consistent, predictable location.

### Affected Components

-   `presentation/main.py`: The composition root where repositories are instantiated.
-   All `JsonFile*Repository` classes in the `infrastructure` layer.

---

# Issue: Input Handler Ignores Modal Focus

## Problem

The current `PygameInputHandler` iterates through a hardcoded list of all potential views and sends events to any that are active. This breaks modal behavior. For example, when `ShopItemView` is open on top of `ShopView`, a mouse click will be processed by **both** views. A `_modal_stack` was introduced in the `Game` class to track focus, but the input handler does not currently use it.

## Proposed Solution

Refactor `PygameInputHandler.handle_events` to be aware of the `Game._modal_stack`. If the stack is not empty, events should be dispatched *only* to the topmost view on the stack.

### Affected Components
-   `presentation/input_handler.py`
-   `presentation/game.py`
---

# Issue: Duplicated Logic in UI View Components

## Problem

Many of the UI view components (`CharDataView`, `DeckView`, `HomeView`, etc.) contain significant amounts of duplicated code for initialization and event handling.

## Proposed Solution

Create a `BaseView` class that all other view components can inherit from. The `BaseView` will handle common setup and provide a standard `handle_event` implementation.

### Affected Components

-   All classes in `src/decker_pygame/presentation/components/` that represent a full view/dialog.

---

# Issue: Inconsistent Type Hinting Syntax

## Problem

Throughout the codebase, there is an inconsistent use of type hints for built-in collections (e.g., `list[int]` vs. `typing.List[int]`). The project's `ruff` configuration (`UP007` is disabled) suggests a preference for the `typing` module's versions.

## Proposed Solution

Perform a codebase-wide audit and refactor all type hints for collections to use their counterparts from the `typing` module (`List`, `Dict`, `Tuple`, `Optional`).

### Affected Components

-   Potentially all `.py` files in `src/`.

---

# Issue: Unorganized UI Component Directory

## Problem

The `src/decker_pygame/presentation/components` directory currently contains a mix of different types of UI elements (views, widgets, HUD elements) without a clear structure.

## Proposed Solution

Reorganize the `components` directory into subdirectories based on the type of UI element (e.g., `views/`, `widgets/`, `hud/`) to improve discoverability and clarify the architecture of the presentation layer.

### Affected Components

-   `src/decker_pygame/presentation/components/` and all files within it.
-   All files that import from the `components` directory.

---

# Issue: Program-related Logic is in DeckService

## Problem

Currently, logic for retrieving detailed program data resides in the `DeckService`, violating the Single Responsibility Principle and creating unnecessary coupling.

## Proposed Solution

Create a new `ProgramService` dedicated to all use cases related to programs themselves. Move the `get_ice_data` method from `DeckService` to the new `ProgramService`.

### Affected Components

-   `application/deck_service.py`
-   `ports/service_interfaces.py`
-   A new `application/program_service.py` and its interface.
---

# Issue: Tests Identify UI Components by Display Text

## Problem

Many component tests identify child components by their display text, creating a brittle coupling between the tests and the UI's cosmetic details.

## Proposed Solution

1.  **Add a stable identifier to UI components.** Modify base components like `Button` to accept an optional `name: str` or `test_id: str` in their constructor.
2.  **Refactor tests to use this identifier.** Update the tests to find components using this stable name instead of the display text.
3.  **Enforce this pattern** for all new components to prevent this issue from recurring.

### Affected Components
-   `presentation/components/button.py` and other base widgets.
-   All component tests in `tests/presentation/components/` that currently rely on display text.
---

# Issue: Maintaining 100% Test Coverage

## Problem

The project enforces 100% test coverage via a `pre-commit` hook. As the codebase grows, maintaining this standard becomes a significant, ongoing effort that needs to be explicitly tracked.

## Proposed Solution

For every new feature or refactoring, a corresponding work item must be included to write the necessary tests to maintain 100% coverage. This technical debt item serves as a reminder to budget time for testing in all future development.

### Affected Components

-   All new and existing code.
-   The `pre-commit` configuration.

# Issue: Monolithic `Game` Class and Test File

## Problem

The `Game` class in `presentation/game.py` and its corresponding test file, `tests/presentation/test_game.py`, are becoming very large. The `Game` class is acting as a "god object" that manages every single view, and its test file is a correspondingly large monolith.

This has several negative effects:
-   **High Cognitive Load:** It's difficult for developers to navigate and understand the flow of control.
-   **Maintenance Burden:** Adding new views or states requires modifying this central file, increasing the risk of introducing bugs.
-   **Tooling Performance:** Large files can slow down static analysis, linting, and even AI-assisted development, potentially contributing to issues like response truncation.

## Proposed Solution

Refactor the `Game` class to delegate its responsibilities. The existing technical debt item to "Refactor the Game View Management" using a State Machine is the correct long-term solution. This item is being added to raise the priority of that refactoring.

Breaking the `Game` class into smaller, state-focused objects will naturally allow `test_game.py` to be split into smaller, more manageable test files (e.g., `test_home_state.py`, `test_shop_state.py`).

### Affected Components
-   `presentation/game.py`
-   `tests/presentation/test_game.py`
---
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

# Issue: Input Handler Ignores Modal Focus

## Problem

The current `PygameInputHandler` iterates through a hardcoded list of all potential views and sends events to any that are active. This breaks modal behavior. For example, when `ShopItemView` is open on top of `ShopView`, a mouse click will be processed by **both** views. This can lead to unintended actions, like closing the parent view when clicking a button on the child modal.

A `_modal_stack` was introduced in the `Game` class to track focus, but the input handler does not currently use it, rendering the modal system ineffective and buggy.

## Proposed Solution

Refactor `PygameInputHandler.handle_events` to be aware of the `Game._modal_stack`. If the stack is not empty, events (especially mouse events) should be dispatched *only* to the topmost view on the stack (`_modal_stack[-1]`). This will ensure that only the focused modal can receive input, which is the correct and expected behavior for a modal UI system.

### Affected Components
-   `presentation/input_handler.py`
-   `presentation/game.py`
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

---

# Issue: Unorganized UI Component Directory

## Problem

The `src/decker_pygame/presentation/components` directory currently contains a mix of different types of UI elements without a clear structure. It includes:
-   High-level views/dialogs (e.g., `HomeView`, `DeckView`).
-   HUD elements (e.g., `HealthBar`, `AlarmBar`).
-   Low-level, reusable widgets (e.g., `Button`, `TextInput`).

This makes it difficult to navigate the codebase and understand the role of each component.

## Proposed Solution

Reorganize the `components` directory into subdirectories based on the type of UI element (e.g., `views/`, `widgets/`, `hud/`). This will improve discoverability and clarify the architecture of the presentation layer. All import statements will need to be updated accordingly.

### Affected Components

-   `src/decker_pygame/presentation/components/` and all files within it.
-   All files that import from the `components` directory.

---

# Issue: Program-related Logic is in DeckService

## Problem

Currently, logic for retrieving detailed program data (like for the `IceDataView`) resides in the `DeckService`. While this is functional for now, it violates the Single Responsibility Principle. The `DeckService` should be concerned with managing the contents of a deck, not with being a general-purpose query service for all programs.

If other parts of the application (like a `ShopView` or a future `ProgramUpgradeView`) need to query program details, they would be forced to depend on the `DeckService`, creating unnecessary coupling.

## Proposed Solution

Create a new `ProgramService` dedicated to all use cases related to programs themselves.
-   Move the `get_ice_data` method from `DeckService` to the new `ProgramService`.
-   In the future, any new program-specific logic (e.g., `upgrade_program`, `get_program_stats`) should be added to this service.
-   This will make the `DeckService`'s responsibility clearer and reduce coupling between different application services.

### Affected Components

-   `application/deck_service.py`
-   `ports/service_interfaces.py` (for `DeckServiceInterface`)
-   A new `application/program_service.py` and its interface.
---

# Issue: Tests Identify UI Components by Display Text

## Problem

Many component tests, such as `test_file_access_view.py`, identify specific child components by their display text. For example:

```python
delete_buttons = [
    c for c in file_access_view._components if isinstance(c, Button) and c.text == "Delete"
]
```

This creates a brittle coupling between the tests and the UI's cosmetic details. If a designer decides to change the button's text from "Delete" to "Remove", the test will fail even though the button's functionality (its `on_click` callback) is unchanged. Tests should validate behavior, not presentation.

## Proposed Solution

1.  **Add a stable identifier to UI components.** Modify base components like `Button` to accept an optional `name: str` or `test_id: str` in their constructor. This identifier would be for testing and identification purposes only and would not be displayed.
2.  **Refactor tests to use this identifier.** Update the tests to find components using this stable name (`if c.name == "delete_file_button"`) instead of the display text.

This change decouples the tests from the UI's text, making them more robust and less likely to break due to cosmetic changes.

### Affected Components
-   `presentation/components/button.py` and other base widgets.
-   All component tests in `tests/presentation/components/` that currently rely on display text for component identification.

# Issue: Inconsistent `noqa` Requirements for Type-Only Imports

## Problem

In `ports/repository_interfaces.py`, we use `# noqa: F401` to prevent `ruff` from removing certain imports that are only used for type hinting. However, this is applied inconsistently, which can be confusing.

-   `from decker_pygame.domain.character import Character` **requires** `# noqa: F401`.
-   `from decker_pygame.domain.player import Player` **does not** require it.

This happens because `ruff`'s unused-import rule (`F401`) is smart enough to see when a type is used in a method signature (e.g., `def get_by_name(...) -> Optional["Player"]:`), but it fails to see the usage when the type is *only* used as a string forward reference in a generic base class list (e.g., `class CharacterRepositoryInterface(Repository[CharacterId, "Character"], ...)`).

This forces us to manually suppress the linter error for some imports but not others, creating an inconsistent and potentially fragile pattern that relies on developer knowledge of this specific linter quirk.

## Proposed Solution

The current solution is to apply `# noqa: F401` where needed. This is a form of technical debt because we are working around a limitation in our tooling.

A long-term solution would be to monitor `ruff`'s development. If a future version of `ruff` correctly handles this type of usage, or if a configuration option becomes available to change this behavior, we should adopt it and remove the `noqa` comments.

This item serves as documentation for the current workaround and a reminder to investigate better solutions in the future.

### Affected Components

-   `ports/repository_interfaces.py`
-   `pyproject.toml` (if a `ruff` configuration option becomes available)

---
# Issue: Monolithic `MatrixRunView` Component

## Problem

The `MatrixRunView` class in `presentation/components/matrix_run_view.py` is becoming a large, monolithic component. It manually initializes and manages over a dozen child components (health bars, map view, message view, etc.) with hardcoded positions and sizes. This tight coupling makes the view difficult to test, maintain, and reason about. Any change to the matrix run UI requires modifying this single, large file.

## Proposed Solution

Refactor the `MatrixRunView` to use a more data-driven or declarative approach for its layout.

1.  **Externalize Layout Configuration:** Move the positions and sizes of child components from hardcoded values in the `__init__` method to a configuration file (e.g., a dedicated section in `assets.json` or a new `ui_layouts.json`).
2.  **Component Factory:** Create a factory function or class that reads this configuration and dynamically creates and positions the child components.
3.  **Data-Driven Updates:** The `MatrixRunView.update` method would then iterate through its managed components and update them, but the creation and layout logic would be separated.

This will decouple the `MatrixRunView` from the specific layout of its children, making the UI more flexible and the component itself simpler.

### Affected Components

-   `presentation/components/matrix_run_view.py`
-   `tests/presentation/components/test_matrix_run_view.py`
-   Potentially a new UI layout configuration file.

---
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

# Issue: Generic Naming for Matrix-related Domain Models

## Problem

The domain models for computer systems in the matrix, `System` and `Node`, use generic names that could be confused with other concepts (e.g., the operating system, or graph nodes in general). The code would be more self-documenting and flavorful if it used more thematic, cyberpunk-inspired terminology.

## Proposed Solution

Refactor the domain models and all related components to use more evocative names:
-   Rename `System` to `Host`.
-   Rename `Node` to `Subsystem`.
-   Rename `SystemId` to `HostId`.
-   Rename `NodeId` to `SubsystemId`.
-   Rename `SystemRepositoryInterface` to `HostRepositoryInterface`.
-   Update all services, DTOs, views, and tests that currently reference `System` or `Node`.

This change will improve the clarity of the Ubiquitous Language within the codebase, making it easier for developers to understand the purpose of these components at a glance.

### Affected Components

-   All files related to the `System` and `Node` domain models.

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

# Issue: Input Handler Ignores Modal Focus (Status: Complete)

**Resolution:** The `PygameInputHandler` was refactored to check the `Game._modal_stack`. If the stack is not empty, events are now dispatched *only* to the topmost view, correctly implementing modal behavior. The old logic of broadcasting events to all views has been removed.

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
---

# Issue: Magic Numbers for Work Units in ProjectService

## Problem

Currently, the `ProjectService.work_on_project` method accepts an integer representing an amount of time. The presentation layer (`Game` class) calls this service with hardcoded "magic numbers" (`1` for a day, `7` for a week). This has a few disadvantages:
-   **Lack of Clarity:** The meaning of the integer `1` is not immediately obvious from the service's method signature.
-   **Brittleness:** If we ever wanted to change the scale of work units (e.g., from days to hours, where a "day" would become `24`), we would have to find and update these magic numbers in the presentation layer.
-   **Inconsistency:** It violates the principle of making the domain language explicit.

## Proposed Solution

1.  **Create a `WorkUnit` Enum:** In the `domain` layer (e.g., `domain/project.py`), create a new `WorkUnit(Enum)` with members like `DAY = 1` and `WEEK = 7`.
2.  **Refactor `ProjectService`:** Update the `work_on_project` method to accept a `WorkUnit` enum member. The service will then use the enum's `value` to perform its calculations.
3.  **Update `Game` Callbacks:** Refactor the `_on_work_day` and `_on_work_week` methods in `presentation/game.py` to pass the appropriate enum member (e.g., `WorkUnit.DAY`) to the service.

This change will make the domain concept of a "work unit" explicit, improving code clarity and maintainability.

### Affected Components
-   `application/project_service.py`
-   `presentation/game.py`
-   `domain/project.py`
---

# Issue: Placeholder for Current Rating in Project View

## Problem

The `ProjectDataViewDTO` and its underlying `SourceCodeDTO` have a field for `current_rating`, which is intended to show the rating of a schematic's item that the character currently has installed. The `ProjectService` currently populates this with a placeholder `"-"`.

To fully implement this, the service would need to query the character's equipped software (from the `Deck`) and installed chips, which is currently outside its scope.

## Proposed Solution

1.  Enhance the `Character` aggregate with methods to query for installed software/chip ratings by name.
2.  Update the `ProjectService.get_project_data_view_data` method to use these new queries to populate the `current_rating` field accurately.

This will provide more useful information to the player in the R&D screen.

### Affected Components
-   `domain/character.py`
-   `application/project_service.py`
---

# Issue: Hardcoded R&D Project Availability

## Problem

Similar to the "Hardcoded Shop Inventory" issue, the `ProjectService.get_new_project_data` method uses hardcoded lists of available software and chip classes for research. This makes it difficult to add or modify the available research options without changing application code.

## Proposed Solution

1.  **Externalize the data:** Create one or more JSON files in the `data/` directory to define the available researchable items (software and chips), including their base complexity values (see `NewProjectDlg.cpp` for original logic).
2.  **Create a Repository:** Define a `ResearchRepositoryInterface` in the `ports` layer and a `JsonFileResearchRepository` in the `infrastructure` layer to load this data.
3.  **Refactor `ProjectService`:** Inject the `ResearchRepositoryInterface` into the `ProjectService`. The service will now use the repository to fetch the lists of available projects instead of using hardcoded lists.

This change will make the R&D system more data-driven and maintainable.

### Affected Components
-   `application/project_service.py`
-   `ports/repository_interfaces.py` (new `ResearchRepositoryInterface`)
-   A new `infrastructure/json_research_repository.py`.
-   New data files in `data/`.
---

# Issue: Discrepancy in Project Time Calculation

## Problem

There is a notable difference between the original C++ project time calculation and the new Python implementation.

*   **Original C++ Logic (`NewProjectDlg.cpp`):** Used a "complexity" value for each item class (e.g., `GetProgramComplexity`) and a skill-based division to reduce time (`time = (base_time + skill - 1) / skill`). This created a non-linear reduction in time as skill increased.
*   **Current Python Logic (`project_service.py`):** Uses a simplified formula based on the target rating squared (`rating^2 * 100`) and subtracts values based on existing ratings and skill levels.

The current implementation is a valid design choice for game balance, but it deviates from the original game's mechanics.

## Proposed Solution

This is not an urgent issue, but a design choice to be aware of. If we decide to restore the original game's feel, the following steps would be necessary:

1.  **Externalize Complexity Data:** As part of the "Hardcoded R&D Project Availability" task, the data files for researchable items should include their base "complexity" value.
2.  **Update `ProjectService`:** Refactor the `start_new_project` method to use the complexity value and the original division-based formula to calculate `time_required`.

This would more accurately replicate the original game's progression curve for research and development.

### Affected Components
-   `application/project_service.py`
-   Data files created for R&D project availability.
---

# Issue: Lack of End-to-End / Integration Testing

## Problem

Our current test suite consists entirely of unit tests with mocked dependencies. While this is excellent for verifying the logic of individual components in isolation, it cannot answer critical questions about the application as a whole when it's actually running. We have no automated way to verify:
-   **UI Layout:** Are UI elements placed correctly on the screen and do they overlap unexpectedly?
-   **Modal Stack Integrity:** Do nested dialogs (e.g., `ShopView` -> `ShopItemView`) open and close correctly, always returning focus to the correct parent view?
-   **Data Binding:** When a domain model changes, does the UI update correctly in a running game?
-   **Full Gameplay Loops:**
    -   Can a player accept a contract, complete it, receive payment, go to a shop, and successfully purchase an item? (The "Mercenary Loop")
    -   Can a player start a research project, complete it, build the schematic, and transfer the new program to their deck? (The "Inventor Loop")
-   **Game Lifecycle:** Does the application start and exit gracefully without errors?
-   **Persistence Integrity:** Does saving and loading the game correctly restore the full character state (inventory, deck order, credits, etc.)?
-   **Core Mechanics:** Do systems like combat, resting, and crafting function correctly from end to end?
-   **Randomness & Balance:** Do random systems (like die rolls or loot drops) behave within expected parameters?
-   **Error Resilience:** Does the UI respond gracefully with a message when an action fails (e.g., trying to buy an unaffordable item), or does it crash?

Manually testing these scenarios is time-consuming and error-prone.

## Proposed Solution

Build a custom integration testing harness. While generic GUI automation tools like `pyautogui` exist, they are often brittle and slow. A custom harness that interacts directly with the Pygame event loop would be more robust and maintainable.

The harness would involve:
1.  **A Test Runner:** Continue using `pytest`.
2.  **A Controlled Game Loop:** Tests would manually advance the game one frame at a time (`game.run_one_frame()`) instead of letting it run freely. This makes tests deterministic.
3.  **An "Agent" or "Driver":** A test helper class that provides high-level methods to simulate user actions, such as:
    -   `agent.press_key(pygame.K_h)`
    -   `agent.click_view_button("HomeView", "Shop")`
    -   `agent.type_in_active_view("password123")`
4.  **Programmatic Event Injection:** The agent would simulate input by creating `pygame.event.Event` objects and posting them directly to Pygame's event queue.
5.  **State Inspection:** The agent would hold a reference to the `Game` instance, allowing tests to make assertions directly against the state of the UI and domain (e.g., `assert agent.game.shop_view is not None`).

A test case using this harness might look like this:

```python
# tests/integration/test_shop_flow.py
def test_purchasing_an_unaffordable_item_shows_error_message(game_agent):
    # 1. Setup: Navigate to the shop
    game_agent.press_key(pygame.K_h)  # Open HomeView
    game_agent.run_frames(10) # Let UI settle
    game_agent.click_button_with_text("Shop")
    game_agent.run_frames(10)

    # 2. Action: Try to buy an item we can't afford
    # (The test setup would ensure the character has low funds)
    game_agent.click_button_with_text("Buy 'Expensive ICE'")

    # 3. Assert: Check the game state
    game = game_agent.game
    assert "Insufficient credits" in game.message_view.text
    assert game.shop_view is not None # The shop should still be open
```

This would provide a powerful safety net for catching visual regressions and bugs in complex user workflows that unit tests cannot detect.

### Affected Components
-   A new test harness, likely living in `tests/integration/harness.py`.
-   A new test suite, likely in a `tests/integration/` directory.

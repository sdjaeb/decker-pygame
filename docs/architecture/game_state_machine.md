# Game State Machine Architecture

This document details the implementation of the Game State Machine pattern in the Decker-Pygame project. This pattern is a cornerstone of the presentation layer's architecture, designed to manage the game's flow and reduce the complexity of the main `Game` class.

## 1. The Problem: A Monolithic `Game` Class

In earlier stages of development, the `Game` class was responsible for managing every single UI view, handling all game logic, and processing all state transitions. This resulted in a "god object" that was difficult to maintain, test, and reason about. Key issues included:

-   **High Coupling:** The `Game` class was tightly coupled to every view and every piece of game logic.
-   **Scattered Logic:** The rules for transitioning between different parts of the game (e.g., from the main menu to the shop) were scattered across various methods.
-   **Poor Scalability:** Adding a new screen or major feature required significant modifications to this central, complex class.

## 2. The Solution: A State-Driven Approach

To solve these problems, we implemented a formal Game State Machine. In this pattern, the application's flow is broken down into a finite number of distinct **states**. The `Game` class is no longer responsible for *what* to do, but rather for running the **currently active state**.

### Core Components

Our implementation consists of several key components working in concert:

#### a. `GameState` Enum (`src/decker_pygame/presentation/states/game_states.py`)

This `Enum` defines all possible high-level states the game can be in.

```python
class GameState(Enum):
    INTRO = auto()
    NEW_CHAR = auto()
    HOME = auto()
    MATRIX_RUN = auto()
    QUIT = auto()
```

#### b. `BaseState` Protocol (`src/decker_pygame/presentation/states/game_states.py`)

This `Protocol` defines the contract that all concrete state classes must adhere to. It ensures that the `Game` class can interact with any state in a consistent way.

```python
class BaseState(Protocol):
    def on_enter(self) -> None: ...
    def on_exit(self) -> None: ...
    def handle_event(self, event: pygame.event.Event) -> None: ...
    def update(self, dt: float) -> None: ...
    def draw(self, screen: pygame.Surface) -> None: ...
```

#### c. Concrete State Classes (`src/decker_pygame/presentation/states/states.py`)

These are the actual implementations of the states, such as `IntroState`, `HomeState`, and `MatrixRunState`. Each state class is responsible for:

-   **Managing its primary view:** In its `on_enter` method, a state creates and displays its main UI view (e.g., `HomeState` creates `HomeView`). In `on_exit`, it cleans up that view.
-   **Managing its modal views:** All secondary, modal views (like `ShopView` or `DeckView`) are now managed entirely within the state that uses them (e.g., `HomeState`).
-   **Delegating updates and drawing:** The state's `update` and `draw` methods typically delegate to the `Game` class's helper methods, which contain the core sprite update and drawing logic.

#### d. The `Game` Class as a State Machine Runner (`src/decker_pygame/presentation/game.py`)

The `Game` class has been refactored to be a lean state machine runner. Its primary responsibilities in this pattern are:

-   Holding a reference to the `current_state`.
-   Providing a `set_state(new_state)` method to transition between states. This method handles calling `on_exit` on the old state and `on_enter` on the new one.
-   Delegating the main loop's `update` and `draw` calls to the `current_state`.

#### e. The `ViewManager` (`src/decker_pygame/presentation/view_manager.py`)

The `ViewManager` is a helper class owned by `Game`. It is responsible for the low-level mechanics of adding and removing views from the game's sprite group and managing the modal stack for input focus. States use the `ViewManager` to show and hide their views.

### 3. Example Flow: Transitioning from Intro to New Character

1.  The game starts, and `Game.set_state(GameState.INTRO)` is called.
2.  The `Game` class creates an instance of `IntroState` and sets it as `self.current_state`.
3.  `IntroState.on_enter()` is called. It uses the `ViewManager` to create and display the `IntroView`.
4.  The player clicks the "Continue" button in the `IntroView`.
5.  The button's callback, `Game._continue_from_intro()`, is executed.
6.  This method calls `Game.set_state(GameState.NEW_CHAR)`.
7.  The `Game` class calls `IntroState.on_exit()`, which removes the `IntroView`.
8.  The `Game` class then creates an instance of `NewCharState` and sets it as the new `current_state`.
9.  `NewCharState.on_enter()` is called, which creates and displays the `NewCharView`.

### 4. Benefits of this Architecture

-   **Separation of Concerns:** The `Game` class is no longer concerned with the details of any specific screen. Each state is a self-contained unit of functionality.
-   **Improved Maintainability:** Adding a new screen is as simple as creating a new state class and adding it to the `GameState` enum.
-   **Clearer Application Flow:** State transitions are explicit and centralized in the `set_state` method, making the game's overall flow much easier to follow.
-   **Enhanced Testability:** Each state can be tested in isolation, and the `Game` class's state transition logic can be tested independently of any specific UI.

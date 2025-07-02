# Domain-Driven Design (DDD) Implementation Guidelines

## 1. Philosophy

This is a living document. It starts with the core principles we will adopt immediately. As our codebase evolves and we encounter new patterns, this document will be updated.

Our goal is to build software that is:
- **Domain-Centric:** The game's rules and logic are the heart of our application.
- **Maintainable:** Code is separated by concern, making it easier to understand and change.
- **Event-Driven:** We use domain events to communicate changes and decouple components.

## 2. Core Patterns

### 2.1. Layered Architecture

We separate our code into layers. **Dependencies must only point inwards.**

1.  **Domain Layer (Core):** Contains the business logic, rules, and state. It has **zero** dependencies on other layers.
    -   *Building Blocks:* Aggregates, Entities, Value Objects, Domain Events, Repository Interfaces.
2.  **Application Layer:** Orchestrates domain objects to execute use cases.
    -   *Building Blocks:* Application Services, Data Transfer Objects (DTOs).
3.  **Infrastructure Layer:** Implements the technical details for interfaces defined in inner layers.
    -   *Building Blocks:* Concrete Repositories (file-based persistence), event bus implementations.
4.  **Presentation Layer:** The user-facing part of the application. For us, this is the Pygame game loop, rendering, and UI widgets. It interacts with the Application Layer and should be as stateless as possible, receiving its state from services during updates.

### 2.2. Aggregates

An Aggregate is a cluster of domain objects that we treat as a single transactional unit. The **Aggregate Root** is the single entry point to the aggregate.

**Example:** A `Player` is an Aggregate Root. It might contain a list of `Item` objects. To add an item to the player's inventory, you would call `player.add_item(item)`, not modify the item list directly.

**Rules:**
- **Reference by Root:** External objects can only hold a reference to the Aggregate Root.
- **Enforce Invariants:** The Root is responsible for ensuring the aggregate is always in a valid state.
- **Transactional Consistency:** All changes within an aggregate are committed together.

### 2.3. Domain Events

A Domain Event is an object that represents something that happened in the domain. They are a critical part of our event-driven baseline.

**Rules:**
- **Immutable:** Events represent the past; they cannot be changed.
- **Named in Past Tense:** e.g., `PlayerCreated`, `PlayerTookDamage`.
- **Decoupling:** Events allow other parts of the system to react to changes without being tightly coupled.
- **Implementation:** The Aggregate Root creates and collects events. The Application Service dispatches these events *after* the transaction is successfully committed.

### 2.4. Connecting The Layers (Dependency Injection)

The layers are connected at the application's entry point (the "Composition Root"), which for us is `presentation/main.py`.

The `main` function is responsible for:
1.  Instantiating concrete infrastructure components (e.g., `JsonFilePlayerRepository`).
2.  Instantiating application services and injecting the infrastructure components into them (e.g., `PlayerService(repo)`).
3.  Instantiating the main presentation object (e.g., the `Game` class) and injecting the application services into it (e.g., `Game(player_service)`).

This pattern, known as **Dependency Injection**, ensures that high-level components (like `Game`) depend on abstractions (`PlayerService`), not on concrete details. This makes the system flexible, maintainable, and highly testable.

## 3. Initial Persistence Strategy

To start quickly and avoid external dependencies, we will use a simple file-based persistence mechanism.

- **Strategy:** We will implement repositories that serialize aggregates to and from JSON files.
- **Location:** This implementation will live in the `infrastructure` layer, completely separate from the domain model. This allows us to easily swap it for SQLite or another database later without changing any business logic.

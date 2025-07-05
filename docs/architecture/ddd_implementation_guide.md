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
    -   *Base Classes:* The foundational `Entity` and `AggregateRoot` classes live in the `domain/ddd/` sub-package.
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
- **Reference by ID:** An Aggregate Root should refer to other aggregates by their ID, not by holding a direct object reference. This keeps aggregates small and loosely coupled.
- **Transactional Consistency:** All changes within an aggregate are committed together.

### 2.3. Domain Events

A Domain Event is an object that represents something that happened in the domain. They are a critical part of our event-driven baseline.

**Rules:**
- **Immutable:** Events represent the past; they cannot be changed.
- **Named in Past Tense:** e.g., `PlayerCreated`, `PlayerTookDamage`.
- **Decoupling:** Events allow other parts of the system to react to changes without being tightly coupled.
- **Implementation:** The Aggregate Root creates and collects events. The Application Service dispatches these events *after* the transaction is successfully committed.

### 2.4. Domain Event Decorators

To improve code clarity and discoverability, we use decorators to explicitly mark the producers and consumers of domain events.

-   **`@emits(EventType)`**: This decorator is placed on methods (typically on an Aggregate Root) that are responsible for creating one or more domain events. It serves as a clear, self-documenting signpost for event creation.

-   **`@handles(EventType, ...)`**: This decorator is placed on functions (event handlers) to mark them as consumers of one or more domain events.

These decorators attach metadata to the functions, which primarily serves a semantic purpose but could be used for advanced features like auto-discovery of handlers in the future.

### 2.5. Conditional Event Handling

The `EventDispatcher` supports conditional subscriptions. When subscribing a handler, you can provide an optional `condition` function. The handler will only be executed if an event is dispatched *and* the condition function returns `True` for that event.

This is useful for creating specialized handlers that only react to events with specific data, without cluttering the handler itself with conditional logic.

### 2.6. Connecting The Layers (Dependency Injection)

The layers are connected at the application's entry point (the "Composition Root"), which for us is `presentation/main.py`.

The `main` function is responsible for:
1.  Instantiating concrete infrastructure components (e.g., `JsonFilePlayerRepository`).
2.  Instantiating application services and injecting the infrastructure components into them (e.g., `PlayerService(repo)`).
3.  Instantiating the main presentation object (e.g., the `Game` class) and injecting the application services into it.

This pattern, known as **Dependency Injection**, ensures that high-level components (like `Game`) depend on abstractions (`PlayerService`), not on concrete details. This makes the system flexible, maintainable, and highly testable.

## 3. Initial Persistence Strategy

To start quickly and avoid external dependencies, we will use a simple file-based persistence mechanism.

- **Strategy:** We will implement repositories that serialize aggregates to and from JSON files.
- **Location:** This implementation will live in the `infrastructure` layer, completely separate from the domain model. This allows us to easily swap it for SQLite or another database later without changing any business logic.

## 4. Handling Business Rules: Commands vs. Events

It is critical to distinguish between validating a command and conditionally handling an event.

### 4.1. Command Validation (Pre-Condition Checks)

A **Command** is a request to perform an action (e.g., "create a new player"). Business rules that must be satisfied *before* an action can occur are validated at the beginning of an Application Service method.

**Example:** "A player cannot be created until Tutorial Mission X is complete." This check should happen inside the `PlayerService`. If the condition is not met, the service should reject the command (e.g., by raising an exception), and no `PlayerCreated` event will ever be generated.

### 4.2. Sagas (Future Pattern)

For complex, long-running processes that involve multiple events over time (e.g., waiting for `ContractAccepted` and then `DataExtracted` before paying the player), we will use the **Saga** pattern.

A Saga is a stateful component that listens for a sequence of events and can dispatch new commands in response. This is a more advanced pattern that we will implement when a clear use case arises.

## 5. Discovering the Domain: Event Storming

To effectively explore and model the game's complex rules, we will use **Event Storming**. It's important to note that this is not a software component, but a collaborative workshop process designed to create a shared understanding of the domain.

### How It Helps This Project

-   **Answers Design Questions:** It provides a structured way to answer the open questions in our [roadmap](./roadmap.md), such as defining the core gameplay loop and player progression.
-   **Validates the Domain Model:** By mapping out game scenarios, we can validate that our Aggregates (`Player`, `Contract`, etc.) are correctly defined and that their boundaries make sense.
-   **Creates a Blueprint for Code:** The output of an Event Storming session directly translates into our architecture:
    -   **Domain Events** (orange notes) become our event classes.
    -   **Commands** (blue notes) become methods on our Application Services.
    -   **Aggregates** (yellow notes) become our Aggregate Root classes.
    -   **Policies** (purple notes) become our event handlers or Sagas.

By using this process, we ensure our code is a direct reflection of the game's domain logic.

## 6. Event Sourcing (Future Goal)

Our event-driven architecture provides the foundation for a powerful pattern called **Event Sourcing**. While not fully implemented yet, it is a guiding principle for our design.

Instead of storing the *current state* of our aggregates, Event Sourcing involves persisting the full, chronological log of domain events that have occurred. The current state is then derived by replaying these events.

For a detailed explanation of this concept and how our current features relate to it, see the Event Sourcing Guide.

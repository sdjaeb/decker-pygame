# DDD Concepts in Our Codebase

This document provides an overview of the core Domain-Driven Design (DDD) concepts we use and maps them to their specific implementations in this project. It complements the `ddd_implementation_guide.md` by providing a "who's who" of our architecture.

## 1. Ubiquitous Language

This is the shared, common language we use to talk about the game's domain. It appears in our conversations, documentation, and, most importantly, our code.

- **Concept:** `Player`, `Health`, `Alert Level`
- **Implementation:** `Player` class, `health` attribute, etc.

---

## 2. Layered Architecture

Our codebase is separated into distinct layers, each with a specific responsibility. Dependencies only point inwards, from Presentation to Application to Domain.

### Domain Layer

The heart of the application. Contains all core game rules and logic, with zero dependencies on frameworks like Pygame or implementation details like JSON.

- **Aggregates & Entities:** `domain/model.py` (`Player` class)
- **Domain Events:** `domain/events.py` (`PlayerCreated` class)
- **Repository Interfaces:** `domain/repositories.py` (`PlayerRepository` abstract class)

### Application Layer

Orchestrates the domain layer to perform specific use cases. It acts as a bridge between the UI and the core domain.

- **Application Services:** `application/services.py` (`PlayerService` class)

### Infrastructure Layer

Provides the technical implementation for the interfaces defined in the domain layer.

- **Concrete Repositories:** `infrastructure/persistence.py` (`JsonFilePlayerRepository` class)

### Presentation Layer

The user-facing part of the application. It's responsible for rendering the game and handling user input.

- **Game Loop & UI:** `presentation/game.py` (`Game` class), `presentation/components/`
- **Composition Root:** `presentation/main.py`

---

## 3. Key DDD Building Blocks

### Aggregate

A cluster of domain objects that are treated as a single unit for data changes. The entry point is the **Aggregate Root**.

- **Concept:** The `Player` is the central figure for many game actions. Its state (health, inventory, etc.) must be managed consistently.
- **Implementation:** The `Player` class in `domain/model.py` is our first Aggregate Root. All changes to a player's state should go through methods on this class.

### Entity

An object with a distinct, continuous identity. Two entities are not the same just because their attributes are identical.

- **Concept:** A `Player` is an entity. Even if two players have the same name and health, they are different individuals.
- **Implementation:** The `Player` class has a unique `id` of type `PlayerId` to distinguish it from all others.

### Value Object

An object defined by its attributes, not its identity. Two value objects are the same if their attributes are the same. They are typically immutable.

- **Concept:** A specific amount of money, a coordinate on a map, or a color.
- **Implementation:** `PlayerId` in `domain/model.py` is a simple form of a Value Object. It wraps a `UUID` to give it specific domain meaning.

### Repository

Mediates between the domain and the persistence mechanism, providing an in-memory collection-like interface for accessing domain objects.

- **Concept:** We need a way to "get a player" or "save a player" without the domain knowing about files or databases.
- **Implementation:**
    - **Interface (Domain Layer):** The `PlayerRepository` abstract class in `domain/repositories.py` defines the contract (e.g., `get`, `save`).
    - **Implementation (Infrastructure Layer):** The `JsonFilePlayerRepository` in `infrastructure/persistence.py` provides the concrete logic to save a `Player` to a JSON file.

### Application Service

A stateless service that executes a use case by orchestrating domain objects. It does not contain business logic itself.

- **Concept:** A use case like "Create a New Player".
- **Implementation:** The `PlayerService` in `application/services.py` contains the `create_new_player` method. It gets a new ID, calls the `Player.create` factory, and uses the repository to save the result.

### Domain Event

An object that represents something that happened in the domain that other parts of the system might care about.

- **Concept:** When a player is created, we might want to log it, show a UI notification, or trigger another process.
- **Implementation:** The `PlayerCreated` class in `domain/events.py`. The `Player.create` factory method creates and stores this event when a new player is made.

### Composition Root

The single place in the application where all the layers and components are wired together.

- **Concept:** We need one place to create the repository, inject it into the service, and inject the service into the game.
- **Implementation:** The `main()` function in `presentation/main.py` serves as our Composition Root.

---

## 4. Event-Driven Flow (The "Publish-Subscribe" Pattern)

Our architecture uses domain events to decouple different parts of the system. This allows components to react to changes without being directly called.

The flow is as follows:
1.  **Aggregate creates an event:** A method on an Aggregate Root (e.g., `Player.create`) performs a state change and creates a corresponding event object (e.g., `PlayerCreated`). It adds this event to an internal list.
2.  **Application Service saves the state:** The Application Service (e.g., `PlayerService`) calls the repository to persist the Aggregate's new state. This is a single, atomic transaction.
3.  **Application Service dispatches events:** *After* the state has been successfully saved, the Application Service retrieves the list of events from the Aggregate and passes them to an Event Dispatcher.
4.  **Event Dispatcher notifies subscribers:** The dispatcher (an infrastructure component) sends each event to any registered "subscribers" or "handlers" that are interested in that specific type of event. These handlers can then perform side effects, like updating a read model, sending an email, or logging.

- **Implementation Details:**
    - **Event Creation:** `Player.create()` in `domain/model.py`.
    - **Event Dispatch (Future):** The `PlayerService` will be responsible for dispatching events after saving. The dispatcher itself will be an infrastructure component we build later.

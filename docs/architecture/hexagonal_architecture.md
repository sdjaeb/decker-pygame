# Hexagonal Architecture (Ports & Adapters)

This document describes how we apply the principles of Hexagonal Architecture (also known as the "Ports and Adapters" pattern) to the `decker-pygame` project. This architectural style complements our Domain-Driven Design (DDD) approach by providing a clear structure for separating the core application logic from external concerns like the UI, databases, or other APIs.

## 1. The Core Application

The "hexagon" at the center of our architecture contains the pure, unadulterated logic of our application. It has no knowledge of how it is being used or what technologies are used to persist its data.

-   **Domain Layer (`src/decker_pygame/domain`):** This is the innermost part of the core. It contains our Aggregates (`Character`, `Player`), domain events, and repository interfaces. It is pure business logic.
-   **Application Layer (`src/decker_pygame/application`):** This layer surrounds the domain. It contains our Application Services (`CharacterService`, `CraftingService`) which orchestrate the domain objects to execute specific use cases (e.g., `increase_skill`).

The Core is completely independent and can be tested without any UI or database.

## 2. Ports

Ports are the interfaces that define how the Core communicates with the outside world. They are part of the Core but are defined from the Core's point of view. A port is an API that the Core *needs* to function.

We have two main types of ports:

### 2.1. Driving Ports (Input)

These define how external actors can drive the application. In our architecture, the public methods of our **Application Services** serve as our driving ports.

**Example:** The `CharacterService` exposes the `increase_skill(character_id, skill_name)` method. This is a port that the UI (an adapter) can use to command the application to perform an action.

```python
# src/decker_pygame/application/character_service.py

class CharacterService:
    def increase_skill(self, character_id: CharacterId, skill_name: str) -> None:
        # ... implementation
```

### 2.2. Driven Ports (Output)

These define what the Core needs from the outside world, typically for data persistence or other infrastructure tasks. In our architecture, the **Repository Interfaces** are our driven ports.

**Example:** The `CharacterRepositoryInterface` defines the contract that the Core needs for storing and retrieving `Character` aggregates. The Core doesn't know or care *how* they are stored (JSON, SQL, etc.), only that this contract is fulfilled.

```python
# src/decker_pygame/domain/character_repository_interface.py

class CharacterRepositoryInterface(ABC):
    @abstractmethod
    def save(self, character: "Character") -> None:
        # ...
```

## 3. Adapters

Adapters are the components that live outside the Core. They connect the Core's ports to the specific technologies we are using.

### 3.1. Driving Adapters

These are the components that call into the Core's driving ports.

-   **UI Components (`src/decker_pygame/presentation`):** Our Pygame components, like `CharDataView`, are driving adapters. When a user clicks a `+` button, the view's callback calls the `character_service.increase_skill(...)` method, thus "driving" the application.

### 3.2. Driven Adapters

These are the concrete implementations of the Core's driven ports.

-   **Infrastructure (`src/decker_pygame/infrastructure`):** Our `JsonFileCharacterRepository` is a driven adapter. It implements the `CharacterRepositoryInterface` port, translating the Core's request to save a character into the specific action of writing a JSON file to disk.

## 4. Future Improvements
## 4. Explicit Ports and Adapters

To make our architecture even more robust and self-documenting, we have made the roles of Ports and Adapters more explicit.

### 4.1. Explicit Port Modules

All port interfaces, both driving and driven, are now located in a dedicated `src/decker_pygame/ports` directory.

-   **Driving Port Interfaces (`ports/service_interfaces.py`):** These are abstract base classes (e.g., `CharacterServiceInterface`) that define the use cases the application offers. The Application Services in `src/decker_pygame/application` provide the concrete implementations of these interfaces.

-   **Driven Port Interfaces (`ports/repository_interfaces.py`):** These are the abstract base classes for our repositories (e.g., `CharacterRepositoryInterface`). They define the persistence contract required by the Core.

This explicit separation makes it immediately clear what the application's boundaries are.

### 4.2. Decoupled Presentation Logic

The `Game` class delegates the task of interpreting user input to a dedicated **Presentation Adapter** (e.g., `PygameEventHandler`). This adapter's sole responsibility is to translate raw Pygame events (like key presses) into calls to the appropriate methods on our Application Services (our driving ports). This further decouples the UI from the core application logic.

### 4.3. External API Adapters

When we need to communicate with external services (e.g., a high-score server), we follow a standard pattern:

1.  Define a new driven port in `src/decker_pygame/ports` (e.g., `HighScoreServiceInterface`).
2.  Create a corresponding adapter in the `infrastructure` layer (e.g., `ApiHighScoreService`) that implements this interface and handles the actual HTTP communication.
3.  Inject this adapter into the relevant Application Service.

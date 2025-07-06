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

While our current structure aligns well with Hexagonal Architecture, we can make it even more explicit and robust:

-   **Explicit Port Modules:** We could create a dedicated `src/decker_pygame/ports` directory to make the separation even clearer, though the current placement within the `domain` (for repository interfaces) and `application` (for service methods) layers is also a valid and common approach.

-   **Decouple Presentation Logic:** The `Game` class currently contains a mix of game loop management and UI event handling. In the future, we could introduce a more formal "Presentation Adapter" that is solely responsible for translating Pygame events into calls to our application services, further decoupling the UI from the core game state.

-   **External API Adapters:** When we need to communicate with external services (e.g., a high-score server), we would create a new port in the Core (e.g., `HighScoreServiceInterface`) and a corresponding adapter in the `infrastructure` layer that handles the HTTP requests.

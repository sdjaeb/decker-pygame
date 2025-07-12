# Hexagonal Architecture (Ports & Adapters)

This document describes how we apply the principles of Hexagonal Architecture (also known as the "Ports and Adapters" pattern) to the `decker-pygame` project. This architectural style complements our Domain-Driven Design (DDD) approach by providing a clear structure for separating the core application logic from external concerns like the UI, databases, or other APIs.

## 1. The Core Application

The "hexagon" at the center of our architecture contains the pure, unadulterated logic of our application. It has no knowledge of how it is being used or what technologies are used to persist its data.

-   **Domain Layer (`src/decker_pygame/domain`):** This is the innermost part of the core. It contains our Aggregates (`Character`, `Player`) and domain events. It is pure business logic.
-   **Application Layer (`src/decker_pygame/application`):** This layer surrounds the domain. It contains our Application Services (`CharacterService`, `CraftingService`) which orchestrate the domain objects to execute specific use cases (e.g., `increase_skill`).

The Core is completely independent and can be tested without any UI or database.

## 2. Ports

Ports are the interfaces that define how the Core communicates with the outside world. They are part of the Core but are defined from the Core's point of view. A port is an API that the Core *needs* to function.

All port interfaces are explicitly defined in the `src/decker_pygame/ports` directory.
We have two main types of ports:

### 2.1. Driving Ports (Input)

These define how external actors can drive the application. In our architecture, the **Service Interfaces** are our driving ports.

**Example:** The `CharacterServiceInterface` in `ports/service_interfaces.py` defines the contract for character-related use cases, such as `increase_skill(...)` and `get_character_view_data(...)`.

```python
# src/decker_pygame/ports/service_interfaces.py

class CharacterServiceInterface(ABC):
    @abstractmethod
    def increase_skill(self, character_id: "CharacterId", skill_name: str) -> None:
        ...
```

### 2.2. Driven Ports (Output)

These define what the Core needs from the outside world, typically for data persistence or other infrastructure tasks. In our architecture, the **Repository Interfaces** are our driven ports.

**Example**: The `CharacterRepositoryInterface` in `ports/repository_interfaces.py` defines the contract that the Core needs for storing and retrieving `Character` aggregates. The Core doesn't know or care how they are stored (JSON, SQL, etc.), only that this contract is fulfilled.

```python
# src/decker_pygame/ports/repository_interfaces.py

class CharacterRepositoryInterface(ABC):
    @abstractmethod
    def save(self, character: "Character") -> None:
        ...
```

## 3. Adapters

Adapters are the components that live outside the Core. They connect the Core's ports to the specific technologies we are using.

### 3.1. Driving Adapters

These are the components that call into the Core's driving ports.

-   **Input Handler (`src/decker_pygame/presentation/input_handler.py`):** The `PygameInputHandler` is a dedicated driving adapter. Its sole responsibility is to translate raw Pygame events (like key presses) into calls to methods on the `Game` object.
-   **UI Components (`src/decker_pygame/presentation/components`):** Our Pygame components, like `CharDataView`, are also driving adapters. When a user clicks a `+` button, the view's callback calls a method on the `Game` class, which in turn calls the appropriate Application Service (e.g., `character_service.increase_skill(...)`).

### 3.2. Driven Adapters

These are the concrete implementations of the Core's driven ports.

-   **Infrastructure (`src/decker_pygame/infrastructure`):** Our `JsonFileCharacterRepository` is a driven adapter. It implements the `CharacterRepositoryInterface` port, translating the Core's request to save a character into the specific action of writing a JSON file to disk.


## 4. Data Flow and View Models

To maintain a clean boundary between the application and presentation layers, we use dedicated **View Model DTOs**.

**Example:** The `CharacterService` provides a `get_character_view_data()` method. This method is a query that assembles a `CharacterViewData` DTO, which contains all the specific fields required by the `CharDataView` component. This prevents the presentation layer from needing to make multiple service calls and assemble data itself, keeping it "dumb" and focused on rendering.

```python
# src/decker_pygame/application/character_service.py

@dataclass(frozen=True)
class CharacterViewData:
    name: str
    credits: int
    reputation: int
    skills: dict[str, int]
    unused_skill_points: int
    health: int
```

## 5. External API Adapters (Future)

When we need to communicate with external services (e.g., a high-score server), we follow a standard pattern:

1.  Define a new driven port in `src/decker_pygame/ports` (e.g., `HighScoreServiceInterface`).
2.  Create a corresponding adapter in the `infrastructure` layer (e.g., `ApiHighScoreService`) that implements this interface and handles the actual HTTP communication.
3.  Inject this adapter into the relevant Application Service.

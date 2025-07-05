# Architectural Roadmap

This document outlines major architectural enhancements planned for the future. These items are critical for building a more robust, scalable, and maintainable system.

## 1. Transition to Full Event Sourcing

Our current system is event-driven but uses state-oriented persistence. The goal is to transition to a full event-sourcing model where the event log is the single source of truth.

**Tasks:**
-   **Create an Event Store:**
    -   Define an `EventRepositoryInterface` in the `domain` layer.
    -   Implement a `JsonEventRepository` in the `infrastructure` layer that appends events to a log file for each aggregate.
-   **Refactor Aggregates for Replay:**
    -   Add a `replay(events: list[Event])` class method to `AggregateRoot`.
    -   Implement private `_apply(event: Event)` methods within each aggregate (e.g., `_apply_player_created`) to handle state changes.
    -   Remove the `from_dict` methods in favor of replaying events.
-   **Update Application Services:**
    -   Modify services to fetch event streams from the `EventRepository`, replay them to get the current aggregate state, and then append new events.

## 2. Implement the Saga Pattern for Process Management

For long-running business processes that involve multiple aggregates or events over time, we will implement the Saga pattern.

**Tasks:**
-   **Design a Saga Base Class:** Create a `Saga` or `ProcessManager` base class in the `application` layer. It will be stateful and capable of listening for events and dispatching commands.
-   **Implement Saga Persistence:** Define a `SagaRepositoryInterface` and a corresponding `JsonSagaRepository` to save and load the state of active Sagas.
-   **Identify and Implement a Pilot Saga:** Choose a suitable first use case (e.g., a multi-step contract requiring data extraction and then a separate payout) and implement the concrete Saga, its event handlers, and the commands it dispatches.

---

## 3. Open Questions & Next Steps

This section raises key questions to guide our next phase of development, spanning both technical architecture and game design.

### Architectural Questions

-   **Read Models / Projections:** How will the UI get the data it needs to render? Should it query the domain aggregates directly (via services), or should we create separate, optimized read models (projections) that are updated by event handlers? The latter is more scalable but adds complexity.
-   **Command Handling:** Should we formalize the concept of a "Command" (e.g., `CreatePlayerCommand`) and a `CommandBus`? This would make the application's capabilities more explicit than the current service-method approach.
-   **Configuration Management:** As the game grows, how will we manage complex configurations like item stats, contract details, and node layouts? Should these be loaded from static data files (JSON, YAML) into dedicated configuration objects at startup?

### Game Design Questions

-   **Core Gameplay Loop:** What is the central, repeatable loop for the player? Is it simply accepting contracts, executing them, and upgrading gear, or are there other major activities like exploration, story progression, or sandbox-style hacking?
-   **Player Progression:** How does a player "get stronger"? Is it purely through earning credits to buy better programs, or will there be a skill system, experience points, or a reputation mechanic that unlocks new opportunities?
-   **Economy Balancing:** What is the economic baseline for the game? We need to define the initial costs of programs, the rewards for different types of contracts, and the general flow of credits to ensure a balanced and engaging difficulty curve.

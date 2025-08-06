# Event Sourcing in Decker-Pygame

This document provides a detailed overview of the Event Sourcing (ES) pattern and clarifies how our current architecture is designed to support it as a future goal.

## 1. What is Event Sourcing?

**Event Sourcing** is an architectural pattern where all changes to an application's state are stored as a sequence of immutable, time-ordered **events**. Instead of persisting the *current state* of an entity, we persist the full history of events that have ever happened to it.

The event log becomes the single, append-only source of truth. The current state of an entity is a **projection** that can be rebuilt at any time by replaying its events from the beginning.

**Example: A Player's Health**

-   **State-Oriented Persistence (What we do now):** A database or file stores `player.health = 80`. If the player takes 10 more damage, we update that value to `70`. The previous value of 80 is lost.
-   **Event Sourcing (Our future goal):** The event log stores:
    1.  `PlayerCreated(initial_health=100)`
    2.  `PlayerTookDamage(amount=20)`
    3.  `PlayerTookDamage(amount=10)`

The player's current health (70) is calculated by applying these events in order. We have a complete, auditable history of how the state was reached.

## 2. Our Path to Event Sourcing

Our current system is **event-driven**, which is the necessary foundation for being **event-sourced**.

#### What We Have (The Foundation)

-   **Immutable Domain Events:** Classes like `PlayerCreated` are perfect, factual records of things that have successfully occurred.
-   **Aggregates as Event Producers:** Our Aggregate Roots (`Player`, `Character`, `Project`) are responsible for creating valid events when their state changes.
-   **Event Dispatcher:** We have a mechanism to publish these events to the rest of the application.

#### The Missing Pieces

-   **The Event Store:** We are currently missing a repository that persists the *events themselves*. Our `JsonFilePlayerRepository` saves a snapshot of the current state. A true `EventRepository` would append events to a log.
-   **State Reconstruction from Events:** Our aggregates are currently reconstituted from a state snapshot (`from_dict`). A full ES implementation would require a method like `Player.replay(events)` that builds the object's state by applying each event in sequence.

## 3. How Our New Features Contribute

-   **`@emits` and `@handles` Decorators:** These decorators make the event flow explicit. In an ES system, this is vital for tracing how state is built and how side-effects (projections) are triggered. They are signposts in the event stream.

-   **Conditional Handlers:** These are tools for building sophisticated **consumers** of the event stream. While not part of the "sourcing" itself, they are essential for building the read models and other projections that make an ES system useful. For example, a conditional handler could maintain a UI-specific view model (a projection) of a player's status.

-   **Command Validation:** The strict separation of command validation (in the `PlayerService`) from event creation is the gatekeeper for the event store. It guarantees that only valid, consistent events are ever persisted, ensuring the integrity of our source of truth.

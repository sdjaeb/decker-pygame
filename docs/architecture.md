# Architecture Overview

This document provides a high-level entry point to the architecture of the Decker-Pygame project. For detailed information on specific patterns, please refer to the documents linked below.

## Project Structure

The project follows a **Layered Architecture** inspired by Domain-Driven Design and structured according to the principles of Hexagonal Architecture. The source code is organized into four distinct layers within the `src/decker_pygame` directory:

-   `src/decker_pygame/`: The main source code for the game.
    -   `domain/`: The core of the application. Contains the business logic, rules, and state (Aggregates, Entities, Domain Events). It has zero dependencies on other layers.
    -   `application/`: Orchestrates domain objects to execute use cases (Application Services).
    -   `infrastructure/`: Implements technical details for interfaces defined in the inner layers (e.g., file-based repositories).
    -   `presentation/`: The user-facing part of the application (Pygame game loop, UI components, input handling).
-   `tests/`: Contains the `pytest` test suite, mirroring the structure of the `src` directory.
-   `assets/`: Contains all game assets, organized by type.
-   `docs/`: Project documentation, including this file.
    -   `architecture/`: Contains detailed documents on our specific architectural patterns.

## Core Architectural Principles

The goal of this project is to create a modern, maintainable, and Pythonic port of the original Decker game. We achieve this by adhering to several key architectural principles:

-   **Domain-Driven Design (DDD):** We focus on the core domain logic of the game, modeling it with concepts like Aggregates and Domain Events. This ensures the business rules are explicit and isolated.
-   **Hexagonal Architecture (Ports & Adapters):** This structure protects the core domain from external concerns. The UI and persistence layers are "adapters" that plug into the application's "ports" (interfaces), making them swappable.
-   **Event-Driven Architecture:** We use domain events to decouple components and communicate state changes. This creates a more flexible and reactive system, and lays the groundwork for future patterns like Event Sourcing.

For a deeper dive into these concepts and their implementation in our codebase, please see the following documents:

-   [Implementation Guidelines](./architecture/ddd_implementation_guide.md)
-   [DDD Concepts in Our Codebase](./architecture/ddd_concepts.md)
-   [Hexagonal Architecture](./architecture/hexagonal_architecture.md)
-   [Event Sourcing](./architecture/event_sourcing.md)

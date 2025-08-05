# Project Roadmap

This document outlines the major features and architectural enhancements planned for the project.

## 1. Core Gameplay Implementation

With the core architecture now stable, the primary focus is on implementing the gameplay features that make the game playable.

**Tasks:**
-   **Implement the Contract Loop:**
    -   Make the `ContractListView` functional, allowing players to select from available contracts fetched via the `ContractService`.
    -   Implement the "Accept Contract" flow, which will likely transition the game to a new "Matrix Run" state or view.
    -   Define and implement the `MatrixRunView`, which will be the core hacking interface.
-   **Externalize Game Data:**
    -   Move hardcoded data (like initial schematics and contracts) from `main.py` into external JSON or YAML files.
    -   Implement data loaders in the composition root to populate repositories at startup.
-   **Player Progression:**
    -   Flesh out the skill and credit systems.
    -   Implement the "Upgrade Lifestyle" feature.
    -   Design and implement hardware chips and crafting components. (R&D system complete).
    -   Balance the in-game economy (contract rewards vs. item costs).

## 2. Future Architectural Enhancements

These are long-term goals to be considered once the core gameplay is more mature.

**Tasks:**
----
-   **Transition to Full Event Sourcing:** Our current system is event-driven, which is the perfect foundation. A full transition would involve implementing an Event Store and replaying events to constitute aggregates.
-   **Implement the Saga Pattern:** For complex, long-running processes that involve multiple events over time (e.g., a multi-step contract), the Saga pattern will be invaluable.
-   **Formalize a Command Bus:** For even stricter separation, we could introduce a formal Command/Command Bus pattern instead of direct service method calls.

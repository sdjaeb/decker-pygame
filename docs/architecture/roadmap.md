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
    -   **Action:** Move all hardcoded game data (e.g., initial character data, schematics, shop items) from the presentation layer (`main.py`) into external JSON files within a new `data/` directory.
    -   **Tasks:**
        -   Create `data/initial_character.json` to define the player's starting state.
        -   Create `data/schematics.json` to define all researchable items.
        -   Create `data/shop_inventory.json` to define items available in shops.
        -   Create `data/contracts.json` to define the pool of available contracts.
        -   Implement corresponding `JsonFile...Repository` classes in the `infrastructure` layer to load this data.
        -   Update the composition root in `main.py` to use these new data-driven repositories, removing all hardcoded data setup.
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

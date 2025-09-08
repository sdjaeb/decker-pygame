# Project Roadmap

This document outlines the major features and architectural enhancements planned for the project.

## 1. Core Gameplay Implementation

With the core architecture now stable, the primary focus is on implementing the gameplay features that make the game playable.

**Tasks:**
-   **Implement the Contract Loop:**
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

---

## Contract Loop Implementation Plan

This section details the step-by-step plan to implement the core gameplay loop, where a player accepts a contract and performs a matrix run.

### Phase 1: Accepting a Contract (Presentation Layer)

1.  **Make `ContractListView` Interactive:**
    -   The `on_contract_selected` callback currently opens a placeholder `ContractDataView`.
    -   **Action:** Modify this callback to pass the selected `ContractSummaryDTO` to the `ContractDataView`.
2.  **Enhance `ContractDataView`:**
    -   Add an "Accept" button to the view.
    -   The view will display detailed information about the selected contract.
3.  **Implement the "Accept Contract" Flow:**
    -   Create a new method in `HomeState`, `_on_accept_contract(contract_id: ContractId)`.
    -   This method will call a new application service method, `contract_service.accept_contract(character_id, contract_id)`.
    -   Upon successful acceptance, it will call `game.set_state(GameState.MATRIX_RUN)` to transition the game.

### Phase 2: Initiating the Matrix Run (Application & Domain Layers)

1.  **Update `ContractService`:**
    -   Create the `accept_contract` method. This will associate the contract with the character, marking it as "in-progress".
2.  **Update `MatrixRunService`:**
    -   Create a `start_new_run(character_id, contract_id)` method.
    -   This method will be responsible for:
        -   Looking up the contract to find the target `SystemId`.
        -   Loading the `System` (now `Host`) from the `SystemRepository`.
        -   Initializing the `MatrixRun` aggregate with the system data, player's deck, and character stats.
        -   Saving the new `MatrixRun` aggregate.
3.  **Enhance `MatrixRunState`:**
    -   The `on_enter` method for `MatrixRunState` will be modified to call `matrix_run_service.start_new_run(...)`.

### Phase 3: Core Hacking Gameplay (Full Stack)

This is the most complex phase and will be broken down further.

1.  **Player Interaction:**
    -   Implement clicking on nodes in the `NodeGridView`.
    -   This will trigger commands like `matrix_run_service.move_to_node(node_id)` or `matrix_run_service.use_program_on_node(program_id, node_id)`.
2.  **ICE Interaction:**
    -   Implement the combat loop within the `MatrixRun` aggregate.
    -   The `use_program_on_node` command will trigger domain logic where the player's software interacts with the system's ICE.
    -   This will involve using the `DiceService` for skill checks and combat resolution.
3.  **Run Completion:**
    -   Define win/loss conditions (e.g., extracting a file, getting disconnected).
    -   Create a `matrix_run_service.end_run()` method that calculates rewards (credits, reputation) and penalties.
    -   This will emit a `MatrixRunCompleted` event.
    -   The `Game` will listen for this event and transition to the `MissionResultsView`.

## 2. Future Architectural Enhancements

These are long-term goals to be considered once the core gameplay is more mature.

**Tasks:**
----
-   **Transition to Full Event Sourcing:** Our current system is event-driven, which is the perfect foundation. A full transition would involve implementing an Event Store and replaying events to constitute aggregates.
-   **Implement the Saga Pattern:** For complex, long-running processes that involve multiple events over time (e.g., a multi-step contract), the Saga pattern will be invaluable.
-   **Formalize a Command Bus:** For even stricter separation, we could introduce a formal Command/Command Bus pattern instead of direct service method calls.

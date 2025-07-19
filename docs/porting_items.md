# Decker Source File Audit & Porting Priorities

## TL;DR: File Grouping and Porting Priority

| Group                        | Files (examples)                                                                 | Importance | Status      | Notes                                                                                             |
|------------------------------|----------------------------------------------------------------------------------|------------|-------------|---------------------------------------------------------------------------------------------------|
| **Core Data Models / Logic** | Area, Character, Contract, Ice, Node, Program, Shop, ShopItem, Source, System, Global | 1 (Highest) | In Progress | Ported into the `domain`, `application`, and `infrastructure` layers of our DDD architecture. |
| **UI Components / Widgets**  | ActiveBar, AlarmBar, ClockView, CustomButton, HealthBar, ImageArray, MapView, etc. | 2          | To Do       |
| **Dialogs / Screens**        | BuildDialog, CharDataDialog, ContractDataDialog, DeckDataDialog, EntryDlg, etc.  | 3          | To Do       |
| **Main Application / Engine**| Decker, DeckerGraphics, DeckerSound, DSFile, StdAfx                             | 1          | In Progress |
| **Utility / Support**        | Global                                                                           | 2-3        | In Progress |

---

## Detailed Breakdown

### 1. Core Data Models / Game Logic (**Highest Importance**) - Ported to DDD
These files define the fundamental data structures and logic for the game. They are the backbone of the application and should be ported first, as most other components depend on them.

- **Area.cpp/h**: Represents locations or regions in the game. (`Ported`)
- **Character.cpp/h**: Player and NPC data, stats, inventory, etc. (`Ported`)
- **Contract.cpp/h**: Missions or jobs available to the player. (`Ported`)
- **Ice.cpp/h**: Security programs (Intrusion Countermeasures Electronics). (`Ported`)
- **Node.cpp/h**: Network nodes or locations. (`Ported`)
- **Program.cpp/h**: Hacking programs/tools. (`Ported`)
- **Shop.cpp/h**: In-game shops. (`Ported`)
- **ShopItem.cpp/h**: Items available for purchase. (`Ported`)
- **Source.cpp/h**: Likely represents data sources or lootable objects. (`Ported`)
- **System.cpp/h**: Underlying system logic or world state. (`Ported`)
- **Global.cpp/h**: Global variables, constants, or helpers. (`Partially Ported to utils.py`)

**Porting Status:** Largely Complete.

**Architectural Notes:** The logic from these core C++ files has been refactored into our new Domain-Driven Design architecture.
- **Core rules and state** (e.g., `Player` data) are now **Aggregates** in `src/decker_pygame/domain/model.py`.
- **Use cases** (e.g., creating a character) are handled by **Application Services** in `src/decker_pygame/application/services.py`.
- **Persistence** (saving/loading) is managed by **Repositories** defined in `src/decker_pygame/domain/repositories.py` and implemented in `src/decker_pygame/infrastructure/persistence.py`.
- This separation ensures our core game logic is independent of UI or data storage details.

---

### 2. UI Components / Widgets (**High Importance**)
Reusable interface elements that are used across multiple screens or dialogs. Port these after the core models, as they are needed to build the UI.

- **ActiveBar.cpp/h** (`Ported`)
- **AlarmBar.cpp/h** (`Ported`)
- **ClockView.cpp/h** (`Ported`)
- **CustomButton.cpp/h** (`Ported`)
- **HealthBar.cpp/h** (`Ported`)
- **ImageArray.cpp/h** (`Ported`)
- **ImageDisplay.cpp/h** (`Ported`)
- **MapView.cpp/h** (`Ported`)
- **MatrixView.cpp/h** (`Ported`)
- **MessageView.cpp/h** (`Ported`)
- **NameBar.cpp/h** (`Ported`)
- **NodeView.cpp/h** (`Ported`)

**Porting Priority:** 2

---

### 3. Dialogs / Screens (**Medium Importance**)
Modal dialogs and main screens for editing/viewing specific data. These depend on both the data models and UI components.

- **BuildDialog.cpp/h** (`Ported as BuildView`)
- **CharDataDialog.cpp/h** (`Ported as CharDataView`)
- **ContractDataDialog.cpp/h** (`Ported as ContractDataView`)
- **ContractListDialog.cpp/h** (`Ported as ContractListView`)
- **DeckDataDialog.cpp/h** (`Ported as DeckView`)
- **EntryDlg.cpp/h**
- **FileAccessDlg.cpp/h**
- **HomeView.cpp/h** (`Ported as HomeView`)
- **IceDataDlg.cpp/h**
- **IntroDlg.cpp/h** (`Ported as IntroView`)
- **MissionResultsDlg.cpp/h**
- **NameDlg.cpp/h** (`Ported as TextInput component`)
- **NewCharDlg.cpp/h** (`Ported as NewCharView`)
- **NewProjectDlg.cpp/h**
- **OptionsDlg.cpp/h**
- **OrderDlg.cpp/h** (`Ported as OrderView`)
- **ProjectDataDlg.cpp/h**
- **RestDlg.cpp/h**
- **ShopItem.cpp/h**
- **SoundEditDlg.cpp/h**
- **TransferDlg.cpp/h** (`Ported as TransferView`)

**Porting Priority:** 3

#### Proposed Porting Groups for Remaining Dialogs

Based on an analysis of the remaining dialogs, we can group them by functionality to guide the next phase of porting. The status of each group will be updated as work progresses.

**Group A: Core Player Lifecycle (Status: Complete)**
These views are essential for starting a new game and providing a central hub for the player.
- **`HomeView.cpp/h`**: Port to `HomeView`. This will be the main player dashboard, with buttons to access Character data, Deck, Contracts, etc.
- **`NewCharDlg.cpp/h`**: Port to `NewCharView`. This view will handle the character creation process.
- **`NameDlg.cpp/h`**: Port to a reusable `NameInputView` or similar text input component, to be used by `NewCharView`.
- **`IntroDlg.cpp/h`**: Port to `IntroView`. A simple view to display the game's introduction.

**Group B: Core Gameplay Loop (Status: Complete)**
These views are part of the main contract/mission cycle.
- **`MissionResultsDlg.cpp/h`**: Port to `MissionResultsView`.
- **`RestDlg.cpp/h`**: Port to `RestView`.

**Group C: Data Display & Shop (Status: Complete)**
These views are for displaying information and handling commerce.
- **`ShopItem.cpp/h`**: Port to `ShopView` and `ShopItemView`. (Complete).
- **`IceDataDlg.cpp/h`**: Port to `IceDataView`. (Complete).

**Group D: In-Mission Interaction (Status: Complete)**
These views are likely used during the hacking/matrix part of the game.
- **`FileAccessDlg.cpp/h`**: Port to `FileAccessView`. (Complete).
- **`EntryDlg.cpp/h`**: Port to `EntryView` (e.g., for password prompts). (Complete).

**Group E: System & Configuration (Status: Complete)**
These are lower-priority views for game settings.
- **`OptionsDlg.cpp/h`**: Port to `OptionsView`. (Complete).
- **`SoundEditDlg.cpp/h`**: Port to `SoundEditView`. (Complete).

**Group F: "Project" Feature**
This feature needs further analysis.
- **`NewProjectDlg.cpp/h`**
- **`ProjectDataDlg.cpp/h`**

**Recommendation:**
The next step should be to implement **Group A**. This will establish a complete game startup flow: Intro -> New Character -> Home Dashboard.

---

### 4. Main Application / Engine (**Highest Importance**)
Top-level application logic, main loop, graphics, sound, and file handling. These are essential for the game to run and should be ported alongside the core models.

- **Decker.cpp/h**: Main application/game loop.
- **DeckerGraphics.cpp/h**: Graphics rendering.
- **DeckerSound.cpp/h**: Sound and music.
- **DSFile.cpp/h**: File I/O.
- **StdAfx.cpp/h**: Precompiled headers/support (may not be needed in Python).

**Porting Priority:** 1

---

### 5. Utility / Support (**Medium to Low Importance**)
General helpers, global state, or constants. Port as needed to support other modules.

- **Global.cpp/h**

**Porting Priority:** 2-3

---

## Recommendations

- **Start with Core Data Models and Main Application/Engine** (Priority 1).
- **Next, port UI Components/Widgets** (Priority 2).
- **Then, move to Dialogs/Screens and Utility/Support** (Priority 3).

This order ensures you have the foundational logic and structures in place before building out the UI

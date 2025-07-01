# Decker Source File Audit & Porting Priorities

## TL;DR: File Grouping and Porting Priority

| Group                        | Files (examples)                                                                 | Importance | Status      |
|------------------------------|----------------------------------------------------------------------------------|------------|-------------|
| **Core Data Models / Logic** | Area, Character, Contract, Ice, Node, Program, Shop, ShopItem, Source, System, Global | 1 (Highest) | In Progress |
| **UI Components / Widgets**  | ActiveBar, AlarmBar, ClockView, CustomButton, HealthBar, ImageArray, MapView, etc. | 2          | To Do       |
| **Dialogs / Screens**        | BuildDialog, CharDataDialog, ContractDataDialog, DeckDataDialog, EntryDlg, etc.  | 3          | To Do       |
| **Main Application / Engine**| Decker, DeckerGraphics, DeckerSound, DSFile, StdAfx                             | 1          | In Progress |
| **Utility / Support**        | Global                                                                           | 2-3        | In Progress |

---

## Detailed Breakdown

### 1. Core Data Models / Game Logic (**Highest Importance**)
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

**Porting Priority:** 1 (Highest) - **Largely Complete**

---

### 2. UI Components / Widgets (**High Importance**)
Reusable interface elements that are used across multiple screens or dialogs. Port these after the core models, as they are needed to build the UI.

- **ActiveBar.cpp/h**
- **AlarmBar.cpp/h**
- **ClockView.cpp/h**
- **CustomButton.cpp/h**
- **HealthBar.cpp/h**
- **ImageArray.cpp/h**
- **ImageDisplay.cpp/h**
- **MapView.cpp/h**
- **MatrixView.cpp/h**
- **MessageView.cpp/h**
- **NameBar.cpp/h**
- **NodeView.cpp/h**

**Porting Priority:** 2

---

### 3. Dialogs / Screens (**Medium Importance**)
Modal dialogs and main screens for editing/viewing specific data. These depend on both the data models and UI components.

- **BuildDialog.cpp/h**
- **CharDataDialog.cpp/h**
- **ContractDataDialog.cpp/h**
- **ContractListDialog.cpp/h**
- **DeckDataDialog.cpp/h**
- **EntryDlg.cpp/h**
- **FileAccessDlg.cpp/h**
- **HomeView.cpp/h**
- **IceDataDlg.cpp/h**
- **IntroDlg.cpp/h**
- **MissionResultsDlg.cpp/h**
- **NameDlg.cpp/h**
- **NewCharDlg.cpp/h**
- **NewProjectDlg.cpp/h**
- **OptionsDlg.cpp/h**
- **OrderDlg.cpp/h**
- **ProjectDataDlg.cpp/h**
- **RestDlg.cpp/h**
- **ShopItem.cpp/h**
- **SoundEditDlg.cpp/h**
- **TransferDlg.cpp/h**

**Porting Priority:** 3

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

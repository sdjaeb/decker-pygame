"""This module defines the main Game class, which orchestrates the presentation layer.

It handles the main game loop, event processing, and the display of all UI components.
"""

from collections.abc import Callable
from functools import partial
from typing import Optional, TypeVar, cast

import pygame

from decker_pygame.application.crafting_service import CraftingError
from decker_pygame.application.dtos import (
    EntryViewDTO,
    FileAccessViewDTO,
    IceDataViewDTO,
    MissionResultsDTO,
    NewProjectViewDTO,
    RestViewDTO,
    ShopItemViewDTO,
)
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.ports.service_interfaces import (
    CharacterServiceInterface,
    ContractServiceInterface,
    CraftingServiceInterface,
    DeckServiceInterface,
    DSFileServiceInterface,
    LoggingServiceInterface,
    MatrixRunServiceInterface,
    NodeServiceInterface,
    PlayerServiceInterface,
    ProjectServiceInterface,
    SettingsServiceInterface,
    ShopServiceInterface,
)
from decker_pygame.presentation.asset_service import AssetService
from decker_pygame.presentation.components.build_view import BuildView
from decker_pygame.presentation.components.char_data_view import CharDataView
from decker_pygame.presentation.components.contract_data_view import ContractDataView
from decker_pygame.presentation.components.contract_list_view import ContractListView
from decker_pygame.presentation.components.deck_view import DeckView
from decker_pygame.presentation.components.entry_view import EntryView
from decker_pygame.presentation.components.file_access_view import FileAccessView
from decker_pygame.presentation.components.home_view import HomeView
from decker_pygame.presentation.components.ice_data_view import IceDataView
from decker_pygame.presentation.components.intro_view import IntroView
from decker_pygame.presentation.components.matrix_run_view import (
    MatrixRunView,
)
from decker_pygame.presentation.components.message_view import MessageView
from decker_pygame.presentation.components.mission_results_view import (
    MissionResultsView,
)

# from decker_pygame.presentation.components.project_data_view import ProjectDataView
from decker_pygame.presentation.components.new_char_view import NewCharView
from decker_pygame.presentation.components.new_project_view import NewProjectView
from decker_pygame.presentation.components.options_view import OptionsView
from decker_pygame.presentation.components.order_view import OrderView
from decker_pygame.presentation.components.project_data_view import ProjectDataView
from decker_pygame.presentation.components.rest_view import RestView
from decker_pygame.presentation.components.shop_item_view import ShopItemView
from decker_pygame.presentation.components.shop_view import ShopView
from decker_pygame.presentation.components.sound_edit_view import (
    SoundEditView,
)
from decker_pygame.presentation.components.transfer_view import TransferView
from decker_pygame.presentation.debug_actions import DebugActions
from decker_pygame.presentation.input_handler import PygameInputHandler
from decker_pygame.presentation.protocols import Eventful
from decker_pygame.settings import BLACK, FPS, UI_FACE

V = TypeVar("V", bound=pygame.sprite.Sprite)


class Game:
    """Main game loop and presentation logic.

    Handles the main game loop, event processing, and the display of all UI
    components.

    Args:
        screen (pygame.Surface): The main display surface.
        asset_service (AssetService): The service for loading game assets.
        player_service (PlayerServiceInterface): Service for player operations.
        player_id (PlayerId): The ID of the current player.
        character_service (CharacterServiceInterface): Service for character ops.
        contract_service (ContractServiceInterface): Service for contract ops.
        crafting_service (CraftingServiceInterface): Service for crafting ops.
        deck_service (DeckServiceInterface): The service for deck operations.
        ds_file_service (DSFileServiceInterface): Service for DSFile operations.
        shop_service (ShopServiceInterface): The service for shop operations.
        node_service (NodeServiceInterface): The service for node operations.
        settings_service (SettingsServiceInterface): The service for game settings.
        project_service (ProjectServiceInterface): The service for R&D projects.
        matrix_run_service (MatrixRunServiceInterface): Service for matrix run ops.
        event_dispatcher (EventDispatcher): The dispatcher for domain events.
        character_id (CharacterId): The ID of the current character.
        logging_service (LoggingServiceInterface): Service for logging.

    Attributes:
        screen (pygame.Surface): The main display surface.
        clock (pygame.time.Clock): The game clock for managing FPS.
        is_running (bool): Flag to control the main game loop.
        all_sprites (pygame.sprite.Group[pygame.sprite.Sprite]): Group for all sprites.
        player_service (PlayerServiceInterface): Service for player operations.
        character_service (CharacterServiceInterface): Service for character operations.
        contract_service (ContractServiceInterface): Service for contract operations.
        crafting_service (CraftingServiceInterface): Service for crafting operations.
        ds_file_service (DSFileServiceInterface): Service for DSFile operations.
        deck_service (DeckServiceInterface): The service for deck operations.
        shop_service (ShopServiceInterface): The service for shop operations.
        node_service (NodeServiceInterface): The service for node operations.
        settings_service (SettingsServiceInterface): The service for game settings.
        project_service (ProjectServiceInterface): The service for R&D projects.
        matrix_run_service (MatrixRunServiceInterface): Service for matrix run ops.
        player_id (PlayerId): The ID of the current player.
        asset_service (AssetService): The service for loading game assets.
        character_id (CharacterId): The ID of the current character.
        logging_service (LoggingServiceInterface): Service for logging.
        message_view (MessageView): The UI component for displaying messages.
        input_handler (PygameInputHandler): The handler for user input.
        debug_actions (DebugActions): A container for debugging actions.
        intro_view (Optional[IntroView]): The introduction view, if open.
        new_char_view (Optional[NewCharView]): The new character view, if open.
        rest_view (Optional[RestView]): The rest and recovery view, if open.
        mission_results_view (Optional[MissionResultsView]): The mission results
            view.
        home_view (Optional[HomeView]): The main menu view, if open.
        build_view (Optional[BuildView]): The build view, if open.
        shop_item_view (Optional[ShopItemView]): The shop item view, if open.
        char_data_view (Optional[CharDataView]): The character data view, if open.
        deck_view (Optional[DeckView]): The deck view, if open.
        order_view (Optional[OrderView]): The deck ordering view, if open.
        transfer_view (Optional[TransferView]): The program transfer view, if open.
        shop_view (Optional[ShopView]): The shop view, if open.
        contract_list_view (Optional[ContractListView]): The contract list view,
            if open.
        contract_data_view (Optional[ContractDataView]): The contract data view,
            if open.
        ice_data_view (Optional[IceDataView]): The ICE data view, if open.
        file_access_view (Optional[FileAccessView]): The file access view, if open.
        entry_view (Optional[EntryView]): The text entry view, if open.
        options_view (Optional[OptionsView]): The game options view, if open.
        sound_edit_view (Optional[SoundEditView]): The sound edit view, if open.
        new_project_view (Optional[NewProjectView]): The new project view, if open.
        project_data_view (Optional[ProjectDataView]): The project data view, if open.
        matrix_run_view (Optional[MatrixRunView]): The main matrix run view,
            if open.
    """

    _modal_stack: list[Eventful]
    screen: pygame.Surface
    clock: pygame.time.Clock
    is_running: bool
    all_sprites: pygame.sprite.Group[pygame.sprite.Sprite]
    player_service: PlayerServiceInterface
    character_service: CharacterServiceInterface
    contract_service: ContractServiceInterface
    crafting_service: CraftingServiceInterface
    ds_file_service: DSFileServiceInterface
    deck_service: DeckServiceInterface
    shop_service: ShopServiceInterface
    node_service: NodeServiceInterface
    settings_service: SettingsServiceInterface
    project_service: ProjectServiceInterface
    matrix_run_service: MatrixRunServiceInterface
    player_id: PlayerId
    asset_service: AssetService
    character_id: CharacterId
    logging_service: LoggingServiceInterface
    message_view: MessageView
    input_handler: PygameInputHandler
    debug_actions: DebugActions
    intro_view: Optional[IntroView] = None
    new_char_view: Optional[NewCharView] = None
    rest_view: Optional[RestView] = None
    mission_results_view: Optional[MissionResultsView] = None
    home_view: Optional[HomeView] = None
    build_view: Optional[BuildView] = None
    shop_item_view: Optional[ShopItemView] = None
    char_data_view: Optional[CharDataView] = None
    deck_view: Optional[DeckView] = None
    order_view: Optional[OrderView] = None
    transfer_view: Optional[TransferView] = None
    shop_view: Optional[ShopView] = None
    contract_list_view: Optional[ContractListView] = None
    contract_data_view: Optional[ContractDataView] = None
    ice_data_view: Optional[IceDataView] = None
    file_access_view: Optional[FileAccessView] = None
    entry_view: Optional[EntryView] = None
    options_view: Optional[OptionsView] = None
    sound_edit_view: Optional[SoundEditView] = None
    new_project_view: Optional[NewProjectView] = None
    project_data_view: Optional[ProjectDataView] = None
    matrix_run_view: Optional[MatrixRunView] = None

    def __init__(
        self,
        screen: pygame.Surface,
        asset_service: AssetService,
        player_service: PlayerServiceInterface,
        player_id: PlayerId,
        character_service: CharacterServiceInterface,
        contract_service: ContractServiceInterface,
        crafting_service: CraftingServiceInterface,
        deck_service: DeckServiceInterface,
        ds_file_service: DSFileServiceInterface,
        shop_service: ShopServiceInterface,
        node_service: NodeServiceInterface,
        settings_service: SettingsServiceInterface,
        project_service: ProjectServiceInterface,
        matrix_run_service: MatrixRunServiceInterface,
        event_dispatcher: EventDispatcher,
        character_id: CharacterId,
        logging_service: LoggingServiceInterface,
    ) -> None:
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.all_sprites = pygame.sprite.Group[pygame.sprite.Sprite]()
        self.asset_service = asset_service
        self.player_service = player_service
        self.character_service = character_service
        self.contract_service = contract_service
        self.player_id = player_id
        self.crafting_service = crafting_service
        self.deck_service = deck_service
        self.shop_service = shop_service
        self.ds_file_service = ds_file_service
        self.node_service = node_service
        self.settings_service = settings_service
        self.project_service = project_service
        self.matrix_run_service = matrix_run_service
        self.character_id = character_id
        self.event_dispatcher = event_dispatcher
        self.logging_service = logging_service
        self._modal_stack = []
        self.debug_actions = DebugActions(self, self.event_dispatcher)
        self.input_handler = PygameInputHandler(
            self, logging_service, self.debug_actions
        )

        self.message_view = MessageView(
            position=(10, 600), size=(400, 150), background_color=UI_FACE
        )
        self.toggle_intro_view()

    def _toggle_view(
        self,
        view_attr: str,
        view_factory: Callable[[], Optional[V]],
    ) -> None:
        """Generic method to open or close a view.

        Args:
            view_attr (str): The name of the attribute on `self` that holds the
                view instance.
            view_factory (Callable[[], Optional[V]]): A function that creates and
                returns a view instance, or None on failure.
        """
        current_view = getattr(self, view_attr)
        if current_view:
            self.all_sprites.remove(current_view)
            setattr(self, view_attr, None)
            if hasattr(current_view, "handle_event"):
                eventful_view = cast(Eventful, current_view)
                if eventful_view in self._modal_stack:
                    self._modal_stack.remove(eventful_view)

        else:
            new_view = view_factory()
            if new_view:
                setattr(self, view_attr, new_view)
                self.all_sprites.add(new_view)

                if hasattr(new_view, "handle_event"):
                    self._modal_stack.append(cast(Eventful, new_view))

    def quit(self) -> None:
        """Signals the game to exit the main loop."""
        self.is_running = False

    def _continue_from_intro(self) -> None:
        """Closes the intro view and opens the new character view."""
        if self.intro_view:
            self.toggle_intro_view()
        self.toggle_new_char_view()

    def _handle_character_creation(self, name: str) -> None:
        """Handles the creation of a new character, then transitions to home."""
        # This is where we would call the character_service to persist the new
        # character and update the game's character_id.
        self.logging_service.log("Character Creation", {"name": name})
        if self.new_char_view:
            self.toggle_new_char_view()
        self.toggle_home_view()

    def toggle_new_char_view(self) -> None:
        """Opens or closes the new character view."""

        def factory() -> NewCharView:
            return NewCharView(on_create=self._handle_character_creation)

        self._toggle_view("new_char_view", factory)

    def toggle_intro_view(self) -> None:
        """Opens or closes the intro view."""

        def factory() -> IntroView:
            return IntroView(on_continue=self._continue_from_intro)

        self._toggle_view("intro_view", factory)

    def toggle_home_view(self) -> None:
        """Opens or closes the home view."""

        def factory() -> HomeView:
            return HomeView(
                on_char=self.toggle_char_data_view,
                on_deck=self.toggle_deck_view,
                on_contracts=self.toggle_contract_list_view,
                on_build=self.toggle_build_view,
                on_shop=self.toggle_shop_view,
                on_transfer=self.toggle_transfer_view,
                on_projects=self.toggle_project_data_view,
            )

        self._toggle_view("home_view", factory)

    def toggle_matrix_run_view(self) -> None:
        """Opens or closes the main matrix run view."""

        def factory() -> MatrixRunView:
            return MatrixRunView(asset_service=self.asset_service)

        self._toggle_view("matrix_run_view", factory)

    def _on_purchase(self, item_name: str) -> None:
        """Callback to handle purchasing an item from the shop."""

        def action() -> None:
            # For now, we assume a single, default shop.
            self.shop_service.purchase_item(self.character_id, item_name, "DefaultShop")
            self.show_message(f"Purchased {item_name}.")

        self._execute_and_refresh_view(action, self.toggle_shop_view)

    def toggle_shop_view(self) -> None:
        """Opens or closes the shop view."""

        def factory() -> Optional[ShopView]:
            shop_data = self.shop_service.get_shop_view_data("DefaultShop")
            if not shop_data:
                self.show_message("Error: Could not load shop data.")
                return None
            return ShopView(
                data=shop_data,
                on_close=self.toggle_shop_view,
                on_purchase=self._on_purchase,
                on_view_details=self._on_show_item_details,
            )

        self._toggle_view("shop_view", factory)

    def toggle_shop_item_view(self, data: Optional["ShopItemViewDTO"] = None) -> None:
        """Opens or closes the Shop Item details view."""

        def factory() -> Optional["ShopItemView"]:
            if data:
                return ShopItemView(
                    data=data,
                    on_close=self.toggle_shop_item_view,
                )
            return None

        self._toggle_view("shop_item_view", factory)

    def _on_new_project(self) -> None:
        """Closes the project data view and opens the new project view."""
        self.toggle_project_data_view()
        self.toggle_new_project_view()

    def _on_work_day(self) -> None:
        """Callback to add one day of work to the current project."""

        def action() -> None:
            self.project_service.work_on_project(self.character_id, 1)
            self.show_message("One day of work completed.")

        self._execute_and_refresh_view(action, self.toggle_project_data_view)

    def _on_work_week(self) -> None:
        """Callback to add one week of work to the current project."""

        def action() -> None:
            self.project_service.work_on_project(self.character_id, 7)
            self.show_message("One week of work completed.")

        self._execute_and_refresh_view(action, self.toggle_project_data_view)

    def _on_finish_project(self) -> None:
        """Callback to complete the current project."""

        def action() -> None:
            self.project_service.complete_project(self.character_id)
            self.show_message("Project finished.")

        self._execute_and_refresh_view(action, self.toggle_project_data_view)

    def _on_build_schematic(self, schematic_id: str) -> None:
        """Callback to build an item from a schematic."""

        def action() -> None:
            self.project_service.build_from_schematic(self.character_id, schematic_id)
            # Success message is handled by the ItemCrafted event handler

        self._execute_and_refresh_view(action, self.toggle_project_data_view)

    def _on_trash_schematic(self, schematic_id: str) -> None:
        """Callback to delete a schematic."""

        def action() -> None:
            self.project_service.trash_schematic(self.character_id, schematic_id)
            self.show_message("Schematic trashed.")

        self._execute_and_refresh_view(action, self.toggle_project_data_view)

    def toggle_project_data_view(self) -> None:
        """Opens or closes the main project management view."""

        def factory() -> Optional[ProjectDataView]:
            data = self.project_service.get_project_data_view_data(self.character_id)
            if not data:
                self.show_message("Error: Could not retrieve project data.")
                return None
            return ProjectDataView(
                data=data,
                on_close=self.toggle_project_data_view,
                on_new_project=self._on_new_project,
                on_work_day=self._on_work_day,
                on_work_week=self._on_work_week,
                on_finish_project=self._on_finish_project,
                on_build=self._on_build_schematic,
                on_trash=self._on_trash_schematic,
            )

        self._toggle_view("project_data_view", factory)

    def _on_rest(self) -> None:
        """Callback for when the player chooses to rest."""
        # Here we would call a service to perform the rest action
        self.logging_service.log("Player Action", {"action": "rest"})
        self.show_message("You feel rested and recovered.")
        # After resting, close the view.
        if self.rest_view:
            self.toggle_rest_view()

    def toggle_rest_view(self, data: Optional[RestViewDTO] = None) -> None:
        """Opens or closes the rest view."""

        def factory() -> Optional[RestView]:
            if data:
                return RestView(
                    data=data,
                    on_rest=self._on_rest,
                    on_close=self.toggle_rest_view,
                )
            return None

        self._toggle_view("rest_view", factory)

    def toggle_mission_results_view(
        self, data: Optional[MissionResultsDTO] = None
    ) -> None:
        """Opens or closes the mission results view."""

        def factory() -> Optional[MissionResultsView]:
            if data:
                return MissionResultsView(
                    data=data, on_close=self.toggle_mission_results_view
                )
            # This view should not be opened without data.
            return None

        self._toggle_view("mission_results_view", factory)

    def toggle_build_view(self) -> None:
        """Opens or closes the build view."""

        def factory() -> Optional[BuildView]:
            schematics = self.crafting_service.get_character_schematics(
                self.character_id
            )
            if not schematics:
                self.show_message("No schematics known.")
                return None
            return BuildView(
                position=(200, 150),
                size=(400, 300),
                schematics=schematics,
                on_build_click=self._handle_build_click,
            )

        self._toggle_view("build_view", factory)

    def _handle_build_click(self, schematic_name: str) -> None:
        """Callback for when a build button is clicked in the BuildView."""
        try:
            self.crafting_service.craft_item(self.character_id, schematic_name)
            # A success message is already handled by the ItemCrafted event handler
            # in main.py, so no need to show a message here.
        except CraftingError as e:
            self.show_message(f"Crafting failed: {e}")

    def _execute_and_refresh_view(
        self, action: Callable[[], None], view_toggler: Callable[[], None]
    ) -> None:
        """Executes an action and refreshes a view by toggling it off and on."""
        try:
            action()
            view_toggler()  # close
            view_toggler()  # open
        except Exception as e:
            self.show_message(f"Error: {e}")

    def _on_increase_skill(self, skill_name: str) -> None:
        """Callback to handle increasing a skill."""

        def action() -> None:
            self.character_service.increase_skill(self.character_id, skill_name)

        self._execute_and_refresh_view(action, self.toggle_char_data_view)

    def _on_decrease_skill(self, skill_name: str) -> None:
        """Callback to handle decreasing a skill."""

        def action() -> None:
            self.character_service.decrease_skill(self.character_id, skill_name)

        self._execute_and_refresh_view(action, self.toggle_char_data_view)

    def toggle_char_data_view(self) -> None:
        """Opens or closes the character data view."""

        def factory() -> Optional["CharDataView"]:
            view_data = self.character_service.get_character_view_data(
                self.character_id, self.player_id
            )
            if not view_data:
                self.show_message("Error: Could not retrieve character/player data.")
                return None
            return CharDataView(
                position=(150, 100),
                data=view_data,
                on_close=self.toggle_char_data_view,
                on_increase_skill=self._on_increase_skill,
                on_decrease_skill=self._on_decrease_skill,
            )

        self._toggle_view("char_data_view", factory)

    def toggle_deck_view(self) -> None:
        """Opens or closes the deck view."""

        def factory() -> Optional["DeckView"]:
            char_data = self.character_service.get_character_data(self.character_id)
            if not char_data:
                self.show_message(
                    "Error: Could not retrieve character data to find deck."
                )
                return None

            deck_data = self.deck_service.get_deck_view_data(char_data.deck_id)
            if not deck_data:
                self.show_message("Error: Could not retrieve deck data.")
                return None

            return DeckView(
                data=deck_data,
                on_close=self.toggle_deck_view,
                on_order=self._on_order_deck,
                on_program_click=self._on_program_click,
            )

        self._toggle_view("deck_view", factory)

    def _move_program_and_refresh(self, move_action: Callable[..., None]) -> None:
        """Generic helper to move a program and refresh the order view."""
        char_data = self.character_service.get_character_data(self.character_id)
        if not char_data:
            self.show_message("Error: Could not find character to modify deck.")
            return
        try:
            move_action(char_data.deck_id)
            self._on_order_deck()  # Refresh the order view
        except Exception as e:
            self.show_message(f"Error: {e}")

    def _on_move_program_up(self, program_name: str) -> None:
        """Callback to handle moving a program up in the deck order."""
        self._move_program_and_refresh(
            lambda deck_id: self.deck_service.move_program_up(deck_id, program_name)
        )

    def _on_move_program_down(self, program_name: str) -> None:
        """Callback to handle moving a program down in the deck order."""
        self._move_program_and_refresh(
            lambda deck_id: self.deck_service.move_program_down(deck_id, program_name)
        )

    def _on_move_program_to_deck(self, program_name: str) -> None:
        """Callback to handle moving a program to the deck."""
        char_data = self.character_service.get_character_data(self.character_id)
        if not char_data:
            self.show_message("Error: Could not find character to modify deck.")
            return

        def action() -> None:
            self.deck_service.move_program_to_deck(self.character_id, program_name)

        self._execute_and_refresh_view(action, self.toggle_transfer_view)

    def _on_move_program_to_storage(self, program_name: str) -> None:
        """Callback to handle moving a program to storage."""
        char_data = self.character_service.get_character_data(self.character_id)
        if not char_data:
            self.show_message("Error: Could not find character to modify deck.")
            return

        def action() -> None:
            self.deck_service.move_program_to_storage(self.character_id, program_name)

        self._execute_and_refresh_view(action, self.toggle_transfer_view)

    def toggle_transfer_view(self) -> None:
        """Opens or closes the program transfer view."""

        def factory() -> Optional["TransferView"]:
            view_data = self.deck_service.get_transfer_view_data(self.character_id)
            if not view_data:
                self.show_message("Error: Could not retrieve transfer data.")
                return None
            return TransferView(
                data=view_data,
                on_close=self.toggle_transfer_view,
                on_move_to_deck=self._on_move_program_to_deck,
                on_move_to_storage=self._on_move_program_to_storage,
            )

        self._toggle_view("transfer_view", factory)

    def _on_program_click(self, program_name: str) -> None:
        """Callback for when a program is clicked, to show its details."""
        ice_data = self.deck_service.get_ice_data(program_name)
        if not ice_data:
            self.show_message(f"No detailed data available for {program_name}.")
            return
        self.toggle_ice_data_view(ice_data)

    def toggle_ice_data_view(self, data: Optional[IceDataViewDTO] = None) -> None:
        """Opens or closes the ICE data view."""

        def factory() -> Optional[IceDataView]:
            if data:
                return IceDataView(data=data, on_close=self.toggle_ice_data_view)
            return None

        self._toggle_view("ice_data_view", factory)

    def toggle_contract_list_view(self) -> None:
        """Opens or closes the contract list view."""

        def factory() -> ContractListView:
            return ContractListView(position=(200, 150), size=(400, 300))

        self._toggle_view("contract_list_view", factory)

    def toggle_contract_data_view(self) -> None:
        """Opens or closes the contract data view."""

        def factory() -> ContractDataView:
            return ContractDataView(
                position=(200, 150), size=(400, 300), contract_name="Placeholder"
            )

        self._toggle_view("contract_data_view", factory)

    def _on_download_file(self, file_name: str) -> None:
        """Callback to handle downloading a file."""
        # In a real implementation, this would call a service.
        self.show_message(f"Downloading {file_name}...")

    def _on_delete_file(self, file_name: str) -> None:
        """Callback to handle deleting a file."""
        # In a real implementation, this would call a service.
        self.show_message(f"Deleting {file_name}...")

    def toggle_file_access_view(self, data: Optional[FileAccessViewDTO] = None) -> None:
        """Opens or closes the file access view."""

        def factory() -> Optional[FileAccessView]:
            if data:
                return FileAccessView(
                    data=data,
                    on_close=self.toggle_file_access_view,
                    on_download=self._on_download_file,
                    on_delete=self._on_delete_file,
                )
            return None

        self._toggle_view("file_access_view", factory)

    def show_file_access_view(self, node_id: str) -> None:
        """Fetches node data and shows the file access view."""
        if self.file_access_view:
            self.toggle_file_access_view()
            return

        node_data = self.node_service.get_node_files(node_id)
        if not node_data:
            self.show_message(f"Error: Could not access node '{node_id}'.")
            return
        self.toggle_file_access_view(node_data)

    def _on_save_game(self) -> None:
        """Callback to handle saving the game."""
        # This will eventually call a service to persist all aggregates.
        self.show_message("Game Saved (Not Implemented).")

    def _on_load_game(self) -> None:
        """Callback to handle loading the game."""
        self.show_message("Game Loaded (Not Implemented).")

    def _on_quit_to_menu(self) -> None:
        """Callback to handle quitting to the main menu."""
        # This will eventually transition the game state.
        self.show_message("Quit to Menu (Not Implemented).")
        self.toggle_options_view()

    def _on_toggle_sound(self, enabled: bool) -> None:
        """Callback to handle toggling sound."""
        self.settings_service.set_sound_enabled(enabled)
        self.show_message(f"Sound {'Enabled' if enabled else 'Disabled'}.")

    def _on_toggle_tooltips(self, enabled: bool) -> None:
        """Callback to handle toggling tooltips."""
        self.settings_service.set_tooltips_enabled(enabled)
        self.show_message(f"Tooltips {'Enabled' if enabled else 'Disabled'}.")

    def toggle_options_view(self) -> None:
        """Opens or closes the options view."""

        def factory() -> Optional[OptionsView]:
            options_data = self.settings_service.get_options()
            return OptionsView(
                data=options_data,
                on_save=self._on_save_game,
                on_load=self._on_load_game,
                on_quit=self._on_quit_to_menu,
                on_close=self.toggle_options_view,
                on_toggle_sound=self._on_toggle_sound,
                on_toggle_tooltips=self._on_toggle_tooltips,
            )

        self._toggle_view("options_view", factory)

    def _on_master_volume_change(self, volume: float) -> None:
        """Callback for master volume slider."""
        self.settings_service.set_master_volume(volume)

    def _on_music_volume_change(self, volume: float) -> None:
        """Callback for music volume slider."""
        self.settings_service.set_music_volume(volume)

    def _on_sfx_volume_change(self, volume: float) -> None:
        """Callback for sfx volume slider."""
        self.settings_service.set_sfx_volume(volume)

    def toggle_sound_edit_view(self) -> None:
        """Opens or closes the sound edit view."""

        def factory() -> Optional[SoundEditView]:
            sound_data = self.settings_service.get_sound_options()
            return SoundEditView(
                data=sound_data,
                on_close=self.toggle_sound_edit_view,
                on_master_volume_change=self._on_master_volume_change,
                on_music_volume_change=self._on_music_volume_change,
                on_sfx_volume_change=self._on_sfx_volume_change,
            )

        self._toggle_view("sound_edit_view", factory)

    def _on_start_project(self, item_type: str, item_class: str, rating: int) -> None:
        """Callback to handle starting a new research project."""
        try:
            self.project_service.start_new_project(
                self.character_id, item_type, item_class, rating
            )
            self.show_message(f"Started research on {item_class} v{rating}.")
            self.toggle_new_project_view()
        except Exception as e:
            self.show_message(f"Error: {e}")

    def toggle_new_project_view(self) -> None:
        """Toggles the visibility of the new project view."""

        def factory() -> Optional[NewProjectView]:
            data = self.project_service.get_new_project_data(self.character_id)
            if not data:
                self.show_message("Error: Could not retrieve project data.")
                return None
            return self._create_new_project_view(data)

        self._toggle_view("new_project_view", factory)

    def _create_new_project_view(
        self, data: NewProjectViewDTO
    ) -> Optional[NewProjectView]:
        """Factory method for creating the NewProjectView."""
        return NewProjectView(
            data=data,
            on_start=self._on_start_project,
            on_close=self.toggle_new_project_view,
        )

    def _on_entry_submit(self, text: str, node_id: str) -> None:
        """Callback to handle submitting text from the entry view."""
        is_valid = self.node_service.validate_password(node_id, text)
        if is_valid:
            self.show_message("Access Granted.")
            # In a real scenario, this would unlock something or transition state.
        else:
            self.show_message("Access Denied.")

        # Close the view after submission
        self.toggle_entry_view()

    def toggle_entry_view(self, node_id: Optional[str] = None) -> None:
        """Opens or closes the entry view for a given node."""

        def factory() -> Optional[EntryView]:
            if node_id:
                dto = EntryViewDTO(
                    prompt=f"Enter Password for {node_id}:", is_password=True
                )
                return EntryView(
                    data=dto,
                    on_submit=partial(self._on_entry_submit, node_id=node_id),
                    on_close=self.toggle_entry_view,
                )
            return None

        self._toggle_view("entry_view", factory)

    def show_message(self, text: str) -> None:
        """Displays a message in the message view."""
        self.message_view.set_text(text)

    def _update(self, dt: int, total_seconds: int) -> None:
        """Update game state.

        Args:
            dt (int): Time since last frame in milliseconds.
            total_seconds (int): Total seconds elapsed since game start.

        Returns:
            None:
        """
        # Update the top-most modal view, or all sprites if no modal is active.
        if self._modal_stack:
            top_view = self._modal_stack[-1]
            if isinstance(top_view, pygame.sprite.Sprite):
                if isinstance(top_view, MatrixRunView):
                    data = self.matrix_run_service.get_matrix_run_view_data(
                        self.character_id, self.player_id
                    )
                    data.run_time_in_seconds = total_seconds
                    top_view.update(data)
                else:
                    top_view.update(dt)  # Other views might still need dt
        else:
            # Update all sprites, but only pass dt if they don't need total_seconds
            for sprite in self.all_sprites:
                if isinstance(sprite, MatrixRunView):
                    data = self.matrix_run_service.get_matrix_run_view_data(
                        self.character_id, self.player_id
                    )
                    data.run_time_in_seconds = total_seconds
                    sprite.update(data)
                else:
                    sprite.update(dt)

    def run(self) -> None:
        """Run the main game loop.

        Returns:
            None:
        """
        while self.is_running:
            dt = self.clock.tick(FPS)  # dt in milliseconds
            total_seconds = pygame.time.get_ticks() // 1000

            self.input_handler.handle_events()
            self._update(dt, total_seconds)

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

    def _on_order_deck(self) -> None:
        """Callback for when the 'Order' button is clicked in the DeckView.

        Opens the OrderView.
        """
        char_data = self.character_service.get_character_data(self.character_id)
        if not char_data:
            self.show_message("Error: Could not retrieve character data to find deck.")
            return

        deck_data = self.deck_service.get_deck_view_data(char_data.deck_id)
        if not deck_data:
            self.show_message("Error: Could not retrieve deck data.")
            return

        # Close the current DeckView or OrderView before opening a new OrderView
        if self.deck_view:
            self.all_sprites.remove(self.deck_view)
            self.deck_view = None
        if self.order_view:
            self.all_sprites.remove(self.order_view)
            self.order_view = None

        self.order_view = OrderView(
            data=deck_data,
            # Closing the OrderView should take you back to the DeckView
            on_close=self.toggle_deck_view,
            on_move_up=self._on_move_program_up,
            on_move_down=self._on_move_program_down,
        )
        self.all_sprites.add(self.order_view)

    def _on_show_item_details(self, item_name: str) -> None:
        """Callback to handle displaying details for a specific shop item."""
        item_details = self.shop_service.get_item_details("DefaultShop", item_name)
        if item_details:
            self.toggle_shop_item_view(item_details)
        else:
            self.show_message(f"Could not retrieve details for {item_name}.")

"""This module defines the main Game class, which orchestrates the presentation layer.

It handles the main game loop, event processing, and the display of all UI components.
"""

from collections.abc import Callable
from functools import partial
from typing import Optional, TypeVar

import pygame

from decker_pygame.application.dtos import (
    EntryViewDTO,
    FileAccessViewDTO,
    MissionResultsDTO,
    NewProjectViewDTO,
    RestViewDTO,
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
from decker_pygame.presentation.states.game_states import BaseState, GameState
from decker_pygame.presentation.states.states import (
    HomeState,
    IntroState,
    MatrixRunState,
    NewCharState,
)
from decker_pygame.presentation.view_manager import ViewManager
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
        states (dict[GameState, type[BaseState]]): A mapping of game state enums
            to their corresponding state classes.
        current_state (BaseState | None): The currently active game state.
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
        view_manager (ViewManager): The manager for UI views.
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

    screen: pygame.Surface
    clock: pygame.time.Clock
    is_running: bool
    all_sprites: pygame.sprite.Group[pygame.sprite.Sprite]
    states: dict[GameState, type[BaseState]]
    current_state: BaseState | None
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
    view_manager: ViewManager
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
        self.states = {
            GameState.INTRO: IntroState,
            GameState.NEW_CHAR: NewCharState,
            GameState.HOME: HomeState,
            GameState.MATRIX_RUN: MatrixRunState,
        }
        self.current_state = None
        self.view_manager = ViewManager(self)
        self.debug_actions = DebugActions(self, self.event_dispatcher)
        self.input_handler = PygameInputHandler(
            self, logging_service, self.debug_actions
        )
        self.message_view = MessageView(
            position=(10, 600), size=(400, 150), background_color=UI_FACE
        )
        self.all_sprites.add(self.message_view)
        self.set_state(GameState.INTRO)

    def quit(self) -> None:
        """Signals the game to exit the main loop."""
        self.is_running = False

    def set_state(self, new_state_enum: GameState) -> None:
        """Transition to a new game state."""
        if self.current_state:
            self.current_state.on_exit()

        if new_state_enum == GameState.QUIT:
            self.quit()
            return

        state_class = self.states.get(new_state_enum)
        if state_class:
            self.current_state = state_class(self)
            self.current_state.on_enter()
        else:
            # This case should ideally not be hit if all states are registered.
            # For now, we can log an error or raise one.
            # A more robust solution might be a fallback state.
            self.logging_service.log(
                "State Machine Error",
                {"message": f"State {new_state_enum} not found."},
            )
            self.quit()

    def update_sprites(self, dt: float) -> None:
        """Update sprites based on modal focus.

        This method contains the core sprite update logic, which is called by the
        currently active game state. It updates only the top-most modal view if
        one is active, otherwise it updates all sprites.

        Args:
            dt (float): Time since last frame in seconds.
        """
        total_seconds = pygame.time.get_ticks() // 1000
        dt_ms = int(dt * 1000)

        # Update the top-most modal view, or all sprites if no modal is active.
        if self.view_manager.modal_stack:
            top_view = self.view_manager.modal_stack[-1]
            if isinstance(top_view, pygame.sprite.Sprite):
                # The modal stack can contain non-sprite objects that are eventful.
                # We only care about updating sprites.
                if isinstance(top_view, MatrixRunView):
                    data = self.matrix_run_service.get_matrix_run_view_data(
                        self.character_id, self.player_id
                    )
                    data.run_time_in_seconds = total_seconds
                    top_view.update(data)
                else:
                    # Other views might still need dt in milliseconds
                    top_view.update(dt_ms)
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
                    sprite.update(dt_ms)

    def _continue_from_intro(self) -> None:
        """Transitions from the intro state to the new character state."""
        self.set_state(GameState.NEW_CHAR)

    def _handle_character_creation(self, name: str) -> None:
        """Handles the creation of a new character, then transitions to home."""
        # This is where we would call the character_service to persist the new
        # character and update the game's character_id.
        self.logging_service.log("Character Creation", {"name": name})
        # The state transition will handle closing the new_char_view.
        self.set_state(GameState.HOME)

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

        self.view_manager.toggle_view("project_data_view", factory)

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

        self.view_manager.toggle_view("rest_view", factory)

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

        self.view_manager.toggle_view("mission_results_view", factory)

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

        self.view_manager.toggle_view("file_access_view", factory)

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

        self.view_manager.toggle_view("options_view", factory)

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

        self.view_manager.toggle_view("sound_edit_view", factory)

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

        self.view_manager.toggle_view("new_project_view", factory)

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

        self.view_manager.toggle_view("entry_view", factory)

    def show_message(self, text: str) -> None:
        """Displays a message in the message view."""
        self.message_view.set_text(text)

    def run(self) -> None:
        """Run the main game loop."""
        while self.is_running:
            dt_ms = self.clock.tick(FPS)
            dt_s = dt_ms / 1000.0

            self.input_handler.handle_events()

            if self.current_state:
                self.current_state.update(dt_s)

            self.screen.fill(BLACK)

            if self.current_state:
                self.current_state.draw(self.screen)

            pygame.display.flip()

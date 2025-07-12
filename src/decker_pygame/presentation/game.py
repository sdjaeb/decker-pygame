"""This module defines the main Game class, which orchestrates the presentation layer.

It handles the main game loop, event processing, and the display of all UI components.
"""

from collections.abc import Callable
from typing import Optional, TypeVar

import pygame

from decker_pygame.application.crafting_service import CraftingError
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.ports.service_interfaces import (
    CharacterServiceInterface,
    ContractServiceInterface,
    CraftingServiceInterface,
    DeckServiceInterface,
    LoggingServiceInterface,
    PlayerServiceInterface,
)
from decker_pygame.presentation.asset_loader import load_spritesheet
from decker_pygame.presentation.components.active_bar import ActiveBar
from decker_pygame.presentation.components.alarm_bar import AlarmBar
from decker_pygame.presentation.components.build_view import BuildView
from decker_pygame.presentation.components.char_data_view import CharDataView
from decker_pygame.presentation.components.contract_data_view import ContractDataView
from decker_pygame.presentation.components.contract_list_view import ContractListView
from decker_pygame.presentation.components.deck_view import DeckView
from decker_pygame.presentation.components.health_bar import HealthBar
from decker_pygame.presentation.components.message_view import MessageView
from decker_pygame.presentation.components.order_view import OrderView
from decker_pygame.presentation.components.transfer_view import TransferView
from decker_pygame.presentation.input_handler import PygameInputHandler
from decker_pygame.presentation.utils import scale_icons
from decker_pygame.settings import (
    BLACK,
    FPS,
    GFX,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    TRANSPARENT_COLOR,
    UI_FACE,
)

V = TypeVar("V", bound=pygame.sprite.Sprite)


class Game:
    """Main game loop and presentation logic."""

    screen: pygame.Surface
    clock: pygame.time.Clock
    is_running: bool
    all_sprites: pygame.sprite.Group[pygame.sprite.Sprite]
    active_bar: ActiveBar
    alarm_bar: AlarmBar
    health_bar: HealthBar
    player_service: PlayerServiceInterface
    character_service: CharacterServiceInterface
    contract_service: ContractServiceInterface
    crafting_service: CraftingServiceInterface
    deck_service: DeckServiceInterface
    player_id: PlayerId
    character_id: CharacterId
    logging_service: LoggingServiceInterface
    message_view: MessageView
    input_handler: PygameInputHandler
    build_view: Optional[BuildView] = None
    char_data_view: Optional[CharDataView] = None
    deck_view: Optional[DeckView] = None
    order_view: Optional[OrderView] = None
    transfer_view: Optional[TransferView] = None
    contract_list_view: Optional[ContractListView] = None
    contract_data_view: Optional[ContractDataView] = None

    def __init__(
        self,
        player_service: PlayerServiceInterface,
        player_id: PlayerId,
        character_service: CharacterServiceInterface,
        contract_service: ContractServiceInterface,
        crafting_service: CraftingServiceInterface,
        deck_service: DeckServiceInterface,
        character_id: CharacterId,
        logging_service: LoggingServiceInterface,
    ) -> None:
        """Initialize the Game.

        Args:
            player_service (PlayerServiceInterface): Service for player ops.
            player_id (PlayerId): The current player's ID.
            character_service (CharacterServiceInterface): Service for character ops.
            contract_service (ContractServiceInterface): Service for contract ops.
            crafting_service (CraftingServiceInterface): Service for crafting ops.
            deck_service (DeckServiceInterface): Service for deck operations.
            character_id (CharacterId): The current character's ID.
            logging_service (LoggingServiceInterface): Service for logging.
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.all_sprites = pygame.sprite.Group[pygame.sprite.Sprite]()
        self.player_service = player_service
        self.character_service = character_service
        self.contract_service = contract_service
        self.player_id = player_id
        self.crafting_service = crafting_service
        self.deck_service = deck_service
        self.character_id = character_id
        self.logging_service = logging_service
        self.input_handler = PygameInputHandler(self, logging_service)

        self._load_assets()

    def _load_assets(self) -> None:
        """Load game assets (images, sounds, etc).

        Returns:
            None
        """
        # Load icons at their native source size
        native_icons, _ = load_spritesheet(
            GFX.program_icon_sheet,
            sprite_width=GFX.program_icon_source_size,
            sprite_height=GFX.program_icon_source_size,
            colorkey=TRANSPARENT_COLOR,
        )

        # Scale the icons up to the size required by the UI components
        target_size = (GFX.active_bar_image_size, GFX.active_bar_image_size)
        program_icons = scale_icons(native_icons, target_size)

        self.active_bar = ActiveBar(position=(0, 0), image_list=program_icons)
        self.all_sprites.add(self.active_bar)

        # Position from DeckerSource_1_12/MatrixView.cpp
        self.alarm_bar = AlarmBar(position=(206, 342), width=200, height=50)
        self.all_sprites.add(self.alarm_bar)

        self.health_bar = HealthBar(position=(10, 342), width=180, height=50)
        self.all_sprites.add(self.health_bar)

        self.message_view = MessageView(
            position=(10, 600), size=(400, 150), background_color=UI_FACE
        )
        self.all_sprites.add(self.message_view)

    def _toggle_view(
        self,
        view_attr: str,
        view_factory: Callable[[], Optional[V]],
    ) -> None:
        """Generic method to open or close a view.

        Args:
            view_attr: The name of the attribute on `self` that holds the view instance.
            view_factory: A function that creates and returns a view instance, or None
                          on failure.
        """
        current_view = getattr(self, view_attr)
        if current_view:
            self.all_sprites.remove(current_view)
            setattr(self, view_attr, None)
        else:
            new_view = view_factory()
            if new_view:
                setattr(self, view_attr, new_view)
                self.all_sprites.add(new_view)

    def quit(self) -> None:
        """Signals the game to exit the main loop."""
        self.is_running = False

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

        def factory() -> Optional[CharDataView]:
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

        def factory() -> Optional[DeckView]:
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
            )

        self._toggle_view("deck_view", factory)

    def _on_move_program_up(self, program_name: str) -> None:
        """Callback to handle moving a program up in the deck order."""
        char_data = self.character_service.get_character_data(self.character_id)
        if not char_data:
            self.show_message("Error: Could not find character to modify deck.")
            return
        try:
            self.deck_service.move_program_up(char_data.deck_id, program_name)
            self._on_order_deck()  # Refresh the order view
        except Exception as e:
            self.show_message(f"Error: {e}")

    def _on_move_program_down(self, program_name: str) -> None:
        """Callback to handle moving a program down in the deck order."""
        char_data = self.character_service.get_character_data(self.character_id)
        if not char_data:
            self.show_message("Error: Could not find character to modify deck.")
            return
        try:
            self.deck_service.move_program_down(char_data.deck_id, program_name)
            self._on_order_deck()  # Refresh the order view
        except Exception as e:
            self.show_message(f"Error: {e}")

    def _on_move_program_to_deck(self, program_name: str) -> None:
        """Callback to handle moving a program to the deck."""

        def action() -> None:
            self.deck_service.move_program_to_deck(self.character_id, program_name)

        self._execute_and_refresh_view(action, self.toggle_transfer_view)

    def _on_move_program_to_storage(self, program_name: str) -> None:
        """Callback to handle moving a program to storage."""

        def action() -> None:
            self.deck_service.move_program_to_storage(self.character_id, program_name)

        self._execute_and_refresh_view(action, self.toggle_transfer_view)

    def toggle_transfer_view(self) -> None:
        """Opens or closes the program transfer view."""

        def factory() -> Optional[TransferView]:
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

    def show_message(self, text: str) -> None:
        """Displays a message in the message view."""
        self.message_view.set_text(text)

    def _update(self) -> None:
        """Update game state.

        Returns:
            None
        """
        player_status = self.player_service.get_player_status(self.player_id)
        if player_status:
            self.health_bar.update_health(
                player_status.current_health, player_status.max_health
            )
            # self.alarm_bar.update_state(player.alert_level, player.is_crashing)

        self.all_sprites.update()

    def run(self) -> None:
        """Run the main game loop.

        Returns:
            None
        """
        while self.is_running:
            self.input_handler.handle_events()
            self._update()

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

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

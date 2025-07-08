import pygame

from decker_pygame.application.crafting_service import CraftingError
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.ports.service_interfaces import (
    CharacterServiceInterface,
    ContractServiceInterface,
    CraftingServiceInterface,
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
from decker_pygame.presentation.components.health_bar import HealthBar
from decker_pygame.presentation.components.message_view import MessageView
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
    player_id: PlayerId
    character_id: CharacterId
    logging_service: LoggingServiceInterface
    message_view: MessageView
    input_handler: PygameInputHandler
    build_view: BuildView | None = None
    char_data_view: CharDataView | None = None
    contract_list_view: ContractListView | None = None
    contract_data_view: ContractDataView | None = None

    def __init__(
        self,
        player_service: PlayerServiceInterface,
        player_id: PlayerId,
        character_service: CharacterServiceInterface,
        contract_service: ContractServiceInterface,
        crafting_service: CraftingServiceInterface,
        character_id: CharacterId,
        logging_service: LoggingServiceInterface,
    ) -> None:
        """
        Initialize the Game.

        Args:
            player_service (PlayerServiceInterface): Service for player ops.
            player_id (PlayerId): The current player's ID.
            character_service (CharacterServiceInterface): Service for character ops.
            contract_service (ContractServiceInterface): Service for contract ops.
            crafting_service (CraftingServiceInterface): Service for crafting ops.
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
        self.character_id = character_id
        self.logging_service = logging_service
        self.input_handler = PygameInputHandler(self, logging_service)

        self._load_assets()

    def _load_assets(self) -> None:
        """
        Load game assets (images, sounds, etc).

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

    def quit(self) -> None:
        """Signals the game to exit the main loop."""
        self.is_running = False

    def toggle_build_view(self) -> None:
        """Opens or closes the build view."""
        if self.build_view:
            self.all_sprites.remove(self.build_view)
            self.build_view = None
        else:
            schematics = self.crafting_service.get_character_schematics(
                self.character_id
            )
            if not schematics:
                print("No schematics known.")
                return

            self.build_view = BuildView(
                position=(200, 150),
                size=(400, 300),
                schematics=schematics,
                on_build_click=self._handle_build_click,
            )
            self.all_sprites.add(self.build_view)

    def _handle_build_click(self, schematic_name: str) -> None:
        """Callback for when a build button is clicked in the BuildView."""
        try:
            self.crafting_service.craft_item(self.character_id, schematic_name)
            self.show_message(f"Successfully crafted {schematic_name}!")
        except CraftingError as e:
            self.show_message(f"Crafting failed: {e}")

    def _on_increase_skill(self, skill_name: str) -> None:
        """Callback to handle increasing a skill."""
        try:
            self.character_service.increase_skill(self.character_id, skill_name)
            self.toggle_char_data_view()  # Close
            self.toggle_char_data_view()  # and re-open to refresh
        except Exception as e:
            self.show_message(f"Error: {e}")

    def _on_decrease_skill(self, skill_name: str) -> None:
        """Callback to handle decreasing a skill."""
        self.character_service.decrease_skill(self.character_id, skill_name)
        self.toggle_char_data_view()  # Close
        self.toggle_char_data_view()  # and re-open to refresh

    def toggle_char_data_view(self) -> None:
        """Opens or closes the character data view."""
        if self.char_data_view:
            self.all_sprites.remove(self.char_data_view)
            self.char_data_view = None
        else:
            char_data = self.character_service.get_character_data(self.character_id)
            player_status = self.player_service.get_player_status(self.player_id)

            if not char_data or not player_status:
                print("Could not retrieve character/player data.")
                return

            self.char_data_view = CharDataView(
                position=(150, 100),
                size=(400, 450),
                character_name=char_data.name,
                reputation=char_data.reputation,
                money=char_data.credits,
                health=player_status.current_health,
                skills=char_data.skills,
                unused_skill_points=char_data.unused_skill_points,
                on_close=self.toggle_char_data_view,
                on_increase_skill=self._on_increase_skill,
                on_decrease_skill=self._on_decrease_skill,
            )
            self.all_sprites.add(self.char_data_view)

    def toggle_contract_list_view(self) -> None:
        """Opens or closes the contract list view."""
        if self.contract_list_view:
            self.all_sprites.remove(self.contract_list_view)
            self.contract_list_view = None
        else:
            self.contract_list_view = ContractListView(
                position=(200, 150), size=(400, 300)
            )
            self.all_sprites.add(self.contract_list_view)

    def toggle_contract_data_view(self) -> None:
        """Opens or closes the contract data view."""
        if self.contract_data_view:
            self.all_sprites.remove(self.contract_data_view)
            self.contract_data_view = None
        else:
            self.contract_data_view = ContractDataView(
                position=(200, 150), size=(400, 300), contract_name="Placeholder"
            )
            self.all_sprites.add(self.contract_data_view)

    def show_message(self, text: str) -> None:
        """Displays a message in the message view."""
        self.message_view.set_text(text)

    def _update(self) -> None:
        """
        Update game state.

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
        """
        Run the main game loop.

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

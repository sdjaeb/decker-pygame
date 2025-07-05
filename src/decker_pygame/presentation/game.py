import pygame

from decker_pygame.application.crafting_service import CraftingError, CraftingService
from decker_pygame.application.player_service import PlayerService
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.presentation.asset_loader import load_spritesheet
from decker_pygame.presentation.components.active_bar import ActiveBar
from decker_pygame.presentation.components.alarm_bar import AlarmBar
from decker_pygame.presentation.components.build_view import BuildView
from decker_pygame.presentation.components.message_view import MessageView
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
    player_service: PlayerService
    player_id: PlayerId
    crafting_service: CraftingService
    character_id: CharacterId
    message_view: MessageView
    build_view: BuildView | None = None

    def __init__(
        self,
        player_service: PlayerService,
        player_id: PlayerId,
        crafting_service: CraftingService,
        character_id: CharacterId,
    ) -> None:
        """
        Initialize the Game.

        Args:
            player_service (PlayerService): Service for player operations.
            player_id (PlayerId): The current player's ID.
            crafting_service (CraftingService): Service for crafting operations.
            character_id (CharacterId): The current character's ID.
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.all_sprites = pygame.sprite.Group[pygame.sprite.Sprite]()
        self.player_service = player_service
        self.player_id = player_id
        self.crafting_service = crafting_service
        self.character_id = character_id

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
        program_icons = [
            pygame.transform.scale(icon, target_size) for icon in native_icons
        ]

        self.active_bar = ActiveBar(position=(0, 0), image_list=program_icons)
        self.all_sprites.add(self.active_bar)

        # Position from DeckerSource_1_12/MatrixView.cpp
        self.alarm_bar = AlarmBar(206, 342, 200, 50)
        self.all_sprites.add(self.alarm_bar)

        self.message_view = MessageView(
            position=(10, 600), size=(400, 150), background_color=UI_FACE
        )
        self.all_sprites.add(self.message_view)

    def _handle_events(self) -> None:
        """
        Handle user input and system events.

        Returns:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self._toggle_build_view()

            if self.build_view:
                self.build_view.handle_event(event)

    def _toggle_build_view(self) -> None:
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
        print(f"Attempting to build: {schematic_name}")
        try:
            self.crafting_service.craft_item(self.character_id, schematic_name)
            print(f"Successfully crafted {schematic_name}!")
        except CraftingError as e:
            print(f"Crafting failed: {e}")

    def show_message(self, text: str) -> None:
        """Displays a message in the message view."""
        self.message_view.set_text(text)

    def _update(self) -> None:
        """
        Update game state.

        Returns:
            None
        """
        # In the future, we will get player state from the service:
        # player = self.player_service.get_player(self.player_id)
        # self.alarm_bar.update_state(player.alert_level, player.is_crashing)

        self.all_sprites.update()
        # self.alarm_bar.update_state(0, False) # Example placeholder

    def run(self) -> None:
        """
        Run the main game loop.

        Returns:
            None
        """
        while self.is_running:
            self._handle_events()
            self._update()

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

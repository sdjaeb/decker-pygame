import pygame
from decker_pygame.asset_loader import load_spritesheet
from decker_pygame.components.active_bar import ActiveBar
from decker_pygame.components.alarm_bar import AlarmBar
from decker_pygame.settings import (
    ALARM,
    BLACK,
    FPS,
    GFX,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    TRANSPARENT_COLOR,
)


class Game:
    """Encapsulates the main game loop and state."""

    screen: pygame.Surface
    clock: pygame.time.Clock
    is_running: bool
    all_sprites: pygame.sprite.Group
    active_bar: ActiveBar
    alarm_bar: AlarmBar

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.all_sprites = pygame.sprite.Group()

        # --- Temporary state for demonstration ---
        self.alert_level = 0
        self.is_crashing = False
        self.last_alarm_update = pygame.time.get_ticks()
        # -----------------------------------------
        self._load_assets()

    def _load_assets(self) -> None:
        """Load game assets and create initial game objects."""
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
        self.alarm_bar = AlarmBar(position=(206, 342))
        self.all_sprites.add(self.alarm_bar)

    def _handle_events(self) -> None:
        """Process user input and other events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self) -> None:
        """Update game state."""
        # --- Temporary logic to cycle alarm state for demonstration ---
        now = pygame.time.get_ticks()
        if now - self.last_alarm_update > 2000:  # every 2 seconds
            self.last_alarm_update = now
            if self.is_crashing:
                self.is_crashing = False
                self.alert_level = 0
            elif self.alert_level == len(ALARM.colors) - 1:
                self.is_crashing = True
            else:
                self.alert_level += 1
        # ----------------------------------------------------------

        self.all_sprites.update()
        self.alarm_bar.update_state(self.alert_level, self.is_crashing)

    def run(self) -> None:
        """The main game loop."""
        while self.is_running:
            self._handle_events()
            self._update()

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

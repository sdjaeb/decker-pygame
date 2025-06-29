import pygame
from decker_pygame.asset_loader import load_images
from decker_pygame.components.active_bar import ActiveBar
from decker_pygame.settings import GFX, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE


class Game:
    """Encapsulates the main game loop and state."""

    screen: pygame.Surface
    clock: pygame.time.Clock
    is_running: bool
    all_sprites: pygame.sprite.Group
    active_bar: ActiveBar

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.all_sprites = pygame.sprite.Group()
        self._load_assets()

    def _load_assets(self) -> None:
        """Load game assets and create initial game objects."""
        program_icons = load_images(
            "programs", (GFX.active_bar_image_size, GFX.active_bar_image_size)
        )
        self.active_bar = ActiveBar(position=(0, 0), image_list=program_icons)
        self.all_sprites.add(self.active_bar)

    def _handle_events(self) -> None:
        """Process user input and other events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def run(self) -> None:
        """The main game loop."""
        while self.is_running:
            self._handle_events()
            self.all_sprites.update()

            self.screen.fill((0, 0, 0))  # Black background
            self.all_sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)  # Limit frame rate to 60 FPS

        pygame.quit()

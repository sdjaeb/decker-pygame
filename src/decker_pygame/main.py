import sys

import pygame

import decker_pygame.asset_loader as asset_loader
from decker_pygame.components.active_bar import ActiveBar
from decker_pygame.settings import (
    BLACK,
    FPS,
    GFX,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
)


class Game:
    """Encapsulates the main game logic and loop."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.all_sprites = pygame.sprite.Group()
        self.program_icons: list[pygame.Surface] = []

        self._load_assets()

    def _load_assets(self) -> None:
        """Load all game assets after the display is initialized."""
        self.program_icons = asset_loader.load_image_sheet(
            path=GFX.program_icon_sheet,
            width=GFX.active_bar_image_size,
            height=GFX.active_bar_image_size,
            colorkey=(255, 0, 255),
        )

    def _setup(self) -> None:
        """Create game objects and setup initial state."""
        active_bar = ActiveBar(position=(10, 10), image_list=self.program_icons)
        self.all_sprites.add(active_bar)

        # --- Example Usage: Activate some programs ---
        # Icon indices are based on the order in programs.bmp
        active_bar.set_active_program(slot=0, image_index=1)  # Example: Analyze
        active_bar.set_active_program(slot=2, image_index=4)  # Example: Deception
        active_bar.set_active_program(slot=5, image_index=7)  # Example: Evasion

    def _handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_running = False

    def _update(self) -> None:
        """Update all game objects."""
        self.all_sprites.update()

    def _draw(self) -> None:
        """Draw everything to the screen."""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self) -> None:
        """The main game loop."""
        self._setup()
        while self.is_running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        pygame.quit()


def main() -> None:
    """The main function and entry point for the Decker game."""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pygame.quit()
        sys.exit(1)
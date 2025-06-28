import sys

import pygame

from decker_pygame.asset_loader import PROGRAM_ICONS
from decker_pygame.components.active_bar import ActiveBar
from decker_pygame.settings import (
    BLACK,
    FPS,
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

    def _setup(self) -> None:
        """Create game objects and setup initial state."""
        active_bar = ActiveBar(position=(10, 10), image_list=PROGRAM_ICONS)
        self.all_sprites.add(active_bar)

        # --- Example Usage: Activate some programs ---


    active_bar = ActiveBar(position=(10, 10), image_list=placeholder_icons)
    all_sprites.add(active_bar)

    # --- Example Usage: Activate some programs ---
    active_bar.set_active_program(slot=0, image_index=1)
    active_bar.set_active_program(slot=2, image_index=4)
    active_bar.set_active_program(slot=5, image_index=7)

    # --- Main Game Loop ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        all_sprites.update()

        screen.fill(BLACK)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
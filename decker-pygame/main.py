import sys

import pygame

from decker_pygame.components.active_bar import ActiveBar

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- Colors ---
BLACK = (0, 0, 0)


def main() -> None:
    """The main function for the Decker game."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Decker-Pygame")
    clock = pygame.time.Clock()

    # --- Asset Loading (Placeholders) ---
    # The original C++ code uses a CImageList. We will simulate this with a
    # list of placeholder surfaces until we port the asset loading.
    placeholder_icons = []
    for i in range(10):  # Assuming 10 possible program icons
        icon = pygame.Surface([16, 16])
        icon.fill((i * 25, 255 - (i * 25), (i * 10) % 255))
        pygame.draw.rect(icon, BLACK, icon.get_rect(), 1)  # border
        placeholder_icons.append(icon)

    # --- Game Object Creation ---
    all_sprites = pygame.sprite.Group()

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
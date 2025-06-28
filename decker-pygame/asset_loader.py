from pathlib import Path

import pygame

from decker_pygame.settings import ACTIVE_IMAGE_SIZE, PROGRAM_ICON_SHEET


def load_image(path: str | Path, colorkey: pygame.Color | None = None) -> pygame.Surface:
    """Loads an image, converting it for performance."""
    try:
        image = pygame.image.load(path).convert()
    except pygame.error as e:
        print(f"Unable to load image: {path}")
        raise SystemExit(e) from e

    if colorkey:
        image.set_colorkey(colorkey)

    return image


def load_image_sheet(
    path: str | Path, width: int, height: int, colorkey: pygame.Color | None = None
) -> list[pygame.Surface]:
    """Loads a spritesheet and slices it into a list of surfaces."""
    sheet = load_image(path, colorkey)
    sheet_width, sheet_height = sheet.get_size()
    cols = sheet_width // width
    rows = sheet_height // height
    images = []

    for row_index in range(rows):
        for col_index in range(cols):
            rect = pygame.Rect(col_index * width, row_index * height, width, height)
            image = pygame.Surface(rect.size).convert()
            image.blit(sheet, (0, 0), rect)
            if colorkey:
                image.set_colorkey(colorkey)
            images.append(image)

    return images


# --- Pre-loaded Game Assets ---
# The original game uses a single bitmap for all program icons.
# The color magenta (255, 0, 255) is used for transparency.
PROGRAM_ICONS = load_image_sheet(
    PROGRAM_ICON_SHEET,
    ACTIVE_IMAGE_SIZE,
    ACTIVE_IMAGE_SIZE,
    colorkey=(255, 0, 255),
)
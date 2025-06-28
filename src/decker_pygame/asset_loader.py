from pathlib import Path

import pygame

from decker_pygame.settings import GFX


def load_image(path: str | Path, colorkey: pygame.Color | None = None) -> pygame.Surface:
    """Loads an image, converting it for performance."""
    path_obj = Path(path)
    if not path_obj.is_file():
        print(f"Error: Asset not found at path: {path_obj.resolve()}")
        print("Please ensure all game assets from 'DeckerSource_1_12' have been copied correctly.")
        raise FileNotFoundError(f"Asset not found: {path_obj.resolve()}")

    try:
        # Use the Path object for loading
        image = pygame.image.load(path_obj).convert()
    except pygame.error as e:
        print(f"Pygame error while loading image: {path_obj}")
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
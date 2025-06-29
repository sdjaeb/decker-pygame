from pathlib import Path

import pygame
from decker_pygame.settings import GFX
from pygame.typing import ColorLike


def load_images(
    subdirectory: str,
    size: tuple[int, int] | None = None,
    base_path: Path | None = None,
) -> list[pygame.Surface]:
    """
    Loads all images from a subdirectory within the main asset folder.

    Args:
        subdirectory: The name of the folder within the assets directory.
        size: An optional (width, height) tuple to scale the images to.
        base_path: The base path to the assets folder, for testing purposes.

    Returns:
        A list of loaded and optionally resized pygame.Surface objects,
        sorted by filename.
    """
    asset_path = (base_path or GFX.asset_folder) / subdirectory
    image_extensions = {".png", ".jpg", ".jpeg", ".bmp"}
    images = []

    for file_path in sorted(asset_path.iterdir()):
        if file_path.suffix.lower() in image_extensions:
            image = pygame.image.load(str(file_path)).convert_alpha()  # type: ignore[attr-defined]
            if size:
                image = pygame.transform.scale(image, size)  # type: ignore[attr-defined]
            images.append(image)
    return images


def load_spritesheet(
    filename: str,
    sprite_width: int,
    sprite_height: int,
    base_path: Path | None = None,
    colorkey: ColorLike | None = None,
) -> tuple[list[pygame.Surface], tuple[int, int]]:
    """
    Loads images from a spritesheet by introspecting its dimensions.

    Args:
        filename: The filename of the spritesheet in the assets folder.
        sprite_width: The width of a single sprite.
        sprite_height: The height of a single sprite.
        base_path: The base path to the assets folder, for testing purposes.
        colorkey: The color to treat as transparent.

    Returns:
        A tuple containing the list of sprites and the (width, height) of the sheet.
    """
    asset_path = (base_path or GFX.asset_folder) / filename
    sheet = pygame.image.load(str(asset_path)).convert()

    sheet_width, sheet_height = sheet.get_size()
    columns = sheet_width // sprite_width
    rows = sheet_height // sprite_height

    sprites = []
    for row in range(rows):
        for col in range(columns):
            rect = pygame.Rect(
                col * sprite_width, row * sprite_height, sprite_width, sprite_height
            )
            image = pygame.Surface((sprite_width, sprite_height))
            image.blit(sheet, (0, 0), rect)
            if colorkey:
                image.set_colorkey(colorkey)
            sprites.append(image)
    return sprites, (sheet_width, sheet_height)

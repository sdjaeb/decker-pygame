"""Provides utility functions for loading game assets.

This includes helpers for loading images and spritesheets.
"""

from pathlib import Path
from typing import Optional

import pygame
from pygame.typing import ColorLike

from decker_pygame.settings import GFX


def load_images(
    subdirectory: str,
    size: Optional[tuple[int, int]] = None,
    base_path: Optional[Path] = None,
) -> list[pygame.Surface]:
    """Loads all images from a subdirectory within the main asset folder.

    Args:
        subdirectory (str): The name of the folder within the assets directory.
        size (Optional[tuple[int, int]]): An optional (width, height) tuple to scale
            the images to.
        base_path (Optional[Path]): The base path to the assets folder, for testing.

    Returns:
        list[pygame.Surface]: A list of loaded and optionally resized pygame.Surface
            objects, sorted by filename.
    """
    asset_path = (base_path or GFX.asset_folder) / subdirectory
    image_extensions = {".png", ".jpg", ".jpeg", ".bmp"}
    images = []

    for file_path in sorted(asset_path.iterdir()):
        if file_path.suffix.lower() in image_extensions:
            image = pygame.image.load(str(file_path)).convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            images.append(image)
    return images


def load_spritesheet(
    filename: str,
    sprite_width: int,
    sprite_height: int,
    base_path: Optional[Path] = None,
    colorkey: Optional[ColorLike] = None,
) -> tuple[list[pygame.Surface], tuple[int, int]]:
    """Loads images from a spritesheet by introspecting its dimensions.

    Args:
        filename (str): The filename of the spritesheet in the assets folder.
        sprite_width (int): The width of a single sprite.
        sprite_height (int): The height of a single sprite.
        base_path (Optional[Path]): The base path to the assets folder, for testing.
        colorkey (Optional[ColorLike]): The color to treat as transparent.

    Returns:
        tuple[list[pygame.Surface], tuple[int, int]]: A tuple containing the list of
        sprites and the (width, height) of the sheet.
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

"""Provides utility functions for loading game assets.

This includes helpers for loading images and spritesheets.
"""

from pathlib import Path
from typing import Optional

import pygame
from pygame.typing import ColorLike


def load_images(
    base_path: Path,
    subdirectory: str,
    size: Optional[tuple[int, int]] = None,
) -> list[pygame.Surface]:
    """Loads all images from a subdirectory within the main asset folder.

    Args:
        base_path (Path): The base path to the assets folder.
        subdirectory (str): The name of the folder within the assets directory.
        size (Optional[tuple[int, int]]): An optional (width, height) tuple to scale
            the images to.

    Returns:
        list[pygame.Surface]: A list of loaded and optionally resized pygame.Surface
            objects, sorted by filename.
    """
    asset_path = base_path / subdirectory
    image_extensions = {".png", ".jpg", ".jpeg", ".bmp"}
    images: list[pygame.Surface] = []
    # If the directory doesn't exist, return an empty list instead of
    # raising; callers (the AssetService) expect to handle missing assets
    # gracefully.
    if not asset_path.exists() or not asset_path.is_dir():
        return images

    for file_path in sorted(asset_path.iterdir()):
        if file_path.suffix.lower() in image_extensions:
            loaded = pygame.image.load(str(file_path))
            # convert_alpha() may require a video/display to be initialized
            # (common in headless CI). Attempt conversion but fall back to
            # the raw loaded surface if the conversion fails.
            try:
                image = loaded.convert_alpha()
            except pygame.error:
                image = loaded
            if size:
                image = pygame.transform.scale(image, size)
            images.append(image)
    return images


def load_spritesheet(
    filename: str,
    sprite_width: int,
    sprite_height: int,
    base_path: Path,
    colorkey: Optional[ColorLike] = None,
) -> tuple[list[pygame.Surface], tuple[int, int]]:
    """Loads images from a spritesheet by introspecting its dimensions.

    Args:
        filename (str): The filename of the spritesheet in the assets folder.
        sprite_width (int): The width of a single sprite.
        sprite_height (int): The height of a single sprite.
        base_path (Path): The base path to the assets folder.
        colorkey (Optional[ColorLike]): The color to treat as transparent.

    Returns:
        tuple[list[pygame.Surface], tuple[int, int]]: A tuple containing the list of
        sprites and the (width, height) of the sheet.
    """
    asset_path = base_path / filename

    # Call pygame.image.load directly; tests frequently mock this call and
    # patching allows the loader to work even when the filesystem path
    # doesn't actually exist in the test environment.
    loaded = pygame.image.load(str(asset_path))
    try:
        sheet = loaded.convert_alpha()
    except pygame.error:
        sheet = loaded

    sheet_width, sheet_height = sheet.get_size()
    columns = sheet_width // sprite_width
    rows = sheet_height // sprite_height

    sprites = []
    for row in range(rows):
        for col in range(columns):
            rect = pygame.Rect(
                col * sprite_width, row * sprite_height, sprite_width, sprite_height
            )
            # Use SRCALPHA to ensure the new surface can handle transparency,
            # matching the format of the parent sheet.
            image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), rect)
            if colorkey:
                image.set_colorkey(colorkey)
            sprites.append(image)
    return sprites, (sheet_width, sheet_height)

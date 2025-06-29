from pathlib import Path

import pygame
from decker_pygame.settings import GFX


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
    if base_path is None:
        base_path = GFX.asset_folder
    asset_path = base_path / subdirectory
    image_extensions = {".png", ".jpg", ".jpeg", ".bmp"}
    images = []

    for file_path in sorted(asset_path.iterdir()):
        if file_path.suffix.lower() in image_extensions:
            image = pygame.image.load(str(file_path)).convert_alpha()  # type: ignore[attr-defined]
            if size:
                image = pygame.transform.scale(image, size)  # type: ignore[attr-defined]
            images.append(image)
    return images

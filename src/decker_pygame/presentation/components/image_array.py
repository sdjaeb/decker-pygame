"""This module defines the ImageArray component."""

import pygame


class ImageArray(pygame.sprite.Sprite):
    """A sprite that can display one of several images from a list.

    This is useful for animations or multi-state icons.
    Ported from ImageArray.cpp/h.

    Args:
        position (tuple[int, int]): The (x, y) position of the top-left corner.
        images (list[pygame.Surface]): A list of pygame.Surface objects to use as
            frames.

    Attributes:
        image (pygame.Surface): The currently displayed image from the array.
        rect (pygame.Rect): The rectangular area of the image.

    Raises:
        ValueError: If the images list is empty.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _images: list[pygame.Surface]
    _current_index: int

    def __init__(self, position: tuple[int, int], images: list[pygame.Surface]):
        super().__init__()
        if not images:
            raise ValueError("ImageArray must be initialized with at least one image.")

        self._images = images
        self._current_index = 0
        self.image = self._images[self._current_index]
        self.rect = self.image.get_rect(topleft=position)

    def set_image(self, index: int) -> None:
        """Set the currently displayed image by its index in the list.

        Args:
            index (int): The index of the image to display.
        """
        if not (0 <= index < len(self._images)):
            print(f"Warning: Invalid index {index} for ImageArray.")
            return

        self._current_index = index
        self.image = self._images[self._current_index]

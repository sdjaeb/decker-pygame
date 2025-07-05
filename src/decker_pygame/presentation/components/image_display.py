import pygame


class ImageDisplay(pygame.sprite.Sprite):
    """
    A simple sprite that displays a single, static image.
    This is useful for backgrounds, logos, or other non-interactive elements.
    Ported from ImageDisplay.cpp/h.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, position: tuple[int, int], image: pygame.Surface):
        """
        Initialize the ImageDisplay.

        Args:
            position: The (x, y) position of the top-left corner.
            image: The pygame.Surface to display.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

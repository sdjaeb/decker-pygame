import pygame

from decker_pygame.presentation.utils import get_and_ensure_rect


class MatrixView(pygame.sprite.Sprite):
    """
    A composite sprite that acts as a container for other UI components,
    representing the main matrix interface view.
    Ported from MatrixView.cpp/h.
    """

    image: pygame.Surface
    rect: pygame.Rect
    components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        background_color: pygame.Color,
    ):
        """
        Initialize the MatrixView.

        Args:
            position: The (x, y) position of the top-left corner of the view.
            size: The (width, height) of the view's surface.
            background_color: The background color of the view.
        """
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self._background_color = background_color
        self.components = pygame.sprite.Group[pygame.sprite.Sprite]()

        self.update()

    def add_component(
        self, sprite: pygame.sprite.Sprite, relative_pos: tuple[int, int]
    ) -> None:
        """
        Adds a component to the view at a position relative to the view's top-left.

        Args:
            sprite: The sprite component to add.
            relative_pos: The (x, y) position for the sprite, relative to this view.
        """
        rect = get_and_ensure_rect(sprite)
        rect.topleft = relative_pos
        self.components.add(sprite)
        self.update()

    def update(self) -> None:
        """
        Updates all contained components and redraws them onto this view's surface.
        """
        self.components.update()
        self.image.fill(self._background_color)
        self.components.draw(self.image)

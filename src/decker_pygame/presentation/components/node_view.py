import pygame


class NodeView(pygame.sprite.Sprite):
    """
    A sprite that represents a single node on a map, capable of displaying
    different visual states (e.g., normal, targeted, accessed).
    Ported from NodeView.cpp/h.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _images: list[pygame.Surface]
    _current_index: int

    def __init__(self, position: tuple[int, int], images: list[pygame.Surface]):
        """
        Initialize the NodeView.

        Args:
            position: The (x, y) position of the top-left corner.
            images: A list of pygame.Surface objects to use for different states.

        Raises:
            ValueError: If the images list is empty.
        """
        super().__init__()
        if not images:
            raise ValueError("NodeView must be initialized with at least one image.")

        self._images = images
        self._current_index = 0
        self.image = self._images[self._current_index]
        self.rect = self.image.get_rect(topleft=position)

    def set_state(self, state_index: int) -> None:
        """
        Set the node's visual state by its index in the image list.

        Args:
            state_index: The index of the image to display.
        """
        if not (0 <= state_index < len(self._images)):
            print(f"Warning: Invalid state_index {state_index} for NodeView.")
            return

        self._current_index = state_index
        self.image = self._images[self._current_index]

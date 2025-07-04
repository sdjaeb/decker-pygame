from collections.abc import Callable

import pygame


class CustomButton(pygame.sprite.Sprite):
    """A reusable button sprite that handles visual states and click events."""

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(
        self,
        position: tuple[int, int],
        image_up: pygame.Surface,
        image_down: pygame.Surface,
        on_click: Callable[[], None],
    ):
        """
        Initialize the CustomButton.

        Args:
            position: The (x, y) position of the top-left corner.
            image_up: The surface to display when the button is not pressed.
            image_down: The surface to display when the button is pressed.
            on_click: A zero-argument function to call when the button is clicked.
        """
        super().__init__()
        self._image_up = image_up
        self._image_down = image_down
        self._on_click = on_click

        self.image = self._image_up
        self.rect = self.image.get_rect(topleft=position)
        self._is_pressed = False

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle a single pygame event.

        This method checks for mouse button events to trigger the button's action
        and update its visual state.

        Args:
            event: The pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._is_pressed = True
                self.image = self._image_down
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Only trigger the click if the mouse is released over the button
            if self.rect.collidepoint(event.pos) and self._is_pressed:
                self._on_click()

            # Always reset state on mouse up
            self._is_pressed = False
            self.image = self._image_up

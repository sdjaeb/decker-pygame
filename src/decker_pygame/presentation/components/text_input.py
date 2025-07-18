"""This module defines a reusable text input widget."""

import pygame

from decker_pygame.settings import UI_FONT

from .base_widgets import Clickable


class TextInput(Clickable):
    """A UI component for single-line text input.

    Args:
        position (tuple[int, int]): The top-left corner of the widget.
        size (tuple[int, int]): The (width, height) of the widget.
        label (str): A label to display next to the input box.
        initial_text (str, optional): The initial text in the box. Defaults to "".
        is_password (bool, optional): If True, the input text will be masked.
            Defaults to False.

    Attributes:
        image (pygame.Surface): The surface that represents the widget.
        rect (pygame.Rect): The rectangular area of the widget.
        text (str): The current text content of the input box.
    """

    image: pygame.Surface
    rect: pygame.Rect
    text: str

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        label: str,
        initial_text: str = "",
        is_password: bool = False,
    ):
        # TextInput doesn't have a single 'on_click' action, but it must
        # satisfy the Clickable interface. We provide a no-op lambda.
        # The super call initializes the pygame.sprite.Sprite via Clickable.
        super().__init__(on_click=lambda: None)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self._label = label
        self.text = initial_text
        self._active = False
        self._is_password = is_password

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = (220, 220, 220)  # Light Grey
        self._active_border_color = (0, 120, 215)  # Blue
        self._inactive_border_color = (128, 128, 128)  # Dark Grey
        self._padding = 5

        self._render()

    def handle_event(self, event: pygame.event.Event) -> None:  # Public method first
        """Handles user input events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self._active = not self._active
            else:
                self._active = False
        elif event.type == pygame.KEYDOWN and self._active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

        self._render()  # Calls the private _render method

    def _render(self) -> None:
        """Renders the text input box."""
        self.image.fill(self._background_color)

        # Draw border
        border_color = (
            self._active_border_color if self._active else self._inactive_border_color
        )
        pygame.draw.rect(self.image, border_color, self.image.get_rect(), 2)

        # Draw label to the left of the input box
        # We render it to a separate surface first to position it correctly.
        # This is a common technique for complex layouts.
        # The label is not a child component; it's part of this component's render.
        label_surface = self._font.render(self._label, True, self._font_color)
        label_rect = label_surface.get_rect(
            midleft=(
                -label_surface.get_width() - self._padding,
                self.image.get_height() // 2,
            )
        )
        self.image.blit(label_surface, label_rect)

        # Draw text
        display_text = self.text
        if self._is_password:
            display_text = "*" * len(self.text)

        text_surface = self._font.render(display_text, True, self._font_color)
        text_rect = text_surface.get_rect(
            midleft=(self._padding, self.image.get_height() // 2)
        )
        self.image.blit(text_surface, text_rect)

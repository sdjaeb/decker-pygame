"""This module defines a generic Button component."""

from collections.abc import Callable

import pygame

from decker_pygame.settings import (
    UI_BORDER,
    UI_BORDER_WIDTH,
    UI_FACE,
    UI_FACE_PRESSED,
    UI_FONT,
    UI_FONT_DISABLED,
)

from .base_widgets import Clickable


class Button(Clickable):
    """A clickable button widget that handles visual pressed/unpressed states.

    Args:
        position (tuple[int, int]): The top-left corner of the button.
        size (tuple[int, int]): The (width, height) of the button.
        text (str): The text to display on the button.
        on_click (Callable[[], None]): The function to call when clicked.
        is_transparent (bool): If True, the button will have no visible background
            or border. Defaults to False.
    """

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        text: str,
        on_click: Callable[[], None],
        is_transparent: bool = False,
    ):
        super().__init__(on_click)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)
        self.text = text
        self._is_pressed = False
        self._is_enabled = True
        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._is_transparent = is_transparent

        self._render()

    def set_enabled(self, enabled: bool) -> None:
        """Sets the button's enabled state and redraws it."""
        if self._is_enabled != enabled:
            self._is_enabled = enabled
            self._render()

    def _render(self) -> None:
        """Renders the button's surface based on its current state."""
        if not self._is_enabled:
            text_color = UI_FONT_DISABLED
        elif self._is_pressed:
            text_color = UI_FONT.light_font_color
        else:
            text_color = UI_FONT.dark_font_color
        bg_color = UI_FACE_PRESSED if self._is_pressed else UI_FACE

        # Use SRCALPHA to support transparency
        self.image.fill((0, 0, 0, 0))

        if not self._is_transparent:
            self.image.fill(bg_color)
            pygame.draw.rect(
                self.image, UI_BORDER, self.image.get_rect(), UI_BORDER_WIDTH
            )

        text_surface = self._font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles mouse click events with press and release states."""
        if not self._is_enabled:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._is_pressed = True
                self._render()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Only trigger the click if the mouse is released over the button
            if self.rect.collidepoint(event.pos) and self._is_pressed:
                self._on_click()

            # Always reset state on mouse up
            self._is_pressed = False
            self._render()

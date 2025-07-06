from collections.abc import Callable

import pygame

from decker_pygame.settings import UI_FACE, UI_FONT

from .base_widgets import Clickable


class Button(Clickable):
    """A clickable button widget that handles visual pressed/unpressed states."""

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        text: str,
        on_click: Callable[[], None],
    ):
        """Initialize the Button."""
        super().__init__(on_click=on_click)
        self.rect = pygame.Rect(position, size)
        self.text = text

        font = pygame.font.Font(UI_FONT.default_font_name, UI_FONT.default_font_size)

        # Unpressed state
        self._image_up = pygame.Surface(size)
        self._image_up.fill(UI_FACE)
        pygame.draw.rect(self._image_up, (0, 0, 0), self._image_up.get_rect(), 1)
        text_surf_up = font.render(text, True, UI_FONT.dark_font_color)
        text_rect_up = text_surf_up.get_rect(center=self._image_up.get_rect().center)
        self._image_up.blit(text_surf_up, text_rect_up)

        # Pressed state (inverted colors)
        self._image_down = pygame.Surface(size)
        self._image_down.fill(UI_FONT.dark_font_color)  # Inverted background
        pygame.draw.rect(self._image_down, (0, 0, 0), self._image_down.get_rect(), 1)
        text_surf_down = font.render(text, True, UI_FACE)  # Inverted font color
        text_rect_down = text_surf_down.get_rect(
            center=self._image_down.get_rect().center
        )
        self._image_down.blit(text_surf_down, text_rect_down)

        self.image = self._image_up
        self._is_pressed = False

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles mouse click events with press and release states."""
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

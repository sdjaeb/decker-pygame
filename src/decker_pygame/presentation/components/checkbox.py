"""This module defines a Checkbox component."""

from collections.abc import Callable

import pygame
from pygame.color import Color

from decker_pygame.presentation.components.base_widgets import Clickable
from decker_pygame.settings import PADDING, UI_BORDER, UI_FACE, UI_FONT, WHITE


class Checkbox(Clickable):
    """A checkbox widget that can be toggled on or off.

    Args:
        position (tuple[int, int]): The top-left corner of the checkbox.
        label (str): The text label to display next to the checkbox.
        on_toggle (Callable[[bool], None]): Callback when the state changes.
        name (str | None, optional): A stable identifier for testing. Defaults to the
            checkbox's label.
        initial_state (bool, optional): The initial checked state. Defaults to False.
        size (int, optional): The size of the checkbox square. Defaults to 16.
    """

    def __init__(
        self,
        position: tuple[int, int],
        label: str,
        on_toggle: Callable[[bool], None],
        *,
        name: str | None = None,
        initial_state: bool = False,
        size: int = 16,
    ):
        super().__init__(on_click=self._toggle_state)

        self.is_checked = initial_state
        self.on_toggle = on_toggle
        self._label = label
        self.name = name if name is not None else self._label
        self._size = size

        self._font = pygame.font.Font(None, UI_FONT.default_font_size)
        label_surface = self._font.render(self._label, True, WHITE)

        # The total width is the box, padding, and the label text.
        total_width = self._size + PADDING + label_surface.get_width()
        total_height = max(self._size, label_surface.get_height())

        self.image = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)

        self._box_rect = pygame.Rect(0, 0, self._size, self._size)
        self._label_rect = label_surface.get_rect(
            midleft=(self._size + PADDING, total_height // 2)
        )
        self.image.blit(label_surface, self._label_rect)

    def _toggle_state(self) -> None:
        """Toggles the checked state and calls the callback."""
        self.is_checked = not self.is_checked
        self.on_toggle(self.is_checked)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles mouse click events to toggle the checkbox state.

        Args:
            event (pygame.event.Event): The pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._on_click()

    def update(self) -> None:
        """Redraws the checkbox based on its current state."""
        # Clear only the box area to preserve the label text
        self.image.fill((0, 0, 0, 0), self._box_rect)

        # Draw the box
        pygame.draw.rect(self.image, UI_FACE, self._box_rect)
        pygame.draw.rect(self.image, UI_BORDER, self._box_rect, 1)

        # Draw the checkmark if checked
        if self.is_checked:
            lines = [
                ((3, self._size // 2), (self._size // 2 - 1, self._size - 4)),
                (
                    (self._size // 2 - 2, self._size - 4),
                    (self._size - 4, 4),
                ),
            ]
            for start, end in lines:
                pygame.draw.line(self.image, Color("black"), start, end, 2)

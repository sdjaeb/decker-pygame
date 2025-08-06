"""This module defines a Slider component."""

from collections.abc import Callable

import pygame

from decker_pygame.presentation.components.base_widgets import Clickable
from decker_pygame.settings import UI_BORDER, UI_FACE, UI_FACE_PRESSED


class Slider(Clickable):
    """A slider widget for selecting a value within a range.

    Args:
        position (tuple[int, int]): The top-left corner of the slider.
        size (tuple[int, int]): The (width, height) of the slider track.
        min_val (float): The minimum value of the slider.
        max_val (float): The maximum value of the slider.
        initial_val (float): The initial value of the slider.
        on_change (Callable[[float], None]): Callback when the value changes.
    """

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        min_val: float,
        max_val: float,
        initial_val: float,
        on_change: Callable[[float], None],
    ):
        super().__init__(on_click=lambda: None)  # Clickable, but no single action

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)

        self._min_val = min_val
        self._max_val = max_val
        self.value = initial_val
        self.on_change = on_change

        self._dragging = False
        self._handle_width = 10
        self._handle_rect = pygame.Rect(0, 0, self._handle_width, self.rect.height)

    def _update_value_from_pos(self, x_pos: int) -> None:
        """Updates the slider's value based on the handle's x-position."""
        # Clamp position to be within the slider's track
        clamped_x = max(0, min(x_pos, self.rect.width - self._handle_width))

        # Calculate the value as a percentage of the track width
        value_range = self._max_val - self._min_val
        pos_as_pct = clamped_x / (self.rect.width - self._handle_width)
        new_value = self._min_val + (pos_as_pct * value_range)

        if new_value != self.value:
            self.value = new_value
            self.on_change(self.value)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles mouse events to control the slider.

        Args:
            event (pygame.event.Event): The pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._dragging = True
                # Immediately jump to the clicked position
                self._update_value_from_pos(event.pos[0] - self.rect.x)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self._dragging:
                self._update_value_from_pos(event.pos[0] - self.rect.x)

    def update(self) -> None:
        """Redraws the slider track and handle based on the current value."""
        # Draw the track
        self.image.fill(UI_FACE)
        pygame.draw.rect(self.image, UI_BORDER, self.image.get_rect(), 1)

        # Calculate handle position
        value_range = self._max_val - self._min_val
        if value_range == 0:
            pos_as_pct = 0.0
        else:
            pos_as_pct = (self.value - self._min_val) / value_range

        handle_x = pos_as_pct * (self.rect.width - self._handle_width)
        self._handle_rect.x = handle_x

        # Draw the handle
        handle_color = UI_FACE_PRESSED if self._dragging else UI_BORDER
        pygame.draw.rect(self.image, handle_color, self._handle_rect)

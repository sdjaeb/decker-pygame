"""This module defines a reusable ListView component."""

from collections.abc import Callable
from typing import Any

import pygame

from decker_pygame.settings import (
    UI_BORDER,
    UI_FACE,
    UI_FACE_PRESSED,
    UI_FONT,
    WHITE,
)

from .base_widgets import Clickable


class ListView(Clickable):
    """A widget for displaying a list of items in columns and handling selection."""

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        columns: list[tuple[str, int]],  # List of (header_text, width)
        on_selection_change: Callable[[Any | None], None],
    ):
        # The on_click is a dummy here; selection logic is more complex.
        super().__init__(on_click=lambda: None)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self._columns = columns
        self._on_selection_change = on_selection_change

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._line_height = self._font.get_linesize()
        self._padding = 5

        self._items: list[Any] = []
        self._item_rects: list[pygame.Rect] = []
        self._selected_index: int | None = None

    def set_items(
        self, items: list[Any], item_renderer: Callable[[Any], list[str]]
    ) -> None:
        """Sets the items to display in the list.

        Args:
            items (list[Any]): A list of data objects.
            item_renderer (Callable[[Any], list[str]]): A function that takes a data
                object and returns a list of strings, one for each column.
        """
        self._items = items
        self._item_renderer = item_renderer
        self._selected_index = None
        self._on_selection_change(None)
        self._render()

    def _render(self) -> None:
        """Renders the list view's surface."""
        self.image.fill(UI_FACE)
        pygame.draw.rect(self.image, UI_BORDER, self.image.get_rect(), 1)
        self._item_rects.clear()

        # Draw headers
        x_offset = self._padding
        y_offset = self._padding
        for header, width in self._columns:
            header_surface = self._font.render(header, True, WHITE)
            self.image.blit(header_surface, (x_offset, y_offset))
            x_offset += width

        y_offset += self._line_height

        # Draw items
        for i, item in enumerate(self._items):
            item_row_rect = pygame.Rect(0, y_offset, self.rect.width, self._line_height)
            self._item_rects.append(item_row_rect)

            if i == self._selected_index:
                pygame.draw.rect(self.image, UI_FACE_PRESSED, item_row_rect)

            rendered_cols = self._item_renderer(item)
            x_offset = self._padding
            for j, col_text in enumerate(rendered_cols):
                _, col_width = self._columns[j]
                text_surface = self._font.render(col_text, True, WHITE)
                self.image.blit(text_surface, (x_offset, y_offset))
                x_offset += col_width

            y_offset += self._line_height

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles mouse clicks to select items."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                # Translate mouse position to be relative to the list view
                local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
                new_selection = None
                for i, item_rect in enumerate(self._item_rects):
                    if item_rect.collidepoint(local_pos):
                        new_selection = i
                        break

                if self._selected_index != new_selection:
                    self._selected_index = new_selection
                    selected_item_data = (
                        self._items[self._selected_index]
                        if self._selected_index is not None
                        else None
                    )
                    self._on_selection_change(selected_item_data)
                    self._render()

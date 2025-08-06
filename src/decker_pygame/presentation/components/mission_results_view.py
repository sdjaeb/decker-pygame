"""This module defines the MissionResultsView component."""

from collections.abc import Callable

import pygame

from decker_pygame.application.dtos import MissionResultsDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class MissionResultsView(pygame.sprite.Sprite):
    """A UI component that displays the results of a completed mission.

    Ported from MissionResultsDlg.cpp/h.

    Args:
        data (MissionResultsDTO): The data to display.
        on_close (Callable[[], None]): Callback for when the user closes the view.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(self, data: MissionResultsDTO, on_close: Callable[[], None]):
        super().__init__()
        self._data = data
        self._on_close = on_close

        self.image = pygame.Surface((400, 250))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = UI_FACE
        self._padding = 20
        self._line_height = self._font.get_linesize()

        self._components = pygame.sprite.Group()
        self._create_widgets()
        self._render()

    def _create_widgets(self) -> None:
        """Creates the UI widgets for the view."""
        close_button = Button(
            position=(self.image.get_width() // 2 - 50, self.image.get_height() - 60),
            size=(100, 40),
            text="Continue",
            on_click=self._on_close,
        )
        self._components.add(close_button)

    def _render(self) -> None:
        """Renders the view's static elements and widgets."""
        self.image.fill(self._background_color)

        title_text = "Mission Results"
        title_surface = self._font.render(title_text, True, self._font_color)
        title_rect = title_surface.get_rect(
            centerx=self.image.get_width() // 2, y=self._padding
        )
        self.image.blit(title_surface, title_rect)

        y_offset = title_rect.bottom + self._padding * 2

        status_text = "Success" if self._data.was_successful else "Failure"
        lines = [
            f"Contract: {self._data.contract_name}",
            f"Status: {status_text}",
            f"Credits Earned: ${self._data.credits_earned}",
            f"Reputation Change: {self._data.reputation_change:+}",
        ]

        for line in lines:
            text_surface = self._font.render(line, True, self._font_color)
            text_rect = text_surface.get_rect(left=self._padding * 2, y=y_offset)
            self.image.blit(text_surface, text_rect)
            y_offset += self._line_height

        self._components.draw(self.image)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles events passed from the input handler."""
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
            new_event = pygame.event.Event(
                event.type, button=event.button, pos=local_pos
            )
            for component in self._components:
                if isinstance(component, Clickable):
                    component.handle_event(new_event)

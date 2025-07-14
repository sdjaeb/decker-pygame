"""This module defines the RestView component."""

from collections.abc import Callable

import pygame

from decker_pygame.application.dtos import RestViewData
from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class RestView(pygame.sprite.Sprite):
    """A UI component that allows the player to rest and heal.

    Ported from RestDlg.cpp/h.

    Args:
        data (RestViewData): The data to display.
        on_rest (Callable[[], None]): Callback for when the user rests.
        on_close (Callable[[], None]): Callback for when the user closes the view.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        data: RestViewData,
        on_rest: Callable[[], None],
        on_close: Callable[[], None],
    ):
        super().__init__()
        self._data = data
        self._on_rest = on_rest
        self._on_close = on_close

        self.image = pygame.Surface((350, 200))
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
        button_y = self.image.get_height() - 60

        rest_button = Button(
            position=(self._padding, button_y),
            size=(100, 40),
            text="Rest",
            on_click=self._on_rest,
        )
        self._components.add(rest_button)

        cancel_button = Button(
            position=(self.image.get_width() - 100 - self._padding, button_y),
            size=(100, 40),
            text="Cancel",
            on_click=self._on_close,
        )
        self._components.add(cancel_button)

    def _render(self) -> None:
        """Renders the view's static elements and widgets."""
        self.image.fill(self._background_color)

        title_text = "Rest & Recover"
        title_surface = self._font.render(title_text, True, self._font_color)
        title_rect = title_surface.get_rect(
            centerx=self.image.get_width() // 2, y=self._padding
        )
        self.image.blit(title_surface, title_rect)

        y_offset = title_rect.bottom + self._padding
        lines = [
            f"Cost to rest: ${self._data.cost}",
            f"Health recovered: {self._data.health_recovered}%",
        ]
        for line in lines:
            text_surface = self._font.render(line, True, self._font_color)
            text_rect = text_surface.get_rect(
                centerx=self.image.get_width() // 2, y=y_offset
            )
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

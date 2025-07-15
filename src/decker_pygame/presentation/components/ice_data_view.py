"""This module defines the IceDataView component."""

from collections.abc import Callable

import pygame

from decker_pygame.application.dtos import IceDataViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class IceDataView(pygame.sprite.Sprite):
    """A UI component for displaying detailed information about an ICE program.

    Args:
        data (IceDataViewDTO): The data required to render the view.
        on_close (Callable[[], None]): A callback for when the view is closed.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        data: IceDataViewDTO,
        on_close: Callable[[], None],
    ) -> None:
        super().__init__()
        self._data = data
        self._on_close = on_close

        self.image = pygame.Surface((400, 300))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = UI_FACE
        self._line_height = self._font.get_linesize()
        self._padding = 10

        self._components = pygame.sprite.Group()
        self._close_button = Button(
            position=(self.image.get_width() - 90, self.image.get_height() - 40),
            size=(80, 30),
            text="Close",
            on_click=self._on_close,
        )
        self._components.add(self._close_button)

        self._render_data()

    def _render_data(self) -> None:
        """Renders the ICE data onto the view's surface."""
        self.image.fill(self._background_color)

        title_surface = self._font.render(self._data.name, True, self._font_color)
        title_rect = title_surface.get_rect(
            centerx=self.image.get_width() // 2, y=self._padding
        )
        self.image.blit(title_surface, title_rect)

        y_offset = title_rect.bottom + self._padding * 2
        data_lines = [
            f"Type: {self._data.ice_type}",
            f"Strength: {self._data.strength}",
            f"Cost: ${self._data.cost}",
            f"Description: {self._data.description}",
        ]
        for line in data_lines:
            line_surface = self._font.render(line, True, self._font_color)
            self.image.blit(line_surface, (self._padding, y_offset))
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

from collections.abc import Callable

import pygame

from decker_pygame.application.deck_service import DeckViewData
from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class DeckView(pygame.sprite.Sprite):
    """A UI component that displays the player's deck of programs."""

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        data: DeckViewData,
        on_close: Callable[[], None],
        on_order: Callable[[], None],
    ) -> None:
        super().__init__()
        self._data = data
        self._on_close = on_close
        self._on_order = on_order

        self.image = pygame.Surface((400, 450))
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
        self._order_button = Button(
            position=(self.image.get_width() - 180, self.image.get_height() - 40),
            size=(80, 30),
            text="Order",
            on_click=self._on_order,
        )
        self._components.add(self._close_button, self._order_button)

        self._render_data()

    def _render_data(self) -> None:
        """Renders the deck data onto the view's surface."""
        self.image.fill(self._background_color)

        title_text = (
            f"Deck Memory: {self._data.used_deck_size} / {self._data.total_deck_size}"
        )
        title_surface = self._font.render(title_text, True, self._font_color)
        self.image.blit(title_surface, (self._padding, self._padding))

        y_offset = self._padding + self._line_height * 2
        for program in self._data.programs:
            program_text = f"- {program.name} ({program.size}MB)"
            program_surface = self._font.render(program_text, True, self._font_color)
            self.image.blit(program_surface, (self._padding, y_offset))
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

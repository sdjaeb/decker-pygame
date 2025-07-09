from collections.abc import Callable
from functools import partial

import pygame

from decker_pygame.application.deck_service import DeckViewData
from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class OrderView(pygame.sprite.Sprite):
    """A UI component for re-ordering items."""

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]
    _up_buttons: dict[str, Button]
    _down_buttons: dict[str, Button]

    def __init__(
        self,
        data: DeckViewData,
        on_close: Callable[[], None],
        on_move_up: Callable[[str], None],
        on_move_down: Callable[[str], None],
    ) -> None:
        super().__init__()
        self._data = data
        self._on_close = on_close
        self._on_move_up = on_move_up
        self._on_move_down = on_move_down

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
        self._components.add(self._close_button)

        self._up_buttons = {}
        self._down_buttons = {}
        y_offset = self._padding
        button_size = (50, 20)
        num_programs = len(self._data.programs)

        for i, program in enumerate(self._data.programs):
            program_text = f"{i + 1}. {program.name}"
            program_surface = self._font.render(program_text, True, self._font_color)
            self.image.blit(program_surface, (self._padding, y_offset))

            button_x = self.image.get_width() - button_size[0] * 2 - self._padding * 3

            # Add "Up" button if not the first item
            if i > 0:
                up_button = Button(
                    (button_x, y_offset - 2),
                    button_size,
                    "Up",
                    partial(self._on_move_up, program.name),
                )
                self._components.add(up_button)
                self._up_buttons[program.name] = up_button

            button_x += button_size[0] + self._padding

            # Add "Down" button if not the last item
            if i < num_programs - 1:
                down_button = Button(
                    (button_x, y_offset - 2),
                    button_size,
                    "Down",
                    partial(self._on_move_down, program.name),
                )
                self._components.add(down_button)
                self._down_buttons[program.name] = down_button

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

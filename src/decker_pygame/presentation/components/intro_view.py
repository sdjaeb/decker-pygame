"""This module defines the IntroView component."""

from collections.abc import Callable

import pygame

from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class IntroView(pygame.sprite.Sprite):
    """A UI component that displays the game's introduction.

    Ported from IntroDlg.cpp/h.

    Args:
        on_continue (Callable[[], None]): Callback for when the user continues.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(self, on_continue: Callable[[], None]):
        super().__init__()
        self._on_continue = on_continue

        self.image = pygame.Surface((500, 300))
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
        continue_button = Button(
            position=(self.image.get_width() // 2 - 50, self.image.get_height() - 60),
            size=(100, 40),
            text="Continue",
            on_click=self._on_continue,
        )
        self._components.add(continue_button)

    def _render(self) -> None:
        """Renders the view's static elements and widgets."""
        self.image.fill(self._background_color)

        intro_text = (
            "Welcome to Decker.\n\n"
            "The year is 2072.\n"
            "Megacorporations rule the world from their arcologies,\n"
            "casting long shadows over the sprawling urban landscapes.\n\n"
            "You are a decker, a ghost in the machine.\n"
            "Your currency is data, your weapon is code.\n\n"
            "Your story begins now."
        )

        y_offset = self._padding
        for line in intro_text.splitlines():
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

"""This module defines the NewCharView component."""

from collections.abc import Callable

import pygame

from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.text_input import TextInput
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class NewCharView(pygame.sprite.Sprite):
    """A UI component for creating a new character.

    Ported from NewCharDlg.cpp/h and NameDlg.cpp/h.

    Args:
        on_create (Callable[[str], None]): Callback for when the user creates a
            character, passing the chosen name.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(self, on_create: Callable[[str], None]):
        super().__init__()
        self._on_create = on_create

        self.image = pygame.Surface((400, 200))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = UI_FACE
        self._padding = 20

        self._components = pygame.sprite.Group()
        self._create_widgets()
        self._render()

    def _handle_create_click(self) -> None:
        """Handles the create button click."""
        name = self._name_input.text
        if name:
            self._on_create(name)

    def _create_widgets(self) -> None:
        """Creates the UI widgets for the view."""
        self._name_input = TextInput((120, 80), (220, 30), "Character Name:", "Decker")
        self._components.add(self._name_input)

        create_button = Button(
            (self.image.get_width() // 2 - 50, 140),
            (100, 40),
            "Create",
            self._handle_create_click,
        )
        self._components.add(create_button)

    def _render(self) -> None:
        """Renders the view's static elements and widgets."""
        self.image.fill(self._background_color)
        title_surface = self._font.render(
            "Create New Character", True, self._font_color
        )
        title_rect = title_surface.get_rect(
            centerx=self.image.get_width() // 2, y=self._padding
        )
        self.image.blit(title_surface, title_rect)
        self._components.draw(self.image)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles events passed from the input handler."""
        local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
        new_event = pygame.event.Event(event.type, **{**event.dict, "pos": local_pos})
        for component in self._components:
            if isinstance(component, Clickable):
                component.handle_event(new_event)

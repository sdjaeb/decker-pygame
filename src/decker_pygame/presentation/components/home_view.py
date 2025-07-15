"""This module defines the HomeView component."""

from collections.abc import Callable

import pygame

from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class HomeView(pygame.sprite.Sprite):
    """A UI component that serves as the main dashboard.

    Ported from HomeView.cpp/h.

    Args:
        on_char (Callable[[], None]): Callback for viewing character data.
        on_deck (Callable[[], None]): Callback for viewing the deck.
        on_contracts (Callable[[], None]): Callback for viewing contracts.
        on_build (Callable[[], None]): Callback for opening the build view.
        on_shop (Callable[[], None]): Callback for opening the shop view.
        on_transfer (Callable[[], None]): Callback for opening the transfer view.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        on_char: Callable[[], None],
        on_deck: Callable[[], None],
        on_contracts: Callable[[], None],
        on_build: Callable[[], None],
        on_shop: Callable[[], None],
        on_transfer: Callable[[], None],
    ):
        super().__init__()
        self._on_char = on_char
        self._on_deck = on_deck
        self._on_contracts = on_contracts
        self._on_build = on_build
        self._on_shop = on_shop
        self._on_transfer = on_transfer

        self.image = pygame.Surface((200, 300))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = UI_FACE
        self._padding = 10

        self._components = pygame.sprite.Group()
        self._create_buttons()
        self._render()

    def _create_buttons(self) -> None:
        """Creates the UI buttons for the view."""
        button_width = 180
        button_height = 40
        y_offset = self._padding * 2 + self._font.get_linesize()
        button_actions = [
            ("Character", self._on_char),
            ("Deck", self._on_deck),
            ("Contracts", self._on_contracts),
            ("Build", self._on_build),
            ("Shop", self._on_shop),
            ("Transfer", self._on_transfer),
        ]

        for text, action in button_actions:
            button = Button(
                ((self.image.get_width() - button_width) // 2, y_offset),
                (button_width, button_height),
                text,
                action,
            )
            self._components.add(button)
            y_offset += button_height + self._padding

    def _render(self) -> None:
        """Renders the view's static elements and buttons."""
        self.image.fill(self._background_color)

        title_surface = self._font.render("Main Menu", True, self._font_color)
        title_rect = title_surface.get_rect(
            centerx=self.image.get_width() // 2, y=self._padding
        )
        self.image.blit(title_surface, title_rect)

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

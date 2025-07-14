"""This module defines the ShopView component for displaying shop items."""

from collections.abc import Callable
from functools import partial

import pygame

from decker_pygame.application.dtos import ShopViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class ShopView(pygame.sprite.Sprite):
    """A UI component for displaying and interacting with a shop's inventory.

    Args:
        data (ShopViewDTO): The data required to render the view.
        on_close (Callable[[], None]): A callback for when the view is closed.
        on_purchase (Callable[[str], None]): A callback for when an item is purchased.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        data: ShopViewDTO,
        on_close: Callable[[], None],
        on_purchase: Callable[[str], None],
    ) -> None:
        super().__init__()
        self._data = data
        self._on_close = on_close
        self._on_purchase = on_purchase

        self.image = pygame.Surface((500, 450))
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
        """Renders the shop data onto the view's surface."""
        self.image.fill(self._background_color)

        # Render title
        title_surface = self._font.render(self._data.shop_name, True, self._font_color)
        title_rect = title_surface.get_rect(
            centerx=self.image.get_width() // 2, y=self._padding
        )
        self.image.blit(title_surface, title_rect)

        # Render items
        y_offset = title_rect.bottom + self._padding * 2
        button_size = (60, 20)
        for item in self._data.items:
            # Render item name and cost
            item_text = f"{item.name} - ${item.cost}"
            item_surface = self._font.render(item_text, True, self._font_color)
            self.image.blit(item_surface, (self._padding, y_offset))

            # Render description below name
            desc_surface = self._font.render(
                f"  {item.description}", True, self._font_color
            )
            self.image.blit(desc_surface, (self._padding, y_offset + self._line_height))

            # Add "Buy" button
            button_x = self.image.get_width() - button_size[0] - self._padding
            buy_button = Button(
                (button_x, y_offset),
                button_size,
                "Buy",
                partial(self._on_purchase, item.name),
            )
            self._components.add(buy_button)

            y_offset += self._line_height * 2 + self._padding

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

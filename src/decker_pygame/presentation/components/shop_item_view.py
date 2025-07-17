"""Define the ShopItemView component for displaying detailed item information."""

from collections.abc import Callable

import pygame

from decker_pygame.application.dtos import ShopItemViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class ShopItemView(pygame.sprite.Sprite):
    """A UI component for displaying detailed information about a shop item.

    Args:
        data (ShopItemViewDTO): The data required to render the view.
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
        data: ShopItemViewDTO,
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
        """Renders the shop item data onto the view's surface."""
        self.image.fill(self._background_color)

        # Render item name
        title_surface = self._font.render(self._data.name, True, self._font_color)
        title_rect = title_surface.get_rect(
            centerx=self.image.get_width() // 2, y=self._padding
        )
        self.image.blit(title_surface, title_rect)

        # Render item details
        y_offset = title_rect.bottom + self._padding * 2
        details = [
            f"Cost: ${self._data.cost}",
            f"Type: {self._data.item_type.value}",  # Assuming item_type is an enum
            f"Description: {self._data.description}",
        ] + [f"{k}: {v}" for k, v in self._data.other_stats.items()]

        for detail in details:
            detail_surface = self._font.render(detail, True, self._font_color)
            self.image.blit(detail_surface, (self._padding, y_offset))
            y_offset += self._line_height + self._padding

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

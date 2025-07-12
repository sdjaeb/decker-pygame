"""This module defines the ContractDataView component."""

import pygame

from decker_pygame.settings import UI_FACE, UI_FONT


class ContractDataView(pygame.sprite.Sprite):
    """A UI component that displays contract data.

    Ported from ContractDataDialog.cpp/h.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        contract_name: str,
    ):
        """Initialize the ContractDataView."""
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self._contract_name = contract_name

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = UI_FACE
        self._padding = 10

        self._render_data()

    def _render_data(self) -> None:
        """Renders the contract data onto the view's surface."""
        self.image.fill(self._background_color)

        text = f"Contract: {self._contract_name}"
        text_surface = self._font.render(text, True, self._font_color)
        text_rect = text_surface.get_rect(topleft=(self._padding, self._padding))

        self.image.blit(text_surface, text_rect)

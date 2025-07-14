"""This module defines the BuildView component for the crafting UI."""

from collections.abc import Callable

import pygame

from decker_pygame.domain.crafting import Schematic
from decker_pygame.settings import UI_FACE, UI_FONT


class BuildView(pygame.sprite.Sprite):
    """A UI component that displays a list of craftable schematics.

    user interaction for crafting items. Ported from BuildDialog.cpp/h.

    Args:
        position (tuple[int, int]): The top-left corner of the view.
        size (tuple[int, int]): The (width, height) of the view.
        schematics (list[Schematic]): The list of schematics to display.
        on_build_click (Callable[[str], None]): Callback when a build item is
            clicked.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        schematics: list[Schematic],
        on_build_click: Callable[[str], None],
    ):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self._schematics = schematics
        self._on_build_click = on_build_click

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = UI_FACE
        self._line_height = self._font.get_linesize()
        self._padding = 10

        self._schematic_rects: list[pygame.Rect] = []
        self._render_schematics()

    def _render_schematics(self) -> None:
        """Renders the list of schematics onto the view's surface."""
        self.image.fill(self._background_color)
        self._schematic_rects.clear()

        y_offset = self._padding
        for schematic in self._schematics:
            text = f"Build: {schematic.name} (Cost: {schematic.cost[0].quantity}cr)"
            text_surface = self._font.render(text, True, self._font_color)
            text_rect = text_surface.get_rect(topleft=(self._padding, y_offset))

            self.image.blit(text_surface, text_rect)
            self._schematic_rects.append(text_rect)
            y_offset += self._line_height

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles user input events, specifically mouse clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
            for i, schematic_rect in enumerate(self._schematic_rects):
                if schematic_rect.collidepoint(local_pos):
                    self._on_build_click(self._schematics[i].name)
                    break

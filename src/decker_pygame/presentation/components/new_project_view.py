"""This module defines the NewProjectView component."""

from collections.abc import Callable
from typing import Optional

import pygame

from decker_pygame.application.dtos import NewProjectViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.text_input import TextInput
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT

from .base_widgets import Clickable


class NewProjectView(pygame.sprite.Sprite):
    """A UI component for starting a new research project."""

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        data: NewProjectViewDTO,
        on_start: Callable[[str, str, int], None],
        on_close: Callable[[], None],
    ):
        super().__init__()
        self._data = data
        self._on_start = on_start
        self._on_close = on_close

        self.image = pygame.Surface((500, 400))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = UI_FACE
        self._padding = 20

        # State
        self._active_tab: str = "software"
        self._selected_item: Optional[str] = None
        self._item_rects: list[pygame.Rect] = []

        self._components = pygame.sprite.Group[pygame.sprite.Sprite]()
        self._create_widgets()
        self._render()

    def _create_widgets(self) -> None:
        # Tabs
        self._software_tab_button = Button(
            (self._padding, 50),
            (100, 30),
            "Software",
            lambda: self._set_active_tab("software"),
        )
        self._chip_tab_button = Button(
            (self._padding + 110, 50),
            (100, 30),
            "Chips",
            lambda: self._set_active_tab("chip"),
        )
        self._components.add(self._software_tab_button, self._chip_tab_button)

        # Rating Input
        self._rating_input = TextInput((300, 200), (150, 30), "Rating:", "1")
        self._components.add(self._rating_input)

        # Action Buttons
        start_button = Button(
            (self.image.get_width() - 220, self.image.get_height() - 60),
            (100, 40),
            "Start",
            self._handle_start_click,
        )
        cancel_button = Button(
            (self.image.get_width() - 110, self.image.get_height() - 60),
            (100, 40),
            "Cancel",
            self._on_close,
        )
        self._components.add(start_button, cancel_button)

    def _set_active_tab(self, tab_name: str) -> None:
        self._active_tab = tab_name
        self._selected_item = None
        self._render()

    def _handle_start_click(self) -> None:
        if not self._selected_item:
            return
        try:
            rating = int(self._rating_input.text)
            if rating > 0:
                self._on_start(self._active_tab, self._selected_item, rating)
        except (ValueError, TypeError):
            # Ignore if rating is not a valid integer
            pass

    def _render(self) -> None:
        self.image.fill(self._background_color)

        # Title
        title_surface = self._font.render(
            "Start New Research Project", True, self._font_color
        )
        title_rect = title_surface.get_rect(
            centerx=self.image.get_width() // 2, y=self._padding
        )
        self.image.blit(title_surface, title_rect)

        # Skill display
        skill_text = ""
        if self._active_tab == "software":
            skill_text = f"Programming Skill: {self._data.programming_skill}"
        else:
            skill_text = f"Chip Design Skill: {self._data.chip_design_skill}"

        skill_surface = self._font.render(skill_text, True, self._font_color)
        skill_rect = skill_surface.get_rect(topleft=(300, 100))
        self.image.blit(skill_surface, skill_rect)

        # Render item list and components
        self._render_item_list()
        self._components.draw(self.image)

    def _render_item_list(self) -> None:
        list_area = pygame.Rect(self._padding, 90, 250, self.image.get_height() - 160)
        pygame.draw.rect(self.image, (200, 200, 200), list_area)  # List background
        pygame.draw.rect(self.image, (0, 0, 0), list_area, 1)  # List border

        items_to_display = (
            self._data.available_software
            if self._active_tab == "software"
            else self._data.available_chips
        )

        self._item_rects.clear()
        y_offset = list_area.y + 5
        for item in items_to_display:
            color = (0, 0, 200) if item == self._selected_item else self._font_color
            item_surface = self._font.render(item, True, color)
            item_rect = item_surface.get_rect(topleft=(list_area.x + 5, y_offset))
            self.image.blit(item_surface, item_rect)
            self._item_rects.append(item_rect)
            y_offset += self._font.get_linesize()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles user input events for the view.

        This method processes clicks on the item list to select an item for
        research. It also translates mouse coordinates and forwards events to
        its child components (buttons, text input).

        Args:
            event (pygame.event.Event): The pygame event to process.
        """
        local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            items_to_display = (
                self._data.available_software
                if self._active_tab == "software"
                else self._data.available_chips
            )
            for i, item_rect in enumerate(self._item_rects):
                if item_rect.collidepoint(local_pos):
                    self._selected_item = items_to_display[i]
                    self._render()

        new_event = pygame.event.Event(event.type, **{**event.dict, "pos": local_pos})
        for component in self._components:
            if isinstance(component, Clickable):
                component.handle_event(new_event)

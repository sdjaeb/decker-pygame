"""This module defines the ProjectDataView component."""

from collections.abc import Callable

import pygame

from decker_pygame.application.dtos import ProjectDataViewDTO, SourceCodeDTO
from decker_pygame.presentation.components.base_widgets import Clickable
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.label import Label
from decker_pygame.presentation.components.list_view import ListView
from decker_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, UI_FACE, UI_FONT


class ProjectDataView(pygame.sprite.Sprite):
    """A UI component for managing R&D projects. Ported from ProjectDataDlg.cpp/h."""

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]
    _build_button: Button
    _trash_button: Button
    _source_list: ListView

    def __init__(
        self,
        data: ProjectDataViewDTO,
        on_close: Callable[[], None],
        on_new_project: Callable[[], None],
        on_work_day: Callable[[], None],
        on_work_week: Callable[[], None],
        on_finish_project: Callable[[], None],
        on_build: Callable[[str], None],
        on_trash: Callable[[str], None],
    ):
        super().__init__()
        self._data = data
        self.image = pygame.Surface((600, 400))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = UI_FACE
        self._padding = 10

        self._selected_source_code: SourceCodeDTO | None = None
        self._components = pygame.sprite.Group()
        self._create_widgets(
            on_close,
            on_new_project,
            on_work_day,
            on_work_week,
            on_finish_project,
            on_build,
            on_trash,
        )
        self._render()

    def _handle_selection_change(self, item: SourceCodeDTO | None) -> None:
        """Callback for when the list view selection changes."""
        self._selected_source_code = item
        can_build_or_trash = self._selected_source_code is not None
        self._build_button.set_enabled(can_build_or_trash)
        self._trash_button.set_enabled(can_build_or_trash)

    def _create_widgets(
        self,
        on_close: Callable[[], None],
        on_new: Callable[[], None],
        on_work_day: Callable[[], None],
        on_work_week: Callable[[], None],
        on_finish: Callable[[], None],
        on_build: Callable[[str], None],
        on_trash: Callable[[str], None],
    ) -> None:
        # --- Labels ---
        labels_data = [
            (f"Date: {self._data.date}", (self._padding, 10)),
            (f"Project: {self._data.project_type}", (self._padding, 30)),
            (f"Time Left: {self._data.project_time_left}", (self._padding, 50)),
            (f"Chip Burning: {self._data.chip_type}", (self._padding, 80)),
            (f"Time Left: {self._data.chip_time_left}", (self._padding, 100)),
        ]
        for text, pos in labels_data:
            label = Label(text, pos, font=self._font, color=self._font_color)
            self._components.add(label)

        # --- Buttons ---
        list_pos = (self._padding, 140)
        list_size = (400, 240)
        button_x = list_pos[0] + list_size[0] + self._padding
        button_w = 150
        button_h = 30
        button_y = list_pos[1]

        new_button = Button(
            (button_x, button_y), (button_w, button_h), "New Project", on_new
        )
        new_button.set_enabled(self._data.can_start_new_project)
        self._components.add(new_button)
        button_y += button_h + self._padding

        work_day_button = Button(
            (button_x, button_y), (button_w, button_h), "Work Day", on_work_day
        )
        work_day_button.set_enabled(self._data.can_work_on_project)
        self._components.add(work_day_button)
        button_y += button_h + self._padding

        work_week_button = Button(
            (button_x, button_y), (button_w, button_h), "Work Week", on_work_week
        )
        work_week_button.set_enabled(self._data.can_work_on_project)
        self._components.add(work_week_button)
        button_y += button_h + self._padding

        finish_button = Button(
            (button_x, button_y), (button_w, button_h), "Finish", on_finish
        )
        finish_button.set_enabled(self._data.can_work_on_project)
        self._components.add(finish_button)
        button_y += button_h + self._padding

        self._build_button = Button(
            (button_x, button_y),
            (button_w, button_h),
            "Build",
            lambda: on_build(self._selected_source_code.id)
            if self._selected_source_code
            else None,
        )
        self._build_button.set_enabled(False)  # Disabled until selection
        self._components.add(self._build_button)
        button_y += button_h + self._padding

        self._trash_button = Button(
            (button_x, button_y),
            (button_w, button_h),
            "Trash",
            lambda: on_trash(self._selected_source_code.id)
            if self._selected_source_code
            else None,
        )
        self._trash_button.set_enabled(False)  # Disabled until selection
        self._components.add(self._trash_button)

        close_button = Button(
            (button_x, self.image.get_height() - button_h - self._padding),
            (button_w, button_h),
            "Close",
            on_close,
        )
        self._components.add(close_button)

        # --- Source Code List ---
        columns = [("Type", 250), ("Rating", 75), ("Current", 75)]
        self._source_list = ListView(
            list_pos, list_size, columns, self._handle_selection_change
        )
        self._components.add(self._source_list)

        # Populate the list last, after all other widgets are created
        self._source_list.set_items(
            self._data.source_codes,
            lambda item: [item.type, str(item.rating), item.current_rating],
        )

    def _render(self) -> None:
        """Renders the view's surface."""
        self.image.fill(self._background_color)
        self._components.draw(self.image)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles mouse events and delegates them to child components."""
        if event.type in (
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEMOTION,
        ):
            local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
            new_event = pygame.event.Event(
                event.type, **{**event.dict, "pos": local_pos}
            )
            for component in self._components:
                if isinstance(component, Clickable):
                    component.handle_event(new_event)

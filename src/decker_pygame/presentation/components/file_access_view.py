"""This module defines the FileAccessView component."""

import functools
from collections.abc import Callable

import pygame

from decker_pygame.application.dtos import FileAccessViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.label import Label
from decker_pygame.settings import (
    BUTTON_HEIGHT,
    BUTTON_WIDTH,
    PADDING,
    UI_BORDER,
    UI_BORDER_WIDTH,
    UI_FACE,
    UI_FONT,
    WHITE,
)

from .base_widgets import Clickable


class FileAccessView(pygame.sprite.Sprite):
    """A view for interacting with files on a network node."""

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        data: FileAccessViewDTO,
        on_close: Callable[[], None],
        on_download: Callable[[str], None],
        on_delete: Callable[[str], None],
        position: tuple[int, int] = (100, 100),
        size: tuple[int, int] = (600, 400),
    ):
        super().__init__()
        self.data = data
        self.on_close = on_close
        self.on_download = on_download
        self.on_delete = on_delete

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)

        self._font = pygame.font.Font(None, UI_FONT.default_font_size)
        self._components = pygame.sprite.Group()

        self._create_layout()

    def _create_layout(self) -> None:
        # Background and border
        self.image.fill(UI_FACE)
        pygame.draw.rect(self.image, UI_BORDER, self.image.get_rect(), UI_BORDER_WIDTH)

        # Title
        title = Label(
            f"Accessing: {self.data.node_name}",
            (PADDING, PADDING),
            font=self._font,
            color=WHITE,
        )
        self._components.add(title)

        # Headers
        y_offset = title.rect.bottom + PADDING * 2
        headers = ["File Name", "Size (KB)", "Type", "Actions"]
        x_positions = [PADDING, 250, 350, 450]
        for i, header_text in enumerate(headers):
            header_label = Label(
                header_text,
                (x_positions[i], y_offset),
                font=self._font,
                color=WHITE,
            )
            self._components.add(header_label)

        y_offset += self._font.get_linesize() + PADDING

        # File list
        for file_dto in self.data.files:
            # File details
            name_label = Label(
                file_dto["name"], (x_positions[0], y_offset), font=self._font
            )
            size_label = Label(
                str(file_dto["size"]), (x_positions[1], y_offset), font=self._font
            )
            type_label = Label(
                file_dto["file_type"], (x_positions[2], y_offset), font=self._font
            )
            self._components.add(name_label, size_label, type_label)

            # Buttons
            download_button = Button(
                position=(x_positions[3], y_offset),
                size=(BUTTON_WIDTH // 2, BUTTON_HEIGHT),
                text="Download",
                on_click=functools.partial(self.on_download, file_dto["name"]),
                name=f"download_{file_dto['name']}",
            )
            delete_button = Button(
                position=(x_positions[3] + BUTTON_WIDTH // 2 + PADDING, y_offset),
                size=(BUTTON_WIDTH // 2, BUTTON_HEIGHT),
                text="Delete",
                on_click=functools.partial(self.on_delete, file_dto["name"]),
                name=f"delete_{file_dto['name']}",
            )
            self._components.add(download_button, delete_button)

            y_offset += self._font.get_linesize() + PADDING

        # Close button
        close_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        close_button_rect.bottomright = (
            self.rect.width - PADDING,
            self.rect.height - PADDING,
        )
        close_button = Button(
            position=close_button_rect.topleft,
            size=close_button_rect.size,
            text="Close",
            on_click=self.on_close,
            name="close",
        )
        self._components.add(close_button)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle a single pygame event.

        This method translates mouse coordinates to be relative to the view's
        surface before passing the event to its child components.

        Args:
            event (pygame.event.Event): The pygame event to process.
        """
        event_to_pass = event
        if event.type in (
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEMOTION,
        ):
            local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
            # Create a new event with the translated position, copying other attributes
            event_to_pass = pygame.event.Event(
                event.type, {**event.dict, "pos": local_pos}
            )

        for component in self._components:
            if isinstance(component, Clickable):
                component.handle_event(event_to_pass)

    def update(self) -> None:
        """Update the view's surface.

        This method redraws the background and all child components. It is
        typically called once per frame.
        """
        self.image.fill(UI_FACE)
        pygame.draw.rect(self.image, UI_BORDER, self.image.get_rect(), UI_BORDER_WIDTH)
        self._components.update()
        self._components.draw(self.image)

"""This module defines the EntryView component for user text input."""

from collections.abc import Callable

import pygame

from decker_pygame.application.dtos import EntryViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.label import Label
from decker_pygame.presentation.components.text_input import TextInput
from decker_pygame.settings import PADDING, UI_FACE, UI_FONT, WHITE

from .base_widgets import Clickable


class EntryView(pygame.sprite.Sprite):
    """A view for user text entry, like a password prompt.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.

    Args:
        data (EntryViewDTO): The data to configure the view.
        on_submit (Callable[[str], None]): Callback when the user submits text.
        on_close (Callable[[], None]): Callback when the user closes the view.
        position (tuple[int, int]): The top-left corner of the view.
        size (tuple[int, int]): The (width, height) of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        data: EntryViewDTO,
        on_submit: Callable[[str], None],
        on_close: Callable[[], None],
        position: tuple[int, int] = (200, 200),
        size: tuple[int, int] = (400, 150),
    ):
        super().__init__()
        self.data = data
        self.on_submit = on_submit
        self.on_close = on_close

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)

        self._font = pygame.font.Font(None, UI_FONT.default_font_size)
        self._components = pygame.sprite.Group()
        self._text_input: TextInput

        self._create_layout()

    def _handle_submit(self) -> None:
        """Internal handler to pass the text input's value to the callback."""
        self.on_submit(self._text_input.text)

    def _create_layout(self) -> None:
        """Creates and arranges the sub-components of the view."""
        self.image.fill(UI_FACE)

        prompt_label = Label(
            self.data.prompt,
            (PADDING, PADDING),
            font=self._font,
            color=WHITE,
        )
        self._components.add(prompt_label)

        self._text_input = TextInput(
            (PADDING, prompt_label.rect.bottom + PADDING),
            (self.rect.width - PADDING * 2, 30),
            label="",  # No label needed as it's separate
            is_password=self.data.is_password,
        )
        self._components.add(self._text_input)

        ok_button = Button(
            (self.rect.width - 180, self.rect.height - 40),
            (80, 30),
            "OK",
            self._handle_submit,
        )
        cancel_button = Button(
            (self.rect.width - 90, self.rect.height - 40),
            (80, 30),
            "Cancel",
            self.on_close,
        )
        self._components.add(ok_button, cancel_button)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle a single pygame event."""
        event_to_pass = event
        # Only translate coordinates for mouse events
        if event.type in (
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEMOTION,
        ):
            local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
            event_to_pass = pygame.event.Event(
                event.type, {**event.dict, "pos": local_pos}
            )

        for component in self._components:
            if isinstance(component, Clickable):
                component.handle_event(event_to_pass)

    def update(self) -> None:
        """Update the view's surface."""
        self.image.fill(UI_FACE)
        self._components.update()
        self._components.draw(self.image)

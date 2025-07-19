"""This module defines the SoundEditView component."""

from collections.abc import Callable

import pygame

from decker_pygame.application.dtos import SoundEditViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.label import Label
from decker_pygame.presentation.components.slider import Slider
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


class SoundEditView(pygame.sprite.Sprite):
    """A view for editing sound volume levels.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.

    Args:
        data (SoundEditViewDTO): The current state of the sound options.
        on_close (Callable[[], None]): Callback for the 'Close' button.
        on_master_volume_change (Callable[[float], None]): Callback for master volume.
        on_music_volume_change (Callable[[float], None]): Callback for music volume.
        on_sfx_volume_change (Callable[[float], None]): Callback for SFX volume.
        position (tuple[int, int], optional): The top-left corner. Defaults to
            (250, 250).
        size (tuple[int, int], optional): The (width, height). Defaults to (300, 200).
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        data: SoundEditViewDTO,
        on_close: Callable[[], None],
        on_master_volume_change: Callable[[float], None],
        on_music_volume_change: Callable[[float], None],
        on_sfx_volume_change: Callable[[float], None],
        position: tuple[int, int] = (250, 250),
        size: tuple[int, int] = (300, 200),
    ):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self._components = pygame.sprite.Group()

        self._create_layout(
            data,
            on_close,
            on_master_volume_change,
            on_music_volume_change,
            on_sfx_volume_change,
        )

    def _create_layout(
        self,
        data: SoundEditViewDTO,
        on_close: Callable[[], None],
        on_master_volume_change: Callable[[float], None],
        on_music_volume_change: Callable[[float], None],
        on_sfx_volume_change: Callable[[float], None],
    ) -> None:
        """Creates and arranges the sub-components of the view."""
        self.image.fill(UI_FACE)
        pygame.draw.rect(self.image, UI_BORDER, self.image.get_rect(), UI_BORDER_WIDTH)

        font = pygame.font.Font(None, UI_FONT.default_font_size)
        y_offset = PADDING

        # Sliders and Labels
        sliders_data = [
            ("Master Volume", data.master_volume, on_master_volume_change),
            ("Music", data.music_volume, on_music_volume_change),
            ("SFX", data.sfx_volume, on_sfx_volume_change),
        ]

        for label_text, initial_val, on_change_cb in sliders_data:
            label = Label(label_text, (PADDING, y_offset), font=font, color=WHITE)
            self._components.add(label)

            slider = Slider(
                (PADDING * 2 + 100, y_offset),
                (150, 20),
                0.0,
                1.0,
                initial_val,
                on_change_cb,
            )
            self._components.add(slider)
            y_offset += slider.rect.height + PADDING

        # Close Button
        close_button = Button(
            (
                self.rect.width - BUTTON_WIDTH - PADDING,
                self.rect.height - BUTTON_HEIGHT - PADDING,
            ),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
            "Close",
            on_close,
        )
        self._components.add(close_button)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle a single pygame event."""
        event_to_pass = event
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
        pygame.draw.rect(self.image, UI_BORDER, self.image.get_rect(), UI_BORDER_WIDTH)
        self._components.update()
        self._components.draw(self.image)

"""This module defines the OptionsView component."""

from collections.abc import Callable

import pygame

from decker_pygame.application.dtos import OptionsViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.checkbox import Checkbox
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


class OptionsView(pygame.sprite.Sprite):
    """A view for displaying and changing game options.

    This view acts as an in-game menu, allowing the player to save, load, quit,
    and change settings like sound and tooltips.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.

    Args:
        data (OptionsViewDTO): The current state of the game options.
        on_save (Callable[[], None]): Callback for the 'Save' button.
        on_load (Callable[[], None]): Callback for the 'Load' button.
        on_quit (Callable[[], None]): Callback for the 'Quit' button.
        on_close (Callable[[], None]): Callback for the 'Close' button.
        on_toggle_sound (Callable[[bool], None]): Callback for the sound checkbox.
        on_toggle_tooltips (Callable[[bool], None]): Callback for the tooltips checkbox.
        position (tuple[int, int], optional): The top-left corner. Defaults to
            (200, 200).
        size (tuple[int, int], optional): The (width, height). Defaults to (400, 300).
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        data: OptionsViewDTO,
        on_save: Callable[[], None],
        on_load: Callable[[], None],
        on_quit: Callable[[], None],
        on_close: Callable[[], None],
        on_toggle_sound: Callable[[bool], None],
        on_toggle_tooltips: Callable[[bool], None],
        position: tuple[int, int] = (200, 200),
        size: tuple[int, int] = (400, 300),
    ):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self._components = pygame.sprite.Group()

        self._create_layout(
            data,
            on_save,
            on_load,
            on_quit,
            on_close,
            on_toggle_sound,
            on_toggle_tooltips,
        )

    def _create_layout(
        self,
        data: OptionsViewDTO,
        on_save: Callable[[], None],
        on_load: Callable[[], None],
        on_quit: Callable[[], None],
        on_close: Callable[[], None],
        on_toggle_sound: Callable[[bool], None],
        on_toggle_tooltips: Callable[[bool], None],
    ) -> None:
        """Creates and arranges the sub-components of the view."""
        self.image.fill(UI_FACE)
        pygame.draw.rect(self.image, UI_BORDER, self.image.get_rect(), UI_BORDER_WIDTH)

        font = pygame.font.Font(None, UI_FONT.default_font_size)

        # Title
        title = Label("Options", (PADDING, PADDING), font=font, color=WHITE)
        self._components.add(title)

        y_offset = title.rect.bottom + PADDING * 2

        # Checkboxes
        sound_checkbox = Checkbox(
            (PADDING, y_offset),
            "Sound Enabled",
            on_toggle_sound,
            name="sound_enabled",
            initial_state=data.sound_enabled,
        )
        self._components.add(sound_checkbox)
        y_offset += sound_checkbox.rect.height + PADDING

        tooltips_checkbox = Checkbox(
            (PADDING, y_offset),
            "Tooltips Enabled",
            on_toggle_tooltips,
            name="tooltips_enabled",
            initial_state=data.tooltips_enabled,
        )
        self._components.add(tooltips_checkbox)
        y_offset += tooltips_checkbox.rect.height + PADDING * 2

        # Action Buttons
        button_x = PADDING
        button_y = y_offset
        button_size = (BUTTON_WIDTH, BUTTON_HEIGHT)

        save_button = Button(
            (button_x, button_y), button_size, "Save Game", on_save, name="save_game"
        )
        self._components.add(save_button)
        button_y += BUTTON_HEIGHT + PADDING

        load_button = Button(
            (button_x, button_y), button_size, "Load Game", on_load, name="load_game"
        )
        self._components.add(load_button)
        button_y += BUTTON_HEIGHT + PADDING

        quit_button = Button(
            (button_x, button_y),
            button_size,
            "Quit to Main Menu",
            on_quit,
            name="quit_to_main_menu",
        )
        self._components.add(quit_button)

        # Close Button
        close_button = Button(
            (
                self.rect.width - BUTTON_WIDTH - PADDING,
                self.rect.height - BUTTON_HEIGHT - PADDING,
            ),
            button_size,
            "Close",
            on_close,
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

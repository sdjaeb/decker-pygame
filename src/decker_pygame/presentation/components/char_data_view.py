"""This module defines the CharDataView component for the character stats UI."""

from collections.abc import Callable
from functools import partial

import pygame

from decker_pygame.application.character_service import CharacterViewData
from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import UI_FACE, UI_FONT

from .base_widgets import Clickable


class CharDataView(pygame.sprite.Sprite):
    """A UI component that displays character data.

    Ported from CharDataDialog.cpp/h.

    Args:
        position (tuple[int, int]): The top-left corner of the view.
        data (CharacterViewData): The data to display.
        on_close (Callable[[], None]): Callback to close the view.
        on_increase_skill (Callable[[str], None]): Callback to increase a skill.
        on_decrease_skill (Callable[[str], None]): Callback to decrease a skill.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _view_deck_button: Button
    _upgrade_lifestyle_button: Button
    _close_button: Button
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        position: tuple[int, int],
        data: CharacterViewData,
        on_close: Callable[[], None],
        on_increase_skill: Callable[[str], None],
        on_decrease_skill: Callable[[str], None],
    ):
        super().__init__()
        self.image = pygame.Surface((400, 450))  # Standard size
        self.rect = self.image.get_rect(topleft=position)
        self._data = data
        self._on_close = on_close
        self._on_increase_skill = on_increase_skill
        self._on_decrease_skill = on_decrease_skill

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = UI_FACE
        self._line_height = self._font.get_linesize()
        self._padding = 10

        self._components = pygame.sprite.Group()

        # --- Buttons ---
        button_h = 30
        button_y = self.image.get_height() - button_h - self._padding

        # View Deck Button
        view_deck_w = 100
        view_deck_x = self._padding
        self._view_deck_button = Button(
            position=(view_deck_x, button_y),
            size=(view_deck_w, button_h),
            text="View Deck",
            on_click=self._on_close,  # Placeholder
        )

        # Upgrade Lifestyle Button
        upgrade_w = 140
        upgrade_x = view_deck_x + view_deck_w + self._padding
        self._upgrade_lifestyle_button = Button(
            position=(upgrade_x, button_y),
            size=(upgrade_w, button_h),
            text="Upgrade Lifestyle",
            on_click=self._on_close,  # Placeholder
        )

        # Close Button
        close_w = 80
        close_x = self.image.get_width() - close_w - self._padding
        self._close_button = Button(
            position=(close_x, button_y),
            size=(close_w, button_h),
            text="Close",
            on_click=self._on_close,
        )
        self._components.add(
            self._view_deck_button, self._upgrade_lifestyle_button, self._close_button
        )

        self._render_data()

    def _render_data(self) -> None:
        """Renders the character data onto the view's surface."""
        self.image.fill(self._background_color)

        y_offset = self._padding
        for text in [
            f"Name: {self._data.name}",
            f"Reputation: {self._data.reputation}",
            f"Money: ${self._data.credits}",
            f"Health: {self._data.health}%",
        ]:
            text_surface = self._font.render(text, True, self._font_color)
            text_rect = text_surface.get_rect(topleft=(self._padding, y_offset))
            self.image.blit(text_surface, text_rect)
            y_offset += self._line_height

        # --- Skills ---
        y_offset += self._padding
        skills_header_text = (
            f"Skills: (Points Available: {self._data.unused_skill_points})"
        )
        skills_header = self._font.render(skills_header_text, True, self._font_color)
        self.image.blit(skills_header, (self._padding, y_offset))
        y_offset += self._line_height

        button_size = (20, 20)
        value_width = 40

        for skill, value in self._data.skills.items():
            skill_label_text = f"  {skill.title()}:"
            skill_label_surface = self._font.render(
                skill_label_text, True, self._font_color
            )
            skill_label_rect = skill_label_surface.get_rect(
                topleft=(self._padding, y_offset)
            )
            self.image.blit(skill_label_surface, skill_label_rect)

            x_offset = skill_label_rect.right + self._padding * 2
            # --- Decrease Button ---
            if value > 0:
                # The lambda s=skill captures the current skill name for the callback
                dec_button = Button(
                    (x_offset, y_offset - 2),
                    button_size,
                    "-",
                    # Use partial to capture the skill name for the callback
                    partial(self._on_decrease_skill, skill),
                )
                self._components.add(dec_button)
            x_offset += button_size[0] + self._padding

            # --- Skill Value ---
            value_surface = self._font.render(str(value), True, self._font_color)
            value_rect = value_surface.get_rect(
                topleft=(x_offset, y_offset), width=value_width
            )
            self.image.blit(value_surface, value_rect)
            x_offset += value_rect.width

            # --- Increase Button ---
            cost_to_increase = value + 1
            if self._data.unused_skill_points >= cost_to_increase:
                inc_button = Button(
                    (x_offset, y_offset - 2),
                    button_size,
                    "+",
                    # Use partial to capture the skill name for the callback
                    partial(self._on_increase_skill, skill),
                )
                self._components.add(inc_button)

            y_offset += self._line_height

        # Draw child components onto this view's surface
        self._components.draw(self.image)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles mouse clicks and delegates them to child components."""
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            # Create a new event with the position translated to be relative to the view
            local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
            new_event = pygame.event.Event(
                event.type, button=event.button, pos=local_pos
            )
            for component in self._components:
                if isinstance(component, Clickable):
                    component.handle_event(new_event)

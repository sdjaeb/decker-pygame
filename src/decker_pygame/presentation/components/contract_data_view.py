"""This module defines the ContractDataView component."""

from collections.abc import Callable
from functools import partial

import pygame

from decker_pygame.application.dtos import ContractSummaryDTO
from decker_pygame.domain.ids import ContractId
from decker_pygame.presentation.components.base_widgets import Clickable
from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import UI_FACE, UI_FONT


class ContractDataView(pygame.sprite.Sprite):
    """A UI component that displays contract data.

    Ported from ContractDataDialog.cpp/h.

    Args:
        position (tuple[int, int]): The top-left corner of the view.
        size (tuple[int, int]): The (width, height) of the view.
        contract (ContractSummaryDTO): The contract data to display.
        on_accept (Callable[[ContractId], None]): Callback when the accept button is
            clicked.

    Attributes:
        image (pygame.Surface): The surface that represents the view.
        rect (pygame.Rect): The rectangular area of the view.
    """

    image: pygame.Surface
    rect: pygame.Rect
    _components: pygame.sprite.Group[pygame.sprite.Sprite]

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        contract: ContractSummaryDTO,
        on_accept: Callable[[ContractId], None],
    ):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self._contract = contract

        self._font = pygame.font.Font(
            UI_FONT.default_font_name, UI_FONT.default_font_size
        )
        self._font_color = UI_FONT.dark_font_color
        self._background_color = UI_FACE
        self._padding = 10
        self._components = pygame.sprite.Group()

        self._accept_button = Button(
            (self.image.get_width() - 90, self.image.get_height() - 40),
            (80, 30),
            "Accept",
            # Use partial to pass the contract ID to the callback
            partial(on_accept, self._contract.id),
        )
        self._components.add(self._accept_button)
        self._render_data()

    def _render_data(self) -> None:
        """Renders the contract data onto the view's surface."""
        self.image.fill(self._background_color)

        y_offset = self._padding

        lines = [
            f"Title: {self._contract.title}",
            f"Client: {self._contract.client}",
            f"Reward: ${self._contract.reward}",
        ]

        for line in lines:
            text_surface = self._font.render(line, True, self._font_color)
            text_rect = text_surface.get_rect(topleft=(self._padding, y_offset))
            self.image.blit(text_surface, text_rect)
            y_offset += text_surface.get_height() + 5

        self._components.draw(self.image)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles events passed from the input handler."""
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            # Translate mouse coordinates to be relative to this view
            local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
            new_event = pygame.event.Event(
                event.type, button=event.button, pos=local_pos
            )
            for component in self._components:
                if isinstance(component, Clickable):
                    component.handle_event(new_event)

"""This module defines the ContractListView component."""

from collections.abc import Callable
from typing import Optional

import pygame

from decker_pygame.application.dtos import ContractSummaryDTO
from decker_pygame.presentation.components.list_view import ListView
from decker_pygame.settings import UI_FACE


class ContractListView(pygame.sprite.Sprite):
    """A UI component that displays a list of contracts by wrapping a generic ListView.

    Ported from ContractListDialog.cpp/h.

    Args:
        position (tuple[int, int]): The top-left corner of the view.
        size (tuple[int, int]): The (width, height) of the view.
        on_contract_selected (Callable[[Optional[ContractSummaryDTO]], None]):
            A callback function that is invoked when the user selects or
            deselects a contract in the list. It receives the selected
            contract DTO, or None if the selection is cleared.

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
        on_contract_selected: Callable[[Optional[ContractSummaryDTO]], None],
    ):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self._background_color = UI_FACE

        columns = [("Client", 150), ("Title", 200), ("Reward", 50)]
        self._list_view = ListView(
            position=(0, 0),  # Relative to this container
            size=size,
            columns=columns,
            on_selection_change=on_contract_selected,
        )
        self._components = pygame.sprite.Group(self._list_view)

    def _contract_renderer(self, contract: ContractSummaryDTO) -> list[str]:
        return [contract.client, contract.title, f"${contract.reward}"]

    def set_contracts(self, contracts: list[ContractSummaryDTO]) -> None:
        """Populates the list with contract data."""
        self._list_view.set_items(contracts, self._contract_renderer)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles events by passing them to the underlying list view."""
        self._list_view.handle_event(event)

    def update(self) -> None:
        """Updates and redraws the view."""
        self.image.fill(self._background_color)
        self._components.update()
        self._components.draw(self.image)

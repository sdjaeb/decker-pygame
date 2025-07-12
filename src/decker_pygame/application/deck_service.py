"""This module defines the application service for deck-related operations.

It includes the DeckService, which orchestrates use cases like moving programs
between a character's deck and storage, and the Data Transfer Objects (DTOs)
used to pass deck data to the presentation layer.
"""

import uuid
from collections.abc import Callable
from dataclasses import dataclass

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.deck import Deck
from decker_pygame.domain.ids import CharacterId, DeckId
from decker_pygame.ports.repository_interfaces import (
    CharacterRepositoryInterface,
    DeckRepositoryInterface,
)
from decker_pygame.ports.service_interfaces import DeckServiceInterface


@dataclass(frozen=True)
class DeckProgramDTO:
    """Data Transfer Object for a single program in the deck."""

    name: str
    size: int


@dataclass(frozen=True)
class DeckViewData:
    """A dedicated View Model DTO for the deck view.

    This class aggregates all data needed by the DeckView and OrderView components.
    """

    programs: list[DeckProgramDTO]
    # TODO: These will be derived from character stats later
    total_deck_size: int = 100
    used_deck_size: int = 0


@dataclass(frozen=True)
class TransferViewData:
    """A dedicated View Model DTO for the transfer view.

    This class aggregates all data needed by the TransferView component.
    """

    deck_programs: list[DeckProgramDTO]
    stored_programs: list[DeckProgramDTO]


class DeckServiceError(Exception):
    """Base exception for deck service errors."""


class DeckService(DeckServiceInterface):
    """Application service for deck-related operations."""

    def __init__(
        self,
        deck_repo: DeckRepositoryInterface,
        character_repo: CharacterRepositoryInterface,
        event_dispatcher: EventDispatcher,
    ) -> None:
        """Initialize the DeckService.

        Args:
            deck_repo: The repository for deck aggregates.
            character_repo: The repository for character aggregates.
            event_dispatcher: The dispatcher for domain events.
        """
        self.deck_repo = deck_repo
        self.character_repo = character_repo
        self.event_dispatcher = event_dispatcher

    def create_deck(self) -> DeckId:
        """Creates a new, empty deck, saves it, and returns its ID."""
        deck_id = DeckId(uuid.uuid4())
        deck = Deck(id=deck_id, programs=[])
        self.deck_repo.save(deck)
        return deck_id

    def get_deck_view_data(self, deck_id: DeckId) -> DeckViewData | None:
        """Retrieves and aggregates all data needed for the deck view."""
        deck = self.deck_repo.get(deck_id)
        if not deck:
            return None

        program_dtos = [DeckProgramDTO(name=p.name, size=p.size) for p in deck.programs]
        used_size = sum(p.size for p in deck.programs)

        return DeckViewData(programs=program_dtos, used_deck_size=used_size)

    def get_transfer_view_data(
        self, character_id: CharacterId
    ) -> TransferViewData | None:
        """Retrieves and aggregates all data needed for the transfer view."""
        character = self.character_repo.get(character_id)
        if not character:
            return None

        deck = self.deck_repo.get(character.deck_id)
        if not deck:
            return None

        deck_programs = [
            DeckProgramDTO(name=p.name, size=p.size) for p in deck.programs
        ]
        stored_programs = [
            DeckProgramDTO(name=p.name, size=p.size) for p in character.stored_programs
        ]

        return TransferViewData(
            deck_programs=deck_programs, stored_programs=stored_programs
        )

    def move_program_to_deck(
        self, character_id: CharacterId, program_name: str
    ) -> None:
        """Moves a program from a character's storage to their deck."""
        character = self.character_repo.get(character_id)
        if not character:
            raise DeckServiceError(f"Character with ID {character_id} not found.")

        deck = self.deck_repo.get(character.deck_id)
        if not deck:
            raise DeckServiceError(f"Deck with ID {character.deck_id} not found.")

        try:
            program_to_move = character.remove_stored_program(program_name)
            deck.add_program(program_to_move)
        except ValueError as e:
            raise DeckServiceError(str(e)) from e

        self.character_repo.save(character)
        self.deck_repo.save(deck)

    def move_program_to_storage(
        self, character_id: CharacterId, program_name: str
    ) -> None:
        """Moves a program from a character's deck to their storage."""
        character = self.character_repo.get(character_id)
        if not character:
            raise DeckServiceError(f"Character with ID {character_id} not found.")

        deck = self.deck_repo.get(character.deck_id)
        if not deck:
            raise DeckServiceError(f"Deck with ID {character.deck_id} not found.")

        try:
            program_to_move = deck.remove_program(program_name)
            character.stored_programs.append(program_to_move)
        except ValueError as e:
            raise DeckServiceError(str(e)) from e

        self.character_repo.save(character)
        self.deck_repo.save(deck)

    def _execute_deck_change(
        self, deck_id: DeckId, change_func: Callable[[Deck], None]
    ) -> None:
        """Helper to load, modify, and save a deck."""
        deck = self.deck_repo.get(deck_id)
        if not deck:
            raise DeckServiceError(f"Deck with ID {deck_id} not found.")

        try:
            change_func(deck)
        except ValueError as e:
            raise DeckServiceError(str(e)) from e

        self.deck_repo.save(deck)
        # In the future, we might dispatch deck-related events here
        # self.event_dispatcher.dispatch(deck.events)
        # deck.clear_events()

    def move_program_up(self, deck_id: DeckId, program_name: str) -> None:
        """Use case to move a program up in the deck order."""
        self._execute_deck_change(
            deck_id, lambda deck: deck.move_program_up(program_name)
        )

    def move_program_down(self, deck_id: DeckId, program_name: str) -> None:
        """Use case to move a program down in the deck order."""
        self._execute_deck_change(
            deck_id, lambda deck: deck.move_program_down(program_name)
        )

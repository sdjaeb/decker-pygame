"""This module defines the application service for character-related operations.

It includes the CharacterService, which orchestrates use cases like increasing
a character's skill.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING, Optional

from decker_pygame.application.dtos import CharacterDataDTO, CharacterViewDTO
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.character import Character
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface
from decker_pygame.ports.service_interfaces import CharacterServiceInterface

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.ports.service_interfaces import PlayerServiceInterface


class CharacterServiceError(Exception):
    """Base exception for character service errors."""


class CharacterService(CharacterServiceInterface):
    """Application service for character-related operations."""

    def __init__(
        self,
        character_repo: CharacterRepositoryInterface,
        player_service: "PlayerServiceInterface",
        event_dispatcher: EventDispatcher,
    ) -> None:
        self.character_repo = character_repo
        self.player_service = player_service
        self.event_dispatcher = event_dispatcher

    def get_character_name(self, character_id: CharacterId) -> Optional[str]:
        """Retrieves the name of a character."""
        character = self.character_repo.get(character_id)
        if not character:
            return None
        return character.name

    def get_character_data(
        self, character_id: CharacterId
    ) -> Optional[CharacterDataDTO]:
        """Retrieves a DTO with character data for UI display."""
        character = self.character_repo.get(character_id)
        if not character:
            return None

        return CharacterDataDTO(
            name=character.name,
            credits=character.credits,
            skills=character.skills,
            unused_skill_points=character.unused_skill_points,
            deck_id=character.deck_id,
        )

    def get_character_view_data(
        self, character_id: CharacterId, player_id: PlayerId
    ) -> Optional[CharacterViewDTO]:
        """Retrieves and aggregates all data needed for the character view.

        This method acts as a query that assembles a dedicated View Model DTO,
        simplifying the data fetching logic for the presentation layer.
        """
        character = self.character_repo.get(character_id)
        player_status = self.player_service.get_player_status(player_id)

        if not character or not player_status:
            return None

        return CharacterViewDTO(
            name=character.name,
            credits=character.credits,
            reputation=character.reputation,
            skills=character.skills,
            unused_skill_points=character.unused_skill_points,
            health=player_status.current_health,
        )

    def _execute_skill_change(
        self,
        character_id: CharacterId,
        change_func: Callable[[Character], None],
    ) -> None:
        """Helper to load, modify, save a character, and dispatch events."""
        character = self.character_repo.get(character_id)
        if not character:
            raise CharacterServiceError(f"Character with ID {character_id} not found.")

        try:
            change_func(character)
        except ValueError as e:
            # Translate domain error into application-specific error
            raise CharacterServiceError(str(e)) from e

        self.character_repo.save(character)
        self.event_dispatcher.dispatch(character.events)
        character.clear_events()

    def increase_skill(self, character_id: CharacterId, skill_name: str) -> None:
        """Use case to increase a character's skill."""
        self._execute_skill_change(
            character_id, lambda char: char.increase_skill(skill_name)
        )

    def decrease_skill(self, character_id: CharacterId, skill_name: str) -> None:
        """Use case to decrease a character's skill."""
        self._execute_skill_change(
            character_id, lambda char: char.decrease_skill(skill_name)
        )

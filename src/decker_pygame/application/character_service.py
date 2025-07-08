from collections.abc import Callable
from dataclasses import dataclass

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.character import Character
from decker_pygame.domain.ids import CharacterId
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface
from decker_pygame.ports.service_interfaces import CharacterServiceInterface


@dataclass(frozen=True)
class CharacterDataDTO:
    """Data Transfer Object for character data to be displayed in the UI."""

    name: str
    credits: int
    skills: dict[str, int]
    unused_skill_points: int
    reputation: int = 0  # Placeholder for now


class CharacterServiceError(Exception):
    """Base exception for character service errors."""


class CharacterService(CharacterServiceInterface):
    """Application service for character-related operations."""

    def __init__(
        self,
        character_repo: CharacterRepositoryInterface,
        event_dispatcher: EventDispatcher,
    ) -> None:
        """
        Initialize the CharacterService.

        Args:
            character_repo: Repository for character aggregates.
            event_dispatcher: The dispatcher for domain events.
        """
        self.character_repo = character_repo
        self.event_dispatcher = event_dispatcher

    def get_character_name(self, character_id: CharacterId) -> str | None:
        """
        Retrieves the name of a character.
        """
        character = self.character_repo.get(character_id)
        if not character:
            return None
        return character.name

    def get_character_data(self, character_id: CharacterId) -> CharacterDataDTO | None:
        """
        Retrieves a DTO with character data for UI display.
        """
        character = self.character_repo.get(character_id)
        if not character:
            return None

        return CharacterDataDTO(
            name=character.name,
            credits=character.credits,
            skills=character.skills,
            unused_skill_points=character.unused_skill_points,
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

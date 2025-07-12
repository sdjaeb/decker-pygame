from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.character import Character
from decker_pygame.domain.ids import CharacterId, DeckId, PlayerId
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface
from decker_pygame.ports.service_interfaces import CharacterServiceInterface

if TYPE_CHECKING:  # pragma: no cover
    from decker_pygame.ports.service_interfaces import PlayerServiceInterface


@dataclass(frozen=True)
class CharacterDataDTO:
    """Data Transfer Object for character data to be displayed in the UI."""

    name: str
    credits: int
    skills: dict[str, int]
    unused_skill_points: int
    deck_id: DeckId
    reputation: int = 0  # Placeholder for now


@dataclass(frozen=True)
class CharacterViewData:
    """
    A dedicated View Model DTO that aggregates all data needed for the
    character data view.
    """

    name: str
    credits: int
    reputation: int
    skills: dict[str, int]
    unused_skill_points: int
    health: int


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
        """
        Initialize the CharacterService.

        Args:
            character_repo: Repository for character aggregates.
            player_service: Service for player-related queries.
            event_dispatcher: The dispatcher for domain events.
        """
        self.character_repo = character_repo
        self.player_service = player_service
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
            deck_id=character.deck_id,
        )

    def get_character_view_data(
        self, character_id: CharacterId, player_id: PlayerId
    ) -> CharacterViewData | None:
        """
        Retrieves and aggregates all data needed for the character view.

        This method acts as a query that assembles a dedicated View Model DTO,
        simplifying the data fetching logic for the presentation layer.
        """
        char_data = self.get_character_data(character_id)
        player_status = self.player_service.get_player_status(player_id)

        if not char_data or not player_status:
            return None

        return CharacterViewData(
            name=char_data.name,
            credits=char_data.credits,
            reputation=char_data.reputation,
            skills=char_data.skills,
            unused_skill_points=char_data.unused_skill_points,
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

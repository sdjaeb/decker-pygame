"""This module defines the service for matrix run-related use cases."""

from decker_pygame.application.dtos import MatrixRunViewDTO
from decker_pygame.domain.events import MatrixLogEntryCreated
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.ports.repository_interfaces import (
    CharacterRepositoryInterface,
    DeckRepositoryInterface,
    PlayerRepositoryInterface,
)
from decker_pygame.ports.service_interfaces import (
    MatrixRunServiceInterface,
)


class MatrixRunService(MatrixRunServiceInterface):
    """Service for handling matrix run logic."""

    def __init__(
        self,
        character_repo: CharacterRepositoryInterface,
        deck_repo: DeckRepositoryInterface,
        player_repo: PlayerRepositoryInterface,
    ):
        self._character_repo = character_repo
        self._deck_repo = deck_repo
        self._player_repo = player_repo
        self._messages: list[str] = []
        self._max_messages = 5  # Keep the log from growing indefinitely

    def on_matrix_log_entry(self, event: MatrixLogEntryCreated) -> None:
        """Handles the event for a new matrix log entry."""
        self._messages.append(event.message)
        if len(self._messages) > self._max_messages:
            self._messages = self._messages[-self._max_messages :]

    def get_matrix_run_view_data(
        self, character_id: CharacterId, player_id: PlayerId
    ) -> MatrixRunViewDTO:
        """Retrieves a DTO with all data needed for the matrix run view."""
        character = self._character_repo.get(character_id)
        player = self._player_repo.get(player_id)
        deck = self._deck_repo.get(character.deck_id) if character else None

        if not character or not deck or not player:
            return MatrixRunViewDTO()

        # Max health is hardcoded as 100 in Player.create
        health_percent = (player.health / 100) * 100
        # Max deck health is assumed to be 100
        deck_health_percent = (deck.health / 100) * 100

        # In the future, this data would come from a System/Node aggregate
        dummy_nodes = {"cpu": (50, 50), "data_store_1": (100, 100)}
        dummy_connections = [("cpu", "data_store_1")]

        return MatrixRunViewDTO(
            physical_health=health_percent,
            mental_health=health_percent,  # Using same value for now
            deck_health=deck_health_percent,
            messages=self._messages,
            software=[p.name for p in deck.programs],
            nodes=dummy_nodes,
            connections=dummy_connections,
        )

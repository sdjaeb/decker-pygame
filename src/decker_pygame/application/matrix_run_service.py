"""This module defines the service for matrix run-related use cases."""

import uuid

from decker_pygame.application.dtos import MatrixRunViewDTO
from decker_pygame.domain.events import MatrixLogEntryCreated
from decker_pygame.domain.ids import CharacterId, PlayerId, SystemId
from decker_pygame.ports.repository_interfaces import (
    CharacterRepositoryInterface,
    DeckRepositoryInterface,
    PlayerRepositoryInterface,
    SystemRepositoryInterface,
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
        system_repo: SystemRepositoryInterface,
    ):
        self._character_repo = character_repo
        self._deck_repo = deck_repo
        self._player_repo = player_repo
        self._system_repo = system_repo
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
        # For now, we'll hardcode the system ID we're running against.
        # In the future, this would come from the contract or node being accessed.
        system_id = SystemId(uuid.UUID("a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5"))
        system = self._system_repo.get(system_id)

        if not character or not deck or not player or not system:
            return MatrixRunViewDTO()

        # Max health is hardcoded as 100 in Player.create
        health_percent = (player.health / 100) * 100
        # Max deck health is assumed to be 100
        deck_health_percent = (deck.health / 100) * 100

        # Map domain data to DTO format
        nodes_for_dto = {node.name: node.position for node in system.nodes}
        node_map_by_id = {node.id: node for node in system.nodes}
        connections_for_dto = []
        for start_id, end_id in system.connections:
            start_node = node_map_by_id.get(start_id)
            end_node = node_map_by_id.get(end_id)
            if start_node and end_node:
                connections_for_dto.append((start_node.name, end_node.name))

        return MatrixRunViewDTO(
            physical_health=health_percent,
            mental_health=health_percent,  # Using same value for now
            deck_health=deck_health_percent,
            messages=self._messages,
            software=[p.name for p in deck.programs],
            nodes=nodes_for_dto,
            connections=connections_for_dto,
        )

"""This module defines the service for matrix run-related use cases."""

from decker_pygame.application.dtos import MatrixRunViewDTO
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

        return MatrixRunViewDTO(
            physical_health=health_percent,
            mental_health=health_percent,  # Using same value for now
            deck_health=deck_health_percent,
            software=[p.name for p in deck.programs],
            # Other fields can be populated as the domain evolves
        )

# player_service.py

import uuid

from decker_pygame.domain.ids import PlayerId
from decker_pygame.domain.player import Player
from decker_pygame.domain.player_repository_interface import PlayerRepositoryInterface


class PlayerService:
    """Application service for player-related operations."""

    def __init__(self, player_repo: PlayerRepositoryInterface) -> None:
        """
        Initialize the PlayerService.

        Args:
            player_repo (PlayerRepositoryInterface): Repository for player aggregates.
        """
        self.player_repo = player_repo

    def create_new_player(self, name: str) -> PlayerId:
        """
        Create a new player, save it, and return the new player's ID.

        Args:
            name (str): Name of the new player.

        Returns:
            PlayerId: The ID of the newly created player.
        """
        player_id = PlayerId(uuid.uuid4())
        player = Player.create(player_id=player_id, name=name, initial_health=100)

        self.player_repo.save(player)
        # self.event_dispatcher.dispatch(player.events)
        return PlayerId(player.id)

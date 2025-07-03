# player_service.py

import uuid

from decker_pygame.domain.ids import PlayerId
from decker_pygame.domain.player import Player
from decker_pygame.domain.player_repository_interface import PlayerRepositoryInterface


class PlayerService:
    def __init__(self, player_repo: PlayerRepositoryInterface) -> None:
        self.player_repo = player_repo
        # In a real system, an event dispatcher would also be injected here.

    def create_new_player(self, name: str) -> PlayerId:
        """
        Creates a new player, saves it, and returns the new player's ID.
        """
        player_id = PlayerId(uuid.uuid4())
        player = Player.create(player_id=player_id, name=name, initial_health=100)

        self.player_repo.save(player)
        # self.event_dispatcher.dispatch(player.events)
        return PlayerId(player.id)

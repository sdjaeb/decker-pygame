import uuid

from decker_pygame.domain.model import Player, PlayerId
from decker_pygame.domain.repositories import PlayerRepository


class PlayerService:
    def __init__(self, player_repo: PlayerRepository):
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
        return player.id

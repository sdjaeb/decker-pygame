from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.events import PlayerCreated
from decker_pygame.domain.ids import AggregateId, PlayerId


class Player(AggregateRoot):
    """The Player aggregate root."""

    def __init__(self, id: PlayerId, name: str, health: int) -> None:
        super().__init__(id=AggregateId(id))
        self.name = name
        self.health = health

    @staticmethod
    def create(player_id: PlayerId, name: str, initial_health: int) -> "Player":
        """Factory to create a new player, raising a domain event."""
        player = Player(id=player_id, name=name, health=initial_health)
        player._events.append(
            PlayerCreated(
                player_id=PlayerId(player.id),
                name=player.name,
                initial_health=player.health,
            )
        )
        return player

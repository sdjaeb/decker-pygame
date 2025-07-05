import uuid
from typing import Any

from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.events import PlayerCreated
from decker_pygame.domain.ids import AggregateId, PlayerId


class Player(AggregateRoot):
    """The Player aggregate root."""

    def __init__(self, id: PlayerId, name: str, health: int) -> None:
        """
        Initialize a Player aggregate.

        Args:
            id (PlayerId): Unique identifier for the player.
            name (str): The player's name.
            health (int): The player's starting health.
        """
        super().__init__(id=AggregateId(id))
        self.name = name
        self.health = health

    @staticmethod
    def create(player_id: PlayerId, name: str, initial_health: int) -> "Player":
        """
        Factory to create a new player, raising a PlayerCreated domain event.

        Args:
            player_id (PlayerId): Unique identifier for the new player.
            name (str): The player's name.
            initial_health (int): The player's starting health.

        Returns:
            Player: The newly created Player aggregate.
        """
        player = Player(id=player_id, name=name, health=initial_health)
        player._events.append(
            PlayerCreated(
                player_id=PlayerId(player.id),
                name=player.name,
                initial_health=player.health,
            )
        )
        return player

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the aggregate to a dictionary.

        Returns:
            A dictionary representation of the Player.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "health": self.health,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Player":
        """
        Reconstitute a Player from a dictionary.

        Args:
            data: The dictionary data.

        Returns:
            A Player instance.
        """
        return cls(
            id=PlayerId(uuid.UUID(data["id"])), name=data["name"], health=data["health"]
        )

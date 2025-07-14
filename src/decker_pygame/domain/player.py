"""This module defines the Player aggregate root."""

import uuid
from typing import Any

from decker_pygame.application.decorators import emits
from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.events import PlayerCreated
from decker_pygame.domain.ids import AggregateId, PlayerId


class Player(AggregateRoot):
    """The Player aggregate root.

    Args:
        id (PlayerId): Unique identifier for the player.
        name (str): The player's name.
        health (int): The player's starting health.
    """

    def __init__(self, id: PlayerId, name: str, health: int) -> None:
        super().__init__(id=AggregateId(id))
        self.name = name
        self.health = health

    @staticmethod
    @emits(PlayerCreated)
    def create(player_id: PlayerId, name: str, initial_health: int) -> "Player":
        """Factory to create a new player, raising a PlayerCreated domain event.

        Args:
            player_id (PlayerId): Unique identifier for the new player.
            name (str): The player's name.
            initial_health (int): The player's starting health.

        Returns:
            "Player": The newly created Player aggregate.
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
        """Serialize the aggregate to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the Player.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "health": self.health,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Player":
        """Reconstitute a Player from a dictionary.

        Args:
            data (dict[str, Any]): The dictionary data.

        Returns:
            "Player": A Player instance.
        """
        return cls(
            id=PlayerId(uuid.UUID(data["id"])), name=data["name"], health=data["health"]
        )

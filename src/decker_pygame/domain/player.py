import uuid
from typing import Any, NewType

from decker_pygame.domain.events import Event, PlayerCreated

PlayerId = NewType("PlayerId", uuid.UUID)


class Player:
    """The Player aggregate root."""

    def __init__(self, id: PlayerId, name: str, health: int) -> None:
        self.id = id
        self.name = name
        self.health = health
        self._events: list[Event] = []

    @staticmethod
    def create(player_id: PlayerId, name: str, initial_health: int) -> "Player":
        """Factory to create a new player, raising a domain event."""
        player = Player(id=player_id, name=name, health=initial_health)
        player._events.append(
            PlayerCreated(
                player_id=player.id,
                name=player.name,
                initial_health=player.health,  # type: ignore[arg-type]
            )
        )
        return player

    @property
    def events(self) -> list[Event]:
        return list(self._events)

    def clear_events(self) -> None:
        self._events.clear()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Player) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

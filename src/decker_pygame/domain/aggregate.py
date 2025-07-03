from typing import Any

from decker_pygame.domain.events import Event
from decker_pygame.domain.ids import AggregateId


class AggregateRoot:
    def __init__(self, id: AggregateId) -> None:
        self.id = id
        self._events: list[Event] = []

    @property
    def events(self) -> list[Event]:
        return list(self._events)

    def clear_events(self) -> None:
        self._events.clear()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AggregateRoot):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

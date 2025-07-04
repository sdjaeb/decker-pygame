from decker_pygame.domain.ddd.entity import Entity
from decker_pygame.domain.events import Event
from decker_pygame.domain.ids import AggregateId


class AggregateRoot(Entity):
    """A base class for aggregate roots, extending Entity with event handling."""

    def __init__(self, id: AggregateId) -> None:
        super().__init__(id=id)
        self._events: list[Event] = []

    @property
    def events(self) -> list[Event]:
        return list(self._events)

    def clear_events(self) -> None:
        self._events.clear()

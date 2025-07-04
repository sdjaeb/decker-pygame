from decker_pygame.domain.ddd.entity import Entity
from decker_pygame.domain.events import Event
from decker_pygame.domain.ids import AggregateId


class AggregateRoot(Entity):
    """
    DDD Aggregate Root base class.

    An Aggregate Root is the entry point to an aggregate, enforcing invariants
    and managing domain events. All references from outside the aggregate
    should point to the root, not to internal entities.
    """

    def __init__(self, id: AggregateId) -> None:
        """
        Initialize the aggregate root with an ID and empty event list.

        Args:
            id (AggregateId): The unique identifier for the aggregate root.
        """
        super().__init__(id=id)
        self._events: list[Event] = []

    @property
    def events(self) -> list[Event]:
        """
        Return a copy of the list of domain events.

        Returns:
            list[Event]: The list of domain events.
        """
        return list(self._events)

    def clear_events(self) -> None:
        """
        Clear all stored domain events.

        Returns:
            None
        """
        self._events.clear()

"""This module provides the EventDispatcher class.

The EventDispatcher is a central component in our event-driven architecture.
It allows different parts of the application to communicate in a decoupled
manner by subscribing to and dispatching domain events.
"""

from collections import defaultdict
from collections.abc import Callable
from typing import Any, TypeVar, cast

from decker_pygame.domain.events import Event

E = TypeVar("E", bound=Event)
Subscriber = Callable[[E], None]
Condition = Callable[[E], bool]


class EventDispatcher:
    """A simple event dispatcher using the publish-subscribe pattern.

    The dispatcher is initialized with a mapping of event types to subscribers.
    """

    def __init__(self) -> None:
        # The internal storage uses `Any` for the event type in the callable.
        # This is a concession to mypy's type system, as dicts cannot easily
        # express the relationship between a key's type and its value's type.
        # The public `subscribe` method provides the necessary type safety.
        self._subscribers: dict[
            type[Event],
            list[tuple[Callable[[Any], None], Callable[[Any], bool] | None]],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: type[E],
        subscriber: Subscriber[E],
        *,
        condition: Condition[E] | None = None,
    ) -> None:
        """Register a subscriber for a specific event type.

        Args:
            event_type (type[E]): The class of the event to subscribe to.
            subscriber (Subscriber[E]): A callable that will be invoked with the
                event.
            condition (Condition[E] | None): An optional callable that must return
                True for the subscriber to be invoked.
        """
        # We cast here to satisfy the internal storage type. The public signature
        # with the TypeVar E ensures the caller provides a valid pair.
        self._subscribers[event_type].append(
            (subscriber, cast(Callable[[Any], bool] | None, condition))
        )

    def dispatch(self, events: list[Event]) -> None:
        """Dispatch a list of events to all registered subscribers."""
        for event in events:
            event_type = type(event)
            if event_type in self._subscribers:
                for subscriber, condition in self._subscribers[event_type]:
                    if condition is None or condition(event):
                        subscriber(event)

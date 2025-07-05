# ruff: noqa: UP047
from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from decker_pygame.domain.events import Event

P = ParamSpec("P")
R = TypeVar("R")
E = TypeVar("E", bound=Event)
F = TypeVar("F", bound=Callable[[Any], None])


def emits(*event_types: type[Event]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator to mark a function as an emitter of one or more domain events.

    This is primarily for semantic clarity and discoverability. It attaches a
    `_emits` attribute to the function for potential introspection.

    Args:
        *event_types: The Event class or classes that this function can emit.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return func(*args, **kwargs)

        setattr(wrapper, "_emits", event_types)  # noqa: B010
        return wrapper

    return decorator


def handles(*event_types: type[Event]) -> Callable[[F], F]:
    """
    A decorator to mark a function as a handler for one or more domain events.

    This is for semantic clarity and discoverability.

    Args:
        *event_types: The Event class or classes that this function handles.
    """

    def decorator(func: F) -> F:
        # Append the new event types to any existing ones.
        setattr(func, "_handles", getattr(func, "_handles", []) + list(event_types))  # noqa: B010
        return func

    return decorator

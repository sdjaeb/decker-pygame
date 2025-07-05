from collections.abc import Callable

from decker_pygame.application.decorators import handles
from decker_pygame.application.logging_service import LoggingService
from decker_pygame.domain.events import Event, PlayerCreated


def create_event_logging_handler(
    logging_service: LoggingService,
) -> Callable[[Event], None]:
    """
    A factory that creates a generic event handler for logging.

    This handler extracts data from any domain event and passes it to the
    logging service for structured logging.
    """

    @handles(Event)  # type: ignore[type-abstract]
    def log_event(event: Event) -> None:
        event_type = type(event).__name__
        log_data = {
            key: str(value)
            for key, value in event.__dict__.items()
            if not key.startswith("_")
        }
        logging_service.log(f"Domain Event: {event_type}", data=log_data)

    return log_event


def log_special_player_created(event: PlayerCreated) -> None:
    """
    A handler that only logs when a specific condition is met.
    Note: This handler is not decorated with @handles because its subscription
    logic (the condition) is handled by the EventDispatcher at runtime.
    """
    print(f"EVENT LOG: A special player named '{event.name}' was created!")


def is_special_player(event: PlayerCreated) -> bool:
    """A condition function that returns True if the player's name is 'Rynn'."""
    return event.name.lower() == "rynn"

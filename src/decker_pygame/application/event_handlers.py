from decker_pygame.application.decorators import handles
from decker_pygame.domain.events import PlayerCreated


@handles(PlayerCreated)
def log_player_created(event: PlayerCreated) -> None:
    """
    A simple event handler that logs when a player is created.
    """
    print(f"EVENT LOG: Player '{event.name}' created with ID {event.player_id}.")


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

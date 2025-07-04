import abc

from decker_pygame.domain.ids import PlayerId
from decker_pygame.domain.player import Player


class PlayerRepositoryInterface(abc.ABC):
    """Abstract base class for player repository implementations."""

    @abc.abstractmethod
    def get(self, player_id: PlayerId) -> Player | None:
        """Retrieve a player by ID.

        Args:
            player_id (PlayerId): The ID of the player.

        Returns:
            Player | None: The player if found, else None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, player: Player) -> None:
        """Save a player aggregate.

        Args:
            player (Player): The player to save.
        """
        raise NotImplementedError

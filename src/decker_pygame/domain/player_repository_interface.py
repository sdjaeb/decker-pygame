import abc

from decker_pygame.domain.ids import PlayerId
from decker_pygame.domain.player import Player


class PlayerRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def get(self, player_id: PlayerId) -> Player | None:
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, player: Player) -> None:
        raise NotImplementedError

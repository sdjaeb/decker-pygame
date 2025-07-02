import abc

from decker_pygame.domain.model import Player, PlayerId


class PlayerRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, player_id: PlayerId) -> Player | None:
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, player: Player) -> None:
        raise NotImplementedError

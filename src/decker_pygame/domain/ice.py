from decker_pygame.domain.ddd.entity import Entity
from decker_pygame.domain.ids import IceId


class Ice(Entity):
    """Represents Intrusion Countermeasures Electronics (ICE)."""

    def __init__(self, id: IceId, name: str, strength: int) -> None:
        """
        Initialize an Ice entity.

        Args:
            id (IceId): Unique identifier for the ICE.
            name (str): Name of the ICE.
            strength (int): Strength of the ICE.
        """
        super().__init__(id=id)
        self.name = name
        self.strength = strength

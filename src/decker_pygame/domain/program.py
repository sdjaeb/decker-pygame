import uuid
from typing import Any

from decker_pygame.domain.ddd.entity import Entity
from decker_pygame.domain.ids import ProgramId


class Program(Entity):
    """Represents a program or piece of software in the game.

    This may become a Value Object later if programs are defined only by their
    attributes and have no unique identity.
    """

    def __init__(self, id: ProgramId, name: str) -> None:
        """
        Initialize a Program.

        Args:
            id (ProgramId): Unique identifier for the program.
            name (str): Name of the program.
        """
        super().__init__(id=id)
        self.name = name

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the entity to a dictionary.

        Returns:
            A dictionary representation of the Program.
        """
        return {"id": str(self.id), "name": self.name}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Program":
        """
        Reconstitute a Program from a dictionary.

        Args:
            data: The dictionary data.

        Returns:
            A Program instance.
        """
        return cls(id=ProgramId(uuid.UUID(data["id"])), name=data["name"])

import uuid
from typing import Any

from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.ids import AggregateId, DeckId
from decker_pygame.domain.program import Program


class Deck(AggregateRoot):
    """Represents a character's deck, which holds their programs."""

    def __init__(self, id: DeckId, programs: list[Program]) -> None:
        """Initialize a Deck."""
        super().__init__(id=AggregateId(id))
        self.programs = programs

    def add_program(self, program: Program) -> None:
        """Adds a program to the deck."""
        # In the future, this is where we would check for deck memory limits.
        self.programs.append(program)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the aggregate to a dictionary.
        """
        return {
            "id": str(self.id),
            "programs": [prog.to_dict() for prog in self.programs],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Deck":
        """
        Reconstitute a Deck from a dictionary.
        """
        return cls(
            id=DeckId(uuid.UUID(data["id"])),
            programs=[Program.from_dict(p_data) for p_data in data["programs"]],
        )

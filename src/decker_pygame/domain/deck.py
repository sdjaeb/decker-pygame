"""This module defines the Deck aggregate root."""

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

    def remove_program(self, program_name: str) -> Program:
        """Finds, removes, and returns a program from the deck."""
        try:
            index = next(
                i for i, p in enumerate(self.programs) if p.name == program_name
            )
        except StopIteration:
            raise ValueError(f"Program '{program_name}' not found in deck.") from None
        return self.programs.pop(index)

    def move_program_up(self, program_name: str) -> None:
        """Moves a specified program one position up in the order."""
        try:
            index = next(
                i for i, p in enumerate(self.programs) if p.name == program_name
            )
        except StopIteration:
            raise ValueError(f"Program '{program_name}' not found in deck.") from None

        if index > 0:
            # Swap with the previous item
            self.programs[index], self.programs[index - 1] = (
                self.programs[index - 1],
                self.programs[index],
            )

    def move_program_down(self, program_name: str) -> None:
        """Moves a specified program one position down in the order."""
        try:
            index = next(
                i for i, p in enumerate(self.programs) if p.name == program_name
            )
        except StopIteration:
            raise ValueError(f"Program '{program_name}' not found in deck.") from None

        if index < len(self.programs) - 1:
            # Swap with the next item
            self.programs[index], self.programs[index + 1] = (
                self.programs[index + 1],
                self.programs[index],
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the aggregate to a dictionary."""
        return {
            "id": str(self.id),
            "programs": [prog.to_dict() for prog in self.programs],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Deck":
        """Reconstitute a Deck from a dictionary."""
        return cls(
            id=DeckId(uuid.UUID(data["id"])),
            programs=[Program.from_dict(p_data) for p_data in data["programs"]],
        )

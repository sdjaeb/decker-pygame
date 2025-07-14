"""This module defines the Character aggregate root."""

import uuid
from typing import Any

from decker_pygame.application.decorators import emits
from decker_pygame.domain.crafting import Schematic
from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.events import (
    CharacterCreated,
    ItemCrafted,
    SkillDecreased,
    SkillIncreased,
)
from decker_pygame.domain.ids import AggregateId, CharacterId, DeckId, ProgramId
from decker_pygame.domain.program import Program


class Character(AggregateRoot):
    """Represents a character aggregate root.

    Args:
        id (CharacterId): Unique identifier for the character.
        name (str): Character's name.
        skills (dict[str, int]): Mapping of skill names to values.
        deck_id (DeckId): The ID of the character's deck.
        stored_programs (list[Program]): List of programs not in the active deck.
        schematics (list[Schematic]): List of known program schematics.
        credits (int): Amount of credits the character has.
        unused_skill_points (int): Points available to spend on skills.
    """

    def __init__(
        self,
        id: CharacterId,
        name: str,
        skills: dict[str, int],
        deck_id: DeckId,
        stored_programs: list[Program],
        schematics: list[Schematic],
        credits: int,
        unused_skill_points: int,
    ) -> None:
        super().__init__(id=AggregateId(id))
        self.name = name
        self.skills = skills
        self.deck_id = deck_id
        self.stored_programs = stored_programs
        self.credits = credits
        self.schematics = schematics
        self.unused_skill_points = unused_skill_points

    @staticmethod
    @emits(CharacterCreated)
    def create(
        character_id: CharacterId,
        name: str,
        deck_id: DeckId,
        initial_skills: dict[str, int],
        initial_credits: int,
        initial_skill_points: int,
    ) -> "Character":
        """Factory to create a new character, raising a CharacterCreated domain event.

        Args:
            character_id (CharacterId): Unique identifier for the character.
            name (str): Character's name.
            deck_id (DeckId): The ID of the character's associated deck.
            initial_skills (dict[str, int]): Initial skills.
            initial_credits (int): Starting credits.
            initial_skill_points (int): Starting skill points.

        Returns:
            "Character": The newly created character.
        """
        character = Character(
            id=character_id,
            name=name,
            skills=initial_skills,
            deck_id=deck_id,
            stored_programs=[],
            schematics=[],
            credits=initial_credits,
            unused_skill_points=initial_skill_points,
        )
        character._events.append(
            CharacterCreated(
                character_id=CharacterId(character.id), name=character.name
            )
        )
        return character

    @emits(ItemCrafted)
    def craft(self, schematic: Schematic) -> None:
        """Crafts an item from a schematic, consuming resources and creating an event.

        Note: Pre-condition checks (e.g., if the character has enough credits)
        are the responsibility of the calling Application Service. This method
        enforces the outcome of the crafting action.

        Args:
            schematic (Schematic): The schematic to use for crafting.

        Raises:
            ValueError: If the character has insufficient credits.
        """
        # Deduct resources
        for resource in schematic.cost:
            if resource.name == "credits":
                if self.credits < resource.quantity:
                    raise ValueError(f"Insufficient credits to craft {schematic.name}.")
                self.credits -= resource.quantity
            # In the future, other resource types would be handled here.

        # Create the new program and add it to inventory
        new_program = Program(
            id=ProgramId(uuid.uuid4()),
            name=schematic.produces_item_name,
            size=schematic.produces_item_size,
        )
        self.stored_programs.append(new_program)

        # Emit the domain event
        self._events.append(
            ItemCrafted(
                character_id=CharacterId(self.id),
                schematic_name=schematic.name,
                item_id=ProgramId(new_program.id),
                item_name=new_program.name,
            )
        )

    def remove_stored_program(self, program_name: str) -> Program:
        """Finds, removes, and returns a program from storage."""
        try:
            index = next(
                i for i, p in enumerate(self.stored_programs) if p.name == program_name
            )
        except StopIteration:
            raise ValueError(
                f"Program '{program_name}' not found in storage."
            ) from None
        return self.stored_programs.pop(index)

    @emits(SkillIncreased)
    def increase_skill(self, skill_name: str) -> None:
        """Increases a skill level if there are enough points."""
        if skill_name not in self.skills:
            raise ValueError(f"Skill '{skill_name}' does not exist.")

        current_level = self.skills[skill_name]
        cost = current_level + 1

        if self.unused_skill_points < cost:
            raise ValueError("Not enough skill points.")

        self.unused_skill_points -= cost
        self.skills[skill_name] += 1
        new_level = self.skills[skill_name]

        self._events.append(
            SkillIncreased(
                character_id=CharacterId(self.id),
                skill_name=skill_name,
                new_level=new_level,
            )
        )

    @emits(SkillDecreased)
    def decrease_skill(self, skill_name: str) -> None:
        """Decreases a skill level and refunds points."""
        if skill_name not in self.skills:
            raise ValueError(f"Skill '{skill_name}' does not exist.")

        current_level = self.skills[skill_name]
        if current_level <= 0:
            raise ValueError("Cannot decrease skill below 0.")

        refund = current_level
        self.unused_skill_points += refund
        self.skills[skill_name] -= 1
        new_level = self.skills[skill_name]

        self._events.append(
            SkillDecreased(
                character_id=CharacterId(self.id),
                skill_name=skill_name,
                new_level=new_level,
            )
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the aggregate to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the Character.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "skills": self.skills,
            "deck_id": str(self.deck_id),
            "stored_programs": [p.to_dict() for p in self.stored_programs],
            "schematics": [s.to_dict() for s in self.schematics],
            "credits": self.credits,
            "unused_skill_points": self.unused_skill_points,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Character":
        """Reconstitute a Character from a dictionary.

        Args:
            data (dict[str, Any]): The dictionary data.

        Returns:
            "Character": A Character instance.
        """
        return cls(
            id=CharacterId(uuid.UUID(data["id"])),
            name=data["name"],
            skills=data["skills"],
            deck_id=DeckId(uuid.UUID(data["deck_id"])),
            stored_programs=[
                Program.from_dict(p_data) for p_data in data.get("stored_programs", [])
            ],
            schematics=[Schematic.from_dict(s_data) for s_data in data["schematics"]],
            credits=data["credits"],
            unused_skill_points=data["unused_skill_points"],
        )

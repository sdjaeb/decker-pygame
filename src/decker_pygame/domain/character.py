from decker_pygame.domain.aggregate import AggregateRoot
from decker_pygame.domain.events import CharacterCreated
from decker_pygame.domain.ids import AggregateId, CharacterId
from decker_pygame.domain.program import Program


class Character(AggregateRoot):
    """Placeholder for the Character aggregate root."""

    def __init__(
        self,
        id: CharacterId,
        name: str,
        skills: dict[str, int],
        inventory: list[Program],
        credits: int,
    ) -> None:
        super().__init__(id=AggregateId(id))
        self.name = name
        self.skills = skills
        self.inventory = inventory
        self.credits = credits

    @staticmethod
    def create(character_id: CharacterId, name: str) -> "Character":
        """Factory to create a new character, raising a domain event."""
        character = Character(
            id=character_id, name=name, skills={}, inventory=[], credits=0
        )
        character._events.append(
            CharacterCreated(
                character_id=CharacterId(character.id), name=character.name
            )
        )
        return character

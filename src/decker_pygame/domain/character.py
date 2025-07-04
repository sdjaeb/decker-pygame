from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.events import CharacterCreated
from decker_pygame.domain.ids import AggregateId, CharacterId
from decker_pygame.domain.program import Program


class Character(AggregateRoot):
    """Represents a character aggregate root."""

    def __init__(
        self,
        id: CharacterId,
        name: str,
        skills: dict[str, int],
        inventory: list[Program],
        credits: int,
    ) -> None:
        """
        Initialize a Character.

        Args:
            id (CharacterId): Unique identifier for the character.
            name (str): Character's name.
            skills (Dict[str, int]): Mapping of skill names to values.
            inventory (List[Program]): List of owned programs.
            credits (int): Amount of credits the character has.
        """
        super().__init__(id=AggregateId(id))
        self.name = name
        self.skills = skills
        self.inventory = inventory
        self.credits = credits

    @staticmethod
    def create(
        character_id: CharacterId,
        name: str,
        initial_skills: dict[str, int],
        initial_credits: int,
    ) -> "Character":
        """
        Factory to create a new character, raising a CharacterCreated domain event.

        Args:
            character_id (CharacterId): Unique identifier for the character.
            name (str): Character's name.
            initial_skills (Dict[str, int]): Initial skills.
            initial_credits (int): Starting credits.

        Returns:
            Character: The newly created character.
        """
        character = Character(
            id=character_id,
            name=name,
            skills=initial_skills,
            inventory=[],
            credits=initial_credits,
        )
        character._events.append(
            CharacterCreated(
                character_id=CharacterId(character.id), name=character.name
            )
        )
        return character

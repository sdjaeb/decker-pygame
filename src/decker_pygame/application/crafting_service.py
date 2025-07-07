from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.crafting import Schematic
from decker_pygame.domain.ids import CharacterId
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface


class CraftingError(Exception):
    """Base exception for crafting-related errors."""

    pass


class SchematicNotFoundError(CraftingError):
    """Raised when a character does not know a specific schematic."""

    pass


class InsufficientResourcesError(CraftingError):
    """Raised when a character does not have the resources to craft an item."""

    pass


class CraftingService:
    """Application service for crafting-related operations."""

    def __init__(
        self,
        character_repo: CharacterRepositoryInterface,
        event_dispatcher: EventDispatcher,
    ) -> None:
        """Initialize the CraftingService."""
        self.character_repo = character_repo
        self.event_dispatcher = event_dispatcher

    def get_character_schematics(self, character_id: CharacterId) -> list[Schematic]:
        """
        Retrieves the list of known schematics for a given character.

        This is a query method to provide data to the presentation layer.

        Args:
            character_id: The ID of the character.

        Returns:
            A list of schematics the character knows.
        """
        character = self.character_repo.get(character_id)
        if not character:
            return []
        return character.schematics

    def craft_item(self, character_id: CharacterId, schematic_name: str) -> None:
        """
        Orchestrates the use case of a character crafting an item.

        Args:
            character_id: The ID of the character who is crafting.
            schematic_name: The name of the schematic to use.

        Raises:
            CraftingError: If crafting fails due to business rule violations.
        """
        character = self.character_repo.get(character_id)
        if not character:
            raise CraftingError(f"Character with ID {character_id} not found.")

        # Find the schematic the character knows
        try:
            schematic_to_use = next(
                s for s in character.schematics if s.name == schematic_name
            )
        except StopIteration:
            raise SchematicNotFoundError(
                f"Character does not know schematic '{schematic_name}'."
            ) from None

        # Execute the domain logic
        try:
            character.craft(schematic_to_use)
        except ValueError as e:
            # Translate domain error into application-specific error
            raise InsufficientResourcesError(str(e)) from e

        # Persist the new state
        self.character_repo.save(character)

        # Dispatch events
        self.event_dispatcher.dispatch(character.events)
        character.clear_events()

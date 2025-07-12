"""Provides the base class for Entities in the domain model."""

import uuid
from typing import Any

EntityId = uuid.UUID  # Type alias for clarity


class Entity:
    """DDD Entity base class.

    An Entity is an object defined by its identity rather than its attributes.
    Entities are compared by their unique identifier, not by value.
    All domain entities should inherit from this class.
    """

    def __init__(self, id: EntityId) -> None:
        """Initialize the entity with a unique identifier.

        Args:
            id (EntityId): The unique identifier for the entity.
        """
        self._id = id  # Private attribute for immutability

    @property
    def id(self) -> EntityId:
        """The unique identifier for the entity (read-only).

        Returns:
            EntityId: The entity's unique identifier.
        """
        return self._id

    def __eq__(self, other: Any) -> bool:
        """Check equality based on entity ID.

        Args:
            other (Any): The object to compare.

        Returns:
            bool: True if IDs are equal, False otherwise.
        """
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Return a hash based on the entity ID.

        Returns:
            int: The hash value.
        """
        return hash(self.id)

import uuid
from typing import Any


class Entity:
    """A base class for domain entities, providing identity and equality."""

    def __init__(self, id: uuid.UUID) -> None:
        self.id = id

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

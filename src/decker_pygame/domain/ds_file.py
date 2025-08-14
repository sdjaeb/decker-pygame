"""This module defines the DSFile domain entity."""

import uuid
from enum import Enum
from typing import Any

from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.ids import AggregateId, DSFileId


class DSFileType(str, Enum):
    """Represents the type of a DSFile."""

    DATA = "data"
    PROGRAM = "program"
    SYSTEM = "system"


class DSFile(AggregateRoot):
    """Represents a file within a datastore in the game world.

    This is an aggregate root, as it will be individually loaded and saved.
    Ported from DSFile.cpp/h.
    """

    id: DSFileId
    name: str
    file_type: DSFileType
    size: int  # in megabytes or some other unit
    content: str  # The actual data or a path to it

    def __init__(
        self, id: DSFileId, name: str, file_type: DSFileType, size: int, content: str
    ) -> None:
        super().__init__(id=AggregateId(id))
        self.name = name
        self.file_type = file_type
        self.size = size
        self.content = content

    def to_dict(self) -> dict[str, Any]:
        """Serialize the aggregate to a dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "file_type": self.file_type.value,
            "size": self.size,
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DSFile":
        """Reconstitute a DSFile from a dictionary."""
        return cls(
            id=DSFileId(uuid.UUID(data["id"])),
            name=data["name"],
            file_type=DSFileType(data["file_type"]),
            size=data["size"],
            content=data["content"],
        )

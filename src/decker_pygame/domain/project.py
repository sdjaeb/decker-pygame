"""This module defines domain objects related to the R&D system."""

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Optional


class ProjectType(Enum):
    """An enumeration for the types of research projects."""

    SOFTWARE = "software"
    CHIP = "chip"


@dataclass
class ActiveProject:
    """A Value Object representing an active research project.

    Attributes:
        project_type (ProjectType): The type of item being researched.
        item_class (str): The specific class of the item (e.g., "Sentry ICE").
        target_rating (int): The rating/level being researched.
        time_required (int): The total time units required to complete the project.
        time_spent (int): The time units already spent on the project.
    """

    project_type: ProjectType
    item_class: str
    target_rating: int
    time_required: int
    time_spent: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize the value object to a dictionary."""
        data = asdict(self)
        data["project_type"] = self.project_type.value
        return data

    @classmethod
    def from_dict(cls, data: Optional[dict[str, Any]]) -> Optional["ActiveProject"]:
        """Reconstitute an ActiveProject from a dictionary."""
        if data is None:
            return None

        # Make a copy to avoid modifying the original dict, then convert the
        # string back to a ProjectType enum before instantiation.
        data_copy = data.copy()
        data_copy["project_type"] = ProjectType(data_copy["project_type"])
        return cls(**data_copy)

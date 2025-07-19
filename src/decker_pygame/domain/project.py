"""This module defines domain objects related to the R&D system."""

from dataclasses import asdict, dataclass
from typing import Any, Optional


@dataclass
class ActiveProject:
    """A Value Object representing an active research project.

    Attributes:
        item_type (str): The type of item being researched (e.g., "software", "chip").
        item_class (str): The specific class of the item (e.g., "Sentry ICE").
        target_rating (int): The rating/level being researched.
        time_required (int): The total time units required to complete the project.
        time_spent (int): The time units already spent on the project.
    """

    item_type: str
    item_class: str
    target_rating: int
    time_required: int
    time_spent: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize the value object to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Optional[dict[str, Any]]) -> Optional["ActiveProject"]:
        """Reconstitute an ActiveProject from a dictionary."""
        if data is None:
            return None
        return cls(**data)

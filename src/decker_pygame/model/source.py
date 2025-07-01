"""
Pydantic model for a Source (a lootable data object).
"""

from pydantic import BaseModel, Field


class Source(BaseModel):
    """Represents a data source or other lootable object within a node."""

    name: str
    data_value: int = Field(
        default=0, ge=0, description="The value of the data if accessed."
    )
    is_looted: bool = Field(
        default=False, description="Whether the source has been accessed/looted."
    )

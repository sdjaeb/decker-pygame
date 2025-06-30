from typing import Annotated

from pydantic import BaseModel, Field


class Character(BaseModel):
    """Represents the player character or an NPC."""

    name: str
    skills: dict[str, int] = Field(default_factory=dict)
    inventory: list[int] = Field(default_factory=list)  # Assuming item IDs
    # Use Annotated and Field to ensure credits are non-negative
    credits: Annotated[int, Field(ge=0)] = 0

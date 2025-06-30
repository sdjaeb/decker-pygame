from pydantic import BaseModel, Field, conint


class Character(BaseModel):
    """Represents the player character or an NPC."""

    name: str
    skills: dict[str, int] = Field(default_factory=dict)
    inventory: list[int] = Field(default_factory=list)  # Assuming item IDs
    # Use conint (constrained integer) to ensure credits are non-negative
    credits: conint(ge=0) = 0

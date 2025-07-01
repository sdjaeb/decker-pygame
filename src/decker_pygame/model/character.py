from pydantic import BaseModel, Field

from decker_pygame.model.program import Program


class Character(BaseModel):
    """Represents the player character or an NPC."""

    name: str
    skills: dict[str, int] = Field(default_factory=dict)
    inventory: list[Program] = Field(default_factory=list)
    credits: int = Field(default=0, ge=0)

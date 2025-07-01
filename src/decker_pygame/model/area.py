from pydantic import BaseModel, Field

from decker_pygame.model.contract import Contract


class Area(BaseModel):
    """Represents a distinct location or node within the game world/cyberspace."""

    id: int
    name: str
    description: str
    security_level: int
    connected_areas: list[int] = Field(default_factory=list)
    contracts: list[Contract] = Field(default_factory=list)

"""
Pydantic model for a Program.
"""

from pydantic import BaseModel, Field

from decker_pygame.model.enums import ProgramType


class Program(BaseModel):
    """Represents a hacking program a character can own or buy."""

    name: str
    type: ProgramType
    size: int = Field(..., gt=0, description="The memory size the program occupies.")
    cost: int = Field(..., ge=0, description="The purchase cost of the program.")
    description: str

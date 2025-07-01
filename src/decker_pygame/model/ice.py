"""
Pydantic model for ICE (Intrusion Countermeasures Electronics).
"""

from pydantic import BaseModel, Field

from decker_pygame.model.enums import IceType


class Ice(BaseModel):
    """Represents a security program (ICE) in a system node."""

    name: str
    type: IceType
    strength: int = Field(..., ge=0, description="The strength or rating of the ICE.")
    is_active: bool = Field(
        default=False, description="Whether the ICE has been triggered."
    )

"""
Pydantic model for a System.
"""

from pydantic import BaseModel, Field

from decker_pygame.model.node import Node


class System(BaseModel):
    """Represents a full computer system, composed of multiple nodes."""

    name: str  # e.g., "Saeder-Krupp Corporate HQ"
    alert_level: float = Field(
        default=0.0,
        ge=0.0,
        description="The current security alert level of the system.",
    )
    nodes: list[Node] = Field(default_factory=list)

"""
Pydantic model for a Node in a System.
"""

from pydantic import BaseModel, Field

from decker_pygame.model.ice import Ice
from decker_pygame.model.source import Source


class Node(BaseModel):
    """Represents a single node within a computer system."""

    name: str
    ice: list[Ice] = Field(
        default_factory=list, description="ICE protecting this node."
    )
    sources: list[Source] = Field(
        default_factory=list, description="Data sources within this node."
    )
    # Connections to other nodes could be represented by their names/IDs
    connections: list[str] = Field(
        default_factory=list, description="List of connected node names/IDs."
    )
    is_breached: bool = Field(
        default=False, description="Whether the node's security has been breached."
    )

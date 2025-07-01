"""
Centralized enumerations for Pydantic models and game logic.
"""

from enum import Enum


class IceType(str, Enum):
    """Enumeration for ICE types."""

    BLACK = "Black"
    WHITE = "White"
    GRAY = "Gray"


class ProgramType(str, Enum):
    """Enumeration for Program types."""

    ATTACK = "Attack"
    STEALTH = "Stealth"
    UTILITY = "Utility"
    DEFENSE = "Defense"

"""
General-purpose utility functions.

This module is intended to hold helper functions ported from the original
Global.cpp or created as needed for common tasks.
"""


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamps a value between a minimum and maximum."""
    return max(min_value, min(value, max_value))

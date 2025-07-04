"""
General-purpose utility functions.

This module is intended to hold helper functions ported from the original
Global.cpp or created as needed for common tasks.
"""


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a value between a minimum and maximum.

    Args:
        value (float): The value to clamp.
        min_value (float): The minimum allowed value.
        max_value (float): The maximum allowed value.

    Returns:
        float: The clamped value.
    """
    return max(min_value, min(value, max_value))

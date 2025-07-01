import pytest

from decker_pygame.utils import clamp


@pytest.mark.parametrize(
    "value, min_val, max_val, expected",
    [
        (5, 0, 10, 5),  # Value within range
        (-5, 0, 10, 0),  # Value below minimum
        (15, 0, 10, 10),  # Value above maximum
        (0, 0, 10, 0),  # Value at minimum boundary
        (10, 0, 10, 10),  # Value at maximum boundary
        (5.5, 0.0, 10.0, 5.5),  # Float value
        (-1.1, -1.0, 1.0, -1.0),  # Float below min
        (1.1, -1.0, 1.0, 1.0),  # Float above max
    ],
)
def test_clamp(value, min_val, max_val, expected):
    """Tests the clamp function with various inputs."""
    assert clamp(value, min_val, max_val) == expected

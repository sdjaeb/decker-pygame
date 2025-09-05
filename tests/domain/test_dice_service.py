"""Tests for the DiceService."""

from unittest.mock import patch

import pytest

from decker_pygame.domain.dice_service import DiceService


@pytest.fixture
def dice_service() -> DiceService:
    """Provides a DiceService instance for tests."""
    return DiceService()


def test_dice_roll(dice_service: DiceService):
    """Tests a standard dice roll with a modifier."""
    # Mock random.randint to return predictable values
    with patch("random.randint", side_effect=[3, 5, 1]) as mock_randint:
        # Roll 3d6+2
        result = dice_service.roll(3, 6, 2)

        # The result should be the sum of the mocked rolls plus the modifier
        assert result == 3 + 5 + 1 + 2
        assert mock_randint.call_count == 3

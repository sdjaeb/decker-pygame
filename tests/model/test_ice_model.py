import pytest
from pydantic import ValidationError

from decker_pygame.model.enums import IceType
from decker_pygame.model.ice import Ice


def test_ice_creation():
    """Tests basic creation of an Ice instance."""
    ice = Ice(name="Tar Pit", type=IceType.BLACK, strength=5)
    assert ice.name == "Tar Pit"
    assert ice.type == IceType.BLACK
    assert ice.strength == 5
    assert ice.is_active is False


def test_ice_default_values():
    """Tests that default values are applied correctly."""
    ice = Ice(name="Trace", type=IceType.WHITE, strength=3)
    assert ice.is_active is False


def test_ice_strength_validation():
    """Tests that negative strength raises a validation error."""
    with pytest.raises(ValidationError):
        Ice(name="Invalid ICE", type=IceType.GRAY, strength=-1)

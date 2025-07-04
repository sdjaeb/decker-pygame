import uuid

from decker_pygame.domain.ice import Ice
from decker_pygame.domain.ids import IceId


def test_ice_creation():
    """Tests creating an ICE entity."""
    ice_id = IceId(uuid.uuid4())
    ice = Ice(id=ice_id, name="BlackICE", strength=10)

    assert ice.id == ice_id
    assert ice.name == "BlackICE"
    assert ice.strength == 10

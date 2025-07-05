import uuid

from decker_pygame.domain.ice import Ice
from decker_pygame.domain.ids import IceId


def test_ice_serialization_roundtrip():
    """Tests that an Ice entity can be serialized and deserialized correctly."""
    ice_id = IceId(uuid.uuid4())
    original_ice = Ice(id=ice_id, name="Black Ice", strength=8)

    ice_dict = original_ice.to_dict()

    assert ice_dict == {"id": str(ice_id), "name": "Black Ice", "strength": 8}

    reconstituted_ice = Ice.from_dict(ice_dict)

    assert reconstituted_ice == original_ice
    assert reconstituted_ice.name == original_ice.name
    assert reconstituted_ice.strength == original_ice.strength

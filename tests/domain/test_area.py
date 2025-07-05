import uuid

from decker_pygame.domain.area import Area
from decker_pygame.domain.ids import AreaId, ContractId


def test_area_serialization_roundtrip():
    """Tests that an Area can be serialized and deserialized correctly."""
    area_id = AreaId(uuid.uuid4())
    contract_id = ContractId(uuid.uuid4())
    original_area = Area(
        id=area_id,
        name="Downtown",
        description="The bustling city center.",
        security_level=3,
        contract_ids=[contract_id],
    )

    area_dict = original_area.to_dict()

    assert area_dict == {
        "id": str(area_id),
        "name": "Downtown",
        "description": "The bustling city center.",
        "security_level": 3,
        "contract_ids": [str(contract_id)],
    }

    reconstituted_area = Area.from_dict(area_dict)

    assert reconstituted_area == original_area
    assert reconstituted_area.name == original_area.name
    assert reconstituted_area.contract_ids == original_area.contract_ids


def test_area_add_contract():
    """Tests that adding a contract correctly modifies the area."""
    area = Area(
        id=AreaId(uuid.uuid4()),
        name="The Sprawl",
        description="Urban decay and high tech.",
        security_level=5,
        contract_ids=[],
    )
    assert not area.contract_ids

    new_contract_id = ContractId(uuid.uuid4())
    area.add_contract(new_contract_id)

    assert len(area.contract_ids) == 1
    assert area.contract_ids[0] == new_contract_id

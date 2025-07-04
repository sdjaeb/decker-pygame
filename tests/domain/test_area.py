import uuid

from decker_pygame.domain.area import Area
from decker_pygame.domain.contract import Contract
from decker_pygame.domain.ids import AreaId, ContractId


def test_area_creation():
    """Tests creating an area with default empty contracts."""
    area = Area(
        id=AreaId(uuid.uuid4()),
        name="Downtown",
        description="The neon-drenched heart of the city.",
        security_level=3,
        contract_ids=[],
    )
    assert area.name == "Downtown"
    assert area.contract_ids == []


def test_area_with_contracts():
    """Tests creating an area with a list of contracts."""
    area_id = AreaId(uuid.uuid4())
    contract = Contract(
        id=ContractId(uuid.uuid4()),
        title="Data Heist",
        client="Anonymous",
        target_area_id=area_id,
        description="...",
        reward_credits=5000,
    )
    area = Area(
        id=area_id,
        name="Corporate Plaza",
        description="...",
        security_level=5,
        contract_ids=[],
    )
    area.add_contract(ContractId(contract.id))

    assert len(area.contract_ids) == 1
    assert area.contract_ids[0] == contract.id

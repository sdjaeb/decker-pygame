import uuid

from decker_pygame.domain.contract import Contract
from decker_pygame.domain.ids import AreaId, ContractId


def test_contract_creation():
    """Tests creating a contract."""
    contract = Contract(
        id=ContractId(uuid.uuid4()),
        title="Data Heist",
        client="Anonymous",
        target_area_id=AreaId(uuid.uuid4()),
        description="...",
        reward_credits=5000,
    )

    assert contract.title == "Data Heist"
    assert contract.reward_credits == 5000


def test_contract_equality():
    """Contracts should be equal if they have the same ID."""
    contract_id = ContractId(uuid.uuid4())
    area_id = AreaId(uuid.uuid4())
    contract1 = Contract(contract_id, "c1", "client1", area_id, "desc1", 100)
    contract2 = Contract(contract_id, "c2", "client2", area_id, "desc2", 200)
    contract3 = Contract(
        ContractId(uuid.uuid4()), "c1", "client1", area_id, "desc1", 100
    )

    assert contract1 == contract2
    assert contract1 != contract3
    assert contract1 != "not a contract"


def test_contract_hash():
    """Contracts with the same ID should have the same hash."""
    contract_id = ContractId(uuid.uuid4())
    area_id = AreaId(uuid.uuid4())
    contract1 = Contract(contract_id, "c1", "client1", area_id, "desc1", 100)
    contract2 = Contract(contract_id, "c2", "client2", area_id, "desc2", 200)

    assert hash(contract1) == hash(contract2)
    assert len({contract1, contract2}) == 1

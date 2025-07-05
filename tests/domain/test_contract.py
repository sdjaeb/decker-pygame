import uuid

from decker_pygame.domain.contract import Contract
from decker_pygame.domain.ids import AreaId, ContractId


def test_contract_serialization_roundtrip():
    """Tests that a Contract can be serialized and deserialized correctly."""
    contract_id = ContractId(uuid.uuid4())
    area_id = AreaId(uuid.uuid4())
    original_contract = Contract(
        id=contract_id,
        title="Data Heist",
        client="Ares Corp",
        target_area_id=area_id,
        description="Steal the data.",
        reward_credits=5000,
    )

    contract_dict = original_contract.to_dict()

    reconstituted_contract = Contract.from_dict(contract_dict)

    assert reconstituted_contract == original_contract
    assert reconstituted_contract.title == original_contract.title
    assert reconstituted_contract.client == original_contract.client
    assert reconstituted_contract.target_area_id == original_contract.target_area_id
    assert reconstituted_contract.description == original_contract.description
    assert reconstituted_contract.reward_credits == original_contract.reward_credits

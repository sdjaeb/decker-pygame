import os
import tempfile
import uuid

from decker_pygame.domain.contract import Contract
from decker_pygame.domain.ids import AreaId, ContractId
from decker_pygame.infrastructure.json_contract_repository import (
    JsonFileContractRepository,
)


def test_save_and_get_contract():
    """Tests that a contract can be saved and retrieved."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonFileContractRepository(base_path=tmpdir)
        contract_id = ContractId(uuid.uuid4())
        contract = Contract(
            id=contract_id,
            title="Test Contract",
            client="Test Corp",
            target_area_id=AreaId(uuid.uuid4()),
            description="A test contract.",
            reward_credits=1000,
        )

        repo.save(contract)

        retrieved_contract = repo.get(contract_id)

        assert retrieved_contract is not None
        assert retrieved_contract.id == contract.id
        assert retrieved_contract.title == "Test Contract"


def test_get_all_contracts():
    """Tests that all contracts can be retrieved."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonFileContractRepository(base_path=tmpdir)

        # Create and save two contracts
        contract1 = Contract(
            id=ContractId(uuid.uuid4()),
            title="Contract 1",
            client="Client A",
            target_area_id=AreaId(uuid.uuid4()),
            description="First",
            reward_credits=100,
        )
        contract2 = Contract(
            id=ContractId(uuid.uuid4()),
            title="Contract 2",
            client="Client B",
            target_area_id=AreaId(uuid.uuid4()),
            description="Second",
            reward_credits=200,
        )
        repo.save(contract1)
        repo.save(contract2)

        all_contracts = repo.get_all()
        assert len(all_contracts) == 2
        assert {c.title for c in all_contracts} == {"Contract 1", "Contract 2"}


def test_get_all_with_corrupted_file():
    """Tests that get_all skips corrupted or invalid JSON files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonFileContractRepository(base_path=tmpdir)

        # Create a valid contract
        valid_contract = Contract(
            id=ContractId(uuid.uuid4()),
            title="Valid Contract",
            client="Good Client",
            target_area_id=AreaId(uuid.uuid4()),
            description="This one works.",
            reward_credits=100,
        )
        repo.save(valid_contract)

        # Create a corrupted file
        with open(os.path.join(tmpdir, "corrupted.json"), "w") as f:
            f.write("{not_a_valid_json:")

        all_contracts = repo.get_all()
        assert len(all_contracts) == 1
        assert all_contracts[0].id == valid_contract.id


def test_get_nonexistent_contract():
    """Tests that get returns None for a non-existent contract."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonFileContractRepository(base_path=tmpdir)
        contract_id = ContractId(uuid.uuid4())

        retrieved_contract = repo.get(contract_id)

        assert retrieved_contract is None


def test_repository_creates_directory_on_init():
    """Tests that the repository creates its base directory if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        new_dir_path = os.path.join(tmpdir, "new_contracts")
        assert not os.path.exists(new_dir_path)

        JsonFileContractRepository(base_path=new_dir_path)

        assert os.path.exists(new_dir_path)


def test_get_all_on_nonexistent_directory():
    """Tests that get_all returns an empty list if the base path doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        non_existent_path = os.path.join(tmpdir, "non_existent")
        # __init__ will create it, so we must delete it after.
        repo = JsonFileContractRepository(base_path=non_existent_path)
        os.rmdir(non_existent_path)

        contracts = repo.get_all()
        assert contracts == []

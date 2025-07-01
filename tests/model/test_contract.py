import pytest
from pydantic import ValidationError

from decker_pygame.model.contract import Contract


def test_contract_creation():
    """Tests basic creation of a Contract."""
    contract = Contract(
        id=1,
        title="Smash and Grab",
        client="Mr. Johnson",
        target_area_id=2,
        description="...",
        reward_credits=1000,
    )
    assert contract.id == 1
    assert contract.title == "Smash and Grab"
    assert contract.client == "Mr. Johnson"
    assert contract.target_area_id == 2
    assert contract.reward_credits == 1000
    assert contract.objectives == []
    assert contract.is_completed is False


def test_contract_validation():
    """Tests that a negative reward raises a validation error."""
    with pytest.raises(ValidationError):
        # This should fail because reward_credits cannot be negative.
        Contract(
            id=2,
            title="Bad Contract",
            client="Shady Corp",
            target_area_id=3,
            description="...",
            reward_credits=-100,
        )

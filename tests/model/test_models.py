import pytest
from decker_pygame.model.area import Area
from decker_pygame.model.character import Character
from decker_pygame.model.contract import Contract
from pydantic import ValidationError


def test_character_creation_defaults():
    """Tests that a Character can be created with default values."""
    char = Character(name="Test Decker")
    assert char.name == "Test Decker"
    assert char.skills == {}
    assert char.inventory == []
    assert char.credits == 0


def test_character_creation_with_values():
    """Tests that a Character can be created with specific values."""
    skills = {"hacking": 5, "electronics": 3}
    inventory = [101, 203]
    char = Character(name="Jax", skills=skills, inventory=inventory, credits=5000)
    assert char.name == "Jax"
    assert char.skills == {"hacking": 5, "electronics": 3}
    assert char.inventory == [101, 203]
    assert char.credits == 5000


def test_area_creation_defaults():
    """Tests that an Area can be created with default values."""
    area = Area(id=1, name="City Grid", description="Main hub", security_level=2)
    assert area.id == 1
    assert area.name == "City Grid"
    assert area.description == "Main hub"
    assert area.security_level == 2
    assert area.connected_areas == []


def test_contract_creation_defaults():
    """Tests that a Contract can be created with default values."""
    contract = Contract(
        id=101,
        title="Data Heist",
        description="Steal the data.",
        client="Mr. Johnson",
        target_area_id=5,
    )
    assert contract.id == 101
    assert contract.title == "Data Heist"
    assert contract.objectives == []
    assert contract.reward_credits == 0
    assert contract.is_completed is False


def test_character_creation_invalid_credits():
    """Tests that creating a Character with negative credits raises an error."""
    with pytest.raises(ValidationError) as excinfo:
        Character(name="Broke Bob", credits=-100)
    # Check that the error message is informative
    assert "Input should be greater than or equal to 0" in str(excinfo.value)


def test_contract_creation_invalid_reward():
    """Tests that creating a Contract with a negative reward raises an error."""
    with pytest.raises(ValidationError):
        Contract(
            id=102,
            title="Bad Deal",
            description="This is a scam.",
            client="Scammer",
            target_area_id=1,
            reward_credits=-500,
        )

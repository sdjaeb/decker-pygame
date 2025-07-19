"""This module contains tests for the domain objects related to crafting."""

from decker_pygame.domain.crafting import RequiredResource, Schematic


def test_schematic_serialization_roundtrip():
    """Tests that a Schematic can be serialized to and from a dictionary."""
    schematic = Schematic(
        name="Test Schematic",
        produces_item_name="Test Item",
        produces_item_size=10,
        rating=1,
        cost=[RequiredResource(name="credits", quantity=100)],
    )

    data = schematic.to_dict()

    assert data == {
        "name": "Test Schematic",
        "produces_item_name": "Test Item",
        "produces_item_size": 10,
        "rating": 1,
        "cost": [{"name": "credits", "quantity": 100}],
    }

    reconstituted = Schematic.from_dict(data)
    assert reconstituted == schematic

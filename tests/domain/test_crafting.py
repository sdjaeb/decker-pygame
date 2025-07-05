from decker_pygame.domain.crafting import RequiredResource, Schematic


def test_schematic_serialization_roundtrip():
    """Tests that a Schematic can be serialized and deserialized correctly."""
    original_schematic = Schematic(
        name="IcePick v1 Schematic",
        produces_item_name="IcePick v1",
        cost=[RequiredResource(name="credits", quantity=500)],
    )

    schematic_dict = original_schematic.to_dict()

    assert schematic_dict == {
        "name": "IcePick v1 Schematic",
        "produces_item_name": "IcePick v1",
        "cost": [{"name": "credits", "quantity": 500}],
    }

    reconstituted_schematic = Schematic.from_dict(schematic_dict)

    assert reconstituted_schematic == original_schematic

from decker_pygame.domain.crafting import RequiredResource, Schematic


def test_schematic_serialization_roundtrip():
    """Tests that a Schematic can be serialized and deserialized correctly."""
    schematic = Schematic(
        name="IcePick",
        produces_item_name="IcePick v1",
        produces_item_size=10,
        cost=[RequiredResource("credits", 100)],
    )
    schematic_dict = schematic.to_dict()

    assert schematic_dict == {
        "name": "IcePick",
        "produces_item_name": "IcePick v1",
        "produces_item_size": 10,
        "cost": [{"name": "credits", "quantity": 100}],
    }

    reconstituted_schematic = Schematic.from_dict(schematic_dict)
    assert reconstituted_schematic == schematic

# from decker_pygame.domain.model.area import Area
# from decker_pygame.domain.contract import Contract


from decker_pygame.model.area import Area
from decker_pygame.model.contract import Contract


def test_area_creation():
    """Tests creating an area with default empty contracts."""
    area = Area(
        id=1,
        name="Downtown",
        description="The neon-drenched heart of the city.",
        security_level=3,
    )
    assert area.name == "Downtown"
    assert area.contracts == []


def test_area_with_contracts():
    """Tests creating an area with a list of contracts."""
    contract = Contract(
        id=101,
        title="Data Heist",
        client="Anonymous",
        target_area_id=2,
        description="...",
        reward_credits=5000,
    )
    area = Area(
        id=2,
        name="Corporate Plaza",
        description="...",
        security_level=5,
        contracts=[contract],
    )
    assert len(area.contracts) == 1
    assert area.contracts[0].title == "Data Heist"

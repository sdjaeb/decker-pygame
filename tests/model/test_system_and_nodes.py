import pytest
from pydantic import ValidationError

from decker_pygame.model.enums import IceType
from decker_pygame.model.ice import Ice
from decker_pygame.model.node import Node
from decker_pygame.model.source import Source
from decker_pygame.model.system import System


def test_source_creation():
    """Tests basic creation of a Source."""
    source = Source(name="Corp Secrets", data_value=10000)
    assert source.name == "Corp Secrets"
    assert source.data_value == 10000
    assert source.is_looted is False


def test_source_validation():
    """Tests validation for Source."""
    with pytest.raises(ValidationError):
        Source(name="Bad Data", data_value=-500)


def test_node_creation():
    """Tests creation of a Node with ICE and Sources."""
    ice1 = Ice(name="Killer", type=IceType.BLACK, strength=7)
    source1 = Source(name="Payroll", data_value=5000)
    node = Node(
        name="CPU",
        ice=[ice1],
        sources=[source1],
        connections=["Memory", "Sub-processor"],
    )
    assert node.name == "CPU"
    assert len(node.ice) == 1
    assert node.ice[0].name == "Killer"
    assert len(node.sources) == 1
    assert node.sources[0].name == "Payroll"
    assert node.connections == ["Memory", "Sub-processor"]
    assert node.is_breached is False


def test_empty_node_creation():
    """Tests creating a node with default empty lists."""
    node = Node(name="Empty Node")
    assert node.ice == []
    assert node.sources == []
    assert node.connections == []


def test_system_creation():
    """Tests creation of a System with nodes."""
    node1 = Node(name="Entrypoint")
    node2 = Node(name="Core CPU")
    system = System(name="Ares Macrotechnology", nodes=[node1, node2])
    assert system.name == "Ares Macrotechnology"
    assert len(system.nodes) == 2
    assert system.nodes[0].name == "Entrypoint"
    assert system.alert_level == 0.0


def test_system_validation():
    """Tests validation for System."""
    with pytest.raises(ValidationError):
        System(name="Bad System", alert_level=-1.0)

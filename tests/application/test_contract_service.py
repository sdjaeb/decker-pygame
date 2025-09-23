import uuid
from unittest.mock import MagicMock, Mock

from decker_pygame.application.contract_service import ContractService
from decker_pygame.application.dtos import ContractSummaryDTO
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.contract import Contract
from decker_pygame.domain.ids import AreaId, ContractId
from decker_pygame.ports.repository_interfaces import ContractRepositoryInterface


def make_domain_contract(id_: str, title: str, client: str, reward: int):
    """Create a simple domain-like object with the attributes used by the DTO."""
    obj = MagicMock()
    obj.id = id_
    obj.title = title
    obj.client = client
    obj.reward_credits = reward
    return obj


def test_get_available_contracts_converts_to_dto():
    # Arrange: repository returns two simple domain objects
    repo = MagicMock()
    domain_contracts = [
        make_domain_contract("c1", "Fix Bug", "ACME", 100),
        make_domain_contract("c2", "Write Patch", "Globex", 250),
    ]
    repo.get_all.return_value = domain_contracts

    # Event dispatcher isn't used by this method, provide a dummy
    event_dispatcher = MagicMock()

    svc = ContractService(contract_repo=repo, event_dispatcher=event_dispatcher)

    # Act
    summaries = svc.get_available_contracts()

    # Assert
    assert len(summaries) == 2
    assert isinstance(summaries[0], ContractSummaryDTO)
    assert summaries[0].id == domain_contracts[0].id
    assert summaries[0].title == domain_contracts[0].title
    assert summaries[0].client == domain_contracts[0].client
    assert summaries[0].reward == domain_contracts[0].reward_credits


def test_contract_service_initialization():
    """Tests that the service initializes correctly."""
    mock_repo = Mock(spec=ContractRepositoryInterface)
    mock_dispatcher = Mock(spec=EventDispatcher)

    service = ContractService(contract_repo=mock_repo, event_dispatcher=mock_dispatcher)

    assert service.contract_repo is mock_repo
    assert service.event_dispatcher is mock_dispatcher


def test_get_available_contracts():
    """Tests that the service correctly retrieves and maps contracts to DTOs."""
    mock_repo = Mock(spec=ContractRepositoryInterface)
    mock_dispatcher = Mock()

    # Create a mock domain object
    contract_id = ContractId(uuid.uuid4())
    mock_contract = Contract(
        id=contract_id,
        title="Test Contract",
        client="Test Corp",
        target_area_id=AreaId(uuid.uuid4()),
        description="A test.",
        reward_credits=5000,
    )
    mock_repo.get_all.return_value = [mock_contract]

    service = ContractService(contract_repo=mock_repo, event_dispatcher=mock_dispatcher)

    # Act
    summaries = service.get_available_contracts()

    # Assert
    mock_repo.get_all.assert_called_once()
    assert len(summaries) == 1
    summary = summaries[0]
    assert isinstance(summary, ContractSummaryDTO)
    assert summary.id == contract_id
    assert summary.title == "Test Contract"
    assert summary.reward == 5000

import uuid
from unittest.mock import Mock

from decker_pygame.application.contract_service import (
    ContractService,
    ContractSummaryDTO,
)
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.contract import Contract
from decker_pygame.domain.ids import AreaId, ContractId
from decker_pygame.ports.repository_interfaces import ContractRepositoryInterface


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

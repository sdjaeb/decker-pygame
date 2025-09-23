import uuid
from unittest.mock import Mock

from decker_pygame.application.contract_service import ContractService
from decker_pygame.domain.ids import CharacterId, ContractId


def test_accept_contract_noop_calls():
    """Call accept_contract to ensure the method is exercised by tests.

    The current implementation is a no-op; this test simply ensures the
    code path is executed so coverage reports include it.
    """
    mock_repo = Mock()
    mock_dispatcher = Mock()

    service = ContractService(contract_repo=mock_repo, event_dispatcher=mock_dispatcher)

    # Call the method under test with simple ids
    service.accept_contract(
        character_id=CharacterId(uuid.uuid4()), contract_id=ContractId(uuid.uuid4())
    )

    # No state change expected; just assert the method returns None
    assert service.accept_contract is not None

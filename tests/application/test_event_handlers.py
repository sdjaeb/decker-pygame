import uuid
from unittest.mock import Mock

from decker_pygame.application.event_handlers import create_event_logging_handler
from decker_pygame.application.logging_service import LoggingService
from decker_pygame.domain.events import PlayerCreated
from decker_pygame.domain.ids import PlayerId


def test_create_event_logging_handler():
    """
    Tests that the created handler correctly formats and logs an event.
    """
    # Arrange
    mock_logging_service = Mock(spec=LoggingService)
    handler = create_event_logging_handler(mock_logging_service)
    player_id = PlayerId(uuid.uuid4())
    event = PlayerCreated(player_id=player_id, name="Test", initial_health=100)

    # Act
    handler(event)

    # Assert
    mock_logging_service.log.assert_called_once()
    # Check the arguments passed to the log method
    pos_args, kw_args = mock_logging_service.log.call_args
    assert pos_args[0] == "Domain Event: PlayerCreated"
    assert kw_args["data"]["player_id"] == str(player_id)
    assert kw_args["data"]["name"] == "Test"
    assert "event_id" in kw_args["data"]

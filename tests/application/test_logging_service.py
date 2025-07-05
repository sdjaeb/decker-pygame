from unittest.mock import Mock

from decker_pygame.application.logging_service import (
    ConsoleLogWriter,
    LoggingService,
    LogWriter,
)


def test_logging_service_dispatches_to_writers():
    """Tests that the service calls the write method on all registered writers."""
    # Arrange
    mock_writer1 = Mock(spec=LogWriter)
    mock_writer2 = Mock(spec=LogWriter)
    service = LoggingService(writers=[mock_writer1, mock_writer2])
    message = "Test message"
    data = {"key": "value"}

    # Act
    service.log(message, data)

    # Assert
    mock_writer1.write.assert_called_once_with(message, data)
    mock_writer2.write.assert_called_once_with(message, data)


def test_logging_service_register():
    """Tests that the register method correctly adds a new writer."""
    # Arrange
    mock_writer1 = Mock(spec=LogWriter)
    mock_writer2 = Mock(spec=LogWriter)
    # Start with one writer
    service = LoggingService(writers=[mock_writer1])

    # Act
    # Register a second writer
    service.register(mock_writer2)

    # Log a message to see if both are called
    message = "Test message"
    data = {"key": "value"}
    service.log(message, data)

    # Assert
    mock_writer1.write.assert_called_once_with(message, data)
    mock_writer2.write.assert_called_once_with(message, data)


def test_logging_service_register_from_empty():
    """Tests that the register method correctly adds a new writer."""
    # Arrange
    service = LoggingService(writers=[])  # Start with no writers
    mock_writer = Mock(spec=LogWriter)

    # Act
    service.register(mock_writer)

    # Assert by logging a message and checking if the new writer is called
    service.log("test", {})
    mock_writer.write.assert_called_once_with("test", {})


def test_console_log_writer(capsys):
    """Tests that the console writer prints a formatted JSON string."""
    writer = ConsoleLogWriter()
    writer.write("Test", {"id": 1})

    captured = capsys.readouterr()
    assert '"message": "Test"' in captured.out
    assert '"id": 1' in captured.out

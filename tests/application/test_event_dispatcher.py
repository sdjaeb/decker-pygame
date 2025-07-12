import uuid
from unittest.mock import Mock

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.events import BaseEvent, CharacterCreated, PlayerCreated
from decker_pygame.domain.ids import CharacterId, PlayerId


def test_event_dispatcher():
    """Verify that the dispatcher calls the correct subscriber for an event."""
    # Arrange
    dispatcher = EventDispatcher()
    mock_subscriber = Mock()
    mock_other_subscriber = Mock()

    # A generic event that should not be handled
    generic_event = BaseEvent()
    # The specific event we are subscribing to
    player_created_event = PlayerCreated(
        player_id=PlayerId(uuid.uuid4()), name="Test", initial_health=100
    )

    dispatcher.subscribe(PlayerCreated, mock_subscriber)
    dispatcher.subscribe(BaseEvent, mock_other_subscriber)

    # Act
    dispatcher.dispatch([generic_event, player_created_event])

    # Assert
    mock_subscriber.assert_called_once_with(player_created_event)
    mock_other_subscriber.assert_called_once_with(generic_event)


def test_event_dispatcher_with_condition():
    """Verify that conditional subscribers are only called if their condition is met."""
    # Arrange
    dispatcher = EventDispatcher()
    conditional_subscriber = Mock()
    unmet_conditional_subscriber = Mock()

    event = PlayerCreated(
        player_id=PlayerId(uuid.uuid4()), name="Test", initial_health=100
    )
    other_event = CharacterCreated(character_id=CharacterId(uuid.uuid4()), name="Other")

    # This subscriber should be called because the condition is true
    dispatcher.subscribe(
        PlayerCreated, conditional_subscriber, condition=lambda e: e.name == "Test"
    )
    # This subscriber should NOT be called because the condition is false
    dispatcher.subscribe(
        PlayerCreated,
        unmet_conditional_subscriber,
        condition=lambda e: e.name == "Fail",
    )

    # Act
    dispatcher.dispatch([event, other_event])

    # Assert
    conditional_subscriber.assert_called_once_with(event)
    unmet_conditional_subscriber.assert_not_called()

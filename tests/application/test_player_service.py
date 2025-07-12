import uuid
from unittest.mock import Mock, patch

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.application.player_service import (
    PlayerService,
    PlayerStatusDTO,
)
from decker_pygame.domain.player import Player, PlayerId
from decker_pygame.ports.repository_interfaces import PlayerRepositoryInterface


def test_create_new_player():
    """
    Verify the PlayerService correctly orchestrates player creation.
    """
    # Arrange
    mock_repo = Mock(spec=PlayerRepositoryInterface)
    mock_dispatcher = Mock(spec=EventDispatcher)
    player_service = PlayerService(
        player_repo=mock_repo, event_dispatcher=mock_dispatcher
    )
    player_name = "Deckard"

    # We patch uuid.uuid4 to have a predictable ID
    test_uuid = uuid.uuid4()
    expected_player_id = PlayerId(test_uuid)

    # We need to patch uuid where it's used: in the services module
    with patch(
        "decker_pygame.application.player_service.uuid.uuid4", return_value=test_uuid
    ):
        # We also patch the Player.create factory
        with patch(
            "decker_pygame.application.player_service.Player.create"
        ) as mock_player_create:
            # Configure the mock that Player.create will return.
            # It must have an `id` attribute to avoid an AttributeError in the service.
            mock_created_player = Mock(spec=Player)
            mock_created_player.id = expected_player_id
            mock_created_player.events = []  # Mock the events list
            mock_player_create.return_value = mock_created_player

            # Act
            returned_player_id = player_service.create_new_player(name=player_name)

            # Assert
            # 1. Check that the returned ID is the one we configured
            assert returned_player_id == expected_player_id

            # 2. Check that the factory was called with the correct arguments
            mock_player_create.assert_called_once_with(
                player_id=expected_player_id, name=player_name, initial_health=100
            )

            # 3. Check that the repository saved the mock player we configured
            mock_repo.save.assert_called_once_with(mock_created_player)

            # 4. Check that the dispatcher was called with the player's events
            mock_dispatcher.dispatch.assert_called_once_with(mock_created_player.events)
            mock_created_player.clear_events.assert_called_once()


def test_get_player_status():
    """Tests retrieving player status for the UI."""
    # Arrange
    mock_repo = Mock(spec=PlayerRepositoryInterface)
    player_service = PlayerService(player_repo=mock_repo, event_dispatcher=Mock())
    player_id = PlayerId(uuid.uuid4())

    mock_player = Mock(spec=Player)
    mock_player.health = 80
    mock_repo.get.return_value = mock_player

    # Act
    status = player_service.get_player_status(player_id)

    # Assert
    mock_repo.get.assert_called_once_with(player_id)
    assert isinstance(status, PlayerStatusDTO)
    assert status.current_health == 80
    assert status.max_health == 100  # Based on current implementation


def test_get_player_status_not_found():
    """Tests that getting status for a non-existent player returns None."""
    mock_repo = Mock(spec=PlayerRepositoryInterface)
    player_service = PlayerService(player_repo=mock_repo, event_dispatcher=Mock())
    player_id = PlayerId(uuid.uuid4())
    mock_repo.get.return_value = None

    assert player_service.get_player_status(player_id) is None

import uuid
from unittest.mock import Mock, patch

from decker_pygame.application.player_service import PlayerService
from decker_pygame.domain.player import Player, PlayerId
from decker_pygame.domain.player_repository_interface import PlayerRepositoryInterface


def test_create_new_player():
    """
    Verify the PlayerService correctly orchestrates player creation.
    """
    # Arrange
    mock_repo = Mock(spec=PlayerRepositoryInterface)
    player_service = PlayerService(player_repo=mock_repo)
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

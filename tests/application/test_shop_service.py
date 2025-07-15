import uuid
from unittest.mock import Mock

import pytest

from decker_pygame.application.dtos import ShopItemDTO, ShopViewDTO
from decker_pygame.application.shop_service import ShopService, ShopServiceError
from decker_pygame.domain.character import Character
from decker_pygame.domain.ids import CharacterId
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface


@pytest.fixture
def mock_char_repo() -> Mock:
    """Provides a mock CharacterRepository."""
    return Mock(spec=CharacterRepositoryInterface)


@pytest.fixture
def shop_service(mock_char_repo: Mock) -> ShopService:
    """Provides a ShopService instance with a mocked character repository."""
    return ShopService(character_repo=mock_char_repo)


def test_get_shop_view_data_success(shop_service: ShopService):
    """Tests successfully retrieving shop data."""
    view_data = shop_service.get_shop_view_data("DefaultShop")

    assert isinstance(view_data, ShopViewDTO)
    assert view_data.shop_name == "The Digital Dive"
    assert len(view_data.items) == 2
    assert isinstance(view_data.items[0], ShopItemDTO)


def test_get_shop_view_data_not_found(shop_service: ShopService):
    """Tests that None is returned for a non-existent shop."""
    assert shop_service.get_shop_view_data("NonExistentShop") is None


def test_purchase_item_success(shop_service: ShopService, mock_char_repo: Mock):
    """Tests the successful purchase of an item."""
    char_id = CharacterId(uuid.uuid4())
    mock_character = Mock(spec=Character)
    mock_character.credits = 1000
    mock_character.stored_programs = []
    mock_char_repo.get.return_value = mock_character

    shop_service.purchase_item(char_id, "IcePick v1", "DefaultShop")

    assert mock_character.credits == 500
    assert len(mock_character.stored_programs) == 1
    assert mock_character.stored_programs[0].name == "IcePick v1"
    mock_char_repo.save.assert_called_once_with(mock_character)


def test_purchase_item_insufficient_credits(
    shop_service: ShopService, mock_char_repo: Mock
):
    """Tests that purchasing fails with insufficient credits."""
    char_id = CharacterId(uuid.uuid4())
    mock_character = Mock(spec=Character)
    mock_character.credits = 100  # Not enough for a 500 credit item
    mock_char_repo.get.return_value = mock_character

    with pytest.raises(ShopServiceError, match="Insufficient credits"):
        shop_service.purchase_item(char_id, "IcePick v1", "DefaultShop")


def test_purchase_item_not_in_shop(shop_service: ShopService, mock_char_repo: Mock):
    """Tests that purchasing fails if the item is not in the shop."""
    char_id = CharacterId(uuid.uuid4())
    mock_character = Mock(spec=Character)
    mock_character.credits = 1000
    mock_char_repo.get.return_value = mock_character

    with pytest.raises(ShopServiceError, match="not found in shop"):
        shop_service.purchase_item(char_id, "NonExistentItem", "DefaultShop")


def test_purchase_item_character_not_found(
    shop_service: ShopService, mock_char_repo: Mock
):
    """Tests that purchasing fails if the character is not found."""
    mock_char_repo.get.return_value = None
    char_id = CharacterId(uuid.uuid4())

    with pytest.raises(ShopServiceError, match="Character not found"):
        shop_service.purchase_item(char_id, "IcePick v1", "DefaultShop")


def test_purchase_item_shop_not_found(shop_service: ShopService, mock_char_repo: Mock):
    """Tests that purchasing fails if the shop is not found."""
    char_id = CharacterId(uuid.uuid4())
    mock_character = Mock(spec=Character)
    mock_character.credits = 1000
    mock_char_repo.get.return_value = mock_character

    with pytest.raises(ShopServiceError, match="Shop not found"):
        shop_service.purchase_item(char_id, "IcePick v1", "NonExistentShop")

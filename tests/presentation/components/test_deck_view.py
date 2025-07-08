from unittest.mock import Mock

from decker_pygame.application.deck_service import DeckViewData
from decker_pygame.presentation.components.deck_view import DeckView


def test_deck_view_initialization():
    """Tests that the DeckView can be initialized."""
    mock_data = DeckViewData(programs=[])
    mock_on_close = Mock()

    view = DeckView(data=mock_data, on_close=mock_on_close)
    assert view is not None

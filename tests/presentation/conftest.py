"""This file contains shared fixtures for the presentation layer tests."""

import uuid
from collections.abc import Generator
from dataclasses import dataclass
from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.ports.service_interfaces import (
    CharacterServiceInterface,
    ContractServiceInterface,
    CraftingServiceInterface,
    DeckServiceInterface,
    DSFileServiceInterface,
    LoggingServiceInterface,
    MatrixRunServiceInterface,
    NodeServiceInterface,
    PlayerServiceInterface,
    ProjectServiceInterface,
    SettingsServiceInterface,
    ShopServiceInterface,
)
from decker_pygame.presentation.asset_service import AssetService
from decker_pygame.presentation.game import Game
from decker_pygame.presentation.input_handler import PygameInputHandler


@dataclass
class Mocks:
    """A container for all mocked objects used in game tests."""

    game: Game
    asset_service: Mock
    player_service: Mock
    character_service: Mock
    contract_service: Mock
    crafting_service: Mock
    deck_service: Mock
    ds_file_service: Mock
    shop_service: Mock
    node_service: Mock
    settings_service: Mock
    project_service: Mock
    matrix_run_service: Mock
    logging_service: Mock
    event_dispatcher: Mock


@pytest.fixture
def game_with_mocks() -> Generator[Mocks]:
    """Provides a fully mocked Game instance and its mocked dependencies."""
    mock_screen = Mock(spec=pygame.Surface)
    mock_asset_service = Mock(spec=AssetService)
    mock_player_service = Mock(spec=PlayerServiceInterface)
    mock_character_service = Mock(spec=CharacterServiceInterface)
    mock_contract_service = Mock(spec=ContractServiceInterface)
    mock_crafting_service = Mock(spec=CraftingServiceInterface)
    mock_deck_service = Mock(spec=DeckServiceInterface)
    mock_ds_file_service = Mock(spec=DSFileServiceInterface)
    mock_shop_service = Mock(spec=ShopServiceInterface)
    mock_node_service = Mock(spec=NodeServiceInterface)
    mock_settings_service = Mock(spec=SettingsServiceInterface)
    mock_project_service = Mock(spec=ProjectServiceInterface)
    mock_matrix_run_service = Mock(spec=MatrixRunServiceInterface)
    mock_logging_service = Mock(spec=LoggingServiceInterface)
    mock_event_dispatcher = Mock(spec=EventDispatcher)
    dummy_player_id = PlayerId(uuid.uuid4())
    dummy_character_id = CharacterId(uuid.uuid4())

    # Configure the asset service mock to return a valid icon
    mock_asset_service.get_spritesheet.return_value = [pygame.Surface((16, 16))]

    # Mock all external dependencies called in Game.__init__ and Game.run
    with (
        patch("pygame.display.flip"),
        patch("pygame.time.Clock"),
        patch(
            "decker_pygame.presentation.game.PygameInputHandler",
            spec=PygameInputHandler,
        ),
    ):
        game = Game(
            screen=mock_screen,
            asset_service=mock_asset_service,
            player_service=mock_player_service,
            player_id=dummy_player_id,
            character_service=mock_character_service,
            contract_service=mock_contract_service,
            crafting_service=mock_crafting_service,
            deck_service=mock_deck_service,
            ds_file_service=mock_ds_file_service,
            shop_service=mock_shop_service,
            node_service=mock_node_service,
            settings_service=mock_settings_service,
            project_service=mock_project_service,
            matrix_run_service=mock_matrix_run_service,
            event_dispatcher=mock_event_dispatcher,
            character_id=dummy_character_id,
            logging_service=mock_logging_service,
        )
        yield Mocks(
            game=game,
            asset_service=mock_asset_service,
            player_service=mock_player_service,
            character_service=mock_character_service,
            contract_service=mock_contract_service,
            crafting_service=mock_crafting_service,
            deck_service=mock_deck_service,
            ds_file_service=mock_ds_file_service,
            shop_service=mock_shop_service,
            node_service=mock_node_service,
            settings_service=mock_settings_service,
            project_service=mock_project_service,
            matrix_run_service=mock_matrix_run_service,
            logging_service=mock_logging_service,
            event_dispatcher=mock_event_dispatcher,
        )

import uuid

from decker_pygame.domain.events import PlayerCreated
from decker_pygame.domain.model import Player, PlayerId


def test_player_equality():
    """Players should be equal if they have the same ID."""
    player_id = PlayerId(uuid.uuid4())
    player1 = Player(id=player_id, name="p1", health=100)
    player2 = Player(id=player_id, name="p2", health=50)
    player3 = Player(id=PlayerId(uuid.uuid4()), name="p1", health=100)

    assert player1 == player2
    assert player1 != player3
    assert player1 != "not a player"


def test_player_hash():
    """Players with the same ID should have the same hash."""
    player_id = PlayerId(uuid.uuid4())
    player1 = Player(id=player_id, name="p1", health=100)
    player2 = Player(id=player_id, name="p2", health=50)

    assert hash(player1) == hash(player2)
    assert len({player1, player2}) == 1


def test_player_factory_and_events():
    """Covers the Player.create factory and event handling."""
    player_id = PlayerId(uuid.uuid4())
    player = Player.create(player_id=player_id, name="Deckard", initial_health=100)

    assert len(player.events) == 1
    assert isinstance(player.events[0], PlayerCreated)

    player.clear_events()
    assert not player.events


def test_player_can_be_used_in_a_set():
    """Covers the __hash__ method by using the object as a set key."""
    player = Player(id=PlayerId(uuid.uuid4()), name="p1", health=100)
    player_set = {player}
    assert player in player_set

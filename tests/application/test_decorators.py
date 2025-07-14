from decker_pygame.application.decorators import emits, handles
from decker_pygame.domain.events import CharacterCreated, Event, PlayerCreated


def test_emits_decorator_attaches_metadata():
    """Tests that the @emits decorator marks a function correctly."""

    @emits(PlayerCreated, CharacterCreated)
    def my_emitter(arg1: int, arg2: int) -> int:
        return arg1 + arg2

    # The decorator should not change the function's behavior
    assert my_emitter(1, 2) == 3
    # It should attach the metadata
    assert hasattr(my_emitter, "_emits")
    assert my_emitter._emits == (PlayerCreated, CharacterCreated)


def test_handles_decorator_attaches_metadata():
    """Tests that the @handles decorator attaches metadata correctly."""

    # Test with a single event
    @handles(PlayerCreated)
    def single_handler(event: PlayerCreated) -> None:
        pass

    assert hasattr(single_handler, "_handles")
    assert single_handler._handles == [PlayerCreated]

    # Test with multiple events
    @handles(PlayerCreated, CharacterCreated)
    def multi_handler(event: Event) -> None:
        pass

    assert hasattr(multi_handler, "_handles")
    assert multi_handler._handles == [PlayerCreated, CharacterCreated]

    # Test that stacking still works as expected
    @handles(CharacterCreated)
    @handles(PlayerCreated)
    def stacked_handler(event: Event) -> None:
        pass

    assert hasattr(stacked_handler, "_handles")
    assert stacked_handler._handles == [PlayerCreated, CharacterCreated]

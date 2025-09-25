from unittest.mock import Mock

import pygame

from decker_pygame.presentation.components.button import Button


def make_click_event(pos):
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1})


def make_release_event(pos):
    return pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": pos, "button": 1})


def test_button_click_triggers_on_click():
    clicked = Mock()
    btn = Button(position=(0, 0), size=(50, 20), text="OK", on_click=clicked)

    # Press inside the rect
    down = make_click_event((10, 5))
    btn.handle_event(down)

    # Release inside the rect should call the handler
    up = make_release_event((10, 5))
    btn.handle_event(up)

    clicked.assert_called_once()


def test_button_click_exception_is_propagated_and_logged(monkeypatch):
    def raiser():
        raise RuntimeError("boom")

    btn = Button(position=(0, 0), size=(50, 20), text="Fail", on_click=raiser)

    # Patch plog so we can assert it's called for the exception
    plog_calls = []

    def fake_plog(msg, **kwargs):
        plog_calls.append((msg, kwargs))

    monkeypatch.setattr("decker_pygame.presentation.components.button.plog", fake_plog)

    btn.handle_event(make_click_event((5, 5)))
    try:
        btn.handle_event(make_release_event((5, 5)))
    except RuntimeError:
        # Expected
        pass

    # Ensure the exception log was emitted
    assert any("Exception in button on_click" in m for m, _ in plog_calls)

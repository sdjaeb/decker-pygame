import json
from io import StringIO

from decker_pygame.presentation import logging as plog


def capture_print(func, *args, **kwargs):
    """Capture print output from function call and return as a string."""
    import sys

    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        func(*args, **kwargs)
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdout = old_stdout


def test_log_without_data_emits_json_with_expected_keys():
    out = capture_print(plog.log, "hello world")
    assert out
    obj = json.loads(out)
    # required keys
    assert "timestamp" in obj
    assert obj["level"] == "INFO"
    assert obj["category"] == "app"
    assert obj["message"] == "hello world"
    assert "data" not in obj


def test_log_with_data_includes_data_field():
    payload = {"a": 1}
    out = capture_print(plog.log, "with data", data=payload)
    obj = json.loads(out)
    assert obj["message"] == "with data"
    assert "data" in obj
    assert obj["data"] == payload

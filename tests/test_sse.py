"""Tests for SSEParser."""

import pytest
from agent_stream import SSEParser


# ---------------------------------------------------------------------------
# parse_line
# ---------------------------------------------------------------------------

def test_parse_data_json():
    parser = SSEParser()
    result = parser.parse_line('data: {"choices": [{"delta": {"content": "Hi"}}]}')
    assert result == {"data": {"choices": [{"delta": {"content": "Hi"}}]}}


def test_parse_data_raw_string():
    parser = SSEParser()
    result = parser.parse_line("data: hello world")
    assert result == {"data": "hello world"}


def test_parse_done_sentinel():
    parser = SSEParser()
    result = parser.parse_line("data: [DONE]")
    assert result == {"done": True}


def test_parse_event_field():
    parser = SSEParser()
    result = parser.parse_line("event: message")
    assert result == {"event": "message"}


def test_parse_id_field():
    parser = SSEParser()
    result = parser.parse_line("id: 42")
    assert result == {"id": "42"}


def test_parse_retry_field():
    parser = SSEParser()
    result = parser.parse_line("retry: 3000")
    assert result == {"retry": 3000}


def test_parse_blank_line_returns_none():
    parser = SSEParser()
    assert parser.parse_line("") is None
    assert parser.parse_line("\n") is None


def test_parse_comment_returns_none():
    parser = SSEParser()
    assert parser.parse_line(": this is a comment") is None


# ---------------------------------------------------------------------------
# parse_stream
# ---------------------------------------------------------------------------

def test_parse_stream_basic():
    parser = SSEParser()
    lines = [
        "event: message",
        "data: hello",
        "",
        "data: world",
        "",
    ]
    events = list(parser.parse_stream(lines))
    assert len(events) == 2
    assert events[0] == {"event": "message", "data": "hello"}
    assert events[1] == {"data": "world"}


def test_parse_stream_done_stops_iteration():
    parser = SSEParser()
    lines = [
        "data: first",
        "",
        "data: [DONE]",
        "data: should-not-appear",
    ]
    events = list(parser.parse_stream(lines))
    # Should yield the first data event, then {done: True}
    assert any(e.get("data") == "first" for e in events)
    assert any(e.get("done") for e in events)
    # Nothing after [DONE]
    assert not any(e.get("data") == "should-not-appear" for e in events)


def test_parse_stream_trailing_event_without_blank():
    """Event at end of stream without trailing blank line is still yielded."""
    parser = SSEParser()
    lines = ["data: trailing"]
    events = list(parser.parse_stream(lines))
    assert events == [{"data": "trailing"}]


def test_parse_stream_empty():
    parser = SSEParser()
    assert list(parser.parse_stream([])) == []

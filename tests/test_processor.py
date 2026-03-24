"""Tests for StreamProcessor."""

import pytest
from agent_stream import StreamProcessor


def test_collect_passthrough():
    result = StreamProcessor(["a", "b", "c"]).collect()
    assert result == ["a", "b", "c"]


def test_filter():
    result = StreamProcessor(["", "hello", "", "world"]).filter(bool).collect()
    assert result == ["hello", "world"]


def test_map():
    result = StreamProcessor(["hello", "world"]).map(str.upper).collect()
    assert result == ["HELLO", "WORLD"]


def test_take():
    result = StreamProcessor(range(100)).take(3).collect()
    assert result == [0, 1, 2]


def test_filter_map_chaining():
    result = (
        StreamProcessor(["a", "", "b", "  ", "c"])
        .filter(str.strip)
        .map(str.upper)
        .collect()
    )
    assert result == ["A", "B", "C"]


def test_to_string():
    result = StreamProcessor(["Hello", ", ", "world"]).to_string()
    assert result == "Hello, world"


def test_to_string_with_sep():
    result = StreamProcessor(["a", "b", "c"]).to_string(sep="-")
    assert result == "a-b-c"


def test_take_then_map():
    result = StreamProcessor(range(10)).take(3).map(lambda x: x * 2).collect()
    assert result == [0, 2, 4]


def test_empty_stream():
    assert StreamProcessor([]).collect() == []
    assert StreamProcessor([]).to_string() == ""


def test_take_more_than_available():
    result = StreamProcessor([1, 2]).take(100).collect()
    assert result == [1, 2]


def test_filter_all_out():
    result = StreamProcessor(["a", "b"]).filter(lambda x: False).collect()
    assert result == []


def test_fluent_returns_same_instance():
    sp = StreamProcessor(["x"])
    assert sp.filter(bool) is sp
    assert sp.map(str.upper) is sp
    assert sp.take(1) is sp

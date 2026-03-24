"""Tests for StreamCollector."""

import pytest
from agent_stream import StreamCollector


# ---------------------------------------------------------------------------
# Basic accumulation
# ---------------------------------------------------------------------------

def test_feed_str_chunks():
    sc = StreamCollector()
    sc.feed("Hello")
    sc.feed(", ")
    sc.feed("world")
    assert sc.collected == "Hello, world"


def test_feed_bytes_decoded():
    sc = StreamCollector()
    sc.feed(b"Hello")
    sc.feed(b" bytes")
    assert sc.collected == "Hello bytes"


def test_chunk_count():
    sc = StreamCollector()
    sc.feed("a")
    sc.feed("b")
    sc.feed("c")
    assert sc.chunk_count == 3


def test_collect_from_iterable():
    sc = StreamCollector()
    result = sc.collect(["one", " ", "two"])
    assert result == "one two"
    assert sc.is_complete is True


def test_is_complete_false_before_collect():
    sc = StreamCollector()
    sc.feed("partial")
    assert sc.is_complete is False


def test_reset_clears_state():
    sc = StreamCollector()
    sc.feed("data")
    sc.reset()
    assert sc.collected == ""
    assert sc.chunk_count == 0
    assert sc.is_complete is False


def test_on_chunk_callback_called():
    seen = []
    sc = StreamCollector(on_chunk=seen.append)
    sc.feed("x")
    sc.feed("y")
    assert seen == ["x", "y"]


def test_on_complete_callback_called():
    completed = []
    sc = StreamCollector(on_complete=completed.append)
    sc.collect(["a", "b"])
    assert completed == ["ab"]


def test_collect_empty_stream():
    sc = StreamCollector()
    result = sc.collect([])
    assert result == ""
    assert sc.is_complete is True


def test_collect_bytes_stream():
    sc = StreamCollector()
    result = sc.collect([b"hi", b" there"])
    assert result == "hi there"

"""Tests for ChunkBuffer."""

import pytest
from agent_stream import ChunkBuffer


def test_write_and_read_all():
    buf = ChunkBuffer()
    buf.write("hello")
    buf.write(" world")
    assert buf.read() == "hello world"


def test_available_tracks_chars():
    buf = ChunkBuffer()
    buf.write("abc")
    assert buf.available == 3
    buf.read(1)
    assert buf.available == 2


def test_read_n_chars():
    buf = ChunkBuffer()
    buf.write("abcdef")
    assert buf.read(3) == "abc"
    assert buf.read(3) == "def"
    assert buf.available == 0


def test_peek_does_not_consume():
    buf = ChunkBuffer()
    buf.write("hello")
    assert buf.peek(3) == "hel"
    assert buf.available == 5  # unchanged


def test_is_full():
    buf = ChunkBuffer(max_size=5)
    buf.write("hello")
    assert buf.is_full is True


def test_overflow_raises_buffer_error():
    buf = ChunkBuffer(max_size=5)
    buf.write("hello")
    with pytest.raises(BufferError):
        buf.write("x")


def test_read_after_empty_returns_empty():
    buf = ChunkBuffer()
    assert buf.read() == ""
    assert buf.read(5) == ""


def test_invalid_max_size():
    with pytest.raises(ValueError):
        ChunkBuffer(max_size=0)


def test_write_non_string_raises():
    buf = ChunkBuffer()
    with pytest.raises(TypeError):
        buf.write(123)  # type: ignore


def test_read_more_than_available():
    buf = ChunkBuffer()
    buf.write("hi")
    assert buf.read(100) == "hi"


def test_peek_zero():
    buf = ChunkBuffer()
    buf.write("data")
    assert buf.peek(0) == ""

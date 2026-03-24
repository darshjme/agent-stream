"""StreamProcessor — fluent lazy pipeline for streaming chunks."""

from __future__ import annotations
from typing import Callable, Generator, Iterable, Iterator, TypeVar

T = TypeVar("T")


class StreamProcessor:
    """Lazy, fluent stream processing pipeline.

    Transformations (``filter``, ``map``, ``take``) are applied lazily;
    data only flows when ``collect()`` or ``to_string()`` is called.

    Example::

        result = (
            StreamProcessor(chunks)
            .filter(lambda c: c.strip())
            .map(str.upper)
            .take(5)
            .to_string()
        )
    """

    def __init__(self, stream: Iterable) -> None:
        self._stream: Iterable = stream
        # Lazy ops: list of callables that wrap the previous iterator
        self._ops: list[Callable[[Iterator], Iterator]] = []

    # ------------------------------------------------------------------
    # Fluent transformations (all return *self* for chaining)
    # ------------------------------------------------------------------

    def filter(self, predicate: Callable[[object], bool]) -> "StreamProcessor":
        """Keep only chunks for which *predicate* returns truthy."""
        def _filter(it: Iterator) -> Generator:
            for item in it:
                if predicate(item):
                    yield item
        self._ops.append(_filter)
        return self

    def map(self, transform: Callable[[object], object]) -> "StreamProcessor":
        """Apply *transform* to every chunk."""
        def _map(it: Iterator) -> Generator:
            for item in it:
                yield transform(item)
        self._ops.append(_map)
        return self

    def take(self, n: int) -> "StreamProcessor":
        """Keep only the first *n* chunks."""
        def _take(it: Iterator) -> Generator:
            count = 0
            for item in it:
                if count >= n:
                    break
                yield item
                count += 1
        self._ops.append(_take)
        return self

    # ------------------------------------------------------------------
    # Terminal operations
    # ------------------------------------------------------------------

    def collect(self) -> list:
        """Materialize the pipeline into a list."""
        return list(self._build_iterator())

    def to_string(self, sep: str = "") -> str:
        """Join all chunks with *sep* (default: no separator)."""
        return sep.join(str(item) for item in self._build_iterator())

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _build_iterator(self) -> Iterator:
        it: Iterator = iter(self._stream)
        for op in self._ops:
            it = op(it)
        return it

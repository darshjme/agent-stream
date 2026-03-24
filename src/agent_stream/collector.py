"""StreamCollector — accumulates chunks from any iterable stream."""

from __future__ import annotations
from typing import Callable, Iterable, Optional


class StreamCollector:
    """Accumulates text chunks from a streaming source.

    Supports optional callbacks on each chunk and on completion.
    Works with any iterable that yields str or bytes.
    """

    def __init__(
        self,
        on_chunk: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None,
    ) -> None:
        self._on_chunk = on_chunk
        self._on_complete = on_complete
        self._buffer: list[str] = []
        self._chunk_count: int = 0
        self._is_complete: bool = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def feed(self, chunk: str | bytes) -> None:
        """Process one chunk, appending it to the internal buffer.

        Decodes bytes to str (UTF-8) automatically. Calls *on_chunk*
        callback if provided.
        """
        if isinstance(chunk, (bytes, bytearray)):
            chunk = chunk.decode("utf-8", errors="replace")
        self._buffer.append(chunk)
        self._chunk_count += 1
        if self._on_chunk is not None:
            self._on_chunk(chunk)

    def collect(self, stream: Iterable[str | bytes]) -> str:
        """Drain *stream*, accumulate all chunks, return full text.

        Marks the collector as complete and calls *on_complete* callback.
        """
        for chunk in stream:
            self.feed(chunk)
        self._is_complete = True
        result = self.collected
        if self._on_complete is not None:
            self._on_complete(result)
        return result

    def reset(self) -> None:
        """Clear accumulated state so the collector can be reused."""
        self._buffer.clear()
        self._chunk_count = 0
        self._is_complete = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def collected(self) -> str:
        """Return current accumulated text (all chunks joined)."""
        return "".join(self._buffer)

    @property
    def chunk_count(self) -> int:
        """Number of chunks fed so far."""
        return self._chunk_count

    @property
    def is_complete(self) -> bool:
        """True after *collect()* finishes draining the stream."""
        return self._is_complete

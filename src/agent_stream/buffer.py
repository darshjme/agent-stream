"""ChunkBuffer — fixed-capacity circular character buffer for streaming."""

from __future__ import annotations
from collections import deque


class ChunkBuffer:
    """A fixed-capacity text buffer for streaming chunks.

    New writes that exceed *max_size* raise ``BufferError``.
    Data is consumed in FIFO order; ``peek`` inspects without consuming.
    """

    def __init__(self, max_size: int = 10_000) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be a positive integer")
        self._max_size = max_size
        self._data: deque[str] = deque()
        self._total: int = 0  # chars currently in buffer

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def write(self, chunk: str) -> None:
        """Append *chunk* to the buffer.

        Raises ``BufferError`` if adding *chunk* would exceed *max_size*.
        """
        if not isinstance(chunk, str):
            raise TypeError(f"chunk must be str, got {type(chunk).__name__}")
        if len(chunk) == 0:
            return
        if self._total + len(chunk) > self._max_size:
            raise BufferError(
                f"ChunkBuffer overflow: buffer holds {self._total} chars, "
                f"writing {len(chunk)} chars would exceed max_size={self._max_size}"
            )
        self._data.append(chunk)
        self._total += len(chunk)

    # ------------------------------------------------------------------
    # Read / Peek
    # ------------------------------------------------------------------

    def read(self, n: int = -1) -> str:
        """Consume and return up to *n* characters (or all if n == -1)."""
        if n == -1 or n >= self._total:
            # Consume everything
            result = "".join(self._data)
            self._data.clear()
            self._total = 0
            return result

        # Consume exactly n characters
        result_parts: list[str] = []
        remaining = n
        while remaining > 0 and self._data:
            head = self._data[0]
            if len(head) <= remaining:
                result_parts.append(head)
                remaining -= len(head)
                self._total -= len(head)
                self._data.popleft()
            else:
                result_parts.append(head[:remaining])
                self._data[0] = head[remaining:]
                self._total -= remaining
                remaining = 0
        return "".join(result_parts)

    def peek(self, n: int) -> str:
        """Return up to *n* characters without consuming them."""
        if n <= 0:
            return ""
        result_parts: list[str] = []
        consumed = 0
        for chunk in self._data:
            if consumed >= n:
                break
            take = min(len(chunk), n - consumed)
            result_parts.append(chunk[:take])
            consumed += take
        return "".join(result_parts)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def available(self) -> int:
        """Number of characters currently in the buffer."""
        return self._total

    @property
    def is_full(self) -> bool:
        """True when the buffer has reached its *max_size* capacity."""
        return self._total >= self._max_size

    @property
    def max_size(self) -> int:
        """Maximum capacity in characters."""
        return self._max_size

"""SSEParser — Server-Sent Events parser (RFC 8895 + OpenAI extensions)."""

from __future__ import annotations
import json
from typing import Generator, Iterable, Optional


class SSEParser:
    """Parse Server-Sent Events line-by-line or from an iterable of lines.

    Supports standard SSE fields (data, event, id, retry) and the
    OpenAI-style ``[DONE]`` terminator.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse_line(self, line: str) -> Optional[dict]:
        """Parse a single SSE line and return a structured dict or None.

        Returns a dict with at least one of these keys:
        - ``{"data": <parsed_json_or_raw_str>}``
        - ``{"event": <event_type>}``
        - ``{"id": <last_event_id>}``
        - ``{"retry": <milliseconds_int>}``
        - ``{"done": True}``  — for "[DONE]" terminator

        Returns ``None`` for blank lines or comment lines (``:``) that
        carry no semantic meaning.
        """
        line = line.rstrip("\r\n")

        # Blank line — event boundary, no data
        if not line:
            return None

        # Comment
        if line.startswith(":"):
            return None

        # Field: value  (colon may have a space after it)
        if ":" in line:
            field, _, raw_value = line.partition(":")
            # Strip exactly one leading space per spec
            if raw_value.startswith(" "):
                raw_value = raw_value[1:]
        else:
            # Line is a field name with no value — treat as empty string
            field = line
            raw_value = ""

        field = field.strip()

        if field == "data":
            # OpenAI [DONE] terminator
            if raw_value.strip() == "[DONE]":
                return {"done": True}
            # Try to JSON-decode; fall back to raw string
            try:
                return {"data": json.loads(raw_value)}
            except json.JSONDecodeError:
                return {"data": raw_value}

        elif field == "event":
            return {"event": raw_value}

        elif field == "id":
            return {"id": raw_value}

        elif field == "retry":
            try:
                return {"retry": int(raw_value)}
            except ValueError:
                return {"retry": raw_value}

        # Unknown field — return as-is
        return {field: raw_value}

    def parse_stream(self, lines: Iterable[str]) -> Generator[dict, None, None]:
        """Yield parsed SSE events from an iterable of lines.

        Blank lines delimit events; this generator accumulates fields
        within an event block and yields the merged dict when the block
        ends (blank line). A final incomplete block is also yielded.

        The ``[DONE]`` sentinel causes the generator to stop iteration.
        """
        current_event: dict = {}

        for line in lines:
            parsed = self.parse_line(line)

            # Blank line → flush current event if non-empty
            if parsed is None:
                if current_event:
                    yield current_event
                    current_event = {}
                continue

            # [DONE] sentinel
            if parsed.get("done"):
                if current_event:
                    yield current_event
                yield {"done": True}
                return

            # Merge field into current event
            current_event.update(parsed)

        # Yield any trailing (non-blank-terminated) event
        if current_event:
            yield current_event

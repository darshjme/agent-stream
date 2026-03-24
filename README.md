<div align="center">
<img src="assets/hero.svg" width="100%"/>
</div>

# agent-stream

**Streaming response handling for LLM agents — chunk accumulation, SSE parsing, partial callbacks, stream interruption.**

[![PyPI version](https://img.shields.io/pypi/v/agent-stream?color=blue&style=flat-square)](https://pypi.org/project/agent-stream/) [![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://python.org) [![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE) [![Tests](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)](#)

---

## The Problem

Without streaming, the user waits for the entire response before seeing anything — perceived latency is total latency. Streaming reduces time-to-first-token and enables real-time pipelines that buffer-and-batch cannot match.

## Installation

```bash
pip install agent-stream
```

## Quick Start

```python
from agent_stream import ChunkBuffer, StreamCollector, StreamProcessor

# Initialise
instance = ChunkBuffer(name="my_agent")

# Use
# see API reference below
print(result)
```

## API Reference

### `ChunkBuffer`

```python
class ChunkBuffer:
    """A fixed-capacity text buffer for streaming chunks.
    def __init__(self, max_size: int = 10_000) -> None:
    def write(self, chunk: str) -> None:
        """Append *chunk* to the buffer.
    def read(self, n: int = -1) -> str:
        """Consume and return up to *n* characters (or all if n == -1)."""
```

### `StreamCollector`

```python
class StreamCollector:
    """Accumulates text chunks from a streaming source.
    def __init__(
    def feed(self, chunk: str | bytes) -> None:
        """Process one chunk, appending it to the internal buffer.
    def collect(self, stream: Iterable[str | bytes]) -> str:
        """Drain *stream*, accumulate all chunks, return full text.
    def reset(self) -> None:
        """Clear accumulated state so the collector can be reused."""
```

### `StreamProcessor`

```python
class StreamProcessor:
    """Lazy, fluent stream processing pipeline.
    def __init__(self, stream: Iterable) -> None:
    def filter(self, predicate: Callable[[object], bool]) -> "StreamProcessor":
        """Keep only chunks for which *predicate* returns truthy."""
    def map(self, transform: Callable[[object], object]) -> "StreamProcessor":
        """Apply *transform* to every chunk."""
    def take(self, n: int) -> "StreamProcessor":
        """Keep only the first *n* chunks."""
```


## How It Works

### Flow

```mermaid
flowchart LR
    A[User Code] -->|create| B[ChunkBuffer]
    B -->|configure| C[StreamCollector]
    C -->|execute| D{Success?}
    D -->|yes| E[Return Result]
    D -->|no| F[Error Handler]
    F --> G[Fallback / Retry]
    G --> C
```

### Sequence

```mermaid
sequenceDiagram
    participant App
    participant ChunkBuffer
    participant StreamCollector

    App->>+ChunkBuffer: initialise()
    ChunkBuffer->>+StreamCollector: configure()
    StreamCollector-->>-ChunkBuffer: ready
    App->>+ChunkBuffer: run(context)
    ChunkBuffer->>+StreamCollector: execute(context)
    StreamCollector-->>-ChunkBuffer: result
    ChunkBuffer-->>-App: WorkflowResult
```

## Philosophy

> *Sarasvatī* — the river goddess — flows without accumulation; a true stream processes and releases.

---

*Part of the [arsenal](https://github.com/darshjme/arsenal) — production stack for LLM agents.*

*Built by [Darshankumar Joshi](https://github.com/darshjme), Gujarat, India.*

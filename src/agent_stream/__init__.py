"""agent-stream: Streaming response handling for LLM agents."""

from .collector import StreamCollector
from .sse import SSEParser
from .buffer import ChunkBuffer
from .processor import StreamProcessor

__version__ = "0.1.0"
__all__ = ["StreamCollector", "SSEParser", "ChunkBuffer", "StreamProcessor"]

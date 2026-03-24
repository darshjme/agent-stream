# Changelog

All notable changes to **agent-stream** will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.1.0] — 2026-03-24

### Added
- `StreamCollector` — accumulates str/bytes chunks from any iterable; on_chunk / on_complete callbacks.
- `SSEParser` — RFC 8895 Server-Sent Events parser; supports data, event, id, retry fields and the OpenAI `[DONE]` terminator.
- `ChunkBuffer` — fixed-capacity FIFO character buffer with overflow protection, peek, and partial reads.
- `StreamProcessor` — lazy fluent pipeline (filter / map / take / collect / to_string).
- Zero runtime dependencies; Python ≥ 3.10.
- 25 pytest tests (100 % pass).

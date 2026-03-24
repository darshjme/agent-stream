# Contributing to agent-stream

Thank you for your interest in contributing!

## Getting Started

```bash
git clone https://github.com/your-org/agent-stream
cd agent-stream
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest tests/ -v
```

## Guidelines

- **Style**: PEP 8, type annotations on all public APIs.
- **Tests**: every new feature or bug-fix must include at least one pytest test.
- **Docs**: update `README.md` and `CHANGELOG.md` under `[Unreleased]`.
- **No deps**: keep runtime dependencies at zero; dev deps are fine.

## Pull Requests

1. Fork the repo and create a feature branch: `git checkout -b feat/my-feature`.
2. Write your code + tests.
3. Run `python -m pytest tests/ -v` — all tests must pass.
4. Open a PR with a clear description of *what* and *why*.

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). Be kind.

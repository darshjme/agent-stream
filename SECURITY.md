# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅         |

## Reporting a Vulnerability

If you discover a security vulnerability in **agent-stream**, please **do not** open a public GitHub issue.

Instead, email the maintainers directly (see `pyproject.toml`) with:

1. A description of the vulnerability.
2. Steps to reproduce.
3. Potential impact.
4. (Optional) suggested fix.

We aim to acknowledge reports within **48 hours** and to publish a patch within **7 days** for critical issues.

## Scope

- Malformed SSE data causing parser crashes or hangs.
- `ChunkBuffer` overflow bypasses.
- Any RCE or data-exfiltration vector introduced via streaming callbacks.

## Out of Scope

- Vulnerabilities in LLM providers whose responses you stream (out of our control).
- Issues arising from running untrusted `transform` callables inside `StreamProcessor` (caller's responsibility).

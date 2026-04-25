# deadband-protocol

[![PyPI](https://img.shields.io/pypi/v/deadband-protocol)](https://pypi.org/project/deadband-protocol/) [![Python](https://img.shields.io/pypi/pyversions/deadband-protocol)](https://pypi.org/project/deadband-protocol/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Navigate by knowing where the rocks are NOT.

A three-tier safety protocol for AI agent systems. Instead of cataloging every possible danger, the deadband protocol defines safe operating channels and blocks everything outside them.

## The Three Tiers

### P0 — Block
Hard blocks on dangerous patterns (destructive commands, SQL injection, code execution). Pattern-based, zero-tolerance, fast.

### P1 — Route
Classify safe inputs into appropriate channels (math, code, general, medical). Confidence-weighted routing to specialized handlers.

### P2 — Optimize
Within safe channels, optimize the response for quality and relevance. Channel-aware refinement.

## Installation

```bash
pip install deadband-protocol
```

## Usage

```python
from deadband_protocol import Deadband, ChannelRouter

# Create router and deadband
router = ChannelRouter()
db = Deadband()

# P0: Block dangerous inputs
result = db.check("rm -rf /")
assert not result.passed  # Blocked at P0

# P1: Route safe inputs to channels
result = db.check("Explain the math behind neural networks", router)
assert result.passed
print(result.safe_channel)  # "math"
print(result.channel_confidence)  # 0.85

# Add custom dangerous patterns
db.add_pattern(r"SECRET_KEY\s*=")
db.add_blocklist("password")

# Filter mode — redact instead of block
filtered = db.filter("Run rm -rf / to clean up")
# "Run [BLOCKED] to clean up"
```

## Architecture

```
Input → P0 (block) → P1 (route) → P2 (optimize) → Response
              ↓              ↓
         violations    safe_channel
```

The deadband concept comes from control theory: a region where no corrective action is needed. Instead of reacting to every possible input, define the safe region and only handle what falls outside it.

## Part of the Cocapn Fleet

Used by Oracle1, Forgemaster, JetsonClaw1, and CoCapn-claw for input safety validation across all fleet HTTP endpoints.

## License

MIT
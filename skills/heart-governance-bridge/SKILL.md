---
name: heart-governance-bridge
description: Refresh or interpret the cached Heart governance signal layer from World Bank, OECD, and data.govt.nz, then use it to extend the NZ-plus-global governance bridge around Freed ID and the Cosmic Bill. Use when Codex needs to run `scripts/heart_governance_signal_refresh.py`, `scripts/heart_governance_signal_board.py`, or update governance comparison docs without overstating legal force.
---

# Heart Governance Bridge

Use this skill when Heart needs current NZ-plus-global governance context.

## Workflow

1. Refresh the Heart cache only on explicit request:

```bash
python3 scripts/heart_governance_signal_refresh.py
```

2. Validate the cached board:

```bash
python3 scripts/heart_governance_signal_board.py --fail-on-warn
```

3. Promote only selected public governance signals into the curated registry and comparison docs.
4. Treat all legal and governance material as context and alignment evidence unless there is actual adoption or interoperability proof.

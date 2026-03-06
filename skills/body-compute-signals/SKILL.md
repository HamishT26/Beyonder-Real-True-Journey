---
name: body-compute-signals
description: Refresh or interpret the cached Body compute signal layer from Crossref and GitHub watchlists, then use it to annotate Trinity OS maturity and risk posture. Use when Codex needs to run `scripts/body_compute_signal_refresh.py`, `scripts/body_compute_signal_board.py`, or update Body comparisons without turning them into vendor-parity claims.
---

# Body Compute Signals

Use this skill when Body needs public ecosystem context while staying standards-first.

## Workflow

1. Refresh the Body cache only on demand:

```bash
python3 scripts/body_compute_signal_refresh.py
```

2. Validate the cached board:

```bash
python3 scripts/body_compute_signal_board.py --fail-on-warn
```

3. Use the fixed GitHub watchlist and Crossref metadata as advisory architecture context.
4. Keep Body policy decisions tied to benchmark, trend, and stress evidence rather than public repo excitement.

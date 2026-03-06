---
name: mind-theory-signals
description: Refresh or interpret the cached Mind theory signal layer from arXiv and OpenAlex, then promote only standards-first findings into GMUT comparison docs. Use when Codex needs to run `scripts/mind_theory_signal_refresh.py`, `scripts/mind_theory_signal_board.py`, or update Mind comparison language without relaxing evidence boundaries.
---

# Mind Theory Signals

Use this skill when Mind needs current public theory context without treating it as proof.

## Workflow

1. Refresh the cache only when live public intake is explicitly wanted:

```bash
python3 scripts/mind_theory_signal_refresh.py
```

2. Validate the cached board:

```bash
python3 scripts/mind_theory_signal_board.py --fail-on-warn
```

3. Promote only selected signals into the curated public-source registry and Mind docs.
4. Keep all theory intake tagged as comparator or falsification context unless a separate measured anchor supports more.

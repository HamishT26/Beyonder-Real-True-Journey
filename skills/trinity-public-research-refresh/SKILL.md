---
name: trinity-public-research-refresh
description: Refresh the cached public-source Trinity research layer and its downstream comparison artifacts. Use when Codex needs to update `docs/trinity-public-source-registry-v1.json`, rerun the offline public research validator or signal board, or revise standards-first Mind, Body, and Heart comparison docs from public and local sources only.
---

# Trinity Public Research Refresh

Refresh the Trinity public-source corpus without introducing live-network dependencies into the runtime suite.

Keep the evidence boundary explicit: public sources can refine comparison language, context, and next falsification steps, but they do not override deterministic repo validation artifacts.

## Workflow

1. Update `docs/trinity-public-source-registry-v1.json` from public and local sources only.
2. Prefer `official_primary`, `official_secondary`, and `research_primary` sources.
3. Keep `public_reporting` out of comparison-driving updates unless it is clearly marked as supplemental.
4. Run the cached validator:

```bash
python3 scripts/validate_trinity_public_research.py --fail-on-warn
```

5. Run the cached public signal board:

```bash
python3 scripts/trinity_public_signal_board.py --fail-on-warn
```

6. Update dependent docs only after the validator and board are green:
   - `docs/trinity-public-research-brief-2026-03-06.md`
   - `docs/comparative-validation-grid-v1.md`
   - `docs/grand-unified-narrative-brief.md`
7. Preserve `verified`, `inference`, and `open gap` boundaries in every narrative update.

## Source rules

- Use public web sources and repo-local state only.
- Do not assume authenticated APIs, MCP resources, or browser sessions.
- Prefer official standards, legislation, institutional updates, and primary research.
- Treat scripture, broader metaphysical comparators, and non-standard paradigms as optional follow-on research lanes unless the user explicitly asks to fold them into the active comparison pack.

## Output rules

- Keep the research layer cached and offline-checkable.
- Do not add live web fetches to `scripts/run_all_trinity_systems.py`.
- Use new sources to refine comparator posture and next checks, not to claim runtime readiness.

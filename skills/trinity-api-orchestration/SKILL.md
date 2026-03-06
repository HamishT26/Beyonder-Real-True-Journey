---
name: trinity-api-orchestration
description: Orchestrate the deterministic public API layer across manifest validation, per-pillar boards, and the constellation board. Use when Codex needs to work with `docs/trinity-api-source-manifest-v1.json`, `docs/trinity-api-query-pack-v1.json`, the three cached pillar signals, or `scripts/trinity_api_constellation_board.py`.
---

# Trinity API Orchestration

Use this skill when working on the public API signal layer as a whole.

## Workflow

1. Keep `docs/trinity-api-source-manifest-v1.json` and `docs/trinity-api-query-pack-v1.json` as the source of truth.
2. Validate the manifest before trusting cached outputs:

```bash
python3 scripts/trinity_api_source_manifest_validator.py --fail-on-warn
```

3. Run the three pillar boards, then the constellation board.
4. Keep live refresh optional and cached validation default.

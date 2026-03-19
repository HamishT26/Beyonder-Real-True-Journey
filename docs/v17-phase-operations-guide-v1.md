# V17 Phase Operations Guide

## Authority Model

- repo authority: `repo_first`
- shared latest promotes only from full-suite closeout
- quick/evidence lane writes only to v17-specific latest surfaces
- Google Drive remains `operator_hold`
- materialization remains `readiness_only`

## Checkpoints

1. Shared baseline anchor: `e45da1dd2dd184c4e3fd218ece27b8f29589f8f6`
2. V17 bootstrap anchor: `468b96d90bc2785be19854b44c62217a47afc800`
3. Quick runs preserve v17 evidence-first truth without displacing shared latest.
4. Standard, deep, collab, offline-only, and materialize L2-L5 are the promotion gate for shared latest.

## Runtime Truth

- Overlay slots `27-31` are fixed.
- Required fields: `requested_model`, `offered_model`, `selected_model`, `resolved_model`, `runtime_surface`.
- `unknown` is allowed only while truth is incomplete.
- `external_live_overlay_state` must remain `awaiting_thread_boot` or `packaged_handoff` until the full runtime field set is auditable.

## Identity Rules

- official council count remains `11`
- no new official members
- no new certificates
- no new Freed IDs
- `.codex/agents/*.toml` overlays are durable overlays, not new roster entries

## Claims

- `confirmed_evidence`: repo-backed or official-source-backed
- `inference`: reasoned synthesis, not direct proof
- `open_gap`: unresolved or unproven
- never upgrade comparative promise into external establishment without evidence

## Handoff

- read `docs/v17-baseline-state-v1.json`
- read `docs/v17-runtime-truth-resolution-board-v1.json`
- read `docs/v17-closeout-summary-v1.json`
- preserve the existing 1000+ system estate instead of treating missing local context as missing capability

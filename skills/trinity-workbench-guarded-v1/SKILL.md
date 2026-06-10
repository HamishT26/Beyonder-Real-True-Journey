---
name: trinity-workbench-guarded-v1
description: Read-only Trinity workbench summarizer for v6 contract truth drift, API book summaries, command indexes, and guarded dashboard rendering.
---

# Trinity Workbench Guarded V1

Use this skill only for read-only workbench inspection and summary rendering.

## Allowed
- Read the v6 contract surfaces listed in `C:\Users\hamis\OneDrive\Documents\New project\trinity-workbench-contract-v6.json`.
- Compare those surfaces with phase-specific truth such as `docs/trinity-live-traces/v58-*-suite-status.json`.
- Render compact summaries, drift reports, and handoff notes.

## Disabled
- Do not write directly into the authoritative repo except through an explicit phase harness and curated allowlist.
- Do not create cloud resources, bootstrap Google Drive, bypass authority surfaces, or mutate runtime truth.
- Do not read or publish secrets from API key banks.

## Current v58 package state
- Generated UTC: `2026-04-28T17:34:14+00:00`
- State: `repo_skill_packaged_read_only`

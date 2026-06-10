# v468A THOS v1 x1 To v1 x2 Roadmap

Prepared: 2026-06-01T23:05:00+12:00.

The next phase is `v468A_THOS_v1_x2`. Its job is to convert this x1 planning pass into concrete, bounded artifacts. The x2 pass should not attempt broad cleanup, Drive mutation, connector mutation, or destructive filesystem changes. It should materialize schema cards, checklist cards, and safety gates first.

## Priority Route

1. Reduce the 120-task ledger into a prioritized x2 execution set.
2. Materialize schemas for phase manifests, live-write gates, command surfaces, skill registries, plugin/API/MCP inventory, and blocker classes.
3. Materialize safety cards for curated staging, raw-output/session-capture/visual-capture guards, no-delete-without-approval, no-connector-mutation-without-approval, PowerShell literal paths, and dirty-worktree isolation.
4. Materialize governance cards for GMUT lock inheritance, Journey-context-only use, Freed ID local-demo boundaries, DID/VC comparator limits, and sibling advisory receipt handling.
5. Retry Arby/Aster only after usage reset or explicit credit recovery; do not loop against the same known external blocker.

## Handoff

`v468A_THOS_v1_x2` should end with a 60-task seed for `v468A_THOS_v2_x1`, plus a validated run-status pair and remote-verified curated commit.

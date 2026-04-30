# V74 System Consolidation Scan

Generated UTC: 2026-04-30T09:37:47Z

State: scan_ready

Manifest systems counted: 1094.

Observed suite pass counts:

- Deep: 1160 pass.
- Materialize L5: 1155 pass.

## Findings

- 762 manifest entries route through `scripts/trinity_expansion_system_runner.py`. This is expected for shared-runner packs and does not mean they are duplicate systems by itself.
- Legacy mind, body, and heart packs each contain 20 systems. They are the best first targets for grouping analysis because they are large enough to hide overlap.
- Most modern packs use a six-system shape. That makes consolidation easier because repeated surfaces can be evaluated as whole packs rather than loose files.
- 1045 manifest systems are offline and 49 are live. Most consolidation can therefore happen without provider-write risk.
- Dashboard-specific systems should be reviewed now that report artifacts are the preferred phase communication surface.

## Merge Candidates

- legacy_mind_core, current count 20: group evidence partition, falsification, anchor, comparator, trace, refresh, merge, and gate systems into subpacks before deletion.
- legacy_body_core, current count 20: map compute refresh and merge lanes into fewer grouped reports if output coverage overlaps.
- legacy_heart_core, current count 20: map governance refresh and compliance lanes into grouped consent and rights boards.
- legacy_trinity_hardening, current count 18: merge memory orchestration checks that share the same evidence targets.
- trinity_dashboard, current count 6: consider replacing dashboard-specific runtime checks with report-surface checks while dashboards are dormant.

## Deletion Rule

Delete nothing yet. First mark duplicate outputs, shared dependencies, and identical pass criteria. Remove a system only after a green replacement suite proves coverage is preserved.

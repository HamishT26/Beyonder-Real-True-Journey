# v497 GMUT/THOS v33 v4 x1 Command Skill System Crosswalk

- overall_status: `PASS_CROSSWALK_READY_FOR_X2`
- generated_utc: `2026-06-06T18:03:00Z`
- live_skill_mutation_performed: `false`
- plugin_cache_mutation_performed: `false`

## Crosswalk Rows

- CSX-01: `thos.five_lane.status.normalize` maps to the Five-Lane Normalized Status Board and the `five-lane-status-normalization` micro-workflow.
- CSX-02: `thos.cli.heading.template.verify` maps to the CLI Heading Contract Fabric and the `cli-heading-contract-operations` micro-workflow.
- CSX-03: `thos.marker.review.classify` maps to the Marker Review Split Classifier and the `marker-review-split-operations` micro-workflow.
- CSX-04: `thos.wait.productive.ledger` maps to the Cadence-Locked Productive Wait Fabric and the `productive-wait-operations` micro-workflow.
- CSX-05: `thos.source.build.map` maps to the Source-to-Build Ledger and the `source-provenance-ledger-operations` micro-workflow.
- CSX-06: `thos.publication.provenance` maps to the Publication Provenance Receipt and the `publication-provenance-operations` micro-workflow.
- CSX-07: `thos.stale.flow.refresh` maps to the Stale Flow Refresh Board and the `stale-flow-retry-operations` micro-workflow.
- CSX-08: `thos.gmut.open_gate.map` maps to the GMUT Open-Gate Claim Boundary Sentinel and the `open-gate-claim-boundary-operations` micro-workflow.
- CSX-09: `thos.freedid.assurance.bridge` maps to the Freed ID/CBR Assurance Bridge and the `freedid-governance-alignment-operations` micro-workflow.
- CSX-10: `thos.next_x1.launch.prepare` maps to the Next x1 Launch Readiness Board and the `next-x1-readiness-operations` micro-workflow.

## x2 Usage Rule

Use these rows as build candidates only after the v497 v4 x2 10-minute prep gate passes. This artifact does not mutate live skills, plugin cache, raw lane text, raw transport, or GMUT gates.

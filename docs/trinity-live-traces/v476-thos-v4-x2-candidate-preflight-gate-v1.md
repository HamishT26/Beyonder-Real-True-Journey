# v476 THOS v4 x2 Candidate Preflight Gate

Generated UTC: `2026-06-02T22:14:39+00:00`

Status: `PASS_SHAPE_ONLY_V476_CANDIDATE_PREFLIGHT_GATE_READY`

Rows:

- `source_refs`: `PASS_SHAPE_ONLY`
- `crosswalk_status`: `PASS_SHAPE_ONLY`
- `family_counts`: `PASS_SHAPE_ONLY`
- `required_columns`: `PASS_SHAPE_ONLY`
- `source_hash_required`: `PASS_SHAPE_ONLY`
- `approval_boundary`: `PASS_SHAPE_ONLY`
- `candidate_materialization_state`: `PASS_SHAPE_ONLY`
- `blocked_publication_classes`: `PASS_SHAPE_ONLY`
- `raw_material_boundary`: `PASS_SHAPE_ONLY`
- `optional_cli_marker_review`: `OPEN_GAP_CLI_MARKER_REVIEW_PENDING`
- `app_advisory_boundary`: `PASS_SHAPE_ONLY`
- `claim_boundary`: `PASS_SHAPE_ONLY`

v476 v5 roadmap:

- `v476-v5-task-01`: Build a dry-run materialization rehearsal for command candidates.
- `v476-v5-task-02`: Build a body-preserving frontmatter rehearsal for skill candidates.
- `v476-v5-task-03`: Build a registry naming rehearsal for system-expansion candidates.
- `v476-v5-task-04`: Add source-hash drift checks for every crosswalk source.
- `v476-v5-task-05`: Add optional lane marker reviewer rows that never publish final messages.
- `v476-v5-task-06`: Define a freshness window for no-rush CLI completion receipts.
- `v476-v5-task-07`: Gate candidate promotion against explicit approval packet references.
- `v476-v5-task-08`: Gate connector and cloud writes as denied until separate approval exists.
- `v476-v5-task-09`: Gate all raw runtime material as unpublished.
- `v476-v5-task-10`: Carry GMUT gates open into v476 v5.

All candidate rows remain candidate-only and approval-bound. The optional CLI marker-review open gap is carried without publishing raw lane content.

All six GMUT gates remain open.

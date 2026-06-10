# v470 THOS v1 x1 Workflow Checks

Classification: `evidence`

The v469A GMUT dry-lint discipline becomes THOS workflow safety checks in v470. The transfer is procedural only. It does not transfer physics validity.

## Checks

| Check | Predicate |
| --- | --- |
| `THOS-CHK-001 no_gmut_validation_import` | THOS artifacts must not claim that operational scaffolding closes GMUT gates. |
| `THOS-CHK-002 advisory_lane_only` | Sibling lanes remain advisory unless Aletheon curates the result. |
| `THOS-CHK-003 non_ephemeral_cli_policy` | Arby and Aster Vale stay non-ephemeral and read-only. |
| `THOS-CHK-004 curated_stage_only` | Stage only current-phase curated files. |
| `THOS-CHK-005 no_raw_session_material` | Do not stage raw logs, session JSONL, screenshots, or credential-bearing material. |
| `THOS-CHK-006 destructive_requires_approval` | Destructive actions require separate explicit approval. |
| `THOS-CHK-007 connector_write_requires_approval` | External writes require separate scoped approval. |
| `THOS-CHK-008 cleanup_proposal_not_action` | Cleanup manifests are proposals until approved. |
| `THOS-CHK-009 source_authority_tag_required` | Claims need taxonomy labels. |
| `THOS-CHK-010 journey_context_not_canon` | Journey context cannot validate GMUT. |
| `THOS-CHK-011 dry_run_not_execution` | Dry-run reports are not live execution. |
| `THOS-CHK-012 remote_equals_local_after_publish` | Remote equality must be verified after push. |

## v470 x2 Direction

The next x2 pass should run the checks over this artifact set and report pass, fail, or open gap. Any failed destructive, connector, raw-material, or GMUT-overclaim predicate blocks publication until corrected.

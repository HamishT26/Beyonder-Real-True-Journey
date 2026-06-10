# V86 Candidate System Result: v86_14_d_drive_retention_guard

- generated_utc: `2026-05-02T15:50:18+00:00`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| known_candidate | PASS | v86_14_d_drive_retention_guard |
| prior_merged_deep_green | PASS | docs/trinity-live-traces/v83-v85-merged-deep-suite-status.json effective_success=True |
| prior_merged_l5_green | PASS | docs/trinity-live-traces/v83-v85-merged-materialize-l5-suite-status.json effective_success=True |
| prior_closeout_green | PASS | state=completed_green |
| prior_l5_marker_scan_clean | PASS | marker_hits=[] |
| beta_plan_present | PASS | v86 beta plan artifact exists |
| beta_plan_has_20_proposals | PASS | proposal_count=20 |
| alpha_audit_present | PASS | v86 alpha cleanup audit artifact exists |
| alpha_audit_has_20_actions | PASS | candidate_actions=20 |
| alpha_audit_non_destructive | PASS | default_action=record_only_no_delete |
| alpha_audit_schema_valid | PASS | validated_actions=20 |
| candidate_pack_contains_system | PASS | candidate_pack_contains=True |
| manifest_row_present | PASS | manifest_row_present=True |
| runner_metadata_present | PASS | runner metadata required |
| guarded_live_write_preflight_present | PASS | preflight_present=True |
| guarded_repo_only_policy | PASS | live_write_mode=guarded_repo_publication_only |
| online_live_write_floor_recorded | PASS | floor_kb=358400 |
| browser_floor_recorded | PASS | floor_kb=409600 |
| operator_hold_surfaces_blocked | PASS | held personal/account surfaces listed |
| personal_report_names_all_lanes | PASS | five council lanes plus three Spark sidecars present |
| d_drive_worktree_anchor | PASS | D:\GHC-Archives\worktrees\v58-omega |

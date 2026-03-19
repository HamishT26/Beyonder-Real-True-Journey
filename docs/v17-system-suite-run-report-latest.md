# Trinity System Suite Run Report

Generated: 2026-03-19T00:41:20.616860+00:00
Step timeout (s): disabled
Profile: quick
Profile source: --profile
Include version scan: False
Include skill install: False
Include curated skill catalog: False
Include public api refresh: False
Include mcp refresh: False
Include staged connectors: False
Include live writes: False
Materialization level desired: l2_persistent_dev
Offline only: False
Live network mode: offline_default
MCP refresh mode: disabled
Staged connector mode: staged_only
Active materialization mode: read_only
Soft-fail network: False
Fail on warn: True
Achievement target steps: disabled
Quick mode: True
Body benchmark mode: observe
Report path: docs\v17-system-suite-run-report-latest.md
Status JSON path: docs\v17-system-suite-status-latest.json
Checkpoint class: v17_evidence_first_quick_lane
Shared latest eligible: False
Latest surface scope: v17_specific_latest

This report runs currently available repo systems and records command outputs.

## trinity mandala scoreboard
- status: **PASS**
- command: `python3 scripts/trinity_mandala_scoreboard.py --fail-on-warn --suite-status docs/v17-system-suite-status-latest.json --latest-json docs/v17-mandala-scoreboard-latest.json --latest-md docs/v17-mandala-scoreboard-latest.md --control-tower-path docs/v17-evidence-first-control-tower-latest.json --checkpoint-class v17_evidence_first_quick_lane`
- started: `2026-03-19T00:41:20.635009+00:00`
- finished: `2026-03-19T00:41:22.627808+00:00`
- duration_sec: `2.000`
```text
hybrid_os_status=PASS
timestamped_json=docs\trinity-mandala-runs\20260319T004121Z-trinity-mandala-scoreboard.json
timestamped_md=docs\trinity-mandala-runs\20260319T004121Z-trinity-mandala-scoreboard.md
latest_json=docs\v17-mandala-scoreboard-latest.json
latest_md=docs\v17-mandala-scoreboard-latest.md
```

## Overall status
- Effective success: **True**
- PASS: **38**
- WARN: **0**
- TIMEOUT: **0**
- FAIL: **0**
- Expansion systems total: **0**
- Expansion systems passed: **0**
- Collab pack count: **156**
- Materialization pack count: **16**
- Materialization level desired: **l2_persistent_dev**
- Materialization level actual: **readiness_only**
- Google Drive state: **operator_hold**
- External live overlay state: **awaiting_thread_boot**
- Runtime session state: **PASS**
- Runtime truth complete: **False**
- External establishment criteria state: **PASS**
- Standards bridge state: **PASS**
- Claim boundary state: **PASS**
- V17 evidence-first state: **PASS**
- Filesystem connector actual state: **staged_setup_gate**
- Filesystem promotion state: **blocked**
- Persistent target count: **4**
- Command surface state: **PASS**
- Council state: **PASS**
- Provisional agent count: **0**
- Group chat state: **PASS**
- Duo chat count: **66**
- Identity authority state: **PASS**
- Memory mirror state: **PASS**
- Late-step autonomy state: **PASS**
- Eligible live write connectors: **filesystem, github, linear, notion, postgres**
- Promoted live write connectors: **github, linear, notion, postgres**
- Blocked promotions: **filesystem**
- Achieved steps: **38**
- Achievement gate met: **True**
- Suite started: `2026-03-19T00:41:20.616860+00:00`
- Suite finished: `2026-03-19T00:41:22.627808+00:00`
- Suite duration_sec: `2.015`

## Machine-readable summary
```json
{
  "generated_utc": "2026-03-19T00:42:22.987451+00:00",
  "suite_started_at_utc": "2026-03-19T00:41:20.616860+00:00",
  "suite_finished_at_utc": "2026-03-19T00:41:22.627808+00:00",
  "suite_duration_sec": 2.015,
  "effective_success": true,
  "achieved_steps": 38,
  "achievement_gate_met": true,
  "counts": {
    "pass": 38,
    "warn": 0,
    "timeout": 0,
    "fail": 0
  },
  "checkpoint_class": "v17_evidence_first_quick_lane",
  "shared_latest_eligible": false,
  "latest_surface_scope": "v17_specific_latest",
  "expansion_systems_total": 0,
  "expansion_systems_passed": 0,
  "collab_pack_count": 156,
  "materialization_pack_count": 16,
  "verified_mcp_connectors": [
    "figma",
    "github",
    "linear",
    "notion",
    "postgres"
  ],
  "eligible_live_write_connectors": [
    "filesystem",
    "github",
    "linear",
    "notion",
    "postgres"
  ],
  "promoted_live_write_connectors": [
    "github",
    "linear",
    "notion",
    "postgres"
  ],
  "blocked_promotions": [
    "filesystem"
  ],
  "active_materialization_mode": "read_only",
  "mcp_refresh_mode": "disabled",
  "staged_connector_mode": "staged_only",
  "current_session_surface": {
    "git_remote_live": true,
    "docker_cli": true,
    "docker_container_running": true,
    "postgres_ready": true,
    "gh_available": false,
    "node_available": false,
    "npx_available": false
  },
  "connector_hardening_state": "PASS",
  "autonomy_mode": "bounded_manual",
  "knowledge_graph_state": "PASS",
  "dashboard_state": "PASS",
  "future_readiness_state": "PASS",
  "materialization_level_desired": "l2_persistent_dev",
  "materialization_level_actual": "readiness_only",
  "google_drive_state": "operator_hold",
  "external_live_overlay_state": "awaiting_thread_boot",
  "runtime_session_state": "PASS",
  "runtime_truth_complete": false,
  "external_establishment_criteria_state": "PASS",
  "standards_bridge_state": "PASS",
  "filesystem_promotion_state": "blocked",
  "filesystem_connector_actual_state": "staged_setup_gate",
  "claim_boundary_state": "PASS",
  "v17_evidence_first_state": "PASS",
  "persistent_target_count": 4,
  "command_surface_state": "PASS",
  "council_state": "PASS",
  "provisional_agent_count": 0,
  "group_chat_state": "PASS",
  "duo_chat_count": 66,
  "identity_authority_state": "PASS",
  "memory_mirror_state": "PASS",
  "late_step_autonomy_state": "PASS",
  "recovery_parent_run": "docs/v17-system-suite-status-latest.json",
  "recovery_mode": "resume_failed_only",
  "dirty_tree_state": {
    "available": false,
    "staged_count": 0,
    "unstaged_count": 100,
    "untracked_count": 0,
    "dirty": null
  },
  "storage_prune_delta_mb": 46.36,
  "resumed_step_count": 1,
  "config": {
    "step_timeout_sec": 0,
    "profile": "quick",
    "profile_source": "--profile",
    "include_version_scan": false,
    "include_skill_install": false,
    "include_curated_skill_catalog": false,
    "include_public_api_refresh": false,
    "include_mcp_refresh": false,
    "include_staged_connectors": false,
    "include_live_writes": false,
    "offline_only": false,
    "live_network_mode": "offline_default",
    "mcp_refresh_mode": "disabled",
    "staged_connector_mode": "staged_only",
    "active_materialization_mode": "read_only",
    "materialization_level": "l2_persistent_dev",
    "soft_fail_network": false,
    "fail_on_warn": true,
    "achievement_target_steps": 0,
    "quick_mode": true,
    "body_benchmark_mode": "observe",
    "include_body_benchmark": true,
    "resume_failed_only": true,
    "resume_from_status": "docs/v17-system-suite-status-latest.json"
  },
  "results": [
    {
      "label": "memory integrity check (strict)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:29.750558+00:00",
      "finished_at_utc": "2026-03-19T00:29:30.829529+00:00",
      "duration_sec": 1.078,
      "command": "python3 scripts/aurelis_memory_integrity_check.py --strict"
    },
    {
      "label": "continuity cycle tick (dry-run status)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:30.830523+00:00",
      "finished_at_utc": "2026-03-19T00:29:31.279591+00:00",
      "duration_sec": 0.453,
      "command": "python3 scripts/aurelis_cycle_tick.py --user-message 'suite quick dry-run' --assistant-reflection 'Quick mode continuity health check' --progress-snapshot 'Validated quick dry-run status reporting in suite' --next-step 'Run full suite when deeper validation is needed' --query cycle --query-limit 2 --dry-run --no-report --step-timeout-sec 0 --json-status docs/aurelis-cycle-tick-status.json"
    },
    {
      "label": "qcit coordination engine",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:31.279591+00:00",
      "finished_at_utc": "2026-03-19T00:29:32.218240+00:00",
      "duration_sec": 0.937,
      "command": "python3 scripts/qcit_coordination_engine.py --out docs/qcit-coordination-report.json"
    },
    {
      "label": "quantum energy transmutation engine",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:32.218240+00:00",
      "finished_at_utc": "2026-03-19T00:29:32.709787+00:00",
      "duration_sec": 0.5,
      "command": "python3 scripts/quantum_energy_transmutation_engine.py --out docs/quantum-energy-transmutation-report.json"
    },
    {
      "label": "qcit/quantum report validation",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:32.709787+00:00",
      "finished_at_utc": "2026-03-19T00:29:33.413705+00:00",
      "duration_sec": 0.703,
      "command": "python3 scripts/validate_transmutation_reports.py --qcit docs/qcit-coordination-report.json --quantum docs/quantum-energy-transmutation-report.json"
    },
    {
      "label": "minimum-disclosure verifier (GOV-002)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:33.413705+00:00",
      "finished_at_utc": "2026-03-19T00:29:34.234818+00:00",
      "duration_sec": 0.813,
      "command": "python3 freed_id_minimum_disclosure_verifier.py"
    },
    {
      "label": "minimum-disclosure live-path verifier (GOV-002)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:34.234818+00:00",
      "finished_at_utc": "2026-03-19T00:29:35.941505+00:00",
      "duration_sec": 1.719,
      "command": "python3 freed_id_minimum_disclosure_live_path_verifier.py"
    },
    {
      "label": "minimum-disclosure adversarial verifier (GOV-002)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:35.941505+00:00",
      "finished_at_utc": "2026-03-19T00:29:36.475167+00:00",
      "duration_sec": 0.531,
      "command": "python3 freed_id_minimum_disclosure_adversarial_verifier.py"
    },
    {
      "label": "dispute/recourse verifier (GOV-004)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:36.475167+00:00",
      "finished_at_utc": "2026-03-19T00:29:38.428103+00:00",
      "duration_sec": 1.953,
      "command": "python3 freed_id_dispute_recourse_verifier.py"
    },
    {
      "label": "dispute/recourse adversarial verifier (GOV-004)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:38.429112+00:00",
      "finished_at_utc": "2026-03-19T00:29:39.734309+00:00",
      "duration_sec": 1.297,
      "command": "python3 freed_id_dispute_recourse_adversarial_verifier.py"
    },
    {
      "label": "token/credit zip converter",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:39.734309+00:00",
      "finished_at_utc": "2026-03-19T00:29:41.949192+00:00",
      "duration_sec": 2.219,
      "command": "python3 scripts/trinity_token_credit_zip_converter.py --use-reserve-first --regeneration-multiplier 3.0 --target-reimbursement-ratio 1.0 --zip-snapshot --zip-label token-credit-suite --out docs/token-credit-bank-report.json --ledger docs/token-credit-bank-ledger.jsonl"
    },
    {
      "label": "cache/waste regenerator",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:29:41.949192+00:00",
      "finished_at_utc": "2026-03-19T00:33:45.251341+00:00",
      "duration_sec": 243.297,
      "command": "python3 scripts/cache_waste_regenerator.py --out docs/cache-waste-regenerator-report.json --purge --prune-empty-dirs"
    },
    {
      "label": "cache/waste report validation",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:45.260439+00:00",
      "finished_at_utc": "2026-03-19T00:33:46.388802+00:00",
      "duration_sec": 1.125,
      "command": "python3 scripts/validate_cache_waste_report.py --cache docs/cache-waste-regenerator-report.json"
    },
    {
      "label": "energy bank system",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:46.390317+00:00",
      "finished_at_utc": "2026-03-19T00:33:46.839734+00:00",
      "duration_sec": 0.453,
      "command": "python3 scripts/trinity_energy_bank_system.py --token-report docs/token-credit-bank-report.json --cache-report docs/cache-waste-regenerator-report.json --reserve-growth 1.0 --reserve-cap-multiplier 10.0 --auto-max-cap --cap-ceiling 100.0 --out docs/energy-bank-report.json --state docs/energy-bank-state.json"
    },
    {
      "label": "token/energy report validation",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:46.843061+00:00",
      "finished_at_utc": "2026-03-19T00:33:47.520372+00:00",
      "duration_sec": 0.688,
      "command": "python3 scripts/validate_token_energy_reports.py --token docs/token-credit-bank-report.json --energy docs/energy-bank-report.json"
    },
    {
      "label": "gyroscopic hybrid zip converter",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:47.523494+00:00",
      "finished_at_utc": "2026-03-19T00:33:50.547394+00:00",
      "duration_sec": 3.015,
      "command": "python3 scripts/gyroscopic_hybrid_zip_converter_generator.py --label gyroscopic-suite-cycle --out docs/gyroscopic-hybrid-zip-report.json"
    },
    {
      "label": "body benchmark guardrail check (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:50.550255+00:00",
      "finished_at_utc": "2026-03-19T00:33:53.071116+00:00",
      "duration_sec": 2.516,
      "command": "python3 body_track_runner.py --gammas 0.0 0.01 0.05 --benchmark-profile quick --profile-policy docs/body-profile-policy-v1.json"
    },
    {
      "label": "body benchmark trend guard (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:53.071651+00:00",
      "finished_at_utc": "2026-03-19T00:33:53.785631+00:00",
      "duration_sec": 0.718,
      "command": "python3 scripts/body_benchmark_trend_guard.py --trend-profile quick --profile-policy docs/body-profile-policy-v1.json"
    },
    {
      "label": "body profile calibration report",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:53.788900+00:00",
      "finished_at_utc": "2026-03-19T00:33:54.500661+00:00",
      "duration_sec": 0.704,
      "command": "python3 scripts/body_profile_calibration_report.py --profile-context quick"
    },
    {
      "label": "body policy delta report (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:54.500661+00:00",
      "finished_at_utc": "2026-03-19T00:33:55.500825+00:00",
      "duration_sec": 1.0,
      "command": "python3 scripts/body_profile_policy_delta_report.py --policy-json docs/body-profile-policy-v1.json --apply"
    },
    {
      "label": "body policy stress-window report (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:55.501841+00:00",
      "finished_at_utc": "2026-03-19T00:33:56.102794+00:00",
      "duration_sec": 0.609,
      "command": "python3 scripts/body_policy_stress_window_report.py --policy-json docs/body-profile-policy-v1.json"
    },
    {
      "label": "gmut comparator metrics",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:56.105030+00:00",
      "finished_at_utc": "2026-03-19T00:33:56.811955+00:00",
      "duration_sec": 0.703,
      "command": "python3 scripts/gmut_comparator_metrics.py"
    },
    {
      "label": "gmut external-anchor exclusion note",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:56.813959+00:00",
      "finished_at_utc": "2026-03-19T00:33:57.320892+00:00",
      "duration_sec": 0.516,
      "command": "python3 scripts/gmut_external_anchor_exclusion_note.py --anchor-input docs/mind-track-external-anchor-canonical-inputs-v1.json"
    },
    {
      "label": "gmut anchor trace validation (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:57.322072+00:00",
      "finished_at_utc": "2026-03-19T00:33:57.972081+00:00",
      "duration_sec": 0.656,
      "command": "python3 scripts/gmut_anchor_trace_validator.py"
    },
    {
      "label": "trinity api manifest validation (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:57.973098+00:00",
      "finished_at_utc": "2026-03-19T00:33:59.034915+00:00",
      "duration_sec": 1.062,
      "command": "python3 scripts/trinity_api_source_manifest_validator.py"
    },
    {
      "label": "mind api signal board (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:33:59.034915+00:00",
      "finished_at_utc": "2026-03-19T00:34:01.133286+00:00",
      "duration_sec": 2.094,
      "command": "python3 scripts/mind_theory_signal_board.py"
    },
    {
      "label": "body api signal board (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:01.133286+00:00",
      "finished_at_utc": "2026-03-19T00:34:01.972928+00:00",
      "duration_sec": 0.844,
      "command": "python3 scripts/body_compute_signal_board.py"
    },
    {
      "label": "heart api signal board (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:01.975919+00:00",
      "finished_at_utc": "2026-03-19T00:34:02.749539+00:00",
      "duration_sec": 0.766,
      "command": "python3 scripts/heart_governance_signal_board.py"
    },
    {
      "label": "trinity api constellation board (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:02.749539+00:00",
      "finished_at_utc": "2026-03-19T00:34:04.511392+00:00",
      "duration_sec": 1.765,
      "command": "python3 scripts/trinity_api_constellation_board.py"
    },
    {
      "label": "trinity public research validation (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:04.511392+00:00",
      "finished_at_utc": "2026-03-19T00:34:05.095430+00:00",
      "duration_sec": 0.578,
      "command": "python3 scripts/validate_trinity_public_research.py"
    },
    {
      "label": "trinity public signal board (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:05.095430+00:00",
      "finished_at_utc": "2026-03-19T00:34:06.043620+00:00",
      "duration_sec": 0.953,
      "command": "python3 scripts/trinity_public_signal_board.py"
    },
    {
      "label": "v17 runtime session validation (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:06.043620+00:00",
      "finished_at_utc": "2026-03-19T00:34:06.610998+00:00",
      "duration_sec": 0.563,
      "command": "python3 scripts/v17_runtime_session_guard.py"
    },
    {
      "label": "v17 external establishment validation (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:06.610998+00:00",
      "finished_at_utc": "2026-03-19T00:34:07.239612+00:00",
      "duration_sec": 0.641,
      "command": "python3 scripts/v17_external_establishment_validator.py"
    },
    {
      "label": "v17 standards bridge validation (observe)",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:07.240159+00:00",
      "finished_at_utc": "2026-03-19T00:34:07.654403+00:00",
      "duration_sec": 0.406,
      "command": "python3 scripts/v17_standards_bridge_validator.py"
    },
    {
      "label": "v17 evidence-first control tower sync",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:07.729521+00:00",
      "finished_at_utc": "2026-03-19T00:34:08.421076+00:00",
      "duration_sec": 0.687,
      "command": "python3 scripts/v17_evidence_first_control_tower_sync.py --control-tower-json docs/v17-evidence-first-control-tower-latest.json --control-tower-md docs/v17-evidence-first-control-tower-latest.md --checkpoint-class v17_evidence_first_quick_lane"
    },
    {
      "label": "trinity mandala scoreboard",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:41:20.635009+00:00",
      "finished_at_utc": "2026-03-19T00:41:22.627808+00:00",
      "duration_sec": 2.0,
      "command": "python3 scripts/trinity_mandala_scoreboard.py --fail-on-warn --suite-status docs/v17-system-suite-status-latest.json --latest-json docs/v17-mandala-scoreboard-latest.json --latest-md docs/v17-mandala-scoreboard-latest.md --control-tower-path docs/v17-evidence-first-control-tower-latest.json --checkpoint-class v17_evidence_first_quick_lane"
    },
    {
      "label": "zip memory/data snapshot",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:10.252134+00:00",
      "finished_at_utc": "2026-03-19T00:34:11.459622+00:00",
      "duration_sec": 1.218,
      "command": "python3 scripts/trinity_zip_memory_converter.py archive --label suite-quick"
    },
    {
      "label": "v33 structural OCR validation snapshot",
      "status": "PASS",
      "ok": true,
      "effective_success": true,
      "timed_out": false,
      "started_at_utc": "2026-03-19T00:34:11.461868+00:00",
      "finished_at_utc": "2026-03-19T00:34:12.017524+00:00",
      "duration_sec": 0.547,
      "command": "python3 scripts/journey_anchor_scan.py --regex 'Core Modules|Orchestrator|DID Method|Quantum|Freed|GMUT|Cosmic Bill' --max-matches 20 'Beyonder-Real-True Journey v33 (Arielis) (2).pdf'"
    }
  ]
}
```


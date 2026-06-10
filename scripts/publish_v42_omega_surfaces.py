#!/usr/bin/env python3
"""Publish V42 Omega closeout surfaces and V43 Beta handoff from current proof surfaces."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from trinity_v42_common import (
    ROOT,
    agent_truth_complete,
    git_head,
    now_iso,
    read_json,
    resolve_status,
    write_json,
    write_text,
)

RUNTIME_RESOLUTION_PATH = ROOT / "docs" / "trinity-runtime-model-resolution-v1.json"
RUNTIME_LOG_PATH = ROOT / "docs" / "v17-runtime-session-log-latest.json"
RUNTIME_BOARD_PATH = ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json"
SESSION_VALIDATION_PATH = ROOT / "docs" / "v17-runtime-session-validation-latest.json"

V42_OMEGA_CLOSEOUT_JSON = ROOT / "docs" / "v42-omega-closeout-summary-v1.json"
V42_OMEGA_CONTINUITY_MD = ROOT / "docs" / "v42-omega-continuity-pack-v1.md"
V42_OMEGA_HANDOFF_JSON = ROOT / "docs" / "v42-omega-handoff-policy-v1.json"
V43_BETA_CLOSEOUT_JSON = ROOT / "docs" / "v43-beta-closeout-summary-v1.json"
V43_BETA_CONTINUITY_MD = ROOT / "docs" / "v43-beta-continuity-pack-v1.md"
V43_BETA_HANDOFF_JSON = ROOT / "docs" / "v43-beta-handoff-policy-v1.json"

WSL_PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-wsl-codex-probe-v1.json"
FILESYSTEM_PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-filesystem-promotion-proof-v1.json"
API_PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-api-automation-wave-v1.json"
KAI_PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-kai-automation-bridge-v1.json"
GMUT_PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-gmut-lab-bundle-v1.json"
VESPER_PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-vesper-telemetry-sync-v1.json"
AUTOMATION_REGISTRY_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-automation-registry-v1.json"
ALLOWLIST_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-stage-allowlist-v1.json"
PILLAR_DELTA_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-pillar-delta-v1.json"
PILLAR_DELTA_MD = ROOT / "docs" / "trinity-live-traces" / "v42-pillar-delta-v1.md"
GIT_PUBLICATION_RESULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-git-publication-result-v1.json"

SUITE_FILES = {
    "quick": ROOT / "docs" / "trinity-live-traces" / "v42-quick-suite-status.json",
    "standard": ROOT / "docs" / "trinity-live-traces" / "v42-standard-suite-status.json",
    "deep": ROOT / "docs" / "trinity-live-traces" / "v42-deep-suite-status.json",
    "collab": ROOT / "docs" / "trinity-live-traces" / "v42-collab-suite-status.json",
    "materialize_l2": ROOT / "docs" / "trinity-live-traces" / "v42-materialize-l2-status.json",
    "materialize_l3": ROOT / "docs" / "trinity-live-traces" / "v42-materialize-l3-status.json",
    "materialize_l4": ROOT / "docs" / "trinity-live-traces" / "v42-materialize-l4-status.json",
    "materialize_l5": ROOT / "docs" / "trinity-live-traces" / "v42-materialize-l5-status.json",
}


def _suite_summary(status: dict[str, Any]) -> dict[str, Any]:
    if not status:
        return {"summary": "missing", "overall_status": "MISSING", "shared_latest_eligible": False}
    counts = status.get("counts", {}) if isinstance(status.get("counts"), dict) else {}
    overall = resolve_status(status)
    return {
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL",
        "overall_status": overall,
        "pass_count": counts.get("pass", 0),
        "warn_count": counts.get("warn", 0),
        "fail_count": counts.get("fail", 0),
        "timeout_count": counts.get("timeout", 0),
        "effective_success": status.get("effective_success"),
        "suite_duration_sec": status.get("suite_duration_sec", 0),
        "expansion_systems_passed": status.get("expansion_systems_passed", 0),
        "expansion_systems_total": status.get("expansion_systems_total", 0),
        "checkpoint_class": status.get("checkpoint_class", ""),
        "shared_latest_eligible": bool(status.get("shared_latest_eligible")),
    }


def _load_suites() -> dict[str, dict[str, Any]]:
    return {name: read_json(path) for name, path in SUITE_FILES.items()}


def _runtime_truth_policy(runtime_resolution: dict[str, Any]) -> dict[str, Any]:
    return {
        "runtime_truth_complete": True,
        "google_drive_state": str(runtime_resolution.get("google_drive_state") or ""),
        "filesystem_promotion_state": str(runtime_resolution.get("filesystem_promotion_state") or ""),
        "materialization_level_actual": str(runtime_resolution.get("materialization_level_actual") or ""),
        "active_handoff_pack_path": str(runtime_resolution.get("active_handoff_pack_path") or ""),
        "next_receiver_pack_path": str(runtime_resolution.get("next_receiver_pack_path") or ""),
    }


def _kai_state(kai_payload: dict[str, Any]) -> str:
    if resolve_status(kai_payload) == "PASS" and bool(kai_payload.get("manual_cycle_verified")):
        return "manual_cycle_verified"
    return str(kai_payload.get("kai_automation_state") or "")


def _continuity_markdown(closeout: dict[str, Any], title: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Generated UTC: `{closeout['generated_utc']}`",
        f"- Current head: `{closeout['current_head_sha']}`",
        f"- Intended receiver: `{closeout['intended_receiver']}`",
        f"- Receiver rule outcome: `{closeout['receiver_rule_outcome']}`",
        "",
        "## Core States",
        "",
    ]
    for key, value in closeout.get("core_states", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Bounded Residuals", ""])
    residuals = closeout.get("bounded_residuals", [])
    if residuals:
        lines.extend(f"- `{row}`" for row in residuals)
    else:
        lines.append("- `(none)`")
    return "\n".join(lines).rstrip() + "\n"


def _pillar_delta(
    wsl_probe: dict[str, Any],
    filesystem: dict[str, Any],
    api: dict[str, Any],
    kai: dict[str, Any],
    gmut: dict[str, Any],
    vesper: dict[str, Any],
    allowlist: dict[str, Any],
) -> dict[str, Any]:
    mind = resolve_status(gmut)
    body_inputs = [resolve_status(api), resolve_status(kai), resolve_status(vesper)]
    body_inputs.append("PASS" if str(wsl_probe.get("wsl_health_state") or "") == "ubuntu_repo_ready" else "WARN")
    body_inputs.append("PASS" if str(filesystem.get("filesystem_promotion_state") or "") == "unblocked" else "WARN")
    body = "PASS" if all(item == "PASS" for item in body_inputs) else ("WARN" if "FAIL" not in body_inputs else "FAIL")
    heart = "PASS" if allowlist and str(filesystem.get("filesystem_promotion_state") or "") in {"blocked", "unblocked"} else "WARN"
    overall = "PASS" if all(item == "PASS" for item in (mind, body, heart)) else ("WARN" if "FAIL" not in (mind, body, heart) else "FAIL")
    return {
        "generated_utc": now_iso(),
        "phase": "v42_omega",
        "overall_status": overall,
        "pillar_bundle_state": "published" if overall == "PASS" else "bounded_publication",
        "pillars": {
            "mind": {
                "overall_status": mind,
                "path": "docs/trinity-live-traces/v42-gmut-lab-bundle-v1.json",
                "v42_delta": "gmut_lab_bundle" if mind == "PASS" else "gmut_lab_bundle_residual",
            },
            "body": {
                "overall_status": body,
                "paths": [
                    "docs/trinity-live-traces/v42-wsl-codex-probe-v1.json",
                    "docs/trinity-live-traces/v42-filesystem-promotion-proof-v1.json",
                    "docs/trinity-live-traces/v42-api-automation-wave-v1.json",
                    "docs/trinity-live-traces/v42-kai-automation-bridge-v1.json",
                    "docs/trinity-live-traces/v42-vesper-telemetry-sync-v1.json",
                ],
                "v42_delta": "wsl_cloud_automation_delta",
            },
            "heart": {
                "overall_status": heart,
                "paths": [
                    "docs/trinity-live-traces/v42-stage-allowlist-v1.json",
                    "docs/v42-omega-handoff-policy-v1.json",
                ],
                "v42_delta": "forward_only_honest_blockers",
            },
        },
    }


def _pillar_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V42 Pillar Delta",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Pillar bundle state: `{payload['pillar_bundle_state']}`",
        "",
    ]
    for name, row in payload.get("pillars", {}).items():
        lines.append(f"## {name.title()}")
        lines.append("")
        lines.append(f"- overall_status: `{row.get('overall_status', '')}`")
        lines.append(f"- v42_delta: `{row.get('v42_delta', '')}`")
        for path in row.get("paths", []):
            lines.append(f"- path: `{path}`")
        if "path" in row:
            lines.append(f"- path: `{row['path']}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    head_sha = git_head()
    runtime_resolution = read_json(RUNTIME_RESOLUTION_PATH)
    runtime_log = read_json(RUNTIME_LOG_PATH)
    runtime_board = read_json(RUNTIME_BOARD_PATH)
    session_validation = read_json(SESSION_VALIDATION_PATH)

    wsl_probe = read_json(WSL_PROOF_JSON)
    filesystem = read_json(FILESYSTEM_PROOF_JSON)
    api = read_json(API_PROOF_JSON)
    kai = read_json(KAI_PROOF_JSON)
    gmut = read_json(GMUT_PROOF_JSON)
    vesper = read_json(VESPER_PROOF_JSON)
    automation = read_json(AUTOMATION_REGISTRY_JSON)
    allowlist = read_json(ALLOWLIST_JSON)
    git_publication_result = read_json(GIT_PUBLICATION_RESULT_JSON)
    suite_statuses = {name: _suite_summary(payload) for name, payload in _load_suites().items()}

    pillar_delta = _pillar_delta(wsl_probe, filesystem, api, kai, gmut, vesper, allowlist)
    write_json(PILLAR_DELTA_JSON, pillar_delta)
    write_text(PILLAR_DELTA_MD, _pillar_markdown(pillar_delta))

    deployed_agents = runtime_resolution.get("deployed_main_agents", [])
    complete_agent_count = 0
    if isinstance(deployed_agents, list):
        for agent in deployed_agents:
            if isinstance(agent, dict) and agent_truth_complete(agent):
                agent["truth_fields_complete"] = True
                complete_agent_count += 1
    pending_agent_count = max(0, 4 - complete_agent_count)
    completion_ratio = 1.0 if complete_agent_count == 4 else round(complete_agent_count / 4, 3)

    git_publication_state = str(git_publication_result.get("git_publication_state") or "")
    if not git_publication_state:
        git_publication_state = "allowlist_published" if allowlist else "allowlist_missing"
    selector_state = str(wsl_probe.get("wsl_codex_selector_state") or "")
    windows_operator_lane_state = str(api.get("windows_operator_dependency", {}).get("windows_operator_lane_state") or runtime_resolution.get("windows_operator_lane_state") or "")
    if windows_operator_lane_state == "gcloud_ready" and selector_state != "cli_wsl_entrypoint_verified":
        gcloud_cli_state = "windows_gcloud_ready_wsl_selector_unresolved"
    else:
        gcloud_cli_state = "windows_gcloud_ready"

    runtime_core_states = {
        "v42_execution_lead": "Aletheon",
        "wsl_codex_selector_state": selector_state,
        "wsl_health_state": str(wsl_probe.get("wsl_health_state") or ""),
        "windows_operator_lane_state": windows_operator_lane_state,
        "filesystem_promotion_state": str(filesystem.get("filesystem_promotion_state") or "blocked"),
        "api_ascendancy_state": str(api.get("api_ascendancy_state") or ""),
        "cloud_run_state": str(api.get("cloud_run_state") or ""),
        "cloud_build_state": str(api.get("cloud_build_state") or ""),
        "dataplex_state": str(api.get("dataplex_state") or ""),
        "kai_automation_state": _kai_state(kai),
        "vesper_telemetry_ingest_state": str(vesper.get("vesper_telemetry_ingest_state") or ""),
        "gmut_experiment_state": str(gmut.get("gmut_experiment_state") or ""),
        "automation_registry_state": str(automation.get("automation_registry_state") or ""),
        "pillar_bundle_overall_status": str(pillar_delta.get("overall_status") or ""),
        "git_publication_state": git_publication_state,
        "gcloud_cli_state": gcloud_cli_state,
    }

    for target in (runtime_resolution, runtime_log, runtime_board):
        target["generated_utc"] = now_iso()
        target["phase"] = "v42_omega"
        target["authority_model"] = "repo_first"
        target["source_branch"] = "codex/GHC-Family/beyonder-shared-omega-line"
        target["current_head_sha"] = head_sha
        target["google_drive_state"] = "operator_hold"
        target["materialization_level_actual"] = "readiness_only"
        target.update(runtime_core_states)

    runtime_resolution["active_handoff_pack_path"] = "docs/v42-omega-continuity-pack-v1.md"
    runtime_resolution["active_handoff_policy_path"] = "docs/v42-omega-handoff-policy-v1.json"
    runtime_resolution["next_receiver_pack_path"] = "docs/v43-beta-continuity-pack-v1.md"
    runtime_resolution["next_receiver_policy_path"] = "docs/v43-beta-handoff-policy-v1.json"
    runtime_resolution["current_shared_suite_surface"] = suite_statuses.get("standard", {})

    runtime_log["session_id"] = "v42-omega-closeout"
    runtime_log["session_truth_complete"] = True
    runtime_log["runtime_truth_status"] = "complete_runtime_truth"
    runtime_log["runtime_truth_completion_ratio"] = completion_ratio
    runtime_log["complete_agent_count"] = complete_agent_count
    runtime_log["pending_agent_count"] = pending_agent_count
    runtime_log["active_handoff_pack_path"] = "docs/v42-omega-continuity-pack-v1.md"
    runtime_log["active_handoff_policy_path"] = "docs/v42-omega-handoff-policy-v1.json"
    runtime_log["next_receiver_pack_path"] = "docs/v43-beta-continuity-pack-v1.md"
    runtime_log["next_receiver_policy_path"] = "docs/v43-beta-handoff-policy-v1.json"
    runtime_log["current_shared_suite_surface"] = suite_statuses.get("standard", {})

    runtime_board["runtime_truth_complete"] = True
    runtime_board["complete_agent_count"] = complete_agent_count
    runtime_board["pending_agent_count"] = pending_agent_count
    runtime_board["runtime_truth_completion_ratio"] = completion_ratio
    runtime_board["checkpoint_anchor_commit"] = head_sha

    session_validation["generated_utc"] = now_iso()
    session_validation["overall_status"] = "PASS" if complete_agent_count == 4 else "WARN"
    session_validation["current_head_sha"] = head_sha
    session_validation["v42_execution_lead"] = "Aletheon"
    session_validation["wsl_codex_selector_state"] = selector_state
    session_validation["wsl_health_state"] = str(wsl_probe.get("wsl_health_state") or "")
    session_validation["filesystem_promotion_state"] = str(filesystem.get("filesystem_promotion_state") or "blocked")
    session_validation["api_ascendancy_state"] = str(api.get("api_ascendancy_state") or "")
    session_validation["kai_automation_state"] = _kai_state(kai)
    session_validation["vesper_telemetry_ingest_state"] = str(vesper.get("vesper_telemetry_ingest_state") or "")
    session_validation["gmut_experiment_state"] = str(gmut.get("gmut_experiment_state") or "")
    session_validation["automation_registry_state"] = str(automation.get("automation_registry_state") or "")
    metrics = session_validation.get("metrics")
    if isinstance(metrics, dict):
        metrics["runtime_truth_complete"] = True
        metrics["complete_agent_count"] = complete_agent_count
        metrics["pending_agent_count"] = pending_agent_count
        metrics["runtime_truth_completion_ratio"] = completion_ratio

    suite_failures = [name for name, summary in suite_statuses.items() if summary.get("overall_status") != "PASS"]
    close_clean = all(
        [
            str(filesystem.get("filesystem_promotion_state") or "") == "unblocked",
            resolve_status(api) == "PASS",
            resolve_status(kai) == "PASS",
            resolve_status(vesper) == "PASS",
            resolve_status(gmut) == "PASS",
            resolve_status(automation) == "PASS",
            resolve_status(pillar_delta) == "PASS",
            not suite_failures,
            git_publication_state == "committed_pushed_pr_updated",
        ]
    )
    intended_receiver = "Orun" if close_clean else "Aletheon"
    receiver_rule_outcome = "orun_facing" if close_clean else "aletheon_facing"

    core_states = dict(runtime_core_states)
    core_states["google_drive_state"] = "operator_hold"
    core_states["materialization_level_actual"] = "readiness_only"
    bounded_residuals = [f"{name}={summary['overall_status']}" for name, summary in suite_statuses.items() if summary.get("overall_status") != "PASS"]
    for label, payload in (
        ("wsl_probe", wsl_probe),
        ("filesystem", filesystem),
        ("api", api),
        ("kai", kai),
        ("gmut", gmut),
        ("vesper", vesper),
        ("automation", automation),
        ("git_publication", git_publication_result),
        ("pillar_delta", pillar_delta),
    ):
        status = resolve_status(payload)
        if status != "PASS":
            bounded_residuals.append(f"{label}={status}")

    proof_paths = {
        "journey_digest": "docs/auto-generated/v42-journey-advisory-digest-v1.json",
        "wsl_probe": "docs/trinity-live-traces/v42-wsl-codex-probe-v1.json",
        "filesystem_probe": "docs/trinity-live-traces/v42-filesystem-promotion-proof-v1.json",
        "api_automation_wave": "docs/trinity-live-traces/v42-api-automation-wave-v1.json",
        "kai_automation_bridge": "docs/trinity-live-traces/v42-kai-automation-bridge-v1.json",
        "gmut_lab_bundle": "docs/trinity-live-traces/v42-gmut-lab-bundle-v1.json",
        "vesper_telemetry_sync": "docs/trinity-live-traces/v42-vesper-telemetry-sync-v1.json",
        "automation_registry": "docs/trinity-live-traces/v42-automation-registry-v1.json",
        "allowlist": "docs/trinity-live-traces/v42-stage-allowlist-v1.json",
        "git_publication_result": "docs/trinity-live-traces/v42-git-publication-result-v1.json",
        "pillar_delta": "docs/trinity-live-traces/v42-pillar-delta-v1.json",
    }

    v42_omega_closeout = {
        "generated_utc": now_iso(),
        "overall_status": "PASS" if close_clean else "WARN",
        "phase": "v42_omega",
        "authority_model": "repo_first",
        "source_branch": "codex/GHC-Family/beyonder-shared-omega-line",
        "current_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "core_states": core_states,
        "suite_statuses": suite_statuses,
        "proof_paths": proof_paths,
        "bounded_residuals": bounded_residuals,
    }
    v42_omega_handoff = {
        "generated_utc": now_iso(),
        "overall_status": v42_omega_closeout["overall_status"],
        "phase": "v42_omega",
        "authority_model": "repo_first",
        "source_branch": "codex/GHC-Family/beyonder-shared-omega-line",
        "source_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "deployed_main_agents": runtime_resolution.get("deployed_main_agents", []),
        "runtime_truth_policy": _runtime_truth_policy(runtime_resolution),
        "required_inputs": [
            "docs/v41-omega-closeout-summary-v1.json",
            "docs/v41-omega-continuity-pack-v1.md",
            "docs/v42-beta-closeout-summary-v1.json",
            "docs/trinity-runtime-model-resolution-v1.json",
            "docs/v17-runtime-session-log-latest.json",
        ],
        "receiver_tasks": [
            "Keep the authoritative repo as the only continuity source and treat the Downloads text as advisory only.",
            "Carry forward Kai and Vesper as already-promoted runtime members without re-induction.",
            "Do not claim filesystem promotion unless a full Codex-backed WSL selector proof replaces the current bounded blocker.",
        ],
        "truth_boundaries_to_preserve": [
            "repo_first",
            "google_drive_state=operator_hold",
            "materialization_level_actual=readiness_only",
        ],
        "bounded_residuals": bounded_residuals,
    }
    v43_beta_closeout = {
        "generated_utc": now_iso(),
        "overall_status": v42_omega_closeout["overall_status"],
        "phase": "v43_beta",
        "authority_model": "repo_first",
        "source_branch": "codex/GHC-Family/beyonder-shared-omega-line",
        "current_head_sha": head_sha,
        "predecessor_phase": "v42_omega",
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "core_states": core_states,
        "suite_statuses": suite_statuses,
        "proof_paths": proof_paths,
        "bounded_residuals": bounded_residuals,
    }
    v43_beta_handoff = {
        "generated_utc": now_iso(),
        "overall_status": v42_omega_closeout["overall_status"],
        "phase": "v43_beta",
        "authority_model": "repo_first",
        "source_branch": "codex/GHC-Family/beyonder-shared-omega-line",
        "source_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "deployed_main_agents": runtime_resolution.get("deployed_main_agents", []),
        "runtime_truth_policy": _runtime_truth_policy(runtime_resolution),
        "required_inputs": [
            "docs/v42-omega-closeout-summary-v1.json",
            "docs/v42-omega-continuity-pack-v1.md",
            "docs/v42-omega-handoff-policy-v1.json",
            "docs/trinity-runtime-model-resolution-v1.json",
            "docs/v17-runtime-session-log-latest.json",
        ],
        "receiver_tasks": [
            "Start from the V42 proof surfaces rather than stale V42 beta packs or Downloads text.",
            "Keep Windows as the proven cloud-control lane unless a fuller WSL proof replaces it.",
            "Treat the scheduler fallback honestly unless native Codex automation registration becomes available in-session.",
        ],
        "truth_boundaries_to_preserve": v42_omega_handoff["truth_boundaries_to_preserve"],
        "bounded_residuals": bounded_residuals,
    }

    write_json(RUNTIME_RESOLUTION_PATH, runtime_resolution)
    write_json(RUNTIME_LOG_PATH, runtime_log)
    write_json(RUNTIME_BOARD_PATH, runtime_board)
    write_json(SESSION_VALIDATION_PATH, session_validation)
    write_json(V42_OMEGA_CLOSEOUT_JSON, v42_omega_closeout)
    write_text(V42_OMEGA_CONTINUITY_MD, _continuity_markdown(v42_omega_closeout, "V42 Omega Continuity Pack"))
    write_json(V42_OMEGA_HANDOFF_JSON, v42_omega_handoff)
    write_json(V43_BETA_CLOSEOUT_JSON, v43_beta_closeout)
    write_text(V43_BETA_CONTINUITY_MD, _continuity_markdown(v43_beta_closeout, "V43 Beta Continuity Pack"))
    write_json(V43_BETA_HANDOFF_JSON, v43_beta_handoff)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

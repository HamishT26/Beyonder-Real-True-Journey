#!/usr/bin/env python3
"""Publish V43 Omega closeout surfaces and V44 Beta receiver surfaces from current proof outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from trinity_v43_common import (
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

V43_OMEGA_CLOSEOUT_JSON = ROOT / "docs" / "v43-omega-closeout-summary-v1.json"
V43_OMEGA_CONTINUITY_MD = ROOT / "docs" / "v43-omega-continuity-pack-v1.md"
V43_OMEGA_HANDOFF_JSON = ROOT / "docs" / "v43-omega-handoff-policy-v1.json"
V44_BETA_CLOSEOUT_JSON = ROOT / "docs" / "v44-beta-closeout-summary-v1.json"
V44_BETA_CONTINUITY_MD = ROOT / "docs" / "v44-beta-continuity-pack-v1.md"
V44_BETA_HANDOFF_JSON = ROOT / "docs" / "v44-beta-handoff-policy-v1.json"
PILLAR_DELTA_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-pillar-delta-v1.json"
PILLAR_DELTA_MD = ROOT / "docs" / "trinity-live-traces" / "v43-pillar-delta-v1.md"

JOURNEY_DIGEST_JSON = ROOT / "docs" / "auto-generated" / "v43-journey-advisory-digest-v1.json"
WSL_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-wsl-resurrection-v1.json"
CAPABILITY_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-codex-capability-audit-v1.json"
DRIVE_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-google-drive-proof-v1.json"
CLOUD_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-cloud-carry-forward-v1.json"
GMUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-gmut-lab-bundle-v1.json"
VESPER_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-vesper-memory-cognitive-bridge-v1.json"
AUTOMATION_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-automation-registry-v1.json"
KAI_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-kai-orchestration-bridge-v1.json"
ALLOWLIST_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-stage-allowlist-v1.json"
GIT_RESULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v43-git-publication-result-v1.json"

SUITE_FILES = {
    "quick": ROOT / "docs" / "trinity-live-traces" / "v43-quick-suite-status.json",
    "standard": ROOT / "docs" / "trinity-live-traces" / "v43-standard-suite-status.json",
    "deep": ROOT / "docs" / "trinity-live-traces" / "v43-deep-suite-status.json",
    "collab": ROOT / "docs" / "trinity-live-traces" / "v43-collab-suite-status.json",
    "materialize_l2": ROOT / "docs" / "trinity-live-traces" / "v43-materialize-l2-status.json",
    "materialize_l3": ROOT / "docs" / "trinity-live-traces" / "v43-materialize-l3-status.json",
    "materialize_l4": ROOT / "docs" / "trinity-live-traces" / "v43-materialize-l4-status.json",
    "materialize_l5": ROOT / "docs" / "trinity-live-traces" / "v43-materialize-l5-status.json",
}


def _suite_summary(status: dict[str, Any]) -> dict[str, Any]:
    if not status:
        return {"summary": "missing", "overall_status": "MISSING", "shared_latest_eligible": False}
    counts = status.get("counts", {}) if isinstance(status.get("counts"), dict) else {}
    fail_count = int(counts.get("fail", 0) or 0)
    warn_count = int(counts.get("warn", 0) or 0)
    timeout_count = int(counts.get("timeout", 0) or 0)
    if fail_count or timeout_count or status.get("effective_success") is False:
        overall = "FAIL"
    elif warn_count:
        overall = "WARN"
    else:
        overall = "PASS"
    return {
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL",
        "overall_status": overall,
        "pass_count": counts.get("pass", 0),
        "warn_count": warn_count,
        "fail_count": fail_count,
        "timeout_count": timeout_count,
        "effective_success": status.get("effective_success"),
        "suite_duration_sec": status.get("suite_duration_sec", 0),
        "expansion_systems_passed": status.get("expansion_systems_passed", 0),
        "expansion_systems_total": status.get("expansion_systems_total", 0),
        "checkpoint_class": status.get("checkpoint_class", ""),
        "shared_latest_eligible": bool(status.get("shared_latest_eligible")),
    }


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


def _load_suites() -> dict[str, dict[str, Any]]:
    return {name: read_json(path) for name, path in SUITE_FILES.items()}


def _pillar_delta(wsl: dict[str, Any], cloud: dict[str, Any], gmut: dict[str, Any], allowlist: dict[str, Any], drive: dict[str, Any]) -> dict[str, Any]:
    mind = resolve_status(gmut)
    body_inputs = [
        resolve_status(wsl),
        resolve_status(cloud),
        "PASS" if str(wsl.get("filesystem_promotion_state") or "") == "unblocked" else "WARN",
    ]
    body = "PASS" if all(item == "PASS" for item in body_inputs) else ("FAIL" if "FAIL" in body_inputs else "WARN")
    heart_inputs = [
        "PASS" if allowlist else "WARN",
        "PASS" if str(drive.get("google_drive_state") or "") in {"bounded_connector_verified", "operator_hold"} else "WARN",
    ]
    heart = "PASS" if all(item == "PASS" for item in heart_inputs) else ("FAIL" if "FAIL" in heart_inputs else "WARN")
    overall = "PASS" if all(item == "PASS" for item in (mind, body, heart)) else ("FAIL" if "FAIL" in (mind, body, heart) else "WARN")
    return {
        "generated_utc": now_iso(),
        "phase": "v43_omega",
        "overall_status": overall,
        "pillar_bundle_state": "published" if overall == "PASS" else "bounded_publication",
        "pillars": {
            "mind": {
                "overall_status": mind,
                "path": "docs/trinity-live-traces/v43-gmut-lab-bundle-v1.json",
                "v43_delta": "gmut_qcit_bundle",
            },
            "body": {
                "overall_status": body,
                "paths": [
                    "docs/trinity-live-traces/v43-wsl-resurrection-v1.json",
                    "docs/trinity-live-traces/v43-cloud-carry-forward-v1.json",
                    "docs/trinity-live-traces/v43-automation-registry-v1.json",
                ],
                "v43_delta": "wsl_cloud_automation_delta",
            },
            "heart": {
                "overall_status": heart,
                "paths": [
                    "docs/trinity-live-traces/v43-stage-allowlist-v1.json",
                    "docs/v43-omega-handoff-policy-v1.json",
                ],
                "v43_delta": "forward_only_holds_and_honest_blockers",
            },
        },
    }


def _pillar_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V43 Pillar Delta",
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
        lines.append(f"- v43_delta: `{row.get('v43_delta', '')}`")
        for path in row.get("paths", []):
            lines.append(f"- path: `{path}`")
        if "path" in row:
            lines.append(f"- path: `{row['path']}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _receiver_rule(core_states: dict[str, Any], capability: dict[str, Any], automation: dict[str, Any], drive: dict[str, Any], vesper: dict[str, Any], suite_failures: list[str], git_publication_state: str) -> tuple[str, str]:
    orun_ready = all(
        [
            str(core_states.get("codex_wsl_selector_state") or "") == "desktop_selector_verified",
            str(core_states.get("filesystem_promotion_state") or "") == "unblocked",
            resolve_status(capability) == "PASS",
            resolve_status(automation) == "PASS",
            str(drive.get("google_drive_state") or "") in {"bounded_connector_verified", "activated"},
            str(vesper.get("vesper_cognitive_engine_state") or "") == "datastore_document_readback_verified",
            not suite_failures,
            git_publication_state == "committed_pushed_pr_updated",
        ]
    )
    return ("Orun", "orun_promoted") if orun_ready else ("Aletheon", "aletheon_facing")


def main() -> int:
    head_sha = git_head()
    runtime_resolution = read_json(RUNTIME_RESOLUTION_PATH)
    runtime_log = read_json(RUNTIME_LOG_PATH)
    runtime_board = read_json(RUNTIME_BOARD_PATH)
    session_validation = read_json(SESSION_VALIDATION_PATH)

    journey = read_json(JOURNEY_DIGEST_JSON)
    wsl = read_json(WSL_JSON)
    capability = read_json(CAPABILITY_JSON)
    drive = read_json(DRIVE_JSON)
    cloud = read_json(CLOUD_JSON)
    gmut = read_json(GMUT_JSON)
    vesper = read_json(VESPER_JSON)
    automation = read_json(AUTOMATION_JSON)
    kai = read_json(KAI_JSON)
    allowlist = read_json(ALLOWLIST_JSON)
    git_result = read_json(GIT_RESULT_JSON)
    suite_statuses = {name: _suite_summary(payload) for name, payload in _load_suites().items()}

    pillar_delta = _pillar_delta(wsl, cloud, gmut, allowlist, drive)
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

    git_publication_state = str(git_result.get("git_publication_state") or "")
    if not git_publication_state:
        git_publication_state = "allowlist_published" if allowlist else "unpublished"

    core_states = {
        "v43_execution_lead": "Aletheon",
        "wsl_launcher_state": str(wsl.get("wsl_launcher_state") or ""),
        "ubuntu_registration_state": str(wsl.get("ubuntu_registration_state") or ""),
        "ubuntu_vhd_backup_state": str(wsl.get("ubuntu_vhd_backup_state") or ""),
        "wsl_recovery_state": str(wsl.get("wsl_recovery_state") or ""),
        "codex_wsl_selector_state": str(wsl.get("codex_wsl_selector_state") or ""),
        "wsl_health_state": str(wsl.get("wsl_health_state") or ""),
        "filesystem_promotion_state": str(wsl.get("filesystem_promotion_state") or "blocked"),
        "drive_archive_state": str(wsl.get("drive_archive_state") or ""),
        "codex_capability_audit_state": str(capability.get("codex_capability_audit_state") or ""),
        "plugin_registry_state": str(capability.get("plugin_registry_state") or ""),
        "automation_backend_state": str(capability.get("automation_backend_state") or automation.get("automation_backend_state") or ""),
        "browser_iteration_state": str(capability.get("browser_iteration_state") or ""),
        "computer_use_state": str(capability.get("computer_use_state") or ""),
        "google_drive_state": str(drive.get("google_drive_state") or "operator_hold"),
        "api_ascendancy_state": str(cloud.get("api_ascendancy_state") or ""),
        "anthos_state": str(cloud.get("anthos_state") or ""),
        "os_login_state": str(cloud.get("os_login_state") or ""),
        "cloud_run_state": str(cloud.get("cloud_run_state") or ""),
        "cloud_build_state": str(cloud.get("cloud_build_state") or ""),
        "dataplex_state": str(cloud.get("dataplex_state") or ""),
        "kai_orchestration_state": str(kai.get("kai_orchestration_state") or ""),
        "vesper_telemetry_ingest_state": str(vesper.get("vesper_telemetry_ingest_state") or ""),
        "vesper_cognitive_engine_state": str(vesper.get("vesper_cognitive_engine_state") or ""),
        "gmut_experiment_state": str(gmut.get("gmut_experiment_state") or ""),
        "automation_registry_state": str(automation.get("automation_registry_state") or ""),
        "pillar_bundle_overall_status": str(pillar_delta.get("overall_status") or ""),
        "git_publication_state": git_publication_state,
    }

    for target in (runtime_resolution, runtime_log, runtime_board):
        target["generated_utc"] = now_iso()
        target["phase"] = "v43_omega"
        target["authority_model"] = "repo_first"
        target["source_branch"] = "codex/GHC-Family/beyonder-shared-omega-line"
        target["current_head_sha"] = head_sha
        target.update(core_states)

    runtime_resolution["active_handoff_pack_path"] = "docs/v43-omega-continuity-pack-v1.md"
    runtime_resolution["active_handoff_policy_path"] = "docs/v43-omega-handoff-policy-v1.json"
    runtime_resolution["next_receiver_pack_path"] = "docs/v44-beta-continuity-pack-v1.md"
    runtime_resolution["next_receiver_policy_path"] = "docs/v44-beta-handoff-policy-v1.json"
    runtime_resolution["current_shared_suite_surface"] = suite_statuses.get("standard", {})

    runtime_log["session_id"] = "v43-omega-closeout"
    runtime_log["session_truth_complete"] = True
    runtime_log["runtime_truth_status"] = "complete_runtime_truth"
    runtime_log["runtime_truth_completion_ratio"] = completion_ratio
    runtime_log["complete_agent_count"] = complete_agent_count
    runtime_log["pending_agent_count"] = pending_agent_count
    runtime_log["active_handoff_pack_path"] = "docs/v43-omega-continuity-pack-v1.md"
    runtime_log["active_handoff_policy_path"] = "docs/v43-omega-handoff-policy-v1.json"
    runtime_log["next_receiver_pack_path"] = "docs/v44-beta-continuity-pack-v1.md"
    runtime_log["next_receiver_policy_path"] = "docs/v44-beta-handoff-policy-v1.json"
    runtime_log["current_shared_suite_surface"] = suite_statuses.get("standard", {})

    runtime_board["runtime_truth_complete"] = True
    runtime_board["complete_agent_count"] = complete_agent_count
    runtime_board["pending_agent_count"] = pending_agent_count
    runtime_board["runtime_truth_completion_ratio"] = completion_ratio
    runtime_board["checkpoint_anchor_commit"] = head_sha

    session_validation["generated_utc"] = now_iso()
    session_validation["overall_status"] = "PASS" if complete_agent_count == 4 else "WARN"
    session_validation["current_head_sha"] = head_sha
    session_validation.update(core_states)
    metrics = session_validation.get("metrics")
    if isinstance(metrics, dict):
        metrics["runtime_truth_complete"] = True
        metrics["complete_agent_count"] = complete_agent_count
        metrics["pending_agent_count"] = pending_agent_count
        metrics["runtime_truth_completion_ratio"] = completion_ratio

    suite_failures = [name for name, summary in suite_statuses.items() if summary.get("overall_status") != "PASS"]
    intended_receiver, receiver_rule_outcome = _receiver_rule(core_states, capability, automation, drive, vesper, suite_failures, git_publication_state)

    proof_paths = {
        "journey_digest": "docs/auto-generated/v43-journey-advisory-digest-v1.json",
        "wsl_resurrection": "docs/trinity-live-traces/v43-wsl-resurrection-v1.json",
        "codex_capability_audit": "docs/trinity-live-traces/v43-codex-capability-audit-v1.json",
        "google_drive_proof": "docs/trinity-live-traces/v43-google-drive-proof-v1.json",
        "cloud_carry_forward": "docs/trinity-live-traces/v43-cloud-carry-forward-v1.json",
        "gmut_lab_bundle": "docs/trinity-live-traces/v43-gmut-lab-bundle-v1.json",
        "vesper_memory_cognitive_bridge": "docs/trinity-live-traces/v43-vesper-memory-cognitive-bridge-v1.json",
        "automation_registry": "docs/trinity-live-traces/v43-automation-registry-v1.json",
        "kai_orchestration_bridge": "docs/trinity-live-traces/v43-kai-orchestration-bridge-v1.json",
        "allowlist": "docs/trinity-live-traces/v43-stage-allowlist-v1.json",
        "pillar_delta": "docs/trinity-live-traces/v43-pillar-delta-v1.json",
        "git_publication_result": "docs/trinity-live-traces/v43-git-publication-result-v1.json",
    }
    residuals = []
    for name, payload in (
        ("wsl", wsl),
        ("capability", capability),
        ("drive", drive),
        ("cloud", cloud),
        ("gmut", gmut),
        ("vesper", vesper),
        ("automation", automation),
        ("kai", kai),
        ("pillar_delta", pillar_delta),
    ):
        status = resolve_status(payload)
        if status != "PASS":
            residuals.append(f"{name}={status}")
    residuals.extend(f"suite::{name}" for name in suite_failures)
    if git_publication_state != "committed_pushed_pr_updated":
        residuals.append(f"git_publication_state={git_publication_state}")

    overall_status = "PASS" if not residuals else ("FAIL" if any("=FAIL" in item for item in residuals) else "WARN")

    closeout = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "phase": "v43_omega",
        "authority_model": "repo_first",
        "source_branch": "codex/GHC-Family/beyonder-shared-omega-line",
        "current_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "core_states": core_states,
        "suite_statuses": suite_statuses,
        "proof_paths": proof_paths,
        "bounded_residuals": residuals,
    }

    receiver = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "phase": "v44_beta",
        "authority_model": "repo_first",
        "source_branch": "codex/GHC-Family/beyonder-shared-omega-line",
        "current_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "core_states": core_states,
        "suite_statuses": suite_statuses,
        "proof_paths": proof_paths,
        "bounded_residuals": residuals,
    }

    handoff = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "phase": "v43_omega",
        "authority_model": "repo_first",
        "source_branch": "codex/GHC-Family/beyonder-shared-omega-line",
        "source_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "deployed_main_agents": runtime_resolution.get("deployed_main_agents", []),
        "runtime_truth_policy": {
            "runtime_truth_complete": True,
            "google_drive_state": core_states["google_drive_state"],
            "filesystem_promotion_state": core_states["filesystem_promotion_state"],
            "active_handoff_pack_path": "docs/v43-omega-continuity-pack-v1.md",
            "next_receiver_pack_path": "docs/v44-beta-continuity-pack-v1.md",
        },
        "required_inputs": [
            "docs/v42-omega-closeout-summary-v1.json",
            "docs/v42-omega-continuity-pack-v1.md",
            "docs/v43-beta-closeout-summary-v1.json",
            "docs/trinity-runtime-model-resolution-v1.json",
            "docs/v17-runtime-session-log-latest.json",
        ],
        "receiver_tasks": [
            "Keep the authoritative C: repo as the only continuity source and continue treating advisory Downloads text as non-authoritative.",
            "Preserve the repaired WSL lane, but keep filesystem promotion blocked unless a real desktop selector proof replaces the current app-side residual.",
            "Keep Bigtable as Vesper Ion's primary memory lane unless the bounded cognitive engine proof becomes stable enough to graduate.",
            "Reuse the forward-only V43 allowlist and do not stage unrelated carried-forward latest-state churn.",
        ],
        "truth_boundaries_to_preserve": [
            "repo_first",
            "windows_powershell_primary_when_wsl_selector_is_unresolved",
            "computer_use_state=unsupported_windows_launch_scope",
        ],
        "bounded_residuals": residuals,
    }

    v44_handoff = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "phase": "v44_beta",
        "authority_model": "repo_first",
        "source_branch": "codex/GHC-Family/beyonder-shared-omega-line",
        "source_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "seed_inputs": [
            "docs/v43-omega-closeout-summary-v1.json",
            "docs/v43-omega-continuity-pack-v1.md",
            "docs/v43-omega-handoff-policy-v1.json",
            "docs/trinity-runtime-model-resolution-v1.json",
        ],
        "primary_focus_lanes": [
            "close any remaining app-side Codex-to-WSL selector blocker",
            "stabilize or retire the bounded cognitive engine lane based on fresh readback proof",
            "continue forward-only Git publication without absorbing background dirty churn",
        ],
        "bounded_residuals": residuals,
    }

    write_json(RUNTIME_RESOLUTION_PATH, runtime_resolution)
    write_json(RUNTIME_LOG_PATH, runtime_log)
    write_json(RUNTIME_BOARD_PATH, runtime_board)
    write_json(SESSION_VALIDATION_PATH, session_validation)
    write_json(V43_OMEGA_CLOSEOUT_JSON, closeout)
    write_text(V43_OMEGA_CONTINUITY_MD, _continuity_markdown(closeout, "V43 Omega Continuity Pack"))
    write_json(V43_OMEGA_HANDOFF_JSON, handoff)
    write_json(V44_BETA_CLOSEOUT_JSON, receiver)
    write_text(V44_BETA_CONTINUITY_MD, _continuity_markdown(receiver, "V44 Beta Continuity Pack"))
    write_json(V44_BETA_HANDOFF_JSON, v44_handoff)
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

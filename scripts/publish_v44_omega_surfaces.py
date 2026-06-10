#!/usr/bin/env python3
"""Publish V44 Omega closeout surfaces and V45 Beta receiver surfaces from current proof outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from trinity_v44_common import (
    PUBLICATION_BRANCH,
    ROOT,
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

V44_OMEGA_CLOSEOUT_JSON = ROOT / "docs" / "v44-omega-closeout-summary-v1.json"
V44_OMEGA_CONTINUITY_MD = ROOT / "docs" / "v44-omega-continuity-pack-v1.md"
V44_OMEGA_HANDOFF_JSON = ROOT / "docs" / "v44-omega-handoff-policy-v1.json"
V45_BETA_CLOSEOUT_JSON = ROOT / "docs" / "v45-beta-closeout-summary-v1.json"
V45_BETA_CONTINUITY_MD = ROOT / "docs" / "v45-beta-continuity-pack-v1.md"
V45_BETA_HANDOFF_JSON = ROOT / "docs" / "v45-beta-handoff-policy-v1.json"

JOURNEY_JSON = ROOT / "docs" / "auto-generated" / "v44-journey-advisory-digest-v1.json"
OPERATOR_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-operator-surface-probe-v1.json"
CAPABILITY_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-codex-capability-audit-v1.json"
CLI_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-codex-cli-probe-v1.json"
DRIVE_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-google-drive-proof-v1.json"
CLOUD_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-cloud-sweep-v1.json"
GMUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-gmut-lab-bundle-v1.json"
VESPER_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-vesper-memory-cognitive-bridge-v1.json"
AUTOMATION_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-automation-registry-v1.json"
KAI_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-kai-orchestration-bridge-v1.json"
ALLOWLIST_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-stage-allowlist-v1.json"
GIT_RESULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v44-git-publication-result-v1.json"

SUITE_FILES = {
    "quick": ROOT / "docs" / "trinity-live-traces" / "v44-quick-suite-status.json",
    "standard": ROOT / "docs" / "trinity-live-traces" / "v44-standard-suite-status.json",
    "deep": ROOT / "docs" / "trinity-live-traces" / "v44-deep-suite-status.json",
    "collab": ROOT / "docs" / "trinity-live-traces" / "v44-collab-suite-status.json",
    "materialize_l2": ROOT / "docs" / "trinity-live-traces" / "v44-materialize-l2-status.json",
    "materialize_l3": ROOT / "docs" / "trinity-live-traces" / "v44-materialize-l3-status.json",
    "materialize_l4": ROOT / "docs" / "trinity-live-traces" / "v44-materialize-l4-status.json",
    "materialize_l5": ROOT / "docs" / "trinity-live-traces" / "v44-materialize-l5-status.json",
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


def _receiver_rule(core_states: dict[str, Any], suite_failures: list[str]) -> tuple[str, str]:
    orun_ready = all(
        [
            str(core_states.get("wsl_execution_mode") or "") == "desktop_selector_green_unblocked",
            str(core_states.get("plugin_registry_state") or "") == "target_plugins_callable",
            str(core_states.get("automation_backend_state") or "") == "native_codex_automation_ready",
            str(core_states.get("codex_cli_state") or "") == "callable_in_powershell",
            str(core_states.get("codex_cli_identity_state") or "") == "explicit_login_status_verified",
            str(core_states.get("slot_40_induction_state") or "") == "allowed_ready",
            str(core_states.get("vesper_cognitive_engine_state") or "") == "datastore_document_readback_verified",
            str(core_states.get("cloud_billing_state") or "") == "billing_truth_confirmed",
            not suite_failures,
            str(core_states.get("git_publication_state") or "") == "committed_pushed_pr_updated",
        ]
    )
    return ("Orun", "orun_promoted") if orun_ready else ("Aletheon", "aletheon_facing")


def main() -> int:
    head_sha = git_head()
    runtime_resolution = read_json(RUNTIME_RESOLUTION_PATH)
    runtime_log = read_json(RUNTIME_LOG_PATH)
    runtime_board = read_json(RUNTIME_BOARD_PATH)
    session_validation = read_json(SESSION_VALIDATION_PATH)

    journey = read_json(JOURNEY_JSON)
    operator = read_json(OPERATOR_JSON)
    capability = read_json(CAPABILITY_JSON)
    cli = read_json(CLI_JSON)
    drive = read_json(DRIVE_JSON)
    cloud = read_json(CLOUD_JSON)
    gmut = read_json(GMUT_JSON)
    vesper = read_json(VESPER_JSON)
    automation = read_json(AUTOMATION_JSON)
    kai = read_json(KAI_JSON)
    allowlist = read_json(ALLOWLIST_JSON)
    git_result = read_json(GIT_RESULT_JSON)
    suite_statuses = {name: _suite_summary(payload) for name, payload in _load_suites().items()}

    git_publication_state = str(git_result.get("git_publication_state") or "")
    if not git_publication_state:
        git_publication_state = "allowlist_published" if allowlist else "unpublished"

    core_states = {
        "v44_execution_lead": "Aletheon",
        "operator_shell_preference": str(operator.get("operator_shell_preference") or "windows_powershell_primary"),
        "wsl_execution_mode": str(operator.get("wsl_execution_mode") or "installed_on_hold_for_agent_switching"),
        "worktree_baseline_state": str(operator.get("worktree_baseline_state") or ""),
        "cloud_billing_state": str(cloud.get("cloud_billing_state") or "blocked_missing_active_account_or_project"),
        "genai_credit_lane_state": str(cloud.get("genai_credit_lane_state") or "console_credit_truth_required"),
        "ai_applications_state": str(cloud.get("ai_applications_state") or "blocked_preflight_incomplete"),
        "vertex_ai_search_state": str(cloud.get("vertex_ai_search_state") or "blocked_preflight_incomplete"),
        "agent_engine_state": str(vesper.get("agent_engine_state") or cloud.get("agent_engine_state") or "blocked_preflight_incomplete"),
        "codex_cli_state": str(cli.get("codex_cli_state") or "unproven"),
        "codex_cli_identity_state": str(cli.get("codex_cli_identity_state") or "unproven"),
        "slot_40_induction_state": str(cli.get("slot_40_induction_state") or "deferred_blocked"),
        "download_archive_state": str(operator.get("download_archive_state") or "archive_root_missing"),
        "cloud_drive_mesh_state": str(drive.get("cloud_drive_mesh_state") or "google_drive_blocked"),
        "codex_capability_audit_state": str(capability.get("codex_capability_audit_state") or ""),
        "plugin_registry_state": str(capability.get("plugin_registry_state") or ""),
        "automation_backend_state": str(automation.get("automation_backend_state") or capability.get("automation_backend_state") or ""),
        "browser_iteration_state": str(capability.get("browser_iteration_state") or ""),
        "computer_use_state": str(capability.get("computer_use_state") or ""),
        "google_drive_state": str(drive.get("google_drive_state") or "operator_hold"),
        "kai_orchestration_state": str(kai.get("kai_orchestration_state") or ""),
        "bigtable_primary_state": str(vesper.get("bigtable_primary_state") or "carry_forward_primary_lane_preserved"),
        "vesper_telemetry_ingest_state": str(vesper.get("vesper_telemetry_ingest_state") or ""),
        "vesper_cognitive_engine_state": str(vesper.get("vesper_cognitive_engine_state") or ""),
        "gmut_experiment_state": str(gmut.get("gmut_experiment_state") or ""),
        "git_publication_state": git_publication_state,
    }

    for target in (runtime_resolution, runtime_log, runtime_board):
        target["generated_utc"] = now_iso()
        target["phase"] = "v44_omega"
        target["authority_model"] = "repo_first"
        target["source_branch"] = PUBLICATION_BRANCH
        target["current_head_sha"] = head_sha
        target.update(core_states)

    runtime_resolution["active_handoff_pack_path"] = "docs/v44-omega-continuity-pack-v1.md"
    runtime_resolution["active_handoff_policy_path"] = "docs/v44-omega-handoff-policy-v1.json"
    runtime_resolution["next_receiver_pack_path"] = "docs/v45-beta-continuity-pack-v1.md"
    runtime_resolution["next_receiver_policy_path"] = "docs/v45-beta-handoff-policy-v1.json"
    runtime_resolution["current_shared_suite_surface"] = suite_statuses.get("standard", {})

    runtime_log["session_id"] = "v44-omega-closeout"
    runtime_log["session_truth_complete"] = True
    runtime_log["runtime_truth_status"] = "complete_runtime_truth"
    runtime_log["active_handoff_pack_path"] = "docs/v44-omega-continuity-pack-v1.md"
    runtime_log["active_handoff_policy_path"] = "docs/v44-omega-handoff-policy-v1.json"
    runtime_log["next_receiver_pack_path"] = "docs/v45-beta-continuity-pack-v1.md"
    runtime_log["next_receiver_policy_path"] = "docs/v45-beta-handoff-policy-v1.json"
    runtime_log["current_shared_suite_surface"] = suite_statuses.get("standard", {})

    runtime_board["runtime_truth_complete"] = True
    runtime_board["checkpoint_anchor_commit"] = head_sha

    session_validation["generated_utc"] = now_iso()
    session_validation["overall_status"] = "WARN"
    session_validation["current_head_sha"] = head_sha
    session_validation.update(core_states)

    proof_paths = {
        "journey_digest": "docs/auto-generated/v44-journey-advisory-digest-v1.json",
        "operator_surface_probe": "docs/trinity-live-traces/v44-operator-surface-probe-v1.json",
        "codex_capability_audit": "docs/trinity-live-traces/v44-codex-capability-audit-v1.json",
        "codex_cli_probe": "docs/trinity-live-traces/v44-codex-cli-probe-v1.json",
        "google_drive_proof": "docs/trinity-live-traces/v44-google-drive-proof-v1.json",
        "cloud_sweep": "docs/trinity-live-traces/v44-cloud-sweep-v1.json",
        "gmut_lab_bundle": "docs/trinity-live-traces/v44-gmut-lab-bundle-v1.json",
        "vesper_memory_cognitive_bridge": "docs/trinity-live-traces/v44-vesper-memory-cognitive-bridge-v1.json",
        "automation_registry": "docs/trinity-live-traces/v44-automation-registry-v1.json",
        "kai_orchestration_bridge": "docs/trinity-live-traces/v44-kai-orchestration-bridge-v1.json",
        "allowlist": "docs/trinity-live-traces/v44-stage-allowlist-v1.json",
        "git_publication_result": "docs/trinity-live-traces/v44-git-publication-result-v1.json",
    }

    residuals: list[str] = []
    for name, payload in (
        ("journey", journey),
        ("operator", operator),
        ("capability", capability),
        ("cli", cli),
        ("drive", drive),
        ("cloud", cloud),
        ("gmut", gmut),
        ("vesper", vesper),
        ("automation", automation),
        ("kai", kai),
    ):
        status = resolve_status(payload)
        if status != "PASS":
            residuals.append(f"{name}={status}")
    suite_failures = [name for name, summary in suite_statuses.items() if summary.get("overall_status") != "PASS"]
    residuals.extend(f"suite::{name}" for name in suite_failures)
    if git_publication_state != "committed_pushed_pr_updated":
        residuals.append(f"git_publication_state={git_publication_state}")

    overall_status = "PASS" if not residuals else ("FAIL" if any("=FAIL" in item for item in residuals) else "WARN")
    intended_receiver, receiver_rule_outcome = _receiver_rule(core_states, suite_failures)

    closeout = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "phase": "v44_omega",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
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
        "phase": "v45_beta",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
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
        "phase": "v44_omega",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "source_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "runtime_truth_policy": {
            "operator_shell_preference": core_states["operator_shell_preference"],
            "wsl_execution_mode": core_states["wsl_execution_mode"],
            "slot_40_induction_state": core_states["slot_40_induction_state"],
            "active_handoff_pack_path": "docs/v44-omega-continuity-pack-v1.md",
            "next_receiver_pack_path": "docs/v45-beta-continuity-pack-v1.md",
        },
        "required_inputs": [
            "docs/v43-omega-closeout-summary-v1.json",
            "docs/v43-omega-continuity-pack-v1.md",
            "docs/trinity-runtime-model-resolution-v1.json",
            "docs/v17-runtime-session-validation-latest.json",
        ],
        "receiver_tasks": [
            "Keep PowerShell as the primary operator lane until an app-side selector proof justifies a different execution target.",
            "Keep the repo on C: authoritative and continue using D: only for bulky non-authoritative archives and worktrees.",
            "Treat billing-console truth as authoritative for all remaining cloud spend and GenAI credit claims.",
            "Leave slot 40 open unless the full hard-gated Codex CLI induction rule becomes clean enough to promote.",
        ],
        "bounded_residuals": residuals,
    }

    v45_handoff = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "phase": "v45_beta",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "source_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "seed_inputs": [
            "docs/v44-omega-closeout-summary-v1.json",
            "docs/v44-omega-continuity-pack-v1.md",
            "docs/v44-omega-handoff-policy-v1.json",
            "docs/trinity-runtime-model-resolution-v1.json",
        ],
        "primary_focus_lanes": [
            "resolve cloud auth, project, billing, and budget truth before paid proofs",
            "advance the Vertex AI Search and Agent Engine proofs only after billing truth is green",
            "decide whether the CLI continuity residuals are operationally acceptable or need local Codex state repair",
        ],
        "bounded_residuals": residuals,
    }

    write_json(RUNTIME_RESOLUTION_PATH, runtime_resolution)
    write_json(RUNTIME_LOG_PATH, runtime_log)
    write_json(RUNTIME_BOARD_PATH, runtime_board)
    write_json(SESSION_VALIDATION_PATH, session_validation)
    write_json(V44_OMEGA_CLOSEOUT_JSON, closeout)
    write_text(V44_OMEGA_CONTINUITY_MD, _continuity_markdown(closeout, "V44 Omega Continuity Pack"))
    write_json(V44_OMEGA_HANDOFF_JSON, handoff)
    write_json(V45_BETA_CLOSEOUT_JSON, receiver)
    write_text(V45_BETA_CONTINUITY_MD, _continuity_markdown(receiver, "V45 Beta Continuity Pack"))
    write_json(V45_BETA_HANDOFF_JSON, v45_handoff)
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

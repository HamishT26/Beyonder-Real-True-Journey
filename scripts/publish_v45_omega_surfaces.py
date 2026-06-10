#!/usr/bin/env python3
"""Publish V45 Omega closeout surfaces and V46 Beta receiver surfaces from current proof outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from trinity_v45_common import (
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

V45_OMEGA_CLOSEOUT_JSON = ROOT / "docs" / "v45-omega-closeout-summary-v1.json"
V45_OMEGA_CONTINUITY_MD = ROOT / "docs" / "v45-omega-continuity-pack-v1.md"
V45_OMEGA_HANDOFF_JSON = ROOT / "docs" / "v45-omega-handoff-policy-v1.json"
V46_BETA_CLOSEOUT_JSON = ROOT / "docs" / "v46-beta-closeout-summary-v1.json"
V46_BETA_CONTINUITY_MD = ROOT / "docs" / "v46-beta-continuity-pack-v1.md"
V46_BETA_HANDOFF_JSON = ROOT / "docs" / "v46-beta-handoff-policy-v1.json"

JOURNEY_JSON = ROOT / "docs" / "auto-generated" / "v45-journey-advisory-digest-v1.json"
OPERATOR_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-operator-surface-probe-v1.json"
CODEX_HOME_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-codex-home-repair-v1.json"
CLI_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-codex-cli-slot40-probe-v1.json"
CLOUD_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-cloud-research-digest-v1.json"
ALLOWLIST_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-stage-allowlist-v1.json"
GIT_RESULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-git-publication-result-v1.json"
OPERATOR_NOTE = ROOT / "docs" / "v45-powershell-operator-note-v1.md"

SUITE_FILES = {
    "quick": ROOT / "docs" / "trinity-live-traces" / "v45-quick-suite-status.json",
    "standard": ROOT / "docs" / "trinity-live-traces" / "v45-standard-suite-status.json",
    "deep": ROOT / "docs" / "trinity-live-traces" / "v45-deep-suite-status.json",
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
    current_head = closeout.get("current_head_sha") or closeout.get("source_head_sha") or ""
    lines = [
        f"# {title}",
        "",
        f"- Generated UTC: `{closeout['generated_utc']}`",
        f"- Current head: `{current_head}`",
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
            str(core_states.get("powershell_hygiene_state") or "") == "powershell_ready",
            str(core_states.get("local_codex_hygiene_state") or "") in {"skill_bom_frontmatter_repaired", "no_skill_bom_frontmatter_issue_detected"},
            str(core_states.get("codex_cli_auth_state") or "") in {"stable_login_verified", "callable_with_refresh_residuals"},
            str(core_states.get("slot_40_induction_state") or "") in {"allowed_ready", "deferred_blocked"},
            str(core_states.get("plugin_surface_split_state") or "") == "explicit_app_cli_split_recorded",
            str(core_states.get("git_publication_state") or "") == "committed_pushed_pr_updated",
            not suite_failures,
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
    codex_home = read_json(CODEX_HOME_JSON)
    cli = read_json(CLI_JSON)
    cloud = read_json(CLOUD_JSON)
    allowlist = read_json(ALLOWLIST_JSON)
    git_result = read_json(GIT_RESULT_JSON)
    suite_statuses = {name: _suite_summary(payload) for name, payload in _load_suites().items()}

    git_publication_state = str(git_result.get("git_publication_state") or "")
    if not git_publication_state:
        git_publication_state = "allowlist_published" if allowlist else "unpublished"

    core_states = {
        "v45_execution_lead": "Aletheon",
        "worktree_baseline_state": str(operator.get("worktree_baseline_state") or ""),
        "operator_shell_preference": str(operator.get("operator_shell_preference") or "windows_powershell_primary"),
        "powershell_hygiene_state": str(operator.get("powershell_hygiene_state") or "powershell_probe_failed"),
        "wsl_execution_mode": str(operator.get("wsl_execution_mode") or "installed_on_hold_for_agent_switching"),
        "cloud_activation_mode": str(cloud.get("cloud_activation_mode") or "research_only_until_billing_truth"),
        "gcloud_auth_state": str(cloud.get("gcloud_auth_state") or "no_active_account"),
        "gcloud_project_state": str(cloud.get("gcloud_project_state") or "no_active_project"),
        "billing_console_credit_state": str(cloud.get("billing_console_credit_state") or "console_confirmation_required"),
        "credit_claim_state": str(cloud.get("credit_claim_state") or "operator_claim_unverified"),
        "vertex_ai_credit_research_state": str(cloud.get("vertex_ai_credit_research_state") or "bounded_research_ready"),
        "kai_activation_state": str(cloud.get("kai_activation_state") or "standby_waiting_for_billing_truth"),
        "vesper_activation_state": str(cloud.get("vesper_activation_state") or "standby_waiting_for_billing_truth"),
        "codex_cli_state": str(cli.get("codex_cli_state") or "unproven"),
        "codex_cli_auth_state": str(cli.get("codex_cli_auth_state") or "login_status_unverified"),
        "codex_cli_model_proof_state": str(cli.get("codex_cli_model_proof_state") or "unverifiable_from_surface"),
        "slot_40_probe_state": str(cli.get("slot_40_probe_state") or "candidate_probe_not_attempted"),
        "slot_40_induction_state": str(cli.get("slot_40_induction_state") or "deferred_blocked"),
        "local_codex_hygiene_state": str(codex_home.get("local_codex_hygiene_state") or "not_run"),
        "drive_download_policy_state": str(operator.get("drive_download_policy_state") or "v45_d_targets_missing"),
        "plugin_surface_split_state": str(operator.get("plugin_surface_split_state") or "unproven"),
        "git_publication_state": git_publication_state,
    }

    for target in (runtime_resolution, runtime_log, runtime_board):
        target["generated_utc"] = now_iso()
        target["phase"] = "v45_omega"
        target["authority_model"] = "repo_first"
        target["source_branch"] = PUBLICATION_BRANCH
        target["current_head_sha"] = head_sha
        target.update(core_states)

    runtime_resolution["active_handoff_pack_path"] = "docs/v45-omega-continuity-pack-v1.md"
    runtime_resolution["active_handoff_policy_path"] = "docs/v45-omega-handoff-policy-v1.json"
    runtime_resolution["next_receiver_pack_path"] = "docs/v46-beta-continuity-pack-v1.md"
    runtime_resolution["next_receiver_policy_path"] = "docs/v46-beta-handoff-policy-v1.json"
    runtime_resolution["current_shared_suite_surface"] = suite_statuses.get("standard", {})

    runtime_log["session_id"] = "v45-omega-closeout"
    runtime_log["session_truth_complete"] = True
    runtime_log["runtime_truth_status"] = "complete_runtime_truth"
    runtime_log["active_handoff_pack_path"] = "docs/v45-omega-continuity-pack-v1.md"
    runtime_log["active_handoff_policy_path"] = "docs/v45-omega-handoff-policy-v1.json"
    runtime_log["next_receiver_pack_path"] = "docs/v46-beta-continuity-pack-v1.md"
    runtime_log["next_receiver_policy_path"] = "docs/v46-beta-handoff-policy-v1.json"
    runtime_log["current_shared_suite_surface"] = suite_statuses.get("standard", {})

    runtime_board["runtime_truth_complete"] = True
    runtime_board["checkpoint_anchor_commit"] = head_sha

    session_validation["generated_utc"] = now_iso()
    session_validation["overall_status"] = "WARN"
    session_validation["current_head_sha"] = head_sha
    session_validation.update(core_states)

    proof_paths = {
        "journey_digest": "docs/auto-generated/v45-journey-advisory-digest-v1.json",
        "operator_surface_probe": "docs/trinity-live-traces/v45-operator-surface-probe-v1.json",
        "codex_home_repair": "docs/trinity-live-traces/v45-codex-home-repair-v1.json",
        "codex_cli_slot40_probe": "docs/trinity-live-traces/v45-codex-cli-slot40-probe-v1.json",
        "cloud_research_digest": "docs/trinity-live-traces/v45-cloud-research-digest-v1.json",
        "stage_allowlist": "docs/trinity-live-traces/v45-stage-allowlist-v1.json",
        "git_publication_result": "docs/trinity-live-traces/v45-git-publication-result-v1.json",
        "operator_note": "docs/v45-powershell-operator-note-v1.md",
    }

    residuals: list[str] = []
    for name, payload in (
        ("journey", journey),
        ("operator", operator),
        ("codex_home", codex_home),
        ("cli", cli),
        ("cloud", cloud),
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
        "phase": "v45_omega",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "source_head_sha": head_sha,
        "current_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "summary": {
            "cloud_activation_mode": core_states["cloud_activation_mode"],
            "slot_40_probe_state": core_states["slot_40_probe_state"],
            "slot_40_induction_state": core_states["slot_40_induction_state"],
            "codex_cli_auth_state": core_states["codex_cli_auth_state"],
            "codex_cli_model_proof_state": core_states["codex_cli_model_proof_state"],
        },
        "core_states": core_states,
        "proof_paths": proof_paths,
        "suite_statuses": suite_statuses,
        "bounded_residuals": residuals,
        "operator_note_path": "docs/v45-powershell-operator-note-v1.md",
    }

    handoff = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "phase": "v46_beta",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "source_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "required_inputs": [
            "docs/v45-omega-closeout-summary-v1.json",
            "docs/v45-omega-continuity-pack-v1.md",
            "docs/v45-omega-handoff-policy-v1.json",
            "docs/trinity-runtime-model-resolution-v1.json",
            "docs/v17-runtime-session-validation-latest.json",
        ],
        "primary_focus_lanes": [
            "clear the billing and project truth gate before any paid cloud proof",
            "decide whether the slot 40 model-proof residual is operationally acceptable or needs a different proof method",
            "continue PowerShell-first publication and D-drive hygiene without touching the dirty C: checkout",
        ],
        "bounded_residuals": residuals,
    }

    write_json(RUNTIME_RESOLUTION_PATH, runtime_resolution)
    write_json(RUNTIME_LOG_PATH, runtime_log)
    write_json(RUNTIME_BOARD_PATH, runtime_board)
    write_json(SESSION_VALIDATION_PATH, session_validation)
    write_json(V45_OMEGA_CLOSEOUT_JSON, closeout)
    write_text(V45_OMEGA_CONTINUITY_MD, _continuity_markdown(closeout, "V45 Omega Continuity Pack"))
    write_json(V45_OMEGA_HANDOFF_JSON, closeout)
    write_json(V46_BETA_CLOSEOUT_JSON, handoff)
    write_text(V46_BETA_CONTINUITY_MD, _continuity_markdown(handoff, "V46 Beta Continuity Pack"))
    write_json(V46_BETA_HANDOFF_JSON, handoff)
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

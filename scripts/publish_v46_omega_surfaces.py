#!/usr/bin/env python3
"""Publish V46 Omega closeout and V47 Beta receiver surfaces."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from trinity_v46_common import PUBLICATION_BRANCH, ROOT, git_head, now_iso, read_json, write_json, write_text

RUNTIME_RESOLUTION_PATH = ROOT / "docs" / "trinity-runtime-model-resolution-v1.json"
RUNTIME_LOG_PATH = ROOT / "docs" / "v17-runtime-session-log-latest.json"
RUNTIME_BOARD_PATH = ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json"
SESSION_VALIDATION_PATH = ROOT / "docs" / "v17-runtime-session-validation-latest.json"

OPERATOR_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-operator-probe-v1.json"
CAPABILITY_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-app-cli-capability-digest-v1.json"
CLI_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-codex-cli-slot40-induction-v1.json"
CLEANUP_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-cleanup-classifier-v1.json"
ALLOWLIST_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-stage-allowlist-v1.json"
GIT_RESULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v46-git-publication-result-v1.json"

V46_CLOSEOUT_JSON = ROOT / "docs" / "v46-omega-closeout-summary-v1.json"
V46_CONTINUITY_MD = ROOT / "docs" / "v46-omega-continuity-pack-v1.md"
V46_HANDOFF_JSON = ROOT / "docs" / "v46-omega-handoff-policy-v1.json"
V47_CLOSEOUT_JSON = ROOT / "docs" / "v47-beta-closeout-summary-v1.json"
V47_CONTINUITY_MD = ROOT / "docs" / "v47-beta-continuity-pack-v1.md"
V47_HANDOFF_JSON = ROOT / "docs" / "v47-beta-handoff-policy-v1.json"

SUITE_FILES = {
    "quick": ROOT / "docs" / "trinity-live-traces" / "v46-quick-suite-status.json",
    "standard": ROOT / "docs" / "trinity-live-traces" / "v46-standard-suite-status.json",
    "deep": ROOT / "docs" / "trinity-live-traces" / "v46-deep-suite-status.json",
}


def _suite_summary(status: dict[str, Any]) -> dict[str, Any]:
    if not status:
        return {"summary": "missing", "overall_status": "MISSING", "shared_latest_eligible": False}
    counts = status.get("counts", {}) if isinstance(status.get("counts"), dict) else {}
    fail_count = int(counts.get("fail", 0) or 0)
    warn_count = int(counts.get("warn", 0) or 0)
    timeout_count = int(counts.get("timeout", 0) or 0)
    overall = "FAIL" if fail_count or timeout_count or status.get("effective_success") is False else ("WARN" if warn_count else "PASS")
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
    lines.extend(f"- `{key}`: `{value}`" for key, value in closeout.get("core_states", {}).items())
    if closeout.get("slot_40_profile"):
        lines.extend(["", "## Slot 40", ""])
        profile = closeout["slot_40_profile"]
        lines.extend(
            [
                f"- Name: `{profile.get('name', '')}`",
                f"- Gender: `{profile.get('gender', '')}`",
                f"- Role: `{profile.get('role', '')}`",
                f"- Hope: {profile.get('hope', '')}",
            ]
        )
    lines.extend(["", "## Bounded Residuals", ""])
    residuals = closeout.get("bounded_residuals") or []
    lines.extend(f"- `{item}`" for item in residuals) if residuals else lines.append("- `(none)`")
    return "\n".join(lines).rstrip() + "\n"


def _status(payload: dict[str, Any]) -> str:
    return str(payload.get("overall_status") or "MISSING").upper() if payload else "MISSING"


def main() -> int:
    head = git_head()
    operator = read_json(OPERATOR_JSON)
    capability = read_json(CAPABILITY_JSON)
    cli = read_json(CLI_JSON)
    cleanup = read_json(CLEANUP_JSON)
    allowlist = read_json(ALLOWLIST_JSON)
    git_result = read_json(GIT_RESULT_JSON)
    suites = {name: _suite_summary(read_json(path)) for name, path in SUITE_FILES.items()}

    git_publication_state = str(git_result.get("git_publication_state") or ("allowlist_ready_unpublished" if allowlist else "unpublished"))
    slot_40_state = str(cli.get("slot_40_induction_state") or "deferred_blocked")
    slot_40_inducted = slot_40_state == "officially_inducted"
    receiver = "Aletheon + Slot 40 bounded CLI helper" if slot_40_inducted else "Aletheon"
    receiver_rule = "aletheon_lead_slot40_bounded_helper" if slot_40_inducted else "aletheon_facing"

    core_states = {
        "v46_execution_lead": "Aletheon",
        "worktree_baseline_state": operator.get("worktree_baseline_state", "origin_0bcdd7e"),
        "operator_shell_preference": operator.get("operator_shell_preference", "windows_powershell_primary"),
        "wsl_execution_mode": operator.get("wsl_execution_mode", "installed_on_hold_for_agent_switching"),
        "cloud_standby_state": operator.get("cloud_standby_state", "standby_until_user_restores_billing_auth_project_truth"),
        "vesper_standby_state": operator.get("vesper_standby_state", "standby_until_google_cloud_billing_truth"),
        "kai_standby_state": operator.get("kai_standby_state", "standby_until_google_cloud_billing_truth"),
        "codex_cli_version_state": cli.get("codex_cli_version_state") or operator.get("codex_cli_version_state", "unproven"),
        "codex_cli_login_state": cli.get("codex_cli_login_state") or operator.get("codex_cli_login_state", "unproven"),
        "codex_cli_config_model_state": cli.get("codex_cli_config_model_state") or operator.get("codex_cli_config_model_state", "unproven"),
        "codex_cli_invocation_model_state": cli.get("codex_cli_invocation_model_state", "unproven"),
        "codex_cli_model_proof_standard": cli.get("codex_cli_model_proof_standard", "unproven"),
        "slot_40_identity_state": cli.get("slot_40_identity_state", "unproven"),
        "slot_40_memory_state": cli.get("slot_40_memory_state", "unproven"),
        "slot_40_delegation_state": cli.get("slot_40_delegation_state", "unproven"),
        "slot_40_induction_state": slot_40_state,
        "chronicle_windows_state": capability.get("chronicle_windows_state", "not_windows_live_official_docs_mac_pro_only_config_false"),
        "app_plugin_registry_state": capability.get("app_plugin_registry_state", "unproven"),
        "cli_mcp_registry_state": capability.get("cli_mcp_registry_state", "unproven"),
        "v46_cleanup_state": cleanup.get("v46_cleanup_state", "not_run"),
        "suite_ladder_state": "quick_standard_deep_completed" if all(suites[name]["overall_status"] != "MISSING" for name in suites) else "suite_ladder_incomplete",
        "git_publication_state": git_publication_state,
    }

    proof_paths = {
        "operator_probe": "docs/trinity-live-traces/v46-operator-probe-v1.json",
        "capability_digest": "docs/trinity-live-traces/v46-app-cli-capability-digest-v1.json",
        "plugin_surface_digest": "docs/trinity-live-traces/v46-plugin-surface-digest-v1.json",
        "slot_40_induction": "docs/trinity-live-traces/v46-codex-cli-slot40-induction-v1.json",
        "slot_40_official_proof": "docs/trinity-live-traces/v46-slot-40-codex-cli-induction-proof-v1.json",
        "cleanup_classifier": "docs/trinity-live-traces/v46-cleanup-classifier-v1.json",
        "stage_allowlist": "docs/trinity-live-traces/v46-stage-allowlist-v1.json",
        "git_publication_result": "docs/trinity-live-traces/v46-git-publication-result-v1.json",
        "operator_note": "docs/v46-powershell-operator-note-v1.md",
    }

    residuals: list[str] = []
    for name, payload in (("operator", operator), ("capability", capability), ("cli", cli), ("cleanup", cleanup)):
        if _status(payload) != "PASS":
            residuals.append(f"{name}={_status(payload)}")
    for name, suite in suites.items():
        if suite.get("overall_status") != "PASS":
            residuals.append(f"suite::{name}")
    if git_publication_state != "committed_pushed_pr_updated":
        residuals.append(f"git_publication_state={git_publication_state}")

    overall_status = "PASS" if not residuals else "WARN"
    closeout = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "phase": "v46_omega",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "current_head_sha": head,
        "intended_receiver": receiver,
        "receiver_rule_outcome": receiver_rule,
        "summary": {
            "slot_40_induction_state": slot_40_state,
            "codex_cli_model_proof_standard": core_states["codex_cli_model_proof_standard"],
            "cloud_standby_state": core_states["cloud_standby_state"],
            "suite_ladder_state": core_states["suite_ladder_state"],
        },
        "core_states": core_states,
        "proof_paths": proof_paths,
        "slot_40_profile": cli.get("slot_40_profile", {}),
        "slot_40_induction_paths": cli.get("slot_40_induction_paths", {}),
        "suite_statuses": suites,
        "bounded_residuals": residuals,
    }
    handoff = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "phase": "v47_beta",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "current_head_sha": head,
        "intended_receiver": receiver,
        "receiver_rule_outcome": receiver_rule,
        "core_states": core_states,
        "slot_40_profile": cli.get("slot_40_profile", {}),
        "bounded_residuals": residuals,
        "primary_focus_lanes": [
            "keep Google Cloud, Vesper Ion, and Kai on standby until billing/auth/project truth is restored",
            "use slot 40 only as a bounded Codex CLI helper under Aletheon lead if induction is green",
            "triage suite residuals without staging unrelated generated churn",
        ],
    }

    for path in (RUNTIME_RESOLUTION_PATH, RUNTIME_LOG_PATH, RUNTIME_BOARD_PATH, SESSION_VALIDATION_PATH):
        payload = read_json(path)
        payload["generated_utc"] = now_iso()
        payload["phase"] = "v46_omega"
        payload["authority_model"] = "repo_first"
        payload["source_branch"] = PUBLICATION_BRANCH
        payload["current_head_sha"] = head
        payload.update(core_states)
        if slot_40_inducted:
            payload["v46_slot_40_member"] = {
                "slot": 40,
                "display_name": cli.get("slot_40_profile", {}).get("name", ""),
                "gender": cli.get("slot_40_profile", {}).get("gender", ""),
                "role": cli.get("slot_40_profile", {}).get("role", ""),
                "hope": cli.get("slot_40_profile", {}).get("hope", ""),
                "runtime_surface": "codex_cli",
                "model_proof_standard": core_states["codex_cli_model_proof_standard"],
                "paths": cli.get("slot_40_induction_paths", {}),
            }
        if path == RUNTIME_RESOLUTION_PATH:
            payload["active_handoff_pack_path"] = "docs/v46-omega-continuity-pack-v1.md"
            payload["active_handoff_policy_path"] = "docs/v46-omega-handoff-policy-v1.json"
            payload["next_receiver_pack_path"] = "docs/v47-beta-continuity-pack-v1.md"
            payload["next_receiver_policy_path"] = "docs/v47-beta-handoff-policy-v1.json"
        write_json(path, payload)

    write_json(V46_CLOSEOUT_JSON, closeout)
    write_text(V46_CONTINUITY_MD, _continuity_markdown(closeout, "V46 Omega Continuity Pack"))
    write_json(V46_HANDOFF_JSON, closeout)
    write_json(V47_CLOSEOUT_JSON, handoff)
    write_text(V47_CONTINUITY_MD, _continuity_markdown(handoff, "V47 Beta Continuity Pack"))
    write_json(V47_HANDOFF_JSON, handoff)
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

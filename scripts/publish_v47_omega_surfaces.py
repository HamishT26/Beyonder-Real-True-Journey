#!/usr/bin/env python3
"""Publish V47 Omega closeout and V48 Beta receiver surfaces."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from trinity_v47_common import PUBLICATION_BRANCH, ROOT, git_head, now_iso, read_json, write_json, write_text

RUNTIME_RESOLUTION_PATH = ROOT / "docs" / "trinity-runtime-model-resolution-v1.json"
RUNTIME_LOG_PATH = ROOT / "docs" / "v17-runtime-session-log-latest.json"
RUNTIME_BOARD_PATH = ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json"
SESSION_VALIDATION_PATH = ROOT / "docs" / "v17-runtime-session-validation-latest.json"

OPERATOR_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-operator-probe-v1.json"
ARI_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-ari-colearning-proof-v1.json"
CAPABILITY_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-codex-memory-capability-digest-v1.json"
PLUGIN_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-plugin-surface-digest-v1.json"
HYGIENE_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-codex-home-hygiene-v1.json"
CLEANUP_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-cleanup-classifier-v1.json"
ALLOWLIST_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-stage-allowlist-v1.json"
GIT_RESULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-git-publication-result-v1.json"
V46_CLOSEOUT_JSON = ROOT / "docs" / "v46-omega-closeout-summary-v1.json"

V47_CLOSEOUT_JSON = ROOT / "docs" / "v47-omega-closeout-summary-v1.json"
V47_CONTINUITY_MD = ROOT / "docs" / "v47-omega-continuity-pack-v1.md"
V47_HANDOFF_JSON = ROOT / "docs" / "v47-omega-handoff-policy-v1.json"
V48_CLOSEOUT_JSON = ROOT / "docs" / "v48-beta-closeout-summary-v1.json"
V48_CONTINUITY_MD = ROOT / "docs" / "v48-beta-continuity-pack-v1.md"
V48_HANDOFF_JSON = ROOT / "docs" / "v48-beta-handoff-policy-v1.json"

SUITE_FILES = {
    "quick": ROOT / "docs" / "trinity-live-traces" / "v47-quick-suite-status.json",
    "standard": ROOT / "docs" / "trinity-live-traces" / "v47-standard-suite-status.json",
    "deep": ROOT / "docs" / "trinity-live-traces" / "v47-deep-suite-status.json",
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


def _status(payload: dict[str, Any]) -> str:
    return str(payload.get("overall_status") or "MISSING").upper() if payload else "MISSING"


def _ari_profile(v46_closeout: dict[str, Any]) -> dict[str, Any]:
    profile = v46_closeout.get("slot_40_profile", {}) if isinstance(v46_closeout.get("slot_40_profile"), dict) else {}
    return {
        "slot": 40,
        "name": profile.get("name", "Ari"),
        "gender": profile.get("gender", "nonbinary"),
        "role": profile.get("role", "GHC slot 40 Codex CLI implementation agent"),
        "hope": profile.get("hope", "To turn evidence into durable working systems"),
        "runtime_surface": "codex_cli",
        "v47_activation_rule": "bounded_helper_under_aletheon_lead",
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
    if closeout.get("ari_profile"):
        profile = closeout["ari_profile"]
        lines.extend(["", "## Ari", ""])
        lines.extend(
            [
                f"- Slot: `{profile.get('slot', 40)}`",
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


def main() -> int:
    head = git_head()
    operator = read_json(OPERATOR_JSON)
    ari = read_json(ARI_JSON)
    capability = read_json(CAPABILITY_JSON)
    plugin = read_json(PLUGIN_JSON)
    hygiene = read_json(HYGIENE_JSON)
    cleanup = read_json(CLEANUP_JSON)
    allowlist = read_json(ALLOWLIST_JSON)
    git_result = read_json(GIT_RESULT_JSON)
    v46_closeout = read_json(V46_CLOSEOUT_JSON)
    suites = {name: _suite_summary(read_json(path)) for name, path in SUITE_FILES.items()}
    ari_profile = _ari_profile(v46_closeout)

    ari_green = (
        ari.get("ari_activation_state") == "verified"
        and ari.get("ari_memory_state") == "verified"
        and ari.get("ari_delegation_state") == "verified"
    )
    receiver = "Aletheon + Ari bounded CLI helper" if ari_green else "Aletheon"
    receiver_rule = "aletheon_lead_ari_bounded_helper" if ari_green else "aletheon_facing_ari_probe_residual"
    git_publication_state = str(git_result.get("git_publication_state") or ("allowlist_ready_unpublished" if allowlist else "unpublished"))

    core_states = {
        "v47_execution_lead": "Aletheon",
        "ari_activation_state": ari.get("ari_activation_state", "not_run"),
        "bigtable_state": operator.get("bigtable_state", "operator_reported_bigtable_deleted_unverified_until_gcp_auth_restored"),
        "cloud_standby_state": operator.get("cloud_standby_state", "standby_until_user_restores_billing_auth_project_truth"),
        "codex_memory_state": capability.get("codex_memory_state") or operator.get("codex_memory_state", "memory_state_unverified"),
        "chronicle_windows_state": capability.get("chronicle_windows_state") or operator.get("chronicle_windows_state", "not_windows_live"),
        "codex_cli_warning_state": ari.get("codex_cli_warning_state") or capability.get("codex_cli_warning_state", "not_run"),
        "app_plugin_registry_state": plugin.get("app_plugin_registry_state") or capability.get("app_plugin_registry_state", "unproven"),
        "cli_mcp_registry_state": plugin.get("cli_mcp_registry_state") or operator.get("cli_mcp_registry_state", "unproven"),
        "iab_state": operator.get("iab_state", "available_not_callable_from_session"),
        "admin_shell_state": operator.get("admin_shell_state", "not_administrator_or_unverified"),
        "v47_cleanup_state": cleanup.get("v47_cleanup_state", "not_run"),
        "suite_ladder_state": "quick_standard_deep_completed" if all(suites[name]["overall_status"] != "MISSING" for name in suites) else "suite_ladder_incomplete",
        "git_publication_state": git_publication_state,
        "vesper_standby_state": operator.get("vesper_standby_state", "standby_until_google_cloud_billing_truth"),
        "kai_standby_state": operator.get("kai_standby_state", "standby_until_google_cloud_billing_truth"),
        "wsl_execution_mode": operator.get("wsl_execution_mode", "installed_on_hold_for_agent_switching"),
        "local_codex_hygiene_state": hygiene.get("local_codex_hygiene_state", "not_run"),
    }

    proof_paths = {
        "operator_probe": "docs/trinity-live-traces/v47-operator-probe-v1.json",
        "ari_colearning": "docs/trinity-live-traces/v47-ari-colearning-proof-v1.json",
        "codex_memory_capability_digest": "docs/trinity-live-traces/v47-codex-memory-capability-digest-v1.json",
        "plugin_surface_digest": "docs/trinity-live-traces/v47-plugin-surface-digest-v1.json",
        "codex_home_hygiene": "docs/trinity-live-traces/v47-codex-home-hygiene-v1.json",
        "cleanup_classifier": "docs/trinity-live-traces/v47-cleanup-classifier-v1.json",
        "stage_allowlist": "docs/trinity-live-traces/v47-stage-allowlist-v1.json",
        "git_publication_result": "docs/trinity-live-traces/v47-git-publication-result-v1.json",
        "operator_note": "docs/v47-powershell-operator-note-v1.md",
        "aletheon_reflection": "docs/trinity-agent-reflections/v47-aletheon-reflection-v1.md",
        "ari_reflection": "docs/trinity-agent-reflections/v47-ari-reflection-v1.md",
    }

    residuals: list[str] = []
    for name, payload in (
        ("operator", operator),
        ("ari", ari),
        ("capability", capability),
        ("hygiene", hygiene),
        ("cleanup", cleanup),
    ):
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
        "phase": "v47_omega",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "current_head_sha": head,
        "intended_receiver": receiver,
        "receiver_rule_outcome": receiver_rule,
        "summary": {
            "ari_activation_state": core_states["ari_activation_state"],
            "cloud_standby_state": core_states["cloud_standby_state"],
            "bigtable_state": core_states["bigtable_state"],
            "codex_memory_state": core_states["codex_memory_state"],
            "suite_ladder_state": core_states["suite_ladder_state"],
        },
        "core_states": core_states,
        "proof_paths": proof_paths,
        "ari_profile": ari_profile,
        "suite_statuses": suites,
        "bounded_residuals": residuals,
        "official_source_anchors": capability.get("official_source_anchors", []),
    }
    handoff = {
        "generated_utc": now_iso(),
        "overall_status": overall_status,
        "phase": "v48_beta",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "current_head_sha": head,
        "intended_receiver": receiver,
        "receiver_rule_outcome": receiver_rule,
        "core_states": core_states,
        "ari_profile": ari_profile,
        "bounded_residuals": residuals,
        "primary_focus_lanes": [
            "keep GCP, Vertex AI, Bigtable, Agent Engine, Gemini CLI, Kai, and Vesper on standby until billing/auth/project truth is restored",
            "continue Codex app/CLI co-learning with Ari only as a bounded helper under Aletheon lead",
            "fix or quarantine suite residuals before running heavier collab/materialize lanes",
            "preserve forward-only git publication with curated allowlists only",
        ],
    }

    for path in (RUNTIME_RESOLUTION_PATH, RUNTIME_LOG_PATH, RUNTIME_BOARD_PATH, SESSION_VALIDATION_PATH):
        payload = read_json(path)
        payload["generated_utc"] = now_iso()
        payload["phase"] = "v47_omega"
        payload["authority_model"] = "repo_first"
        payload["source_branch"] = PUBLICATION_BRANCH
        payload["current_head_sha"] = head
        payload.update(core_states)
        payload["v47_ari_member"] = ari_profile
        if path == RUNTIME_RESOLUTION_PATH:
            payload["active_handoff_pack_path"] = "docs/v47-omega-continuity-pack-v1.md"
            payload["active_handoff_policy_path"] = "docs/v47-omega-handoff-policy-v1.json"
            payload["next_receiver_pack_path"] = "docs/v48-beta-continuity-pack-v1.md"
            payload["next_receiver_policy_path"] = "docs/v48-beta-handoff-policy-v1.json"
        write_json(path, payload)

    write_json(V47_CLOSEOUT_JSON, closeout)
    write_text(V47_CONTINUITY_MD, _continuity_markdown(closeout, "V47 Omega Continuity Pack"))
    write_json(V47_HANDOFF_JSON, closeout)
    write_json(V48_CLOSEOUT_JSON, handoff)
    write_text(V48_CONTINUITY_MD, _continuity_markdown(handoff, "V48 Beta Continuity Pack"))
    write_json(V48_HANDOFF_JSON, handoff)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Publish V48 Omega closeout and V49 Beta receiver surfaces."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from trinity_v48_common import PUBLICATION_BRANCH, ROOT, git_head, now_iso, read_json, write_json, write_text

RUNTIME_RESOLUTION_PATH = ROOT / "docs" / "trinity-runtime-model-resolution-v1.json"
RUNTIME_LOG_PATH = ROOT / "docs" / "v17-runtime-session-log-latest.json"
RUNTIME_BOARD_PATH = ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json"
SESSION_VALIDATION_PATH = ROOT / "docs" / "v17-runtime-session-validation-latest.json"

OPERATOR_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-operator-probe-v1.json"
CLEANUP_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-cleanup-classifier-v1.json"
JOURNEY_JSON = ROOT / "docs" / "auto-generated" / "v48-journey-advisory-digest-v1.json"
CONTROL_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-control-plane-digest-v1.json"
KIMICLAW_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-kimiclaw-prep-v1.json"
ARI_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-ari-collaboration-proof-v1.json"
ALLOWLIST_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-stage-allowlist-v1.json"
GIT_RESULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v48-git-publication-result-v1.json"

V48_CLOSEOUT_JSON = ROOT / "docs" / "v48-omega-closeout-summary-v1.json"
V48_CONTINUITY_MD = ROOT / "docs" / "v48-omega-continuity-pack-v1.md"
V48_HANDOFF_JSON = ROOT / "docs" / "v48-omega-handoff-policy-v1.json"
V49_CLOSEOUT_JSON = ROOT / "docs" / "v49-beta-closeout-summary-v1.json"
V49_CONTINUITY_MD = ROOT / "docs" / "v49-beta-continuity-pack-v1.md"
V49_HANDOFF_JSON = ROOT / "docs" / "v49-beta-handoff-policy-v1.json"

SUITE_FILES = {
    "quick": ROOT / "docs" / "trinity-live-traces" / "v48-quick-suite-status.json",
    "standard": ROOT / "docs" / "trinity-live-traces" / "v48-standard-suite-status.json",
    "deep": ROOT / "docs" / "trinity-live-traces" / "v48-deep-suite-status.json",
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
    lines.extend(["", "## Bounded Residuals", ""])
    residuals = closeout.get("bounded_residuals") or []
    lines.extend(f"- `{item}`" for item in residuals) if residuals else lines.append("- `(none)`")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    head = git_head()
    operator = read_json(OPERATOR_JSON)
    cleanup = read_json(CLEANUP_JSON)
    journey = read_json(JOURNEY_JSON)
    control = read_json(CONTROL_JSON)
    kimiclaw = read_json(KIMICLAW_JSON)
    ari = read_json(ARI_JSON)
    allowlist = read_json(ALLOWLIST_JSON)
    git_result = read_json(GIT_RESULT_JSON)
    suites = {name: _suite_summary(read_json(path)) for name, path in SUITE_FILES.items()}
    git_publication_state = str(git_result.get("git_publication_state") or ("allowlist_ready_unpublished" if allowlist else "unpublished"))
    suite_state = "quick_standard_deep_completed" if all(suites[name]["overall_status"] != "MISSING" for name in suites) else "suite_ladder_incomplete"
    deep_repeats = bool(suites.get("deep", {}).get("fail_count") == suites.get("standard", {}).get("fail_count") and suites.get("deep", {}).get("overall_status") == suites.get("standard", {}).get("overall_status"))

    core_states = {
        "v48_execution_lead": "Aletheon",
        "ari_activation_state": operator.get("ari_activation_state", "verified_bounded_helper"),
        "cloud_execution_mode": operator.get("cloud_execution_mode", "standby_billing_auth_project_not_cleared"),
        "gcp_standby_state": operator.get("gcp_standby_state", "standby_until_user_restores_billing_auth_project_truth"),
        "kai_standby_state": operator.get("kai_standby_state", "standby_until_google_cloud_billing_truth"),
        "vesper_standby_state": operator.get("vesper_standby_state", "standby_until_google_cloud_billing_truth"),
        "bigtable_state": operator.get("bigtable_state", "operator_reported_bigtable_deleted_unverified_until_gcp_auth_restored"),
        "local_to_cloud_runtime_state": operator.get("local_to_cloud_runtime_state", "on_hold_app_side_model_unavailable"),
        "local_archive_cleanup_state": cleanup.get("local_archive_cleanup_state", "not_run"),
        "archive_calibration_state": cleanup.get("archive_calibration_state", "not_run"),
        "bank_mesh_state": "local_d_drive_repo_side_scaffold_only_cloud_banks_on_standby",
        "control_plane_state": control.get("control_plane_state", "not_run"),
        "vercel_free_tier_state": control.get("vercel_free_tier_state", "not_run"),
        "neon_free_tier_state": control.get("neon_free_tier_state", "not_run"),
        "circleci_state": control.get("circleci_state", "not_run"),
        "notion_mission_control_state": control.get("notion_mission_control_state", "not_run"),
        "kimiclaw_research_state": kimiclaw.get("kimiclaw_research_state", "not_run"),
        "slot_41_preparation_state": kimiclaw.get("slot_41_preparation_state", "not_run"),
        "swarm_42_53_state": kimiclaw.get("swarm_42_53_state", "not_run"),
        "plugin_surface_split_state": control.get("plugin_surface_split_state", "not_run"),
        "codex_cli_extension_state": control.get("codex_cli_extension_state", "not_run"),
        "suite_ladder_state": suite_state,
        "git_publication_state": git_publication_state,
    }

    residuals: list[str] = []
    for name, payload in (("operator", operator), ("cleanup", cleanup), ("journey", journey), ("control", control), ("kimiclaw", kimiclaw), ("ari", ari)):
        if _status(payload) not in {"PASS"}:
            residuals.append(f"{name}={_status(payload)}")
    for name, suite in suites.items():
        if suite.get("overall_status") != "PASS":
            residuals.append(f"suite::{name}")
    if git_publication_state not in {"committed_pushed_pr45_branch_updated", "committed_pushed_pr_updated"}:
        residuals.append(f"git_publication_state={git_publication_state}")
    if deep_repeats:
        residuals.append("deep_repeats_standard_fail_family_stop_before_materialize")

    closeout = {
        "generated_utc": now_iso(),
        "overall_status": "PASS" if not residuals else "WARN",
        "phase": "v48_omega",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "current_head_sha": head,
        "intended_receiver": "Aletheon + Ari bounded helper; slot 41 future operator induction",
        "receiver_rule_outcome": "v49_aletheon_facing_ari_bounded_helper_kimiclaw_prepared_not_inducted",
        "summary": {
            "local_archive_cleanup_state": core_states["local_archive_cleanup_state"],
            "control_plane_state": core_states["control_plane_state"],
            "slot_41_preparation_state": core_states["slot_41_preparation_state"],
            "swarm_42_53_state": core_states["swarm_42_53_state"],
            "suite_ladder_state": suite_state,
        },
        "core_states": core_states,
        "proof_paths": {
            "operator_probe": "docs/trinity-live-traces/v48-operator-probe-v1.json",
            "cleanup_classifier": "docs/trinity-live-traces/v48-cleanup-classifier-v1.json",
            "journey_digest": "docs/auto-generated/v48-journey-advisory-digest-v1.json",
            "control_plane": "docs/trinity-live-traces/v48-control-plane-digest-v1.json",
            "kimiclaw_prep": "docs/trinity-live-traces/v48-kimiclaw-prep-v1.json",
            "ari_collaboration": "docs/trinity-live-traces/v48-ari-collaboration-proof-v1.json",
            "stage_allowlist": "docs/trinity-live-traces/v48-stage-allowlist-v1.json",
            "git_publication_result": "docs/trinity-live-traces/v48-git-publication-result-v1.json",
        },
        "suite_statuses": suites,
        "bounded_residuals": residuals,
        "official_source_anchors": [
            {"name": "Vercel pricing", "url": "https://vercel.com/pricing"},
            {"name": "Vercel Hobby plan", "url": "https://vercel.com/docs/accounts/plans/hobby"},
            {"name": "Vercel Sandbox pricing and limits", "url": "https://vercel.com/docs/vercel-sandbox/pricing"},
            {"name": "Neon pricing", "url": "https://neon.com/pricing"},
            {"name": "Moonshot platform overview", "url": "https://platform.moonshot.ai/docs/overview"},
            {"name": "Kimi Claw introduction", "url": "https://www.kimi.com/resources/kimi-claw-introduction"},
        ],
    }
    handoff = {
        "generated_utc": now_iso(),
        "overall_status": closeout["overall_status"],
        "phase": "v49_beta",
        "authority_model": "repo_first",
        "source_branch": PUBLICATION_BRANCH,
        "current_head_sha": head,
        "intended_receiver": closeout["intended_receiver"],
        "receiver_rule_outcome": closeout["receiver_rule_outcome"],
        "core_states": core_states,
        "bounded_residuals": residuals,
        "primary_focus_lanes": [
            "continue cleanup only with backup-first generated-artifact rules",
            "prove or defer Vercel/Neon/CircleCI live connector surfaces before external writes",
            "keep slot 41 prepared_not_inducted until the operator performs Kimiclaw induction",
            "do not run materialize/collab unless suite residuals produce new signal",
        ],
    }
    for path in (RUNTIME_RESOLUTION_PATH, RUNTIME_LOG_PATH, RUNTIME_BOARD_PATH, SESSION_VALIDATION_PATH):
        payload = read_json(path)
        payload["generated_utc"] = now_iso()
        payload["phase"] = "v48_omega"
        payload["authority_model"] = "repo_first"
        payload["source_branch"] = PUBLICATION_BRANCH
        payload["current_head_sha"] = head
        payload.update(core_states)
        if path == RUNTIME_RESOLUTION_PATH:
            payload["active_handoff_pack_path"] = "docs/v48-omega-continuity-pack-v1.md"
            payload["active_handoff_policy_path"] = "docs/v48-omega-handoff-policy-v1.json"
            payload["next_receiver_pack_path"] = "docs/v49-beta-continuity-pack-v1.md"
            payload["next_receiver_policy_path"] = "docs/v49-beta-handoff-policy-v1.json"
        write_json(path, payload)
    write_json(V48_CLOSEOUT_JSON, closeout)
    write_text(V48_CONTINUITY_MD, _continuity_markdown(closeout, "V48 Omega Continuity Pack"))
    write_json(V48_HANDOFF_JSON, closeout)
    write_json(V49_CLOSEOUT_JSON, handoff)
    write_text(V49_CONTINUITY_MD, _continuity_markdown(handoff, "V49 Beta Continuity Pack"))
    write_json(V49_HANDOFF_JSON, handoff)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

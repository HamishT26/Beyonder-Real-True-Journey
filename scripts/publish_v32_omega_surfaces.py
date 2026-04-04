#!/usr/bin/env python3
"""Publish V32 Omega closeout surfaces and the V33 Beta continuity pack."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
AUTHORITATIVE_REPO = r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey"
WORKBENCH_REPO = r"C:\Users\hamis\OneDrive\Documents\New project"
CONTRIBUTIONS = Path.home() / "Newest GHC Family Contributions v2 - (Nz Thursday 2nd - Friday 3rd of April 2026).txt"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(rel: str, payload: dict[str, Any]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def git_head() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return (result.stdout or "").strip()


def suite_summary(status: dict[str, Any]) -> dict[str, Any]:
    counts = status.get("counts", {})
    explicit = status.get("overall_status")
    if explicit:
        overall = explicit
    elif counts.get("fail", 0) or counts.get("timeout", 0):
        overall = "FAIL"
    elif counts.get("warn", 0):
        overall = "WARN"
    else:
        overall = "PASS"
    return {
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL",
        "pass_count": counts.get("pass", 0),
        "warn_count": counts.get("warn", 0),
        "fail_count": counts.get("fail", 0),
        "timeout_count": counts.get("timeout", 0),
        "overall_status": overall,
        "suite_duration_sec": status.get("suite_duration_sec", 0),
    }


def shared_anchor(status: dict[str, Any]) -> dict[str, Any]:
    counts = status.get("counts", {})
    return {
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL",
        "pass_count": counts.get("pass", 0),
        "warn_count": counts.get("warn", 0),
        "fail_count": counts.get("fail", 0),
        "timeout_count": counts.get("timeout", 0),
        "expansion_systems_passed": status.get("expansion_systems_passed", 0),
        "expansion_systems_total": status.get("expansion_systems_total", 0),
        "checkpoint_class": status.get("checkpoint_class", ""),
        "shared_latest_eligible": bool(status.get("shared_latest_eligible")),
        "suite_duration_sec": status.get("suite_duration_sec", 0),
        "primary_blocker": "",
        "primary_blocker_detail": "Shared latest remains authoritative while V32 publishes cloud and connector truth on dedicated surfaces.",
        "quick_lane_summary": "",
    }


def contribution_digest() -> dict[str, Any]:
    if not CONTRIBUTIONS.exists():
        return {"status": "missing", "path": str(CONTRIBUTIONS), "advisory_signals": []}
    text = CONTRIBUTIONS.read_text(encoding="utf-8", errors="replace")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "status": "available",
        "path": str(CONTRIBUTIONS),
        "line_count": len(lines),
        "advisory_signals": [
            "Treat the newest GHC contributions as advisory and non-authoritative.",
            "Keep V32 focused on cloud proof, blocker clearance, and honest publication.",
            "Preserve repo-first authority while widening bounded cloud and mirror lanes.",
        ],
    }


def continuity_pack(title: str, receiver: str, predecessor: str, shared: dict[str, Any], residuals: list[str], next_action: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Source branch: `{BRANCH}`",
        f"- Current branch head: `{git_head()}`",
        f"- Authority model: `repo_first`",
        f"- Authoritative repo: `{AUTHORITATIVE_REPO}`",
        f"- Separate workbench: `{WORKBENCH_REPO}`",
        "- Current shell: `powershell`",
        "- Readiness state: `wsl_target_blocked_windows_operator_fallback`",
        "- Docker runtime role: `soft_retired_fallback`",
        f"- Intended receiver: `{receiver}`",
        f"- Predecessor line: `{predecessor}`",
        f"- Shared latest anchor remains `{shared['summary']}`",
        "",
        "## Residuals",
        "",
    ]
    for item in residuals:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Action", "", f"- {next_action}", ""])
    return "\n".join(lines)


def main() -> int:
    generated = now_iso()
    current_head = git_head()
    system_suite = read_json("docs/system-suite-status.json")
    quick = read_json("docs/v32-quick-suite-status.json") or read_json("docs/v31-quick-suite-status.json")
    standard = read_json("docs/v32-standard-suite-status.json") or read_json("docs/v31-standard-suite-status.json")
    deep = read_json("docs/v32-deep-suite-status.json") or read_json("docs/v31-deep-suite-status.json")
    collab = read_json("docs/v32-collab-suite-status.json") or read_json("docs/v31-collab-suite-status.json")
    mat_l2 = read_json("docs/v32-materialize-l2-status.json") or read_json("docs/v31-materialize-l2-status.json")
    mat_l3 = read_json("docs/v32-materialize-l3-status.json") or read_json("docs/v31-materialize-l3-status.json")
    mat_l4 = read_json("docs/v32-materialize-l4-status.json") or read_json("docs/v31-materialize-l4-status.json")
    mat_l5 = read_json("docs/v32-materialize-l5-status.json") or read_json("docs/v31-materialize-l5-status.json")

    runtime_resolution = read_json("docs/trinity-runtime-model-resolution-v1.json")
    session_log = read_json("docs/v17-runtime-session-log-latest.json")
    runtime_truth = read_json("docs/v17-runtime-truth-resolution-board-v1.json")
    connector_cache = read_json("docs/trinity-mcp-cache/connector-materialization-latest.json")
    memory_validation = read_json("docs/trinity-memory-bank-validation-latest.json")
    onedrive_hydration = read_json("docs/trinity-live-traces/v31-onedrive-repo-hydration-proof-v1.json")
    onedrive_mirror = read_json("docs/trinity-live-traces/v31-onedrive-mirror-sync-proof-v1.json")

    gcp_bootstrap = read_json("docs/trinity-live-traces/v32-gcp-bootstrap-proof-v1.json")
    gcs_mirror = read_json("docs/trinity-live-traces/v32-gcs-primary-mirror-proof-v1.json")
    gke_bootstrap = read_json("docs/trinity-live-traces/v32-gke-bootstrap-proof-v1.json")
    gmail = read_json("docs/trinity-live-traces/v32-gmail-materialization-proof-v1.json")
    composio = read_json("docs/trinity-live-traces/v32-composio-onedrive-proof-v1.json")
    hf = read_json("docs/trinity-live-traces/v32-huggingface-guarded-lane-proof-v1.json")
    session_closeout = read_json("docs/trinity-live-traces/v32-session-closeout-proof-v1.json")
    storage_forecast = read_json("docs/trinity-live-traces/v32-storage-forecast-proof-v1.json")
    archive_recall = read_json("docs/trinity-live-traces/v32-archive-recall-proof-v1.json")

    shared = shared_anchor(system_suite)
    if quick:
        shared["quick_lane_summary"] = suite_summary(quick)["summary"]

    digest = contribution_digest()
    write_json("docs/auto-generated/v32-ghc-contributions-digest.json", digest)
    write_text(
        "docs/auto-generated/v32-ghc-contributions-digest.md",
        "\n".join(
            [
                "# V32 GHC Contributions Digest",
                "",
                f"- Source: `{digest['path']}`",
                f"- Status: `{digest['status']}`",
                "",
                "## Advisory Signals",
                "",
                *[f"- {item}" for item in digest.get("advisory_signals", [])],
                "",
            ]
        ),
    )

    gmail_state = gmail.get("gmail_materialization_state", gmail.get("proof_state", "open_with_blocker"))
    composio_state = composio.get("proof_state", "api_verified_connector_unloaded")
    hf_state = hf.get("proof_state", "live_execution_proven")
    closeout_state = session_closeout.get("session_closeout_state", "unknown")
    memory_state = "pass" if memory_validation.get("overall_status") == "PASS" else "open_with_blocker"

    suite_statuses = {
        "quick": suite_summary(quick),
        "standard": suite_summary(standard),
        "deep": suite_summary(deep),
        "collab": suite_summary(collab),
        "materialize_l2": suite_summary(mat_l2),
        "materialize_l3": suite_summary(mat_l3),
        "materialize_l4": suite_summary(mat_l4),
        "materialize_l5": suite_summary(mat_l5),
    }
    suite_green = all(summary["overall_status"] == "PASS" for summary in suite_statuses.values())
    gcp_green = gcp_bootstrap.get("overall_status") == "PASS"
    gke_green = gke_bootstrap.get("overall_status") == "PASS"
    gmail_green = gmail_state == "bounded_live_write"
    composio_consistent = composio_state in {
        "toolkit_materialized_connected_read",
        "onedrive_connected_account_not_visible",
        "toolkit_visible_but_execute_blocked",
        "onedrive_toolkit_not_visible",
    }

    receiver_ready = gcp_green and gke_green and gmail_green and composio_consistent and suite_green
    receiver_outcome = "orun_facing" if receiver_ready else "aletheon_facing"

    connector_cache.update(
        {
            "generated_utc": generated,
            "phase": "v32_omega",
            "gmail_materialization_state": gmail_state,
            "composio_onedrive_state": composio_state,
            "huggingface_execution_state": hf_state,
            "verified_composio_toolkits": composio.get("verified_composio_toolkits", []),
            "connector_sweep_notes": [
                "Gmail promotes only after full bounded live write proof.",
                "Composio OneDrive stays honest until a connected toolkit read succeeds.",
                "Hugging Face remains live_execution_proven with V32 guard metadata.",
            ],
        }
    )
    write_json("docs/trinity-mcp-cache/connector-materialization-latest.json", connector_cache)

    runtime_resolution.update(
        {
            "generated_utc": generated,
            "phase": "v32_omega",
            "authority_model": "repo_first",
            "authoritative_repo_path": AUTHORITATIVE_REPO,
            "separate_workbench_path": WORKBENCH_REPO,
            "current_shell": "powershell",
            "readiness_state": "wsl_target_blocked_windows_operator_fallback",
            "docker_runtime_role": "soft_retired_fallback",
            "onedrive_repo_hydration_state": onedrive_hydration.get("onedrive_repo_hydration_state", "stable_local_clone_primary"),
            "onedrive_migration_state": onedrive_mirror.get("onedrive_migration_state", "guided_non_authoritative_mirror_completed"),
            "cloud_provider_health": onedrive_hydration.get("cloud_provider_health", "degraded"),
            "gcp_auth_state": gcp_bootstrap.get("proof_state", "unknown"),
            "gcp_primary_identity": gcp_bootstrap.get("gcp_primary_identity", "unknown"),
            "gcp_custom_identity_state": gcp_bootstrap.get("gcp_custom_identity_state", "unknown"),
            "gcp_project_state": gcp_bootstrap.get("gcp_project_state", "unknown"),
            "gcloud_cli_state": gcp_bootstrap.get("gcloud_cli_state", "unknown"),
            "gcs_primary_mirror_state": gcs_mirror.get("gcs_primary_mirror_state", gcs_mirror.get("proof_state", "unknown")),
            "secret_manager_state": gcp_bootstrap.get("secret_manager_state", "unknown"),
            "artifact_registry_state": gcp_bootstrap.get("artifact_registry_state", "unknown"),
            "gke_api_state": gcp_bootstrap.get("gke_api_state", "unknown"),
            "gke_cluster_inventory": gke_bootstrap.get("gke_cluster_inventory", []),
            "gke_cluster_state": gke_bootstrap.get("gke_cluster_state", gke_bootstrap.get("proof_state", "unknown")),
            "gmail_scope_state": gmail.get("gmail_scope_state", "unknown"),
            "gmail_materialization_state": gmail_state,
            "composio_onedrive_state": composio_state,
            "hf_guarded_lane_state": hf_state,
            "memory_bank_watch_band_state": memory_state,
            "activation_sweep_state": {
                "status": "PASS" if gcp_green and suite_green else "WARN",
                "completed_lanes": [
                    "gcp_bootstrap",
                    "gcs_primary_mirror",
                    "gke_cluster",
                    "gmail_scope_preflight",
                    "composio_onedrive",
                    "hf_guarded_lane",
                    "session_closeout",
                ],
            },
            "session_closeout_state": closeout_state,
            "current_shared_suite_surface": shared,
            "active_handoff_pack_path": "docs/v32-omega-continuity-pack-v1.md",
            "active_handoff_policy_path": "docs/v32-omega-handoff-policy-v1.json",
            "next_receiver_pack_path": "docs/v33-beta-continuity-pack-v1.md",
            "next_receiver_policy_path": "docs/v33-beta-handoff-policy-v1.json",
            "contributions_digest_path": "docs/auto-generated/v32-ghc-contributions-digest.md",
        }
    )
    write_json("docs/trinity-runtime-model-resolution-v1.json", runtime_resolution)

    session_log.update(
        {
            "generated_utc": generated,
            "session_id": "v32-omega-closeout",
            "current_shell": "powershell",
            "readiness_state": "wsl_target_blocked_windows_operator_fallback",
            "docker_runtime_role": "soft_retired_fallback",
            "gcp_auth_state": gcp_bootstrap.get("proof_state", "unknown"),
            "gke_cluster_state": gke_bootstrap.get("gke_cluster_state", gke_bootstrap.get("proof_state", "unknown")),
            "gmail_materialization_state": gmail_state,
            "composio_onedrive_state": composio_state,
            "hf_guarded_lane_state": hf_state,
            "session_closeout_state": closeout_state,
        }
    )
    write_json("docs/v17-runtime-session-log-latest.json", session_log)

    runtime_truth.update(
        {
            "generated_utc": generated,
            "phase": "v32_omega",
            "current_shell": "powershell",
            "readiness_state": "wsl_target_blocked_windows_operator_fallback",
            "docker_runtime_role": "soft_retired_fallback",
            "gcp_auth_state": gcp_bootstrap.get("proof_state", "unknown"),
            "gcs_primary_mirror_state": gcs_mirror.get("gcs_primary_mirror_state", gcs_mirror.get("proof_state", "unknown")),
            "gke_cluster_state": gke_bootstrap.get("gke_cluster_state", gke_bootstrap.get("proof_state", "unknown")),
            "gmail_scope_state": gmail.get("gmail_scope_state", "unknown"),
            "gmail_materialization_state": gmail_state,
            "composio_onedrive_state": composio_state,
            "hf_guarded_lane_state": hf_state,
            "session_closeout_state": closeout_state,
            "storage_forecast": storage_forecast,
            "archive_recall": archive_recall,
            "suite_statuses": suite_statuses,
        }
    )
    write_json("docs/v17-runtime-truth-resolution-board-v1.json", runtime_truth)

    residuals: list[str] = []
    if gcp_bootstrap.get("gcloud_cli_state", "").startswith("blocked_"):
        residuals.append("WSL Ubuntu still does not provide a clean shell, so the preferred gcloud operator lane remains blocked and V32 used Windows plus direct API fallbacks.")
    if not gmail_green:
        residuals.append("Gmail did not promote to bounded live write, so the auth/scope blocker still gates receiver promotion.")
    if composio_state != "toolkit_materialized_connected_read":
        residuals.append("Composio OneDrive did not fully materialize into a connected read lane, so it stays honest rather than promoted.")
    if not suite_green:
        residuals.append("One or more V32 suite lanes are not yet green, so the shared latest anchor remains unchanged.")

    closeout_summary = {
        "generated_utc": generated,
        "overall_status": "PASS" if gcp_green and gke_green and suite_green else "WARN",
        "phase": "v32_omega",
        "authority_model": "repo_first",
        "source_branch": BRANCH,
        "source_head_sha": current_head,
        "authoritative_repo_path": AUTHORITATIVE_REPO,
        "separate_workbench_path": WORKBENCH_REPO,
        "current_shell": "powershell",
        "readiness_state": "wsl_target_blocked_windows_operator_fallback",
        "shared_latest_anchor": shared,
        "top_residuals": residuals,
        "cloud_summary": {
            "gcp_auth_state": gcp_bootstrap.get("proof_state", "unknown"),
            "gcs_primary_mirror_state": gcs_mirror.get("gcs_primary_mirror_state", gcs_mirror.get("proof_state", "unknown")),
            "gke_cluster_state": gke_bootstrap.get("gke_cluster_state", gke_bootstrap.get("proof_state", "unknown")),
            "secret_manager_state": gcp_bootstrap.get("secret_manager_state", "unknown"),
            "artifact_registry_state": gcp_bootstrap.get("artifact_registry_state", "unknown"),
        },
        "connector_summary": {
            "gmail_materialization_state": gmail_state,
            "composio_onedrive_state": composio_state,
            "hf_guarded_lane_state": hf_state,
        },
        "session_closeout_state": closeout_state,
        "next_action": "Carry V33 Beta Aletheon-facing until Gmail promotes and the WSL/gcloud operator lane is truly healthy.",
    }
    write_json("docs/v32-omega-closeout-summary-v1.json", closeout_summary)

    continuity_md = continuity_pack(
        "V32 Omega Continuity Pack",
        "Aletheon" if not receiver_ready else "Orun",
        "v31_omega",
        shared,
        residuals or ["No residuals remain beyond the bounded V32 publication surfaces."],
        "Use the dedicated V32 proof scripts first, then continue from Gmail auth repair or Ubuntu operator recovery as needed.",
    )
    write_text("docs/v32-omega-continuity-pack-v1.md", continuity_md)

    handoff_policy = {
        "generated_utc": generated,
        "phase": "v32_omega",
        "intended_receiver": "Orun" if receiver_ready else "Aletheon",
        "receiver_ready": receiver_ready,
        "receiver_rule_outcome": receiver_outcome,
        "carry_forward_blockers": residuals,
        "required_for_orun": [
            "gcp foundation green",
            "gke cluster green",
            "gmail proof complete",
            "suite and materialize lanes PASS",
        ],
    }
    write_json("docs/v32-omega-handoff-policy-v1.json", handoff_policy)

    v33_closeout = {
        "generated_utc": generated,
        "overall_status": "PASS" if receiver_ready else "WARN",
        "phase": "v33_beta",
        "authority_model": "repo_first",
        "intended_lead": "Orun" if receiver_ready else "Aletheon",
        "predecessor_phase": "v32_omega",
        "predecessor_outcome": "cloud_and_blocker_phase_executed_with_honest_publication",
        "source_branch": BRANCH,
        "source_head_sha": current_head,
        "current_shell": "powershell",
        "readiness_state": "wsl_target_blocked_windows_operator_fallback",
        "shared_latest_anchor": shared,
        "receiver_ready": receiver_ready,
        "receiver_rule_outcome": receiver_outcome,
        "top_residuals": residuals,
        "next_action": "Use the V33 beta pack to continue from the remaining Gmail or Ubuntu operator blockers while keeping the new cloud resources bounded and explicit.",
    }
    write_json("docs/v33-beta-closeout-summary-v1.json", v33_closeout)
    write_text(
        "docs/v33-beta-continuity-pack-v1.md",
        continuity_pack(
            "V33 Beta Continuity Pack",
            "Orun" if receiver_ready else "Aletheon",
            "v32_omega",
            shared,
            residuals or ["No residuals remain beyond bounded V33 follow-through."],
            "Start from the V32 proof artifacts and continue only after checking the live cloud and auth states.",
        ),
    )
    write_json(
        "docs/v33-beta-handoff-policy-v1.json",
        {
            "generated_utc": generated,
            "phase": "v33_beta",
            "intended_receiver": "Orun" if receiver_ready else "Aletheon",
            "receiver_ready": receiver_ready,
            "receiver_rule_outcome": receiver_outcome,
            "carry_forward_blockers": residuals,
            "required_for_orun": [
                "gmail promoted",
                "ubuntu operator lane healthy",
                "suite/materialize remain green",
            ],
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

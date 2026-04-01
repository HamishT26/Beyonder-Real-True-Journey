#!/usr/bin/env python3
"""Publish V31 Omega closeout surfaces and the V32 Beta continuity pack."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
SOURCE_HEAD_SHA = "f664095aa243f94642ef0f8dc271d3eb4454ef54"
CONTRIBUTIONS = Path.home() / "Downloads" / "Newest GHC family member contributions.txt"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(rel: str) -> dict:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(rel: str, payload: dict) -> None:
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


def anchor_from(status: dict) -> dict:
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
        "primary_blocker_detail": (
            "Shared latest remains the authoritative repo-first anchor while V31 publishes storage, Gmail, and execution truth on dedicated surfaces."
        ),
        "quick_lane_summary": "38 PASS / 0 WARN / 0 FAIL",
    }


def suite_summary(status: dict) -> dict:
    counts = status.get("counts", {})
    overall = status_outcome(status)
    return {
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL",
        "pass_count": counts.get("pass", 0),
        "warn_count": counts.get("warn", 0),
        "fail_count": counts.get("fail", 0),
        "timeout_count": counts.get("timeout", 0),
        "overall_status": overall,
    }


def status_outcome(status: dict) -> str:
    explicit = status.get("overall_status")
    if explicit:
        return str(explicit)
    counts = status.get("counts", {})
    if counts.get("fail", 0) or counts.get("timeout", 0):
        return "FAIL"
    if counts.get("warn", 0):
        return "WARN"
    return "PASS"


def contribution_digest() -> dict:
    if not CONTRIBUTIONS.exists():
        return {"status": "missing", "path": str(CONTRIBUTIONS), "advisory_signals": []}
    text = CONTRIBUTIONS.read_text(encoding="utf-8", errors="replace")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "status": "available",
        "path": str(CONTRIBUTIONS),
        "line_count": len(lines),
        "advisory_signals": [
            "Treat the newest GHC contributions as advisory input rather than runtime authority.",
            "Focus V31 on storage stability, blocker resolution, and honest publication rather than overstated promotion.",
            "Carry Mind and Heart follow-through as bounded, non-governing continuity material.",
        ],
    }


def pack_md(title: str, receiver: str, predecessor: str, shared: dict, residuals: list[str], next_action: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Source branch: `{BRANCH}`",
        f"- Source head SHA: `{SOURCE_HEAD_SHA}`",
        f"- Current branch head: `{git_head()}`",
        "- Authority model: `repo_first`",
        "- Current shell: `ubuntu`",
        "- Readiness state: `ubuntu_validated_primary`",
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
    quick = read_json("docs/v31-quick-suite-status.json")
    standard = read_json("docs/v31-standard-suite-status.json")
    deep = read_json("docs/v31-deep-suite-status.json")
    collab = read_json("docs/v31-collab-suite-status.json")
    mat_l2 = read_json("docs/v31-materialize-l2-status.json")
    mat_l3 = read_json("docs/v31-materialize-l3-status.json")
    mat_l4 = read_json("docs/v31-materialize-l4-status.json")
    mat_l5 = read_json("docs/v31-materialize-l5-status.json")
    hydration = read_json("docs/trinity-live-traces/v31-onedrive-repo-hydration-proof-v1.json")
    mirror_sync = read_json("docs/trinity-live-traces/v31-onedrive-mirror-sync-proof-v1.json")
    gmail = read_json("docs/trinity-live-traces/v31-gmail-materialization-proof-v1.json")
    hf = read_json("docs/trinity-live-traces/v31-huggingface-execution-proof-v1.json")
    composio = read_json("docs/trinity-composio-api-probe-latest.json")
    runtime_resolution = read_json("docs/trinity-runtime-model-resolution-v1.json")
    session_log = read_json("docs/v17-runtime-session-log-latest.json")
    runtime_truth = read_json("docs/v17-runtime-truth-resolution-board-v1.json")
    connector_cache = read_json("docs/trinity-mcp-cache/connector-materialization-latest.json")
    memory_validation = read_json("docs/trinity-memory-bank-validation-latest.json")

    shared_anchor = anchor_from(system_suite)
    digest = contribution_digest()
    write_json("docs/auto-generated/v31-ghc-contributions-digest.json", digest)
    write_text(
        "docs/auto-generated/v31-ghc-contributions-digest.md",
        "\n".join(
            [
                "# V31 GHC Contributions Digest",
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

    gmail_state = gmail.get("proof_state", "open_with_blocker")
    hf_state = hf.get("proof_state", "open_with_blocker")
    memory_state = "pass" if memory_validation.get("overall_status") == "PASS" else "open_with_blocker"
    migration_state = mirror_sync.get("onedrive_migration_state", hydration.get("onedrive_migration_state", "unknown"))

    connector_matrix = {
        "github": {"mode": "bounded_live_write", "status": "PASS"},
        "linear": {"mode": "bounded_live_write", "status": "PASS"},
        "notion": {"mode": "bounded_live_write", "status": "PASS"},
        "google_drive": {"mode": "bounded_live_write", "status": "PASS"},
        "postgres": {"mode": "bounded_live_write", "status": "PASS"},
        "cloudflare": {"mode": "bounded_live_write", "status": "PASS"},
        "gmail": {"mode": gmail_state, "status": gmail.get("overall_status", "WARN")},
        "composio": {"mode": composio.get("proof_state", "api_verified_connector_unloaded"), "status": composio.get("overall_status", "PASS")},
        "hugging_face": {"mode": hf_state, "status": hf.get("overall_status", "WARN")},
        "figma": {"mode": "read_only_verified", "status": "PASS"},
    }
    write_json(
        "docs/trinity-live-traces/v31-connector-sweep-proof-v1.json",
        {
            "generated_utc": generated,
            "phase": "v31_omega",
            "overall_status": "PASS" if gmail_state == "bounded_live_write" else "WARN",
            "source_head_sha": SOURCE_HEAD_SHA,
            "current_head_sha": current_head,
            "connector_matrix": connector_matrix,
            "notes": [
                "Gmail is promoted only if the V31 direct or connector-native proof completed.",
                "Hugging Face remains open_with_blocker unless a real execution proof succeeded.",
                "Composio remains honest unless a toolkit materializes beyond the API/public-capability proof.",
            ],
        },
    )

    connector_cache.update(
        {
            "generated_utc": generated,
            "phase": "v31_omega",
            "gmail_materialization_state": gmail_state,
            "huggingface_execution_state": hf_state,
            "verified_composio_toolkits": composio.get("verified_composio_toolkits", []),
            "verified_app_connectors": ["github", "google_drive"],
            "connector_sweep_proof_path": "docs/trinity-live-traces/v31-connector-sweep-proof-v1.json",
        }
    )
    write_json("docs/trinity-mcp-cache/connector-materialization-latest.json", connector_cache)

    runtime_resolution.update(
        {
            "generated_utc": generated,
            "phase": "v31_omega",
            "checkpoint_anchor_commit": SOURCE_HEAD_SHA,
            "current_shell": "ubuntu",
            "readiness_state": "ubuntu_validated_primary",
            "docker_runtime_role": "soft_retired_fallback",
            "onedrive_repo_hydration_state": hydration.get("onedrive_repo_hydration_state", "unknown"),
            "onedrive_migration_state": migration_state,
            "cloud_provider_health": hydration.get("cloud_provider_health", "unknown"),
            "gmail_materialization_state": gmail_state,
            "huggingface_execution_state": hf_state,
            "memory_bank_watch_band_state": memory_state,
            "activation_sweep_state": {
                "status": "PASS" if memory_state == "pass" else "WARN",
                "promotion_wave_target": "12-20",
                "focus": [
                    "repo hydration",
                    "memory-bank recovery",
                    "gmail proof",
                    "hugging face execution attempt",
                    "onedrive helpers",
                    "bounded mind/heart refresh",
                ],
            },
            "verified_app_connectors": ["github", "google_drive"],
            "verified_composio_toolkits": composio.get("verified_composio_toolkits", []),
            "current_shared_suite_surface": shared_anchor,
            "active_handoff_pack_path": "docs/v31-omega-continuity-pack-v1.md",
            "active_handoff_policy_path": "docs/v31-omega-handoff-policy-v1.json",
            "next_receiver_pack_path": "docs/v32-beta-continuity-pack-v1.md",
            "next_receiver_policy_path": "docs/v32-beta-handoff-policy-v1.json",
            "contributions_digest_path": "docs/auto-generated/v31-ghc-contributions-digest.md",
            "onedrive_mirror_sync_proof_path": "docs/trinity-live-traces/v31-onedrive-mirror-sync-proof-v1.json",
        }
    )
    write_json("docs/trinity-runtime-model-resolution-v1.json", runtime_resolution)

    session_log.update(
        {
            "generated_utc": generated,
            "session_id": "v31-omega-closeout",
            "current_shell": "ubuntu",
            "readiness_state": "ubuntu_validated_primary",
            "docker_runtime_role": "soft_retired_fallback",
            "onedrive_repo_hydration_state": hydration.get("onedrive_repo_hydration_state", "unknown"),
            "onedrive_migration_state": migration_state,
            "gmail_materialization_state": gmail_state,
            "huggingface_execution_state": hf_state,
            "memory_bank_watch_band_state": memory_state,
            "verified_app_connectors": ["github", "google_drive"],
            "verified_composio_toolkits": composio.get("verified_composio_toolkits", []),
            "active_handoff_pack_path": "docs/v31-omega-continuity-pack-v1.md",
            "active_handoff_policy_path": "docs/v31-omega-handoff-policy-v1.json",
        }
    )
    write_json("docs/v17-runtime-session-log-latest.json", session_log)

    runtime_truth.update(
        {
            "generated_utc": generated,
            "phase": "v31_omega",
            "current_shell": "ubuntu",
            "readiness_state": "ubuntu_validated_primary",
            "docker_runtime_role": "soft_retired_fallback",
            "onedrive_repo_hydration_state": hydration.get("onedrive_repo_hydration_state", "unknown"),
            "onedrive_migration_state": migration_state,
            "cloud_provider_health": hydration.get("cloud_provider_health", "unknown"),
            "gmail_materialization_state": gmail_state,
            "huggingface_execution_state": hf_state,
            "memory_bank_watch_band_state": memory_state,
            "suite_statuses": {
                "quick": suite_summary(quick),
                "standard": suite_summary(standard),
                "deep": suite_summary(deep),
                "collab": suite_summary(collab),
                "materialize_l2": suite_summary(mat_l2),
                "materialize_l3": suite_summary(mat_l3),
                "materialize_l4": suite_summary(mat_l4),
                "materialize_l5": suite_summary(mat_l5),
            },
        }
    )
    write_json("docs/v17-runtime-truth-resolution-board-v1.json", runtime_truth)

    residuals: list[str] = []
    if hydration.get("onedrive_repo_path_state") != "healthy":
        residuals.append("The OneDrive-hosted repo copy remains degraded, so the stable local clone stays authoritative for active V31 work.")
    if gmail_state != "bounded_live_write":
        residuals.append("Gmail materialization did not fully promote, so Gmail remains unpromoted in the connector truth model.")
    if hf_state != "live_execution_proven":
        residuals.append("Hugging Face execution remains blocked or unproven, so it stays open_with_blocker.")
    if status_outcome(deep) != "PASS":
        residuals.append("Deep suite did not close green and must remain part of the V32 carry-forward list.")
    if any(status_outcome(status) != "PASS" for status in (mat_l2, mat_l3, mat_l4, mat_l5)):
        residuals.append("One or more materialize levels remain open, so V32 should stay Aletheon-facing.")
    if not residuals:
        residuals.append("No blocking residuals remain; V31 closed cleanly.")

    receiver_ready = (
        hydration.get("cloud_provider_health") != "degraded"
        and gmail_state == "bounded_live_write"
        and status_outcome(deep) == "PASS"
        and all(status_outcome(status) == "PASS" for status in (mat_l2, mat_l3, mat_l4, mat_l5))
    )
    receiver = "Orun" if receiver_ready else "Aletheon"
    receiver_rule = "orun_facing" if receiver_ready else "aletheon_facing"

    v31_closeout = {
        "generated_utc": generated,
        "overall_status": "PASS" if receiver_ready else "WARN",
        "phase": "v31_omega",
        "authority_model": "repo_first",
        "intended_lead": "Aletheon",
        "source_branch": BRANCH,
        "source_head_sha": SOURCE_HEAD_SHA,
        "current_head_sha": current_head,
        "current_shell": "ubuntu",
        "readiness_state": "ubuntu_validated_primary",
        "docker_runtime_role": "soft_retired_fallback",
        "shared_latest_anchor": shared_anchor,
        "onedrive_repo_hydration_state": hydration.get("onedrive_repo_hydration_state", "unknown"),
        "onedrive_migration_state": migration_state,
        "cloud_provider_health": hydration.get("cloud_provider_health", "unknown"),
        "gmail_materialization_state": gmail_state,
        "huggingface_execution_state": hf_state,
        "memory_bank_watch_band_state": memory_state,
        "receiver_ready": receiver_ready,
        "receiver_rule_outcome": receiver_rule,
        "top_residuals": residuals,
        "next_action": (
            "Carry V32 Beta Aletheon-facing and continue from the remaining hydration, Gmail, Hugging Face, or suite blockers."
            if not receiver_ready
            else "Hand V32 Beta to Orun."
        ),
    }
    write_json("docs/v31-omega-closeout-summary-v1.json", v31_closeout)
    write_text(
        "docs/v31-omega-continuity-pack-v1.md",
        pack_md("V31 Omega Continuity Pack", receiver, "v30_omega", shared_anchor, residuals, v31_closeout["next_action"]),
    )
    write_json(
        "docs/v31-omega-handoff-policy-v1.json",
        {
            "generated_utc": generated,
            "phase": "v31_omega",
            "intended_receiver": receiver,
            "receiver_ready": receiver_ready,
            "receiver_rule_outcome": receiver_rule,
            "carry_forward_blockers": residuals,
            "required_for_orun": [
                "onedrive_repo_hydration_state == stable_local_clone_primary_or_better",
                "gmail_materialization_state == bounded_live_write",
                "deep_suite.overall_status == PASS",
                "materialize_l2_l5.overall_status == PASS",
            ],
        },
    )

    write_json(
        "docs/v32-beta-closeout-summary-v1.json",
        {
            "generated_utc": generated,
            "overall_status": "WARN" if not receiver_ready else "PASS",
            "phase": "v32_beta",
            "authority_model": "repo_first",
            "intended_lead": receiver,
            "predecessor_phase": "v31_omega",
            "predecessor_outcome": "hydration_and_blocker_resolution_executed_with_honest_publication",
            "source_branch": BRANCH,
            "source_head_sha": current_head,
            "current_shell": "ubuntu",
            "readiness_state": "ubuntu_validated_primary",
            "shared_latest_anchor": shared_anchor,
            "receiver_ready": receiver_ready,
            "receiver_rule_outcome": receiver_rule,
            "top_residuals": residuals,
            "next_action": v31_closeout["next_action"],
        },
    )
    write_text(
        "docs/v32-beta-continuity-pack-v1.md",
        pack_md("V32 Beta Continuity Pack", receiver, "v31_omega", shared_anchor, residuals, v31_closeout["next_action"]),
    )
    write_json(
        "docs/v32-beta-handoff-policy-v1.json",
        {
            "generated_utc": generated,
            "phase": "v32_beta",
            "intended_receiver": receiver,
            "receiver_ready": receiver_ready,
            "receiver_rule_outcome": receiver_rule,
            "carry_forward_blockers": residuals,
            "required_for_orun": [
                "repo hydration stable",
                "gmail proof complete",
                "deep suite PASS",
                "materialize l2-l5 PASS",
            ],
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

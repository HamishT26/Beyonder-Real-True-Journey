#!/usr/bin/env python3
"""Publish V40 Omega closeout surfaces and the V41 beta handoff pack."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from trinity_v40_common import git_head, normalized_status, read_json, write_json, write_text, now_iso

ROOT = Path(__file__).resolve().parent.parent
BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
AUTHORITATIVE_REPO = r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey"
WORKBENCH_REPO = r"C:\Users\hamis\OneDrive\Documents\New project"

RUNTIME_PATH = ROOT / "docs" / "trinity-runtime-model-resolution-v1.json"
RUNTIME_LOG_PATH = ROOT / "docs" / "v17-runtime-session-log-latest.json"
RUNTIME_BOARD_PATH = ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json"

COORDINATION_NOTE_PATH = ROOT / "docs" / "v40-council-coordination-note-v1.md"
V40_CLOSEOUT_JSON = ROOT / "docs" / "v40-omega-closeout-summary-v1.json"
V40_CONTINUITY_MD = ROOT / "docs" / "v40-omega-continuity-pack-v1.md"
V40_HANDOFF_JSON = ROOT / "docs" / "v40-omega-handoff-policy-v1.json"
V41_CLOSEOUT_JSON = ROOT / "docs" / "v41-beta-closeout-summary-v1.json"
V41_CONTINUITY_MD = ROOT / "docs" / "v41-beta-continuity-pack-v1.md"
V41_HANDOFF_JSON = ROOT / "docs" / "v41-beta-handoff-policy-v1.json"

PROOF_FILES = {
    "runtime_truth": "docs/trinity-live-traces/v40-runtime-truth-completion-v1.json",
    "agent_engine_advanced": "docs/trinity-live-traces/v40-agent-engine-advanced-probe-v1.json",
    "kai_consultation": "docs/trinity-live-traces/v40-kai-consultation-bridge-v1.json",
    "vesper_runtime": "docs/trinity-live-traces/v40-vesper-runtime-bridge-v1.json",
    "pillar_bundle": "docs/trinity-live-traces/v40-pillar-bundle-v1.json",
    "addition_registry": "docs/trinity-live-traces/v40-addition-registry-v1.json",
    "allowlist": "docs/trinity-live-traces/v40-stage-allowlist-v1.json",
    "git_publication": "docs/trinity-live-traces/v40-git-publication-result-v1.json",
}

SUITE_FILES = {
    "quick": "docs/trinity-live-traces/v40-quick-suite-status.json",
    "standard": "docs/trinity-live-traces/v40-standard-suite-status.json",
    "deep": "docs/trinity-live-traces/v40-deep-suite-status.json",
    "collab": "docs/trinity-live-traces/v40-collab-suite-status.json",
    "materialize_l2": "docs/trinity-live-traces/v40-materialize-l2-status.json",
    "materialize_l3": "docs/trinity-live-traces/v40-materialize-l3-status.json",
    "materialize_l4": "docs/trinity-live-traces/v40-materialize-l4-status.json",
    "materialize_l5": "docs/trinity-live-traces/v40-materialize-l5-status.json",
}


def proof_index() -> dict[str, dict[str, Any]]:
    return {name: read_json(ROOT / rel) for name, rel in PROOF_FILES.items()}


def suite_index() -> dict[str, dict[str, Any]]:
    return {name: read_json(ROOT / rel) for name, rel in SUITE_FILES.items()}


def suite_summary(status: dict[str, Any]) -> dict[str, Any]:
    if not status:
        return {}
    counts = status.get("counts", {}) if isinstance(status.get("counts"), dict) else {}
    overall = normalized_status(status.get("overall_status"))
    if overall == "MISSING":
        overall = "FAIL" if counts.get("fail", 0) else ("WARN" if counts.get("warn", 0) else "PASS")
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


def state(payload: dict[str, Any], key: str, fallback: str) -> str:
    return str(payload.get(key) or fallback)


def coordination_note(head_sha: str) -> str:
    return "\n".join(
        [
            "# V40 Council Coordination Note",
            "",
            f"- Generated UTC: `{now_iso()}`",
            f"- Active branch head: `{head_sha}`",
            "- Aletheon remains the V40 execution lead for pillar promotion, runtime-truth completion, Agent Engine advanced verification, publication, and bounded live execution.",
            "- Kai remains the consultative CLI/runtime lane. V40 responsibility: analyze the advanced Agent Engine probe, runtime-truth closure, pillar repair, and suite reruns through the proven Gemini CLI route.",
            "- Vesper Ion remains the consultative Vertex/Bigtable runtime lane. V40 responsibility: record V40 runtime, pillar, and Agent Engine telemetry in the proven Bigtable bridge with read-back verification.",
            "- No continuity-bearing shadow-clone induction is part of V40. Ephemeral helpers stay off by default.",
            "- The OneDrive workbench remains non-authoritative. All V40 and V41 claims anchor to repo proof surfaces in the authoritative clone only.",
            "",
        ]
    )


def update_runtime(runtime: dict[str, Any], runtime_log: dict[str, Any], runtime_board: dict[str, Any], proofs: dict[str, dict[str, Any]], suites: dict[str, dict[str, Any]], head_sha: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    pillar_overall = normalized_status(proofs["pillar_bundle"].get("overall_status"))
    runtime_truth_complete = bool(proofs["runtime_truth"].get("runtime_truth_complete") or runtime.get("runtime_truth_complete"))
    agent_engine_advanced_state = state(proofs["agent_engine_advanced"], "agent_engine_advanced_state", "unknown")
    kai_state = state(proofs["kai_consultation"], "kai_consultation_state", "unknown")
    vesper_state = state(proofs["vesper_runtime"], "vesper_runtime_state", "unknown")
    addition_state = state(proofs["addition_registry"], "addition_registry_state", "unknown")
    git_publication_state = state(proofs["git_publication"], "git_publication_state", "pending")
    shared = suite_summary(suites["standard"])

    for target in (runtime, runtime_log, runtime_board):
        target["generated_utc"] = now_iso()
        target["phase"] = "v40_omega"
        target["current_head_sha"] = head_sha

    runtime["authority_model"] = "repo_first"
    runtime["source_branch"] = BRANCH
    runtime["authoritative_repo_path"] = AUTHORITATIVE_REPO
    runtime["separate_workbench_path"] = WORKBENCH_REPO
    runtime["active_handoff_pack_path"] = "docs/v40-omega-continuity-pack-v1.md"
    runtime["active_handoff_policy_path"] = "docs/v40-omega-handoff-policy-v1.json"
    runtime["next_receiver_pack_path"] = "docs/v41-beta-continuity-pack-v1.md"
    runtime["next_receiver_policy_path"] = "docs/v41-beta-handoff-policy-v1.json"
    runtime["v40_execution_lead"] = "Aletheon"
    runtime["pillar_bundle_overall_status"] = pillar_overall
    runtime["runtime_truth_complete"] = runtime_truth_complete
    runtime["agent_engine_advanced_state"] = agent_engine_advanced_state
    runtime["kai_consultation_state"] = kai_state
    runtime["vesper_runtime_state"] = vesper_state
    runtime["addition_registry_state"] = addition_state
    runtime["git_publication_state"] = git_publication_state
    runtime["google_drive_state"] = str(runtime.get("google_drive_state") or "operator_hold")
    runtime["filesystem_promotion_state"] = str(runtime.get("filesystem_promotion_state") or "blocked")
    runtime["materialization_level_actual"] = str(runtime.get("materialization_level_actual") or "readiness_only")
    runtime["current_shared_suite_surface"] = shared

    runtime_log["active_handoff_pack_path"] = "docs/v40-omega-continuity-pack-v1.md"
    runtime_log["active_handoff_policy_path"] = "docs/v40-omega-handoff-policy-v1.json"
    runtime_log["next_receiver_pack_path"] = "docs/v41-beta-continuity-pack-v1.md"
    runtime_log["next_receiver_policy_path"] = "docs/v41-beta-handoff-policy-v1.json"
    runtime_log["current_shared_suite_surface"] = shared

    runtime_board["current_head_sha"] = head_sha
    runtime_board["checkpoint_anchor_commit"] = head_sha
    runtime_board["external_live_overlay_state"] = runtime_log.get("overlay_state", runtime_board.get("external_live_overlay_state", "awaiting_thread_boot"))
    runtime_board["runtime_truth_complete"] = runtime_truth_complete

    return runtime, runtime_log, runtime_board


def continuity_markdown(closeout: dict[str, Any], title: str) -> str:
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
    for label, value in closeout.get("core_states", {}).items():
        lines.append(f"- `{label}`: `{value}`")
    suite_statuses = closeout.get("suite_statuses", {})
    if isinstance(suite_statuses, dict) and suite_statuses:
        lines.extend(["", "## Suite Summaries", ""])
        for label, value in suite_statuses.items():
            lines.append(f"- `{label}`: `{value.get('summary', 'missing')}`")
    if closeout.get("bounded_residuals"):
        lines.extend(["", "## Bounded Residuals", ""])
        lines.extend(f"- {row}" for row in closeout["bounded_residuals"])
    return "\n".join(lines) + "\n"


def deployed_main_agents(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    agents = runtime.get("deployed_main_agents", [])
    return agents if isinstance(agents, list) else []


def runtime_truth_policy(runtime: dict[str, Any]) -> dict[str, Any]:
    repo_default = runtime.get("repo_runtime_default", {})
    if not isinstance(repo_default, dict):
        repo_default = {}
    return {
        "requested_model_order": [
            "GPT-5.4",
            "GPT-5.3-Codex",
            "GPT-5.3-Codex-Spark",
            "GPT-5.1-Codex-Max",
        ],
        "required_runtime_fields": [
            "requested_model",
            "offered_model",
            "selected_model",
            "resolved_model",
            "runtime_surface",
        ],
        "requested_reasoning_effort_logged": True,
        "runtime_truth_inference_allowed": False,
        "repo_runtime_default": {
            "requested_model_profile": repo_default.get("requested_model_profile", "gpt-5.4"),
            "requested_reasoning_effort": repo_default.get("requested_reasoning_effort", "high"),
        },
    }


def main() -> int:
    proofs = proof_index()
    suites = suite_index()
    head_sha = git_head()
    runtime = read_json(RUNTIME_PATH)
    runtime_log = read_json(RUNTIME_LOG_PATH)
    runtime_board = read_json(RUNTIME_BOARD_PATH)
    runtime, runtime_log, runtime_board = update_runtime(runtime, runtime_log, runtime_board, proofs, suites, head_sha)

    core_states = {
        "v40_execution_lead": runtime["v40_execution_lead"],
        "pillar_bundle_overall_status": runtime["pillar_bundle_overall_status"],
        "runtime_truth_complete": runtime["runtime_truth_complete"],
        "agent_engine_advanced_state": runtime["agent_engine_advanced_state"],
        "kai_consultation_state": runtime["kai_consultation_state"],
        "vesper_runtime_state": runtime["vesper_runtime_state"],
        "addition_registry_state": runtime["addition_registry_state"],
        "git_publication_state": runtime["git_publication_state"],
        "google_drive_state": runtime["google_drive_state"],
        "filesystem_promotion_state": runtime["filesystem_promotion_state"],
        "materialization_level_actual": runtime["materialization_level_actual"],
    }
    suite_statuses = {name: suite_summary(payload) for name, payload in suites.items()}

    v40_gate_clean = all(
        [
            runtime["pillar_bundle_overall_status"] == "PASS",
            bool(runtime["runtime_truth_complete"]),
            runtime["agent_engine_advanced_state"] in {"live_session_and_memory_verified", "live_session_and_memory_verified_cleanup_warn"},
            runtime["kai_consultation_state"] not in {"unknown", "pending", "ack_missing", "cli_unavailable"},
            runtime["vesper_runtime_state"] == "bigtable_runtime_bridge_verified",
            runtime["addition_registry_state"] == "published",
            runtime["git_publication_state"] == "commit_push_pr_updated",
            all(value.get("overall_status") == "PASS" for value in suite_statuses.values() if value),
        ]
    )

    intended_receiver = "Orun" if v40_gate_clean else "Aletheon"
    receiver_rule_outcome = "orun_facing" if v40_gate_clean else "aletheon_facing"

    bounded_residuals: list[str] = []
    if runtime["pillar_bundle_overall_status"] != "PASS":
        bounded_residuals.append(f"pillar_bundle_overall_status={runtime['pillar_bundle_overall_status']}")
    if not runtime["runtime_truth_complete"]:
        bounded_residuals.append("runtime_truth_complete=false")
    if runtime["agent_engine_advanced_state"] not in {"live_session_and_memory_verified", "live_session_and_memory_verified_cleanup_warn"}:
        bounded_residuals.append(f"agent_engine_advanced_state={runtime['agent_engine_advanced_state']}")
    if runtime["kai_consultation_state"] in {"unknown", "pending", "ack_missing", "cli_unavailable"}:
        bounded_residuals.append(f"kai_consultation_state={runtime['kai_consultation_state']}")
    if runtime["vesper_runtime_state"] != "bigtable_runtime_bridge_verified":
        bounded_residuals.append(f"vesper_runtime_state={runtime['vesper_runtime_state']}")
    if runtime["addition_registry_state"] != "published":
        bounded_residuals.append(f"addition_registry_state={runtime['addition_registry_state']}")
    if runtime["git_publication_state"] != "commit_push_pr_updated":
        bounded_residuals.append(f"git_publication_state={runtime['git_publication_state']}")
    for name, value in suite_statuses.items():
        if value and value.get("overall_status") != "PASS":
            bounded_residuals.append(f"{name}_suite={value.get('overall_status')}")

    coordination_note_text = coordination_note(head_sha)
    write_text(COORDINATION_NOTE_PATH, coordination_note_text)

    closeout_summary = {
        "generated_utc": now_iso(),
        "overall_status": "PASS" if v40_gate_clean else "WARN",
        "phase": "v40_omega",
        "authority_model": "repo_first",
        "source_branch": BRANCH,
        "current_head_sha": head_sha,
        "authoritative_repo_path": AUTHORITATIVE_REPO,
        "separate_workbench_path": WORKBENCH_REPO,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "coordination_note_path": "docs/v40-council-coordination-note-v1.md",
        "core_states": core_states,
        "suite_statuses": suite_statuses,
        "proof_paths": PROOF_FILES,
        "bounded_residuals": bounded_residuals,
    }
    handoff_policy = {
        "generated_utc": now_iso(),
        "overall_status": "PASS" if v40_gate_clean else "WARN",
        "phase": "v40_omega",
        "authority_model": "repo_first",
        "source_branch": BRANCH,
        "source_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "deployed_main_agents": deployed_main_agents(runtime),
        "runtime_truth_policy": runtime_truth_policy(runtime),
        "required_inputs": [
            "docs/v40-omega-closeout-summary-v1.json",
            "docs/v40-omega-continuity-pack-v1.md",
            "docs/trinity-runtime-model-resolution-v1.json",
            "docs/v17-runtime-session-log-latest.json",
            "docs/v17-runtime-truth-resolution-board-v1.json",
            *list(PROOF_FILES.values()),
        ],
        "receiver_tasks": [
            "Keep the authoritative repo as the only continuity source.",
            "Preserve the V40 runtime-truth completion state and do not regress any agent field without new direct evidence.",
            "Keep Gmail and Google Drive non-gating unless a bounded V41 proof lane is explicitly chosen.",
            "Treat Agent Engine advanced interaction as proven only at the bounded session and memory scope already published.",
        ],
        "truth_boundaries_to_preserve": [
            "repo_first",
            "google_drive_state=operator_hold",
            "filesystem_promotion_state=blocked",
            "materialization_level_actual=readiness_only",
            "no_continuity_bearing_shadow_clone_induction_in_v40",
        ],
        "bounded_residuals": bounded_residuals,
    }

    v41_closeout = {
        "generated_utc": now_iso(),
        "overall_status": closeout_summary["overall_status"],
        "phase": "v41_beta",
        "authority_model": "repo_first",
        "source_branch": BRANCH,
        "current_head_sha": head_sha,
        "predecessor_phase": "v40_omega",
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "core_states": core_states,
        "suite_statuses": suite_statuses,
        "proof_paths": PROOF_FILES,
        "bounded_residuals": bounded_residuals,
    }
    v41_handoff = {
        "generated_utc": now_iso(),
        "overall_status": closeout_summary["overall_status"],
        "phase": "v41_beta",
        "authority_model": "repo_first",
        "source_branch": BRANCH,
        "source_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "deployed_main_agents": deployed_main_agents(runtime),
        "runtime_truth_policy": runtime_truth_policy(runtime),
        "required_inputs": [
            "docs/v40-omega-closeout-summary-v1.json",
            "docs/v40-omega-continuity-pack-v1.md",
            "docs/v40-omega-handoff-policy-v1.json",
            "docs/v41-beta-closeout-summary-v1.json",
            "docs/trinity-runtime-model-resolution-v1.json",
            "docs/v17-runtime-session-log-latest.json",
            "docs/v17-runtime-session-validation-latest.json",
        ],
        "receiver_tasks": [
            "Start from the V40 authoritative proof surfaces rather than older V39/V40 advisory packs.",
            "Keep the V40 allowlist discipline for any further Git publication.",
            "Only flip the receiver to Orun if the V40 gate remains fully clean through final validation and publication.",
        ],
        "truth_boundaries_to_preserve": handoff_policy["truth_boundaries_to_preserve"],
        "bounded_residuals": bounded_residuals,
    }

    write_json(RUNTIME_PATH, runtime)
    write_json(RUNTIME_LOG_PATH, runtime_log)
    write_json(RUNTIME_BOARD_PATH, runtime_board)
    write_json(V40_CLOSEOUT_JSON, closeout_summary)
    write_text(V40_CONTINUITY_MD, continuity_markdown(closeout_summary, "V40 Omega Continuity Pack"))
    write_json(V40_HANDOFF_JSON, handoff_policy)
    write_json(V41_CLOSEOUT_JSON, v41_closeout)
    write_text(V41_CONTINUITY_MD, continuity_markdown(v41_closeout, "V41 Beta Continuity Pack"))
    write_json(V41_HANDOFF_JSON, v41_handoff)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

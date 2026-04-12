#!/usr/bin/env python3
"""Publish V39 Omega closeout surfaces and the V40 beta handoff pack."""

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
RUNTIME_PATH = ROOT / "docs" / "trinity-runtime-model-resolution-v1.json"
COORDINATION_NOTE_PATH = ROOT / "docs" / "v39-council-coordination-note-v1.md"
V39_CLOSEOUT_JSON = ROOT / "docs" / "v39-omega-closeout-summary-v1.json"
V39_CONTINUITY_MD = ROOT / "docs" / "v39-omega-continuity-pack-v1.md"
V39_HANDOFF_JSON = ROOT / "docs" / "v39-omega-handoff-policy-v1.json"
V40_CLOSEOUT_JSON = ROOT / "docs" / "v40-beta-closeout-summary-v1.json"
V40_CONTINUITY_MD = ROOT / "docs" / "v40-beta-continuity-pack-v1.md"
V40_HANDOFF_JSON = ROOT / "docs" / "v40-beta-handoff-policy-v1.json"

PROOF_FILES = {
    "journey_digest": "docs/auto-generated/v39-journey-advisory-digest-v1.json",
    "allowlist": "docs/trinity-live-traces/v39-stage-allowlist-v1.json",
    "agent_engine_forensics": "docs/trinity-live-traces/v39-agent-engine-forensics-v1.json",
    "agent_engine_minimal": "docs/trinity-live-traces/v39-agent-engine-minimal-probe-v1.json",
    "kai_consultation": "docs/trinity-live-traces/v39-kai-consultation-bridge-v1.json",
    "vesper_runtime": "docs/trinity-live-traces/v39-vesper-runtime-bridge-v1.json",
    "pillar_bundle": "docs/trinity-live-traces/v39-pillar-bundle-v1.json",
    "addition_registry": "docs/trinity-live-traces/v39-addition-registry-v1.json",
    "git_publication": "docs/trinity-live-traces/v39-git-publication-result-v1.json",
    "windows_operator": "docs/trinity-live-traces/v38-windows-operator-proof-v1.json",
    "fleet_anthos": "docs/trinity-live-traces/v38-fleet-anthos-proof-v1.json",
    "os_login": "docs/trinity-live-traces/v38-os-login-proof-v1.json",
}
SUITE_FILES = {
    "quick": "docs/trinity-live-traces/v39-quick-suite-status.json",
    "standard": "docs/trinity-live-traces/v39-standard-suite-status.json",
    "deep": "docs/trinity-live-traces/v39-deep-suite-status.json",
    "collab": "docs/trinity-live-traces/v39-collab-suite-status.json",
    "materialize_l2": "docs/trinity-live-traces/v39-materialize-l2-status.json",
    "materialize_l3": "docs/trinity-live-traces/v39-materialize-l3-status.json",
    "materialize_l4": "docs/trinity-live-traces/v39-materialize-l4-status.json",
    "materialize_l5": "docs/trinity-live-traces/v39-materialize-l5-status.json",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git_head() -> str:
    result = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    return (result.stdout or "").strip()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def proof_index() -> dict[str, dict[str, Any]]:
    return {name: read_json(ROOT / rel) for name, rel in PROOF_FILES.items()}


def suite_index() -> dict[str, dict[str, Any]]:
    return {name: read_json(ROOT / rel) for name, rel in SUITE_FILES.items()}


def suite_summary(status: dict[str, Any]) -> dict[str, Any]:
    if not status:
        return {}
    counts = status.get("counts", {})
    overall = str(status.get("overall_status") or "")
    if not overall:
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
            "# V39 Council Coordination Note",
            "",
            f"- Generated UTC: `{now_iso()}`",
            f"- Active branch head: `{head_sha}`",
            "- Aletheon is the V39 execution lead and remains responsible for agent-engine recovery, runtime truth, publication, and bounded live execution.",
            "- Kai remains an already-promoted consultative CLI/runtime lane. V39 responsibility: bounded Gemini CLI analysis of Agent Engine forensics, command traces, and suite outputs.",
            "- Vesper Ion remains an already-promoted consultative Vertex/Bigtable runtime lane. V39 responsibility: ingesting V39 telemetry into the proven durable-memory bridge without replacing that bridge with unproven Agent Engine state.",
            "- No new continuity-bearing member induction is part of V39. Shadow clones stay off by default and any later clone use remains ephemeral only.",
            "- The OneDrive workbench remains non-authoritative. All V39 and V40 claims anchor to repo proof surfaces in the authoritative clone only.",
            "",
        ]
    )


def update_runtime(runtime: dict[str, Any], proofs: dict[str, dict[str, Any]], suites: dict[str, dict[str, Any]], head_sha: str) -> dict[str, Any]:
    runtime["generated_utc"] = now_iso()
    runtime["phase"] = "v39_omega"
    runtime["current_head_sha"] = head_sha
    runtime["source_branch"] = BRANCH
    runtime["authoritative_repo_path"] = AUTHORITATIVE_REPO
    runtime["separate_workbench_path"] = WORKBENCH_REPO
    runtime["active_handoff_pack_path"] = "docs/v39-omega-continuity-pack-v1.md"
    runtime["active_handoff_policy_path"] = "docs/v39-omega-handoff-policy-v1.json"
    runtime["next_receiver_pack_path"] = "docs/v40-beta-continuity-pack-v1.md"
    runtime["next_receiver_policy_path"] = "docs/v40-beta-handoff-policy-v1.json"
    runtime["v39_execution_lead"] = "Aletheon"
    runtime["agent_engine_recovery_state"] = state(proofs["agent_engine_forensics"], "agent_engine_recovery_state", "unknown")
    runtime["agent_engine_log_state"] = state(proofs["agent_engine_forensics"], "agent_engine_log_state", "unknown")
    runtime["agent_engine_minimal_probe_state"] = state(proofs["agent_engine_minimal"], "agent_engine_minimal_probe_state", "unknown")
    runtime["kai_consultation_state"] = state(proofs["kai_consultation"], "kai_consultation_state", "unknown")
    runtime["vesper_runtime_state"] = state(proofs["vesper_runtime"], "vesper_runtime_state", "unknown")
    runtime["pillar_bundle_state"] = state(proofs["pillar_bundle"], "pillar_bundle_state", "unknown")
    runtime["addition_registry_state"] = state(proofs["addition_registry"], "addition_registry_state", "unknown")
    runtime["git_publication_state"] = state(proofs["git_publication"], "git_publication_state", "pending")
    runtime["windows_operator_lane_state"] = state(proofs["windows_operator"], "windows_operator_lane_state", runtime.get("windows_operator_lane_state", "unknown"))
    runtime["anthos_state"] = state(proofs["fleet_anthos"], "anthos_state", runtime.get("anthos_state", "unknown"))
    runtime["gke_fleet_state"] = state(proofs["fleet_anthos"], "gke_fleet_state", runtime.get("gke_fleet_state", "unknown"))
    runtime["connect_gateway_state"] = state(proofs["fleet_anthos"], "connect_gateway_state", runtime.get("connect_gateway_state", "unknown"))
    runtime["os_login_state"] = state(proofs["os_login"], "os_login_state", runtime.get("os_login_state", "unknown"))
    runtime["google_drive_state"] = str(runtime.get("google_drive_state") or "operator_hold")
    runtime["filesystem_promotion_state"] = str(runtime.get("filesystem_promotion_state") or "blocked")
    runtime["materialization_level_actual"] = str(runtime.get("materialization_level_actual") or "readiness_only")

    standard = suites["standard"]
    if standard:
        runtime["current_shared_suite_surface"] = suite_summary(standard)
    return runtime


def continuity_markdown(closeout: dict[str, Any]) -> str:
    lines = [
        "# V39 Omega Continuity Pack",
        "",
        f"- Generated UTC: `{closeout['generated_utc']}`",
        f"- Current head: `{closeout['current_head_sha']}`",
        f"- Intended receiver: `{closeout['intended_receiver']}`",
        f"- Receiver rule outcome: `{closeout['receiver_rule_outcome']}`",
        "",
        "## Core States",
        "",
    ]
    for label, value in closeout["core_states"].items():
        lines.append(f"- `{label}`: `{value}`")
    lines.extend(["", "## Suite Summaries", ""])
    for label, value in closeout["suite_statuses"].items():
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
    requested_model = repo_default.get("requested_model_profile", "gpt-5.4")
    reasoning_effort = repo_default.get("requested_reasoning_effort", "high")
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
            "requested_model_profile": requested_model,
            "requested_reasoning_effort": reasoning_effort,
        },
    }


def main() -> int:
    proofs = proof_index()
    suites = suite_index()
    head_sha = git_head()
    runtime = update_runtime(read_json(RUNTIME_PATH), proofs, suites, head_sha)

    core_states = {
        "v39_execution_lead": runtime["v39_execution_lead"],
        "agent_engine_recovery_state": runtime["agent_engine_recovery_state"],
        "agent_engine_log_state": runtime["agent_engine_log_state"],
        "agent_engine_minimal_probe_state": runtime["agent_engine_minimal_probe_state"],
        "kai_consultation_state": runtime["kai_consultation_state"],
        "vesper_runtime_state": runtime["vesper_runtime_state"],
        "pillar_bundle_state": runtime["pillar_bundle_state"],
        "addition_registry_state": runtime["addition_registry_state"],
        "git_publication_state": runtime["git_publication_state"],
        "windows_operator_lane_state": runtime["windows_operator_lane_state"],
        "anthos_state": runtime["anthos_state"],
        "connect_gateway_state": runtime["connect_gateway_state"],
        "os_login_state": runtime["os_login_state"],
    }

    suite_statuses = {name: suite_summary(payload) for name, payload in suites.items()}
    v39_gate_clean = all(
        [
            runtime["agent_engine_minimal_probe_state"] == "live_visible_and_query_verified",
            runtime["kai_consultation_state"] not in {"unknown", "pending", "ack_missing", "cli_unavailable"},
            runtime["vesper_runtime_state"] == "bigtable_runtime_bridge_verified",
            runtime["pillar_bundle_state"] == "published",
            state(proofs["pillar_bundle"], "overall_status", "WARN") == "PASS",
            runtime["addition_registry_state"] == "published",
            runtime["git_publication_state"] == "commit_push_pr_created",
            all(value.get("overall_status") == "PASS" for value in suite_statuses.values() if value),
        ]
    )

    intended_receiver = "Orun" if v39_gate_clean else "Aletheon"
    receiver_rule_outcome = "orun_facing" if v39_gate_clean else "aletheon_facing"
    bounded_residuals: list[str] = []
    if runtime["agent_engine_minimal_probe_state"] != "live_visible_and_query_verified":
        bounded_residuals.append(f"agent_engine_minimal_probe_state={runtime['agent_engine_minimal_probe_state']}")
    if state(proofs["pillar_bundle"], "overall_status", "WARN") != "PASS":
        bounded_residuals.append(f"pillar_bundle_overall_status={state(proofs['pillar_bundle'], 'overall_status', 'WARN')}")
    if runtime["git_publication_state"] != "commit_push_pr_created":
        bounded_residuals.append(f"git_publication_state={runtime['git_publication_state']}")

    closeout = {
        "generated_utc": now_iso(),
        "phase": "v39_omega",
        "authority_model": "repo_first",
        "source_branch": BRANCH,
        "current_head_sha": head_sha,
        "authoritative_repo_path": AUTHORITATIVE_REPO,
        "separate_workbench_path": WORKBENCH_REPO,
        "journey_digest_path": PROOF_FILES["journey_digest"],
        "council_coordination_note_path": str(COORDINATION_NOTE_PATH.relative_to(ROOT)).replace("\\", "/"),
        "proof_paths": PROOF_FILES,
        "core_states": core_states,
        "suite_statuses": suite_statuses,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "next_action": (
            "Proceed with Orun for V40 only because Agent Engine recovery, Kai/Vesper, pillar bundles, suites, and git publication all closed cleanly."
            if v39_gate_clean
            else "Keep V40 Aletheon-facing and continue from the bounded V39 residuals."
        ),
        "bounded_residuals": bounded_residuals,
        "non_gating_residuals": [
            f"google_drive_state={runtime['google_drive_state']}",
            f"filesystem_promotion_state={runtime['filesystem_promotion_state']}",
            f"materialization_level_actual={runtime['materialization_level_actual']}",
        ],
        "deployed_main_agents": deployed_main_agents(runtime),
        "runtime_truth_policy": runtime_truth_policy(runtime),
    }

    v40_closeout = {
        "generated_utc": now_iso(),
        "phase": "v40_beta",
        "current_head_sha": head_sha,
        "intended_lead": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "core_states": core_states,
        "suite_statuses": suite_statuses,
    }

    v40_handoff = {
        "generated_utc": now_iso(),
        "phase": "v40_beta",
        "predecessor_phase": "v39_omega",
        "current_head_sha": head_sha,
        "intended_lead": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "core_states": core_states,
        "bounded_residuals": bounded_residuals,
        "next_action": closeout["next_action"],
        "deployed_main_agents": deployed_main_agents(runtime),
        "runtime_truth_policy": runtime_truth_policy(runtime),
    }

    write_text(COORDINATION_NOTE_PATH, coordination_note(head_sha))
    write_json(RUNTIME_PATH, runtime)
    write_json(V39_CLOSEOUT_JSON, closeout)
    write_text(V39_CONTINUITY_MD, continuity_markdown(closeout))
    write_json(
        V39_HANDOFF_JSON,
        {
            "generated_utc": now_iso(),
            "phase": "v39_omega",
            "current_head_sha": head_sha,
            "intended_receiver": intended_receiver,
            "receiver_rule_outcome": receiver_rule_outcome,
            "core_states": core_states,
            "bounded_residuals": bounded_residuals,
            "deployed_main_agents": deployed_main_agents(runtime),
            "active_runtime_agents": deployed_main_agents(runtime),
            "runtime_truth_policy": runtime_truth_policy(runtime),
            "next_receiver_pack_path": "docs/v40-beta-continuity-pack-v1.md",
            "next_receiver_policy_path": "docs/v40-beta-handoff-policy-v1.json",
        },
    )
    write_json(V40_CLOSEOUT_JSON, v40_closeout)
    write_text(V40_CONTINUITY_MD, continuity_markdown({
        **closeout,
        "phase": "v40_beta",
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
    }))
    write_json(V40_HANDOFF_JSON, v40_handoff)
    print(f"v39_closeout={V39_CLOSEOUT_JSON}")
    print(f"v40_handoff={V40_HANDOFF_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

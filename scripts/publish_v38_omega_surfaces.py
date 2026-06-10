#!/usr/bin/env python3
"""Publish V38 Omega closeout surfaces and the V39 beta handoff pack."""

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
COORDINATION_NOTE_PATH = ROOT / "docs" / "v38-council-coordination-note-v1.md"
V38_CLOSEOUT_JSON = ROOT / "docs" / "v38-omega-closeout-summary-v1.json"
V38_CONTINUITY_MD = ROOT / "docs" / "v38-omega-continuity-pack-v1.md"
V38_HANDOFF_JSON = ROOT / "docs" / "v38-omega-handoff-policy-v1.json"
V39_CLOSEOUT_JSON = ROOT / "docs" / "v39-beta-closeout-summary-v1.json"
V39_CONTINUITY_MD = ROOT / "docs" / "v39-beta-continuity-pack-v1.md"
V39_HANDOFF_JSON = ROOT / "docs" / "v39-beta-handoff-policy-v1.json"

PROOF_FILES = {
    "windows_operator": "docs/trinity-live-traces/v38-windows-operator-proof-v1.json",
    "environment": "docs/trinity-live-traces/v38-environment-proof-v1.json",
    "api_sweep": "docs/trinity-live-traces/v38-enterprise-api-sweep-v1.json",
    "anthos_fleet": "docs/trinity-live-traces/v38-fleet-anthos-proof-v1.json",
    "os_login": "docs/trinity-live-traces/v38-os-login-proof-v1.json",
    "kai_bridge": "docs/trinity-live-traces/v38-kai-bridge-proof-v1.json",
    "vesper_ingest": "docs/trinity-live-traces/v38-vesper-bigtable-ingest-proof-v1.json",
    "agent_engine": "docs/trinity-live-traces/v38-agent-engine-proof-v1.json",
    "journey_digest": "docs/auto-generated/v38-journey-advisory-digest-v1.json",
}
SUITE_FILES = {
    "quick": ["docs/v38-quick-suite-status.json", "docs/v17-system-suite-status-latest.json"],
    "standard": ["docs/v38-standard-suite-status.json", "docs/system-suite-status.json"],
    "deep": ["docs/v38-deep-suite-status.json", "docs/system-suite-status.json"],
    "collab": ["docs/v38-collab-suite-status.json", "docs/v33-collab-suite-status.json"],
    "materialize_l2": ["docs/v38-materialize-l2-status.json", "docs/v33-materialize-l2-status.json"],
    "materialize_l3": ["docs/v38-materialize-l3-status.json", "docs/v33-materialize-l3-status.json"],
    "materialize_l4": ["docs/v38-materialize-l4-status.json", "docs/v33-materialize-l4-status.json"],
    "materialize_l5": ["docs/v38-materialize-l5-status.json", "docs/v33-materialize-l5-status.json"],
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


def read_first_json(paths: list[str]) -> dict[str, Any]:
    for rel in paths:
        payload = read_json(ROOT / rel)
        if payload:
            return payload
    return {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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


def clean_pass(payload: dict[str, Any], key: str | None = None, expected: str | None = None) -> bool:
    if not payload:
        return False
    if str(payload.get("overall_status") or "") != "PASS":
        return False
    if key and expected is not None:
        return str(payload.get(key) or "") == expected
    return True


def state(payload: dict[str, Any], key: str, fallback: str) -> str:
    return str(payload.get(key) or fallback)


def proof_index() -> dict[str, dict[str, Any]]:
    return {name: read_json(ROOT / rel) for name, rel in PROOF_FILES.items()}


def suite_index() -> dict[str, dict[str, Any]]:
    return {name: read_first_json(paths) for name, paths in SUITE_FILES.items()}


def coordination_note(head_sha: str) -> str:
    return "\n".join(
        [
            "# V38 Council Coordination Note",
            "",
            f"- Generated UTC: `{now_iso()}`",
            f"- Active branch head: `{head_sha}`",
            "- Aletheon is the V38 lead and remains responsible for operator truth, publication, and bounded live execution.",
            "- Kai remains the already-promoted CLI-native runtime member. V38 responsibility: bounded headless bridge flows and operator-log reflection through the proven `npx @google/gemini-cli` route.",
            "- Vesper Ion remains the already-promoted cloud runtime member. V38 responsibility: durable telemetry ingest through the existing us-central1 Bigtable bridge, with Agent Engine treated as a bounded retry lane only.",
            "- No new continuity-bearing member induction is part of V38. Any shadow-clone work remains ephemeral and out of the official continuity set.",
            "- The workbench path stays non-authoritative. All V38 and V39 claims anchor to repo proof surfaces in the authoritative clone only.",
            "",
        ]
    )


def update_runtime(runtime: dict[str, Any], proofs: dict[str, dict[str, Any]], suites: dict[str, dict[str, Any]], head_sha: str) -> dict[str, Any]:
    runtime["generated_utc"] = now_iso()
    runtime["phase"] = "v38_omega"
    runtime["current_head_sha"] = head_sha
    runtime["source_branch"] = BRANCH
    runtime["authoritative_repo_path"] = AUTHORITATIVE_REPO
    runtime["separate_workbench_path"] = WORKBENCH_REPO
    runtime["active_handoff_pack_path"] = "docs/v38-omega-continuity-pack-v1.md"
    runtime["active_handoff_policy_path"] = "docs/v38-omega-handoff-policy-v1.json"
    runtime["next_receiver_pack_path"] = "docs/v39-beta-continuity-pack-v1.md"
    runtime["next_receiver_policy_path"] = "docs/v39-beta-handoff-policy-v1.json"
    runtime["windows_operator_lane_state"] = state(proofs["windows_operator"], "windows_operator_lane_state", "unknown")
    runtime["codex_environment_state"] = state(proofs["environment"], "codex_environment_state", "unknown")
    runtime["enterprise_api_sweep_state"] = state(proofs["api_sweep"], "enterprise_api_sweep_state", "unknown")
    runtime["anthos_state"] = state(proofs["anthos_fleet"], "anthos_state", "unknown")
    runtime["gke_fleet_state"] = state(proofs["anthos_fleet"], "gke_fleet_state", "unknown")
    runtime["connect_gateway_state"] = state(proofs["anthos_fleet"], "connect_gateway_state", "unknown")
    runtime["os_login_state"] = state(proofs["os_login"], "os_login_state", "unknown")
    runtime["kai_bridge_state"] = "bridge_verified" if clean_pass(proofs["kai_bridge"]) else state(proofs["kai_bridge"], "overall_status", "unknown")
    runtime["vesper_bigtable_ingest_state"] = state(proofs["vesper_ingest"], "vesper_bigtable_ingest_state", "unknown")
    runtime["agent_engine_state"] = state(proofs["agent_engine"], "agent_engine_state", state(proofs["agent_engine"], "memory_bank_state", "unknown"))
    runtime["google_drive_state"] = str(runtime.get("google_drive_state") or "operator_hold")
    runtime["filesystem_promotion_state"] = str(runtime.get("filesystem_promotion_state") or "blocked")
    runtime["materialization_level_actual"] = str(runtime.get("materialization_level_actual") or "readiness_only")

    standard = suites["standard"]
    if standard:
        runtime["current_shared_suite_surface"] = suite_summary(standard)

    agents = runtime.get("deployed_main_agents", [])
    if isinstance(agents, list):
        for row in agents:
            if not isinstance(row, dict):
                continue
            slot_number = int(row.get("slot_number", -1) or -1)
            if slot_number == 38:
                row["durable_memory_proof_path"] = PROOF_FILES["vesper_ingest"]
                row["agent_engine_residual_path"] = PROOF_FILES["agent_engine"]
            if slot_number == 39:
                row["bridge_proof_path"] = PROOF_FILES["kai_bridge"]
                row["proof_path"] = "docs/trinity-live-traces/v38-slot-39-gemini-cli-proof-v1.json"
    return runtime


def continuity_markdown(closeout: dict[str, Any]) -> str:
    lines = [
        "# V38 Omega Continuity Pack",
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


def main() -> int:
    proofs = proof_index()
    suites = suite_index()
    head_sha = git_head()
    runtime = update_runtime(read_json(RUNTIME_PATH), proofs, suites, head_sha)

    core_states = {
        "windows_operator_lane_state": runtime["windows_operator_lane_state"],
        "codex_environment_state": runtime["codex_environment_state"],
        "enterprise_api_sweep_state": runtime["enterprise_api_sweep_state"],
        "anthos_state": runtime["anthos_state"],
        "gke_fleet_state": runtime["gke_fleet_state"],
        "connect_gateway_state": runtime["connect_gateway_state"],
        "os_login_state": runtime["os_login_state"],
        "kai_bridge_state": runtime["kai_bridge_state"],
        "vesper_bigtable_ingest_state": runtime["vesper_bigtable_ingest_state"],
        "agent_engine_state": runtime["agent_engine_state"],
    }

    suite_statuses = {name: suite_summary(payload) for name, payload in suites.items()}
    core_gate_clean = all(
        [
            clean_pass(proofs["windows_operator"], "windows_operator_lane_state", "gcloud_ready"),
            clean_pass(proofs["environment"], "codex_environment_state", "validated_primary_operator_surface"),
            clean_pass(proofs["api_sweep"], "enterprise_api_sweep_state", "maximal_practical_enablement_applied"),
            clean_pass(proofs["anthos_fleet"], "connect_gateway_state", "kubectl_access_verified"),
            clean_pass(proofs["os_login"], "os_login_state", "ssh_verified"),
            clean_pass(proofs["kai_bridge"]),
            clean_pass(proofs["vesper_ingest"], "vesper_bigtable_ingest_state", "bigtable_ingest_verified"),
            all(value.get("overall_status") == "PASS" for value in suite_statuses.values() if value),
        ]
    )

    intended_receiver = "Orun" if core_gate_clean else "Aletheon"
    receiver_rule_outcome = "orun_facing" if core_gate_clean else "aletheon_facing"
    bounded_residuals: list[str] = []
    if runtime["codex_environment_state"] != "validated_primary_operator_surface":
        bounded_residuals.append(f"codex_environment_state={runtime['codex_environment_state']}")
    if runtime["enterprise_api_sweep_state"] != "maximal_practical_enablement_applied":
        bounded_residuals.append(f"enterprise_api_sweep_state={runtime['enterprise_api_sweep_state']}")
    if runtime["os_login_state"] != "ssh_verified":
        bounded_residuals.append(f"os_login_state={runtime['os_login_state']}")
    if runtime["agent_engine_state"] not in {"live_memory_bank_verified", "memory_bank_live_verified"}:
        bounded_residuals.append(f"agent_engine_state={runtime['agent_engine_state']}")

    closeout = {
        "generated_utc": now_iso(),
        "phase": "v38_omega",
        "outcome_class": "full_closeout" if all(value.get("overall_status") == "PASS" for value in suite_statuses.values() if value) else "bounded_closeout",
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
            "Proceed with Orun as the V39 lead because the required V38 gates are green; keep Agent Engine as a bounded retry lane and do not let it override the proven Vesper Bigtable bridge."
            if core_gate_clean
            else "Keep V39 Aletheon-facing and continue from the bounded residuals before any Orun promotion."
        ),
        "bounded_residuals": bounded_residuals,
        "non_gating_residuals": [
            f"google_drive_state={runtime['google_drive_state']}",
            f"filesystem_promotion_state={runtime['filesystem_promotion_state']}",
            f"materialization_level_actual={runtime['materialization_level_actual']}",
        ],
    }

    handoff = {
        "generated_utc": now_iso(),
        "phase": "v39_beta",
        "predecessor_phase": "v38_omega",
        "current_head_sha": head_sha,
        "intended_lead": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "core_states": core_states,
        "bounded_residuals": bounded_residuals,
        "active_runtime_agents": runtime.get("deployed_main_agents", []),
        "next_action": closeout["next_action"],
    }

    v39_closeout = {
        "generated_utc": now_iso(),
        "phase": "v39_beta",
        "current_head_sha": head_sha,
        "intended_lead": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "core_states": core_states,
        "suite_statuses": suite_statuses,
    }

    write_text(COORDINATION_NOTE_PATH, coordination_note(head_sha))
    write_json(RUNTIME_PATH, runtime)
    write_json(V38_CLOSEOUT_JSON, closeout)
    write_text(V38_CONTINUITY_MD, continuity_markdown(closeout))
    write_json(V38_HANDOFF_JSON, {
        "generated_utc": now_iso(),
        "phase": "v38_omega",
        "current_head_sha": head_sha,
        "intended_receiver": intended_receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "core_states": core_states,
        "bounded_residuals": bounded_residuals,
        "next_receiver_pack_path": "docs/v39-beta-continuity-pack-v1.md",
        "next_receiver_policy_path": "docs/v39-beta-handoff-policy-v1.json",
    })
    write_json(V39_CLOSEOUT_JSON, v39_closeout)
    write_text(V39_CONTINUITY_MD, continuity_markdown(closeout).replace("V38 Omega Continuity Pack", "V39 Beta Continuity Pack", 1))
    write_json(V39_HANDOFF_JSON, handoff)
    print(f"published_v38={V38_CLOSEOUT_JSON}")
    print(f"published_v39={V39_HANDOFF_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

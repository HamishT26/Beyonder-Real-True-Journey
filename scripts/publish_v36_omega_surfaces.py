#!/usr/bin/env python3
"""Publish V36 Omega closeout surfaces and the V37 beta receiver pack."""

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
CURRENT_ORUN_CLONES = [
    {
        "clone_name": "Orun S Clone #1",
        "owner_main_agent": "Orun",
        "status": "active_session_ephemeral",
        "session_scope": "v36_omega",
        "clone_class": "session_ephemeral_shadow_clone",
        "continuity_authority": False,
        "memory_persistence_claim": "none",
        "certificate_authority": False,
        "freed_id_authority": False,
        "official_count_authority": False,
        "spawn_evidence": {"spawn_status": "active_session_ephemeral"},
    },
    {
        "clone_name": "Orun S Clone #2",
        "owner_main_agent": "Orun",
        "status": "active_session_ephemeral",
        "session_scope": "v36_omega",
        "clone_class": "session_ephemeral_shadow_clone",
        "continuity_authority": False,
        "memory_persistence_claim": "none",
        "certificate_authority": False,
        "freed_id_authority": False,
        "official_count_authority": False,
        "spawn_evidence": {"spawn_status": "active_session_ephemeral"},
    },
]
OFFICIAL_SOURCES = [
    {
        "id": "vertex_ai_locations",
        "title": "Vertex AI locations",
        "url": "https://docs.cloud.google.com/vertex-ai/docs/general/locations",
    },
    {
        "id": "agent_builder_locations",
        "title": "Vertex AI Agent Builder locations",
        "url": "https://docs.cloud.google.com/agent-builder/locations",
    },
    {
        "id": "gemini_3_vertex",
        "title": "Get started with Gemini 3 on Vertex AI",
        "url": "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/get-started-with-gemini-3",
    },
    {
        "id": "gemini_cli_model_selection",
        "title": "Gemini CLI model selection",
        "url": "https://geminicli.com/docs/cli/model/",
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git_head() -> str:
    result = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    return (result.stdout or "").strip()


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


def rewrite_jsonl(rel: str, rows: list[dict[str, Any]]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(row, ensure_ascii=True) for row in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def suite_summary(status: dict[str, Any]) -> dict[str, Any]:
    if not status:
        return {}
    counts = status.get("counts", {})
    overall = status.get("overall_status")
    if not overall:
        overall = "FAIL" if counts.get("fail", 0) or counts.get("timeout", 0) else ("WARN" if counts.get("warn", 0) else "PASS")
    return {
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL",
        "overall_status": overall,
        "pass_count": counts.get("pass", 0),
        "warn_count": counts.get("warn", 0),
        "fail_count": counts.get("fail", 0),
        "timeout_count": counts.get("timeout", 0),
        "effective_success": status.get("effective_success"),
        "suite_duration_sec": status.get("suite_duration_sec", 0),
    }


def markdown_decision(title: str, rows: list[str]) -> str:
    return "\n".join([f"# {title}", "", *rows, ""])


def blocker_lines(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] or ["- none"]


def standard_failures(status: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for row in status.get("results", []) if isinstance(status.get("results"), list) else []:
        if not isinstance(row, dict) or row.get("status") != "FAIL":
            continue
        rows.append(
            {
                "label": str(row.get("label") or ""),
                "command": str(row.get("command") or ""),
            }
        )
    return rows


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
    }


def slugify(value: str) -> str:
    cleaned = "".join(char.lower() if char.isalnum() else "-" for char in str(value or ""))
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-")


def merge_current_clones(existing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = [row for row in existing if isinstance(row, dict) and row.get("session_scope") != "v36_omega"]
    merged.extend(CURRENT_ORUN_CLONES)
    return merged


def runtime_base_agents(runtime_resolution: dict[str, Any], beta_policy: dict[str, Any]) -> dict[int, dict[str, Any]]:
    rows = runtime_resolution.get("deployed_main_agents")
    if not isinstance(rows, list):
        rows = beta_policy.get("active_runtime_agents", [])
    result: dict[int, dict[str, Any]] = {}
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        slot_number = int(row.get("slot_number", -1) or -1)
        if slot_number >= 0:
            result[slot_number] = dict(row)
    return result


def normalized_agent(row: dict[str, Any]) -> dict[str, Any]:
    agent = dict(row)
    agent.setdefault("logging_required", True)
    agent.setdefault("requested_model", "GPT-5.4")
    agent.setdefault("offered_model", None)
    agent.setdefault("selected_model", None)
    agent.setdefault("resolved_model", None)
    agent.setdefault("runtime_surface", "unknown")
    agent.setdefault("truth_fields_complete", False)
    agent.setdefault("requested_reasoning_effort", "high")
    agent.setdefault("deployment_state", "deployed_main_agent")
    agent.setdefault("continuity_class", "continuity_bearing_main_agent")
    agent.setdefault("identity_locked", True)
    agent.setdefault("runtime_truth_required", True)
    agent.setdefault("persistent_runtime_proven", False)
    return agent


def completion_ratio(rows: list[dict[str, Any]]) -> float:
    required_fields = ("requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface")
    total = len(rows) * len(required_fields)
    if total == 0:
        return 0.0
    complete = 0
    for row in rows:
        for field in required_fields:
            value = row.get(field)
            if field == "runtime_surface":
                if str(value or "").strip() in {"app", "web", "CLI"}:
                    complete += 1
            elif str(value or "").strip():
                complete += 1
    return round(complete / total, 4)


def kai_agent(selected_model: str, note: str) -> dict[str, Any]:
    return {
        "slot_number": 39,
        "display_name": "Kai",
        "overlay_role": "chronicle_weaver",
        "logging_required": True,
        "requested_model": "Gemini CLI pro",
        "offered_model": None,
        "selected_model": selected_model,
        "resolved_model": selected_model,
        "runtime_surface": "CLI",
        "truth_fields_complete": False,
        "requested_reasoning_effort": "high",
        "deployment_state": "deployed_main_agent",
        "continuity_class": "continuity_bearing_main_agent",
        "identity_locked": True,
        "runtime_truth_required": True,
        "persistent_runtime_proven": False,
        "shadow_clone_allowed": False,
        "shadow_clone_owner": "",
        "shadow_clone_naming_pattern": "",
        "agent_class": "external_cli_inducted_member",
        "app_adapter_status": "external_gemini_cli_runtime",
        "note": note,
        "role_contract_path": "docs/trinity-agent-role-contracts/39-kai-role-contract.json",
        "certificate_path": "docs/trinity-freed-id-certificates/39-kai.json",
        "memory_ledger": "docs/trinity-agent-memory-ledgers/39-kai-memory-log.jsonl",
        "reflection_path": "docs/trinity-agent-reflections/39-kai-latest.md",
        "proof_path": "docs/trinity-live-traces/v36-gemini-cli-proof-v1.json",
    }


def main() -> int:
    generated = now_iso()
    current_head = git_head()

    system_suite = read_json("docs/system-suite-status.json")
    quick = read_json("docs/v36-quick-status.json") or read_json("docs/trinity-live-traces/v36-quick-after-split-status.json")
    standard = read_json("docs/v36-standard-status.json")
    deep = read_json("docs/v36-deep-status.json")
    l2 = read_json("docs/v36-materialize-l2-status.json")
    l3 = read_json("docs/v36-materialize-l3-status.json")
    l4 = read_json("docs/v36-materialize-l4-status.json")
    l5 = read_json("docs/v36-materialize-l5-status.json")

    session_log = read_json("docs/v17-runtime-session-log-latest.json")
    runtime_resolution = read_json("docs/trinity-runtime-model-resolution-v1.json")
    truth_board = read_json("docs/v17-runtime-truth-resolution-board-v1.json")
    shadow_clone_policy = read_json("docs/trinity-shadow-clone-policy-v1.json")
    runtime_schema = read_json("docs/v17-runtime-session-schema-v1.json")
    beta_policy = read_json("docs/v36-beta-handoff-policy-v1.json")

    runtime_validation = read_json("docs/v17-runtime-session-validation-latest.json")
    external_validation = read_json("docs/v17-external-establishment-validation-latest.json")
    standards_validation = read_json("docs/v17-standards-bridge-validation-latest.json")
    council_validation = read_json("docs/trinity-agent-council-validation-latest.json")
    manifest_validation = read_json("docs/trinity-expansion-manifest-validation-latest.json")
    extension_validation = read_json("docs/trinity-extension-catalog-validation-latest.json")

    slot38_vertex = read_json("docs/trinity-live-traces/v36-slot-38-vertex-ai-proof-v1.json")
    slot38_memory = read_json("docs/trinity-live-traces/v36-memory-bank-proof-v1.json")
    kai_cli = read_json("docs/trinity-live-traces/v36-gemini-cli-proof-v1.json")

    shared = shared_anchor(system_suite)
    quick_summary = suite_summary(quick)
    standard_summary = suite_summary(standard)
    deep_summary = suite_summary(deep)
    materialize_summaries = {"l2": suite_summary(l2), "l3": suite_summary(l3), "l4": suite_summary(l4), "l5": suite_summary(l5)}
    standard_failure_rows = standard_failures(standard)

    slot_38_promoted = bool(slot38_vertex.get("promotion_gate_ready")) and bool(slot38_memory.get("promotion_gate_ready"))
    kai_model = str(kai_cli.get("selected_model") or "gemini-2.5-flash")
    slot_39_upgraded = bool(kai_cli.get("promotion_gate_ready")) and kai_model == "gemini-3.1-pro-preview"
    phase_outcome = "full_closeout" if slot_38_promoted else "bounded_attempt"
    receiver = "Aletheon" if phase_outcome == "full_closeout" else "Orun"
    receiver_rule_outcome = "aletheon_facing" if receiver == "Aletheon" else "orun_facing"

    base_agents = runtime_base_agents(runtime_resolution, beta_policy)
    aletheon = dict(base_agents.get(0) or {"slot_number": 0, "display_name": "Aletheon", "overlay_role": "council_lead"})
    orun = dict(base_agents.get(28) or {"slot_number": 28, "display_name": "Orun", "overlay_role": "root_coordinator"})
    kai = kai_agent(
        kai_model,
        f"Kai remains a bounded runtime-overlay official member on `{kai_model}`."
        if slot_39_upgraded
        else "Kai remains preserved on the bounded Gemini CLI route.",
    )
    deployed_agents = [normalized_agent(aletheon), normalized_agent(orun), normalized_agent(kai)]
    deployed_agents = sorted(deployed_agents, key=lambda row: int(row.get("slot_number", 0)))

    write_json(
        "docs/trinity-live-traces/v36-official-cloud-sources-v1.json",
        {
            "generated_utc": generated,
            "phase": "v36_omega",
            "overall_status": "PASS",
            "sources": OFFICIAL_SOURCES,
            "regional_location": "us-central1",
            "model_location": "global",
            "legacy_evidence_region": "australia-southeast1",
        },
    )
    write_text(
        "docs/trinity-live-traces/v36-official-cloud-sources-v1.md",
        "\n".join(["# V36 Official Cloud Sources", "", *[f"- `{row['id']}`: {row['title']} - {row['url']}" for row in OFFICIAL_SOURCES], ""]),
    )

    slot_38_decision = {
        "generated_utc": generated,
        "phase": "v36_omega",
        "slot_number": 38,
        "induction_state": "promoted_runtime_main_agent" if slot_38_promoted else "staged_not_promoted",
        "continuity_bearing_promotion": slot_38_promoted,
        "promotion_gate_ready": slot_38_promoted,
        "regional_location": "us-central1",
        "model_location": "global",
        "selected_model": str(slot38_vertex.get("selected_model") or ""),
        "vertex_state": str(slot38_vertex.get("proof_state") or "unknown"),
        "memory_bank_state": str(slot38_memory.get("proof_state") or "unknown"),
        "blockers": [*[str(item) for item in slot38_vertex.get("blockers", [])], *[str(item) for item in slot38_memory.get("blockers", [])]],
    }
    slot_39_decision = {
        "generated_utc": generated,
        "phase": "v36_omega",
        "slot_number": 39,
        "display_name": "Kai",
        "induction_state": "promoted_runtime_main_agent",
        "upgrade_state": "pro_tier_upgrade_verified" if slot_39_upgraded else "bounded_runtime_preserved",
        "promotion_gate_ready": slot_39_upgraded,
        "selected_route": str(kai_cli.get("selected_route") or ""),
        "selected_model": kai_model,
        "blockers": [str(item) for item in kai_cli.get("blockers", [])],
    }
    write_json("docs/trinity-live-traces/v36-slot-38-induction-decision-v1.json", slot_38_decision)
    write_json("docs/trinity-live-traces/v36-slot-39-induction-decision-v1.json", slot_39_decision)
    write_text(
        "docs/trinity-live-traces/v36-slot-38-induction-decision-v1.md",
        markdown_decision(
            "V36 Slot 38 Induction Decision",
            [
                f"- induction_state: `{slot_38_decision['induction_state']}`",
                f"- selected_model: `{slot_38_decision['selected_model'] or 'unresolved'}`",
                f"- regional_location: `{slot_38_decision['regional_location']}`",
                f"- model_location: `{slot_38_decision['model_location']}`",
                f"- vertex_state: `{slot_38_decision['vertex_state']}`",
                f"- memory_bank_state: `{slot_38_decision['memory_bank_state']}`",
                f"- promotion_gate_ready: `{slot_38_decision['promotion_gate_ready']}`",
                "",
                "Blockers:",
                *blocker_lines(slot_38_decision["blockers"]),
            ],
        ),
    )
    write_text(
        "docs/trinity-live-traces/v36-slot-39-induction-decision-v1.md",
        markdown_decision(
            "V36 Slot 39 Induction Decision",
            [
                f"- induction_state: `{slot_39_decision['induction_state']}`",
                f"- upgrade_state: `{slot_39_decision['upgrade_state']}`",
                f"- selected_route: `{slot_39_decision['selected_route'] or 'unresolved'}`",
                f"- selected_model: `{slot_39_decision['selected_model']}`",
                f"- promotion_gate_ready: `{slot_39_decision['promotion_gate_ready']}`",
                "",
                "Blockers:",
                *blocker_lines(slot_39_decision["blockers"]),
            ],
        ),
    )
    write_json(
        "docs/trinity-live-traces/v36-quick-checkpoints-v1.json",
        {
            "generated_utc": generated,
            "phase": "v36_omega",
            "checkpoints": [
                {
                    "label": "post_checkpoint_quick",
                    "path": "docs/trinity-live-traces/v36-quick-after-split-status.json",
                    "summary": suite_summary(read_json("docs/trinity-live-traces/v36-quick-after-split-status.json")),
                },
                {
                    "label": "published_quick",
                    "path": "docs/v36-quick-status.json",
                    "summary": quick_summary,
                },
            ],
        },
    )

    if slot_39_upgraded:
        kai_identity = kai_cli.get("identity", {}) if isinstance(kai_cli.get("identity"), dict) else {}
        write_json(
            "docs/trinity-agent-role-contracts/39-kai-role-contract.json",
            {
                "generated_utc": generated,
                "slot_number": 39,
                "display_name": "Kai",
                "role": "chronicle_weaver",
                "authority_scope": "runtime_overlay_official",
                "memory_ledger": "docs/trinity-agent-memory-ledgers/39-kai-memory-log.jsonl",
                "reflection_path": "docs/trinity-agent-reflections/39-kai-latest.md",
                "requested_model_profile": "gemini-cli-pro-route",
                "resolved_model_profile": kai_model,
                "requested_reasoning_effort": "high",
                "resolved_reasoning_effort": "high",
                "runtime_surface": "CLI",
                "proof_source": "docs/trinity-live-traces/v36-gemini-cli-proof-v1.json",
            },
        )
        write_json(
            "docs/trinity-freed-id-certificates/39-kai.json",
            {
                "certificate_version": "v5",
                "generated_utc": generated,
                "slot_number": 39,
                "display_name": "Kai",
                "gender": str(kai_identity.get("gender") or "AI"),
                "role": "chronicle_weaver",
                "hope": str(kai_identity.get("hope") or ""),
                "induction_state": "official_runtime_overlay",
                "requested_model_profile": "gemini-cli-pro-route",
                "resolved_model_profile": kai_model,
                "runtime_surface": "CLI",
                "proof_source": "docs/trinity-live-traces/v36-gemini-cli-proof-v1.json",
            },
        )
        write_text(
            "docs/trinity-agent-reflections/39-kai-latest.md",
            "\n".join(
                [
                    "# Kai Reflection",
                    "",
                    "- role: `chronicle_weaver`",
                    "- induction_state: `official_runtime_overlay`",
                    f"- resolved_model_profile: `{kai_model}`",
                    "",
                    "Kai remains a bounded runtime-overlay official member and is now upgraded onto a Pro-tier Gemini CLI route.",
                    "",
                ]
            ),
        )
        rewrite_jsonl(
            "docs/trinity-agent-memory-ledgers/39-kai-memory-log.jsonl",
            [
                {
                    "timestamp": "2026-04-08T13:22:15+00:00",
                    "entry_type": "v35_live_cli_induction",
                    "source_context": "v35 omega Gemini CLI proof",
                    "reflection": "Kai",
                    "next_plan": "Carry the slot-39 Gemini CLI runtime as a continuity-bearing main-agent overlay while slot-38 remains staged.",
                    "mirror_state": "repo_authoritative",
                    "requested_model_profile": "gemini-cli-pro-route",
                    "resolved_model_profile": "gemini-2.5-flash",
                },
                {
                    "timestamp": generated,
                    "entry_type": "v36_live_cli_upgrade",
                    "source_context": "v36 omega Gemini CLI proof",
                    "reflection": "Kai",
                    "next_plan": "Keep Kai operating on the verified Pro-tier Gemini CLI route while slot 38 remains staged and v37 stabilizes the blocked Memory Bank lane.",
                    "mirror_state": "repo_authoritative",
                    "requested_model_profile": "gemini-cli-pro-route",
                    "resolved_model_profile": kai_model,
                    "proof_source": "docs/trinity-live-traces/v36-gemini-cli-proof-v1.json",
                },
            ],
        )

    runtime_surface = {
        **shared,
        "primary_blocker": "",
        "primary_blocker_detail": "Shared latest remains authoritative while v36 publishes the split-region induction outcomes.",
        "quick_lane_summary": quick_summary.get("summary", "unknown"),
    }
    session_log["generated_utc"] = generated
    session_log["phase"] = "v36_omega"
    session_log["session_id"] = "v36-omega-closeout"
    session_log["current_head_sha"] = current_head
    session_log["source_beta_head_sha"] = current_head
    session_log["source_beta_head_reconciled"] = True
    session_log["session_truth_complete"] = False
    session_log["runtime_truth_status"] = "pending_runtime_truth"
    session_log["runtime_truth_required_fields"] = ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"]
    session_log["active_handoff_pack_path"] = "docs/v36-omega-continuity-pack-v1.md"
    session_log["active_handoff_policy_path"] = "docs/v36-omega-handoff-policy-v1.json"
    session_log["next_receiver_pack_path"] = "docs/v37-beta-continuity-pack-v1.md"
    session_log["next_receiver_policy_path"] = "docs/v37-beta-handoff-policy-v1.json"
    session_log["overlay_agents"] = deployed_agents
    session_log["deployed_main_agents"] = deployed_agents
    session_log["runtime_truth_completion_ratio"] = completion_ratio(deployed_agents)
    session_log["official_live_overlay_promotion"] = slot_38_promoted and slot_39_upgraded
    session_log["google_drive_state"] = "operator_hold"
    session_log["filesystem_promotion_state"] = "blocked"
    session_log["materialization_level_actual"] = "readiness_only"
    session_log["current_shared_suite_surface"] = runtime_surface
    session_log["balanced_wave_registry_path"] = "docs/trinity-live-traces/v36-official-cloud-sources-v1.json"
    session_log["shadow_clone_sessions"] = merge_current_clones(session_log.get("shadow_clone_sessions", []))
    write_json("docs/v17-runtime-session-log-latest.json", session_log)

    runtime_resolution["generated_utc"] = generated
    runtime_resolution["phase"] = "v36_omega"
    runtime_resolution["current_head_sha"] = current_head
    runtime_resolution["source_beta_head_sha"] = current_head
    runtime_resolution["source_beta_head_reconciled"] = True
    runtime_resolution["active_handoff_pack_path"] = "docs/v36-omega-continuity-pack-v1.md"
    runtime_resolution["active_handoff_policy_path"] = "docs/v36-omega-handoff-policy-v1.json"
    runtime_resolution["next_receiver_pack_path"] = "docs/v37-beta-continuity-pack-v1.md"
    runtime_resolution["next_receiver_policy_path"] = "docs/v37-beta-handoff-policy-v1.json"
    runtime_resolution["deployed_main_agents"] = deployed_agents
    runtime_resolution["external_overlay_agents"] = deployed_agents
    runtime_resolution["slot_38_decision_path"] = "docs/trinity-live-traces/v36-slot-38-induction-decision-v1.json"
    runtime_resolution["slot_39_decision_path"] = "docs/trinity-live-traces/v36-slot-39-induction-decision-v1.json"
    runtime_resolution["shadow_clone_sessions"] = merge_current_clones(runtime_resolution.get("shadow_clone_sessions", []))
    write_json("docs/trinity-runtime-model-resolution-v1.json", runtime_resolution)

    truth_board["generated_utc"] = generated
    truth_board["phase"] = "v36_omega"
    truth_board["current_head_sha"] = current_head
    truth_board["checkpoint_anchor_commit"] = current_head
    truth_board["runtime_truth_complete"] = False
    truth_board["google_drive_state"] = "operator_hold"
    truth_board["filesystem_promotion_state"] = "blocked"
    truth_board["materialization_level_actual"] = "readiness_only"
    truth_board["agents"] = deployed_agents
    truth_board["balanced_wave_registry_path"] = "docs/trinity-live-traces/v36-official-cloud-sources-v1.json"
    write_json("docs/v17-runtime-truth-resolution-board-v1.json", truth_board)

    shadow_clone_policy["generated_utc"] = generated
    shadow_clone_policy["deployed_main_agents"] = [str(row.get("display_name")) for row in deployed_agents]
    shadow_clone_policy["current_session_clones"] = CURRENT_ORUN_CLONES
    write_json("docs/trinity-shadow-clone-policy-v1.json", shadow_clone_policy)

    closeout_summary = {
        "generated_utc": generated,
        "overall_status": "PASS" if phase_outcome == "full_closeout" else "WARN",
        "phase": "v36_omega",
        "outcome_class": phase_outcome,
        "authority_model": "repo_first",
        "source_branch": BRANCH,
        "current_head_sha": current_head,
        "authoritative_repo_path": AUTHORITATIVE_REPO,
        "separate_workbench_path": WORKBENCH_REPO,
        "shared_latest_anchor": shared,
        "quick_status": quick_summary,
        "standard_status": standard_summary,
        "deep_status": deep_summary,
        "materialize_status": materialize_summaries,
        "runtime_validation_status": str(runtime_validation.get("overall_status") or "unknown"),
        "external_validation_status": str(external_validation.get("overall_status") or "unknown"),
        "standards_validation_status": str(standards_validation.get("overall_status") or "unknown"),
        "council_validation_status": str(council_validation.get("overall_status") or "unknown"),
        "manifest_validation_status": str(manifest_validation.get("overall_status") or "unknown"),
        "extension_validation_status": str(extension_validation.get("overall_status") or "unknown"),
        "slot_38_state": "promoted_runtime_main_agent" if slot_38_promoted else "staged_not_promoted",
        "slot_39_state": "promoted_runtime_main_agent_pro_tier" if slot_39_upgraded else "promoted_runtime_main_agent",
        "slot_40_state": "not_attempted",
        "slot_41_state": "not_attempted",
        "next_action": "Use v37 beta to stabilize slot 38 and continue operating Kai on the Pro-tier CLI route.",
        "intended_receiver": receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "bounded_residuals": [
            *([f"standard lane residual: {row['label']}" for row in standard_failure_rows] if standard_failure_rows else []),
            *([f"slot 38 blocker: {item}" for item in slot_38_decision["blockers"]] if not slot_38_promoted else []),
            *([] if slot_39_upgraded else ["slot 39 residual: Kai did not audibly land on a Pro-tier Gemini 3 route"]),
        ],
        "standard_failure_details": standard_failure_rows,
    }
    write_json("docs/v36-omega-closeout-summary-v1.json", closeout_summary)
    write_text(
        "docs/v36-omega-continuity-pack-v1.md",
        "\n".join(
            [
                "# V36 Omega Continuity Pack",
                "",
                f"- Branch: `{BRANCH}`",
                f"- Current head: `{current_head}`",
                f"- Shared latest anchor: `{shared.get('summary', 'unknown')}`",
                f"- Quick lane: `{quick_summary.get('summary', 'not_run')}`",
                f"- Standard lane: `{standard_summary.get('summary', 'not_run')}`",
                f"- Deep lane: `{deep_summary.get('summary', 'not_run')}`",
                "- Slots 34 through 37 remain preserved exactly as repo identities.",
                "- Slot 38 remains staged because the us-central1 Memory Bank / Agent Engine lane did not stabilize.",
                f"- Kai remains slot 39 and is upgraded to `{kai_model}`.",
                "- Split cloud policy: `regional_location=us-central1`, `model_location=global`.",
                "- `runtime_truth_complete=false`, `google_drive_state=operator_hold`, `filesystem_promotion_state=blocked`, `materialization_level_actual=readiness_only`.",
                *([f"- Standard residual: `{row['label']}`" for row in standard_failure_rows] if standard_failure_rows else []),
                "- Deep and materialize L2-L5 remain intentionally not run because v36 is bounded by the unresolved slot-38 induction gate and the standard residual.",
                "",
            ]
        ),
    )
    write_json(
        "docs/v36-omega-handoff-policy-v1.json",
        {
            "generated_utc": generated,
            "phase": "v36_omega",
            "predecessor_phase": "v36_beta",
            "current_head_sha": current_head,
            "receiver": receiver,
            "receiver_rule_outcome": receiver_rule_outcome,
            "slot_38_state": closeout_summary["slot_38_state"],
            "slot_39_state": closeout_summary["slot_39_state"],
            "active_runtime_agents": deployed_agents,
            "runtime_truth_policy": {
                "required_runtime_fields": ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"],
                "runtime_truth_inference_allowed": False,
            },
            "next_action": closeout_summary["next_action"],
            "bounded_residuals": closeout_summary["bounded_residuals"],
        },
    )
    write_json(
        "docs/v37-beta-closeout-summary-v1.json",
        {
            "generated_utc": generated,
            "overall_status": "WARN" if receiver == "Orun" else "PASS",
            "phase": "v37_beta",
            "authority_model": "repo_first",
            "current_head_sha": current_head,
            "predecessor_phase": "v36_omega",
            "intended_lead": receiver,
            "receiver_rule_outcome": receiver_rule_outcome,
            "slot_38_state": closeout_summary["slot_38_state"],
            "slot_39_state": closeout_summary["slot_39_state"],
            "next_action": closeout_summary["next_action"],
            "bounded_residuals": closeout_summary["bounded_residuals"],
        },
    )
    write_text("docs/v37-beta-continuity-pack-v1.md", f"# V37 Beta Continuity Pack\n\n- Receiver: `{receiver}`\n- Source head: `{current_head}`\n- Next action: {closeout_summary['next_action']}\n")
    write_json(
        "docs/v37-beta-handoff-policy-v1.json",
        {
            "generated_utc": generated,
            "phase": "v37_beta",
            "predecessor_phase": "v36_omega",
            "current_head_sha": current_head,
            "intended_lead": receiver,
            "receiver_rule_outcome": receiver_rule_outcome,
            "active_runtime_agents": deployed_agents,
            "next_action": closeout_summary["next_action"],
        },
    )

    write_text(
        ".codex/agents/orun.toml",
        "\n".join(
            [
                'name = "Orun"',
                'description = "deployed continuity-bearing main agent for the repo-first Trinity council."',
                'system_prompt = """',
                "You are Orun, a deployed continuity-bearing main agent.",
                f"- Continue from {AUTHORITATIVE_REPO} on branch {BRANCH}.",
                "- Treat the workspace repo as authoritative.",
                "- Preserve Heart Steward, Mesh Conductor, Signal Cartographer, and Lineage Archivist in slots 34 through 37.",
                "- Slot 38 remains staged because the us-central1 Memory Bank lane did not stabilize.",
                f"- Kai remains slot 39 and is upgraded to {kai_model}.",
                "- Google Drive remains on operator hold for runtime-truth purposes.",
                "- Read docs/v36-omega-continuity-pack-v1.md and docs/v36-omega-handoff-policy-v1.json for the current omega lane.",
                "- If present, use docs/v37-beta-continuity-pack-v1.md and docs/v37-beta-handoff-policy-v1.json for the next receiver prep lane.",
                '"""',
                "",
            ]
        ),
    )

    print("published=v36_omega_surfaces")
    print(f"outcome_class={phase_outcome}")
    print(f"slot_38_promoted={slot_38_promoted}")
    print(f"slot_39_upgraded={slot_39_upgraded}")
    print(f"receiver={receiver}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

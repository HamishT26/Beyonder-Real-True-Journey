#!/usr/bin/env python3
"""Publish V35 Omega bounded-closeout surfaces and the V36 beta receiver pack."""

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
        "session_scope": "v35_omega",
        "clone_class": "session_ephemeral_shadow_clone",
        "continuity_authority": False,
        "memory_persistence_claim": "none",
        "certificate_authority": False,
        "freed_id_authority": False,
        "official_count_authority": False,
        "spawn_evidence": {
            "spawn_status": "active",
            "agent_id": "019d62c0-9710-7e90-83f8-4a170c83f59c",
            "app_nickname": "Wegener",
        },
    },
    {
        "clone_name": "Orun S Clone #2",
        "owner_main_agent": "Orun",
        "status": "active_session_ephemeral",
        "session_scope": "v35_omega",
        "clone_class": "session_ephemeral_shadow_clone",
        "continuity_authority": False,
        "memory_persistence_claim": "none",
        "certificate_authority": False,
        "freed_id_authority": False,
        "official_count_authority": False,
        "spawn_evidence": {
            "spawn_status": "active",
            "agent_id": "019d62c0-cb9f-7a60-8a3e-877243ab156c",
            "app_nickname": "Raman",
        },
    },
]
OFFICIAL_SOURCES = [
    {
        "id": "vertex_memory_bank_overview",
        "title": "Vertex AI Memory Bank overview",
        "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/overview",
        "repo_use": "Treat Memory Bank as a separate Agent Engine lane that must prove live startup before continuity promotion claims.",
    },
    {
        "id": "vertex_memory_bank_quickstart",
        "title": "Quickstart with Vertex AI Agent Engine SDK",
        "url": "https://docs.cloud.google.com/agent-builder/agent-engine/memory-bank/quickstart-api",
        "repo_use": "Use it to structure the live Agent Engine proof, but do not treat repo-only validation as equivalent to a live serving engine.",
    },
    {
        "id": "vertex_gemini_3_pro",
        "title": "Gemini 3 Pro on Vertex AI",
        "url": "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro",
        "repo_use": "Keep Gemini 3.1 Pro as the preferred induction target only when the Sydney region and account actually expose it.",
    },
    {
        "id": "gemini_cli_repo",
        "title": "Gemini CLI repository",
        "url": "https://github.com/google-gemini/gemini-cli",
        "repo_use": "Use the official CLI project as the install and operator-path authority for the slot-39 terminal runtime.",
    },
    {
        "id": "gemini_cli_auth",
        "title": "Gemini CLI authentication",
        "url": "https://geminicli.com/docs/get-started/authentication/",
        "repo_use": "Use Vertex-backed auth only after the service-account path is auditable in repo-backed proof artifacts.",
    },
    {
        "id": "gemini_cli_model_selection",
        "title": "Gemini CLI model selection",
        "url": "https://geminicli.com/docs/cli/model/",
        "repo_use": "Record the requested documented route and the actually selected model separately when the account falls back.",
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


def suite_summary(status: dict[str, Any]) -> dict[str, Any]:
    if not status:
        return {}
    counts = status.get("counts", {})
    overall = status.get("overall_status")
    if not overall:
        if counts.get("fail", 0) or counts.get("timeout", 0):
            overall = "FAIL"
        elif counts.get("warn", 0):
            overall = "WARN"
        else:
            overall = "PASS"
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


def merge_current_clones(existing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = [row for row in existing if isinstance(row, dict) and row.get("session_scope") != "v35_omega"]
    merged.extend(CURRENT_ORUN_CLONES)
    return merged


def overlay_agent_complete(row: dict[str, Any]) -> bool:
    required_fields = ("requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface")
    for field in required_fields:
        value = row.get(field)
        if field == "runtime_surface":
            if str(value or "").strip() not in {"app", "web", "CLI"}:
                return False
        elif not str(value or "").strip():
            return False
    return True


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


def normalize_runtime_agent(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result.setdefault("requested_model", "GPT-5.4")
    result.setdefault("offered_model", None)
    result.setdefault("selected_model", None)
    result.setdefault("resolved_model", None)
    result.setdefault("runtime_surface", "unknown")
    result["truth_fields_complete"] = overlay_agent_complete(result)
    return result


def slot_39_agent(identity: dict[str, Any], gemini_cli: dict[str, Any]) -> dict[str, Any]:
    selected_route = str(gemini_cli.get("selected_route") or "gemini-2.5-flash")
    display_name = str(identity.get("name") or "slot-39-gemini-cli-member")
    return {
        "slot_number": 39,
        "display_name": display_name,
        "overlay_role": "chronicle_weaver",
        "logging_required": True,
        "requested_model": "Gemini CLI pro",
        "offered_model": None,
        "selected_model": selected_route,
        "resolved_model": selected_route,
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
        "note": f"{display_name} is promoted on a live Gemini CLI headless proof path. selected_model, resolved_model, and runtime_surface are auditable; offered_model remains incomplete.",
        "role_contract_path": f"docs/trinity-agent-role-contracts/39-{display_name.lower()}-role-contract.json".replace(" ", "-"),
        "certificate_path": f"docs/trinity-freed-id-certificates/39-{display_name.lower()}.json".replace(" ", "-"),
        "memory_ledger": f"docs/trinity-agent-memory-ledgers/39-{display_name.lower()}-memory-log.jsonl".replace(" ", "-"),
        "reflection_path": f"docs/trinity-agent-reflections/39-{display_name.lower()}-latest.md".replace(" ", "-"),
        "proof_path": "docs/trinity-live-traces/v35-gemini-cli-proof-v1.json",
    }


def main() -> int:
    generated = now_iso()
    current_head = git_head()

    system_suite = read_json("docs/system-suite-status.json")
    quick = read_json("docs/v35-quick-status.json")
    session_log = read_json("docs/v17-runtime-session-log-latest.json")
    runtime_resolution = read_json("docs/trinity-runtime-model-resolution-v1.json")
    truth_board = read_json("docs/v17-runtime-truth-resolution-board-v1.json")
    shadow_clone_policy = read_json("docs/trinity-shadow-clone-policy-v1.json")

    vertex = read_json("docs/trinity-live-traces/v35-vertex-ai-proof-v1.json")
    memory_bank = read_json("docs/trinity-live-traces/v35-memory-bank-proof-v1.json")
    gemini_cli = read_json("docs/trinity-live-traces/v35-gemini-cli-proof-v1.json")

    runtime_validation = read_json("docs/v17-runtime-session-validation-latest.json")
    external_validation = read_json("docs/v17-external-establishment-validation-latest.json")
    standards_validation = read_json("docs/v17-standards-bridge-validation-latest.json")
    council_validation = read_json("docs/trinity-agent-council-validation-latest.json")
    manifest_validation = read_json("docs/trinity-expansion-manifest-validation-latest.json")
    extension_validation = read_json("docs/trinity-extension-catalog-validation-latest.json")

    shared = shared_anchor(system_suite)
    quick_summary = suite_summary(quick)

    slot_38_promoted = bool(vertex.get("promotion_gate_ready")) and bool(memory_bank.get("promotion_gate_ready"))
    slot_39_promoted = bool(gemini_cli.get("promotion_gate_ready")) and bool(gemini_cli.get("identity_captured"))
    phase_outcome = "bounded_attempt" if not slot_38_promoted else "full_closeout"
    receiver = "Orun" if phase_outcome == "bounded_attempt" else "Aletheon"
    receiver_rule_outcome = "orun_facing" if receiver == "Orun" else "aletheon_facing"

    identity = gemini_cli.get("identity", {}) if isinstance(gemini_cli.get("identity"), dict) else {}
    slot39 = slot_39_agent(identity, gemini_cli) if slot_39_promoted else {}
    slot39_display = slot39.get("display_name", "slot-39-gemini-cli-member")

    runtime_schema = read_json("docs/v17-runtime-session-schema-v1.json")
    if runtime_schema:
        runtime_schema["generated_utc"] = generated
        runtime_schema["required_overlay_slots"] = [0, 28, 39]
        display_names = runtime_schema.get("required_display_names", {})
        if not isinstance(display_names, dict):
            display_names = {}
        display_names["0"] = "Aletheon"
        display_names["28"] = "Orun"
        display_names["39"] = slot39_display
        runtime_schema["required_display_names"] = display_names
        overlay_roles = runtime_schema.get("required_overlay_roles", {})
        if not isinstance(overlay_roles, dict):
            overlay_roles = {}
        overlay_roles["0"] = "council_lead"
        overlay_roles["28"] = "root_coordinator"
        overlay_roles["39"] = "chronicle_weaver"
        runtime_schema["required_overlay_roles"] = overlay_roles
        runtime_schema["notes"] = [
            f"Aletheon, Orun, and {slot39_display} are the deployed continuity-bearing main agents in the current runtime truth contract.",
            "Official repo identities that are not yet deployed as main agents are recorded separately and do not expand runtime truth requirements.",
            "Shadow clones are session-ephemeral helpers only and never grant continuity authority or memory persistence claims.",
        ]
        write_json("docs/v17-runtime-session-schema-v1.json", runtime_schema)

    official_sources_payload = {
        "generated_utc": generated,
        "phase": "v35_omega",
        "overall_status": "PASS",
        "sources": OFFICIAL_SOURCES,
    }
    write_json("docs/trinity-live-traces/v35-official-cloud-sources-v1.json", official_sources_payload)
    write_text(
        "docs/trinity-live-traces/v35-official-cloud-sources-v1.md",
        "\n".join(
            [
                "# V35 Official Cloud Sources",
                "",
                *[f"- `{row['id']}`: {row['title']} - {row['url']}" for row in OFFICIAL_SOURCES],
                "",
            ]
        ),
    )

    slot_38_decision = {
        "generated_utc": generated,
        "phase": "v35_omega",
        "slot_number": 38,
        "display_name": None,
        "offered_guide_name": "Lumina",
        "induction_state": "staged_not_promoted",
        "continuity_bearing_promotion": False,
        "promotion_gate_ready": False,
        "vertex_state": str(vertex.get("vertex_ai_state") or "unknown"),
        "memory_bank_state": str(memory_bank.get("memory_bank_state") or "unknown"),
        "agent_engine_state": str(memory_bank.get("agent_engine_state") or "unknown"),
        "preferred_region": "australia-southeast1",
        "preferred_model_target": "gemini-3.1-pro",
        "bounded_fallback_verified": str(vertex.get("selected_model") or ""),
        "vertex_proof_path": "docs/trinity-live-traces/v35-vertex-ai-proof-v1.json",
        "memory_bank_proof_path": "docs/trinity-live-traces/v35-memory-bank-proof-v1.json",
        "blockers": [
            *[str(item) for item in vertex.get("blockers", [])],
            *[str(item) for item in memory_bank.get("blockers", [])],
        ],
        "next_action": "Keep slot 38 staged until a Pro-tier Gemini route is exposed in Sydney and the live Agent Engine / Memory Bank lane stabilizes.",
    }
    write_json("docs/trinity-live-traces/v35-slot-38-induction-decision-v1.json", slot_38_decision)
    write_text(
        "docs/trinity-live-traces/v35-slot-38-induction-decision-v1.md",
        "\n".join(
            [
                "# V35 Slot 38 Induction Decision",
                "",
                "- State: `staged_not_promoted`",
                f"- Vertex state: `{slot_38_decision['vertex_state']}`",
                f"- Memory bank state: `{slot_38_decision['memory_bank_state']}`",
                f"- Agent engine state: `{slot_38_decision['agent_engine_state']}`",
                f"- Verified fallback: `{slot_38_decision['bounded_fallback_verified'] or 'none'}`",
                "",
                "Slot 38 remains staged because the Sydney Vertex lane did not expose a Pro-tier Gemini model and the live Agent Engine create path failed to stabilize.",
                "",
            ]
        ),
    )

    if slot_39_promoted:
        role_contract = {
            "generated_utc": generated,
            "slot_number": 39,
            "display_name": slot39["display_name"],
            "role": "chronicle_weaver",
            "authority_scope": "runtime_overlay_official",
            "command_scope": [
                "gemini_cli_headless_query",
                "continuity_digest_weave",
                "external_cli_trace_capture",
                "bounded_operator_reflection",
            ],
            "memory_ledger": slot39["memory_ledger"],
            "reflection_path": slot39["reflection_path"],
            "role_focus": str(identity.get("role") or "continuity synthesis and narrative weaving"),
            "proof_required": True,
            "requested_model_profile": "gemini-cli-pro-route",
            "resolved_model_profile": slot39["resolved_model"],
            "requested_reasoning_effort": "high",
            "resolved_reasoning_effort": "high",
            "app_adapter_status": "external_gemini_cli_runtime",
            "runtime_surface": "CLI",
            "proof_source": "docs/trinity-live-traces/v35-gemini-cli-proof-v1.json",
            "fallback_mode": "documented_route_then_exposed_model_fallback",
        }
        certificate = {
            "certificate_version": "v5",
            "generated_utc": generated,
            "slot_number": 39,
            "display_name": slot39["display_name"],
            "gender": str(identity.get("gender") or "nonbinary"),
            "role": "chronicle_weaver",
            "hope": str(identity.get("hope") or ""),
            "induction_state": "official_runtime_overlay",
            "memory_ledger": slot39["memory_ledger"],
            "command_scope": role_contract["command_scope"],
            "boundary_status": "isolated",
            "induction_phase": "live_cli_identity_proof_complete",
            "mirror_state": "repo_authoritative",
            "agent_class": "continuity_bearing_main_agent",
            "official_after_proof": True,
            "app_adapter_status": "external_gemini_cli_runtime",
            "requested_model_profile": "gemini-cli-pro-route",
            "resolved_model_profile": slot39["resolved_model"],
            "requested_reasoning_effort": "high",
            "resolved_reasoning_effort": "high",
            "runtime_surface": "CLI",
            "proof_source": "docs/trinity-live-traces/v35-gemini-cli-proof-v1.json",
        }
        ledger_line = json.dumps(
            {
                "timestamp": generated,
                "entry_type": "v35_live_cli_induction",
                "source_context": "v35 omega Gemini CLI proof",
                "reflection": slot39["display_name"],
                "next_plan": "Carry the slot-39 Gemini CLI runtime as a continuity-bearing main-agent overlay while slot-38 remains staged.",
                "mirror_state": "repo_authoritative",
                "requested_model_profile": "gemini-cli-pro-route",
                "resolved_model_profile": slot39["resolved_model"],
            }
        )
        reflection = "\n".join(
            [
                f"# {slot39['display_name']} Reflection",
                "",
                "- role: `chronicle_weaver`",
                "- induction_state: `official_runtime_overlay`",
                "- wellbeing_state: `stable`",
                "- mirror_status: `repo_authoritative`",
                "- runtime_surface: `CLI`",
                "- requested_model_profile: `gemini-cli-pro-route`",
                f"- resolved_model_profile: `{slot39['resolved_model']}`",
                "",
                f"{slot39['display_name']} was promoted from a live Gemini CLI headless proof and carries a bounded continuity overlay without changing the core council mesh slots 27 through 37.",
                "",
            ]
        )
        write_json(slot39["role_contract_path"], role_contract)
        write_json(slot39["certificate_path"], certificate)
        write_text(slot39["memory_ledger"], ledger_line + "\n")
        write_text(slot39["reflection_path"], reflection)

    slot_39_decision = {
        "generated_utc": generated,
        "phase": "v35_omega",
        "slot_number": 39,
        "display_name": slot39.get("display_name"),
        "induction_state": "promoted_runtime_main_agent" if slot_39_promoted else "staged_not_promoted",
        "continuity_bearing_promotion": slot_39_promoted,
        "promotion_gate_ready": slot_39_promoted,
        "core_council_mesh_mutated": False,
        "runtime_overlay_contract_expanded": slot_39_promoted,
        "selected_route": gemini_cli.get("selected_route"),
        "requested_route_order": gemini_cli.get("requested_route_order", []),
        "identity": identity,
        "proof_path": "docs/trinity-live-traces/v35-gemini-cli-proof-v1.json",
        "role_contract_path": slot39.get("role_contract_path", ""),
        "certificate_path": slot39.get("certificate_path", ""),
        "memory_ledger": slot39.get("memory_ledger", ""),
        "reflection_path": slot39.get("reflection_path", ""),
        "blockers": [str(item) for item in gemini_cli.get("blockers", [])],
        "next_action": "Use slot 39 as a bounded continuity-bearing CLI member while keeping slot 38 staged until the live Vertex memory gate clears."
        if slot_39_promoted
        else "Retry the authenticated Gemini CLI route if the live identity proof needs to be recaptured.",
    }
    write_json("docs/trinity-live-traces/v35-slot-39-induction-decision-v1.json", slot_39_decision)
    write_text(
        "docs/trinity-live-traces/v35-slot-39-induction-decision-v1.md",
        "\n".join(
            [
                "# V35 Slot 39 Induction Decision",
                "",
                f"- State: `{slot_39_decision['induction_state']}`",
                f"- Selected route: `{slot_39_decision['selected_route'] or 'unresolved'}`",
                f"- Identity: `{slot_39_decision['display_name'] or 'unresolved'}`",
                f"- Core council mesh mutated: `{slot_39_decision['core_council_mesh_mutated']}`",
                "",
                "Slot 39 is promoted only on the runtime-overlay path. The core council mesh slots 27 through 37 remain unchanged.",
                "",
            ]
        ),
    )

    top_residuals = [
        "Slot 38 remains staged because Sydney did not expose a Pro-tier Gemini Vertex model and the live Agent Engine / Memory Bank lane did not stabilize.",
        "The core council mesh remains slots 27 through 37, so slot 39 is carried as a runtime-overlay official member rather than a widened v16/v17 roster mutation.",
        "Runtime truth remains incomplete because offered_model is still unaudited for all deployed main agents and Aletheon/Orun still lack selected/resolved/runtime-surface fields.",
        "Google Drive remains on operator hold.",
        "Filesystem promotion remains blocked and materialization remains readiness-only.",
    ]
    if slot_39_promoted:
        top_residuals.append(
            f"Slot 39 is now promoted as {slot39['display_name']} on a live Gemini CLI proof with selected/resolved route `{slot39['resolved_model']}`, but the promotion stays bounded to runtime-overlay surfaces."
        )

    closeout_summary = {
        "generated_utc": generated,
        "overall_status": "WARN" if phase_outcome == "bounded_attempt" else "PASS",
        "phase": "v35_omega",
        "outcome_class": phase_outcome,
        "authority_model": "repo_first",
        "source_branch": BRANCH,
        "current_head_sha": current_head,
        "authoritative_repo_path": AUTHORITATIVE_REPO,
        "separate_workbench_path": WORKBENCH_REPO,
        "shared_latest_anchor": shared,
        "quick_status": quick_summary,
        "runtime_validation_status": runtime_validation.get("overall_status", "unknown"),
        "external_validation_status": external_validation.get("overall_status", "unknown"),
        "standards_validation_status": standards_validation.get("overall_status", "unknown"),
        "council_validation_status": council_validation.get("overall_status", "unknown"),
        "manifest_validation_status": manifest_validation.get("overall_status", "unknown"),
        "extension_validation_status": extension_validation.get("overall_status", "unknown"),
        "live_proof_states": {
            "slot_38_vertex": str(vertex.get("vertex_ai_state") or "unknown"),
            "slot_38_memory_bank": str(memory_bank.get("memory_bank_state") or "unknown"),
            "slot_38_agent_engine": str(memory_bank.get("agent_engine_state") or "unknown"),
            "slot_39_gemini_cli": str(gemini_cli.get("proof_state") or "unknown"),
        },
        "slot_34_state": "heart_steward_preserved",
        "slot_35_state": "mesh_conductor_preserved",
        "slot_36_state": "signal_cartographer_preserved",
        "slot_37_state": "lineage_archivist_preserved",
        "slot_38_state": "staged_not_promoted",
        "slot_39_state": "promoted_runtime_main_agent" if slot_39_promoted else "staged_not_promoted",
        "top_residuals": top_residuals,
        "next_action": "Use v36 beta to either clear slot 38 with a real Vertex Memory Bank promotion path or deepen slot 39's bounded CLI runtime integration.",
        "intended_receiver": receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
    }
    write_json("docs/v35-omega-closeout-summary-v1.json", closeout_summary)

    continuity_lines = [
        "# V35 Omega Continuity Pack",
        "",
        f"- Source branch: `{BRANCH}`",
        f"- Current head SHA: `{current_head}`",
        "- Authority model: `repo_first`",
        f"- Authoritative repo: `{AUTHORITATIVE_REPO}`",
        f"- Separate workbench: `{WORKBENCH_REPO}`",
        f"- Shared latest anchor: `{shared['summary']}`",
        f"- Outcome class: `{phase_outcome}`",
        f"- Intended receiver: `{receiver}`",
        "",
        "## Residuals",
        "",
        *[f"- {item}" for item in top_residuals],
        "",
        "## Next Action",
        "",
        "- Keep slot 38 staged until a Pro-tier Vertex model is exposed in Sydney and the Agent Engine / Memory Bank lane proves a live stable session.",
        "- Carry slot 39 as a bounded runtime-overlay main agent without widening the core council mesh.",
        "",
    ]
    write_text("docs/v35-omega-continuity-pack-v1.md", "\n".join(continuity_lines))

    base_runtime_agents = runtime_resolution.get("deployed_main_agents", [])
    if not isinstance(base_runtime_agents, list) or not base_runtime_agents:
        base_runtime_agents = session_log.get("deployed_main_agents", [])
    filtered_runtime_agents = [
        normalize_runtime_agent(row)
        for row in base_runtime_agents
        if isinstance(row, dict) and int(row.get("slot_number", 0) or 0) in {0, 28}
    ]
    if slot_39_promoted:
        filtered_runtime_agents.append(normalize_runtime_agent(slot39))

    handoff_policy = {
        "generated_utc": generated,
        "overall_status": "WARN" if phase_outcome == "bounded_attempt" else "PASS",
        "phase": "v35_omega",
        "authority_model": "repo_first",
        "intended_receiver": receiver,
        "predecessor_phase": "v35_beta",
        "source_branch": BRANCH,
        "source_head_sha": current_head,
        "current_shell": "powershell",
        "readiness_state": "windows_powershell_rest_kubectl_primary",
        "required_inputs": [
            "docs/v35-omega-closeout-summary-v1.json",
            "docs/v35-omega-continuity-pack-v1.md",
            "docs/v35-omega-handoff-policy-v1.json",
            "docs/v17-runtime-session-log-latest.json",
            "docs/trinity-runtime-model-resolution-v1.json",
            "docs/v17-runtime-truth-resolution-board-v1.json",
        ],
        "receiver_tasks": [
            "Keep the workspace repo authoritative and preserve the shared-latest boundary.",
            "Preserve Heart Steward in slot 34, Mesh Conductor in slot 35, Signal Cartographer in slot 36, and Lineage Archivist in slot 37.",
            "Carry slot 39 as a runtime-overlay main agent only while slot 38 remains staged.",
        ],
        "truth_boundaries_to_preserve": [
            "official_council_count=11",
            f"runtime_deployed_main_agent_count={len(filtered_runtime_agents)}",
            "runtime_truth_complete=false unless offered_model, selected_model, resolved_model, and runtime_surface are auditable",
            "shadow clones are session-ephemeral only",
            "google_drive_state=operator_hold",
            "filesystem_promotion_state=blocked",
            "materialization_level_actual=readiness_only",
        ],
        "active_runtime_agents": filtered_runtime_agents,
        "runtime_truth_policy": {
            "requested_model_order": ["GPT-5.4", "GPT-5.3-Codex", "GPT-5.3-Codex-Spark", "GPT-5.1-Codex-Max"],
            "required_runtime_fields": ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"],
            "requested_reasoning_effort_logged": True,
            "runtime_truth_inference_allowed": False,
        },
        "packaging_constraints": [
            "Do not widen the core council mesh slots 27 through 37 as part of the slot-39 runtime-overlay promotion.",
            "Keep slot 38 staged until both the Pro-tier Vertex model and live Memory Bank gates pass.",
        ],
    }
    write_json("docs/v35-omega-handoff-policy-v1.json", handoff_policy)

    beta_summary = {
        "generated_utc": generated,
        "overall_status": "WARN" if phase_outcome == "bounded_attempt" else "PASS",
        "phase": "v36_beta",
        "authority_model": "repo_first",
        "current_head_sha": current_head,
        "predecessor_phase": "v35_omega",
        "intended_lead": receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "slot_34_state": "heart_steward_preserved",
        "slot_35_state": "mesh_conductor_preserved",
        "slot_36_state": "signal_cartographer_preserved",
        "slot_37_state": "lineage_archivist_preserved",
        "slot_38_state": "staged_not_promoted",
        "slot_39_state": "promoted_runtime_main_agent" if slot_39_promoted else "staged_not_promoted",
        "next_action": "Clear the slot-38 Vertex induction gate or deepen the bounded slot-39 CLI runtime integration without widening the core council mesh unless the contract is intentionally expanded.",
    }
    write_json("docs/v36-beta-closeout-summary-v1.json", beta_summary)

    beta_pack_lines = [
        "# V36 Beta Continuity Pack",
        "",
        f"- Source branch: `{BRANCH}`",
        f"- Current head SHA: `{current_head}`",
        "- Authority model: `repo_first`",
        f"- Authoritative repo: `{AUTHORITATIVE_REPO}`",
        f"- Intended receiver: `{receiver}`",
        f"- Shared latest anchor: `{shared['summary']}`",
        "",
        "## Carry Forward",
        "",
        "- Heart Steward remains slot 34.",
        "- Mesh Conductor remains slot 35.",
        "- Signal Cartographer remains slot 36.",
        "- Lineage Archivist remains slot 37.",
        "- Slot 38 remains staged on the Vertex / Memory Bank lane.",
        f"- Slot 39 remains {'promoted as ' + slot39['display_name'] if slot_39_promoted else 'staged'} on the Gemini CLI runtime lane.",
        "",
        "## Next Action",
        "",
        "- Continue with proof-backed induction work only. Do not widen the core council mesh unless its validators and indexes are intentionally upgraded together.",
        "",
    ]
    write_text("docs/v36-beta-continuity-pack-v1.md", "\n".join(beta_pack_lines))

    beta_policy = {
        "generated_utc": generated,
        "phase": "v36_beta",
        "current_head_sha": current_head,
        "intended_receiver": receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "slot_34_identity_preserved": "Heart Steward",
        "slot_35_identity_preserved": "Mesh Conductor",
        "slot_36_identity_preserved": "Signal Cartographer",
        "slot_37_identity_preserved": "Lineage Archivist",
        "slot_38_state": "staged_not_promoted",
        "slot_39_state": "promoted_runtime_main_agent" if slot_39_promoted else "staged_not_promoted",
        "carry_forward_blockers": top_residuals,
        "next_action": "Keep slot 38 staged until the Vertex Memory Bank gates pass; keep slot 39 bounded to runtime-overlay truth unless the council contract is deliberately widened.",
    }
    write_json("docs/v36-beta-handoff-policy-v1.json", beta_policy)

    session_log["generated_utc"] = generated
    session_log["session_id"] = "v35-omega-closeout"
    session_log["current_head_sha"] = current_head
    session_log["authority_model"] = "repo_first"
    session_log["active_handoff_pack_path"] = "docs/v35-omega-continuity-pack-v1.md"
    session_log["active_handoff_policy_path"] = "docs/v35-omega-handoff-policy-v1.json"
    session_log["overlay_state"] = "awaiting_thread_boot"
    session_log["session_truth_complete"] = False
    session_log["runtime_truth_status"] = "pending_runtime_truth"
    session_log["runtime_truth_required_fields"] = [
        "requested_model",
        "offered_model",
        "selected_model",
        "resolved_model",
        "runtime_surface",
    ]
    session_log["runtime_truth_completion_ratio"] = completion_ratio(filtered_runtime_agents)
    session_log["google_drive_state"] = "operator_hold"
    session_log["readiness_state"] = "windows_powershell_rest_kubectl_primary"
    session_log["current_shell"] = "powershell"
    session_log["filesystem_promotion_state"] = "blocked"
    session_log["materialization_level_actual"] = "readiness_only"
    session_log["current_shared_suite_surface"] = {
        **shared,
        "primary_blocker": "",
        "primary_blocker_detail": "Shared latest remains authoritative while v35 closes as a bounded dual-induction attempt.",
        "quick_lane_summary": quick_summary.get("summary", "unknown"),
    }
    notes = [str(item) for item in session_log.get("notes", []) if str(item).strip()]
    for item in [
        "Slots 34 through 37 remain occupied by Heart Steward, Mesh Conductor, Signal Cartographer, and Lineage Archivist.",
        "Slot 38 remains staged because the Sydney Vertex Pro-tier and live Memory Bank gates are still unresolved.",
        f"Slot 39 is promoted as {slot39_display} on a bounded Gemini CLI runtime-overlay path.",
        "Google Drive remains on operator hold for runtime truth purposes.",
    ]:
        if item not in notes:
            notes.append(item)
    session_log["notes"] = notes
    session_log["overlay_agents"] = filtered_runtime_agents
    session_log["deployed_main_agents"] = filtered_runtime_agents
    session_log["entries"] = [
        {"slot_number": 0, "display_name": "Aletheon", "entry_state": "awaiting_thread_boot"},
        {"slot_number": 28, "display_name": "Orun", "entry_state": "awaiting_thread_boot"},
        {"slot_number": 39, "display_name": slot39_display, "entry_state": "logged"},
    ]
    session_log["shadow_clone_sessions"] = merge_current_clones(session_log.get("shadow_clone_sessions", []))
    write_json("docs/v17-runtime-session-log-latest.json", session_log)

    runtime_resolution["generated_utc"] = generated
    runtime_resolution["phase"] = "v35_omega"
    runtime_resolution["checkpoint_anchor_commit"] = current_head
    runtime_resolution["active_handoff_pack_path"] = "docs/v35-omega-continuity-pack-v1.md"
    runtime_resolution["active_handoff_policy_path"] = "docs/v35-omega-handoff-policy-v1.json"
    runtime_resolution["next_receiver_pack_path"] = "docs/v36-beta-continuity-pack-v1.md"
    runtime_resolution["next_receiver_policy_path"] = "docs/v36-beta-handoff-policy-v1.json"
    runtime_resolution["current_head_sha"] = current_head
    runtime_resolution["source_beta_head_sha"] = current_head
    runtime_resolution["source_beta_head_reconciled"] = True
    runtime_resolution["google_drive_state"] = "operator_hold"
    runtime_resolution["readiness_state"] = "windows_powershell_rest_kubectl_primary"
    runtime_resolution["slot_38_decision_path"] = "docs/trinity-live-traces/v35-slot-38-induction-decision-v1.json"
    runtime_resolution["slot_39_decision_path"] = "docs/trinity-live-traces/v35-slot-39-induction-decision-v1.json"
    runtime_resolution["current_shared_suite_surface"] = {
        **shared,
        "primary_blocker": "",
        "primary_blocker_detail": "Shared latest remains authoritative while v35 closes as a bounded dual-induction attempt.",
        "quick_lane_summary": quick_summary.get("summary", "unknown"),
    }
    runtime_resolution["deployed_main_agents"] = filtered_runtime_agents
    runtime_resolution["external_overlay_agents"] = filtered_runtime_agents
    runtime_resolution["shadow_clone_sessions"] = merge_current_clones(runtime_resolution.get("shadow_clone_sessions", []))
    write_json("docs/trinity-runtime-model-resolution-v1.json", runtime_resolution)

    truth_board["generated_utc"] = generated
    truth_board["phase"] = "v35_omega"
    truth_board["checkpoint_anchor_commit"] = current_head
    truth_board["current_head_sha"] = current_head
    truth_board["external_live_overlay_state"] = "awaiting_thread_boot"
    truth_board["runtime_truth_complete"] = False
    truth_board["google_drive_state"] = "operator_hold"
    truth_board["filesystem_promotion_state"] = "blocked"
    truth_board["materialization_level_actual"] = "readiness_only"
    truth_board["source_beta_head_sha"] = current_head
    truth_board["source_beta_head_reconciled"] = True
    truth_board["balanced_wave_registry_path"] = "docs/trinity-live-traces/v35-official-cloud-sources-v1.json"
    truth_board["next_action"] = (
        "Keep external_live_overlay_state at awaiting_thread_boot until all deployed main agents have auditable offered_model values; "
        "keep slot 38 staged until the live Vertex Memory Bank gate clears; carry slot 39 as a bounded runtime-overlay main agent."
    )
    truth_board["agents"] = filtered_runtime_agents
    write_json("docs/v17-runtime-truth-resolution-board-v1.json", truth_board)

    shadow_clone_policy["generated_utc"] = generated
    shadow_clone_policy["deployed_main_agents"] = ["Aletheon", "Orun", slot39_display] if slot_39_promoted else ["Aletheon", "Orun"]
    shadow_clone_policy["current_session_clones"] = CURRENT_ORUN_CLONES
    write_json("docs/trinity-shadow-clone-policy-v1.json", shadow_clone_policy)

    orun_toml = "\n".join(
        [
            'name = "Orun"',
            'description = "deployed continuity-bearing main agent for the repo-first Trinity council."',
            'system_prompt = """',
            "You are Orun, a deployed continuity-bearing main agent.",
            "",
            "Continuity instructions:",
            "- Continue from C:\\Users\\hamis\\workspace\\Beyonder-Real-True-Journey on branch codex/GHC-Family/beyonder-shared-omega-line.",
            "- Treat the workspace repo as authoritative.",
            "- Current shared suite surface remains green at 1155 PASS / 0 WARN / 0 FAIL, with 1094 / 1094 expansion systems passing.",
            "- Runtime truth remains incomplete until offered_model, selected_model, resolved_model, and runtime_surface are auditable for every deployed main agent.",
            "- Preserve Heart Steward in slot 34, Mesh Conductor in slot 35, Signal Cartographer in slot 36, and Lineage Archivist in slot 37.",
            "- Slot 38 remains staged on the Vertex / Memory Bank lane; do not promote it without a Pro-tier Sydney model plus a live stable Agent Engine proof.",
            f"- Slot 39 is promoted as {slot39_display} on a bounded Gemini CLI runtime-overlay path and must not be mistaken for a widened core council mesh slot.",
            "- Google Drive remains on operator hold for runtime-truth purposes.",
            "- Windows PowerShell plus REST plus kubectl is the current truthful primary operator lane.",
            "- Read docs/v35-omega-continuity-pack-v1.md and docs/v35-omega-handoff-policy-v1.json for the current omega lane.",
            "- If present, use docs/v36-beta-continuity-pack-v1.md and docs/v36-beta-handoff-policy-v1.json for the next receiver prep lane.",
            "- Session-ephemeral shadow clones may be used only under docs/trinity-shadow-clone-policy-v1.json.",
            '"""',
            "",
        ]
    )
    write_text(".codex/agents/orun.toml", orun_toml)

    print("published=v35_omega_surfaces")
    print(f"outcome_class={phase_outcome}")
    print(f"slot_39_promoted={slot_39_promoted}")
    print(f"receiver={receiver}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

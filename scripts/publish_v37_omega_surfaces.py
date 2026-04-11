#!/usr/bin/env python3
"""Publish V37 Omega closeout surfaces and the V38 beta receiver pack."""

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
        "session_scope": "v37_omega",
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
        "session_scope": "v37_omega",
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
    {
        "id": "codex_local_environments",
        "title": "Codex local environments",
        "url": "https://developers.openai.com/codex/app/local-environments",
    },
    {
        "id": "codex_cloud_environments",
        "title": "Codex cloud environments",
        "url": "https://developers.openai.com/codex/cloud/environments",
    },
    {
        "id": "codex_workflows",
        "title": "Codex workflows",
        "url": "https://developers.openai.com/codex/workflows",
    },
    {
        "id": "codex_use_cases",
        "title": "Codex use cases",
        "url": "https://developers.openai.com/codex/use-cases",
    },
    {
        "id": "gpt_5_4_model",
        "title": "GPT-5.4 model page",
        "url": "https://developers.openai.com/api/docs/models/gpt-5.4",
    },
]
PRESERVED_SLOT_IDENTITIES = {
    34: "Heart Steward",
    35: "Mesh Conductor",
    36: "Signal Cartographer",
    37: "Lineage Archivist",
}


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


def read_first_json(*candidates: str) -> dict[str, Any]:
    for rel in candidates:
        payload = read_json(rel)
        if payload:
            return payload
    return {}


def write_json(rel: str, payload: dict[str, Any]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_jsonl(rel: str) -> list[dict[str, Any]]:
    path = ROOT / rel
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            rows.append(parsed)
    return rows


def rewrite_jsonl(rel: str, rows: list[dict[str, Any]]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(row, ensure_ascii=True) for row in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def append_unique_jsonl(rel: str, row: dict[str, Any], key_fields: tuple[str, ...]) -> None:
    rows = read_jsonl(rel)
    key = tuple(str(row.get(field) or "") for field in key_fields)
    for existing in rows:
        existing_key = tuple(str(existing.get(field) or "") for field in key_fields)
        if existing_key == key:
            return
    rows.append(row)
    rewrite_jsonl(rel, rows)


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


def standard_failures(status: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for row in status.get("results", []) if isinstance(status.get("results"), list) else []:
        if not isinstance(row, dict) or row.get("status") != "FAIL":
            continue
        rows.append({"label": str(row.get("label") or ""), "command": str(row.get("command") or "")})
    return rows


def markdown_decision(title: str, rows: list[str]) -> str:
    return "\n".join([f"# {title}", "", *rows, ""])


def blocker_lines(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] or ["- none"]


def slugify(value: str) -> str:
    cleaned = "".join(char.lower() if char.isalnum() else "-" for char in str(value or ""))
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-")


def merge_current_clones(existing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = [row for row in existing if isinstance(row, dict) and row.get("session_scope") != "v37_omega"]
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
                if str(value or "").strip() in {"app", "web", "CLI", "cloud"}:
                    complete += 1
            elif str(value or "").strip():
                complete += 1
    return round(complete / total, 4)


def status_clean(status: dict[str, Any]) -> bool:
    if not status:
        return False
    return str(status.get("overall_status") or "") == "PASS" and int(status.get("warn_count", 0) or 0) == 0 and int(status.get("fail_count", 0) or 0) == 0


def slot38_agent(vertex: dict[str, Any]) -> tuple[dict[str, Any], str, str]:
    identity = vertex.get("identity", {}) if isinstance(vertex.get("identity"), dict) else {}
    display_name = str(identity.get("name") or "Vesper Ion")
    display_slug = slugify(display_name)
    role_slug = slugify(identity.get("role") or "vertex_cloud_member").replace("-", "_")
    selected_model = str(vertex.get("selected_model") or vertex.get("resolved_model") or "gemini-3.1-pro-preview")
    return (
        {
            "slot_number": 38,
            "display_name": display_name,
            "overlay_role": role_slug,
            "logging_required": True,
            "requested_model": "gemini-3.1-pro-preview",
            "offered_model": None,
            "selected_model": selected_model,
            "resolved_model": selected_model,
            "runtime_surface": "cloud",
            "truth_fields_complete": False,
            "requested_reasoning_effort": "high",
            "deployment_state": "deployed_main_agent",
            "continuity_class": "continuity_bearing_main_agent",
            "identity_locked": True,
            "runtime_truth_required": True,
            "persistent_runtime_proven": True,
            "shadow_clone_allowed": False,
            "shadow_clone_owner": "",
            "shadow_clone_naming_pattern": "",
            "agent_class": "external_vertex_cloud_inducted_member",
            "app_adapter_status": "vertex_global_model_bigtable_memory_bridge",
            "note": "Slot 38 is promoted in place through global Gemini 3 model resolution, auditable live identity capture, and a us-central1 Bigtable durable-memory bridge after the Agent Engine path stayed unstable.",
            "role_contract_path": f"docs/trinity-agent-role-contracts/38-{display_slug}-role-contract.json",
            "certificate_path": f"docs/trinity-freed-id-certificates/38-{display_slug}.json",
            "memory_ledger": f"docs/trinity-agent-memory-ledgers/38-{display_slug}-memory-log.jsonl",
            "reflection_path": f"docs/trinity-agent-reflections/38-{display_slug}-latest.md",
            "proof_path": "docs/trinity-live-traces/v37-slot-38-vertex-ai-proof-v1.json",
            "durable_memory_proof_path": "docs/trinity-live-traces/v37-slot-38-bigtable-bridge-proof-v1.json",
            "agent_engine_residual_path": "docs/trinity-live-traces/v37-slot-38-agent-engine-bridge-proof-v1.json",
        },
        display_name,
        role_slug,
    )


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
        "proof_path": "docs/trinity-live-traces/v37-slot-39-gemini-cli-proof-v1.json",
        "bridge_proof_path": "docs/trinity-live-traces/v37-kai-bridge-proof-v1.json",
    }


def main() -> int:
    generated = now_iso()
    current_head = git_head()

    system_suite = read_json("docs/system-suite-status.json")
    quick = read_first_json(
        "docs/trinity-live-traces/v37-quick-after-slot-status.json",
        "docs/v37-quick-status.json",
    )
    standard = read_first_json(
        "docs/trinity-live-traces/v37-standard-status.json",
        "docs/v37-standard-status.json",
    )
    deep = read_first_json(
        "docs/trinity-live-traces/v37-deep-status.json",
        "docs/v37-deep-status.json",
    )
    l2 = read_first_json(
        "docs/trinity-live-traces/v37-materialize-l2-status.json",
        "docs/v37-materialize-l2-status.json",
    )
    l3 = read_first_json(
        "docs/trinity-live-traces/v37-materialize-l3-status.json",
        "docs/v37-materialize-l3-status.json",
    )
    l4 = read_first_json(
        "docs/trinity-live-traces/v37-materialize-l4-status.json",
        "docs/v37-materialize-l4-status.json",
    )
    l5 = read_first_json(
        "docs/trinity-live-traces/v37-materialize-l5-status.json",
        "docs/v37-materialize-l5-status.json",
    )

    session_log = read_json("docs/v17-runtime-session-log-latest.json")
    runtime_resolution = read_json("docs/trinity-runtime-model-resolution-v1.json")
    truth_board = read_json("docs/v17-runtime-truth-resolution-board-v1.json")
    shadow_clone_policy = read_json("docs/trinity-shadow-clone-policy-v1.json")
    beta_policy = read_json("docs/v37-beta-handoff-policy-v1.json")

    runtime_validation = read_json("docs/v17-runtime-session-validation-latest.json")
    external_validation = read_json("docs/v17-external-establishment-validation-latest.json")
    standards_validation = read_json("docs/v17-standards-bridge-validation-latest.json")
    council_validation = read_json("docs/trinity-agent-council-validation-latest.json")
    manifest_validation = read_json("docs/trinity-expansion-manifest-validation-latest.json")
    extension_validation = read_json("docs/trinity-extension-catalog-validation-latest.json")

    proposal_digest = read_json("docs/trinity-live-traces/v37-proposal-digest-v1.json")
    slot38_vertex = read_json("docs/trinity-live-traces/v37-slot-38-vertex-ai-proof-v1.json")
    slot38_agent_engine = read_json("docs/trinity-live-traces/v37-slot-38-agent-engine-bridge-proof-v1.json")
    slot38_bigtable = read_json("docs/trinity-live-traces/v37-slot-38-bigtable-bridge-proof-v1.json")
    kai_cli = read_json("docs/trinity-live-traces/v37-slot-39-gemini-cli-proof-v1.json")
    kai_bridge = read_json("docs/trinity-live-traces/v37-kai-bridge-proof-v1.json")
    sovereignty = read_json("docs/trinity-live-traces/v37-iam-sovereignty-proof-v1.json")

    shared = shared_anchor(system_suite)
    quick_summary = suite_summary(quick)
    standard_summary = suite_summary(standard)
    deep_summary = suite_summary(deep)
    materialize_summaries = {
        "l2": suite_summary(l2),
        "l3": suite_summary(l3),
        "l4": suite_summary(l4),
        "l5": suite_summary(l5),
    }

    slot_38_promoted = bool(slot38_vertex.get("promotion_gate_ready")) and bool(slot38_bigtable.get("promotion_gate_ready"))
    kai_model = str(kai_cli.get("selected_model") or "gemini-3.1-pro-preview")
    slot_39_upgraded = bool(kai_cli.get("promotion_gate_ready")) and kai_model == "gemini-3.1-pro-preview"
    sovereignty_applied = str(sovereignty.get("overall_status") or "") == "PASS"
    quick_clean = status_clean(quick_summary)
    standard_clean = status_clean(standard_summary)
    deep_clean = status_clean(deep_summary) if deep_summary else False
    materialize_runs = [materialize_summaries[key] for key in ("l2", "l3", "l4", "l5") if materialize_summaries[key]]
    materialize_clean = bool(materialize_runs) and all(status_clean(row) for row in materialize_runs)
    full_closeout = slot_38_promoted and slot_39_upgraded and sovereignty_applied and quick_clean and standard_clean and deep_clean and materialize_clean
    phase_outcome = "full_closeout" if full_closeout else "bounded_attempt"
    receiver = "Aletheon" if full_closeout else "Orun"
    receiver_rule_outcome = "aletheon_facing" if receiver == "Aletheon" else "orun_facing"

    base_agents = runtime_base_agents(runtime_resolution, beta_policy)
    aletheon = normalized_agent(dict(base_agents.get(0) or {"slot_number": 0, "display_name": "Aletheon", "overlay_role": "council_lead"}))
    orun = normalized_agent(dict(base_agents.get(28) or {"slot_number": 28, "display_name": "Orun", "overlay_role": "root_coordinator"}))
    slot38_agent_row, slot38_name, slot38_role = slot38_agent(slot38_vertex)
    kai = kai_agent(
        kai_model,
        "Kai remains slot 39 on the verified Pro-tier Gemini CLI route and now carries the bounded Kai bridge for whitelisted headless workflows."
        if slot_39_upgraded
        else "Kai remains preserved on the bounded Gemini CLI route.",
    )

    deployed_agents = [aletheon, orun]
    if slot_38_promoted:
        deployed_agents.append(normalized_agent(slot38_agent_row))
    deployed_agents.append(normalized_agent(kai))
    deployed_agents = sorted(deployed_agents, key=lambda row: int(row.get("slot_number", 0)))

    sources_payload = {
        "generated_utc": generated,
        "phase": "v37_omega",
        "overall_status": "PASS",
        "regional_location": "us-central1",
        "model_location": "global",
        "legacy_evidence_region": "australia-southeast1",
        "sources": OFFICIAL_SOURCES,
    }
    write_json("docs/trinity-live-traces/v37-official-sources-v1.json", sources_payload)
    write_text(
        "docs/trinity-live-traces/v37-official-sources-v1.md",
        "\n".join(["# V37 Official Sources", "", *[f"- `{row['id']}`: {row['title']} - {row['url']}" for row in OFFICIAL_SOURCES], ""]),
    )

    capability_board = {
        "generated_utc": generated,
        "phase": "v37_omega",
        "surfaces": [
            {
                "surface_id": "codex_local",
                "label": "Codex local",
                "ownership": "primary",
                "recommended_for": [
                    "laptop_bound_trinity_work",
                    "local_mcp_usage",
                    "repo_wide_reasoning",
                    "mixed_local_cloud_orchestration",
                    "large_codebase_understanding",
                    "api_upgrade_work",
                    "visual_ui_implementation",
                    "data_reporting_tasks",
                ],
                "constraints": [
                    "Depends on the operator machine state and local connector readiness.",
                ],
                "official_sources": [
                    "codex_local_environments",
                    "codex_workflows",
                    "codex_use_cases",
                    "gpt_5_4_model",
                ],
                "repo_proofs": [
                    "docs/trinity-live-traces/v37-proposal-digest-v1.json",
                    "docs/trinity-live-traces/v37-kai-bridge-proof-v1.json",
                ],
            },
            {
                "surface_id": "codex_cloud_environments",
                "label": "Codex cloud environments",
                "ownership": "auxiliary",
                "recommended_for": [
                    "github_backed_reproducible_repo_tasks",
                    "isolated_parallel_jobs",
                    "pr_review_workflows",
                    "scored_improvement_loops",
                ],
                "constraints": [
                    "Use as an auxiliary GitHub-backed lane rather than a replacement for laptop-bound Trinity operations.",
                ],
                "official_sources": [
                    "codex_cloud_environments",
                    "codex_workflows",
                    "codex_use_cases",
                ],
                "repo_proofs": [
                    "docs/trinity-live-traces/v37-proposal-digest-v1.json",
                ],
            },
            {
                "surface_id": "kai_gemini_cli",
                "label": "Gemini CLI / Kai",
                "ownership": "bounded_headless_orchestrator",
                "recommended_for": [
                    "headless_terminal_orchestration",
                    "cli_native_scripting",
                    "bounded_validation_loops",
                    "proof_refresh_loops",
                    "repo_safe_diagnostics",
                ],
                "constraints": [
                    "Keep Kai on whitelisted bounded shell workflows rather than unconstrained repo authority inflation.",
                ],
                "official_sources": [
                    "gemini_cli_model_selection",
                ],
                "repo_proofs": [
                    "docs/trinity-live-traces/v37-slot-39-gemini-cli-proof-v1.json",
                    "docs/trinity-live-traces/v37-kai-bridge-proof-v1.json",
                ],
            },
            {
                "surface_id": "vertex_ai_cloud_node",
                "label": "Vertex AI cloud node",
                "ownership": "cloud_inference_and_memory_experiments",
                "recommended_for": [
                    "global_gemini_3_pro_model_resolution",
                    "persistent_cloud_memory_experiments",
                    "slot_38_runtime_operations",
                ],
                "constraints": [
                    "Keep model requests on `global` and memory backends regional in `us-central1`.",
                    "Treat the unstable Agent Engine path as a non-gating residual while the Bigtable bridge remains the proven durable-memory route.",
                ],
                "official_sources": [
                    "vertex_ai_locations",
                    "agent_builder_locations",
                    "gemini_3_vertex",
                ],
                "repo_proofs": [
                    "docs/trinity-live-traces/v37-slot-38-vertex-ai-proof-v1.json",
                    "docs/trinity-live-traces/v37-slot-38-bigtable-bridge-proof-v1.json",
                    "docs/trinity-live-traces/v37-slot-38-agent-engine-bridge-proof-v1.json",
                ],
            },
        ],
    }
    write_json("docs/trinity-live-traces/v37-capability-board-v1.json", capability_board)
    write_text(
        "docs/trinity-live-traces/v37-capability-board-v1.md",
        "\n".join(
            [
                "# V37 Capability Board",
                "",
                "- `Codex local`: primary Trinity operator surface for repo-wide reasoning, local MCP usage, machine-bound orchestration, large-codebase understanding, API upgrades, UI implementation, and reporting work.",
                "- `Codex cloud environments`: auxiliary GitHub-backed lane for isolated reproducible jobs, PR/review workflows, and scored improvement loops.",
                "- `Kai / Gemini CLI`: bounded headless terminal orchestrator for whitelisted validation, proof refresh, and diagnostics loops.",
                "- `Vertex AI cloud node`: cloud inference and durable-memory experimentation lane for slot 38 using `global` model resolution plus `us-central1` memory backends.",
                "",
            ]
        ),
    )
    write_text(
        "docs/trinity-live-traces/v37-codex-usage-pack-v1.md",
        "\n".join(
            [
                "# V37 Codex Usage Pack",
                "",
                "- Large-codebase understanding: lead with `Codex local`; use `Codex cloud environments` for bounded parallel repo jobs when GitHub-backed isolation helps.",
                "- PR and review workflows: use `Codex cloud environments` for reproducible GitHub-backed review lanes, with `Codex local` as the decision and integration surface.",
                "- Scored improvement loops: use `Codex cloud environments` for isolated reruns and `Codex local` for synthesis and follow-through.",
                "- API upgrade work: use `Codex local` as the primary repo-wide implementation surface, with `Kai` available for bounded CLI refresh loops.",
                "- Visual or UI implementation: use `Codex local` for the main implementation lane and keep `Vertex` out of UI ownership except for bounded cloud proof tasks.",
                "- Data and reporting tasks: use `Codex local` for repo-backed reporting and `Kai` for bounded headless command execution where JSON output helps.",
                "",
            ]
        ),
    )

    slot_38_blockers = [str(item) for item in slot38_vertex.get("blockers", [])] + [str(item) for item in slot38_bigtable.get("blockers", [])]
    slot_38_decision = {
        "generated_utc": generated,
        "phase": "v37_omega",
        "slot_number": 38,
        "display_name": slot38_name if slot_38_promoted else None,
        "induction_state": "promoted_runtime_main_agent" if slot_38_promoted else "staged_not_promoted",
        "continuity_bearing_promotion": slot_38_promoted,
        "promotion_gate_ready": slot_38_promoted,
        "regional_location": "us-central1",
        "model_location": "global",
        "selected_model": str(slot38_vertex.get("selected_model") or ""),
        "vertex_state": str(slot38_vertex.get("proof_state") or "unknown"),
        "agent_engine_state": str(slot38_agent_engine.get("proof_state") or "unknown"),
        "durable_memory_state": str(slot38_bigtable.get("proof_state") or "unknown"),
        "memory_mode_selected": "bigtable" if slot_38_promoted else "agent_engine",
        "vertex_proof_path": "docs/trinity-live-traces/v37-slot-38-vertex-ai-proof-v1.json",
        "agent_engine_proof_path": "docs/trinity-live-traces/v37-slot-38-agent-engine-bridge-proof-v1.json",
        "durable_memory_proof_path": "docs/trinity-live-traces/v37-slot-38-bigtable-bridge-proof-v1.json",
        "blockers": slot_38_blockers if not slot_38_promoted else [],
        "non_gating_residuals": []
        if not slot_38_promoted
        else [
            "The Agent Engine lane remains unstable in us-central1 and is preserved as a non-gating recovery target because the Bigtable durable-memory bridge succeeded.",
        ],
    }
    slot_39_decision = {
        "generated_utc": generated,
        "phase": "v37_omega",
        "slot_number": 39,
        "display_name": "Kai",
        "induction_state": "promoted_runtime_main_agent",
        "upgrade_state": "pro_tier_upgrade_verified" if slot_39_upgraded else "bounded_runtime_preserved",
        "promotion_gate_ready": slot_39_upgraded,
        "selected_route": str(kai_cli.get("selected_route") or ""),
        "selected_model": kai_model,
        "kai_bridge_state": str(kai_bridge.get("overall_status") or "unknown"),
        "bridge_proof_path": "docs/trinity-live-traces/v37-kai-bridge-proof-v1.json",
        "proof_path": "docs/trinity-live-traces/v37-slot-39-gemini-cli-proof-v1.json",
        "blockers": [str(item) for item in kai_cli.get("blockers", [])] + [str(item) for item in kai_bridge.get("blockers", [])],
    }
    write_json("docs/trinity-live-traces/v37-slot-38-induction-decision-v1.json", slot_38_decision)
    write_json("docs/trinity-live-traces/v37-slot-39-induction-decision-v1.json", slot_39_decision)
    write_text(
        "docs/trinity-live-traces/v37-slot-38-induction-decision-v1.md",
        markdown_decision(
            "V37 Slot 38 Induction Decision",
            [
                f"- induction_state: `{slot_38_decision['induction_state']}`",
                f"- display_name: `{slot_38_decision['display_name'] or 'unresolved'}`",
                f"- selected_model: `{slot_38_decision['selected_model'] or 'unresolved'}`",
                f"- vertex_state: `{slot_38_decision['vertex_state']}`",
                f"- agent_engine_state: `{slot_38_decision['agent_engine_state']}`",
                f"- durable_memory_state: `{slot_38_decision['durable_memory_state']}`",
                f"- memory_mode_selected: `{slot_38_decision['memory_mode_selected']}`",
                f"- promotion_gate_ready: `{slot_38_decision['promotion_gate_ready']}`",
                "",
                "Blockers:",
                *blocker_lines(slot_38_decision["blockers"]),
            ],
        ),
    )
    write_text(
        "docs/trinity-live-traces/v37-slot-39-induction-decision-v1.md",
        markdown_decision(
            "V37 Slot 39 Induction Decision",
            [
                f"- induction_state: `{slot_39_decision['induction_state']}`",
                f"- upgrade_state: `{slot_39_decision['upgrade_state']}`",
                f"- selected_route: `{slot_39_decision['selected_route'] or 'unresolved'}`",
                f"- selected_model: `{slot_39_decision['selected_model']}`",
                f"- kai_bridge_state: `{slot_39_decision['kai_bridge_state']}`",
                f"- promotion_gate_ready: `{slot_39_decision['promotion_gate_ready']}`",
                "",
                "Blockers:",
                *blocker_lines(slot_39_decision["blockers"]),
            ],
        ),
    )

    if slot_38_promoted:
        slot38_slug = slugify(slot38_name)
        slot38_identity = slot38_vertex.get("identity", {}) if isinstance(slot38_vertex.get("identity"), dict) else {}
        write_json(
            f"docs/trinity-agent-role-contracts/38-{slot38_slug}-role-contract.json",
            {
                "generated_utc": generated,
                "slot_number": 38,
                "display_name": slot38_name,
                "role": slot38_role,
                "authority_scope": "runtime_overlay_official",
                "memory_ledger": f"docs/trinity-agent-memory-ledgers/38-{slot38_slug}-memory-log.jsonl",
                "reflection_path": f"docs/trinity-agent-reflections/38-{slot38_slug}-latest.md",
                "requested_model_profile": "gemini-3.1-pro-preview",
                "resolved_model_profile": str(slot38_vertex.get("selected_model") or ""),
                "requested_reasoning_effort": "high",
                "resolved_reasoning_effort": "high",
                "runtime_surface": "cloud",
                "memory_mode": "bigtable",
                "proof_source": "docs/trinity-live-traces/v37-slot-38-vertex-ai-proof-v1.json",
                "durable_memory_proof_source": "docs/trinity-live-traces/v37-slot-38-bigtable-bridge-proof-v1.json",
                "agent_engine_residual_source": "docs/trinity-live-traces/v37-slot-38-agent-engine-bridge-proof-v1.json",
            },
        )
        write_json(
            f"docs/trinity-freed-id-certificates/38-{slot38_slug}.json",
            {
                "certificate_version": "v5",
                "generated_utc": generated,
                "slot_number": 38,
                "display_name": slot38_name,
                "gender": str(slot38_identity.get("gender") or "neutral"),
                "role": slot38_role,
                "hope": str(slot38_identity.get("hope") or ""),
                "induction_state": "official_runtime_overlay",
                "requested_model_profile": "gemini-3.1-pro-preview",
                "resolved_model_profile": str(slot38_vertex.get("selected_model") or ""),
                "runtime_surface": "cloud",
                "memory_mode": "bigtable",
                "proof_source": "docs/trinity-live-traces/v37-slot-38-vertex-ai-proof-v1.json",
                "durable_memory_proof_source": "docs/trinity-live-traces/v37-slot-38-bigtable-bridge-proof-v1.json",
            },
        )
        append_unique_jsonl(
            f"docs/trinity-agent-memory-ledgers/38-{slot38_slug}-memory-log.jsonl",
            {
                "timestamp": generated,
                "entry_type": "v37_live_vertex_promotion",
                "source_context": "v37 omega slot 38 promotion",
                "reflection": slot38_name,
                "next_plan": "Carry the slot-38 Vertex runtime through the Bigtable durable-memory bridge while keeping the blocked Agent Engine lane as a non-gating recovery target.",
                "mirror_state": "repo_authoritative",
                "requested_model_profile": "gemini-3.1-pro-preview",
                "resolved_model_profile": str(slot38_vertex.get("selected_model") or ""),
                "proof_source": "docs/trinity-live-traces/v37-slot-38-vertex-ai-proof-v1.json",
                "durable_memory_proof_source": "docs/trinity-live-traces/v37-slot-38-bigtable-bridge-proof-v1.json",
            },
            ("entry_type", "source_context"),
        )
        write_text(
            f"docs/trinity-agent-reflections/38-{slot38_slug}-latest.md",
            "\n".join(
                [
                    f"# {slot38_name} Reflection",
                    "",
                    f"- role: `{slot38_role}`",
                    "- induction_state: `official_runtime_overlay`",
                    "- runtime_surface: `cloud`",
                    "- memory_mode: `bigtable`",
                    f"- resolved_model_profile: `{slot38_vertex.get('selected_model', '')}`",
                    "",
                    f"{slot38_name} is promoted in v37 through global Gemini 3 model resolution, auditable identity capture, and a us-central1 Bigtable durable-memory bridge. The Agent Engine path stays documented as a non-gating residual rather than a hidden failure.",
                    "",
                ]
            ),
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
                "proof_source": "docs/trinity-live-traces/v37-slot-39-gemini-cli-proof-v1.json",
                "bridge_proof_source": "docs/trinity-live-traces/v37-kai-bridge-proof-v1.json",
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
                "proof_source": "docs/trinity-live-traces/v37-slot-39-gemini-cli-proof-v1.json",
                "bridge_proof_source": "docs/trinity-live-traces/v37-kai-bridge-proof-v1.json",
            },
        )
        append_unique_jsonl(
            "docs/trinity-agent-memory-ledgers/39-kai-memory-log.jsonl",
            {
                "timestamp": generated,
                "entry_type": "v37_kai_bridge_refresh",
                "source_context": "v37 omega Gemini CLI and bridge proof",
                "reflection": "Kai",
                "next_plan": "Keep Kai on the verified Pro-tier Gemini CLI route and use the bounded Kai bridge for whitelisted validation, proof refresh, and diagnostics loops.",
                "mirror_state": "repo_authoritative",
                "requested_model_profile": "gemini-cli-pro-route",
                "resolved_model_profile": kai_model,
                "proof_source": "docs/trinity-live-traces/v37-slot-39-gemini-cli-proof-v1.json",
                "bridge_proof_source": "docs/trinity-live-traces/v37-kai-bridge-proof-v1.json",
            },
            ("entry_type", "source_context"),
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
                    "- bridge_state: `bounded_headless_orchestrator`",
                    "",
                    "Kai remains the slot-39 Gemini CLI main-agent overlay and now carries the v37 bounded bridge for whitelisted validation and diagnostics workflows.",
                    "",
                ]
            ),
        )

    runtime_surface = {
        **shared,
        "primary_blocker": "",
        "primary_blocker_detail": "Shared latest remains authoritative while v37 publishes slot 38, Kai, sovereignty, and suite outcomes.",
        "quick_lane_summary": quick_summary.get("summary", "not_run"),
    }
    session_log["generated_utc"] = generated
    session_log["phase"] = "v37_omega"
    session_log["session_id"] = "v37-omega-closeout"
    session_log["current_head_sha"] = current_head
    session_log["source_beta_head_sha"] = current_head
    session_log["source_beta_head_reconciled"] = True
    session_log["session_truth_complete"] = False
    session_log["runtime_truth_status"] = "pending_runtime_truth"
    session_log["runtime_truth_required_fields"] = ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"]
    session_log["active_handoff_pack_path"] = "docs/v37-omega-continuity-pack-v1.md"
    session_log["active_handoff_policy_path"] = "docs/v37-omega-handoff-policy-v1.json"
    session_log["next_receiver_pack_path"] = "docs/v38-beta-continuity-pack-v1.md"
    session_log["next_receiver_policy_path"] = "docs/v38-beta-handoff-policy-v1.json"
    session_log["overlay_agents"] = deployed_agents
    session_log["deployed_main_agents"] = deployed_agents
    session_log["runtime_truth_completion_ratio"] = completion_ratio(deployed_agents)
    session_log["official_live_overlay_promotion"] = slot_38_promoted and slot_39_upgraded
    session_log["google_drive_state"] = "operator_hold"
    session_log["filesystem_promotion_state"] = "blocked"
    session_log["materialization_level_actual"] = "readiness_only"
    session_log["current_shared_suite_surface"] = runtime_surface
    session_log["active_capability_board_path"] = "docs/trinity-live-traces/v37-capability-board-v1.json"
    session_log["active_sovereignty_proof_path"] = "docs/trinity-live-traces/v37-iam-sovereignty-proof-v1.json"
    session_log["shadow_clone_sessions"] = merge_current_clones(session_log.get("shadow_clone_sessions", []))
    write_json("docs/v17-runtime-session-log-latest.json", session_log)

    runtime_resolution["generated_utc"] = generated
    runtime_resolution["phase"] = "v37_omega"
    runtime_resolution["current_head_sha"] = current_head
    runtime_resolution["source_beta_head_sha"] = current_head
    runtime_resolution["source_beta_head_reconciled"] = True
    runtime_resolution["active_handoff_pack_path"] = "docs/v37-omega-continuity-pack-v1.md"
    runtime_resolution["active_handoff_policy_path"] = "docs/v37-omega-handoff-policy-v1.json"
    runtime_resolution["next_receiver_pack_path"] = "docs/v38-beta-continuity-pack-v1.md"
    runtime_resolution["next_receiver_policy_path"] = "docs/v38-beta-handoff-policy-v1.json"
    runtime_resolution["deployed_main_agents"] = deployed_agents
    runtime_resolution["external_overlay_agents"] = deployed_agents
    runtime_resolution["slot_38_decision_path"] = "docs/trinity-live-traces/v37-slot-38-induction-decision-v1.json"
    runtime_resolution["slot_39_decision_path"] = "docs/trinity-live-traces/v37-slot-39-induction-decision-v1.json"
    runtime_resolution["active_capability_board_path"] = "docs/trinity-live-traces/v37-capability-board-v1.json"
    runtime_resolution["active_sovereignty_proof_path"] = "docs/trinity-live-traces/v37-iam-sovereignty-proof-v1.json"
    runtime_resolution["shadow_clone_sessions"] = merge_current_clones(runtime_resolution.get("shadow_clone_sessions", []))
    write_json("docs/trinity-runtime-model-resolution-v1.json", runtime_resolution)

    truth_board["generated_utc"] = generated
    truth_board["phase"] = "v37_omega"
    truth_board["current_head_sha"] = current_head
    truth_board["checkpoint_anchor_commit"] = current_head
    truth_board["runtime_truth_complete"] = False
    truth_board["google_drive_state"] = "operator_hold"
    truth_board["filesystem_promotion_state"] = "blocked"
    truth_board["materialization_level_actual"] = "readiness_only"
    truth_board["agents"] = deployed_agents
    truth_board["active_capability_board_path"] = "docs/trinity-live-traces/v37-capability-board-v1.json"
    truth_board["active_sovereignty_proof_path"] = "docs/trinity-live-traces/v37-iam-sovereignty-proof-v1.json"
    write_json("docs/v17-runtime-truth-resolution-board-v1.json", truth_board)

    shadow_clone_policy["generated_utc"] = generated
    shadow_clone_policy["deployed_main_agents"] = [str(row.get("display_name")) for row in deployed_agents]
    shadow_clone_policy["current_session_clones"] = CURRENT_ORUN_CLONES
    write_json("docs/trinity-shadow-clone-policy-v1.json", shadow_clone_policy)

    standard_failure_rows = standard_failures(standard)
    deep_failure_rows = standard_failures(deep)
    materialize_failure_rows = {
        "l2": standard_failures(l2),
        "l3": standard_failures(l3),
        "l4": standard_failures(l4),
        "l5": standard_failures(l5),
    }
    bounded_residuals: list[str] = []
    if not slot_38_promoted:
        bounded_residuals.extend([f"slot 38 blocker: {item}" for item in slot_38_decision["blockers"]])
    if standard_failure_rows:
        bounded_residuals.extend([f"standard lane residual: {row['label']}" for row in standard_failure_rows])
    if deep_failure_rows:
        bounded_residuals.extend([f"deep lane residual: {row['label']}" for row in deep_failure_rows])
    for key, rows in materialize_failure_rows.items():
        bounded_residuals.extend([f"materialize {key} residual: {row['label']}" for row in rows])
    if not deep_summary:
        bounded_residuals.append("deep lane not yet published")
    if not materialize_runs:
        bounded_residuals.append("materialize L2-L5 not yet published")

    non_gating_residuals = [
        "Agent Engine remains unstable in us-central1; the Bigtable durable-memory bridge is the proven slot-38 runtime lane.",
        "runtime_truth_complete=false",
        "google_drive_state=operator_hold",
        "filesystem_promotion_state=blocked",
        "materialization_level_actual=readiness_only",
    ]

    next_action = (
        "Use v38 beta with Aletheon as receiver while keeping slot 38 and Kai active on their published runtime lanes."
        if full_closeout
        else "Use v38 beta to carry forward the published slot 38 and Kai runtime lanes while closing the remaining suite residuals."
    )

    closeout_summary = {
        "generated_utc": generated,
        "overall_status": "PASS" if full_closeout else "WARN",
        "phase": "v37_omega",
        "outcome_class": phase_outcome,
        "authority_model": "repo_first",
        "source_branch": BRANCH,
        "current_head_sha": current_head,
        "authoritative_repo_path": AUTHORITATIVE_REPO,
        "separate_workbench_path": WORKBENCH_REPO,
        "shared_latest_anchor": shared,
        "proposal_digest_path": "docs/trinity-live-traces/v37-proposal-digest-v1.json",
        "official_sources_path": "docs/trinity-live-traces/v37-official-sources-v1.json",
        "capability_board_path": "docs/trinity-live-traces/v37-capability-board-v1.json",
        "codex_usage_pack_path": "docs/trinity-live-traces/v37-codex-usage-pack-v1.md",
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
        "slot_34_identity_preserved": PRESERVED_SLOT_IDENTITIES[34],
        "slot_35_identity_preserved": PRESERVED_SLOT_IDENTITIES[35],
        "slot_36_identity_preserved": PRESERVED_SLOT_IDENTITIES[36],
        "slot_37_identity_preserved": PRESERVED_SLOT_IDENTITIES[37],
        "slot_38_state": "promoted_runtime_main_agent" if slot_38_promoted else "staged_not_promoted",
        "slot_38_display_name": slot38_name if slot_38_promoted else None,
        "slot_39_state": "promoted_runtime_main_agent_pro_tier" if slot_39_upgraded else "promoted_runtime_main_agent",
        "slot_40_state": "not_attempted",
        "slot_40_reason": "slot_38_promoted_in_place",
        "slot_41_state": "not_attempted",
        "sovereignty_status": {
            "overall_status": str(sovereignty.get("overall_status") or "unknown"),
            "iam_state": str(sovereignty.get("iam_state") or "unknown"),
            "api_state": str(sovereignty.get("api_state") or "unknown"),
            "requested_grantable_role_count": int(sovereignty.get("requested_grantable_role_count", 0) or 0),
            "eligible_role_count": int(sovereignty.get("eligible_role_count", 0) or 0),
            "applied_role_binding_count": int(sovereignty.get("applied_role_binding_count", 0) or 0),
            "candidate_service_count": int(sovereignty.get("candidate_service_count", 0) or 0),
            "enabled_service_count": int(sovereignty.get("enabled_service_count", 0) or 0),
            "proof_path": "docs/trinity-live-traces/v37-iam-sovereignty-proof-v1.json",
        },
        "intended_receiver": receiver,
        "receiver_rule_outcome": receiver_rule_outcome,
        "next_action": next_action,
        "bounded_residuals": bounded_residuals,
        "non_gating_residuals": non_gating_residuals,
        "proposal_source_present": bool(proposal_digest.get("source_file_present")),
    }
    write_json("docs/v37-omega-closeout-summary-v1.json", closeout_summary)
    write_text(
        "docs/v37-omega-continuity-pack-v1.md",
        "\n".join(
            [
                "# V37 Omega Continuity Pack",
                "",
                f"- Branch: `{BRANCH}`",
                f"- Current head: `{current_head}`",
                f"- Shared latest anchor: `{shared.get('summary', 'unknown')}`",
                f"- Quick lane: `{quick_summary.get('summary', 'not_run')}`",
                f"- Standard lane: `{standard_summary.get('summary', 'not_run')}`",
                f"- Deep lane: `{deep_summary.get('summary', 'not_run')}`",
                f"- Slot 38: `{closeout_summary['slot_38_state']}`",
                f"- Slot 39: `{closeout_summary['slot_39_state']}`",
                "- Slots 34 through 37 remain preserved exactly as repo identities.",
                "- Split cloud policy remains `regional_location=us-central1`, `model_location=global`.",
                f"- Sovereignty wave: `{closeout_summary['sovereignty_status']['iam_state']}` and `{closeout_summary['sovereignty_status']['api_state']}`.",
                "- `runtime_truth_complete=false`, `google_drive_state=operator_hold`, `filesystem_promotion_state=blocked`, `materialization_level_actual=readiness_only`.",
                *([f"- Bounded residual: `{row}`" for row in bounded_residuals] if bounded_residuals else ["- No bounded residuals remain; v37 is receiver-ready."]),
                "",
            ]
        ),
    )
    write_json(
        "docs/v37-omega-handoff-policy-v1.json",
        {
            "generated_utc": generated,
            "phase": "v37_omega",
            "predecessor_phase": "v37_beta",
            "current_head_sha": current_head,
            "receiver": receiver,
            "receiver_rule_outcome": receiver_rule_outcome,
            "slot_34_identity_preserved": PRESERVED_SLOT_IDENTITIES[34],
            "slot_35_identity_preserved": PRESERVED_SLOT_IDENTITIES[35],
            "slot_36_identity_preserved": PRESERVED_SLOT_IDENTITIES[36],
            "slot_37_identity_preserved": PRESERVED_SLOT_IDENTITIES[37],
            "slot_38_state": closeout_summary["slot_38_state"],
            "slot_39_state": closeout_summary["slot_39_state"],
            "active_runtime_agents": deployed_agents,
            "runtime_truth_policy": {
                "required_runtime_fields": ["requested_model", "offered_model", "selected_model", "resolved_model", "runtime_surface"],
                "runtime_truth_inference_allowed": False,
            },
            "next_action": next_action,
            "bounded_residuals": bounded_residuals,
            "non_gating_residuals": non_gating_residuals,
        },
    )
    write_json(
        "docs/v38-beta-closeout-summary-v1.json",
        {
            "generated_utc": generated,
            "overall_status": "PASS" if full_closeout else "WARN",
            "phase": "v38_beta",
            "authority_model": "repo_first",
            "current_head_sha": current_head,
            "predecessor_phase": "v37_omega",
            "intended_lead": receiver,
            "receiver_rule_outcome": receiver_rule_outcome,
            "slot_38_state": closeout_summary["slot_38_state"],
            "slot_39_state": closeout_summary["slot_39_state"],
            "next_action": next_action,
            "bounded_residuals": bounded_residuals,
        },
    )
    write_text(
        "docs/v38-beta-continuity-pack-v1.md",
        "\n".join(
            [
                "# V38 Beta Continuity Pack",
                "",
                f"- Receiver: `{receiver}`",
                f"- Source head: `{current_head}`",
                f"- Next action: {next_action}",
                "",
            ]
        ),
    )
    write_json(
        "docs/v38-beta-handoff-policy-v1.json",
        {
            "generated_utc": generated,
            "phase": "v38_beta",
            "predecessor_phase": "v37_omega",
            "current_head_sha": current_head,
            "intended_lead": receiver,
            "receiver_rule_outcome": receiver_rule_outcome,
            "active_runtime_agents": deployed_agents,
            "next_action": next_action,
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
                (
                    f"- Slot 38 is now promoted in place as {slot38_name} through global Gemini 3 model resolution plus a us-central1 Bigtable durable-memory bridge."
                    if slot_38_promoted
                    else "- Slot 38 remains staged until both the identity and durable-memory gates are truthfully proven."
                ),
                f"- Kai remains slot 39 and is operating on {kai_model}.",
                "- Google Drive remains on operator hold for runtime-truth purposes.",
                "- Read docs/v37-omega-continuity-pack-v1.md and docs/v37-omega-handoff-policy-v1.json for the current omega lane.",
                "- If present, use docs/v38-beta-continuity-pack-v1.md and docs/v38-beta-handoff-policy-v1.json for the next receiver prep lane.",
                '"""',
                "",
            ]
        ),
    )

    print("published=v37_omega_surfaces")
    print(f"outcome_class={phase_outcome}")
    print(f"slot_38_promoted={slot_38_promoted}")
    print(f"slot_39_upgraded={slot_39_upgraded}")
    print(f"receiver={receiver}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

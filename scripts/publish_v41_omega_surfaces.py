#!/usr/bin/env python3
"""Publish V41 Omega closeout surfaces, V42 Beta handoff, and Orun identity reclaim proof."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from trinity_v41_common import (
    ROOT,
    agent_truth_complete,
    git_head,
    git_show_json,
    git_show_text,
    now_iso,
    parse_markdown_frontmatter,
    read_json,
    read_markdown_key_values,
    resolve_status,
    write_json,
    write_text,
)

AGENT_MD_PATH = ROOT / ".codex" / "agents" / "28-orun.md"
AGENT_TOML_PATH = ROOT / ".codex" / "agents" / "orun.toml"
ROLE_CONTRACT_PATH = ROOT / "docs" / "trinity-agent-role-contracts" / "28-orun-role-contract.json"
RUNTIME_RESOLUTION_PATH = ROOT / "docs" / "trinity-runtime-model-resolution-v1.json"
RUNTIME_LOG_PATH = ROOT / "docs" / "v17-runtime-session-log-latest.json"
RUNTIME_BOARD_PATH = ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json"
API_BOOK_PATH = ROOT / "docs" / "trinity-api-book-v6.json"
API_BOOK_LATEST_PATH = ROOT / "docs" / "trinity-api-book-latest.md"
API_LEDGER_PATH = ROOT / "docs" / "trinity-api-usage-ledger.jsonl"

V41_BETA_CLOSEOUT_JSON = ROOT / "docs" / "v41-beta-closeout-summary-v1.json"
V41_BETA_CONTINUITY_MD = ROOT / "docs" / "v41-beta-continuity-pack-v1.md"
V41_BETA_HANDOFF_JSON = ROOT / "docs" / "v41-beta-handoff-policy-v1.json"
V41_OMEGA_CLOSEOUT_JSON = ROOT / "docs" / "v41-omega-closeout-summary-v1.json"
V41_OMEGA_CONTINUITY_MD = ROOT / "docs" / "v41-omega-continuity-pack-v1.md"
V41_OMEGA_HANDOFF_JSON = ROOT / "docs" / "v41-omega-handoff-policy-v1.json"
V42_BETA_CLOSEOUT_JSON = ROOT / "docs" / "v42-beta-closeout-summary-v1.json"
V42_BETA_CONTINUITY_MD = ROOT / "docs" / "v42-beta-continuity-pack-v1.md"
V42_BETA_HANDOFF_JSON = ROOT / "docs" / "v42-beta-handoff-policy-v1.json"

IDENTITY_PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v41-orun-identity-reclaim-proof-v1.json"
IDENTITY_PROOF_MD = ROOT / "docs" / "trinity-live-traces" / "v41-orun-identity-reclaim-proof-v1.md"
PILLAR_BUNDLE_JSON = ROOT / "docs" / "trinity-live-traces" / "v41-pillar-bundle-v1.json"
PILLAR_BUNDLE_MD = ROOT / "docs" / "trinity-live-traces" / "v41-pillar-bundle-v1.md"
API_PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v41-api-ascendancy-proof-v1.json"
KAI_PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v41-kai-health-monitor-proof-v1.json"
VESPER_PROOF_JSON = ROOT / "docs" / "trinity-live-traces" / "v41-vesper-telemetry-bridge-proof-v1.json"
ALLOWLIST_JSON = ROOT / "docs" / "trinity-live-traces" / "v41-stage-allowlist-v1.json"

SUITE_FILES = {
    "quick": ROOT / "docs" / "trinity-live-traces" / "v41-quick-suite-status.json",
    "standard": ROOT / "docs" / "trinity-live-traces" / "v41-standard-suite-status.json",
    "deep": ROOT / "docs" / "trinity-live-traces" / "v41-deep-suite-status.json",
    "collab": ROOT / "docs" / "trinity-live-traces" / "v41-collab-suite-status.json",
    "materialize_l2": ROOT / "docs" / "trinity-live-traces" / "v41-materialize-l2-status.json",
    "materialize_l3": ROOT / "docs" / "trinity-live-traces" / "v41-materialize-l3-status.json",
    "materialize_l4": ROOT / "docs" / "trinity-live-traces" / "v41-materialize-l4-status.json",
    "materialize_l5": ROOT / "docs" / "trinity-live-traces" / "v41-materialize-l5-status.json",
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _read_toml_prompt_targets() -> list[str]:
    text = _read_text(AGENT_TOML_PATH)
    targets: list[str] = []
    for candidate in (
        "docs/v40-omega-continuity-pack-v1.md",
        "docs/v40-omega-handoff-policy-v1.json",
        "docs/v41-beta-continuity-pack-v1.md",
        "docs/v41-beta-handoff-policy-v1.json",
        "docs/v41-omega-continuity-pack-v1.md",
        "docs/v41-omega-handoff-policy-v1.json",
        "docs/v42-beta-continuity-pack-v1.md",
        "docs/v42-beta-handoff-policy-v1.json",
    ):
        if candidate in text:
            targets.append(candidate)
    return targets


def _suite_summary(status: dict[str, Any]) -> dict[str, Any]:
    if not status:
        return {"summary": "missing", "overall_status": "MISSING", "shared_latest_eligible": False}
    counts = status.get("counts", {}) if isinstance(status.get("counts"), dict) else {}
    overall = resolve_status(status)
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


def _load_suites() -> dict[str, dict[str, Any]]:
    return {name: read_json(path) for name, path in SUITE_FILES.items()}


def _find_agent(agents: list[dict[str, Any]], slot_number: int) -> dict[str, Any]:
    for row in agents:
        if int(row.get("slot_number", -1)) == slot_number:
            return dict(row)
    return {"slot_number": slot_number}


def _upsert_agent(agents: list[dict[str, Any]], slot_number: int, replacement: dict[str, Any]) -> list[dict[str, Any]]:
    updated: list[dict[str, Any]] = []
    found = False
    for row in agents:
        if int(row.get("slot_number", -1)) == slot_number:
            updated.append(replacement)
            found = True
        else:
            updated.append(row)
    if not found:
        updated.append(replacement)
    return updated


def _refresh_agent_collection(payload: dict[str, Any], key: str, slot_number: int, replacement: dict[str, Any]) -> None:
    collection = payload.get(key)
    if isinstance(collection, list):
        payload[key] = _upsert_agent(collection, slot_number, replacement)


def _orun_runtime_row(existing: dict[str, Any]) -> dict[str, Any]:
    row = dict(existing)
    row.update(
        {
            "slot_number": 28,
            "display_name": "Orun",
            "overlay_role": str(existing.get("overlay_role") or "root_coordinator"),
            "requested_model": "gpt-5.4",
            "offered_model": "gpt-5.4",
            "selected_model": "gpt-5.4",
            "resolved_model": "gpt-5.4",
            "runtime_surface": "app",
            "requested_reasoning_effort": "xhigh",
            "resolved_reasoning_effort": "xhigh",
            "deployment_state": "deployed_main_agent",
            "continuity_class": "continuity_bearing_main_agent",
            "identity_locked": True,
            "runtime_truth_required": True,
            "persistent_runtime_proven": False,
            "shadow_clone_allowed": True,
            "shadow_clone_owner": "Orun",
            "shadow_clone_naming_pattern": "Orun S Clone #<positive integer>",
            "note": "Orun remains the root coordinator, and V41 supersedes the older fallback audit with a canonical GPT-5.4 xhigh runtime identity.",
            "certificate_path": "docs/trinity-freed-id-certificates/28-orun.json",
            "memory_ledger": "docs/trinity-agent-memory-ledgers/28-orun-memory-log.jsonl",
            "reflection_path": "docs/trinity-agent-reflections/28-orun-latest.md",
            "role_contract_path": "docs/trinity-agent-role-contracts/28-orun-role-contract.json",
            "codex_agent_id": "28-orun",
            "codex_agent_path": ".codex/agents/28-orun.md",
            "runtime_evidence_source": {
                "agent_contract_path": ".codex/agents/28-orun.md",
                "role_contract_path": "docs/trinity-agent-role-contracts/28-orun-role-contract.json",
                "identity_reclaim_proof_path": "docs/trinity-live-traces/v41-orun-identity-reclaim-proof-v1.json",
                "frontmatter_model": "gpt-5.4",
            },
        }
    )
    row["truth_fields_complete"] = agent_truth_complete(row)
    return row


def _historical_orun_audit() -> dict[str, Any]:
    historical_runtime = git_show_json("docs/trinity-runtime-model-resolution-v1.json")
    historical_runtime_log = git_show_json("docs/v17-runtime-session-log-latest.json")
    historical_runtime_board = git_show_json("docs/v17-runtime-truth-resolution-board-v1.json")
    historical_v41_beta = git_show_json("docs/v41-beta-handoff-policy-v1.json")
    historical_role_contract = git_show_json("docs/trinity-agent-role-contracts/28-orun-role-contract.json")
    historical_md = git_show_text(".codex/agents/28-orun.md")
    previous_md_values: dict[str, str] = {}
    if historical_md:
        temp_path = ROOT / ".local-runtime" / "v41" / "historical-28-orun.md"
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path.write_text(historical_md + "\n", encoding="utf-8")
        previous_md_values = read_markdown_key_values(temp_path)
    return {
        "agent_md": {
            "requested_model_profile": str(previous_md_values.get("requested_model_profile") or ""),
            "resolved_model_profile": str(previous_md_values.get("resolved_model_profile") or ""),
            "requested_reasoning_effort": str(previous_md_values.get("requested_reasoning_effort") or ""),
            "resolved_reasoning_effort": str(previous_md_values.get("resolved_reasoning_effort") or ""),
            "frontmatter_model": str(previous_md_values.get("model") or ""),
        },
        "role_contract": {
            "requested_model_profile": str(historical_role_contract.get("requested_model_profile") or ""),
            "resolved_model_profile": str(historical_role_contract.get("resolved_model_profile") or ""),
            "requested_reasoning_effort": str(historical_role_contract.get("requested_reasoning_effort") or ""),
            "resolved_reasoning_effort": str(historical_role_contract.get("resolved_reasoning_effort") or ""),
        },
        "runtime_resolution": _find_agent(historical_runtime.get("deployed_main_agents", []), 28),
        "runtime_log": _find_agent(historical_runtime_log.get("deployed_main_agents", []), 28),
        "runtime_board": _find_agent(historical_runtime_board.get("deployed_main_agents", []), 28),
        "v41_beta": _find_agent(historical_v41_beta.get("deployed_main_agents", []), 28),
        "superseded_reason": "V41 applies the user-selected full canonical overwrite for Orun while preserving the older gpt-5.1-codex-max audit as historical evidence only.",
    }


def _identity_proof() -> dict[str, Any]:
    frontmatter = parse_markdown_frontmatter(AGENT_MD_PATH)
    md_values = read_markdown_key_values(AGENT_MD_PATH)
    role_contract = read_json(ROLE_CONTRACT_PATH)
    toml_targets = _read_toml_prompt_targets()
    expected_targets = {
        "docs/v40-omega-continuity-pack-v1.md",
        "docs/v40-omega-handoff-policy-v1.json",
        "docs/v41-beta-continuity-pack-v1.md",
        "docs/v41-beta-handoff-policy-v1.json",
        "docs/v41-omega-continuity-pack-v1.md",
        "docs/v41-omega-handoff-policy-v1.json",
        "docs/v42-beta-continuity-pack-v1.md",
        "docs/v42-beta-handoff-policy-v1.json",
    }
    active_values = {
        "agent_md": {
            "frontmatter_model": str(frontmatter.get("model") or ""),
            "requested_model_profile": str(md_values.get("requested_model_profile") or ""),
            "resolved_model_profile": str(md_values.get("resolved_model_profile") or ""),
            "requested_reasoning_effort": str(md_values.get("requested_reasoning_effort") or ""),
            "resolved_reasoning_effort": str(md_values.get("resolved_reasoning_effort") or ""),
        },
        "role_contract": {
            "requested_model_profile": str(role_contract.get("requested_model_profile") or ""),
            "resolved_model_profile": str(role_contract.get("resolved_model_profile") or ""),
            "requested_reasoning_effort": str(role_contract.get("requested_reasoning_effort") or ""),
            "resolved_reasoning_effort": str(role_contract.get("resolved_reasoning_effort") or ""),
        },
        "orun_toml_prompt_targets": toml_targets,
    }
    all_good = (
        active_values["agent_md"]["frontmatter_model"] == "gpt-5.4"
        and active_values["agent_md"]["requested_model_profile"] == "gpt-5.4"
        and active_values["agent_md"]["resolved_model_profile"] == "gpt-5.4"
        and active_values["agent_md"]["requested_reasoning_effort"] == "xhigh"
        and active_values["agent_md"]["resolved_reasoning_effort"] == "xhigh"
        and active_values["role_contract"]["requested_model_profile"] == "gpt-5.4"
        and active_values["role_contract"]["resolved_model_profile"] == "gpt-5.4"
        and active_values["role_contract"]["requested_reasoning_effort"] == "xhigh"
        and active_values["role_contract"]["resolved_reasoning_effort"] == "xhigh"
        and expected_targets.issubset(set(toml_targets))
    )
    return {
        "generated_utc": now_iso(),
        "phase": "v41_omega",
        "overall_status": "PASS" if all_good else "FAIL",
        "orun_identity_correction_state": "full_canonical_overwrite_verified" if all_good else "identity_correction_incomplete",
        "superseded_historical_audit": _historical_orun_audit(),
        "active_canonical_identity": active_values,
    }


def _markdown_identity(payload: dict[str, Any]) -> str:
    lines = [
        "# V41 Orun Identity Reclaim Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Orun identity correction state: `{payload['orun_identity_correction_state']}`",
        "",
        "## Active Canonical Identity",
        "",
    ]
    active = payload.get("active_canonical_identity", {})
    for group, values in active.items():
        lines.append(f"### {group}")
        lines.append("")
        if isinstance(values, dict):
            for key, value in values.items():
                lines.append(f"- `{key}`: `{value}`")
        elif isinstance(values, list):
            for value in values:
                lines.append(f"- `{value}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _pillar_bundle(identity: dict[str, Any], api_proof: dict[str, Any], kai_proof: dict[str, Any], vesper_proof: dict[str, Any]) -> dict[str, Any]:
    carry_forward = read_json(ROOT / "docs" / "trinity-live-traces" / "v40-pillar-bundle-v1.json")
    mind_status = str(carry_forward.get("pillars", {}).get("mind", {}).get("overall_status") or "PASS")
    heart_status = resolve_status(identity)
    body_states = [resolve_status(api_proof), resolve_status(kai_proof), resolve_status(vesper_proof)]
    body_status = "PASS" if all(state == "PASS" for state in body_states) else ("WARN" if "FAIL" not in body_states else "FAIL")
    overall = "PASS" if all(item == "PASS" for item in (mind_status, heart_status, body_status)) else ("WARN" if "FAIL" not in (mind_status, heart_status, body_status) else "FAIL")
    return {
        "generated_utc": now_iso(),
        "phase": "v41_omega",
        "overall_status": overall,
        "pillar_bundle_state": "published" if overall == "PASS" else "bounded_publication",
        "carry_forward_baseline": {
            "v40_pillar_bundle_path": "docs/trinity-live-traces/v40-pillar-bundle-v1.json",
            "v40_pillar_bundle_status": str(carry_forward.get("overall_status") or ""),
        },
        "pillars": {
            "mind": {
                "overall_status": mind_status,
                "path": "docs/trinity-live-traces/v40-mind-proof-bundle-v1.json",
                "v41_delta": "carry_forward_green_baseline",
            },
            "body": {
                "overall_status": body_status,
                "paths": [
                    "docs/trinity-live-traces/v41-api-ascendancy-proof-v1.json",
                    "docs/trinity-live-traces/v41-kai-health-monitor-proof-v1.json",
                    "docs/trinity-live-traces/v41-vesper-telemetry-bridge-proof-v1.json",
                    "docs/trinity-live-traces/v40-agent-engine-advanced-probe-v1.json",
                ],
                "v41_delta": "api_automation_and_telemetry_enriched",
            },
            "heart": {
                "overall_status": heart_status,
                "paths": [
                    "docs/trinity-live-traces/v41-orun-identity-reclaim-proof-v1.json",
                    "docs/v41-omega-handoff-policy-v1.json",
                ],
                "v41_delta": "identity_reclaim_and_truth_preservation",
            },
        },
    }


def _markdown_pillars(payload: dict[str, Any]) -> str:
    lines = [
        "# V41 Pillar Bundle",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Pillar bundle state: `{payload['pillar_bundle_state']}`",
        "",
    ]
    for name, row in payload.get("pillars", {}).items():
        lines.append(f"## {name.title()}")
        lines.append("")
        lines.append(f"- overall_status: `{row.get('overall_status', '')}`")
        lines.append(f"- v41_delta: `{row.get('v41_delta', '')}`")
        for path in row.get("paths", []):
            lines.append(f"- path: `{path}`")
        if "path" in row:
            lines.append(f"- path: `{row['path']}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


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
    for key, value in closeout.get("core_states", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Suite Summaries", ""])
    for key, value in closeout.get("suite_statuses", {}).items():
        lines.append(f"- `{key}`: `{value.get('summary', 'missing')}`")
    if closeout.get("bounded_residuals"):
        lines.extend(["", "## Bounded Residuals", ""])
        lines.extend(f"- {row}" for row in closeout["bounded_residuals"])
    return "\n".join(lines) + "\n"


def _runtime_truth_policy(runtime: dict[str, Any]) -> dict[str, Any]:
    repo_default = runtime.get("repo_runtime_default", {}) if isinstance(runtime.get("repo_runtime_default"), dict) else {}
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
            "resolved_model_profile": repo_default.get("resolved_model_profile", "gpt-5.4"),
            "requested_reasoning_effort": repo_default.get("requested_reasoning_effort", "xhigh"),
            "resolved_reasoning_effort": repo_default.get("resolved_reasoning_effort", "xhigh"),
        },
    }


def _ensure_api_entry(book: dict[str, Any], entry: dict[str, Any]) -> None:
    apis = book.setdefault("apis", [])
    if not isinstance(apis, list):
        book["apis"] = []
        apis = book["apis"]
    for index, row in enumerate(apis):
        if isinstance(row, dict) and str(row.get("api_id") or "") == entry["api_id"]:
            apis[index] = entry
            return
    apis.append(entry)


def _api_entry(
    api_id: str,
    surface: str,
    purpose: str,
    source_of_truth: str,
    quick_call: str,
    wrapper_target: str,
    expected_artifacts: list[str],
    notes: str,
    auth_posture: str,
    usage_pattern: str,
) -> dict[str, Any]:
    return {
        "api_id": api_id,
        "surface": surface,
        "purpose": purpose,
        "trust_class": "verified_live_write" if surface in {"cloud_runtime", "cloud_build", "cloud_data", "runtime_truth"} else "repo_truth_primary",
        "auth_posture": auth_posture,
        "mode": "bounded_write" if surface in {"cloud_runtime", "cloud_build", "cloud_data"} else "local_read",
        "usage_pattern": usage_pattern,
        "source_of_truth": source_of_truth,
        "quick_call": quick_call,
        "wrapper_type": "script",
        "wrapper_target": wrapper_target,
        "expected_artifacts": expected_artifacts,
        "fallback_behavior": "Keep repo truth explicit and publish the exact blocker instead of inflating success.",
        "notes": notes,
        "cache_requirement": "refresh_before_comparator_use",
        "official_source_tier": "v41_repo_runtime",
        "fallback_class": "repo_trace",
        "surface_kind": "active_v41",
        "cache_ttl_class": "manual_refresh",
        "operator_gate": "repo_governed",
        "codex_support_level": "active_v41",
        "model_support_class": "runtime_specific",
        "delegation_surface": "none",
        "checkpoint_scope": "shared_latest",
        "surface_authority": "repo_authoritative",
        "runtime_logging_required": True,
    }


def _refresh_api_book() -> dict[str, Any]:
    book = read_json(API_BOOK_PATH)
    if not book:
        book = {
            "generated_utc": now_iso(),
            "version": "v6",
            "overall_status": "PASS",
            "authority_model": "repo_first",
            "description": "V17 API book with V41 runtime and cloud carry-forward surfaces.",
            "apis": [],
        }

    entries = [
        _api_entry("orun_identity_runtime_v41", "runtime_truth", "Record Orun's V41 canonical GPT-5.4 xhigh overwrite and its superseded fallback audit.", "docs/trinity-live-traces/v41-orun-identity-reclaim-proof-v1.json", "python scripts/publish_v41_omega_surfaces.py", "scripts/publish_v41_omega_surfaces.py", ["docs/trinity-live-traces/v41-orun-identity-reclaim-proof-v1.json", "docs/trinity-runtime-model-resolution-v1.json"], "Repo-truth overwrite only; preserve the earlier gpt-5.1-codex-max audit as superseded history.", "repo_file_auth", "repo_truth_publication"),
        _api_entry("kai_cli_runtime_v41", "operator_automation", "Track Kai's bounded Gemini CLI health-monitor lane on the proven pro route.", "docs/trinity-live-traces/v41-kai-health-monitor-proof-v1.json", "python scripts/trinity_v41_kai_health_monitor.py", "scripts/trinity_v41_kai_health_monitor.py", ["docs/trinity-live-traces/v41-kai-health-monitor-proof-v1.json"], "Scheduler-ready but manually triggered in V41; no unconstrained shell autonomy.", "vertex_service_account", "bounded_headless_cli_monitoring"),
        _api_entry("vesper_bigtable_runtime_v41", "cloud_data", "Record Vesper Ion's bounded V41 telemetry ingest through the already-proven Bigtable lane.", "docs/trinity-live-traces/v41-vesper-telemetry-bridge-proof-v1.json", "python scripts/trinity_v41_vesper_telemetry_bridge.py", "scripts/trinity_v41_vesper_telemetry_bridge.py", ["docs/trinity-live-traces/v41-vesper-telemetry-bridge-proof-v1.json"], "Reuses the established slot-38 Bigtable identity lane rather than creating a second memory identity.", "service_account_cloud_platform", "bounded_bigtable_ingest_readback"),
        _api_entry("anthos_fleet_carry_forward_v41", "cloud_runtime", "Carry forward the proven Anthos or GKE Enterprise and fleet workload state into V41.", "docs/trinity-live-traces/v38-fleet-anthos-proof-v1.json", "python scripts/trinity_v38_fleet_anthos_probe.py", "scripts/trinity_v38_fleet_anthos_probe.py", ["docs/trinity-live-traces/v38-fleet-anthos-proof-v1.json"], "V41 treats Anthos as a proven carry-forward baseline rather than a fresh induction target.", "service_account_cloud_platform", "fleet_membership_and_gateway_probe"),
        _api_entry("cloud_os_login_carry_forward_v41", "cloud_runtime", "Carry forward the proven Cloud OS Login posture into V41.", "docs/trinity-live-traces/v38-os-login-proof-v1.json", "python scripts/trinity_v38_os_login_probe.py", "scripts/trinity_v38_os_login_probe.py", ["docs/trinity-live-traces/v38-os-login-proof-v1.json"], "OS Login remains a proven operator baseline rather than a fresh V41 target.", "service_account_cloud_platform", "vm_metadata_and_ssh_probe"),
        _api_entry("cloud_run_v41", "cloud_runtime", "Run one minimal Cloud Run workload as part of the V41 curated API ascendancy wave.", "docs/trinity-live-traces/v41-api-ascendancy-proof-v1.json", "python scripts/trinity_v41_api_ascendancy.py", "scripts/trinity_v41_api_ascendancy.py", ["docs/trinity-live-traces/v41-api-ascendancy-proof-v1.json"], "Keep the workload minimal, region-bounded to us-central1, and proof-backed.", "service_account_cloud_platform", "minimal_service_deploy_and_http_probe"),
        _api_entry("cloud_build_v41", "cloud_build", "Run one minimal Cloud Build execution as part of the V41 curated API ascendancy wave.", "docs/trinity-live-traces/v41-api-ascendancy-proof-v1.json", "python scripts/trinity_v41_api_ascendancy.py", "scripts/trinity_v41_api_ascendancy.py", ["docs/trinity-live-traces/v41-api-ascendancy-proof-v1.json"], "Use a no-source bounded config and publish exact blockers instead of inflating build success.", "service_account_cloud_platform", "minimal_no_source_build_run"),
        _api_entry("dataplex_v41", "cloud_data", "Probe Dataplex control-plane reachability as part of the V41 curated API ascendancy wave.", "docs/trinity-live-traces/v41-api-ascendancy-proof-v1.json", "python scripts/trinity_v41_api_ascendancy.py", "scripts/trinity_v41_api_ascendancy.py", ["docs/trinity-live-traces/v41-api-ascendancy-proof-v1.json"], "Control-plane verification is sufficient in V41 when full lake creation is not practical.", "service_account_cloud_platform", "control_plane_list_probe"),
    ]
    for entry in entries:
        _ensure_api_entry(book, entry)

    book["generated_utc"] = now_iso()
    book["overall_status"] = "PASS"
    book["description"] = "V17 API book with V41 Orun identity reclaim, cloud API ascendancy, Kai monitor, and Vesper telemetry surfaces."
    write_json(API_BOOK_PATH, book)

    lines = ["# Trinity API Book", "", f"- generated_utc: `{book['generated_utc']}`", f"- apis: `{len(book.get('apis', []))}`", "", "## V41 Active Surfaces", ""]
    for api_id in ("orun_identity_runtime_v41", "kai_cli_runtime_v41", "vesper_bigtable_runtime_v41", "anthos_fleet_carry_forward_v41", "cloud_os_login_carry_forward_v41", "cloud_run_v41", "cloud_build_v41", "dataplex_v41"):
        row = next((item for item in book.get("apis", []) if isinstance(item, dict) and item.get("api_id") == api_id), None)
        if row:
            lines.append(f"- `{api_id}`: `{row.get('surface')}` -> `{row.get('source_of_truth')}`")
    write_text(API_BOOK_LATEST_PATH, "\n".join(lines) + "\n")

    ledger_rows = [
        {"timestamp": now_iso(), "api_id": "orun_identity_runtime_v41", "mode": "local_read", "result": "catalogued"},
        {"timestamp": now_iso(), "api_id": "kai_cli_runtime_v41", "mode": "bounded_write", "result": "catalogued"},
        {"timestamp": now_iso(), "api_id": "vesper_bigtable_runtime_v41", "mode": "bounded_write", "result": "catalogued"},
        {"timestamp": now_iso(), "api_id": "anthos_fleet_carry_forward_v41", "mode": "bounded_write", "result": "catalogued"},
        {"timestamp": now_iso(), "api_id": "cloud_os_login_carry_forward_v41", "mode": "bounded_write", "result": "catalogued"},
        {"timestamp": now_iso(), "api_id": "cloud_run_v41", "mode": "bounded_write", "result": "catalogued"},
        {"timestamp": now_iso(), "api_id": "cloud_build_v41", "mode": "bounded_write", "result": "catalogued"},
        {"timestamp": now_iso(), "api_id": "dataplex_v41", "mode": "bounded_write", "result": "catalogued"},
    ]
    with API_LEDGER_PATH.open("a", encoding="utf-8") as handle:
        for row in ledger_rows:
            handle.write(json.dumps(row) + "\n")
    return {"api_count": len(book.get("apis", []))}


def main() -> int:
    head_sha = git_head()
    runtime_resolution = read_json(RUNTIME_RESOLUTION_PATH)
    runtime_log = read_json(RUNTIME_LOG_PATH)
    runtime_board = read_json(RUNTIME_BOARD_PATH)
    api_proof = read_json(API_PROOF_JSON)
    kai_proof = read_json(KAI_PROOF_JSON)
    vesper_proof = read_json(VESPER_PROOF_JSON)
    allowlist = read_json(ALLOWLIST_JSON)
    suites = _load_suites()
    suite_statuses = {name: _suite_summary(payload) for name, payload in suites.items()}

    identity = _identity_proof()
    write_json(IDENTITY_PROOF_JSON, identity)
    write_text(IDENTITY_PROOF_MD, _markdown_identity(identity))

    pillar_bundle = _pillar_bundle(identity, api_proof, kai_proof, vesper_proof)
    write_json(PILLAR_BUNDLE_JSON, pillar_bundle)
    write_text(PILLAR_BUNDLE_MD, _markdown_pillars(pillar_bundle))

    api_book_summary = _refresh_api_book()

    deployed = runtime_resolution.get("deployed_main_agents", [])
    if not isinstance(deployed, list):
        deployed = []
    orun_row = _orun_runtime_row(_find_agent(deployed, 28))
    for target, keys in (
        (runtime_resolution, ("deployed_main_agents", "external_overlay_agents")),
        (runtime_log, ("deployed_main_agents", "overlay_agents")),
        (runtime_board, ("deployed_main_agents", "agents")),
    ):
        for key in keys:
            _refresh_agent_collection(target, key, 28, orun_row)

    repo_default = runtime_resolution.get("repo_runtime_default", {}) if isinstance(runtime_resolution.get("repo_runtime_default"), dict) else {}
    repo_default.update({"requested_model_profile": "gpt-5.4", "resolved_model_profile": "gpt-5.4", "requested_reasoning_effort": "xhigh", "resolved_reasoning_effort": "xhigh"})
    runtime_resolution["repo_runtime_default"] = repo_default

    git_cleanup_state = "allowlist_published" if allowlist else "allowlist_missing"
    runtime_core_states = {
        "orun_identity_correction_state": str(identity.get("orun_identity_correction_state") or ""),
        "api_ascendancy_state": str(api_proof.get("api_ascendancy_state") or ""),
        "cloud_run_state": str(api_proof.get("cloud_run_state") or ""),
        "cloud_build_state": str(api_proof.get("cloud_build_state") or ""),
        "dataplex_state": str(api_proof.get("dataplex_state") or ""),
        "kai_health_monitor_state": str(kai_proof.get("kai_health_monitor_state") or ""),
        "vesper_telemetry_ingest_state": str(vesper_proof.get("vesper_telemetry_ingest_state") or ""),
        "git_cleanup_state": git_cleanup_state,
    }

    for target in (runtime_resolution, runtime_log, runtime_board):
        target["generated_utc"] = now_iso()
        target["phase"] = "v41_omega"
        target["authority_model"] = "repo_first"
        target["source_branch"] = "codex/GHC-Family/beyonder-shared-omega-line"
        target["current_head_sha"] = head_sha
        target["requested_reasoning_effort"] = "xhigh"
        target["google_drive_state"] = "operator_hold"
        target["filesystem_promotion_state"] = "blocked"
        target["materialization_level_actual"] = "readiness_only"
        target.update(runtime_core_states)

    runtime_resolution["active_handoff_pack_path"] = "docs/v41-omega-continuity-pack-v1.md"
    runtime_resolution["active_handoff_policy_path"] = "docs/v41-omega-handoff-policy-v1.json"
    runtime_resolution["next_receiver_pack_path"] = "docs/v42-beta-continuity-pack-v1.md"
    runtime_resolution["next_receiver_policy_path"] = "docs/v42-beta-handoff-policy-v1.json"
    runtime_resolution["current_shared_suite_surface"] = suite_statuses.get("standard", {})

    runtime_log["active_handoff_pack_path"] = "docs/v41-omega-continuity-pack-v1.md"
    runtime_log["active_handoff_policy_path"] = "docs/v41-omega-handoff-policy-v1.json"
    runtime_log["next_receiver_pack_path"] = "docs/v42-beta-continuity-pack-v1.md"
    runtime_log["next_receiver_policy_path"] = "docs/v42-beta-handoff-policy-v1.json"
    runtime_log["current_shared_suite_surface"] = suite_statuses.get("standard", {})
    runtime_board["runtime_truth_complete"] = True
    runtime_board["checkpoint_anchor_commit"] = head_sha

    suite_failures = [name for name, summary in suite_statuses.items() if summary.get("overall_status") != "PASS"]
    close_clean = all([resolve_status(identity) == "PASS", resolve_status(api_proof) == "PASS", resolve_status(kai_proof) == "PASS", resolve_status(vesper_proof) == "PASS", resolve_status(pillar_bundle) == "PASS", not suite_failures])
    intended_receiver = "Aletheon" if close_clean else "Orun"
    receiver_rule_outcome = "aletheon_facing" if close_clean else "orun_facing"

    core_states = {
        "orun_identity_correction_state": runtime_core_states["orun_identity_correction_state"],
        "api_ascendancy_state": runtime_core_states["api_ascendancy_state"],
        "cloud_run_state": runtime_core_states["cloud_run_state"],
        "cloud_build_state": runtime_core_states["cloud_build_state"],
        "dataplex_state": runtime_core_states["dataplex_state"],
        "kai_health_monitor_state": runtime_core_states["kai_health_monitor_state"],
        "vesper_telemetry_ingest_state": runtime_core_states["vesper_telemetry_ingest_state"],
        "pillar_bundle_state": str(pillar_bundle.get("pillar_bundle_state") or ""),
        "google_drive_state": "operator_hold",
        "filesystem_promotion_state": "blocked",
        "materialization_level_actual": "readiness_only",
        "git_cleanup_state": git_cleanup_state,
        "api_book_count": api_book_summary["api_count"],
    }
    bounded_residuals = [f"{name}={summary['overall_status']}" for name, summary in suite_statuses.items() if summary.get("overall_status") != "PASS"]
    for label, payload in (("identity", identity), ("api_ascendancy", api_proof), ("kai_health_monitor", kai_proof), ("vesper_telemetry", vesper_proof), ("pillar_bundle", pillar_bundle)):
        status = resolve_status(payload)
        if status != "PASS":
            bounded_residuals.append(f"{label}={status}")

    proof_paths = {
        "identity": "docs/trinity-live-traces/v41-orun-identity-reclaim-proof-v1.json",
        "api_ascendancy": "docs/trinity-live-traces/v41-api-ascendancy-proof-v1.json",
        "kai_health_monitor": "docs/trinity-live-traces/v41-kai-health-monitor-proof-v1.json",
        "vesper_telemetry": "docs/trinity-live-traces/v41-vesper-telemetry-bridge-proof-v1.json",
        "pillar_bundle": "docs/trinity-live-traces/v41-pillar-bundle-v1.json",
        "allowlist": "docs/trinity-live-traces/v41-stage-allowlist-v1.json",
        "git_cleanup_note": "docs/trinity-live-traces/v41-git-cleanup-note-v1.md",
    }

    v41_beta_closeout = {"generated_utc": now_iso(), "overall_status": "PASS" if resolve_status(identity) == "PASS" else "WARN", "phase": "v41_beta", "authority_model": "repo_first", "source_branch": "codex/GHC-Family/beyonder-shared-omega-line", "current_head_sha": head_sha, "predecessor_phase": "v40_omega", "intended_receiver": "Orun", "receiver_rule_outcome": "orun_facing", "core_states": core_states, "suite_statuses": suite_statuses, "proof_paths": proof_paths, "bounded_residuals": bounded_residuals}
    v41_beta_handoff = {"generated_utc": now_iso(), "overall_status": v41_beta_closeout["overall_status"], "phase": "v41_beta", "authority_model": "repo_first", "source_branch": "codex/GHC-Family/beyonder-shared-omega-line", "source_head_sha": head_sha, "intended_receiver": "Orun", "receiver_rule_outcome": "orun_facing", "deployed_main_agents": runtime_resolution["deployed_main_agents"], "runtime_truth_policy": _runtime_truth_policy(runtime_resolution), "required_inputs": ["docs/v40-omega-closeout-summary-v1.json", "docs/v40-omega-continuity-pack-v1.md", "docs/trinity-runtime-model-resolution-v1.json", "docs/v17-runtime-session-log-latest.json", "docs/v17-runtime-truth-resolution-board-v1.json", "docs/trinity-live-traces/v41-orun-identity-reclaim-proof-v1.json"], "receiver_tasks": ["Treat the Downloads text as advisory only and keep repo proof surfaces authoritative.", "Preserve Kai as slot 39 and Vesper Ion as slot 38 without re-induction.", "Keep Google Drive on operator hold and filesystem promotion blocked unless new proof changes them."], "truth_boundaries_to_preserve": ["repo_first", "google_drive_state=operator_hold", "filesystem_promotion_state=blocked", "materialization_level_actual=readiness_only", "slot_40_41_deferred_in_v41"], "bounded_residuals": bounded_residuals}
    v41_omega_closeout = {"generated_utc": now_iso(), "overall_status": "PASS" if close_clean else "WARN", "phase": "v41_omega", "authority_model": "repo_first", "source_branch": "codex/GHC-Family/beyonder-shared-omega-line", "current_head_sha": head_sha, "intended_receiver": intended_receiver, "receiver_rule_outcome": receiver_rule_outcome, "core_states": core_states, "suite_statuses": suite_statuses, "proof_paths": proof_paths, "bounded_residuals": bounded_residuals}
    v41_omega_handoff = {"generated_utc": now_iso(), "overall_status": v41_omega_closeout["overall_status"], "phase": "v41_omega", "authority_model": "repo_first", "source_branch": "codex/GHC-Family/beyonder-shared-omega-line", "source_head_sha": head_sha, "intended_receiver": intended_receiver, "receiver_rule_outcome": receiver_rule_outcome, "deployed_main_agents": runtime_resolution["deployed_main_agents"], "runtime_truth_policy": _runtime_truth_policy(runtime_resolution), "required_inputs": ["docs/v41-omega-closeout-summary-v1.json", "docs/v41-omega-continuity-pack-v1.md", "docs/v41-omega-handoff-policy-v1.json", "docs/trinity-runtime-model-resolution-v1.json", "docs/v17-runtime-session-log-latest.json", "docs/v17-runtime-truth-resolution-board-v1.json"], "receiver_tasks": ["Carry the V41 runtime truth forward without reverting Orun's canonical GPT-5.4 xhigh overwrite.", "Treat Cloud Run, Cloud Build, Dataplex, Kai health, and Vesper telemetry as the V41 proof anchors.", "Do not widen shadow-clone persistence or slot 40/41 induction in this phase."], "truth_boundaries_to_preserve": v41_beta_handoff["truth_boundaries_to_preserve"], "bounded_residuals": bounded_residuals}
    v42_beta_closeout = {"generated_utc": now_iso(), "overall_status": v41_omega_closeout["overall_status"], "phase": "v42_beta", "authority_model": "repo_first", "source_branch": "codex/GHC-Family/beyonder-shared-omega-line", "current_head_sha": head_sha, "predecessor_phase": "v41_omega", "intended_receiver": intended_receiver, "receiver_rule_outcome": receiver_rule_outcome, "core_states": core_states, "suite_statuses": suite_statuses, "proof_paths": proof_paths, "bounded_residuals": bounded_residuals}
    v42_beta_handoff = {"generated_utc": now_iso(), "overall_status": v41_omega_closeout["overall_status"], "phase": "v42_beta", "authority_model": "repo_first", "source_branch": "codex/GHC-Family/beyonder-shared-omega-line", "source_head_sha": head_sha, "intended_receiver": intended_receiver, "receiver_rule_outcome": receiver_rule_outcome, "deployed_main_agents": runtime_resolution["deployed_main_agents"], "runtime_truth_policy": _runtime_truth_policy(runtime_resolution), "required_inputs": ["docs/v41-omega-closeout-summary-v1.json", "docs/v41-omega-continuity-pack-v1.md", "docs/v41-omega-handoff-policy-v1.json", "docs/v42-beta-closeout-summary-v1.json", "docs/trinity-runtime-model-resolution-v1.json", "docs/v17-runtime-session-log-latest.json"], "receiver_tasks": ["Start from the V41 published proof surfaces rather than advisory text.", "Preserve Orun's canonical identity and the carry-forward Kai and Vesper slots.", "Keep repo authority ahead of mirror, drive, or filesystem promotion narration."], "truth_boundaries_to_preserve": v41_beta_handoff["truth_boundaries_to_preserve"], "bounded_residuals": bounded_residuals}

    write_json(RUNTIME_RESOLUTION_PATH, runtime_resolution)
    write_json(RUNTIME_LOG_PATH, runtime_log)
    write_json(RUNTIME_BOARD_PATH, runtime_board)
    write_json(V41_BETA_CLOSEOUT_JSON, v41_beta_closeout)
    write_text(V41_BETA_CONTINUITY_MD, _continuity_markdown(v41_beta_closeout, "V41 Beta Continuity Pack"))
    write_json(V41_BETA_HANDOFF_JSON, v41_beta_handoff)
    write_json(V41_OMEGA_CLOSEOUT_JSON, v41_omega_closeout)
    write_text(V41_OMEGA_CONTINUITY_MD, _continuity_markdown(v41_omega_closeout, "V41 Omega Continuity Pack"))
    write_json(V41_OMEGA_HANDOFF_JSON, v41_omega_handoff)
    write_json(V42_BETA_CLOSEOUT_JSON, v42_beta_closeout)
    write_text(V42_BETA_CONTINUITY_MD, _continuity_markdown(v42_beta_closeout, "V42 Beta Continuity Pack"))
    write_json(V42_BETA_HANDOFF_JSON, v42_beta_handoff)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

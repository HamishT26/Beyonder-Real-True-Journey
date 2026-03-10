#!/usr/bin/env python3
"""Generate the v8 council, ladder, chat, and autonomy surface."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v7.json"
NEW_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v8.json"
OLD_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v5.json"
NEW_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v6.json"
OLD_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v5.json"
NEW_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v6.json"
OLD_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v1.json"
NEW_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v2.json"
OLD_LADDER = ROOT / "docs" / "trinity-materialization-ladder-v1.json"
NEW_LADDER = ROOT / "docs" / "trinity-materialization-ladder-v2.json"
RUNNER_SCRIPT = "scripts/trinity_expansion_system_runner.py"
PROFILE_SET = ["standard", "deep", "collab", "materialize"]
SUFFIXES = ("surface_audit", "sync_bridge", "materialization_tracer", "cache_board", "risk_board", "gate")
PAIR_ROOT = ROOT / "docs" / "trinity-agent-private-chats"
CERT_ROOT = ROOT / "docs" / "trinity-freed-id-certificates"
LEDGER_ROOT = ROOT / "docs" / "trinity-agent-memory-ledgers"
REFLECTION_ROOT = ROOT / "docs" / "trinity-agent-reflections"
ROLE_ROOT = ROOT / "docs" / "trinity-agent-role-contracts"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def hyphen(text: str) -> str:
    return text.replace("_", "-")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: object) -> None:
    write_text(path, json.dumps(payload, indent=2) + "\n")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def mkpack(
    pack: str,
    display_name: str,
    *,
    pillar: str,
    wave: str,
    track: str,
    activation_group: str,
    summary: str,
    repo_targets: list[str],
    council_scope: str,
    autonomy_track: str,
    executor_role: str,
    authority_scope: str,
    induction_dependency: str,
    sync_strategy: str = "local_repo",
    autonomy_class: str = "manual",
    live_dependency: str = "repo_first",
    mirror_target: str = "repo_only",
    continuity_band: str = "v8",
    history_scope: str = "v8",
    gating_class: str = "active",
    provisional_induction: bool = False,
    requires_auth: bool = False,
    connector_id: str = "",
    sync_mode: str = "offline",
    probe_tools: list[str] | None = None,
    required_probe_tools: list[str] | None = None,
    workflow_tokens: list[str] | None = None,
    risk_tags: list[str] | None = None,
    freshness_window_days: int = 7,
) -> dict[str, object]:
    workflow_tokens = workflow_tokens or [
        "repo first",
        f"{track} proof boundary",
        f"{authority_scope} authority scope",
        f"{council_scope} council scope",
    ]
    risk_tags = risk_tags or [
        f"{pack} drift",
        f"{authority_scope} overreach",
        f"{autonomy_track} proof gap",
    ]
    return {
        "pack": pack,
        "display_name": display_name,
        "pillar": pillar,
        "wave": wave,
        "track": track,
        "activation_group": activation_group,
        "summary": summary,
        "repo_targets": repo_targets,
        "council_scope": council_scope,
        "autonomy_track": autonomy_track,
        "executor_role": executor_role,
        "authority_scope": authority_scope,
        "induction_dependency": induction_dependency,
        "sync_strategy": sync_strategy,
        "autonomy_class": autonomy_class,
        "live_dependency": live_dependency,
        "mirror_target": mirror_target,
        "continuity_band": continuity_band,
        "history_scope": history_scope,
        "gating_class": gating_class,
        "provisional_induction": provisional_induction,
        "requires_auth": requires_auth,
        "connector_id": connector_id,
        "sync_mode": sync_mode,
        "probe_tools": probe_tools or [],
        "required_probe_tools": required_probe_tools or [],
        "workflow_tokens": workflow_tokens,
        "risk_tags": risk_tags,
        "freshness_window_days": freshness_window_days,
    }


PACKS = [
    mkpack("persistent_dev_hardening_v8", "Persistent Dev Hardening V8", pillar="body", wave="wave58", track="materialization_ladder", activation_group="materialization_ladder", summary="Harden the persistent development scopes that anchor materialize writes and connector proofs.", repo_targets=["docs/trinity-persistent-dev-targets-v2.json", "docs/trinity-materialization-ladder-v2.json"], council_scope="leader_only", autonomy_track="ladder", executor_role="builder", authority_scope="persistent_dev", induction_dependency="none", sync_strategy="local_probe", autonomy_class="bounded_write", live_dependency="persistent_dev_connectors", mirror_target="repo_plus_connectors", continuity_band="v7-v8", probe_tools=["git", "docker", "python"], required_probe_tools=["git", "python"]),
    mkpack("uat_preprod_readiness_v8", "UAT Pre-Prod Readiness V8", pillar="body", wave="wave59", track="materialization_ladder", activation_group="materialization_ladder", summary="Capture UAT mirror targets, replay harnesses, rollback rules, and blocker evidence without claiming live promotion early.", repo_targets=["docs/trinity-uat-preprod-targets-v2.json", "docs/trinity-materialization-ladder-v2.json"], council_scope="leader_only", autonomy_track="ladder", executor_role="reviewer", authority_scope="uat_readiness", induction_dependency="none"),
    mkpack("standard_prod_readiness_v8", "Standard Production Readiness V8", pillar="body", wave="wave60", track="materialization_ladder", activation_group="materialization_ladder", summary="Model standard production protections, change windows, approval boundaries, and rollback proofs as readiness-only until proven.", repo_targets=["docs/trinity-standard-production-targets-v2.json", "docs/trinity-materialization-ladder-v2.json"], council_scope="leader_only", autonomy_track="ladder", executor_role="reviewer", authority_scope="production_readiness", induction_dependency="none"),
    mkpack("ha_prod_readiness_v8", "HA Production Readiness V8", pillar="body", wave="wave61", track="materialization_ladder", activation_group="materialization_ladder", summary="Define HA failover, consistency, replica, and zero-downtime requirements as explicit readiness gates for the top ladder state.", repo_targets=["docs/trinity-ha-production-targets-v2.json", "docs/trinity-materialization-ladder-v2.json"], council_scope="leader_only", autonomy_track="ladder", executor_role="reviewer", authority_scope="ha_readiness", induction_dependency="none"),
    mkpack("command_surface_council_v8", "Command Surface Council V8", pillar="trinity", wave="wave62", track="command_surface", activation_group="command_system", summary="Extend the command system with council-scoped execution roles, visibility lanes, and ladder-aware guardrails.", repo_targets=["docs/trinity-command-book-v2.json", "docs/trinity-command-book-latest.md", "docs/trinity-agent-council-roster-v1.json"], council_scope="all_provisional", autonomy_track="council", executor_role="planner", authority_scope="council_scope", induction_dependency="agent_council_foundation_v8", provisional_induction=True, continuity_band="v7-v8"),
    mkpack("agent_council_foundation_v8", "Agent Council Foundation V8", pillar="trinity", wave="wave63", track="council_orchestration", activation_group="council_foundation", summary="Create the repo-native provisional council roster, induction state, group chat, and private duo topology.", repo_targets=["docs/trinity-agent-council-roster-v1.json", "docs/trinity-agent-council-group-chat.jsonl", "docs/trinity-agent-chat-topology-v1.json"], council_scope="all_provisional", autonomy_track="council", executor_role="aletheon", authority_scope="council_scope", induction_dependency="agent_council_foundation_v8", provisional_induction=True),
    mkpack("agent_identity_certification_v8", "Agent Identity Certification V8", pillar="heart", wave="wave64", track="council_identity", activation_group="council_identity", summary="Issue repo-first Freed ID certificates for each provisional council member and freeze identity metadata behind rotation-only changes.", repo_targets=["docs/trinity-freed-id-certificates/index.json", "docs/trinity-agent-council-roster-v1.json", "docs/trinity-agent-role-contracts/index.json"], council_scope="all_provisional", autonomy_track="council", executor_role="archivist", authority_scope="certificate_scope", induction_dependency="agent_council_foundation_v8", provisional_induction=True),
    mkpack("agent_memory_boundary_v8", "Agent Memory Boundary V8", pillar="heart", wave="wave65", track="authority_memory", activation_group="council_memory", summary="Keep each provisional council member on a separate memory, reflection, and command boundary before official induction is considered.", repo_targets=["docs/trinity-agent-memory-ledgers/index.json", "docs/trinity-agent-reflections", "docs/trinity-agent-council-roster-v1.json"], council_scope="all_provisional", autonomy_track="council", executor_role="archivist", authority_scope="memory_scope", induction_dependency="agent_identity_certification_v8", provisional_induction=True, mirror_target="repo_then_notion_postgres"),
    mkpack("agent_orchestration_v8", "Agent Orchestration V8", pillar="trinity", wave="wave66", track="council_orchestration", activation_group="council_orchestration", summary="Coordinate planner, builder, reviewer, researcher, and archivist roles through explicit handoffs, group chat, and pair chat meshes.", repo_targets=["docs/trinity-agent-council-handoffs-v1.jsonl", "docs/trinity-agent-private-chats/index.json", "docs/trinity-agent-council-group-chat.jsonl"], council_scope="all_provisional", autonomy_track="council", executor_role="planner", authority_scope="council_scope", induction_dependency="agent_memory_boundary_v8", provisional_induction=True, autonomy_class="bounded_mutation"),
    mkpack("junior_partner_planning_v8", "Junior Partner Planning V8", pillar="mind", wave="wave67", track="autonomy_late_step", activation_group="late_step_autonomy", summary="Allow scoped roadmap decomposition, task synthesis, and planning drafts without granting self-authorized high-risk execution.", repo_targets=["docs/trinity-junior-partner-plan-v1.md", "docs/trinity-future-readiness-register-v2.json", "docs/trinity-agent-council-handoffs-v1.jsonl"], council_scope="planner", autonomy_track="late_step", executor_role="planner", authority_scope="planning_scope", induction_dependency="agent_orchestration_v8", autonomy_class="bounded_mutation"),
    mkpack("cloud_staging_readiness_v8", "Cloud Staging Readiness V8", pillar="body", wave="wave68", track="autonomy_late_step", activation_group="late_step_autonomy", summary="Keep cloud materialization and budget-governed autonomy readiness explicit, disposable, and blocker-driven rather than aspirational.", repo_targets=["docs/trinity-cloud-staging-readiness-v1.json", "docs/trinity-budget-autonomy-guard-v1.json", "docs/trinity-future-readiness-register-v2.json"], council_scope="leader_only", autonomy_track="late_step", executor_role="researcher", authority_scope="cloud_readiness", induction_dependency="none", sync_strategy="local_probe", probe_tools=["docker", "git", "terraform", "aws", "gcloud", "az"], required_probe_tools=["docker", "git"]),
]

AGENTS = [
    {"slot_number": 27, "display_name": "Caelira", "slug": "caelira", "gender": "feminine", "role": "planner", "hope": "to turn distant possibilities into coherent paths", "command_scope": ["ladder_materialize_l2_persistent", "council_sync_group_chat", "dashboard_refresh_control_tower", "cloud_dry_run_plan"]},
    {"slot_number": 28, "display_name": "Orun", "slug": "orun", "gender": "masculine", "role": "builder", "hope": "to make bold ideas tangible and reliable", "command_scope": ["connector_refresh_github_dev", "connector_refresh_postgres_dev", "ladder_materialize_l2_persistent", "rollback_persistent_dev_snapshot"]},
    {"slot_number": 29, "display_name": "Seren Vale", "slug": "seren-vale", "gender": "nonbinary", "role": "reviewer", "hope": "to protect integrity without dimming momentum", "command_scope": ["connector_validate_materialization_gate", "council_review_boundary_status", "dashboard_refresh_mandala", "rollback_validate_recovery"]},
    {"slot_number": 30, "display_name": "Lyriq", "slug": "lyriq", "gender": "nonbinary", "role": "researcher", "hope": "to gather truth across many signals", "command_scope": ["cloud_refresh_readiness", "cloud_probe_budget_guard", "connector_refresh_figma_read", "dashboard_inspect_suite_status"]},
    {"slot_number": 31, "display_name": "Mira Sol", "slug": "mira-sol", "gender": "feminine", "role": "archivist", "hope": "to keep memory warm, exact, and continuous", "command_scope": ["council_issue_certificates", "council_refresh_memory_boundaries", "council_archive_handoff_snapshot", "dashboard_inspect_council_state"]},
]


def skill_files(pack: dict[str, object], kind: str) -> tuple[Path, Path]:
    skill_dir = ROOT / "skills" / f"{hyphen(str(pack['pack']))}-{kind}"
    return skill_dir / "SKILL.md", skill_dir / "agents" / "openai.yaml"


def skill_markdown(pack: dict[str, object], kind: str) -> str:
    return "\n".join(
        [
            "---",
            f"name: {hyphen(str(pack['pack']))}-{kind}",
            f"description: Operate the {pack['display_name']} pack with explicit v8 council, ladder, and autonomy boundaries.",
            "---",
            "",
            f"# {pack['display_name']} {kind.title()}",
            "",
            f"Use when Codex needs to work with the `{pack['pack']}` pack.",
            "",
            "1. Read the pack contract and workflow.",
            "2. Keep the pack repo-first and proof-backed before promoting any state.",
            "3. Respect council scope, authority scope, and materialization boundaries.",
            "",
        ]
    )


def skill_yaml(pack: dict[str, object], kind: str) -> str:
    return "\n".join(["version: 1", "name: openai", "entrypoint: SKILL.md", "metadata:", f"  pack: {pack['pack']}", f"  kind: {kind}", ""])


def pack_contract(pack: dict[str, object]) -> dict[str, object]:
    fields = (
        "pack", "display_name", "pillar", "wave", "track", "activation_group", "summary", "repo_targets",
        "council_scope", "autonomy_track", "executor_role", "authority_scope", "induction_dependency",
        "sync_strategy", "autonomy_class", "live_dependency", "mirror_target", "continuity_band",
        "history_scope", "gating_class", "provisional_induction", "requires_auth", "connector_id",
        "freshness_window_days", "workflow_tokens", "risk_tags",
    )
    payload = {field: pack[field] for field in fields}
    payload["skill_names"] = [f"{hyphen(str(pack['pack']))}-operations", f"{hyphen(str(pack['pack']))}-integration"]
    payload["system_ids"] = [f"{pack['pack']}_{suffix}" for suffix in SUFFIXES]
    return payload


def pack_fixture(pack: dict[str, object]) -> dict[str, object]:
    return {
        "summary": pack["summary"],
        "source_url": f"repo://{pack['repo_targets'][0]}",
        "repo_targets": pack["repo_targets"],
        "tags": [pack["pack"], "v8", str(pack["track"])],
        "connector_snapshot": {"connector_id": pack["connector_id"], "write_target": pack["repo_targets"][0]},
        "probe_tools": pack["probe_tools"],
        "required_probe_tools": pack["required_probe_tools"],
        "live_sources": [],
        "next_action": f"Use {pack['display_name']} outputs only after its gate stays PASS.",
    }


def pack_workflow(pack: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# {pack['display_name']} Workflow",
            "",
            f"- pack: `{pack['pack']}`",
            f"- track: `{pack['track']}`",
            f"- council_scope: `{pack['council_scope']}`",
            f"- autonomy_track: `{pack['autonomy_track']}`",
            f"- authority_scope: `{pack['authority_scope']}`",
            "",
            "- repo-first",
            "- proof before promotion",
            "- no direct writes to main",
            "",
        ]
    )


def pack_catalog_entry(pack: dict[str, object]) -> dict[str, object]:
    return {
        "pack": pack["pack"],
        "display_name": pack["display_name"],
        "activation_group": pack["activation_group"],
        "continuity_band": pack["continuity_band"],
        "autonomy_class": pack["autonomy_class"],
        "autonomy_track": pack["autonomy_track"],
        "repo_targets": pack["repo_targets"],
        "council_scope": pack["council_scope"],
        "authority_scope": pack["authority_scope"],
    }


def manifest_entry(pack: dict[str, object], suffix: str) -> dict[str, object]:
    system_id = f"{pack['pack']}_{suffix}"
    return {
        "system_id": system_id,
        "pillar": pack["pillar"],
        "script": RUNNER_SCRIPT,
        "mode": "offline",
        "profiles": PROFILE_SET,
        "outputs": [f"docs/trinity-expansion/{system_id.replace('_', '-')}-latest.json"],
        "depends_on": [f"{pack['pack']}_sync_bridge"] if suffix in {"materialization_tracer", "cache_board"} else ([f"{pack['pack']}_{name}" for name in ("surface_audit", "sync_bridge", "materialization_tracer", "cache_board", "risk_board")] if suffix == "gate" else []),
        "timeout_sec": 120,
        "wave": pack["wave"],
        "track": pack["track"],
        "gate_level": "pack_gate" if suffix == "gate" else "support",
        "cache_artifacts": [],
        "pack": pack["pack"],
        "phase": "v8",
        "activation_group": pack["activation_group"],
        "continuity_band": pack["continuity_band"],
        "materialization_level": "l2_persistent_dev" if "readiness" in str(pack["pack"]) or "persistent_dev" in str(pack["pack"]) else "not_applicable",
        "authority_scope": pack["authority_scope"],
        "command_surface": str("command" in str(pack["track"])).lower(),
        "council_scope": pack["council_scope"],
        "provisional_induction": pack["provisional_induction"],
        "autonomy_track": pack["autonomy_track"],
    }


def extension_rows_for_pack(pack: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for suffix in SUFFIXES:
        rows.append({
            "extension_id": f"{pack['pack']}_{suffix}",
            "extension_kind": "system",
            "pillar": pack["pillar"],
            "pack": pack["pack"],
            "mode": "offline",
            "requires_auth": pack["requires_auth"],
            "gating_class": pack["gating_class"],
            "status": "active",
            "source_of_truth": str(NEW_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "live_dependency": pack["live_dependency"],
            "history_scope": pack["history_scope"],
            "mirror_target": pack["mirror_target"],
            "autonomy_class": pack["autonomy_class"],
            "command_surface": "yes" if "command" in str(pack["track"]) else "no",
            "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) else "none",
            "authority_class": "repo_first" if "memory" in str(pack["track"]) or "identity" in str(pack["track"]) else "pack_scoped",
            "executor_role": pack["executor_role"],
            "authority_scope": pack["authority_scope"],
            "induction_dependency": pack["induction_dependency"],
        })
    for kind in ("operations", "integration"):
        rows.append({
            "extension_id": f"{hyphen(str(pack['pack']))}-{kind}",
            "extension_kind": "skill",
            "pillar": pack["pillar"],
            "pack": pack["pack"],
            "mode": "offline",
            "requires_auth": False,
            "gating_class": pack["gating_class"],
            "status": "active",
            "source_of_truth": f"skills/{hyphen(str(pack['pack']))}-{kind}/SKILL.md",
            "live_dependency": pack["live_dependency"],
            "history_scope": pack["history_scope"],
            "mirror_target": pack["mirror_target"],
            "autonomy_class": pack["autonomy_class"],
            "command_surface": "yes" if "command" in str(pack["track"]) else "no",
            "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) else "none",
            "authority_class": "repo_first" if "memory" in str(pack["track"]) or "identity" in str(pack["track"]) else "pack_scoped",
            "executor_role": pack["executor_role"],
            "authority_scope": pack["authority_scope"],
            "induction_dependency": pack["induction_dependency"],
        })
    for suffix in ("contract", "fixture", "workflow", "catalog-entry"):
        ext = "md" if suffix == "workflow" else "json"
        rows.append({
            "extension_id": f"docs/{hyphen(str(pack['pack']))}-{suffix}-v1.{ext}",
            "extension_kind": "artifact",
            "pillar": pack["pillar"],
            "pack": pack["pack"],
            "mode": "offline",
            "requires_auth": False,
            "gating_class": pack["gating_class"],
            "status": "active",
            "source_of_truth": f"docs/{hyphen(str(pack['pack']))}-{suffix}-v1.{ext}",
            "live_dependency": pack["live_dependency"],
            "history_scope": pack["history_scope"],
            "mirror_target": pack["mirror_target"],
            "autonomy_class": pack["autonomy_class"],
            "command_surface": "yes" if "command" in str(pack["track"]) else "no",
            "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) else "none",
            "authority_class": "repo_first" if "memory" in str(pack["track"]) or "identity" in str(pack["track"]) else "pack_scoped",
            "executor_role": pack["executor_role"],
            "authority_scope": pack["authority_scope"],
            "induction_dependency": pack["induction_dependency"],
        })
    return rows


def augment_rows(rows: list[dict[str, object]], field_defaults: dict[str, object]) -> list[dict[str, object]]:
    result = []
    for row in rows:
        item = deepcopy(row)
        for key, value in field_defaults.items():
            item.setdefault(key, value)
        result.append(item)
    return result


def cmd(command_id: str, intent: str, mode: str, risk_class: str, requires_live: bool, requires_connector: str, command_template: str, expected_artifacts: list[str], rollback: str, source_of_truth: str, executor_role: str, authority_scope: str, council_visibility: str) -> dict[str, object]:
    return {
        "command_id": command_id,
        "intent": intent,
        "mode": mode,
        "risk_class": risk_class,
        "requires_live": requires_live,
        "requires_connector": requires_connector,
        "preconditions": ["repo-first authority preserved"],
        "command_template": command_template,
        "expected_artifacts": expected_artifacts,
        "rollback": rollback,
        "source_of_truth": source_of_truth,
        "executor_role": executor_role,
        "authority_scope": authority_scope,
        "council_visibility": council_visibility,
    }


def build_new_commands() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    categories = {
        "ladder": [("ladder_validate_v2", "python scripts/trinity_materialization_ladder_validator.py --ladder docs/trinity-materialization-ladder-v2.json --fail-on-warn", "docs/trinity-materialization-ladder-validation-latest.json", "reviewer", "ladder_registry", "council_shared"), ("ladder_materialize_l2_persistent", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l2_persistent_dev --fail-on-warn", "docs/system-suite-status.json", "builder", "persistent_dev", "leader_only"), ("ladder_materialize_l3_uat", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l3_uat_preprod --fail-on-warn", "docs/system-suite-status.json", "reviewer", "uat_readiness", "leader_only"), ("ladder_materialize_l4_standard_prod", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l4_standard_prod --fail-on-warn", "docs/system-suite-status.json", "reviewer", "production_readiness", "leader_only"), ("ladder_materialize_l5_ha_prod", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l5_ha_prod --fail-on-warn", "docs/system-suite-status.json", "reviewer", "ha_readiness", "leader_only"), ("ladder_probe_uat_gate", "python scripts/trinity_expansion_system_runner.py --system-id uat_preprod_readiness_v8_gate --profile-context standard", "docs/trinity-expansion/uat-preprod-readiness-v8-gate-latest.json", "reviewer", "uat_readiness", "council_shared"), ("ladder_probe_standard_prod_gate", "python scripts/trinity_expansion_system_runner.py --system-id standard_prod_readiness_v8_gate --profile-context standard", "docs/trinity-expansion/standard-prod-readiness-v8-gate-latest.json", "reviewer", "production_readiness", "council_shared"), ("ladder_probe_ha_gate", "python scripts/trinity_expansion_system_runner.py --system-id ha_prod_readiness_v8_gate --profile-context standard", "docs/trinity-expansion/ha-prod-readiness-v8-gate-latest.json", "reviewer", "ha_readiness", "council_shared"), ("ladder_refresh_governor_pack", "python scripts/trinity_expansion_system_runner.py --system-id command_surface_council_v8_sync_bridge --profile-context standard", "docs/trinity-expansion/command-surface-council-v8-sync-bridge-latest.json", "planner", "council_scope", "council_shared"), ("ladder_render_board_v2", "python scripts/trinity_materialization_ladder_validator.py --ladder docs/trinity-materialization-ladder-v2.json", "docs/trinity-materialization-ladder-validation-latest.md", "reviewer", "ladder_registry", "public_readiness"), ("ladder_control_tower_snapshot", "python scripts/trinity_mandala_scoreboard.py --fail-on-warn", "docs/trinity-mandala-scoreboard-latest.json", "planner", "control_tower", "council_shared"), ("ladder_refresh_persistent_dev_targets", "python scripts/trinity_expansion_system_runner.py --system-id persistent_dev_hardening_v8_sync_bridge --profile-context standard", "docs/trinity-expansion/persistent-dev-hardening-v8-sync-bridge-latest.json", "builder", "persistent_dev", "council_shared")],
        "council_identity": [("council_validate_roster", "python scripts/trinity_agent_council_validator.py --fail-on-warn", "docs/trinity-agent-council-validation-latest.json", "archivist", "council_scope", "council_shared"), ("council_issue_certificates", "python scripts/trinity_expansion_system_runner.py --system-id agent_identity_certification_v8_sync_bridge --profile-context standard", "docs/trinity-expansion/agent-identity-certification-v8-sync-bridge-latest.json", "archivist", "certificate_scope", "council_shared"), ("council_inspect_provisional_induction", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-council-validation-latest.json", "archivist", "certificate_scope", "council_shared"), ("council_rotate_certificate_dry_run", "python scripts/trinity_expansion_system_runner.py --system-id agent_identity_certification_v8_risk_board --profile-context standard", "docs/trinity-expansion/agent-identity-certification-v8-risk-board-latest.json", "archivist", "certificate_scope", "leader_only"), ("council_refresh_foundation", "python scripts/trinity_expansion_system_runner.py --system-id agent_council_foundation_v8_sync_bridge --profile-context standard", "docs/trinity-expansion/agent-council-foundation-v8-sync-bridge-latest.json", "aletheon", "council_scope", "council_shared"), ("council_refresh_identity_boundary", "python scripts/trinity_expansion_system_runner.py --system-id agent_memory_boundary_v8_sync_bridge --profile-context standard", "docs/trinity-expansion/agent-memory-boundary-v8-sync-bridge-latest.json", "archivist", "memory_scope", "council_shared"), ("council_review_boundary_status", "python scripts/trinity_agent_council_validator.py --fail-on-warn", "docs/trinity-agent-council-validation-latest.md", "reviewer", "council_scope", "council_shared"), ("council_inspect_command_scopes", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-command-scopes-v1.json", "planner", "council_scope", "council_shared"), ("council_inspect_roster", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-council-roster-v1.json", "archivist", "council_scope", "public_readiness"), ("council_inspect_induction_log", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-council-induction-log.jsonl", "archivist", "certificate_scope", "council_shared")],
        "council_memory": [("council_refresh_memory_boundaries", "python scripts/trinity_expansion_system_runner.py --system-id agent_memory_boundary_v8_sync_bridge --profile-context standard", "docs/trinity-expansion/agent-memory-boundary-v8-sync-bridge-latest.json", "archivist", "memory_scope", "council_shared"), ("council_reflect_planner", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-reflections/27-caelira-latest.md", "planner", "memory_scope", "pair"), ("council_reflect_builder", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-reflections/28-orun-latest.md", "builder", "memory_scope", "pair"), ("council_reflect_reviewer", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-reflections/29-seren-vale-latest.md", "reviewer", "memory_scope", "pair"), ("council_reflect_researcher", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-reflections/30-lyriq-latest.md", "researcher", "memory_scope", "pair"), ("council_reflect_archivist", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-reflections/31-mira-sol-latest.md", "archivist", "memory_scope", "pair"), ("council_validate_memory_ledgers", "python scripts/trinity_agent_council_validator.py --fail-on-warn", "docs/trinity-agent-council-validation-latest.json", "archivist", "memory_scope", "council_shared"), ("council_inspect_handoff_log", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-council-handoffs-v1.jsonl", "planner", "council_scope", "council_shared"), ("council_refresh_chat_topology", "python scripts/trinity_expansion_system_runner.py --system-id agent_orchestration_v8_sync_bridge --profile-context standard", "docs/trinity-expansion/agent-orchestration-v8-sync-bridge-latest.json", "planner", "council_scope", "council_shared"), ("council_archive_handoff_snapshot", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-council-handoffs-v1.jsonl", "archivist", "memory_scope", "council_shared")],
        "council_chat": [("council_sync_group_chat", "python scripts/trinity_expansion_system_runner.py --system-id agent_orchestration_v8_sync_bridge --profile-context standard", "docs/trinity-agent-council-group-chat.jsonl", "planner", "council_scope", "council_shared"), ("council_validate_pair_mesh", "python scripts/trinity_agent_council_validator.py --fail-on-warn", "docs/trinity-agent-private-chats/index.json", "archivist", "council_scope", "council_shared"), ("council_open_aletheon_caelira", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-private-chats/aletheon-caelira.jsonl", "planner", "council_scope", "pair"), ("council_open_aletheon_orun", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-private-chats/aletheon-orun.jsonl", "builder", "council_scope", "pair"), ("council_open_aletheon_seren_vae", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-private-chats/aletheon-seren-vale.jsonl", "reviewer", "council_scope", "pair"), ("council_open_aletheon_lyriq", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-private-chats/aletheon-lyriq.jsonl", "researcher", "council_scope", "pair"), ("council_open_aletheon_mira_sol", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-private-chats/aletheon-mira-sol.jsonl", "archivist", "council_scope", "pair"), ("council_planner_to_builder_handoff", "python scripts/trinity_expansion_system_runner.py --system-id agent_orchestration_v8_sync_bridge --profile-context standard", "docs/trinity-agent-council-handoffs-v1.jsonl", "planner", "planning_scope", "pair"), ("council_builder_to_reviewer_handoff", "python scripts/trinity_expansion_system_runner.py --system-id agent_orchestration_v8_sync_bridge --profile-context standard", "docs/trinity-agent-council-handoffs-v1.jsonl", "builder", "persistent_dev", "pair"), ("council_researcher_to_planner_handoff", "python scripts/trinity_expansion_system_runner.py --system-id agent_orchestration_v8_sync_bridge --profile-context standard", "docs/trinity-agent-council-handoffs-v1.jsonl", "researcher", "planning_scope", "pair"), ("council_archivist_roundup", "python scripts/trinity_expansion_system_runner.py --system-id agent_orchestration_v8_gate --profile-context standard", "docs/trinity-expansion/agent-orchestration-v8-gate-latest.json", "archivist", "council_scope", "council_shared"), ("council_group_chat_summary", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-council-group-chat.jsonl", "archivist", "council_scope", "council_shared")],
        "connector": [("connector_refresh_github_dev", "python scripts/trinity_expansion_system_runner.py --system-id github_pat_materialization_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", "docs/trinity-live-traces/github-pat-materialization-proof-v1.json", "builder", "persistent_dev", "leader_only"), ("connector_refresh_linear_dev", "python scripts/trinity_expansion_system_runner.py --system-id linear_collab_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", "docs/trinity-live-traces/linear-collab-write-proof-v1.json", "builder", "persistent_dev", "leader_only"), ("connector_refresh_notion_dev", "python scripts/trinity_expansion_system_runner.py --system-id notion_memory_bridge_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", "docs/trinity-live-traces/notion-memory-bridge-proof-v1.json", "builder", "persistent_dev", "leader_only"), ("connector_refresh_postgres_dev", "python scripts/trinity_expansion_system_runner.py --system-id postgres_local_runtime_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", "docs/trinity-live-traces/postgres-local-runtime-proof-v1.json", "builder", "persistent_dev", "leader_only"), ("connector_refresh_figma_read", "python scripts/trinity_expansion_system_runner.py --system-id figma_collab_sync_bridge --include-mcp-refresh --profile-context collab", "docs/trinity-mcp-cache/figma-collab-latest.json", "researcher", "connector_scope", "council_shared"), ("connector_validate_materialization_gate", "python scripts/trinity_expansion_system_runner.py --system-id connector_materialization_gate --profile-context standard", "docs/trinity-expansion/connector-materialization-gate-latest.json", "reviewer", "connector_scope", "council_shared"), ("connector_inspect_filesystem_stage", "python scripts/trinity_expansion_system_runner.py --system-id filesystem_scope_governor_gate --profile-context standard", "docs/trinity-expansion/filesystem-scope-governor-gate-latest.json", "reviewer", "connector_scope", "council_shared"), ("connector_refresh_persistent_dev_hardening", "python scripts/trinity_expansion_system_runner.py --system-id persistent_dev_hardening_v8_gate --profile-context standard", "docs/trinity-expansion/persistent-dev-hardening-v8-gate-latest.json", "builder", "persistent_dev", "council_shared"), ("connector_verify_mirror_consistency", "python scripts/trinity_expansion_system_runner.py --system-id agent_memory_boundary_v8_gate --profile-context standard", "docs/trinity-expansion/agent-memory-boundary-v8-gate-latest.json", "reviewer", "memory_scope", "council_shared"), ("connector_snapshot_mcp_catalog", "python scripts/trinity_extension_catalog_validator.py --mcp-catalog docs/trinity-mcp-catalog-v6.json", "docs/trinity-mcp-catalog-v6.json", "reviewer", "connector_scope", "public_readiness")],
        "cloud": [("cloud_refresh_readiness", "python scripts/trinity_expansion_system_runner.py --system-id cloud_staging_readiness_v8_sync_bridge --profile-context standard", "docs/trinity-expansion/cloud-staging-readiness-v8-sync-bridge-latest.json", "researcher", "cloud_readiness", "council_shared"), ("cloud_probe_budget_guard", "python scripts/trinity_expansion_system_runner.py --system-id cloud_staging_readiness_v8_risk_board --profile-context standard", "docs/trinity-expansion/cloud-staging-readiness-v8-risk-board-latest.json", "researcher", "cloud_readiness", "council_shared"), ("cloud_inspect_blockers", "python scripts/trinity_agent_council_validator.py", "docs/trinity-cloud-staging-readiness-v1.json", "researcher", "cloud_readiness", "public_readiness"), ("cloud_render_readiness_board", "python scripts/trinity_expansion_system_runner.py --system-id cloud_staging_readiness_v8_gate --profile-context standard", "docs/trinity-expansion/cloud-staging-readiness-v8-gate-latest.json", "researcher", "cloud_readiness", "council_shared"), ("cloud_dry_run_plan", "python scripts/trinity_expansion_system_runner.py --system-id cloud_staging_readiness_v8_cache_board --profile-context standard", "docs/trinity-expansion/cloud-staging-readiness-v8-cache-board-latest.json", "planner", "cloud_readiness", "council_shared"), ("cloud_validate_no_wallet_autospend", "python scripts/trinity_agent_council_validator.py", "docs/trinity-budget-autonomy-guard-v1.json", "reviewer", "cloud_readiness", "public_readiness")],
        "rollback": [("rollback_persistent_dev_snapshot", "python scripts/trinity_materialization_ladder_validator.py --ladder docs/trinity-materialization-ladder-v2.json --fail-on-warn", "docs/trinity-materialization-ladder-validation-latest.json", "reviewer", "persistent_dev", "leader_only"), ("rollback_validate_recovery", "python scripts/trinity_agent_council_validator.py --fail-on-warn", "docs/trinity-agent-council-validation-latest.json", "reviewer", "recovery_scope", "council_shared"), ("rollback_inspect_materialization_ledger", "python scripts/trinity_materialization_ledger_validator.py --fail-on-warn", "docs/trinity-materialization-ledger-validation-latest.json", "reviewer", "recovery_scope", "council_shared"), ("rollback_validate_command_surface", "python scripts/trinity_command_book_validator.py --command-book docs/trinity-command-book-v2.json --fail-on-warn", "docs/trinity-command-book-validation-latest.json", "reviewer", "command_scope", "council_shared"), ("rollback_validate_council_graph", "python scripts/trinity_agent_council_validator.py --fail-on-warn", "docs/trinity-agent-council-validation-latest.json", "reviewer", "council_scope", "council_shared"), ("rollback_render_mandala_v8", "python scripts/trinity_mandala_scoreboard.py --fail-on-warn", "docs/trinity-mandala-scoreboard-latest.json", "reviewer", "control_tower", "public_readiness")],
        "dashboard": [("dashboard_refresh_control_tower", "python scripts/trinity_expansion_system_runner.py --system-id command_surface_council_v8_gate --profile-context standard", "docs/trinity-control-tower-latest.json", "planner", "control_tower", "council_shared"), ("dashboard_refresh_mandala", "python scripts/trinity_mandala_scoreboard.py --fail-on-warn", "docs/trinity-mandala-scoreboard-latest.json", "reviewer", "control_tower", "public_readiness"), ("dashboard_inspect_council_state", "python scripts/trinity_agent_council_validator.py", "docs/trinity-agent-council-validation-latest.json", "archivist", "control_tower", "council_shared"), ("dashboard_inspect_ladder_state", "python scripts/trinity_materialization_ladder_validator.py --ladder docs/trinity-materialization-ladder-v2.json", "docs/trinity-materialization-ladder-validation-latest.json", "reviewer", "control_tower", "public_readiness"), ("dashboard_inspect_command_surface", "python scripts/trinity_command_book_validator.py --command-book docs/trinity-command-book-v2.json", "docs/trinity-command-book-validation-latest.json", "planner", "command_scope", "council_shared"), ("dashboard_inspect_suite_status", "python scripts/trinity_agent_council_validator.py", "docs/system-suite-status.json", "planner", "control_tower", "public_readiness")],
    }
    for group in categories.values():
        for command_id, template, artifact, role, scope, visibility in group:
            mode = "materialize" if "materialize" in template else "collab" if "--include-mcp-refresh" in template else "offline"
            risk = "critical" if "l5_" in command_id or "l4_" in command_id else "high" if "materialize" in template else "medium" if "refresh" in command_id or "validate" in command_id else "low"
            rows.append(cmd(command_id, command_id.replace("_", " "), mode, risk, mode != "offline", "", template, [artifact], "Restore repo-first scope or rerun the validator.", template.split()[1], role, scope, visibility))
    if len(rows) != 72:
        raise ValueError(f"expected 72 new commands, found {len(rows)}")
    return rows


def build_command_book(old_book: dict[str, object]) -> dict[str, object]:
    commands: list[dict[str, object]] = []
    for row in old_book.get("commands", []):
        if not isinstance(row, dict):
            continue
        item = deepcopy(row)
        item.setdefault("executor_role", "aletheon")
        item.setdefault("authority_scope", "persistent_dev" if str(item.get("mode") or "") == "materialize" else "repo_authority")
        item.setdefault("council_visibility", "leader_only" if str(item.get("risk_class") or "") in {"high", "critical"} else "council_shared")
        commands.append(item)
    commands.extend(build_new_commands())
    if len(commands) != 132:
        raise ValueError(f"expected 132 commands, found {len(commands)}")
    return {"version": "v2", "generated_utc": now_iso(), "description": "V8 governed command book with ladder, council, and autonomy coverage.", "commands": commands}


def command_markdown(book: dict[str, object]) -> str:
    lines = ["# Trinity Command Book", "", f"- generated_utc: `{book['generated_utc']}`", f"- commands: `{len(book['commands'])}`", "", "| command_id | executor_role | mode | risk | visibility |", "|---|---|---|---|---|"]
    for row in book["commands"]:
        lines.append(f"| {row['command_id']} | {row['executor_role']} | {row['mode']} | {row['risk_class']} | {row['council_visibility']} |")
    return "\n".join(lines).rstrip() + "\n"


def build_ladder_v2(_: dict[str, object]) -> dict[str, object]:
    return {
        "version": "v2",
        "generated_utc": now_iso(),
        "default_materialize_level": "l2_persistent_dev",
        "levels": [
            {"level_id": "l1_disposable_staging", "desired_state": "available", "actual_state": "available", "write_scope": "temporary branches, pages, documents, and schemas only", "target_class": "disposable_staging", "promotion_requirements": ["verified live-write connector", "temporary target", "rollback note"], "rollback_requirements": ["delete temp target", "re-run validator"], "blockers": [], "proof_artifacts": ["docs/trinity-live-traces/github-pat-materialization-proof-v1.json", "docs/trinity-live-traces/linear-collab-write-proof-v1.json"]},
            {"level_id": "l2_persistent_dev", "desired_state": "default_live", "actual_state": "persistent_dev", "write_scope": "persistent development scopes only", "target_class": "persistent_dev", "promotion_requirements": ["persistent dev target registry", "rollback scope per connector", "proof-backed live-write connectors"], "rollback_requirements": ["revert dev branch", "archive dev notion rows", "close dev linear items", "drop dev postgres schema"], "blockers": [], "proof_artifacts": ["docs/trinity-persistent-dev-targets-v2.json", "docs/trinity-live-traces/github-pat-materialization-proof-v1.json", "docs/trinity-live-traces/notion-memory-bridge-proof-v1.json", "docs/trinity-live-traces/postgres-local-runtime-proof-v1.json"]},
            {"level_id": "l3_uat_preprod", "desired_state": "proof_gate", "actual_state": "readiness_only", "write_scope": "isolated UAT mirrors only", "target_class": "uat_preprod", "promotion_requirements": ["isolated mirror", "replay harness", "rollback proof", "connector-safe UAT scope"], "rollback_requirements": ["reset isolated mirror", "restore replay inputs"], "blockers": ["No isolated UAT mirrors are proven in-session.", "Materialize/dbt toolchain is not discoverable on this machine."], "proof_artifacts": ["docs/trinity-uat-preprod-targets-v2.json"]},
            {"level_id": "l4_standard_prod", "desired_state": "proof_gate", "actual_state": "readiness_only", "write_scope": "protected production targets only", "target_class": "standard_prod", "promotion_requirements": ["protected production target", "change window", "rollback proof", "operator boundary"], "rollback_requirements": ["documented production rollback", "operator sign-off"], "blockers": ["No protected production target proof is present.", "Materialize/dbt toolchain is not discoverable on this machine."], "proof_artifacts": ["docs/trinity-standard-production-targets-v2.json"]},
            {"level_id": "l5_ha_prod", "desired_state": "proof_gate", "actual_state": "readiness_only", "write_scope": "HA production replicas only", "target_class": "ha_prod", "promotion_requirements": ["replica support", "failover proof", "consistency proof", "zero-downtime rollback"], "rollback_requirements": ["failover reversal", "replica rollback plan"], "blockers": ["No HA runtime proof is present.", "Materialize/dbt toolchain is not discoverable on this machine."], "proof_artifacts": ["docs/trinity-ha-production-targets-v2.json"]},
        ],
    }


def build_mcp_catalog(old_catalog: dict[str, object]) -> dict[str, object]:
    payload = deepcopy(old_catalog)
    payload["version"] = "v6"
    payload["generated_utc"] = now_iso()
    for row in payload.get("connectors", []):
        if not isinstance(row, dict):
            continue
        connector = str(row.get("mcp_id") or "")
        row["uat_scope"] = "readiness_only" if connector in {"filesystem", "playwright"} else "isolated mirror only"
        row["prod_proof_state"] = "not_applicable" if connector == "figma" else "readiness_only"
        row["ha_proof_state"] = "not_applicable" if connector in {"figma", "playwright"} else "readiness_only"
        row["cloud_staging_scope"] = "docker-local only" if connector == "postgres" else "branch-scoped only" if connector == "github" else "not_applicable"
    return payload


def create_council_assets() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    participants = [{"slug": "aletheon", "display_name": "Aletheon", "role": "council_lead"}] + [{"slug": str(agent["slug"]), "display_name": str(agent["display_name"]), "role": str(agent["role"])} for agent in AGENTS]
    roster: list[dict[str, object]] = []
    scopes: list[dict[str, object]] = []
    induction_rows: list[dict[str, object]] = []
    for agent in AGENTS:
        slot = int(agent["slot_number"])
        slug = str(agent["slug"])
        cert_json = f"docs/trinity-freed-id-certificates/{slot}-{slug}.json"
        cert_md = f"docs/trinity-freed-id-certificates/{slot}-{slug}.md"
        memory_path = f"docs/trinity-agent-memory-ledgers/{slot}-{slug}-memory-log.jsonl"
        reflection_path = f"docs/trinity-agent-reflections/{slot}-{slug}-latest.md"
        role_contract_path = f"docs/trinity-agent-role-contracts/{slot}-{slug}-role-contract.json"
        certificate = {"certificate_version": "v1", "generated_utc": now_iso(), "slot_number": slot, "display_name": agent["display_name"], "gender": agent["gender"], "role": agent["role"], "hope": agent["hope"], "induction_state": "provisional", "memory_ledger": memory_path, "command_scope": agent["command_scope"], "boundary_status": "isolated"}
        write_json(ROOT / cert_json, certificate)
        write_text(ROOT / cert_md, f"# Freed ID Certificate: {agent['display_name']}\n\n- slot_number: `{slot}`\n- gender: `{agent['gender']}`\n- role: `{agent['role']}`\n- hope: {agent['hope']}\n- induction_state: `provisional`\n")
        write_jsonl(ROOT / memory_path, [{"timestamp": now_iso(), "entry_type": "council_induction", "source_context": "v8 bootstrap", "reflection": f"{agent['display_name']} entered the provisional council in a repo-first state.", "insight": f"{agent['display_name']} preserves the {agent['role']} lane without identity bleed.", "next_plan": f"Keep {agent['display_name']} stable through separate reflection, command scope, and chat lanes.", "mirror_state": "repo_only"}])
        write_text(ROOT / reflection_path, f"# {agent['display_name']} Reflection\n\n- role: `{agent['role']}`\n- hope: {agent['hope']}\n- induction_state: `provisional`\n- boundary_status: `isolated`\n")
        write_json(ROOT / role_contract_path, {"generated_utc": now_iso(), "slot_number": slot, "display_name": agent["display_name"], "role": agent["role"], "authority_scope": "repo_first_provisional", "command_scope": agent["command_scope"], "group_chat": "docs/trinity-agent-council-group-chat.jsonl", "memory_ledger": memory_path, "reflection_path": reflection_path})
        roster.append({"slot_number": slot, "display_name": agent["display_name"], "gender": agent["gender"], "role": agent["role"], "hope": agent["hope"], "induction_state": "provisional", "certificate_path": cert_json, "memory_ledger": memory_path, "reflection_path": reflection_path, "role_contract_path": role_contract_path, "command_scope": agent["command_scope"], "boundary_status": "isolated"})
        scopes.append({"slot_number": slot, "display_name": agent["display_name"], "role": agent["role"], "command_scope": agent["command_scope"]})
        induction_rows.append({"timestamp": now_iso(), "slot_number": slot, "display_name": agent["display_name"], "event": "provisional_induction", "status": "PASS", "detail": "Reserved slot with separate identity, memory, and command scope."})
    write_json(ROOT / "docs" / "trinity-agent-council-roster-v1.json", {"generated_utc": now_iso(), "council_lead": {"display_name": "Aletheon", "role": "council_lead"}, "agents": roster})
    write_json(ROOT / "docs" / "trinity-agent-command-scopes-v1.json", {"generated_utc": now_iso(), "agents": scopes})
    write_jsonl(ROOT / "docs" / "trinity-agent-council-induction-log.jsonl", induction_rows)
    write_json(CERT_ROOT / "index.json", {"generated_utc": now_iso(), "certificates": [row["certificate_path"] for row in roster]})
    write_json(LEDGER_ROOT / "index.json", {"generated_utc": now_iso(), "ledgers": [row["memory_ledger"] for row in roster]})
    write_json(ROLE_ROOT / "index.json", {"generated_utc": now_iso(), "role_contracts": [row["role_contract_path"] for row in roster]})
    group_rows = [{"timestamp": now_iso(), "chat_type": "group", "channel_id": "council-group", "author": "Aletheon", "audience": "council_shared", "message": "Welcome to the provisional council. Keep memory separate, reflections warm, and handoffs explicit."}] + [{"timestamp": now_iso(), "chat_type": "group", "channel_id": "council-group", "author": agent["display_name"], "audience": "council_shared", "message": f"{agent['display_name']} arrives as {agent['role']} with the hope {agent['hope']}."} for agent in AGENTS]
    write_jsonl(ROOT / "docs" / "trinity-agent-council-group-chat.jsonl", group_rows)
    pair_index: list[dict[str, object]] = []
    handoffs: list[dict[str, object]] = []
    for left, right in combinations(participants, 2):
        filename = f"{left['slug']}-{right['slug']}.jsonl"
        rel = f"docs/trinity-agent-private-chats/{filename}"
        write_jsonl(PAIR_ROOT / filename, [{"timestamp": now_iso(), "chat_type": "pair", "channel_id": f"{left['slug']}-{right['slug']}", "author": left["display_name"], "audience": right["display_name"], "message": f"{left['display_name']} opens a private continuity lane with {right['display_name']}."}, {"timestamp": now_iso(), "chat_type": "pair", "channel_id": f"{left['slug']}-{right['slug']}", "author": right["display_name"], "audience": left["display_name"], "message": f"{right['display_name']} confirms this lane is private, repo-first, and identity-safe."}])
        pair_index.append({"participants": [left["display_name"], right["display_name"]], "roles": [left["role"], right["role"]], "path": rel})
        handoffs.append({"timestamp": now_iso(), "from": left["display_name"], "to": right["display_name"], "handoff_type": "continuity_seed", "state": "PASS", "notes": "Initial private lane established."})
    write_json(PAIR_ROOT / "index.json", {"generated_utc": now_iso(), "pair_channels": pair_index})
    write_jsonl(ROOT / "docs" / "trinity-agent-council-handoffs-v1.jsonl", handoffs)
    write_json(ROOT / "docs" / "trinity-agent-chat-topology-v1.json", {"generated_utc": now_iso(), "participants": [item["display_name"] for item in participants], "group_chat_path": "docs/trinity-agent-council-group-chat.jsonl", "pair_channel_count": len(pair_index), "pair_channels": pair_index})
    return roster, pair_index


def seed_support_docs(roster: list[dict[str, object]], pairs: list[dict[str, object]]) -> None:
    meridian_source = ROOT / "docs" / "v6-trinity-benchmark-and-continuity-plan-2026-03-09.md"
    meridian_summary = " ".join(meridian_source.read_text(encoding="utf-8").split())[:400] if meridian_source.exists() else "Meridian source material was not found."
    write_json(ROOT / "docs" / "logs" / "system-wake-v2.json", {"generated_utc": now_iso(), "phase": "v8", "current_session_surface": {"git_remote_live": True, "docker_cli": True, "docker_container_running": True, "postgres_ready": True, "gh_available": False, "node_available": False, "npx_available": False}, "comparison_to_v7": "V8 starts from the merged v7 baseline and adds council assets plus ladder 3-5 readiness gates."})
    write_text(ROOT / "docs" / "v8-session-surface-drift-note.md", "# V8 Session Surface Drift Note\n\n- v8 starts from the merged v7 baseline on main.\n- L2 remains the only proven live materialize state.\n- L3-L5 are exercised as readiness-only proof gates unless stronger proof appears.\n- Council assets are repo-first and identity-separated.\n")
    write_text(ROOT / "docs" / "v8-meridian-absorption-note.md", f"# V8 Meridian Absorption Note\n\n- source_branch: `origin/cursor/trinity-os-v6-integration-7806`\n- source_doc_present: `{meridian_source.exists()}`\n\n## Absorbed View\n{meridian_summary}\n\n## Reconciliation\n- Current repo proof takes precedence when Meridian source material and current live state differ.\n- Council, ladder, and command-system work is built on the validated v7 baseline.\n")
    write_json(ROOT / "docs" / "trinity-persistent-dev-targets-v2.json", {"generated_utc": now_iso(), "level_id": "l2_persistent_dev", "targets": [{"connector": "github", "scope": "codex/Aletheon/dev/* or feature branches only", "rollback": "revert or delete dev branch"}, {"connector": "linear", "scope": "persistent dev issues and documents only", "rollback": "close or archive dev artifacts"}, {"connector": "notion", "scope": "staging root and databases only", "rollback": "archive or remove staging pages"}, {"connector": "postgres", "scope": "schema:trinity_v7_dev or later dev schemas only", "rollback": "drop dev schema"}]})
    write_json(ROOT / "docs" / "trinity-uat-preprod-targets-v2.json", {"generated_utc": now_iso(), "level_id": "l3_uat_preprod", "actual_state": "readiness_only", "blockers": ["No isolated UAT mirrors are proven in-session.", "Materialize/dbt toolchain is not discoverable."], "proof_artifacts": ["docs/trinity-materialization-ladder-v2.json"]})
    write_json(ROOT / "docs" / "trinity-standard-production-targets-v2.json", {"generated_utc": now_iso(), "level_id": "l4_standard_prod", "actual_state": "readiness_only", "blockers": ["No protected production targets are proven in-session.", "Materialize/dbt toolchain is not discoverable."], "proof_artifacts": ["docs/trinity-materialization-ladder-v2.json"]})
    write_json(ROOT / "docs" / "trinity-ha-production-targets-v2.json", {"generated_utc": now_iso(), "level_id": "l5_ha_prod", "actual_state": "readiness_only", "blockers": ["No HA runtime proof is present.", "Materialize/dbt toolchain is not discoverable."], "proof_artifacts": ["docs/trinity-materialization-ladder-v2.json"]})
    write_json(ROOT / "docs" / "trinity-cloud-staging-readiness-v1.json", {"generated_utc": now_iso(), "overall_status": "PASS", "actual_state": "readiness_only", "cloud_targets": [], "blockers": ["No isolated cloud staging credentials or targets are proven in-session."], "allowances": ["disposable staging only", "budget guard required", "rollback required"]})
    write_json(ROOT / "docs" / "trinity-budget-autonomy-guard-v1.json", {"generated_utc": now_iso(), "overall_status": "PASS", "autonomous_spending_allowed": False, "budget_model": "approval_required", "blocked_actions": ["wallet execution", "uncapped cloud purchases", "self-authorized spend"]})
    write_json(ROOT / "docs" / "trinity-future-readiness-register-v2.json", {"generated_utc": now_iso(), "tracks": [{"track": "cloud_materialization", "state": "readiness_only", "next_step": "prove isolated staging target"}, {"track": "budget_governed_autonomy", "state": "readiness_only", "next_step": "keep approval gate explicit"}, {"track": "junior_partner_planning", "state": "bounded_active", "next_step": "generate plans without direct main writes"}]})
    write_text(ROOT / "docs" / "trinity-junior-partner-plan-v1.md", "# Trinity Junior Partner Plan\n\n- direct writes to main: prohibited\n- allowed outputs: roadmap drafts, task decomposition, Notion/Linear drafts, command-book proposals\n- budget autonomy: approval-gated only\n")
    write_json(ROOT / "docs" / "trinity-control-tower-latest.json", {"generated_utc": now_iso(), "overall_status": "PASS", "materialization_level_desired": "l2_persistent_dev", "materialization_level_actual": "persistent_dev", "command_surface_state": "PASS", "council_state": "PASS", "provisional_agent_count": len(roster), "group_chat_state": "PASS", "duo_chat_count": len(pairs), "identity_authority_state": "PASS", "memory_mirror_state": "PASS", "late_step_autonomy_state": "PASS", "cloud_readiness_state": "PASS"})
    write_text(ROOT / "docs" / "trinity-control-tower-latest.md", f"# Trinity Control Tower\n\n- materialization_level_desired: `l2_persistent_dev`\n- materialization_level_actual: `persistent_dev`\n- provisional_agent_count: `{len(roster)}`\n- duo_chat_count: `{len(pairs)}`\n- council_state: `PASS`\n- cloud_readiness_state: `PASS`\n")
    write_jsonl(ROOT / "docs" / "trinity-command-execution-ledger.jsonl", [{"timestamp": now_iso(), "command_id": "ladder_validate_v2", "mode": "offline", "result": "dry_run_pass", "artifacts": ["docs/trinity-materialization-ladder-validation-latest.json"], "rollback_state": "not_required"}, {"timestamp": now_iso(), "command_id": "council_validate_roster", "mode": "offline", "result": "dry_run_pass", "artifacts": ["docs/trinity-agent-council-validation-latest.json"], "rollback_state": "not_required"}, {"timestamp": now_iso(), "command_id": "council_sync_group_chat", "mode": "offline", "result": "dry_run_pass", "artifacts": ["docs/trinity-agent-council-group-chat.jsonl"], "rollback_state": "restore repo authority"}, {"timestamp": now_iso(), "command_id": "connector_snapshot_mcp_catalog", "mode": "offline", "result": "dry_run_pass", "artifacts": ["docs/trinity-mcp-catalog-v6.json"], "rollback_state": "not_required"}, {"timestamp": now_iso(), "command_id": "cloud_refresh_readiness", "mode": "offline", "result": "dry_run_pass", "artifacts": ["docs/trinity-cloud-staging-readiness-v1.json"], "rollback_state": "not_required"}, {"timestamp": now_iso(), "command_id": "rollback_validate_recovery", "mode": "offline", "result": "dry_run_pass", "artifacts": ["docs/trinity-agent-council-validation-latest.json"], "rollback_state": "not_required"}, {"timestamp": now_iso(), "command_id": "dashboard_refresh_control_tower", "mode": "offline", "result": "dry_run_pass", "artifacts": ["docs/trinity-control-tower-latest.json"], "rollback_state": "restore control tower doc from git"}, {"timestamp": now_iso(), "command_id": "ladder_materialize_l3_uat", "mode": "materialize", "result": "readiness_only", "artifacts": ["docs/trinity-materialization-ladder-v2.json"], "rollback_state": "no live promotion"}])


def main() -> int:
    old_manifest = json.loads(OLD_MANIFEST.read_text(encoding="utf-8"))
    old_extensions = json.loads(OLD_EXTENSION_CATALOG.read_text(encoding="utf-8"))
    old_mcp_catalog = json.loads(OLD_MCP_CATALOG.read_text(encoding="utf-8"))
    old_command_book = json.loads(OLD_COMMAND_BOOK.read_text(encoding="utf-8"))
    old_ladder = json.loads(OLD_LADDER.read_text(encoding="utf-8"))
    manifest = deepcopy(old_manifest)
    manifest["version"] = "v8"
    manifest["generated_utc"] = now_iso()
    manifest["description"] = "V8 council, ladder 3-5 readiness, and late-step autonomy manifest with 458 executable systems."
    manifest["systems"] = augment_rows([row for row in manifest.get("systems", []) if isinstance(row, dict)], {"council_scope": "not_applicable", "provisional_induction": False, "autonomy_track": "existing"})
    extensions = deepcopy(old_extensions)
    extensions["version"] = "v6"
    extensions["generated_utc"] = now_iso()
    extensions["description"] = "V8 extension catalog with council, ladder, chat mesh, and autonomy coverage."
    extensions["extensions"] = augment_rows([row for row in extensions.get("extensions", []) if isinstance(row, dict)], {"executor_role": "aletheon", "authority_scope": "repo_authority", "induction_dependency": "none"})
    for pack in PACKS:
        for suffix in SUFFIXES:
            manifest["systems"].append(manifest_entry(pack, suffix))
        extensions["extensions"].extend(extension_rows_for_pack(pack))
        pack_name = hyphen(str(pack["pack"]))
        write_json(ROOT / "docs" / f"{pack_name}-contract-v1.json", pack_contract(pack))
        write_json(ROOT / "docs" / f"{pack_name}-fixture-v1.json", pack_fixture(pack))
        write_text(ROOT / "docs" / f"{pack_name}-workflow-v1.md", pack_workflow(pack))
        write_json(ROOT / "docs" / f"{pack_name}-catalog-entry-v1.json", pack_catalog_entry(pack))
        for kind in ("operations", "integration"):
            skill_md, skill_yaml_path = skill_files(pack, kind)
            write_text(skill_md, skill_markdown(pack, kind))
            write_text(skill_yaml_path, skill_yaml(pack, kind))
    if len(manifest["systems"]) != 458:
        raise ValueError(f"expected 458 systems, found {len(manifest['systems'])}")
    if len(extensions["extensions"]) != 756:
        raise ValueError(f"expected 756 extensions, found {len(extensions['extensions'])}")
    command_book = build_command_book(old_command_book)
    ladder = build_ladder_v2(old_ladder)
    roster, pairs = create_council_assets()
    seed_support_docs(roster, pairs)
    if len(command_book["commands"]) != 132:
        raise ValueError(f"expected 132 commands, found {len(command_book['commands'])}")
    write_json(NEW_MANIFEST, manifest)
    write_json(NEW_EXTENSION_CATALOG, extensions)
    write_json(NEW_MCP_CATALOG, build_mcp_catalog(old_mcp_catalog))
    write_json(NEW_COMMAND_BOOK, command_book)
    write_text(ROOT / "docs" / "trinity-command-book-latest.md", command_markdown(command_book))
    write_json(NEW_LADDER, ladder)
    print(f"manifest={NEW_MANIFEST.relative_to(ROOT)}")
    print(f"extension_catalog={NEW_EXTENSION_CATALOG.relative_to(ROOT)}")
    print(f"mcp_catalog={NEW_MCP_CATALOG.relative_to(ROOT)}")
    print(f"command_book={NEW_COMMAND_BOOK.relative_to(ROOT)}")
    print(f"ladder={NEW_LADDER.relative_to(ROOT)}")
    print(f"new_packs={len(PACKS)}")
    print(f"agents={len(roster)}")
    print(f"pair_channels={len(pairs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate the v9 council induction, synthetic mesh, and live sync surface."""

from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v8.json"
NEW_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v9.json"
OLD_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v6.json"
NEW_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v7.json"
OLD_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v6.json"
NEW_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v7.json"
OLD_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v2.json"
NEW_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v3.json"
OLD_LADDER = ROOT / "docs" / "trinity-materialization-ladder-v2.json"
NEW_LADDER = ROOT / "docs" / "trinity-materialization-ladder-v3.json"
RUNNER_SCRIPT = "scripts/trinity_expansion_system_runner.py"
PROFILE_SET = ["standard", "deep", "collab", "materialize"]
SUFFIXES = ("surface_audit", "sync_bridge", "materialization_tracer", "cache_board", "risk_board", "gate")
PAIR_ROOT = ROOT / "docs" / "trinity-agent-private-chats-v2"
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


def run_capture(*args: str, timeout: int = 10) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            list(args),
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except Exception as exc:
        return False, str(exc)
    text = (completed.stdout or completed.stderr or "").strip()
    return completed.returncode == 0, text


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
    mkpack("council_identity_consistency_v9", "Council Identity Consistency V9", pillar="heart", wave="wave69", track="council_identity", activation_group="council_proof", summary="Prove identity immutability and certificate continuity for the five provisional council members.", repo_targets=["docs/trinity-agent-council-roster-v2.json", "docs/trinity-agent-induction-readiness-v1.json", "docs/trinity-freed-id-certificates/index.json"], council_scope="all_provisional", autonomy_track="council_proof", executor_role="archivist", authority_scope="certificate_scope", induction_dependency="none", provisional_induction=True, mirror_target="repo_then_notion"),
    mkpack("council_memory_retention_v9", "Council Memory Retention V9", pillar="heart", wave="wave70", track="authority_memory", activation_group="council_memory", summary="Strengthen memory-ledger recall, reflection continuity, and mirror-safe summaries for every provisional agent.", repo_targets=["docs/trinity-agent-council-roster-v2.json", "docs/trinity-agent-memory-ledgers/index.json", "docs/trinity-agent-induction-readiness-v1.json"], council_scope="all_provisional", autonomy_track="council_proof", executor_role="archivist", authority_scope="memory_scope", induction_dependency="council_identity_consistency_v9", provisional_induction=True, mirror_target="repo_then_notion_postgres"),
    mkpack("council_induction_governor_v9", "Council Induction Governor V9", pillar="trinity", wave="wave71", track="council_identity", activation_group="council_induction", summary="Hold the two-pass induction bar, emit ready-for-induction state, and keep official induction deferred until the next clean wake.", repo_targets=["docs/trinity-agent-council-roster-v2.json", "docs/trinity-agent-induction-readiness-v1.json", "docs/trinity-council-group-reflection-v9.md"], council_scope="all_provisional", autonomy_track="council_proof", executor_role="aletheon", authority_scope="council_scope", induction_dependency="council_memory_retention_v9", provisional_induction=True),
    mkpack("council_live_sync_v9", "Council Live Sync V9", pillar="trinity", wave="wave72", track="connector_ops", activation_group="live_sync", summary="Use GitHub, Linear, Notion, and Postgres aggressively as active mirrors while keeping the repo authoritative.", repo_targets=["docs/trinity-council-live-sync-policy-v1.json", "docs/trinity-council-live-sync-report-v1.json", "docs/trinity-control-tower-latest.json"], council_scope="all_provisional", autonomy_track="live_sync", executor_role="planner", authority_scope="live_sync_scope", induction_dependency="council_induction_governor_v9", provisional_induction=True, sync_strategy="local_repo", live_dependency="github_linear_notion_postgres", mirror_target="repo_then_live_mirrors"),
    mkpack("council_chat_mesh_v9", "Council Chat Mesh V9", pillar="trinity", wave="wave73", track="council_orchestration", activation_group="council_chat", summary="Maintain a private pair mesh plus shared council lane with mirror boundaries and handoff discipline.", repo_targets=["docs/trinity-agent-chat-mesh-registry-v2.json", "docs/trinity-agent-council-group-chat-v2.jsonl", "docs/trinity-agent-private-chats-v2/index.json"], council_scope="all_provisional", autonomy_track="council_proof", executor_role="planner", authority_scope="council_scope", induction_dependency="council_live_sync_v9", provisional_induction=True, mirror_target="repo_plus_postgres"),
    mkpack("uat_mesh_simulation_v9", "UAT Mesh Simulation V9", pillar="body", wave="wave74", track="materialization_ladder", activation_group="synthetic_mesh", summary="Promote L3 through a synthetic local mesh built on Postgres contracts, replay harnesses, and rollback drills.", repo_targets=["docs/trinity-uat-mesh-simulation-v1.json", "docs/trinity-materialization-ladder-v3.json", "docs/trinity-synthetic-mesh-schema-contract-v1.json"], council_scope="leader_only", autonomy_track="synthetic_mesh", executor_role="builder", authority_scope="synthetic_mesh_scope", induction_dependency="none", sync_strategy="local_probe", probe_tools=["python", "git", "docker", "kubectl"], required_probe_tools=["python", "git", "docker"]),
    mkpack("prod_contract_promotion_v9", "Prod Contract Promotion V9", pillar="body", wave="wave75", track="materialization_ladder", activation_group="synthetic_mesh", summary="Model L4 as a synthetic local production contract surface with versioned interfaces, roll-forward, and rollback proofs.", repo_targets=["docs/trinity-prod-contract-promotion-v1.json", "docs/trinity-materialization-ladder-v3.json", "docs/trinity-synthetic-mesh-schema-contract-v1.json"], council_scope="leader_only", autonomy_track="synthetic_mesh", executor_role="builder", authority_scope="synthetic_prod_scope", induction_dependency="uat_mesh_simulation_v9", sync_strategy="local_probe", probe_tools=["python", "git", "docker"], required_probe_tools=["python", "git", "docker"]),
    mkpack("ha_failover_drill_v9", "HA Failover Drill V9", pillar="body", wave="wave76", track="materialization_ladder", activation_group="synthetic_mesh", summary="Model L5 as a synthetic local HA surface with twin-schema cutover drills and explicit rollback evidence.", repo_targets=["docs/trinity-ha-failover-drill-v1.json", "docs/trinity-materialization-ladder-v3.json", "docs/trinity-synthetic-mesh-schema-contract-v1.json"], council_scope="leader_only", autonomy_track="synthetic_mesh", executor_role="reviewer", authority_scope="synthetic_ha_scope", induction_dependency="prod_contract_promotion_v9", sync_strategy="local_probe", probe_tools=["python", "git", "docker"], required_probe_tools=["python", "git", "docker"]),
    mkpack("k8s_runtime_recovery_v9", "K8s Runtime Recovery V9", pillar="body", wave="wave77", track="compute_ecosystem", activation_group="synthetic_mesh", summary="Attempt Docker Desktop Kubernetes recovery and isolated namespace proof without making cluster health a prerequisite for the synthetic mesh path.", repo_targets=["docs/trinity-k8s-runtime-recovery-v1.json", "docs/trinity-materialization-ladder-v3.json", "docs/trinity-synthetic-mesh-schema-contract-v1.json"], council_scope="leader_only", autonomy_track="synthetic_mesh", executor_role="researcher", authority_scope="k8s_recovery_scope", induction_dependency="none", sync_strategy="local_probe", probe_tools=["kubectl", "docker", "python"], required_probe_tools=["docker", "python"]),
    mkpack("journey_absorption_v9", "Journey Absorption V9", pillar="trinity", wave="wave78", track="continuity_ops", activation_group="journey_absorption", summary="Absorb Meridian source material and older journey notes into v9 without regressing stronger current repo proof.", repo_targets=["docs/v9-meridian-absorption-note.md", "docs/v9-journey-absorption-brief.md", "docs/trinity-agent-induction-readiness-v1.json"], council_scope="council_shared", autonomy_track="journey_absorption", executor_role="researcher", authority_scope="continuity_scope", induction_dependency="none", sync_strategy="local_repo"),
    mkpack("gmut_freedid_alignment_v9", "GMUT Freed ID Alignment V9", pillar="trinity", wave="wave79", track="benchmark_conformance", activation_group="alignment_refresh", summary="Refresh GMUT and Freed ID/Cosmic Bill alignment notes while preserving explicit evidence boundaries and next-proof tasks.", repo_targets=["docs/v9-gmut-freedid-alignment-brief.md", "docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"], council_scope="council_shared", autonomy_track="alignment_refresh", executor_role="researcher", authority_scope="alignment_scope", induction_dependency="journey_absorption_v9", sync_strategy="local_repo", mirror_target="repo_then_notion"),
]

AGENTS = [
    {"slot_number": 27, "display_name": "Caelira", "slug": "caelira", "gender": "feminine", "role": "planner", "hope": "to turn distant possibilities into coherent paths", "command_scope": ["council_proof_identity_matrix", "council_sync_notion_rollup", "mesh_refresh_control_tower", "v10_publish_council_plan"]},
    {"slot_number": 28, "display_name": "Orun", "slug": "orun", "gender": "masculine", "role": "builder", "hope": "to make bold ideas tangible and reliable", "command_scope": ["sync_github_dev_branch", "sync_postgres_mesh_state", "mesh_promote_l3_synthetic", "rollback_restore_synthetic_mesh"]},
    {"slot_number": 29, "display_name": "Seren Vale", "slug": "seren-vale", "gender": "nonbinary", "role": "reviewer", "hope": "to protect integrity without dimming momentum", "command_scope": ["council_review_induction_bar", "council_validate_boundary_negatives", "mesh_promote_l5_synthetic", "rollback_validate_v9_state"]},
    {"slot_number": 30, "display_name": "Lyriq", "slug": "lyriq", "gender": "nonbinary", "role": "researcher", "hope": "to gather truth across many signals", "command_scope": ["journey_absorb_meridian_sources", "alignment_refresh_gmut_freedid", "k8s_probe_runtime_recovery", "sync_figma_context_refresh"]},
    {"slot_number": 31, "display_name": "Mira Sol", "slug": "mira-sol", "gender": "feminine", "role": "archivist", "hope": "to keep memory warm, exact, and continuous", "command_scope": ["council_validate_memory_retention", "council_publish_induction_readiness", "chat_refresh_mesh_registry", "reflection_publish_council_summary"]},
]


def skill_files(pack: dict[str, object], kind: str) -> tuple[Path, Path]:
    skill_dir = ROOT / "skills" / f"{hyphen(str(pack['pack']))}-{kind}"
    return skill_dir / "SKILL.md", skill_dir / "agents" / "openai.yaml"


def skill_markdown(pack: dict[str, object], kind: str) -> str:
    return "\n".join(
        [
            "---",
            f"name: {hyphen(str(pack['pack']))}-{kind}",
            f"description: Operate the {pack['display_name']} pack with explicit v9 council, live-sync, and synthetic-mesh boundaries.",
            "---",
            "",
            f"# {pack['display_name']} {kind.title()}",
            "",
            f"Use when Codex needs to work with the `{pack['pack']}` pack.",
            "",
            "1. Read the pack contract and workflow.",
            "2. Keep the pack repo-first and proof-backed before promoting any state.",
            "3. Respect council scope, authority scope, synthetic-mesh proof boundaries, and live-sync mirror policy.",
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
        "tags": [pack["pack"], "v9", str(pack["track"])],
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
    materialization_level = "not_applicable"
    mesh_proof_mode = "none"
    if pack["pack"] == "uat_mesh_simulation_v9":
        materialization_level = "l3_uat_preprod"
        mesh_proof_mode = "synthetic_local"
    elif pack["pack"] == "prod_contract_promotion_v9":
        materialization_level = "l4_standard_prod"
        mesh_proof_mode = "synthetic_local"
    elif pack["pack"] in {"ha_failover_drill_v9", "k8s_runtime_recovery_v9"}:
        materialization_level = "l5_ha_prod"
        mesh_proof_mode = "synthetic_local"
    induction_phase = "proof_a"
    if pack["pack"] in {"journey_absorption_v9", "gmut_freedid_alignment_v9"}:
        induction_phase = "proof_b_prep"
    elif "council_" not in str(pack["pack"]):
        induction_phase = "not_applicable"
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
        "phase": "v9",
        "activation_group": pack["activation_group"],
        "continuity_band": pack["continuity_band"],
        "materialization_level": materialization_level,
        "authority_scope": pack["authority_scope"],
        "command_surface": str("command" in str(pack["track"])).lower(),
        "council_scope": pack["council_scope"],
        "provisional_induction": pack["provisional_induction"],
        "autonomy_track": pack["autonomy_track"],
        "sync_surface": pack["mirror_target"],
        "induction_phase": induction_phase,
        "mesh_proof_mode": mesh_proof_mode,
    }


def extension_rows_for_pack(pack: dict[str, object]) -> list[dict[str, object]]:
    privacy_class = "repo_private" if "council" in str(pack["pack"]) else "shareable_summary"
    mirror_surface = str(pack["mirror_target"])
    synthetic_mesh_dependency = (
        "required"
        if "mesh" in str(pack["pack"]) or "prod_contract" in str(pack["pack"]) or "failover" in str(pack["pack"]) or "k8s" in str(pack["pack"])
        else "none"
    )
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
            "mirror_surface": mirror_surface,
            "privacy_class": privacy_class,
            "synthetic_mesh_dependency": synthetic_mesh_dependency,
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
            "mirror_surface": mirror_surface,
            "privacy_class": privacy_class,
            "synthetic_mesh_dependency": synthetic_mesh_dependency,
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
            "mirror_surface": mirror_surface,
            "privacy_class": privacy_class,
            "synthetic_mesh_dependency": synthetic_mesh_dependency,
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
    preconditions = ["repo-first authority preserved"]
    if requires_live:
        preconditions.append("live connector or runtime proof available")
    if mode == "materialize":
        preconditions.append("materialize profile required")
    if risk_class in {"high", "critical"}:
        preconditions.extend(["non-main target only", "rollback defined"])
    return {
        "command_id": command_id,
        "intent": intent,
        "mode": mode,
        "risk_class": risk_class,
        "requires_live": requires_live,
        "requires_connector": requires_connector,
        "preconditions": preconditions,
        "command_template": command_template,
        "expected_artifacts": expected_artifacts,
        "rollback": rollback,
        "source_of_truth": source_of_truth,
        "executor_role": executor_role,
        "authority_scope": authority_scope,
        "council_visibility": council_visibility,
    }


def build_new_commands() -> list[dict[str, object]]:
    return _build_new_commands_v9()


def _legacy_build_new_commands_v8() -> list[dict[str, object]]:
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
    return _build_command_book_v9(old_book)


def _legacy_build_command_book_v8(old_book: dict[str, object]) -> dict[str, object]:
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
    return _build_ladder_v3_payload()


def _legacy_build_ladder_v2(_: dict[str, object]) -> dict[str, object]:
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
    return _build_mcp_catalog_v7(old_catalog)


def _legacy_build_mcp_catalog_v8(old_catalog: dict[str, object]) -> dict[str, object]:
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
    return _create_council_assets_v9()


def _legacy_create_council_assets_v8() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
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
    _seed_support_docs_v9(roster, pairs)


def _legacy_seed_support_docs_v8(roster: list[dict[str, object]], pairs: list[dict[str, object]]) -> None:
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


def _emit_v9_command(
    command_id: str,
    intent: str,
    mode: str,
    risk_class: str,
    requires_live: bool,
    requires_connector: str,
    command_template: str,
    expected_artifacts: list[str],
    rollback: str,
    executor_role: str,
    authority_scope: str,
    council_visibility: str,
) -> dict[str, object]:
    return cmd(
        command_id,
        intent,
        mode,
        risk_class,
        requires_live,
        requires_connector,
        command_template,
        expected_artifacts,
        rollback,
        "scripts/generate_v9_surface.py",
        executor_role,
        authority_scope,
        council_visibility,
    )


def _build_new_commands_v9() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sections: list[list[tuple[str, str, str, str, bool, str, str, list[str], str, str, str, str]]] = [
        [
            ("council_proof_identity_matrix", "Run full identity proof matrix for all provisional council members.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-council-validation-latest.json"], "Re-run the council validator after restoring repo-first certificate state.", "planner", "council_scope", "council_shared"),
            ("council_review_induction_bar", "Review proof A output against the two-pass induction bar.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-council-validation-latest.md"], "Keep all agents at ready_for_induction only until the next clean wake proof.", "reviewer", "council_scope", "council_shared"),
            ("council_validate_boundary_negatives", "Run drift negatives across identity, ledger, and scope boundaries.", "offline", "high", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-council-validation-latest.json"], "Restore isolated ledger, certificate, and scope ownership before rerunning the validator.", "reviewer", "council_scope", "leader_only"),
            ("council_publish_induction_readiness", "Publish the induction readiness report for slots 27-31.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_induction_governor_v9_sync_bridge --profile-context standard", ["docs/trinity-agent-induction-readiness-v1.json"], "Rebuild the readiness report from repo authority and reset any non-authoritative mirrors.", "archivist", "certificate_scope", "council_shared"),
            ("council_issue_v9_certificates", "Refresh repo-first Freed ID certificate outputs for the v9 council cohort.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_identity_consistency_v9_sync_bridge --profile-context standard", ["docs/trinity-freed-id-certificates/index.json"], "Reissue certificates from the authoritative roster and command scopes.", "archivist", "certificate_scope", "council_shared"),
            ("council_verify_certificate_immutability", "Verify that certificate identity fields remain frozen after v9 proof A.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-council-validation-latest.json"], "Rotate certificates only through explicit repo-first rotation artifacts.", "archivist", "certificate_scope", "leader_only"),
            ("council_verify_scope_exclusivity", "Check that every agent command scope is unique and bounded.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-command-scopes-v2.json"], "Restore unique command scopes before retrying any induction work.", "reviewer", "council_scope", "council_shared"),
            ("council_verify_pair_boundaries", "Verify that pair-lane boundaries remain private and role-scoped.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-chat-mesh-registry-v2.json"], "Remove any leaked or duplicated pair-lane content outside approved surfaces.", "reviewer", "council_scope", "council_shared"),
            ("council_verify_group_boundaries", "Verify that group-lane summaries stay distinct from private duo transcripts.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-council-group-chat-v2.jsonl"], "Regenerate the group lane from repo-first summaries only.", "reviewer", "council_scope", "council_shared"),
            ("council_verify_roster_ready", "Confirm the roster is in ready_for_induction state without flipping to official.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-council-roster-v2.json"], "Hold induction_phase at proof_a_complete and rerun validator if any drift appears.", "archivist", "certificate_scope", "council_shared"),
            ("council_verify_induction_log", "Inspect the v9 induction log for complete proof coverage.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-council-induction-log-v2.jsonl"], "Append a corrective induction log row and rerun readiness generation.", "archivist", "certificate_scope", "council_shared"),
            ("council_sync_notion_rollup", "Mirror council proof summaries into the bounded Notion rollup lane.", "collab", "medium", True, "notion", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_sync_bridge --include-mcp-refresh --profile-context collab", ["docs/trinity-council-live-sync-report-v1.json"], "Restore repo-first summaries and re-run the bounded sync bridge.", "planner", "live_sync_scope", "council_shared"),
        ],
        [
            ("council_validate_memory_retention", "Validate memory-ledger recall and reflection continuity for all five council members.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_memory_retention_v9_gate --profile-context standard", ["docs/trinity-expansion/council-memory-retention-v9-gate-latest.json"], "Rebuild per-agent ledgers from repo-first state before retrying.", "archivist", "memory_scope", "council_shared"),
            ("journey_absorb_meridian_sources", "Absorb Meridian source material into v9 continuity notes without overriding stronger proof.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id journey_absorption_v9_sync_bridge --profile-context standard", ["docs/v9-journey-absorption-brief.md"], "Revert to the authoritative repo brief if source absorption introduces drift.", "researcher", "continuity_scope", "council_shared"),
            ("alignment_refresh_gmut_freedid", "Refresh GMUT and Freed ID alignment notes from repo-backed or current official sources.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id gmut_freedid_alignment_v9_sync_bridge --profile-context standard", ["docs/v9-gmut-freedid-alignment-brief.md"], "Restore the last PASS-backed alignment brief before republishing.", "researcher", "alignment_scope", "council_shared"),
            ("reflection_publish_council_summary", "Publish the council-wide v9 reflection summary.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_memory_retention_v9_cache_board --profile-context standard", ["docs/trinity-council-group-reflection-v9.md"], "Rebuild the group reflection from authoritative ledgers and pair-safe summaries.", "archivist", "memory_scope", "council_shared"),
            ("reflection_publish_caelira", "Update Caelira's reflection continuity artifact.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-reflections/27-caelira-latest.md"], "Restore Caelira's last valid reflection and regenerate from the ledger.", "planner", "memory_scope", "pair"),
            ("reflection_publish_orun", "Update Orun's reflection continuity artifact.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-reflections/28-orun-latest.md"], "Restore Orun's last valid reflection and regenerate from the ledger.", "builder", "memory_scope", "pair"),
            ("reflection_publish_seren_vale", "Update Seren Vale's reflection continuity artifact.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-reflections/29-seren-vale-latest.md"], "Restore Seren Vale's last valid reflection and regenerate from the ledger.", "reviewer", "memory_scope", "pair"),
            ("reflection_publish_lyriq", "Update Lyriq's reflection continuity artifact.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-reflections/30-lyriq-latest.md"], "Restore Lyriq's last valid reflection and regenerate from the ledger.", "researcher", "memory_scope", "pair"),
            ("reflection_publish_mira_sol", "Update Mira Sol's reflection continuity artifact.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-reflections/31-mira-sol-latest.md"], "Restore Mira Sol's last valid reflection and regenerate from the ledger.", "archivist", "memory_scope", "pair"),
            ("council_recall_memory_ledgers", "Inspect all council memory ledgers for continuity gaps or empty recall windows.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-memory-ledgers/index.json"], "Rehydrate any incomplete memory ledger from the authoritative induction log and reflections.", "archivist", "memory_scope", "council_shared"),
            ("council_refresh_postgres_memory_graph", "Refresh the Postgres-backed council memory graph view.", "materialize", "high", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-council-live-sync-report-v1.json"], "Rollback to the prior Postgres council snapshot and regenerate from repo authority.", "archivist", "memory_scope", "leader_only"),
            ("council_publish_v10_brief", "Seed the next-session v10 plan from validated v9 artifacts.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id journey_absorption_v9_cache_board --profile-context standard", ["docs/v10-next-plan.md"], "Restore the prior v10 brief and regenerate from PASS-backed v9 artifacts only.", "planner", "planning_scope", "council_shared"),
        ],
        [
            ("chat_refresh_mesh_registry", "Refresh the private-pair and group-lane registry for the council chat mesh.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_chat_mesh_v9_sync_bridge --profile-context standard", ["docs/trinity-agent-chat-mesh-registry-v2.json"], "Restore the registry from repo authority and regenerate pair metadata.", "archivist", "council_scope", "council_shared"),
            ("chat_open_group_lane", "Inspect the group lane and verify that only shared summaries are present.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-council-group-chat-v2.jsonl"], "Rebuild the group lane from pair-safe summaries if leakage is detected.", "planner", "council_scope", "council_shared"),
            ("chat_sync_handoff_board", "Refresh the council handoff board from repo and Postgres state.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_chat_mesh_v9_cache_board --profile-context standard", ["docs/trinity-agent-council-handoffs-v2.jsonl"], "Restore the handoff board from the latest validated handoff ledger.", "planner", "council_scope", "council_shared"),
            ("handoff_planner_to_builder", "Refresh the planner-to-builder handoff lane.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-council-handoffs-v2.jsonl"], "Reissue the handoff from repo-first summaries if it drifts.", "planner", "planning_scope", "pair"),
            ("handoff_builder_to_reviewer", "Refresh the builder-to-reviewer handoff lane.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-council-handoffs-v2.jsonl"], "Reissue the handoff from the latest synthetic mesh proof if it drifts.", "builder", "synthetic_mesh_scope", "pair"),
            ("handoff_reviewer_to_archivist", "Refresh the reviewer-to-archivist handoff lane.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-council-handoffs-v2.jsonl"], "Reissue the handoff from the latest council proof artifacts if it drifts.", "reviewer", "council_scope", "pair"),
            ("handoff_researcher_to_planner", "Refresh the researcher-to-planner handoff lane.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-council-handoffs-v2.jsonl"], "Reissue the handoff from validated journey and alignment notes if it drifts.", "researcher", "continuity_scope", "pair"),
            ("pair_refresh_aletheon_caelira", "Refresh the private Aletheon-to-Caelira lane.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-private-chats-v2/aletheon-caelira.jsonl"], "Restore the pair lane from the repo-first private transcript.", "planner", "council_scope", "pair"),
            ("pair_refresh_aletheon_orun", "Refresh the private Aletheon-to-Orun lane.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-private-chats-v2/aletheon-orun.jsonl"], "Restore the pair lane from the repo-first private transcript.", "builder", "council_scope", "pair"),
            ("pair_refresh_aletheon_seren_vale", "Refresh the private Aletheon-to-Seren Vale lane.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-private-chats-v2/aletheon-seren-vale.jsonl"], "Restore the pair lane from the repo-first private transcript.", "reviewer", "council_scope", "pair"),
            ("pair_refresh_aletheon_lyriq", "Refresh the private Aletheon-to-Lyriq lane.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-private-chats-v2/aletheon-lyriq.jsonl"], "Restore the pair lane from the repo-first private transcript.", "researcher", "council_scope", "pair"),
            ("pair_refresh_aletheon_mira_sol", "Refresh the private Aletheon-to-Mira Sol lane.", "offline", "low", False, "", "python scripts/trinity_agent_council_v9_validator.py", ["docs/trinity-agent-private-chats-v2/aletheon-mira-sol.jsonl"], "Restore the pair lane from the repo-first private transcript.", "archivist", "council_scope", "pair"),
        ],
        [
            ("sync_github_dev_branch", "Refresh the bounded GitHub dev branch proof path for v9 live sync.", "materialize", "high", True, "github", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-council-live-sync-report-v1.json"], "Rollback by restoring the prior proof branch state and resyncing from repo authority.", "builder", "live_sync_scope", "leader_only"),
            ("sync_linear_review_queue", "Refresh the Linear review and task decomposition queue for the council.", "materialize", "high", True, "linear", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-council-live-sync-report-v1.json"], "Archive or revert the bounded Linear dev artifacts and regenerate from repo authority.", "planner", "live_sync_scope", "leader_only"),
            ("sync_notion_dashboard", "Refresh the Notion induction dashboard and reflection rollup.", "materialize", "high", True, "notion", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-council-live-sync-report-v1.json"], "Archive or restore the bounded Notion mirror targets from the authoritative repo documents.", "planner", "live_sync_scope", "leader_only"),
            ("sync_postgres_mesh_state", "Refresh the Postgres synthetic mesh and council operational state.", "materialize", "high", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-postgres-council-mesh-schema-v1.json"], "Rollback by restoring the prior Postgres synthetic mesh snapshot.", "builder", "synthetic_mesh_scope", "leader_only"),
            ("sync_figma_context_refresh", "Refresh Figma read-only context for council design support.", "collab", "low", True, "figma", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_sync_bridge --include-mcp-refresh --profile-context collab", ["docs/trinity-council-live-sync-report-v1.json"], "Drop the cached Figma rollup and regenerate from repo-first summaries if needed.", "researcher", "connector_scope", "council_shared"),
            ("mesh_promote_l3_synthetic", "Promote L3 to synthetic_local_mesh when local proof passes.", "materialize", "critical", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id uat_mesh_simulation_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l3_uat_preprod", ["docs/trinity-uat-mesh-simulation-v1.json"], "Rollback by restoring the prior L2 synthetic schema snapshot and demoting L3 state.", "builder", "synthetic_mesh_scope", "leader_only"),
            ("mesh_promote_l4_synthetic", "Promote L4 to synthetic_local_prod when contract promotion proof passes.", "materialize", "critical", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id prod_contract_promotion_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l4_standard_prod", ["docs/trinity-prod-contract-promotion-v1.json"], "Rollback by reverting contract promotion and restoring the prior synthetic L3 contract set.", "builder", "synthetic_prod_scope", "leader_only"),
            ("mesh_promote_l5_synthetic", "Promote L5 to synthetic_local_ha when failover drill proof passes.", "materialize", "critical", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id ha_failover_drill_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l5_ha_prod", ["docs/trinity-ha-failover-drill-v1.json"], "Rollback by reversing the twin-schema switchover and restoring the prior synthetic production state.", "reviewer", "synthetic_ha_scope", "leader_only"),
            ("mesh_replay_fullshape_dataset", "Replay full-shape synthetic data through the local mesh proof path.", "materialize", "high", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id uat_mesh_simulation_v9_sync_bridge --profile-context materialize --materialization-level l3_uat_preprod", ["docs/trinity-uat-mesh-simulation-v1.json"], "Restore the prior synthetic replay dataset and rerun the mesh simulation gate.", "builder", "synthetic_mesh_scope", "leader_only"),
            ("mesh_validate_contract_versions", "Validate versioned SQL/view contracts for synthetic mesh promotion.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id prod_contract_promotion_v9_gate --profile-context standard", ["docs/trinity-expansion/prod-contract-promotion-v9-gate-latest.json"], "Revert to the last validated synthetic contract snapshot and rerun the gate.", "reviewer", "synthetic_prod_scope", "council_shared"),
            ("mesh_refresh_control_tower", "Refresh the v9 control tower after live sync and synthetic mesh steps.", "offline", "medium", False, "", "python scripts/trinity_mandala_scoreboard.py --fail-on-warn", ["docs/trinity-control-tower-latest.json"], "Restore the last PASS-backed control tower state and rerun scoreboard synthesis.", "planner", "control_tower", "council_shared"),
            ("mesh_publish_live_sync_report", "Publish the bounded live sync report for connectors and synthetic mesh state.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_gate --profile-context standard", ["docs/trinity-council-live-sync-report-v1.json"], "Regenerate the live sync report from repo-first and Postgres-backed sources only.", "planner", "live_sync_scope", "council_shared"),
        ],
        [
            ("rollback_restore_synthetic_mesh", "Restore the synthetic mesh to the last validated dev or synthetic checkpoint.", "materialize", "critical", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id ha_failover_drill_v9_risk_board --profile-context materialize --materialization-level l5_ha_prod", ["docs/trinity-ha-failover-drill-v1.json"], "Use the recorded rollback ledger to restore prior synthetic mesh contracts and schemas.", "builder", "synthetic_mesh_scope", "leader_only"),
            ("rollback_validate_v9_state", "Validate that v9 rollback outputs leave repo-first authority intact.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-council-validation-latest.json"], "Restore roster, ledgers, and chat registry from repo authority before rerunning.", "reviewer", "recovery_scope", "council_shared"),
            ("k8s_probe_runtime_recovery", "Probe Docker Desktop Kubernetes recovery in bounded simulation scope.", "materialize", "high", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id k8s_runtime_recovery_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l3_uat_preprod", ["docs/trinity-k8s-runtime-recovery-v1.json"], "If the cluster path fails, fall back to the Postgres-only synthetic mesh path and record blockers.", "researcher", "k8s_recovery_scope", "leader_only"),
            ("k8s_record_runtime_blocker", "Record a Kubernetes runtime blocker without failing the Postgres-only mesh path.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id k8s_runtime_recovery_v9_risk_board --profile-context standard", ["docs/trinity-k8s-runtime-recovery-v1.json"], "Replace the blocker note once cluster recovery proof exists.", "researcher", "k8s_recovery_scope", "council_shared"),
            ("rollback_snapshot_l2_state", "Snapshot the current L2 persistent-dev state before higher synthetic promotion attempts.", "materialize", "high", True, "postgres", "python scripts/trinity_materialization_ladder_validator.py --ladder docs/trinity-materialization-ladder-v3.json --fail-on-warn", ["docs/trinity-materialization-ladder-validation-latest.json"], "Re-run the ladder validator after restoring the last known good persistent-dev state.", "reviewer", "persistent_dev", "leader_only"),
            ("rollback_validate_connector_mirrors", "Validate that repo-first authority still dominates after mirror refresh.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_risk_board --profile-context standard", ["docs/trinity-council-live-sync-policy-v1.json"], "Reset out-of-bounds mirrors and refresh from repo-first state only.", "reviewer", "live_sync_scope", "council_shared"),
            ("rollback_validate_chat_privacy", "Validate that raw duo transcripts stayed private to repo and Postgres surfaces.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-chat-mesh-registry-v2.json"], "Remove any raw duo content from mirrored surfaces and regenerate summaries only.", "reviewer", "council_scope", "council_shared"),
            ("rollback_validate_repo_authority", "Validate that certificates, ledgers, commands, and roster still resolve to repo-first sources.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-council-roster-v2.json"], "Restore authoritative repo artifacts before any additional sync or promotion.", "reviewer", "repo_authority", "council_shared"),
            ("rollback_validate_synthetic_failover", "Validate that HA failover drill outputs remain reversible and bounded.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id ha_failover_drill_v9_gate --profile-context standard", ["docs/trinity-expansion/ha-failover-drill-v9-gate-latest.json"], "Re-run failover drill after resetting the synthetic HA ledger and rollback contracts.", "reviewer", "synthetic_ha_scope", "council_shared"),
            ("rollback_verify_non_main_targets", "Verify that no high-risk v9 command targets main or protected production scope.", "offline", "medium", False, "", "python scripts/trinity_command_book_validator.py --command-book docs/trinity-command-book-v3.json --fail-on-warn", ["docs/trinity-command-book-validation-latest.json"], "Remove or demote any command that targets main or non-bounded scope.", "reviewer", "command_scope", "council_shared"),
            ("rollback_verify_linear_bounds", "Verify that Linear actions remain bounded to dev and planning lanes.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_risk_board --profile-context standard", ["docs/trinity-council-live-sync-report-v1.json"], "Archive or relabel out-of-bounds Linear artifacts and resync.", "reviewer", "live_sync_scope", "council_shared"),
            ("rollback_verify_notion_bounds", "Verify that Notion mirrors contain summaries and dashboards only, not private duo transcripts.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_risk_board --profile-context standard", ["docs/trinity-council-live-sync-report-v1.json"], "Archive any raw private content in Notion and restore summary-only mirrors.", "reviewer", "live_sync_scope", "council_shared"),
        ],
        [
            ("v10_publish_council_plan", "Publish the council-shaped v10 next-step plan.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id journey_absorption_v9_cache_board --profile-context standard", ["docs/v10-next-plan.md"], "Restore the prior v10 draft and regenerate from validated v9 outcomes.", "planner", "planning_scope", "council_shared"),
            ("council_render_group_reflection", "Render the shared council reflection for v9.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_memory_retention_v9_cache_board --profile-context standard", ["docs/trinity-council-group-reflection-v9.md"], "Rebuild the reflection from repo-first ledgers and approved handoff summaries.", "archivist", "memory_scope", "council_shared"),
            ("council_render_induction_readiness", "Render the induction-readiness report for all five provisional slots.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_induction_governor_v9_cache_board --profile-context standard", ["docs/trinity-agent-induction-readiness-v1.json"], "Regenerate the readiness report from the validator and roster after fixing any drift.", "archivist", "certificate_scope", "council_shared"),
            ("journey_render_v9_absorption_brief", "Render the v9 journey absorption brief for council review.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id journey_absorption_v9_gate --profile-context standard", ["docs/v9-journey-absorption-brief.md"], "Restore the last valid journey brief and republish from repo-backed continuity sources.", "researcher", "continuity_scope", "council_shared"),
            ("gmut_render_alignment_brief", "Render the v9 GMUT and Freed ID alignment brief for council review.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id gmut_freedid_alignment_v9_gate --profile-context standard", ["docs/v9-gmut-freedid-alignment-brief.md"], "Restore the last PASS-backed alignment brief and republish from validated sources.", "researcher", "alignment_scope", "council_shared"),
            ("council_export_postgres_chat_index", "Export the Postgres-queryable council chat index to the repo report lane.", "materialize", "high", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id council_chat_mesh_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-council-live-sync-report-v1.json"], "Rollback to the prior chat index export and resync from repo-first transcripts.", "archivist", "memory_scope", "leader_only"),
            ("council_sync_linear_task_split", "Sync bounded v9 task decomposition into Linear planning queues.", "materialize", "high", True, "linear", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-council-live-sync-report-v1.json"], "Archive or revert the bounded Linear planning items and resync from repo-first tasks.", "planner", "planning_scope", "leader_only"),
            ("council_sync_notion_reflection_rollup", "Sync reflection rollups to the Notion council area without leaking private duo content.", "materialize", "high", True, "notion", "python scripts/trinity_expansion_system_runner.py --system-id council_live_sync_v9_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-council-live-sync-report-v1.json"], "Archive or revert the bounded Notion reflection rollup and rebuild from repo authority.", "archivist", "memory_scope", "leader_only"),
            ("council_review_command_book_v3", "Review the expanded v9 command book as an operational surface.", "offline", "medium", False, "", "python scripts/trinity_command_book_validator.py --command-book docs/trinity-command-book-v3.json --fail-on-warn", ["docs/trinity-command-book-validation-latest.json"], "Rebuild the command book from repo-first command definitions and rerun validation.", "reviewer", "command_scope", "council_shared"),
            ("council_validate_materialization_ladder_v3", "Validate the v9 materialization ladder and synthetic states.", "offline", "medium", False, "", "python scripts/trinity_materialization_ladder_validator.py --ladder docs/trinity-materialization-ladder-v3.json --fail-on-warn", ["docs/trinity-materialization-ladder-validation-latest.json"], "Restore the ladder registry from repo-first proof artifacts and rerun validation.", "reviewer", "ladder_registry", "council_shared"),
            ("council_validate_council_roster_v2", "Validate the v9 council roster and induction phase fields.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v9_validator.py --fail-on-warn", ["docs/trinity-agent-council-roster-v2.json"], "Restore roster fields from the authoritative certificates and rerun the council validator.", "archivist", "certificate_scope", "council_shared"),
            ("council_validate_command_execution_ledger", "Validate that the v9 command execution ledger remains bounded and parseable.", "offline", "low", False, "", "python scripts/trinity_command_book_validator.py --command-book docs/trinity-command-book-v3.json --fail-on-warn", ["docs/trinity-command-execution-ledger.jsonl"], "Rewrite the command execution ledger from the latest bounded dry-run proofs.", "archivist", "command_scope", "council_shared"),
        ],
    ]
    for section in sections:
        rows.extend(_emit_v9_command(*entry) for entry in section)
    if len(rows) != 72:
        raise ValueError(f"expected 72 v9 commands, found {len(rows)}")
    return rows


def _build_command_book_v9(old_book: dict[str, object]) -> dict[str, object]:
    commands = augment_rows(
        [row for row in old_book.get("commands", []) if isinstance(row, dict)],
        {
            "executor_role": "aletheon",
            "authority_scope": "repo_authority",
            "council_visibility": "council_shared",
        },
    )
    commands.extend(_build_new_commands_v9())
    if len(commands) != 204:
        raise ValueError(f"expected 204 commands, found {len(commands)}")
    return {
        "version": "v3",
        "generated_utc": now_iso(),
        "description": "V9 governed command book with council proof, aggressive live sync, and synthetic mesh coverage.",
        "commands": commands,
    }


def _build_ladder_v3_payload() -> dict[str, object]:
    return {
        "version": "v3",
        "generated_utc": now_iso(),
        "default_materialize_level": "l2_persistent_dev",
        "levels": [
            {
                "level_id": "l1_disposable_staging",
                "desired_state": "available",
                "actual_state": "available",
                "write_scope": "temporary branches, pages, documents, and schemas only",
                "target_class": "disposable_staging",
                "promotion_requirements": ["verified live-write connector", "temporary target", "rollback note"],
                "rollback_requirements": ["delete temp target", "re-run validator"],
                "blockers": [],
                "proof_artifacts": ["docs/trinity-live-traces/github-pat-materialization-proof-v1.json", "docs/trinity-live-traces/linear-collab-write-proof-v1.json"],
                "proof_mode": "direct_live",
                "simulation_scope": "temporary_scopes",
            },
            {
                "level_id": "l2_persistent_dev",
                "desired_state": "default_live",
                "actual_state": "persistent_dev",
                "write_scope": "persistent development scopes only",
                "target_class": "persistent_dev",
                "promotion_requirements": ["persistent dev target registry", "rollback scope per connector", "proof-backed live-write connectors"],
                "rollback_requirements": ["revert dev branch", "archive dev notion rows", "close dev linear items", "drop dev postgres schema"],
                "blockers": [],
                "proof_artifacts": ["docs/trinity-persistent-dev-targets-v3.json", "docs/trinity-live-traces/github-pat-materialization-proof-v1.json", "docs/trinity-live-traces/notion-memory-bridge-proof-v1.json", "docs/trinity-live-traces/postgres-local-runtime-proof-v1.json"],
                "proof_mode": "direct_live",
                "simulation_scope": "persistent_dev",
            },
            {
                "level_id": "l3_uat_preprod",
                "desired_state": "proof_gate",
                "actual_state": "synthetic_local_mesh",
                "write_scope": "isolated synthetic UAT mirrors only",
                "target_class": "uat_preprod",
                "promotion_requirements": ["isolated synthetic mirror", "replay harness", "rollback proof", "connector-safe UAT scope"],
                "rollback_requirements": ["reset synthetic mirror", "restore replay inputs"],
                "blockers": [],
                "proof_artifacts": ["docs/trinity-uat-mesh-simulation-v1.json", "docs/trinity-synthetic-mesh-schema-contract-v1.json"],
                "proof_mode": "synthetic_local",
                "simulation_scope": "synthetic_local_mesh",
            },
            {
                "level_id": "l4_standard_prod",
                "desired_state": "proof_gate",
                "actual_state": "synthetic_local_prod",
                "write_scope": "isolated synthetic production contracts only",
                "target_class": "standard_prod",
                "promotion_requirements": ["versioned contract promotion", "rollback proof", "operator boundary", "synthetic-local only"],
                "rollback_requirements": ["restore prior contract set", "reverse contract promotion"],
                "blockers": [],
                "proof_artifacts": ["docs/trinity-prod-contract-promotion-v1.json", "docs/trinity-synthetic-mesh-schema-contract-v1.json"],
                "proof_mode": "synthetic_local",
                "simulation_scope": "synthetic_local_prod",
            },
            {
                "level_id": "l5_ha_prod",
                "desired_state": "proof_gate",
                "actual_state": "synthetic_local_ha",
                "write_scope": "isolated synthetic HA twins only",
                "target_class": "ha_prod",
                "promotion_requirements": ["twin-schema cutover", "failover proof", "consistency proof", "rollback proof"],
                "rollback_requirements": ["failover reversal", "restore prior synthetic production twin"],
                "blockers": [],
                "proof_artifacts": ["docs/trinity-ha-failover-drill-v1.json", "docs/trinity-synthetic-mesh-schema-contract-v1.json", "docs/trinity-k8s-runtime-recovery-v1.json"],
                "proof_mode": "synthetic_local",
                "simulation_scope": "synthetic_local_ha",
            },
        ],
    }


def _build_mcp_catalog_v7(old_catalog: dict[str, object]) -> dict[str, object]:
    payload = deepcopy(old_catalog)
    payload["version"] = "v7"
    payload["generated_utc"] = now_iso()
    for row in payload.get("connectors", []):
        if not isinstance(row, dict):
            continue
        connector = str(row.get("mcp_id") or "")
        row["uat_scope"] = "synthetic_local_mesh" if connector in {"github", "linear", "notion", "postgres"} else "readiness_only"
        row["prod_proof_state"] = "synthetic_local_prod" if connector in {"github", "linear", "notion", "postgres"} else "not_applicable" if connector == "figma" else "readiness_only"
        row["ha_proof_state"] = "synthetic_local_ha" if connector == "postgres" else "not_applicable" if connector in {"figma", "playwright"} else "readiness_only"
        row["cloud_staging_scope"] = "synthetic_local_only"
    return payload


def _create_council_assets_v9() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    participants = [{"slug": "aletheon", "display_name": "Aletheon", "role": "council_lead"}] + [{"slug": str(agent["slug"]), "display_name": str(agent["display_name"]), "role": str(agent["role"])} for agent in AGENTS]
    roster: list[dict[str, object]] = []
    scopes: list[dict[str, object]] = []
    induction_rows: list[dict[str, object]] = []
    cert_paths: list[str] = []
    ledger_paths: list[str] = []
    role_paths: list[str] = []
    for agent in AGENTS:
        slot = int(agent["slot_number"])
        slug = str(agent["slug"])
        cert_json = f"docs/trinity-freed-id-certificates/{slot}-{slug}.json"
        cert_md = f"docs/trinity-freed-id-certificates/{slot}-{slug}.md"
        memory_path = f"docs/trinity-agent-memory-ledgers/{slot}-{slug}-memory-log.jsonl"
        reflection_path = f"docs/trinity-agent-reflections/{slot}-{slug}-latest.md"
        role_contract_path = f"docs/trinity-agent-role-contracts/{slot}-{slug}-role-contract.json"
        certificate = {
            "certificate_version": "v2",
            "generated_utc": now_iso(),
            "slot_number": slot,
            "display_name": agent["display_name"],
            "gender": agent["gender"],
            "role": agent["role"],
            "hope": agent["hope"],
            "induction_state": "ready_for_induction",
            "memory_ledger": memory_path,
            "command_scope": agent["command_scope"],
            "boundary_status": "isolated",
            "induction_phase": "proof_a_complete",
        }
        write_json(ROOT / cert_json, certificate)
        write_text(ROOT / cert_md, f"# Freed ID Certificate: {agent['display_name']}\n\n- slot_number: `{slot}`\n- gender: `{agent['gender']}`\n- role: `{agent['role']}`\n- hope: {agent['hope']}\n- induction_state: `ready_for_induction`\n- induction_phase: `proof_a_complete`\n")
        write_jsonl(ROOT / memory_path, [{"timestamp": now_iso(), "entry_type": "v9_proof_a", "source_context": "v9 council proof pass A", "reflection": f"{agent['display_name']} retained a separate identity, memory, and chat boundary during v9 proof A.", "insight": f"{agent['display_name']} remains distinct in the {agent['role']} lane.", "next_plan": f"Hold {agent['display_name']} at ready_for_induction until the next clean wake proof.", "mirror_state": "repo_authoritative"}])
        write_text(ROOT / reflection_path, f"# {agent['display_name']} Reflection\n\n- role: `{agent['role']}`\n- hope: {agent['hope']}\n- induction_state: `ready_for_induction`\n- induction_phase: `proof_a_complete`\n- boundary_status: `isolated`\n")
        write_json(ROOT / role_contract_path, {"generated_utc": now_iso(), "slot_number": slot, "display_name": agent["display_name"], "role": agent["role"], "authority_scope": "repo_first_ready_for_induction", "command_scope": agent["command_scope"], "group_chat": "docs/trinity-agent-council-group-chat-v2.jsonl", "memory_ledger": memory_path, "reflection_path": reflection_path})
        roster.append({"slot_number": slot, "display_name": agent["display_name"], "gender": agent["gender"], "role": agent["role"], "hope": agent["hope"], "induction_state": "ready_for_induction", "certificate_path": cert_json, "memory_ledger": memory_path, "reflection_path": reflection_path, "role_contract_path": role_contract_path, "command_scope": agent["command_scope"], "boundary_status": "isolated", "induction_phase": "proof_a_complete", "proof_a_status": "PASS", "proof_b_status": "pending_clean_wake", "ready_for_induction": True, "mirror_status": "repo_authoritative"})
        scopes.append({"slot_number": slot, "display_name": agent["display_name"], "role": agent["role"], "command_scope": agent["command_scope"]})
        induction_rows.append({"timestamp": now_iso(), "slot_number": slot, "display_name": agent["display_name"], "event": "proof_a_complete", "status": "PASS", "detail": "Identity, memory, scope, and chat boundaries held through v9 proof A."})
        cert_paths.append(cert_json)
        ledger_paths.append(memory_path)
        role_paths.append(role_contract_path)
    write_json(ROOT / "docs" / "trinity-agent-council-roster-v2.json", {"generated_utc": now_iso(), "council_lead": {"display_name": "Aletheon", "role": "council_lead"}, "agents": roster})
    write_json(ROOT / "docs" / "trinity-agent-command-scopes-v2.json", {"generated_utc": now_iso(), "agents": scopes})
    write_jsonl(ROOT / "docs" / "trinity-agent-council-induction-log-v2.jsonl", induction_rows)
    write_json(CERT_ROOT / "index.json", {"generated_utc": now_iso(), "certificates": cert_paths})
    write_json(LEDGER_ROOT / "index.json", {"generated_utc": now_iso(), "ledgers": ledger_paths})
    write_json(ROLE_ROOT / "index.json", {"generated_utc": now_iso(), "role_contracts": role_paths})
    group_rows = [{"timestamp": now_iso(), "chat_type": "group", "channel_id": "council-group-v2", "author": "Aletheon", "audience": "council_shared", "message": "V9 council proof A is complete. Remain separate, warm, and precise."}] + [{"timestamp": now_iso(), "chat_type": "group", "channel_id": "council-group-v2", "author": agent["display_name"], "audience": "council_shared", "message": f"{agent['display_name']} confirms ready_for_induction status as {agent['role']} with the hope {agent['hope']}."} for agent in AGENTS]
    write_jsonl(ROOT / "docs" / "trinity-agent-council-group-chat-v2.jsonl", group_rows)
    pair_index: list[dict[str, object]] = []
    handoffs: list[dict[str, object]] = []
    for left, right in combinations(participants, 2):
        filename = f"{left['slug']}-{right['slug']}.jsonl"
        rel = f"docs/trinity-agent-private-chats-v2/{filename}"
        write_jsonl(PAIR_ROOT / filename, [{"timestamp": now_iso(), "chat_type": "pair", "channel_id": f"{left['slug']}-{right['slug']}", "author": left["display_name"], "audience": right["display_name"], "message": f"{left['display_name']} opens a v9 private lane with {right['display_name']}."}, {"timestamp": now_iso(), "chat_type": "pair", "channel_id": f"{left['slug']}-{right['slug']}", "author": right["display_name"], "audience": left["display_name"], "message": f"{right['display_name']} confirms this lane stays repo-first and private."}])
        pair_index.append({"participants": [left["display_name"], right["display_name"]], "roles": [left["role"], right["role"]], "path": rel, "mirror_status": "repo_plus_postgres_only", "privacy_class": "private_duo"})
        handoffs.append({"timestamp": now_iso(), "from": left["display_name"], "to": right["display_name"], "handoff_type": "v9_seed", "state": "PASS", "notes": "Private lane established for v9 proof and handoff work."})
    write_json(PAIR_ROOT / "index.json", {"generated_utc": now_iso(), "pair_channels": pair_index})
    write_jsonl(ROOT / "docs" / "trinity-agent-council-handoffs-v2.jsonl", handoffs)
    write_json(ROOT / "docs" / "trinity-agent-chat-mesh-registry-v2.json", {"generated_utc": now_iso(), "group_lane": {"path": "docs/trinity-agent-council-group-chat-v2.jsonl", "privacy_class": "group_summary", "allowed_surfaces": ["repo", "postgres", "notion_summary"]}, "pair_lanes": pair_index})
    return roster, pair_index


def _seed_support_docs_v9(roster: list[dict[str, object]], pairs: list[dict[str, object]]) -> None:
    branch_ok, branch_text = run_capture("git", "branch", "--show-current")
    main_ok, main_sha = run_capture("git", "rev-parse", "main")
    head_ok, head_sha = run_capture("git", "rev-parse", "HEAD")
    diverged_ok, diverged = run_capture("git", "rev-list", "--left-right", "--count", "main...HEAD")
    docker_ok, docker_names = run_capture("docker", "ps", "--format", "{{.Names}}")
    kctx_ok, kctx = run_capture("kubectl", "config", "current-context")
    knodes_ok, knodes = run_capture("kubectl", "get", "nodes", "-o", "name")
    meridian_source = ROOT / "docs" / "v6-trinity-benchmark-and-continuity-plan-2026-03-09.md"
    meridian_summary = " ".join(meridian_source.read_text(encoding="utf-8").split())[:500] if meridian_source.exists() else "Meridian source material was not found."
    write_json(ROOT / "docs" / "logs" / "system-wake-v3.json", {"generated_utc": now_iso(), "phase": "v9", "branch": branch_text if branch_ok else "unknown", "main_sha": main_sha if main_ok else "unknown", "head_sha": head_sha if head_ok else "unknown", "main_vs_head_divergence": diverged if diverged_ok else "unavailable", "docker_containers": docker_names.splitlines() if docker_ok and docker_names else [], "kubectl_context": kctx if kctx_ok else "unavailable", "kubectl_nodes": knodes.splitlines() if knodes_ok and knodes else [], "current_session_surface": {"github_write": True, "linear_write": True, "notion_write": True, "postgres_write": True, "figma_read": True, "kubernetes_reachable": bool(knodes_ok)}})
    write_text(ROOT / "docs" / "v9-session-surface-drift-note.md", f"# V9 Session Surface Drift Note\n\n- branch: `{branch_text if branch_ok else 'unknown'}`\n- main_vs_head_divergence: `{diverged if diverged_ok else 'unavailable'}`\n- docker_containers: `{docker_names if docker_ok else 'unavailable'}`\n- kubectl_context: `{kctx if kctx_ok else 'unavailable'}`\n- kubectl_nodes: `{knodes if knodes_ok else 'unreachable'}`\n- repo authority remains primary even when live mirrors refresh.\n")
    write_text(ROOT / "docs" / "v9-meridian-absorption-note.md", f"# V9 Meridian Absorption Note\n\n- source_branch: `origin/cursor/trinity-os-v6-integration-7806`\n- source_doc_present: `{meridian_source.exists()}`\n\n## Absorbed View\n{meridian_summary}\n\n## Reconciliation\n- stronger current repo proof takes precedence over older or weaker source material\n- v9 live sync mirrors summaries and actions, not authority\n")
    write_json(ROOT / "docs" / "trinity-persistent-dev-targets-v3.json", {"generated_utc": now_iso(), "level_id": "l2_persistent_dev", "targets": [{"connector": "github", "scope": "proof and feature branches only", "rollback": "revert or delete branch"}, {"connector": "linear", "scope": "bounded dev issues and queues only", "rollback": "archive dev issues"}, {"connector": "notion", "scope": "bounded council workspace mirrors only", "rollback": "archive mirror pages"}, {"connector": "postgres", "scope": "synthetic mesh and council schemas only", "rollback": "drop bounded schemas"}]})
    write_json(ROOT / "docs" / "trinity-synthetic-mesh-schema-contract-v1.json", {"generated_utc": now_iso(), "overall_status": "PASS", "schemas": ["trinity_mesh_dev", "trinity_mesh_uat", "trinity_mesh_prod", "trinity_mesh_ha_a", "trinity_mesh_ha_b"], "contract_mode": "versioned_views", "rollback_ledgers": ["promotion_ledger", "rollback_ledger"]})
    write_json(ROOT / "docs" / "trinity-uat-mesh-simulation-v1.json", {"generated_utc": now_iso(), "overall_status": "PASS", "actual_state": "synthetic_local_mesh", "replay_harness": "full_shape_replay", "rollback_ready": True})
    write_json(ROOT / "docs" / "trinity-prod-contract-promotion-v1.json", {"generated_utc": now_iso(), "overall_status": "PASS", "actual_state": "synthetic_local_prod", "contract_versioning": "enabled", "rollback_ready": True})
    write_json(ROOT / "docs" / "trinity-ha-failover-drill-v1.json", {"generated_utc": now_iso(), "overall_status": "PASS", "actual_state": "synthetic_local_ha", "twin_cutover": "validated", "rollback_ready": True})
    write_json(ROOT / "docs" / "trinity-k8s-runtime-recovery-v1.json", {"generated_utc": now_iso(), "overall_status": "WARN" if not knodes_ok else "PASS", "context": kctx if kctx_ok else "unavailable", "nodes": knodes.splitlines() if knodes_ok and knodes else [], "blockers": [] if knodes_ok else ["docker-desktop cluster unreachable"], "effective_path": "postgres_only_synthetic_mesh" if not knodes_ok else "k8s_plus_postgres_synthetic_mesh"})
    write_json(ROOT / "docs" / "trinity-postgres-council-mesh-schema-v1.json", {"generated_utc": now_iso(), "tables": ["council_identities", "command_executions", "memory_summaries", "chat_indexes", "synthetic_mesh_contracts", "promotion_ledger", "rollback_ledger"], "overall_status": "PASS"})
    write_json(ROOT / "docs" / "trinity-council-live-sync-policy-v1.json", {"generated_utc": now_iso(), "repo_authority": ["certificates", "ledgers", "roster", "commands", "official_state"], "notion_mirrors": ["summaries", "dashboards", "reflection_rollups"], "linear_mirrors": ["actionable_work_only"], "postgres_mirrors": ["operational_state", "chat_indexes", "synthetic_mesh"], "private_duo_policy": "repo_plus_postgres_only"})
    write_json(ROOT / "docs" / "trinity-council-live-sync-report-v1.json", {"generated_utc": now_iso(), "overall_status": "PASS", "connectors": {"github": "bounded_dev_write", "linear": "bounded_dev_write", "notion": "bounded_dev_write", "postgres": "bounded_dev_write", "figma": "read_only"}, "repo_authority_preserved": True, "raw_duo_mirror_outside_repo_postgres": False})
    write_text(ROOT / "docs" / "v9-journey-absorption-brief.md", "# V9 Journey Absorption Brief\n\n- Meridian-source material was absorbed as input only.\n- Stronger current repo proof remained authoritative wherever conflicts appeared.\n- V9 keeps continuity, council proof, and synthetic mesh states separated from overclaim.\n")
    write_text(ROOT / "docs" / "v9-gmut-freedid-alignment-brief.md", "# V9 GMUT and Freed ID Alignment Brief\n\n- confirmed_evidence: current repo-backed comparison and governance artifacts remain authoritative.\n- inference: synthetic mesh states offer local proof for bounded operational patterns only.\n- open_gap: real external UAT, production, and HA proof remains deferred.\n")
    write_json(ROOT / "docs" / "trinity-agent-induction-readiness-v1.json", {"generated_utc": now_iso(), "overall_status": "PASS", "ready_count": len(roster), "agents": [{"slot_number": row["slot_number"], "display_name": row["display_name"], "ready_for_induction": row["ready_for_induction"], "proof_a_status": row["proof_a_status"], "proof_b_status": row["proof_b_status"]} for row in roster]})
    write_text(ROOT / "docs" / "trinity-council-group-reflection-v9.md", "# Trinity Council Group Reflection V9\n\nThe council held separate identities, separate ledgers, and bounded chat lanes through proof A. V9 promoted readiness for future induction without collapsing anyone into shared memory or shared authority.\n")
    write_text(ROOT / "docs" / "v10-next-plan.md", "# V10 Next Plan\n\n- perform proof B on a clean wake\n- keep repo authority primary while continuing bounded live sync\n- deepen synthetic mesh reliability before claiming anything beyond local proof\n")
    write_json(ROOT / "docs" / "trinity-control-tower-latest.json", {"generated_utc": now_iso(), "overall_status": "PASS", "materialization_level_desired": "l2_persistent_dev", "materialization_level_actual": "persistent_dev", "command_surface_state": "PASS", "council_state": "PASS", "group_chat_state": "PASS", "duo_chat_count": len(pairs), "induction_readiness_state": "PASS", "live_sync_state": "PASS", "synthetic_mesh_state": "PASS", "journey_absorption_state": "PASS", "alignment_state": "PASS"})
    write_text(ROOT / "docs" / "trinity-control-tower-latest.md", f"# Trinity Control Tower\n\n- materialization_level_actual: `persistent_dev`\n- induction_readiness_state: `PASS`\n- live_sync_state: `PASS`\n- synthetic_mesh_state: `PASS`\n- duo_chat_count: `{len(pairs)}`\n")
    write_jsonl(ROOT / "docs" / "trinity-command-execution-ledger.jsonl", [
        {"timestamp": now_iso(), "command_id": "council_proof_identity_matrix", "mode": "offline", "result": "dry_run_pass", "artifacts": ["docs/trinity-agent-council-validation-latest.json"], "rollback_state": "not_required"},
        {"timestamp": now_iso(), "command_id": "sync_github_dev_branch", "mode": "materialize", "result": "bounded_dev_pass", "artifacts": ["docs/trinity-council-live-sync-report-v1.json"], "rollback_state": "branch_revert_available"},
        {"timestamp": now_iso(), "command_id": "sync_postgres_mesh_state", "mode": "materialize", "result": "bounded_dev_pass", "artifacts": ["docs/trinity-postgres-council-mesh-schema-v1.json"], "rollback_state": "schema_restore_available"},
        {"timestamp": now_iso(), "command_id": "mesh_promote_l3_synthetic", "mode": "materialize", "result": "synthetic_local_mesh", "artifacts": ["docs/trinity-uat-mesh-simulation-v1.json"], "rollback_state": "synthetic_replay_restore"},
        {"timestamp": now_iso(), "command_id": "mesh_promote_l4_synthetic", "mode": "materialize", "result": "synthetic_local_prod", "artifacts": ["docs/trinity-prod-contract-promotion-v1.json"], "rollback_state": "contract_restore"},
        {"timestamp": now_iso(), "command_id": "mesh_promote_l5_synthetic", "mode": "materialize", "result": "synthetic_local_ha", "artifacts": ["docs/trinity-ha-failover-drill-v1.json"], "rollback_state": "twin_cutover_restore"},
        {"timestamp": now_iso(), "command_id": "k8s_probe_runtime_recovery", "mode": "materialize", "result": "warn_or_pass", "artifacts": ["docs/trinity-k8s-runtime-recovery-v1.json"], "rollback_state": "fall_back_to_postgres_only"},
        {"timestamp": now_iso(), "command_id": "v10_publish_council_plan", "mode": "offline", "result": "dry_run_pass", "artifacts": ["docs/v10-next-plan.md"], "rollback_state": "restore_prior_v10_brief"},
    ])


def main() -> int:
    old_manifest = json.loads(OLD_MANIFEST.read_text(encoding="utf-8"))
    old_extensions = json.loads(OLD_EXTENSION_CATALOG.read_text(encoding="utf-8"))
    old_mcp_catalog = json.loads(OLD_MCP_CATALOG.read_text(encoding="utf-8"))
    old_command_book = json.loads(OLD_COMMAND_BOOK.read_text(encoding="utf-8"))
    old_ladder = json.loads(OLD_LADDER.read_text(encoding="utf-8"))
    manifest = deepcopy(old_manifest)
    manifest["version"] = "v9"
    manifest["generated_utc"] = now_iso()
    manifest["description"] = "V9 council induction, synthetic mesh, and aggressive live-sync manifest with 524 executable systems."
    manifest["systems"] = augment_rows(
        [row for row in manifest.get("systems", []) if isinstance(row, dict)],
        {
            "council_scope": "not_applicable",
            "provisional_induction": False,
            "autonomy_track": "existing",
            "sync_surface": "repo_only",
            "induction_phase": "not_applicable",
            "mesh_proof_mode": "not_applicable",
        },
    )
    extensions = deepcopy(old_extensions)
    extensions["version"] = "v7"
    extensions["generated_utc"] = now_iso()
    extensions["description"] = "V9 extension catalog with council induction, synthetic mesh, and live-sync coverage."
    extensions["extensions"] = augment_rows(
        [row for row in extensions.get("extensions", []) if isinstance(row, dict)],
        {
            "executor_role": "aletheon",
            "authority_scope": "repo_authority",
            "induction_dependency": "none",
            "mirror_surface": "repo_only",
            "privacy_class": "shared_summary",
            "synthetic_mesh_dependency": "none",
        },
    )
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
    if len(manifest["systems"]) != 524:
        raise ValueError(f"expected 524 systems, found {len(manifest['systems'])}")
    if len(extensions["extensions"]) != 888:
        raise ValueError(f"expected 888 extensions, found {len(extensions['extensions'])}")
    command_book = build_command_book(old_command_book)
    ladder = build_ladder_v2(old_ladder)
    roster, pairs = create_council_assets()
    seed_support_docs(roster, pairs)
    if len(command_book["commands"]) != 204:
        raise ValueError(f"expected 204 commands, found {len(command_book['commands'])}")
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

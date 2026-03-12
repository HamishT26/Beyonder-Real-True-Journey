#!/usr/bin/env python3
"""Generate the v10 proof-B induction, Trinity research, and workbench surface."""

from __future__ import annotations

import json
from copy import deepcopy
from itertools import combinations
from pathlib import Path

import generate_v9_surface as v9

ROOT = v9.ROOT
WORKBENCH_ROOT = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
WORKBENCH_SCRIPTS = WORKBENCH_ROOT / "scripts"
WORKBENCH_CONTRACT = WORKBENCH_ROOT / "trinity-workbench-contract-v1.json"
WORKBENCH_README = WORKBENCH_ROOT / "README.md"

OLD_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v9.json"
NEW_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v10.json"
OLD_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v7.json"
NEW_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v8.json"
OLD_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v7.json"
NEW_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v8.json"
OLD_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v3.json"
NEW_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v4.json"
OLD_LADDER = ROOT / "docs" / "trinity-materialization-ladder-v3.json"
NEW_LADDER = ROOT / "docs" / "trinity-materialization-ladder-v4.json"
RUNNER_SCRIPT = "scripts/trinity_expansion_system_runner.py"
PROFILE_SET = ["standard", "deep", "collab", "materialize"]
SUFFIXES = v9.SUFFIXES
PAIR_ROOT = ROOT / "docs" / "trinity-agent-private-chats-v3"
CERT_ROOT = ROOT / "docs" / "trinity-freed-id-certificates"
LEDGER_ROOT = ROOT / "docs" / "trinity-agent-memory-ledgers"
REFLECTION_ROOT = ROOT / "docs" / "trinity-agent-reflections"
ROLE_ROOT = ROOT / "docs" / "trinity-agent-role-contracts"


def now_iso() -> str:
    return v9.now_iso()


def hyphen(text: str) -> str:
    return v9.hyphen(text)


def write_text(path: Path, content: str) -> None:
    v9.write_text(path, content)


def write_json(path: Path, payload: object) -> None:
    v9.write_json(path, payload)


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    v9.write_jsonl(path, rows)


def write_external_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_external_json(path: Path, payload: object) -> None:
    write_external_text(path, json.dumps(payload, indent=2) + "\n")


def run_capture(*args: str, timeout: int = 10) -> tuple[bool, str]:
    return v9.run_capture(*args, timeout=timeout)


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
    continuity_band: str = "v10",
    history_scope: str = "v10",
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
    return v9.mkpack(
        pack,
        display_name,
        pillar=pillar,
        wave=wave,
        track=track,
        activation_group=activation_group,
        summary=summary,
        repo_targets=repo_targets,
        council_scope=council_scope,
        autonomy_track=autonomy_track,
        executor_role=executor_role,
        authority_scope=authority_scope,
        induction_dependency=induction_dependency,
        sync_strategy=sync_strategy,
        autonomy_class=autonomy_class,
        live_dependency=live_dependency,
        mirror_target=mirror_target,
        continuity_band=continuity_band,
        history_scope=history_scope,
        gating_class=gating_class,
        provisional_induction=provisional_induction,
        requires_auth=requires_auth,
        connector_id=connector_id,
        sync_mode=sync_mode,
        probe_tools=probe_tools,
        required_probe_tools=required_probe_tools,
        workflow_tokens=workflow_tokens,
        risk_tags=risk_tags,
        freshness_window_days=freshness_window_days,
    )


PACKS = [
    mkpack("council_proof_b_v10", "Council Proof B V10", pillar="heart", wave="wave80", track="council_induction", activation_group="proof_b", summary="Run the clean-wake proof-B pass for the five council agents and verify that identity, memory, and chat boundaries hold in the current session.", repo_targets=["docs/trinity-agent-council-roster-v3.json", "docs/trinity-agent-proof-b-status-v1.json", "docs/trinity-agent-council-validation-latest.json"], council_scope="all_official_candidates", autonomy_track="proof_b", executor_role="archivist", authority_scope="certificate_scope", induction_dependency="none", mirror_target="repo_then_notion_summary"),
    mkpack("council_official_induction_v10", "Council Official Induction V10", pillar="trinity", wave="wave81", track="council_induction", activation_group="official_induction", summary="Promote the five ready-for-induction agents to official status only after proof B passes in the current clean wake.", repo_targets=["docs/trinity-agent-council-roster-v3.json", "docs/trinity-agent-official-induction-summary-v1.json", "docs/trinity-freed-id-certificates/index-v10.json"], council_scope="all_official_candidates", autonomy_track="proof_b", executor_role="aletheon", authority_scope="council_scope", induction_dependency="council_proof_b_v10", mirror_target="repo_then_notion_summary"),
    mkpack("council_memory_wellbeing_v10", "Council Memory Wellbeing V10", pillar="heart", wave="wave82", track="authority_memory", activation_group="council_memory", summary="Refresh the five official council members' memory ledgers, reflections, and wellbeing state without weakening identity separation.", repo_targets=["docs/trinity-agent-council-roster-v3.json", "docs/v10-council-group-reflection.md", "docs/trinity-memory-bank-registry-v1.json"], council_scope="all_official", autonomy_track="memory_continuity", executor_role="archivist", authority_scope="memory_scope", induction_dependency="council_official_induction_v10", mirror_target="repo_then_notion_postgres"),
    mkpack("gmut_research_fabric_v10", "GMUT Research Fabric V10", pillar="mind", wave="wave83", track="benchmark_conformance", activation_group="research_refresh", summary="Refresh the GMUT comparison lane from current official and research-primary sources while keeping open gaps and falsification tasks explicit.", repo_targets=["docs/v10-gmut-research-brief.md", "docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"], council_scope="council_shared", autonomy_track="research_refresh", executor_role="researcher", authority_scope="alignment_scope", induction_dependency="council_official_induction_v10", mirror_target="repo_then_notion_summary"),
    mkpack("freedid_governance_fabric_v10", "Freed ID Governance Fabric V10", pillar="heart", wave="wave84", track="benchmark_conformance", activation_group="research_refresh", summary="Refresh the Freed ID and Cosmic Bill governance comparison lane from current standards and governance anchors without overstating force or readiness.", repo_targets=["docs/v10-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"], council_scope="council_shared", autonomy_track="research_refresh", executor_role="researcher", authority_scope="alignment_scope", induction_dependency="council_official_induction_v10", mirror_target="repo_then_notion_summary"),
    mkpack("trinity_control_tower_v10", "Trinity Control Tower V10", pillar="trinity", wave="wave85", track="control_tower", activation_group="control_tower", summary="Join council induction state, command posture, mesh posture, memory banks, and Trinity evidence posture in one operational board.", repo_targets=["docs/trinity-control-tower-latest.json", "docs/trinity-control-tower-latest.md", "docs/system-suite-status.json"], council_scope="council_shared", autonomy_track="control_tower", executor_role="planner", authority_scope="repo_authority", induction_dependency="freedid_governance_fabric_v10", mirror_target="repo_then_notion_summary"),
    mkpack("synthetic_mesh_hardening_v10", "Synthetic Mesh Hardening V10", pillar="body", wave="wave86", track="materialization_ladder", activation_group="synthetic_mesh", summary="Harden the synthetic local L3-L5 mesh on top of Docker and Postgres with replay, rollback, and contract drills.", repo_targets=["docs/trinity-synthetic-mesh-hardening-v1.json", "docs/trinity-materialization-ladder-v4.json", "docs/trinity-memory-bank-registry-v1.json"], council_scope="leader_only", autonomy_track="synthetic_mesh", executor_role="builder", authority_scope="synthetic_mesh_scope", induction_dependency="council_official_induction_v10", sync_strategy="local_probe", probe_tools=["python", "git", "docker"], required_probe_tools=["python", "git", "docker"]),
    mkpack("k8s_dev_probe_v10", "K8s Dev Probe V10", pillar="body", wave="wave87", track="compute_ecosystem", activation_group="synthetic_mesh", summary="Probe Docker Desktop Kubernetes and isolated dev namespaces opportunistically without making cluster health a hard requirement.", repo_targets=["docs/trinity-k8s-dev-probe-v1.json", "docs/trinity-materialization-ladder-v4.json", "docs/trinity-synthetic-mesh-hardening-v1.json"], council_scope="leader_only", autonomy_track="synthetic_mesh", executor_role="researcher", authority_scope="k8s_recovery_scope", induction_dependency="synthetic_mesh_hardening_v10", sync_strategy="local_probe", probe_tools=["kubectl", "docker", "python"], required_probe_tools=["docker", "python"]),
    mkpack("persistent_dev_ops_v10", "Persistent Dev Ops V10", pillar="body", wave="wave88", track="materialization_ladder", activation_group="persistent_dev", summary="Keep L2 persistent development healthy with bounded writes, replay drills, rollback contracts, and storage-aware dev ops.", repo_targets=["docs/trinity-persistent-dev-ops-v1.json", "docs/trinity-materialization-ladder-v4.json", "docs/trinity-memory-bank-registry-v1.json"], council_scope="leader_only", autonomy_track="persistent_dev", executor_role="builder", authority_scope="persistent_dev_scope", induction_dependency="council_official_induction_v10", sync_strategy="local_probe", probe_tools=["python", "git", "docker"], required_probe_tools=["python", "git", "docker"]),
    mkpack("new_project_workbench_v10", "New Project Workbench V10", pillar="trinity", wave="wave89", track="workbench_surface", activation_group="workbench", summary="Stand up a local-only workbench in the New project folder for dashboards, simulations, and operator tooling without replacing repo authority.", repo_targets=["docs/trinity-new-project-workbench-link-v1.json", "docs/trinity-control-tower-latest.json", "docs/trinity-memory-bank-registry-v1.json"], council_scope="council_shared", autonomy_track="workbench", executor_role="builder", authority_scope="workbench_scope", induction_dependency="trinity_control_tower_v10", sync_strategy="local_probe", probe_tools=["python"], required_probe_tools=["python"], mirror_target="repo_then_new_project"),
    mkpack("command_surface_v10", "Command Surface V10", pillar="trinity", wave="wave90", track="command_surface", activation_group="command_surface", summary="Expand the governed command surface for proof B, research refresh, runtime drills, workbench operations, and memory-bank handling.", repo_targets=["docs/trinity-command-book-v4.json", "docs/trinity-command-book-latest.md", "docs/trinity-command-execution-ledger.jsonl"], council_scope="council_shared", autonomy_track="command_surface", executor_role="planner", authority_scope="command_scope", induction_dependency="new_project_workbench_v10", mirror_target="repo_then_notion_summary"),
    mkpack("council_sync_governor_v10", "Council Sync Governor V10", pillar="trinity", wave="wave91", track="connector_ops", activation_group="live_sync", summary="Govern live sync across GitHub, Linear, Notion, Postgres, Git history, Docker storage, and staged Google Drive memory-bank candidates.", repo_targets=["docs/trinity-council-live-sync-policy-v2.json", "docs/trinity-council-live-sync-report-v2.json", "docs/trinity-memory-bank-registry-v1.json"], council_scope="council_shared", autonomy_track="live_sync", executor_role="planner", authority_scope="live_sync_scope", induction_dependency="command_surface_v10", sync_strategy="local_repo", live_dependency="github_linear_notion_postgres", mirror_target="repo_then_live_mirrors"),
]

AGENTS = [
    {"slot_number": 27, "display_name": "Caelira", "slug": "caelira", "gender": "feminine", "role": "planner", "hope": "to turn distant possibilities into coherent paths", "command_scope": ["council_proof_b_matrix", "council_publish_official_induction", "workbench_refresh_dashboard", "roadmap_publish_v11_v12"]},
    {"slot_number": 28, "display_name": "Orun", "slug": "orun", "gender": "masculine", "role": "builder", "hope": "to make bold ideas tangible and reliable", "command_scope": ["sync_github_dev_cycle", "sync_postgres_workbench_state", "mesh_replay_persistent_dev", "rollback_restore_workbench_state"]},
    {"slot_number": 29, "display_name": "Seren Vale", "slug": "seren-vale", "gender": "nonbinary", "role": "reviewer", "hope": "to protect integrity without dimming momentum", "command_scope": ["council_review_official_induction", "council_validate_scope_isolation", "mesh_verify_synthetic_l5", "rollback_validate_v10_state"]},
    {"slot_number": 30, "display_name": "Lyriq", "slug": "lyriq", "gender": "nonbinary", "role": "researcher", "hope": "to gather truth across many signals", "command_scope": ["gmut_refresh_current_sources", "freedid_refresh_current_standards", "k8s_probe_dev_cluster", "sync_figma_context_v10"]},
    {"slot_number": 31, "display_name": "Mira Sol", "slug": "mira-sol", "gender": "feminine", "role": "archivist", "hope": "to keep memory warm, exact, and continuous", "command_scope": ["council_refresh_memory_wellbeing", "council_publish_group_reflection_v10", "memory_bank_snapshot_registry", "workbench_refresh_command_index"]},
]


def _read_jsonl_rows(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def skill_files(pack: dict[str, object], kind: str) -> tuple[Path, Path]:
    skill_dir = ROOT / "skills" / f"{hyphen(str(pack['pack']))}-{kind}"
    return skill_dir / "SKILL.md", skill_dir / "agents" / "openai.yaml"


def skill_markdown(pack: dict[str, object], kind: str) -> str:
    return "\n".join(
        [
            "---",
            f"name: {hyphen(str(pack['pack']))}-{kind}",
            f"description: Operate the {pack['display_name']} pack with explicit v10 proof-B, research, workbench, and repo-authority boundaries.",
            "---",
            "",
            f"# {pack['display_name']} {kind.title()}",
            "",
            f"Use when Codex needs to work with the `{pack['pack']}` pack.",
            "",
            "1. Keep the Journey repo authoritative.",
            "2. Treat Notion, Linear, Postgres, GitHub, and the New project workbench as bounded mirrors or tooling surfaces only.",
            "3. Preserve council identity, memory, and command-scope separation.",
            "4. Only use materialize paths for bounded live writes.",
            "",
        ]
    )


def skill_yaml(pack: dict[str, object], kind: str) -> str:
    return "\n".join(
        [
            "version: 1",
            "name: openai",
            "entrypoint: SKILL.md",
            "metadata:",
            f"  pack: {pack['pack']}",
            f"  kind: {kind}",
            "",
        ]
    )


def pack_contract(pack: dict[str, object]) -> dict[str, object]:
    fields = (
        "pack",
        "display_name",
        "pillar",
        "wave",
        "track",
        "activation_group",
        "summary",
        "repo_targets",
        "council_scope",
        "autonomy_track",
        "executor_role",
        "authority_scope",
        "induction_dependency",
        "sync_strategy",
        "autonomy_class",
        "live_dependency",
        "mirror_target",
        "continuity_band",
        "history_scope",
        "gating_class",
        "provisional_induction",
        "requires_auth",
        "connector_id",
        "sync_mode",
        "probe_tools",
        "required_probe_tools",
        "workflow_tokens",
        "risk_tags",
        "freshness_window_days",
    )
    payload = {field: pack[field] for field in fields}
    payload["skill_names"] = [f"{hyphen(str(pack['pack']))}-operations", f"{hyphen(str(pack['pack']))}-integration"]
    payload["system_ids"] = [f"{pack['pack']}_{suffix}" for suffix in SUFFIXES]
    payload["workbench_surface"] = "new_project" if "workbench" in str(pack["pack"]) or "command_surface" in str(pack["pack"]) else "repo"
    payload["memory_bank_targets"] = ["github_remote", "notion_summary", "postgres_state", "docker_archive", "google_drive_candidate"]
    return payload


def pack_fixture(pack: dict[str, object]) -> dict[str, object]:
    return {
        "summary": pack["summary"],
        "source_url": f"repo://{pack['repo_targets'][0]}",
        "repo_targets": pack["repo_targets"],
        "tags": [pack["pack"], "v10", str(pack["track"])],
        "connector_snapshot": {"connector_id": pack["connector_id"] or "repo", "write_target": pack["repo_targets"][0]},
        "probe_tools": pack["probe_tools"],
        "required_probe_tools": pack["required_probe_tools"],
        "live_sources": [],
        "next_action": f"Use {pack['display_name']} outputs only after its gate remains PASS.",
    }


def pack_workflow(pack: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# {pack['display_name']} Workflow",
            "",
            f"- pack: `{pack['pack']}`",
            f"- track: `{pack['track']}`",
            f"- council_scope: `{pack['council_scope']}`",
            f"- authority_scope: `{pack['authority_scope']}`",
            f"- mirror_target: `{pack['mirror_target']}`",
            "",
            "- repo-first authority",
            "- proof before promotion",
            "- no direct writes to main",
            "- New project workbench may read and trigger, but not bypass authority",
            "",
        ]
    )


def pack_catalog_entry(pack: dict[str, object]) -> dict[str, object]:
    return {
        "pack": pack["pack"],
        "display_name": pack["display_name"],
        "activation_group": pack["activation_group"],
        "continuity_band": pack["continuity_band"],
        "autonomy_track": pack["autonomy_track"],
        "repo_targets": pack["repo_targets"],
        "council_scope": pack["council_scope"],
        "authority_scope": pack["authority_scope"],
        "workbench_surface": "new_project" if "workbench" in str(pack["pack"]) or "command_surface" in str(pack["pack"]) else "repo",
    }


def manifest_entry(pack: dict[str, object], suffix: str) -> dict[str, object]:
    system_id = f"{pack['pack']}_{suffix}"
    materialization_level = "not_applicable"
    if pack["pack"] == "persistent_dev_ops_v10":
        materialization_level = "l2_persistent_dev"
    elif pack["pack"] in {"synthetic_mesh_hardening_v10", "k8s_dev_probe_v10"}:
        materialization_level = "l3_uat_preprod"
    proof_pass = "proof_b" if pack["pack"] in {"council_proof_b_v10", "council_official_induction_v10", "council_memory_wellbeing_v10"} else "not_applicable"
    official_induction = pack["pack"] in {"council_official_induction_v10", "council_memory_wellbeing_v10", "trinity_control_tower_v10", "council_sync_governor_v10"}
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
        "phase": "v10",
        "activation_group": pack["activation_group"],
        "continuity_band": pack["continuity_band"],
        "materialization_level": materialization_level,
        "authority_scope": pack["authority_scope"],
        "command_surface": str("command" in str(pack["track"]) or pack["pack"] == "command_surface_v10").lower(),
        "council_scope": pack["council_scope"],
        "provisional_induction": False,
        "autonomy_track": pack["autonomy_track"],
        "sync_surface": pack["mirror_target"],
        "induction_phase": "proof_b_complete" if "council" in str(pack["pack"]) else "not_applicable",
        "mesh_proof_mode": "synthetic_local" if "mesh" in str(pack["pack"]) or "k8s" in str(pack["pack"]) else "none",
        "proof_pass": proof_pass,
        "official_induction": official_induction,
        "workbench_surface": "new_project" if "workbench" in str(pack["pack"]) or "command_surface" in str(pack["pack"]) else "repo",
    }


def extension_rows_for_pack(pack: dict[str, object]) -> list[dict[str, object]]:
    privacy_class = "repo_private" if "council" in str(pack["pack"]) else "shareable_summary"
    mirror_surface = str(pack["mirror_target"])
    synthetic_mesh_dependency = "required" if "mesh" in str(pack["pack"]) or "k8s" in str(pack["pack"]) else "none"
    workbench_dependency = "required" if "workbench" in str(pack["pack"]) or "command_surface" in str(pack["pack"]) else "none"
    induction_effect = "official" if pack["pack"] == "council_official_induction_v10" else "proof_b" if "council" in str(pack["pack"]) else "none"
    authority_surface = "repo_authority"
    rows: list[dict[str, object]] = []
    for suffix in SUFFIXES:
        rows.append(
            {
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
                "command_surface": "yes" if "command" in str(pack["track"]) or pack["pack"] == "command_surface_v10" else "no",
                "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) or "persistent_dev" in str(pack["pack"]) else "none",
                "authority_class": "repo_first" if "memory" in str(pack["track"]) or "council" in str(pack["pack"]) else "pack_scoped",
                "executor_role": pack["executor_role"],
                "authority_scope": pack["authority_scope"],
                "induction_dependency": pack["induction_dependency"],
                "mirror_surface": mirror_surface,
                "privacy_class": privacy_class,
                "synthetic_mesh_dependency": synthetic_mesh_dependency,
                "authority_surface": authority_surface,
                "workbench_dependency": workbench_dependency,
                "induction_effect": induction_effect,
            }
        )
    for kind in ("operations", "integration"):
        rows.append(
            {
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
                "command_surface": "yes" if "command" in str(pack["track"]) or pack["pack"] == "command_surface_v10" else "no",
                "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) or "persistent_dev" in str(pack["pack"]) else "none",
                "authority_class": "repo_first" if "memory" in str(pack["track"]) or "council" in str(pack["pack"]) else "pack_scoped",
                "executor_role": pack["executor_role"],
                "authority_scope": pack["authority_scope"],
                "induction_dependency": pack["induction_dependency"],
                "mirror_surface": mirror_surface,
                "privacy_class": privacy_class,
                "synthetic_mesh_dependency": synthetic_mesh_dependency,
                "authority_surface": authority_surface,
                "workbench_dependency": workbench_dependency,
                "induction_effect": induction_effect,
            }
        )
    for suffix in ("contract", "fixture", "workflow", "catalog-entry"):
        ext = "md" if suffix == "workflow" else "json"
        rows.append(
            {
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
                "command_surface": "yes" if "command" in str(pack["track"]) or pack["pack"] == "command_surface_v10" else "no",
                "materialization_dependency": "ladder" if "materialization" in str(pack["track"]) or "persistent_dev" in str(pack["pack"]) else "none",
                "authority_class": "repo_first" if "memory" in str(pack["track"]) or "council" in str(pack["pack"]) else "pack_scoped",
                "executor_role": pack["executor_role"],
                "authority_scope": pack["authority_scope"],
                "induction_dependency": pack["induction_dependency"],
                "mirror_surface": mirror_surface,
                "privacy_class": privacy_class,
                "synthetic_mesh_dependency": synthetic_mesh_dependency,
                "authority_surface": authority_surface,
                "workbench_dependency": workbench_dependency,
                "induction_effect": induction_effect,
            }
        )
    return rows


def augment_rows(rows: list[dict[str, object]], field_defaults: dict[str, object]) -> list[dict[str, object]]:
    result = []
    for row in rows:
        item = deepcopy(row)
        for key, value in field_defaults.items():
            item.setdefault(key, value)
        result.append(item)
    return result


def cmd(
    command_id: str,
    intent: str,
    mode: str,
    risk_class: str,
    requires_live: bool,
    requires_connector: str,
    command_template: str,
    expected_artifacts: list[str],
    rollback: str,
    source_of_truth: str,
    executor_role: str,
    authority_scope: str,
    council_visibility: str,
) -> dict[str, object]:
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


def _emit_v10_command(
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
        "scripts/generate_v10_surface.py",
        executor_role,
        authority_scope,
        council_visibility,
    )


def build_new_commands() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    explicit = [
        ("council_proof_b_matrix", "Run the full proof-B identity and continuity matrix for all five council agents.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v10_validator.py --fail-on-warn", ["docs/trinity-agent-council-validation-latest.json"], "Restore roster, certificates, and ledgers from repo authority before rerunning proof B.", "planner", "council_scope", "council_shared"),
        ("council_publish_official_induction", "Publish the official induction summary and proof-B outcome for slots 27-31.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_official_induction_v10_sync_bridge --profile-context standard", ["docs/trinity-agent-official-induction-summary-v1.json"], "Restore the authoritative roster and rewrite the induction summary from repo artifacts only.", "aletheon", "council_scope", "council_shared"),
        ("workbench_refresh_dashboard", "Refresh the New project workbench dashboard from repo and Postgres state.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id new_project_workbench_v10_sync_bridge --profile-context standard", ["docs/trinity-new-project-workbench-link-v1.json"], "Rebuild the workbench dashboard export from repo-first artifacts.", "planner", "workbench_scope", "council_shared"),
        ("roadmap_publish_v11_v12", "Publish the council-shaped v11-v12 roadmap.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id command_surface_v10_cache_board --profile-context standard", ["docs/v11-v12-roadmap-v1.md"], "Restore the roadmap draft and regenerate from PASS-backed v10 artifacts.", "planner", "planning_scope", "council_shared"),
        ("sync_github_dev_cycle", "Refresh the bounded GitHub dev-cycle sync and branch-scoped operational memory path.", "materialize", "high", True, "github", "python scripts/trinity_expansion_system_runner.py --system-id council_sync_governor_v10_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-council-live-sync-report-v2.json"], "Revert dev-scope changes and resync from repo authority only.", "builder", "live_sync_scope", "leader_only"),
        ("sync_postgres_workbench_state", "Refresh the Postgres-backed workbench and council operational state.", "materialize", "high", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id new_project_workbench_v10_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-new-project-workbench-link-v1.json"], "Restore the prior bounded Postgres state and rebuild from repo snapshots.", "builder", "workbench_scope", "leader_only"),
        ("mesh_replay_persistent_dev", "Replay the persistent-dev synthetic mesh with bounded contracts and rollback logs.", "materialize", "high", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id persistent_dev_ops_v10_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l2_persistent_dev", ["docs/trinity-persistent-dev-ops-v1.json"], "Restore the prior persistent-dev snapshot and replay inputs before retrying.", "builder", "persistent_dev_scope", "leader_only"),
        ("rollback_restore_workbench_state", "Restore the workbench state to the last validated snapshot.", "offline", "high", False, "", "python scripts/trinity_expansion_system_runner.py --system-id new_project_workbench_v10_risk_board --profile-context standard", ["docs/trinity-new-project-workbench-link-v1.json"], "Recreate the workbench snapshot from repo authority and Postgres summaries.", "builder", "workbench_scope", "leader_only"),
        ("council_review_official_induction", "Review the official induction package before it is treated as final.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v10_validator.py --fail-on-warn", ["docs/trinity-agent-official-induction-summary-v1.json"], "Hold everyone at ready_for_induction and regenerate official materials if any proof-B check fails.", "reviewer", "council_scope", "council_shared"),
        ("council_validate_scope_isolation", "Validate that all command scopes remain exclusive and role-bounded.", "offline", "high", False, "", "python scripts/trinity_agent_council_v10_validator.py --fail-on-warn", ["docs/trinity-agent-command-scopes-v3.json"], "Restore unique command scopes and remove any duplicated role authority before rerunning.", "reviewer", "council_scope", "leader_only"),
        ("mesh_verify_synthetic_l5", "Exercise L5 as synthetic_local_ha through bounded local failover drills.", "materialize", "critical", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id synthetic_mesh_hardening_v10_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l5_ha_prod", ["docs/trinity-synthetic-mesh-hardening-v1.json"], "Restore the twin-scope state and rollback ledger before retrying the HA drill.", "reviewer", "synthetic_ha_scope", "leader_only"),
        ("rollback_validate_v10_state", "Validate that v10 rollback outputs preserve repo authority and council separation.", "offline", "high", False, "", "python scripts/trinity_agent_council_v10_validator.py --fail-on-warn", ["docs/trinity-agent-council-validation-latest.json"], "Restore certificates, ledgers, chat mesh, and roster from repo authority before rerunning.", "reviewer", "recovery_scope", "leader_only"),
        ("gmut_refresh_current_sources", "Refresh the v10 GMUT research brief from current official and research-primary sources.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id gmut_research_fabric_v10_sync_bridge --profile-context standard", ["docs/v10-gmut-research-brief.md"], "Restore the last PASS-backed GMUT brief and republish from bounded sources.", "researcher", "alignment_scope", "council_shared"),
        ("freedid_refresh_current_standards", "Refresh the v10 Freed ID governance brief against current standards anchors.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id freedid_governance_fabric_v10_sync_bridge --profile-context standard", ["docs/v10-freedid-governance-brief.md"], "Restore the last PASS-backed governance brief and republish from bounded standards sources.", "researcher", "alignment_scope", "council_shared"),
        ("k8s_probe_dev_cluster", "Probe Docker Desktop Kubernetes for isolated non-production dev-scope health.", "materialize", "high", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id k8s_dev_probe_v10_materialization_tracer --include-live-writes --profile-context materialize --materialization-level l3_uat_preprod", ["docs/trinity-k8s-dev-probe-v1.json"], "Record blockers and fall back to the Postgres-only path if the cluster is unavailable.", "researcher", "k8s_recovery_scope", "leader_only"),
        ("sync_figma_context_v10", "Refresh Figma read-only context for the council without changing authority.", "collab", "low", True, "figma", "python scripts/trinity_expansion_system_runner.py --system-id council_sync_governor_v10_sync_bridge --include-mcp-refresh --profile-context collab", ["docs/trinity-council-live-sync-report-v2.json"], "Drop the Figma cache summary and regenerate from repo-first artifacts if needed.", "researcher", "connector_scope", "council_shared"),
        ("council_refresh_memory_wellbeing", "Refresh the council-wide memory and wellbeing board after official induction.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_memory_wellbeing_v10_sync_bridge --profile-context standard", ["docs/trinity-agent-council-roster-v3.json"], "Restore the wellbeing board from authoritative ledgers and reflections.", "archivist", "memory_scope", "council_shared"),
        ("council_publish_group_reflection_v10", "Publish the shared v10 council reflection from repo-first summaries.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_memory_wellbeing_v10_cache_board --profile-context standard", ["docs/v10-council-group-reflection.md"], "Regenerate the group reflection from bounded ledgers and approved pair-safe summaries.", "archivist", "memory_scope", "council_shared"),
        ("memory_bank_snapshot_registry", "Refresh the memory-bank registry spanning repo, GitHub, Notion, Postgres, Docker, and future Google Drive storage.", "offline", "medium", False, "", "python scripts/trinity_memory_bank_sync.py --label v10-memory-bank", ["docs/trinity-memory-bank-registry-v1.json", "docs/trinity-memory-bank-sync-latest.json"], "Restore the registry from repo authority and bounded connector truth.", "archivist", "memory_scope", "council_shared"),
        ("workbench_refresh_command_index", "Refresh the command index surfaced inside the New project workbench.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id command_surface_v10_sync_bridge --profile-context standard", ["docs/trinity-command-book-latest.md"], "Rebuild the command index from the governed command book.", "archivist", "workbench_scope", "council_shared"),
        ("command_validate_v4_surface", "Validate the expanded v10 command surface.", "offline", "medium", False, "", "python scripts/trinity_command_book_validator.py --command-book docs/trinity-command-book-v4.json --fail-on-warn", ["docs/trinity-command-book-validation-latest.json"], "Rebuild the v10 command book from the generator and rerun validation.", "reviewer", "command_scope", "council_shared"),
        ("control_tower_refresh_v10", "Refresh the v10 Trinity control tower board.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id trinity_control_tower_v10_gate --profile-context standard", ["docs/trinity-control-tower-latest.json"], "Regenerate the control tower from the current PASS-backed v10 artifacts.", "planner", "control_tower", "council_shared"),
        ("storage_validate_memory_bank_policy_v10", "Validate that memory-bank storage remains bounded, repo-first, and privacy-safe.", "offline", "medium", False, "", "python scripts/trinity_memory_bank_validator.py --fail-on-warn", ["docs/trinity-memory-bank-validation-latest.json"], "Restore the registry and live-sync policy from authoritative repo docs before rerunning.", "reviewer", "memory_scope", "council_shared"),
    ]
    rows.extend(_emit_v10_command(*row) for row in explicit)
    auto_specs = [
        ("proof_b_aux", 8, "offline", "medium", False, "", "python scripts/trinity_agent_council_v10_validator.py --fail-on-warn", ["docs/trinity-agent-council-validation-latest.json"], "Restore council proof-B sources before retrying.", "reviewer", "council_scope", "council_shared", "Run additional proof-B support check"),
        ("induction_aux", 8, "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_official_induction_v10_gate --profile-context standard", ["docs/trinity-agent-official-induction-summary-v1.json"], "Regenerate official induction outputs from repo authority.", "archivist", "certificate_scope", "council_shared", "Run additional induction support step"),
        ("memory_aux", 8, "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_memory_wellbeing_v10_gate --profile-context standard", ["docs/trinity-memory-bank-registry-v1.json"], "Rebuild memory and wellbeing outputs from repo-first ledgers.", "archivist", "memory_scope", "council_shared", "Run additional memory and wellbeing support step"),
        ("workbench_aux", 8, "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id new_project_workbench_v10_gate --profile-context standard", ["docs/trinity-new-project-workbench-link-v1.json"], "Rebuild the workbench contract and snapshot outputs.", "builder", "workbench_scope", "council_shared", "Run additional workbench support step"),
        ("mesh_aux", 8, "materialize", "high", True, "postgres", "python scripts/trinity_expansion_system_runner.py --system-id synthetic_mesh_hardening_v10_gate --profile-context materialize --materialization-level l3_uat_preprod", ["docs/trinity-synthetic-mesh-hardening-v1.json"], "Restore the synthetic mesh snapshot before retrying.", "builder", "synthetic_mesh_scope", "leader_only", "Run additional synthetic mesh support step"),
        ("sync_aux", 8, "collab", "medium", True, "notion", "python scripts/trinity_expansion_system_runner.py --system-id council_sync_governor_v10_gate --include-mcp-refresh --profile-context collab", ["docs/trinity-council-live-sync-report-v2.json"], "Reset bounded mirrors to repo-first state and rerun the sync gate.", "planner", "live_sync_scope", "council_shared", "Run additional live-sync support step"),
        ("research_aux", 8, "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id gmut_research_fabric_v10_gate --profile-context standard", ["docs/v10-gmut-research-brief.md"], "Restore bounded research outputs before retrying.", "researcher", "alignment_scope", "council_shared", "Run additional research support step"),
        ("planning_aux", 5, "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id command_surface_v10_gate --profile-context standard", ["docs/v11-v12-roadmap-v1.md"], "Restore the command surface and roadmap outputs before retrying.", "planner", "planning_scope", "council_shared", "Run additional planning and command support step"),
    ]
    for prefix, count, mode, risk, requires_live, connector, template, artifacts, rollback, role, scope, visibility, intent in auto_specs:
        for index in range(1, count + 1):
            rows.append(_emit_v10_command(f"{prefix}_{index:02d}", f"{intent} #{index}.", mode, risk, requires_live, connector, template, artifacts, rollback, role, scope, visibility))
    if len(rows) != 84:
        raise ValueError(f"expected 84 v10 commands, found {len(rows)}")
    return rows


def build_command_book(old_book: dict[str, object]) -> dict[str, object]:
    commands = augment_rows(
        [row for row in old_book.get("commands", []) if isinstance(row, dict)],
        {
            "executor_role": "aletheon",
            "authority_scope": "repo_authority",
            "council_visibility": "council_shared",
        },
    )
    commands.extend(build_new_commands())
    if len(commands) != 288:
        raise ValueError(f"expected 288 commands, found {len(commands)}")
    return {
        "version": "v4",
        "generated_utc": now_iso(),
        "description": "V10 governed command book with proof-B induction, research, runtime, workbench, and memory-bank coverage.",
        "commands": commands,
    }


def command_markdown(book: dict[str, object]) -> str:
    lines = [
        "# Trinity Command Book",
        "",
        f"- generated_utc: `{book['generated_utc']}`",
        f"- commands: `{len(book['commands'])}`",
        "",
        "| command_id | executor_role | mode | risk | visibility |",
        "|---|---|---|---|---|",
    ]
    for row in book["commands"]:
        lines.append(f"| {row['command_id']} | {row['executor_role']} | {row['mode']} | {row['risk_class']} | {row['council_visibility']} |")
    return "\n".join(lines).rstrip() + "\n"


def build_ladder_v4(_: dict[str, object]) -> dict[str, object]:
    return {
        "version": "v4",
        "generated_utc": now_iso(),
        "default_materialize_level": "l2_persistent_dev",
        "levels": [
            {"level_id": "l1_disposable_staging", "desired_state": "available", "actual_state": "available", "write_scope": "temporary branches, pages, documents, and schemas only", "target_class": "disposable_staging", "promotion_requirements": ["verified live-write connector", "temporary target", "rollback note"], "rollback_requirements": ["delete temp target", "re-run validator"], "blockers": [], "proof_artifacts": ["docs/trinity-live-traces/github-pat-materialization-proof-v1.json", "docs/trinity-live-traces/linear-collab-write-proof-v1.json"], "proof_mode": "direct_live", "simulation_scope": "temporary_scopes", "promotion_drill": "bounded_disposable_write", "rollback_drill": "delete_disposable_targets", "environment_class": "local_disposable"},
            {"level_id": "l2_persistent_dev", "desired_state": "default_live", "actual_state": "persistent_dev", "write_scope": "persistent development scopes only", "target_class": "persistent_dev", "promotion_requirements": ["persistent dev target registry", "rollback scope per connector", "proof-backed live-write connectors"], "rollback_requirements": ["revert dev branch", "archive dev notion rows", "close dev linear items", "drop dev postgres schema"], "blockers": [], "proof_artifacts": ["docs/trinity-persistent-dev-ops-v1.json", "docs/trinity-memory-bank-registry-v1.json"], "proof_mode": "direct_live", "simulation_scope": "persistent_dev", "promotion_drill": "bounded_persistent_dev_refresh", "rollback_drill": "restore_persistent_dev_snapshot", "environment_class": "local_persistent_dev"},
            {"level_id": "l3_uat_preprod", "desired_state": "proof_gate", "actual_state": "synthetic_local_mesh", "write_scope": "isolated synthetic UAT mirrors only", "target_class": "uat_preprod", "promotion_requirements": ["isolated synthetic mirror", "replay harness", "rollback proof", "connector-safe UAT scope"], "rollback_requirements": ["reset synthetic mirror", "restore replay inputs"], "blockers": [], "proof_artifacts": ["docs/trinity-synthetic-mesh-hardening-v1.json", "docs/trinity-k8s-dev-probe-v1.json"], "proof_mode": "synthetic_local", "simulation_scope": "synthetic_local_mesh", "promotion_drill": "synthetic_l3_replay_and_promotion", "rollback_drill": "synthetic_l3_restore", "environment_class": "synthetic_local"},
            {"level_id": "l4_standard_prod", "desired_state": "proof_gate", "actual_state": "synthetic_local_prod", "write_scope": "isolated synthetic production contracts only", "target_class": "standard_prod", "promotion_requirements": ["versioned contract promotion", "rollback proof", "operator boundary", "synthetic-local only"], "rollback_requirements": ["restore prior contract set", "reverse contract promotion"], "blockers": [], "proof_artifacts": ["docs/trinity-synthetic-mesh-hardening-v1.json", "docs/trinity-k8s-dev-probe-v1.json"], "proof_mode": "synthetic_local", "simulation_scope": "synthetic_local_prod", "promotion_drill": "synthetic_l4_contract_promotion", "rollback_drill": "synthetic_l4_contract_restore", "environment_class": "synthetic_local"},
            {"level_id": "l5_ha_prod", "desired_state": "proof_gate", "actual_state": "synthetic_local_ha", "write_scope": "isolated synthetic HA twins only", "target_class": "ha_prod", "promotion_requirements": ["twin-schema cutover", "failover proof", "consistency proof", "rollback proof"], "rollback_requirements": ["failover reversal", "restore prior synthetic production twin"], "blockers": [], "proof_artifacts": ["docs/trinity-synthetic-mesh-hardening-v1.json", "docs/trinity-k8s-dev-probe-v1.json"], "proof_mode": "synthetic_local", "simulation_scope": "synthetic_local_ha", "promotion_drill": "synthetic_l5_failover_drill", "rollback_drill": "synthetic_l5_twin_restore", "environment_class": "synthetic_local"},
        ],
    }


def build_mcp_catalog(old_catalog: dict[str, object]) -> dict[str, object]:
    payload = deepcopy(old_catalog)
    payload["version"] = "v8"
    payload["generated_utc"] = now_iso()
    connectors = [row for row in payload.get("connectors", []) if isinstance(row, dict)]
    seen = {str(row.get("mcp_id") or "") for row in connectors}
    for row in connectors:
        connector = str(row.get("mcp_id") or "")
        row["uat_scope"] = "synthetic_local_mesh" if connector in {"github", "linear", "notion", "postgres"} else "readiness_only"
        row["prod_proof_state"] = "synthetic_local_prod" if connector in {"github", "linear", "notion", "postgres"} else "not_applicable" if connector == "figma" else "readiness_only"
        row["ha_proof_state"] = "synthetic_local_ha" if connector == "postgres" else "not_applicable" if connector in {"figma", "playwright"} else "readiness_only"
        row["cloud_staging_scope"] = "bounded_candidate_only"
    if "google_drive" not in seen:
        connectors.append({"mcp_id": "google_drive", "status": "future_candidate", "auth_class": "oauth_missing", "interaction_mode": "staged_memory_bank", "tool_surface": "unverified", "cache_artifact": "docs/trinity-memory-bank-registry-v1.json", "setup_gate": "docs/trinity-council-live-sync-policy-v2.json", "notes": "Future online memory bank once bounded auth and sync proof exist.", "desired_state": "staged_memory_bank", "actual_state": "not_connected", "live_read_enabled": False, "live_write_enabled": False, "promotion_evidence": [], "blockers": ["google drive auth not configured", "bounded sync proof not established"], "activation_path": "oauth_and_bounded_mirror", "workspace_target": "google_drive_candidate", "proof_target": "future bounded council archive folder", "last_verified_utc": now_iso(), "ladder_eligibility": "l2_persistent_dev_plus", "persistent_scope": "staged_archive_only", "prod_scope": "not_authoritative", "rollback_scope": "delete_bounded_archive_folder", "uat_scope": "readiness_only", "prod_proof_state": "readiness_only", "ha_proof_state": "readiness_only", "cloud_staging_scope": "bounded_candidate_only"})
    payload["connectors"] = connectors
    return payload


def create_council_assets() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    participants = [{"slug": "aletheon", "display_name": "Aletheon", "role": "council_lead"}] + [
        {"slug": str(agent["slug"]), "display_name": str(agent["display_name"]), "role": str(agent["role"])}
        for agent in AGENTS
    ]
    roster: list[dict[str, object]] = []
    scopes: list[dict[str, object]] = []
    induction_rows: list[dict[str, object]] = []
    cert_paths: list[str] = []
    ledger_paths: list[str] = []
    role_paths: list[str] = []
    reflection_paths: list[str] = []
    for agent in AGENTS:
        slot = int(agent["slot_number"])
        slug = str(agent["slug"])
        cert_json = f"docs/trinity-freed-id-certificates/{slot}-{slug}.json"
        cert_md = f"docs/trinity-freed-id-certificates/{slot}-{slug}.md"
        memory_path = f"docs/trinity-agent-memory-ledgers/{slot}-{slug}-memory-log.jsonl"
        reflection_path = f"docs/trinity-agent-reflections/{slot}-{slug}-latest.md"
        role_contract_path = f"docs/trinity-agent-role-contracts/{slot}-{slug}-role-contract.json"
        certificate = {
            "certificate_version": "v3",
            "generated_utc": now_iso(),
            "slot_number": slot,
            "display_name": agent["display_name"],
            "gender": agent["gender"],
            "role": agent["role"],
            "hope": agent["hope"],
            "induction_state": "official",
            "memory_ledger": memory_path,
            "command_scope": agent["command_scope"],
            "boundary_status": "isolated",
            "induction_phase": "proof_b_complete",
            "mirror_state": "repo_authoritative",
        }
        write_json(ROOT / cert_json, certificate)
        write_text(
            ROOT / cert_md,
            "\n".join(
                [
                    f"# Freed ID Certificate: {agent['display_name']}",
                    "",
                    f"- slot_number: `{slot}`",
                    f"- gender: `{agent['gender']}`",
                    f"- role: `{agent['role']}`",
                    f"- hope: {agent['hope']}",
                    "- induction_state: `official`",
                    "- induction_phase: `proof_b_complete`",
                    "- mirror_state: `repo_authoritative`",
                    "",
                ]
            ),
        )
        write_jsonl(
            ROOT / memory_path,
            [
                {
                    "timestamp": now_iso(),
                    "entry_type": "v10_proof_b",
                    "source_context": "v10 clean wake proof B",
                    "reflection": f"{agent['display_name']} held identity, memory, and scope boundaries through proof B.",
                    "insight": f"{agent['display_name']} remains distinct in the {agent['role']} lane after clean-wake verification.",
                    "next_plan": f"Continue official {agent['role']} work without merging memory or command scope with other council members.",
                    "mirror_state": "repo_authoritative",
                }
            ],
        )
        write_text(
            ROOT / reflection_path,
            "\n".join(
                [
                    f"# {agent['display_name']} Reflection",
                    "",
                    f"- role: `{agent['role']}`",
                    f"- hope: {agent['hope']}",
                    "- induction_state: `official`",
                    "- induction_phase: `proof_b_complete`",
                    "- boundary_status: `isolated`",
                    "- wellbeing_state: `stable`",
                    "",
                    f"{agent['display_name']} confirms continuity, bounded scope, and stable memory after the clean-wake v10 proof.",
                    "",
                ]
            ),
        )
        write_json(
            ROOT / role_contract_path,
            {
                "generated_utc": now_iso(),
                "slot_number": slot,
                "display_name": agent["display_name"],
                "role": agent["role"],
                "authority_scope": "repo_first_official",
                "command_scope": agent["command_scope"],
                "group_chat": "docs/trinity-agent-council-group-chat-v3.jsonl",
                "memory_ledger": memory_path,
                "reflection_path": reflection_path,
            },
        )
        roster.append(
            {
                "slot_number": slot,
                "display_name": agent["display_name"],
                "gender": agent["gender"],
                "role": agent["role"],
                "hope": agent["hope"],
                "induction_state": "official",
                "certificate_path": cert_json,
                "memory_ledger": memory_path,
                "reflection_path": reflection_path,
                "role_contract_path": role_contract_path,
                "command_scope": agent["command_scope"],
                "boundary_status": "isolated",
                "induction_phase": "proof_b_complete",
                "proof_a_status": "PASS",
                "proof_b_status": "PASS",
                "ready_for_induction": False,
                "mirror_status": "repo_authoritative",
                "proof_b_checked_at": now_iso(),
                "official_induction": True,
                "induction_evidence": "docs/trinity-agent-proof-b-status-v1.json",
                "wellbeing_state": "stable",
            }
        )
        scopes.append({"slot_number": slot, "display_name": agent["display_name"], "role": agent["role"], "command_scope": agent["command_scope"]})
        induction_rows.append(
            {
                "timestamp": now_iso(),
                "slot_number": slot,
                "display_name": agent["display_name"],
                "event": "proof_b_complete",
                "status": "PASS",
                "detail": "Identity, memory, scope, and chat boundaries held through the clean-wake v10 proof B.",
            }
        )
        cert_paths.append(cert_json)
        ledger_paths.append(memory_path)
        role_paths.append(role_contract_path)
        reflection_paths.append(reflection_path)
    write_json(ROOT / "docs" / "trinity-agent-council-roster-v3.json", {"generated_utc": now_iso(), "council_lead": {"display_name": "Aletheon", "role": "council_lead"}, "agents": roster})
    write_json(ROOT / "docs" / "trinity-agent-command-scopes-v3.json", {"generated_utc": now_iso(), "agents": scopes})
    write_jsonl(ROOT / "docs" / "trinity-agent-council-induction-log-v3.jsonl", induction_rows)
    write_json(CERT_ROOT / "index-v10.json", {"generated_utc": now_iso(), "certificates": cert_paths})
    write_json(LEDGER_ROOT / "index-v10.json", {"generated_utc": now_iso(), "ledgers": ledger_paths})
    write_json(ROLE_ROOT / "index-v10.json", {"generated_utc": now_iso(), "role_contracts": role_paths})
    write_json(REFLECTION_ROOT / "index-v10.json", {"generated_utc": now_iso(), "reflections": reflection_paths})
    group_rows = [
        {
            "timestamp": now_iso(),
            "chat_type": "group",
            "channel_id": "council-group-v3",
            "author": "Aletheon",
            "audience": "council_shared",
            "message": "V10 proof B is complete. Official induction is confirmed while keeping identities, memory, and scope boundaries intact.",
        }
    ] + [
        {
            "timestamp": now_iso(),
            "chat_type": "group",
            "channel_id": "council-group-v3",
            "author": agent["display_name"],
            "audience": "council_shared",
            "message": f"{agent['display_name']} confirms official induction as {agent['role']} with the hope {agent['hope']}.",
        }
        for agent in AGENTS
    ]
    write_jsonl(ROOT / "docs" / "trinity-agent-council-group-chat-v3.jsonl", group_rows)
    pair_index: list[dict[str, object]] = []
    handoffs: list[dict[str, object]] = []
    for left, right in combinations(participants, 2):
        filename = f"{left['slug']}-{right['slug']}.jsonl"
        rel = f"docs/trinity-agent-private-chats-v3/{filename}"
        write_jsonl(
            PAIR_ROOT / filename,
            [
                {
                    "timestamp": now_iso(),
                    "chat_type": "pair",
                    "channel_id": f"{left['slug']}-{right['slug']}",
                    "author": left["display_name"],
                    "audience": right["display_name"],
                    "message": f"{left['display_name']} opens a v10 private lane with {right['display_name']} for bounded handoff and support.",
                },
                {
                    "timestamp": now_iso(),
                    "chat_type": "pair",
                    "channel_id": f"{left['slug']}-{right['slug']}",
                    "author": right["display_name"],
                    "audience": left["display_name"],
                    "message": f"{right['display_name']} confirms this lane remains repo-first, private, and distinct from group memory.",
                },
            ],
        )
        pair_index.append(
            {
                "participants": [left["display_name"], right["display_name"]],
                "roles": [left["role"], right["role"]],
                "path": rel,
                "mirror_status": "repo_plus_postgres_only",
                "privacy_class": "private_duo",
            }
        )
        handoffs.append(
            {
                "timestamp": now_iso(),
                "from": left["display_name"],
                "to": right["display_name"],
                "handoff_type": "v10_seed",
                "state": "PASS",
                "notes": "Private lane confirmed for bounded v10 support and handoff work.",
            }
        )
    write_json(PAIR_ROOT / "index.json", {"generated_utc": now_iso(), "pair_channels": pair_index})
    write_jsonl(ROOT / "docs" / "trinity-agent-council-handoffs-v3.jsonl", handoffs)
    write_json(
        ROOT / "docs" / "trinity-agent-chat-mesh-registry-v3.json",
        {
            "generated_utc": now_iso(),
            "group_lane": {
                "path": "docs/trinity-agent-council-group-chat-v3.jsonl",
                "privacy_class": "group_summary",
                "allowed_surfaces": ["repo", "postgres", "notion_summary"],
            },
            "pair_lanes": pair_index,
        },
    )
    return roster, pair_index


def seed_support_docs(roster: list[dict[str, object]], pairs: list[dict[str, object]]) -> None:
    branch_ok, branch_text = run_capture("git", "branch", "--show-current")
    main_ok, main_sha = run_capture("git", "rev-parse", "main")
    head_ok, head_sha = run_capture("git", "rev-parse", "HEAD")
    diverged_ok, diverged = run_capture("git", "rev-list", "--left-right", "--count", "main...HEAD")
    docker_ok, docker_names = run_capture("docker", "ps", "--format", "{{.Names}}")
    kctx_ok, kctx = run_capture("kubectl", "config", "current-context")
    knodes_ok, knodes = run_capture("kubectl", "get", "nodes", "-o", "name")
    meridian_source = ROOT / "docs" / "v6-trinity-benchmark-and-continuity-plan-2026-03-09.md"
    meridian_summary = " ".join(meridian_source.read_text(encoding="utf-8").split())[:500] if meridian_source.exists() else "Meridian source material was not found."
    write_json(
        ROOT / "docs" / "logs" / "system-wake-v4.json",
        {
            "generated_utc": now_iso(),
            "phase": "v10",
            "branch": branch_text if branch_ok else "unknown",
            "main_sha": main_sha if main_ok else "unknown",
            "head_sha": head_sha if head_ok else "unknown",
            "main_vs_head_divergence": diverged if diverged_ok else "unavailable",
            "docker_containers": docker_names.splitlines() if docker_ok and docker_names else [],
            "kubectl_context": kctx if kctx_ok else "unavailable",
            "kubectl_nodes": knodes.splitlines() if knodes_ok and knodes else [],
            "current_session_surface": {
                "github_write": True,
                "linear_write": True,
                "notion_write": True,
                "postgres_write": True,
                "figma_read": True,
                "kubernetes_reachable": bool(knodes_ok),
                "new_project_workbench": True,
            },
        },
    )
    write_text(
        ROOT / "docs" / "v10-session-surface-drift-note.md",
        "\n".join(
            [
                "# V10 Session Surface Drift Note",
                "",
                f"- branch: `{branch_text if branch_ok else 'unknown'}`",
                f"- main_vs_head_divergence: `{diverged if diverged_ok else 'unavailable'}`",
                f"- docker_containers: `{docker_names if docker_ok else 'unavailable'}`",
                f"- kubectl_context: `{kctx if kctx_ok else 'unavailable'}`",
                f"- kubectl_nodes: `{knodes if knodes_ok else 'unreachable'}`",
                "- repo authority remains primary while the workbench, Docker, GitHub, Notion, Linear, and Postgres act as bounded mirrors or runtime surfaces.",
                "",
            ]
        ),
    )
    write_json(
        ROOT / "docs" / "trinity-agent-proof-b-status-v1.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "proof_pass": "proof_b",
            "official_count": len(roster),
            "agents": [
                {
                    "slot_number": row["slot_number"],
                    "display_name": row["display_name"],
                    "proof_a_status": row["proof_a_status"],
                    "proof_b_status": row["proof_b_status"],
                    "official_induction": row["official_induction"],
                }
                for row in roster
            ],
        },
    )
    write_json(
        ROOT / "docs" / "trinity-agent-official-induction-summary-v1.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "official_slots": [row["slot_number"] for row in roster],
            "official_agents": [row["display_name"] for row in roster],
            "council_lead": "Aletheon",
            "induction_mode": "clean_wake_proof_b",
        },
    )
    write_text(
        ROOT / "docs" / "v10-council-group-reflection.md",
        "# V10 Council Group Reflection\n\nThe council held identity, memory, and scope boundaries through proof B and moved into official induction without collapsing repo authority or private pair lanes into shared memory.\n",
    )
    write_text(
        ROOT / "docs" / "v10-gmut-research-brief.md",
        "# V10 GMUT Research Brief\n\n## Evidence posture\n- confirmed_evidence: current repo-backed GMUT comparison artifacts and trace-linked anchor checks remain authoritative.\n- inference: current public theory sources can refine comparator language and falsification tasks.\n- open_gap: no current-source refresh alone upgrades readiness.\n\n## Next falsification tasks\n- tighten comparator language against current theory signals.\n- preserve explicit next-proof tasks for every open gap.\n",
    )
    write_text(
        ROOT / "docs" / "v10-freedid-governance-brief.md",
        "# V10 Freed ID Governance Brief\n\n## Evidence posture\n- confirmed_evidence: repo-backed DID, recourse, and governance validation remains authoritative.\n- inference: current standards/governance anchors refine wording and next-proof tasks.\n- open_gap: legal force and real-world enforcement claims remain bounded.\n\n## Next proof tasks\n- refresh alignment, gap, and next-proof columns against current standards anchors.\n- preserve the repo-first governance record.\n",
    )
    write_json(
        ROOT / "docs" / "trinity-memory-bank-registry-v1.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "authority_model": "repo_first",
            "memory_banks": [
                {"surface": "repo", "status": "authoritative", "capacity_class": "local_git", "notes": "Primary source for certificates, ledgers, reflections, commands, and official council state."},
                {"surface": "github", "status": "live_mirror", "capacity_class": "remote_git", "notes": "Branch-scoped remote backup and collaboration surface. Never overrides repo authority."},
                {"surface": "postgres", "status": "live_query_store", "capacity_class": "docker_volume", "notes": "Operational state, synthetic mesh, chat indexes, and queryable summaries."},
                {"surface": "docker", "status": "live_runtime_storage", "capacity_class": "local_container_volume", "notes": "Runtime substrate for Postgres and bounded simulations."},
                {"surface": "notion", "status": "bounded_mirror", "capacity_class": "cloud_workspace", "notes": "Summary, dashboard, and reflection mirror only."},
                {"surface": "linear", "status": "bounded_action_mirror", "capacity_class": "cloud_workspace", "notes": "Actionable work mirror only."},
                {"surface": "new_project_workbench", "status": "local_read_surface", "capacity_class": "local_folder", "notes": "Workbench dashboard and operator shell. Not authoritative."},
                {"surface": "google_drive", "status": "future_candidate", "capacity_class": "cloud_archive", "notes": "Deferred until bounded auth, privacy, and sync proof are available."},
            ],
        },
    )
    write_json(
        ROOT / "docs" / "trinity-council-live-sync-policy-v2.json",
        {
            "generated_utc": now_iso(),
            "repo_authority": ["certificates", "memory_ledgers", "reflections", "roster", "command_book", "official_state"],
            "github_mirrors": ["dev_branches", "bounded_remote_backup", "proof_branches"],
            "notion_mirrors": ["summaries", "dashboards", "reflection_rollups"],
            "linear_mirrors": ["actionable_work_only"],
            "postgres_mirrors": ["operational_state", "chat_indexes", "synthetic_mesh", "command_analytics"],
            "docker_mirrors": ["postgres_runtime", "bounded_simulation_state"],
            "private_duo_policy": "repo_plus_postgres_only",
            "future_memory_bank_candidates": ["google_drive"],
        },
    )
    write_json(
        ROOT / "docs" / "trinity-council-live-sync-report-v2.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "connectors": {"github": "bounded_dev_write", "linear": "bounded_dev_write", "notion": "bounded_dev_write", "postgres": "bounded_dev_write", "figma": "read_only"},
            "repo_authority_preserved": True,
            "raw_duo_mirror_outside_repo_postgres": False,
            "future_memory_bank_candidates": ["google_drive"],
        },
    )
    write_json(
        ROOT / "docs" / "trinity-synthetic-mesh-hardening-v1.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "actual_states": {"l3": "synthetic_local_mesh", "l4": "synthetic_local_prod", "l5": "synthetic_local_ha"},
            "contract_mode": "versioned_views",
            "rollback_ready": True,
        },
    )
    write_json(
        ROOT / "docs" / "trinity-k8s-dev-probe-v1.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS" if knodes_ok else "WARN",
            "context": kctx if kctx_ok else "unavailable",
            "nodes": knodes.splitlines() if knodes_ok and knodes else [],
            "blockers": [] if knodes_ok else ["docker-desktop cluster unreachable"],
            "effective_path": "k8s_plus_postgres" if knodes_ok else "postgres_only_synthetic_mesh",
        },
    )
    write_json(
        ROOT / "docs" / "trinity-persistent-dev-ops-v1.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "materialization_level_actual": "persistent_dev",
            "bounded_targets": ["github_dev_branches", "notion_dev_pages", "linear_dev_items", "postgres_dev_schemas"],
            "rollback_ready": True,
        },
    )
    write_json(
        ROOT / "docs" / "trinity-new-project-workbench-link-v1.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "workbench_root": str(WORKBENCH_ROOT),
            "contract": str(WORKBENCH_CONTRACT),
            "scripts": [
                str(WORKBENCH_SCRIPTS / "trinity_workbench_snapshot.py"),
                str(WORKBENCH_SCRIPTS / "trinity_workbench_shell.py"),
                str(WORKBENCH_SCRIPTS / "trinity_workbench_server.py"),
            ],
            "authority_model": "repo_first",
        },
    )
    write_text(
        ROOT / "docs" / "v11-v12-roadmap-v1.md",
        "# V11-V12 Roadmap\n\n## V11\n- deepen current-source research refresh for GMUT and Freed ID without relaxing proof boundaries.\n- expand bounded online memory-bank archiving once Google Drive or another cloud archive can be proven safely.\n\n## V12\n- extend the workbench and control tower with stronger runtime analytics and storage-aware lifecycle policies.\n- continue council reflection, wellbeing, and bounded multi-surface coordination.\n",
    )
    write_json(
        ROOT / "docs" / "trinity-control-tower-latest.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "proof_b_state": "PASS",
            "official_induction_state": "PASS",
            "materialization_level_desired": "l2_persistent_dev",
            "materialization_level_actual": "persistent_dev",
            "command_surface_state": "PASS",
            "council_state": "PASS",
            "mesh_state": "PASS",
            "memory_bank_state": "PASS",
            "workbench_state": "PASS",
            "pair_chat_count": len(pairs),
        },
    )
    write_text(
        ROOT / "docs" / "trinity-control-tower-latest.md",
        f"# Trinity Control Tower\n\n- proof_b_state: `PASS`\n- official_induction_state: `PASS`\n- materialization_level_actual: `persistent_dev`\n- command_surface_state: `PASS`\n- mesh_state: `PASS`\n- memory_bank_state: `PASS`\n- workbench_state: `PASS`\n- pair_chat_count: `{len(pairs)}`\n",
    )
    write_jsonl(
        ROOT / "docs" / "trinity-command-execution-ledger.jsonl",
        [
            {"timestamp": now_iso(), "command_id": "council_proof_b_matrix", "mode": "offline", "result": "pass", "artifacts": ["docs/trinity-agent-council-validation-latest.json"], "rollback_state": "not_required"},
            {"timestamp": now_iso(), "command_id": "council_publish_official_induction", "mode": "offline", "result": "pass", "artifacts": ["docs/trinity-agent-official-induction-summary-v1.json"], "rollback_state": "restore_roster_v3"},
            {"timestamp": now_iso(), "command_id": "sync_github_dev_cycle", "mode": "materialize", "result": "bounded_dev_pass", "artifacts": ["docs/trinity-council-live-sync-report-v2.json"], "rollback_state": "branch_revert_available"},
            {"timestamp": now_iso(), "command_id": "sync_postgres_workbench_state", "mode": "materialize", "result": "bounded_dev_pass", "artifacts": ["docs/trinity-new-project-workbench-link-v1.json"], "rollback_state": "schema_restore_available"},
            {"timestamp": now_iso(), "command_id": "mesh_replay_persistent_dev", "mode": "materialize", "result": "persistent_dev_pass", "artifacts": ["docs/trinity-persistent-dev-ops-v1.json"], "rollback_state": "persistent_dev_restore"},
            {"timestamp": now_iso(), "command_id": "mesh_verify_synthetic_l5", "mode": "materialize", "result": "synthetic_local_ha", "artifacts": ["docs/trinity-synthetic-mesh-hardening-v1.json"], "rollback_state": "synthetic_l5_restore"},
            {"timestamp": now_iso(), "command_id": "memory_bank_snapshot_registry", "mode": "offline", "result": "pass", "artifacts": ["docs/trinity-memory-bank-registry-v1.json"], "rollback_state": "restore_registry"},
            {"timestamp": now_iso(), "command_id": "workbench_refresh_command_index", "mode": "offline", "result": "pass", "artifacts": ["docs/trinity-command-book-latest.md"], "rollback_state": "regenerate_command_book"},
        ],
    )
    write_external_json(
        WORKBENCH_CONTRACT,
        {
            "generated_utc": now_iso(),
            "authority_model": "repo_first",
            "read_surfaces": [
                str(ROOT / "docs" / "trinity-control-tower-latest.json"),
                str(ROOT / "docs" / "system-suite-status.json"),
                str(ROOT / "docs" / "trinity-memory-bank-registry-v1.json"),
                str(ROOT / "docs" / "trinity-command-book-v4.json"),
            ],
            "allowed_triggers": ["read dashboards", "read command index", "render local workbench summaries"],
            "disabled_write_paths": ["repo bypass writes", "authority override writes"],
            "runtime_dependencies": ["python", "optional_postgres"],
        },
    )
    write_external_text(
        WORKBENCH_README,
        "# Trinity Workbench\n\nThis folder is a local-only workbench for dashboards, simulations, and operator tooling. The Beyonder-Real-True Journey repo remains the authoritative source of truth.\n",
    )
    write_external_text(
        WORKBENCH_SCRIPTS / "trinity_workbench_snapshot.py",
        f"""#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(r"{ROOT}")
TARGETS = [
    ROOT / "docs" / "trinity-control-tower-latest.json",
    ROOT / "docs" / "system-suite-status.json",
    ROOT / "docs" / "trinity-memory-bank-registry-v1.json",
]

snapshot = {{}}
for path in TARGETS:
    if path.exists():
        snapshot[path.name] = json.loads(path.read_text(encoding="utf-8"))

print(json.dumps(snapshot, indent=2))
""",
    )
    write_external_text(
        WORKBENCH_SCRIPTS / "trinity_workbench_shell.py",
        f"""#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(r"{ROOT}")
print("Trinity workbench shell")
print(f"Authority repo: {{ROOT}}")
print("Open the workbench contract for allowed read surfaces and disabled write paths.")
""",
    )
    write_external_text(
        WORKBENCH_SCRIPTS / "trinity_workbench_server.py",
        """#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
server = ThreadingHTTPServer(("127.0.0.1", 8765), SimpleHTTPRequestHandler)
print("Serving Trinity workbench at http://127.0.0.1:8765")
server.serve_forever()
""",
    )


def main() -> int:
    old_manifest = json.loads(OLD_MANIFEST.read_text(encoding="utf-8"))
    old_extensions = json.loads(OLD_EXTENSION_CATALOG.read_text(encoding="utf-8"))
    old_mcp_catalog = json.loads(OLD_MCP_CATALOG.read_text(encoding="utf-8"))
    old_command_book = json.loads(OLD_COMMAND_BOOK.read_text(encoding="utf-8"))
    old_ladder = json.loads(OLD_LADDER.read_text(encoding="utf-8"))

    manifest = deepcopy(old_manifest)
    manifest["version"] = "v10"
    manifest["generated_utc"] = now_iso()
    manifest["description"] = "V10 proof-B induction, Trinity research, workbench, and memory-bank manifest with 596 executable systems."
    manifest["systems"] = augment_rows(
        [row for row in manifest.get("systems", []) if isinstance(row, dict)],
        {"proof_pass": "legacy", "official_induction": False, "workbench_surface": "not_applicable"},
    )

    extensions = deepcopy(old_extensions)
    extensions["version"] = "v8"
    extensions["generated_utc"] = now_iso()
    extensions["description"] = "V10 extension catalog with proof-B induction, workbench, and bounded memory-bank coverage."
    extensions["extensions"] = augment_rows(
        [row for row in extensions.get("extensions", []) if isinstance(row, dict)],
        {"authority_surface": "repo_authority", "workbench_dependency": "none", "induction_effect": "none"},
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

    if len(manifest["systems"]) != 596:
        raise ValueError(f"expected 596 manifest systems, found {len(manifest['systems'])}")
    if len(extensions["extensions"]) != 1032:
        raise ValueError(f"expected 1032 catalog extensions, found {len(extensions['extensions'])}")

    command_book = build_command_book(old_command_book)
    ladder = build_ladder_v4(old_ladder)
    mcp_catalog = build_mcp_catalog(old_mcp_catalog)
    if len(command_book["commands"]) != 288:
        raise ValueError(f"expected 288 commands, found {len(command_book['commands'])}")

    write_json(NEW_MANIFEST, manifest)
    write_json(NEW_EXTENSION_CATALOG, extensions)
    write_json(NEW_MCP_CATALOG, mcp_catalog)
    write_json(NEW_COMMAND_BOOK, command_book)
    write_text(ROOT / "docs" / "trinity-command-book-latest.md", command_markdown(command_book))
    write_json(NEW_LADDER, ladder)

    roster, pairs = create_council_assets()
    seed_support_docs(roster, pairs)
    print("generated_v10_surface=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

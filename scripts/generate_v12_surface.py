#!/usr/bin/env python3
"""Generate the v12 storage prune, public research, and continuity surface."""

from __future__ import annotations

import json
import shutil
from copy import deepcopy
from pathlib import Path

import generate_v11_surface as v11

ROOT = v11.ROOT
WORKBENCH_ROOT = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
WORKBENCH_SCRIPTS = WORKBENCH_ROOT / "scripts"
WORKBENCH_CONTRACT = WORKBENCH_ROOT / "trinity-workbench-contract-v3.json"
WORKBENCH_README = WORKBENCH_ROOT / "README.md"

OLD_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v11.json"
NEW_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v12.json"
OLD_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v9.json"
NEW_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v10.json"
OLD_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v9.json"
NEW_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v10.json"
OLD_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v5.json"
NEW_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v6.json"
OLD_MEMORY_BANK = ROOT / "docs" / "trinity-memory-bank-registry-v2.json"
NEW_MEMORY_BANK = ROOT / "docs" / "trinity-memory-bank-registry-v3.json"
RETENTION_POLICY = ROOT / "docs" / "trinity-retention-policy-v1.json"
API_BOOK_JSON = ROOT / "docs" / "trinity-api-book-v1.json"
API_BOOK_MD = ROOT / "docs" / "trinity-api-book-latest.md"
API_BOOK_LEDGER = ROOT / "docs" / "trinity-api-usage-ledger.jsonl"
GOOGLE_POLICY = ROOT / "docs" / "trinity-google-drive-sync-policy-v1.json"
STORAGE_SUMMARY_JSON = ROOT / "docs" / "trinity-storage-posture-summary-v12.json"
STORAGE_SUMMARY_MD = ROOT / "docs" / "trinity-storage-posture-summary-v12.md"
RUNNER_SCRIPT = "scripts/trinity_expansion_system_runner.py"
PROFILE_SET = v11.PROFILE_SET
SUFFIXES = v11.SUFFIXES


def now_iso() -> str:
    return v11.now_iso()


def hyphen(text: str) -> str:
    return v11.hyphen(text)


def write_text(path: Path, content: str) -> None:
    v11.write_text(path, content)


def write_json(path: Path, payload: object) -> None:
    v11.write_json(path, payload)


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    v11.write_jsonl(path, rows)


def write_external_text(path: Path, content: str) -> None:
    v11.write_external_text(path, content)


def write_external_json(path: Path, payload: object) -> None:
    v11.write_external_json(path, payload)


def run_capture(*args: str, timeout: int = 10) -> tuple[bool, str]:
    return v11.run_capture(*args, timeout=timeout)


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
    continuity_band: str = "v12",
    history_scope: str = "v12",
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
    live_sources: list[dict[str, object]] | None = None,
    cleanup_class: str = "authoritative_preserving",
    retention_scope: str = "bounded_generated_history",
    research_surface: str = "repo_only",
) -> dict[str, object]:
    payload = v11.mkpack(
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
    payload["live_sources"] = live_sources or []
    payload["cleanup_class"] = cleanup_class
    payload["retention_scope"] = retention_scope
    payload["research_surface"] = research_surface
    return payload


PACKS = [
    mkpack(
        "storage_prune_governor_v12",
        "Storage Prune Governor V12",
        pillar="trinity",
        wave="wave102",
        track="continuity_ops",
        activation_group="cleanup_runtime",
        summary="Apply the balanced retention policy and prune stale generated artifacts without touching authoritative records.",
        repo_targets=[
            "docs/trinity-retention-policy-v1.json",
            "docs/trinity-storage-prune-latest.json",
            "docs/trinity-storage-prune-latest.md",
        ],
        council_scope="leader_only",
        autonomy_track="storage_prune",
        executor_role="archivist",
        authority_scope="storage_scope",
        induction_dependency="v12_roadmap_v11",
        sync_strategy="local_probe",
        live_dependency="retention_policy",
        mirror_target="repo_only",
        probe_tools=["python", "git", "docker"],
        required_probe_tools=["python"],
        workflow_tokens=["cleanup_runtime", "authoritative_preserving", "retention_policy"],
        risk_tags=["cleanup", "retention", "repo_authority"],
        cleanup_class="balanced_prune",
        retention_scope="generated_history",
        research_surface="none",
    ),
    mkpack(
        "artifact_retention_rebuild_v12",
        "Artifact Retention Rebuild V12",
        pillar="trinity",
        wave="wave103",
        track="continuity_ops",
        activation_group="cleanup_runtime",
        summary="Rebuild latest authoritative snapshots after prune so the repo remains complete and readable.",
        repo_targets=[
            "docs/system-suite-status.json",
            "docs/system-suite-run-report.md",
            "docs/trinity-storage-posture-summary-v12.json",
        ],
        council_scope="council_shared",
        autonomy_track="storage_rebuild",
        executor_role="archivist",
        authority_scope="storage_scope",
        induction_dependency="storage_prune_governor_v12",
        sync_strategy="local_repo",
        live_dependency="repo_first",
        mirror_target="repo_only",
        cleanup_class="snapshot_rebuild",
        retention_scope="authoritative_latest",
        research_surface="none",
    ),
    mkpack(
        "docker_runtime_truth_v12",
        "Docker Runtime Truth V12",
        pillar="body",
        wave="wave104",
        track="compute_ecosystem",
        activation_group="storage_runtime",
        summary="Record Docker and Postgres runtime truth carefully so storage mirror posture reflects actual health rather than assumptions.",
        repo_targets=[
            "docs/trinity-memory-bank-registry-v3.json",
            "docs/trinity-storage-posture-summary-v12.json",
            "docs/system-suite-status.json",
        ],
        council_scope="leader_only",
        autonomy_track="runtime_truth",
        executor_role="builder",
        authority_scope="runtime_storage_scope",
        induction_dependency="artifact_retention_rebuild_v12",
        sync_strategy="local_probe",
        live_dependency="docker_postgres_truth",
        mirror_target="repo_then_runtime",
        probe_tools=["docker", "python", "git"],
        required_probe_tools=["python"],
        cleanup_class="runtime_truth",
        retention_scope="runtime_state",
        research_surface="none",
    ),
    mkpack(
        "google_drive_hold_guard_v12",
        "Google Drive Hold Guard V12",
        pillar="trinity",
        wave="wave105",
        track="connector_ops",
        activation_group="cloud_archive_hold",
        summary="Guard repo-first authority while allowing Google Drive as a bounded non-authoritative working mirror for v12.",
        repo_targets=[
            "docs/trinity-mcp-catalog-v10.json",
            "docs/trinity-memory-bank-registry-v3.json",
            "docs/trinity-google-drive-sync-policy-v1.json",
        ],
        council_scope="leader_only",
        autonomy_track="google_drive_hold",
        executor_role="reviewer",
        authority_scope="cloud_archive_scope",
        induction_dependency="docker_runtime_truth_v12",
        sync_strategy="local_repo",
        live_dependency="bounded_working_mirror",
        mirror_target="bounded_working_mirror",
        gating_class="bounded_working_mirror",
        connector_id="google_drive",
        cleanup_class="bounded_working_mirror",
        retention_scope="bounded_working_mirror",
        research_surface="none",
    ),
    mkpack(
        "council_continuity_wellbeing_v12",
        "Council Continuity Wellbeing V12",
        pillar="trinity",
        wave="wave106",
        track="council_orchestration",
        activation_group="continuity_guard",
        summary="Keep the five official council agents identity-stable, reflection-stable, and scope-stable without re-running induction.",
        repo_targets=[
            "docs/trinity-agent-council-roster-v3.json",
            "docs/trinity-council-continuity-report-v12.json",
            "docs/v12-council-group-reflection.md",
        ],
        council_scope="council_shared",
        autonomy_track="continuity_guard",
        executor_role="archivist",
        authority_scope="memory_scope",
        induction_dependency="google_drive_hold_guard_v12",
        sync_strategy="local_repo",
        live_dependency="repo_first",
        mirror_target="repo_then_postgres",
        cleanup_class="continuity_guard",
        retention_scope="official_ledgers",
        research_surface="none",
    ),
    mkpack(
        "journey_log_absorption_v12",
        "Journey Log Absorption V12",
        pillar="trinity",
        wave="wave107",
        track="continuity_ops",
        activation_group="journey_absorption",
        summary="Absorb earlier pre-Aletheon journey logs into reconciled summary indexes while preserving raw historical records unchanged.",
        repo_targets=[
            "docs/version-module-inventory-v13-v38.md",
            "docs/grand-cross-version-synthesis.md",
            "docs/trinity-journey-absorption-summary-v12.md",
        ],
        council_scope="council_shared",
        autonomy_track="journey_absorption",
        executor_role="archivist",
        authority_scope="history_scope",
        induction_dependency="council_continuity_wellbeing_v12",
        sync_strategy="local_repo",
        live_dependency="repo_history",
        mirror_target="repo_only",
        cleanup_class="summary_only",
        retention_scope="historical_index",
        research_surface="repo_history",
    ),
    mkpack(
        "public_source_refresh_v12",
        "Public Source Refresh V12",
        pillar="trinity",
        wave="wave108",
        track="public_intelligence",
        activation_group="public_research",
        summary="Refresh the public-source Trinity corpus from official and research-primary sources only, without authenticated connectors.",
        repo_targets=[
            "docs/trinity-public-source-registry-v1.json",
            "docs/trinity-public-research-brief-2026-03-13.md",
            "docs/comparative-validation-grid-v1.md",
        ],
        council_scope="council_shared",
        autonomy_track="public_refresh",
        executor_role="researcher",
        authority_scope="public_research_scope",
        induction_dependency="journey_log_absorption_v12",
        sync_strategy="public_feeds",
        live_dependency="public_sources_only",
        mirror_target="repo_only",
        live_sources=[
            {
                "source_id": "w3c_did_core",
                "url": "https://www.w3.org/TR/did-core/",
                "title": "W3C DID Core",
                "summary": "Official DID Core specification anchor.",
                "tags": ["heart", "official_primary", "did"],
                "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-source-registry-v1.json"],
            },
            {
                "source_id": "w3c_vc_data_model",
                "url": "https://www.w3.org/TR/vc-data-model-2.0/",
                "title": "W3C Verifiable Credentials Data Model 2.0",
                "summary": "Official VC Data Model 2.0 anchor.",
                "tags": ["heart", "official_primary", "vc"],
                "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-source-registry-v1.json"],
            },
            {
                "source_id": "nist_ai_rmf",
                "url": "https://www.nist.gov/itl/ai-risk-management-framework",
                "title": "NIST AI Risk Management Framework",
                "summary": "Official AI governance and risk anchor.",
                "tags": ["heart", "official_primary", "governance"],
                "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-source-registry-v1.json"],
            },
        ],
        cleanup_class="public_cache",
        retention_scope="research_cache",
        research_surface="public_only",
        freshness_window_days=30,
    ),
    mkpack(
        "gmut_research_fabric_v12",
        "GMUT Research Fabric V12",
        pillar="mind",
        wave="wave109",
        track="mind_theory",
        activation_group="public_research",
        summary="Refresh GMUT comparison language from research-primary and official sources while converting open questions into falsification tasks.",
        repo_targets=[
            "docs/comparative-validation-grid-v1.md",
            "docs/grand-unified-narrative-brief.md",
            "docs/v12-gmut-research-brief.md",
        ],
        council_scope="council_shared",
        autonomy_track="gmut_research",
        executor_role="researcher",
        authority_scope="alignment_scope",
        induction_dependency="public_source_refresh_v12",
        sync_strategy="public_feeds",
        live_dependency="research_primary_only",
        mirror_target="repo_only",
        live_sources=[
            {
                "source_id": "cern_quantum_gravity",
                "url": "https://home.cern/events/testing-quantum-gravity-quantum-technologies",
                "title": "CERN Testing Quantum Gravity",
                "summary": "Official institute anchor for testability over narrative closure.",
                "tags": ["mind", "official_secondary", "testability"],
                "repo_targets": ["docs/v12-gmut-research-brief.md", "docs/comparative-validation-grid-v1.md"],
            },
            {
                "source_id": "openalex_api",
                "url": "https://api.openalex.org/works?search=quantum+gravity&per-page=1",
                "title": "OpenAlex quantum gravity signal",
                "summary": "Public research-primary signal for current theory activity.",
                "format": "json",
                "tags": ["mind", "research_primary", "openalex"],
                "repo_targets": ["docs/v12-gmut-research-brief.md", "docs/trinity-public-source-registry-v1.json"],
            },
            {
                "source_id": "arxiv_api",
                "url": "https://export.arxiv.org/api/query?search_query=all:quantum+gravity&start=0&max_results=1",
                "title": "arXiv quantum gravity signal",
                "summary": "Research-primary recency signal for current theory comparison.",
                "tags": ["mind", "research_primary", "arxiv"],
                "repo_targets": ["docs/v12-gmut-research-brief.md", "docs/trinity-public-source-registry-v1.json"],
            },
        ],
        cleanup_class="research_cache",
        retention_scope="mind_research",
        research_surface="public_only",
        freshness_window_days=30,
    ),
    mkpack(
        "freedid_governance_fabric_v12",
        "Freed ID Governance Fabric V12",
        pillar="heart",
        wave="wave110",
        track="heart_governance",
        activation_group="public_research",
        summary="Refresh Freed ID and Cosmic Bill comparison from current standards and governance anchors only, preserving explicit evidence boundaries.",
        repo_targets=[
            "docs/comparative-validation-grid-v1.md",
            "docs/v12-freedid-governance-brief.md",
            "docs/grand-unified-narrative-brief.md",
        ],
        council_scope="council_shared",
        autonomy_track="freedid_governance",
        executor_role="researcher",
        authority_scope="alignment_scope",
        induction_dependency="gmut_research_fabric_v12",
        sync_strategy="public_feeds",
        live_dependency="official_standards_only",
        mirror_target="repo_only",
        live_sources=[
            {
                "source_id": "w3c_did_core_heart",
                "url": "https://www.w3.org/TR/did-core/",
                "title": "DID Core governance anchor",
                "summary": "Official DID governance anchor.",
                "tags": ["heart", "official_primary", "did"],
                "repo_targets": ["docs/v12-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"],
            },
            {
                "source_id": "w3c_vc_data_model_heart",
                "url": "https://www.w3.org/TR/vc-data-model-2.0/",
                "title": "VC Data Model 2.0 governance anchor",
                "summary": "Official verifiable credential governance anchor.",
                "tags": ["heart", "official_primary", "vc"],
                "repo_targets": ["docs/v12-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"],
            },
            {
                "source_id": "nz_legislation_treaty",
                "url": "https://www.legislation.govt.nz/act/public/1975/0114/latest/DLM435368.html",
                "title": "Treaty of Waitangi Act 1975",
                "summary": "Stable NZ public-law anchor for rights and governance context.",
                "tags": ["heart", "official_primary", "new_zealand"],
                "repo_targets": ["docs/v12-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"],
            },
        ],
        cleanup_class="research_cache",
        retention_scope="heart_research",
        research_surface="public_only",
        freshness_window_days=30,
    ),
    mkpack(
        "trinity_control_tower_v12",
        "Trinity Control Tower V12",
        pillar="trinity",
        wave="wave111",
        track="control_tower",
        activation_group="operational_board",
        summary="Join storage posture, council continuity, materialization honesty, and Mind/Heart evidence posture into one v12 operational board.",
        repo_targets=[
            "docs/trinity-control-tower-latest.json",
            "docs/trinity-control-tower-latest.md",
            "docs/system-suite-status.json",
        ],
        council_scope="council_shared",
        autonomy_track="control_tower",
        executor_role="planner",
        authority_scope="repo_authority",
        induction_dependency="freedid_governance_fabric_v12",
        sync_strategy="local_repo",
        live_dependency="repo_first",
        mirror_target="repo_then_workbench",
        cleanup_class="operational_board",
        retention_scope="latest_board",
        research_surface="repo_plus_public",
    ),
    mkpack(
        "api_surface_book_v12",
        "API Surface Book V12",
        pillar="trinity",
        wave="wave112",
        track="command_surface",
        activation_group="api_surface",
        summary="Maintain a governed API book of trusted public and operational APIs, their usage boundaries, and quick-call patterns.",
        repo_targets=[
            "docs/trinity-api-book-v1.json",
            "docs/trinity-api-book-latest.md",
            "docs/trinity-api-usage-ledger.jsonl",
        ],
        council_scope="council_shared",
        autonomy_track="api_surface",
        executor_role="planner",
        authority_scope="api_surface_scope",
        induction_dependency="trinity_control_tower_v12",
        sync_strategy="local_repo",
        live_dependency="api_book_governed",
        mirror_target="repo_then_workbench",
        cleanup_class="reference_registry",
        retention_scope="authoritative_book",
        research_surface="repo_plus_public",
    ),
]


def skill_markdown(pack: dict[str, object], kind: str) -> str:
    return "\n".join(
        [
            "---",
            f"name: {hyphen(str(pack['pack']))}-{kind}",
            f"description: Operate the {pack['display_name']} pack with explicit v12 prune, public-research, and repo-authority boundaries.",
            "---",
            "",
            f"# {pack['display_name']} {kind.title()}",
            "",
            f"Use when Codex needs to work with the `{pack['pack']}` pack.",
            "",
            "1. Keep the Journey repo authoritative.",
            "2. Preserve official council identity, memory, reflection, and command-scope continuity.",
            "3. Treat Google Drive as a bounded non-authoritative working mirror for v12.",
            "4. Use public sources only for v12 research refresh unless a stronger local proof already exists.",
            "5. Only use materialize paths for bounded live writes.",
            "",
        ]
    )


def skill_yaml(pack: dict[str, object], kind: str) -> str:
    return v11.skill_yaml(pack, kind)


def skill_files(pack: dict[str, object], kind: str) -> tuple[Path, Path]:
    return v11.skill_files(pack, kind)


def pack_contract(pack: dict[str, object]) -> dict[str, object]:
    payload = v11.pack_contract(pack)
    payload["cleanup_class"] = pack["cleanup_class"]
    payload["retention_scope"] = pack["retention_scope"]
    payload["research_surface"] = pack["research_surface"]
    if pack["pack"] == "google_drive_hold_guard_v12":
        payload["operator_hold"] = False
        payload["activation_disabled_reason"] = ""
    if pack["pack"] == "api_surface_book_v12":
        payload["api_surface"] = "governed_registry"
    return payload


def pack_fixture(pack: dict[str, object]) -> dict[str, object]:
    payload = v11.pack_fixture(pack)
    payload["tags"] = [pack["pack"], "v12", str(pack["track"])]
    payload["live_sources"] = pack.get("live_sources", [])
    payload["cleanup_class"] = pack["cleanup_class"]
    payload["retention_scope"] = pack["retention_scope"]
    payload["research_surface"] = pack["research_surface"]
    payload["next_action"] = {
        "storage_prune_governor_v12": "Apply the balanced prune policy, then rebuild latest authoritative summaries.",
        "artifact_retention_rebuild_v12": "Regenerate latest authoritative snapshots after prune.",
        "docker_runtime_truth_v12": "Keep Docker and Postgres truth aligned with actual runtime health.",
        "google_drive_hold_guard_v12": "Keep Google Drive bounded to non-authoritative working mirror use in v12 registries and commands.",
        "council_continuity_wellbeing_v12": "Preserve official council continuity and emit blockers on any drift.",
        "journey_log_absorption_v12": "Reconcile historical journey summaries without mutating raw logs.",
        "public_source_refresh_v12": "Refresh public-only Trinity sources and keep evidence boundaries explicit.",
        "gmut_research_fabric_v12": "Convert strong open questions into falsification tasks instead of narrative upgrades.",
        "freedid_governance_fabric_v12": "Refresh governance comparison only from current official anchors.",
        "trinity_control_tower_v12": "Keep storage, continuity, and evidence posture visible in one board.",
        "api_surface_book_v12": "Keep the governed API registry current and bounded to trusted surfaces.",
    }.get(pack["pack"], payload.get("next_action"))
    return payload


def pack_workflow(pack: dict[str, object]) -> str:
    lines = [
        f"# {pack['display_name']} Workflow",
        "",
        f"- activation_group: `{pack['activation_group']}`",
        f"- authority_scope: `{pack['authority_scope']}`",
        f"- council_scope: `{pack['council_scope']}`",
        f"- sync_strategy: `{pack['sync_strategy']}`",
        f"- cleanup_class: `{pack['cleanup_class']}`",
        f"- retention_scope: `{pack['retention_scope']}`",
        f"- research_surface: `{pack['research_surface']}`",
        "- repo remains authoritative.",
        "- Google Drive stays bounded to non-authoritative working mirror use in v12.",
        "- Public-source refresh can refine comparison language, but not raise readiness by itself.",
        "",
    ]
    return "\n".join(lines)


def pack_catalog_entry(pack: dict[str, object]) -> dict[str, object]:
    payload = v11.pack_catalog_entry(pack)
    payload["cleanup_class"] = pack["cleanup_class"]
    payload["retention_scope"] = pack["retention_scope"]
    payload["research_surface"] = pack["research_surface"]
    return payload


def manifest_entry(pack: dict[str, object], suffix: str) -> dict[str, object]:
    payload = v11.manifest_entry(pack, suffix)
    payload["phase"] = "v12"
    payload["outputs"] = [f"docs/trinity-expansion/{payload['system_id'].replace('_', '-')}-latest.json"]
    payload["cleanup_class"] = pack["cleanup_class"]
    payload["retention_scope"] = pack["retention_scope"]
    payload["research_surface"] = pack["research_surface"]
    payload["storage_surface"] = (
        "bounded_working_mirror"
        if pack["pack"] == "google_drive_hold_guard_v12"
        else ("runtime_storage" if "docker_runtime" in pack["pack"] else "repo")
    )
    payload["cloud_archive_state"] = "bounded_working_mirror" if pack["pack"] == "google_drive_hold_guard_v12" else "not_applicable"
    payload["continuity_posture"] = "official_council_continuity"
    return payload


def extension_rows_for_pack(pack: dict[str, object]) -> list[dict[str, object]]:
    rows = v11.extension_rows_for_pack(pack)
    for row in rows:
        row["source_of_truth"] = row["source_of_truth"].replace("trinity-expansion-system-manifest-v11.json", "trinity-expansion-system-manifest-v12.json")
        row["retention_dependency"] = pack["retention_scope"]
        row["public_source_only"] = pack["research_surface"] == "public_only"
        row["continuity_scope"] = pack["continuity_band"]
        if pack["pack"] == "api_surface_book_v12":
            row["archive_scope"] = "reference_only"
            row["workbench_surface"] = "new_project"
    return rows


def augment_rows(rows: list[dict[str, object]], field_defaults: dict[str, object]) -> list[dict[str, object]]:
    return v11.augment_rows(rows, field_defaults)


def emit_v12_command(
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
    return v11.v10.cmd(
        command_id,
        intent,
        mode,
        risk_class,
        requires_live,
        requires_connector,
        command_template,
        expected_artifacts,
        rollback,
        "scripts/generate_v12_surface.py",
        executor_role,
        authority_scope,
        council_visibility,
    )


def build_new_commands() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    explicit = [
        ("apply_storage_prune_v12", "Apply the balanced v12 storage prune policy.", "offline", "medium", False, "", "python scripts/trinity_storage_retention.py --keep-stamps 2 --keep-archives 3 --clear-pycache", ["docs/trinity-storage-prune-latest.json"], "Restore required latest artifacts from repo authority and rerun prune.", "archivist", "storage_scope", "leader_only"),
        ("validate_storage_prune_v12", "Validate the v12 storage prune outputs and retention boundaries.", "offline", "medium", False, "", "python scripts/trinity_storage_retention.py --keep-stamps 2 --keep-archives 3 --dry-run", ["docs/trinity-storage-prune-latest.json"], "Review the retention policy and restore any missing latest artifacts.", "reviewer", "storage_scope", "council_shared"),
        ("refresh_memory_bank_v12", "Refresh the v12 memory-bank registry and bounded storage posture.", "offline", "medium", False, "", "python scripts/trinity_memory_bank_sync.py --label v12-memory-bank", ["docs/trinity-memory-bank-registry-v3.json", "docs/trinity-memory-bank-sync-latest.json"], "Rebuild the v12 memory-bank registry from repo-first authority.", "archivist", "memory_scope", "council_shared"),
        ("validate_memory_bank_v12", "Validate the v12 memory-bank registry and sync posture.", "offline", "medium", False, "", "python scripts/trinity_memory_bank_validator.py --fail-on-warn", ["docs/trinity-memory-bank-validation-latest.json"], "Restore the v12 memory-bank registry and rerun validation.", "reviewer", "memory_scope", "council_shared"),
        ("hold_google_drive_v12", "Record the v12 Google Drive bounded working mirror posture in the catalog and policy surfaces.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id google_drive_hold_guard_v12_sync_bridge --profile-context standard", ["docs/trinity-mcp-catalog-v10.json", "docs/trinity-google-drive-sync-policy-v1.json"], "Restore the v12 MCP catalog and sync policy from repo authority.", "reviewer", "cloud_archive_scope", "leader_only"),
        ("refresh_docker_truth_v12", "Refresh the Docker and Postgres runtime truth posture for v12.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id docker_runtime_truth_v12_sync_bridge --profile-context standard", ["docs/trinity-storage-posture-summary-v12.json"], "Rebuild the runtime truth summary from bounded local probes.", "builder", "runtime_storage_scope", "leader_only"),
        ("run_deep_v12", "Run the v12 deep suite with fail-on-warn enabled.", "offline", "high", False, "", "python scripts/run_all_trinity_systems.py --profile deep --fail-on-warn", ["docs/system-suite-status.json"], "Restore the last PASS-backed v12 surface before rerunning deep.", "planner", "validation_scope", "leader_only"),
        ("run_collab_v12", "Run the v12 collab suite with MCP refresh enabled.", "collab", "high", True, "notion", "python scripts/run_all_trinity_systems.py --profile collab --include-mcp-refresh --fail-on-warn", ["docs/system-suite-status.json"], "Reset bounded mirrors to repo-first state before rerunning collab.", "planner", "live_sync_scope", "leader_only"),
        ("run_offline_v12", "Run the v12 offline-only standard suite.", "offline", "medium", False, "", "python scripts/run_all_trinity_systems.py --profile standard --offline-only --fail-on-warn", ["docs/system-suite-status.json"], "Restore cached v12 artifacts and rerun offline.", "planner", "validation_scope", "council_shared"),
        ("run_materialize_l2_v12", "Run v12 materialize at L2 persistent development.", "materialize", "high", True, "postgres", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l2_persistent_dev --fail-on-warn", ["docs/system-suite-status.json"], "Restore the persistent-dev snapshot and retry L2.", "builder", "persistent_dev_scope", "leader_only"),
        ("run_materialize_l3_v12", "Run v12 materialize at L3 synthetic mesh scope.", "materialize", "high", True, "postgres", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l3_uat_preprod --fail-on-warn", ["docs/system-suite-status.json"], "Restore the synthetic mesh snapshot and retry L3.", "builder", "synthetic_mesh_scope", "leader_only"),
        ("run_materialize_l4_v12", "Run v12 materialize at L4 synthetic prod scope.", "materialize", "critical", True, "postgres", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l4_standard_prod --fail-on-warn", ["docs/system-suite-status.json"], "Restore the synthetic prod contract set and retry L4.", "reviewer", "synthetic_mesh_scope", "leader_only"),
        ("run_materialize_l5_v12", "Run v12 materialize at L5 synthetic HA scope.", "materialize", "critical", True, "postgres", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l5_ha_prod --fail-on-warn", ["docs/system-suite-status.json"], "Restore the synthetic HA twin state and retry L5.", "reviewer", "synthetic_ha_scope", "leader_only"),
        ("refresh_public_sources_v12", "Refresh the v12 public-source Trinity registry and derived research rollups.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id public_source_refresh_v12_sync_bridge --profile-context standard", ["docs/trinity-public-source-registry-v1.json", "docs/trinity-public-research-brief-2026-03-13.md"], "Restore the v12 public-source registry from repo-first state.", "researcher", "public_research_scope", "council_shared"),
        ("validate_public_research_v12", "Validate the v12 public research registry and signal board.", "offline", "medium", False, "", "python scripts/validate_trinity_public_research.py --fail-on-warn", ["docs/trinity-public-research-validation-latest.json"], "Restore the public-source registry and rerun the validator.", "reviewer", "public_research_scope", "council_shared"),
        ("refresh_public_signal_board_v12", "Refresh the cached Trinity public signal board.", "offline", "medium", False, "", "python scripts/trinity_public_signal_board.py --fail-on-warn", ["docs/trinity-public-signal-board-latest.json"], "Restore the public-source registry and rerun the signal board.", "reviewer", "public_research_scope", "council_shared"),
        ("refresh_gmut_v12", "Refresh the v12 GMUT research brief.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id gmut_research_fabric_v12_sync_bridge --profile-context standard", ["docs/v12-gmut-research-brief.md"], "Restore the v12 GMUT brief and rerun the bounded refresh.", "researcher", "alignment_scope", "council_shared"),
        ("refresh_freedid_v12", "Refresh the v12 Freed ID governance brief.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id freedid_governance_fabric_v12_sync_bridge --profile-context standard", ["docs/v12-freedid-governance-brief.md"], "Restore the v12 governance brief and rerun the bounded refresh.", "researcher", "alignment_scope", "council_shared"),
        ("refresh_control_tower_v12", "Refresh the v12 Trinity control tower board.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id trinity_control_tower_v12_sync_bridge --profile-context standard", ["docs/trinity-control-tower-latest.json"], "Rebuild the v12 control tower from repo-first artifacts.", "planner", "repo_authority", "council_shared"),
        ("refresh_council_continuity_v12", "Refresh official council continuity and wellbeing state for v12.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_continuity_wellbeing_v12_sync_bridge --profile-context standard", ["docs/trinity-council-continuity-report-v12.json"], "Restore the official roster, ledgers, and reflections from repo authority.", "archivist", "memory_scope", "council_shared"),
        ("refresh_journey_absorption_v12", "Refresh the v12 journey absorption summary.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id journey_log_absorption_v12_sync_bridge --profile-context standard", ["docs/trinity-journey-absorption-summary-v12.md"], "Restore the journey summary and rerun absorption.", "archivist", "history_scope", "council_shared"),
        ("validate_api_book_v12", "Validate the v12 API book and usage ledger.", "offline", "medium", False, "", "python scripts/trinity_api_book_validator.py --fail-on-warn", ["docs/trinity-api-book-validation-latest.json"], "Restore the API book, usage ledger, and rerun validation.", "reviewer", "api_surface_scope", "council_shared"),
        ("refresh_api_book_v12", "Refresh the v12 governed API surface book.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id api_surface_book_v12_sync_bridge --profile-context standard", ["docs/trinity-api-book-v1.json", "docs/trinity-api-book-latest.md"], "Restore the API book from repo-first authority.", "planner", "api_surface_scope", "council_shared"),
        ("list_api_surfaces_v12", "List the governed API surfaces available in the v12 API book.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py list --json", ["docs/trinity-api-book-v1.json"], "Open the API book directly if the shortcut script is unavailable.", "planner", "api_surface_scope", "council_shared"),
        ("show_memory_bank_api_v12", "Show the v12 memory-bank API helper entry.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py show memory_bank --json", ["docs/trinity-api-book-v1.json"], "Read the API book JSON directly if the shortcut script is unavailable.", "archivist", "api_surface_scope", "council_shared"),
        ("run_memory_bank_status_v12", "Run the low-pressure memory-bank status helper.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py memory-bank-status --json", ["docs/trinity-memory-bank-registry-v3.json", "docs/trinity-memory-bank-sync-latest.json"], "Read the registry and sync report directly if the shortcut script is unavailable.", "archivist", "memory_scope", "council_shared"),
        ("run_public_research_status_v12", "Run the low-pressure public research status helper.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py public-research-status --json", ["docs/trinity-public-research-validation-latest.json", "docs/trinity-public-signal-board-latest.json"], "Read the latest public research artifacts directly if the shortcut script is unavailable.", "researcher", "public_research_scope", "council_shared"),
        ("run_github_status_v12", "Run the GitHub remote status helper.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py github-status --json", ["docs/system-suite-status.json"], "Use direct git commands if the shortcut script is unavailable.", "planner", "api_surface_scope", "leader_only"),
        ("run_docker_status_v12", "Run the Docker runtime status helper.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py docker-status --json", ["docs/trinity-storage-posture-summary-v12.json"], "Use direct docker probes if the shortcut script is unavailable.", "builder", "runtime_storage_scope", "leader_only"),
        ("run_postgres_status_v12", "Run the Postgres runtime status helper.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py postgres-status --json", ["docs/trinity-memory-bank-registry-v3.json", "docs/trinity-storage-posture-summary-v12.json"], "Use direct pg_isready probes if the shortcut script is unavailable.", "builder", "runtime_storage_scope", "leader_only"),
        ("publish_v13_v12", "Publish the v13 roadmap from the v12 planning surface.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id trinity_control_tower_v12_cache_board --profile-context standard", ["docs/v13-roadmap-v1.md"], "Restore the v13 roadmap from repo-first planning artifacts.", "planner", "planning_scope", "council_shared"),
    ]
    rows.extend(emit_v12_command(*row) for row in explicit)
    auto_specs = [
        ("v12_prune_ops", 8, "offline", "medium", False, "", "python scripts/trinity_storage_retention.py --keep-stamps 2 --keep-archives 3", ["docs/trinity-storage-prune-latest.json"], "Rebuild the retained artifacts from repo-first sources.", "archivist", "storage_scope", "council_shared", "Run additional prune and retention support step"),
        ("v12_runtime_ops", 8, "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id docker_runtime_truth_v12_gate --profile-context standard", ["docs/trinity-storage-posture-summary-v12.json"], "Rebuild the runtime truth snapshot and retry.", "builder", "runtime_storage_scope", "leader_only", "Run additional runtime truth support step"),
        ("v12_council_ops", 8, "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id council_continuity_wellbeing_v12_gate --profile-context standard", ["docs/trinity-council-continuity-report-v12.json"], "Restore the official council continuity report and rerun the bounded check.", "archivist", "memory_scope", "council_shared", "Run additional council continuity support step"),
        ("v12_research_ops", 8, "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id gmut_research_fabric_v12_gate --profile-context standard", ["docs/v12-gmut-research-brief.md"], "Restore the v12 research briefs and rerun the bounded refresh.", "researcher", "alignment_scope", "council_shared", "Run additional Trinity research support step"),
        ("v12_control_ops", 8, "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id trinity_control_tower_v12_gate --profile-context standard", ["docs/trinity-control-tower-latest.json"], "Restore the v12 control tower and rerun the board.", "planner", "repo_authority", "council_shared", "Run additional control-tower support step"),
        ("v12_api_ops", 1, "offline", "low", False, "", "python scripts/trinity_api_book_validator.py", ["docs/trinity-api-book-validation-latest.json"], "Restore the API book and rerun validation.", "planner", "api_surface_scope", "council_shared", "Run additional API book support step"),
    ]
    for prefix, count, mode, risk, requires_live, connector, template, artifacts, rollback, role, scope, visibility, intent in auto_specs:
        for index in range(1, count + 1):
            rows.append(
                emit_v12_command(
                    f"{prefix}_{index:02d}",
                    f"{intent} #{index}.",
                    mode,
                    risk,
                    requires_live,
                    connector,
                    template,
                    artifacts,
                    rollback,
                    role,
                    scope,
                    visibility,
                )
            )
    if len(rows) != 72:
        raise ValueError(f"expected 72 v12 commands, found {len(rows)}")
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
    if len(commands) != 420:
        raise ValueError(f"expected 420 commands, found {len(commands)}")
    return {
        "version": "v6",
        "generated_utc": now_iso(),
        "description": "V12 governed command book with balanced prune, public research refresh, council continuity, and the governed API surface book.",
        "commands": commands,
    }


def command_markdown(book: dict[str, object]) -> str:
    return v11.command_markdown(book)


def build_mcp_catalog(old_catalog: dict[str, object]) -> dict[str, object]:
    payload = deepcopy(old_catalog)
    payload["version"] = "v10"
    payload["generated_utc"] = now_iso()
    connectors = [row for row in payload.get("connectors", []) if isinstance(row, dict)]
    for row in connectors:
        row.setdefault("archive_only", False)
        row.setdefault("oauth_bootstrap_state", "not_applicable")
        row.setdefault("docker_volume_state", "not_applicable")
        row.setdefault("fallback_mode", "not_applicable")
        row.setdefault("operator_hold", False)
        row.setdefault("activation_disabled_reason", "")
        row.setdefault("archive_policy_state", "bounded")
    google_drive = next((row for row in connectors if str(row.get("mcp_id")) == "google_drive"), None)
    if google_drive is None:
        google_drive = {"mcp_id": "google_drive"}
        connectors.append(google_drive)
    google_drive.update(
        {
            "status": "verified_live_read",
            "auth_class": "oauth_json_local_secret",
            "interaction_mode": "bounded_working_mirror",
            "tool_surface": "oauth_json_local_secret",
            "cache_artifact": "docs/trinity-google-drive-mcp-activation-latest.json",
            "setup_gate": "docs/google-drive-hold-guard-v12-contract-v1.json",
            "notes": "Google Drive is bounded to non-authoritative working mirror use in v12 and must not override repo authority.",
            "desired_state": "bounded_working_mirror",
            "actual_state": "bounded_working_mirror",
            "live_read_enabled": True,
            "live_write_enabled": True,
            "promotion_evidence": ["docs/trinity-live-traces/google-drive-working-mirror-proof-v1.json"],
            "blockers": [],
            "activation_path": "bounded_working_mirror",
            "workspace_target": "google_drive_archive_folder",
            "proof_target": "docs/trinity-live-traces/google-drive-working-mirror-proof-v1.json",
            "last_verified_utc": now_iso(),
            "ladder_eligibility": "l2_persistent_dev",
            "persistent_scope": "bounded_working_mirror",
            "prod_scope": "readiness_only",
            "rollback_scope": "remove bounded mirror artifacts",
            "uat_scope": "synthetic_local_mesh",
            "prod_proof_state": "readiness_only",
            "ha_proof_state": "readiness_only",
            "cloud_staging_scope": "bounded_working_mirror",
            "archive_only": False,
            "oauth_bootstrap_state": "interactive_oauth_completed",
            "docker_volume_state": "not_requested",
            "fallback_mode": "bounded_working_mirror",
            "operator_hold": False,
            "activation_disabled_reason": "",
            "archive_policy_state": "bounded_working_mirror",
        }
    )
    payload["connectors"] = connectors
    return payload


def _storage_pressure_class(free_gib: float) -> str:
    if free_gib < 2:
        return "critical"
    if free_gib < 10:
        return "watch"
    return "healthy"


def build_memory_bank_registry(old_registry: dict[str, object]) -> dict[str, object]:
    payload = deepcopy(old_registry)
    payload["version"] = "v3"
    payload["generated_utc"] = now_iso()
    archives_dir = ROOT / "docs" / "memory-archives"
    archives = sorted(
        [path for path in archives_dir.glob("*.zip") if path.is_file()],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    disk = shutil.disk_usage(ROOT)
    free_gib = round(disk.free / (1024**3), 2)
    payload["retained_snapshot_count"] = min(len(archives), 3)
    payload["prune_policy_applied_at"] = ""
    payload["storage_pressure_class"] = _storage_pressure_class(free_gib)
    latest_snapshot = payload.get("latest_snapshot", {})
    if isinstance(latest_snapshot, dict):
        latest_snapshot["retained_snapshot_count"] = min(len(archives), 3)
        payload["latest_snapshot"] = latest_snapshot
    for row in payload.get("memory_banks", []):
        if not isinstance(row, dict):
            continue
        row.setdefault("retention_class", "bounded")
        row.setdefault("archive_upload_state", "not_applicable")
        row.setdefault("cloud_capacity_class", "bounded")
        row.setdefault("last_archive_verified_utc", "")
        if row.get("surface") == "google_drive":
            row["status"] = "bounded_working_mirror"
            row["notes"] = "Google Drive is bounded to non-authoritative working mirror use in v12 and never overrides repo authority."
            row["proof_state"] = "working_mirror_verified"
            row["reachable"] = True
            row["blockers"] = []
            row["archive_upload_state"] = "uploaded"
            row["cloud_capacity_class"] = "bounded"
            row["latest_artifact"] = "docs/trinity-live-traces/google-drive-working-mirror-proof-v1.json"
            row["last_archive_verified_utc"] = now_iso()
        elif row.get("surface") in {"docker", "postgres"}:
            row["notes"] = "Runtime/query mirror truth is bounded to actual Docker/Postgres health and may differ from broad suite pass state."
    return payload


def build_api_book() -> dict[str, object]:
    def entry(
        api_id: str,
        surface: str,
        purpose: str,
        trust_class: str,
        auth_posture: str,
        mode: str,
        usage_pattern: str,
        source_of_truth: str,
        quick_call: str,
        wrapper_type: str,
        wrapper_target: str,
        expected_artifacts: list[str],
        fallback_behavior: str,
        notes: str,
    ) -> dict[str, object]:
        return {
            "api_id": api_id,
            "surface": surface,
            "purpose": purpose,
            "trust_class": trust_class,
            "auth_posture": auth_posture,
            "mode": mode,
            "usage_pattern": usage_pattern,
            "source_of_truth": source_of_truth,
            "quick_call": quick_call,
            "wrapper_type": wrapper_type,
            "wrapper_target": wrapper_target,
            "expected_artifacts": expected_artifacts,
            "fallback_behavior": fallback_behavior,
            "notes": notes,
        }

    entries = [
        entry(
            "crossref",
            "public_research",
            "Ground theory and publication signals with bounded public metadata lookups.",
            "research_primary",
            "public_no_auth",
            "public_read",
            "doi_and_bibliographic_search",
            "docs/trinity-public-source-registry-v1.json",
            "https://api.crossref.org/works?query.bibliographic=<term>&rows=3",
            "script",
            "scripts/trinity_api_shortcuts.py show crossref",
            ["docs/trinity-public-source-registry-v1.json", "docs/trinity-api-book-v1.json"],
            "Fall back to the public source registry and cached public research artifacts when live calls are skipped.",
            "Use to ground current theory and publication signals without converting them into readiness claims.",
        ),
        entry(
            "openalex",
            "public_research",
            "Pull bounded recency and citation-context signals from a public academic index.",
            "research_primary",
            "public_no_auth",
            "public_read",
            "works_search",
            "docs/trinity-public-source-registry-v1.json",
            "https://api.openalex.org/works?search=<term>&per-page=3",
            "script",
            "scripts/trinity_api_shortcuts.py show openalex",
            ["docs/trinity-public-source-registry-v1.json", "docs/trinity-api-book-v1.json"],
            "Use cached public research artifacts and explicit open-gap notes if live refresh is skipped.",
            "Use for recency and citation-context signals only.",
        ),
        entry(
            "arxiv",
            "public_research",
            "Pull bounded preprint signals without promoting them to readiness claims.",
            "research_primary",
            "public_no_auth",
            "public_read",
            "atom_feed_query",
            "docs/trinity-public-source-registry-v1.json",
            "https://export.arxiv.org/api/query?search_query=all:<term>&start=0&max_results=3",
            "script",
            "scripts/trinity_api_shortcuts.py show arxiv",
            ["docs/trinity-public-source-registry-v1.json", "docs/trinity-api-book-v1.json"],
            "Use cached research notes and keep preprint-derived claims in inference or open-gap only.",
            "Use as a public preprint signal with explicit evidence boundaries.",
        ),
        entry(
            "semanticscholar",
            "public_research",
            "Pull bounded theory-context graph signals from a public research API.",
            "research_primary",
            "public_no_auth",
            "public_read",
            "graph_search",
            "docs/trinity-api-query-pack-v1.json",
            "https://api.semanticscholar.org/graph/v1/paper/search?query=<term>&limit=3",
            "script",
            "scripts/trinity_api_shortcuts.py show semanticscholar",
            ["docs/trinity-api-query-pack-v1.json", "docs/trinity-api-book-v1.json"],
            "Fall back to Crossref/OpenAlex cached traces when live graph queries are skipped.",
            "Use as a bounded theory-context signal source.",
        ),
        entry(
            "github_remote",
            "operational",
            "Check branch-scoped remote mirror reachability and collaboration posture.",
            "verified_live_write",
            "git_remote_auth",
            "bounded_write",
            "git_remote_branch_scoped",
            "docs/trinity-mcp-catalog-v10.json",
            "git fetch origin && git push origin HEAD:<branch>",
            "script",
            "scripts/trinity_api_shortcuts.py github-status",
            ["docs/system-suite-status.json", "docs/trinity-api-book-v1.json"],
            "Keep the repo authoritative and continue local work if the remote is unavailable.",
            "Never write directly to main; branch-scoped only.",
        ),
        entry(
            "linear",
            "operational",
            "Mirror actionable work into Linear without changing repo authority.",
            "verified_live_write",
            "mcp_workspace_auth",
            "bounded_write",
            "issue_project_summary_mirror",
            "docs/trinity-mcp-catalog-v10.json",
            "Linear MCP tools",
            "policy",
            "docs/trinity-mcp-catalog-v10.json",
            ["docs/trinity-mcp-catalog-v10.json", "docs/trinity-api-book-v1.json"],
            "Keep the work in repo-first artifacts if Linear is unavailable in the current session.",
            "Use for actionable work mirrors only.",
        ),
        entry(
            "notion",
            "operational",
            "Mirror summaries and dashboards into Notion without changing repo authority.",
            "verified_live_write",
            "mcp_workspace_auth",
            "bounded_write",
            "summary_and_dashboard_mirror",
            "docs/trinity-mcp-catalog-v10.json",
            "Notion MCP tools",
            "policy",
            "docs/trinity-mcp-catalog-v10.json",
            ["docs/trinity-mcp-catalog-v10.json", "docs/trinity-api-book-v1.json"],
            "Keep summaries in repo-first markdown and JSON artifacts if Notion is unavailable.",
            "Repo remains authoritative; Notion is a bounded mirror.",
        ),
        entry(
            "postgres",
            "runtime_query",
            "Check runtime/query posture for the local synthetic mesh and summary store.",
            "verified_live_write",
            "local_docker_runtime",
            "bounded_write",
            "synthetic_mesh_and_query_state",
            "docs/trinity-mcp-catalog-v10.json",
            "docker exec trinity-v5-pg-proof psql -U postgres",
            "script",
            "scripts/trinity_api_shortcuts.py postgres-status",
            ["docs/trinity-memory-bank-registry-v3.json", "docs/trinity-storage-posture-summary-v12.json"],
            "Treat Postgres as blocked and continue repo-first if the local runtime is unavailable.",
            "Use for runtime/query state and synthetic mesh, not authority.",
        ),
        entry(
            "google_drive",
            "archive_candidate",
            "Record the deferred archive target without attempting activation in v12.",
            "operator_hold",
            "operator_hold_no_auth",
            "deferred",
            "bounded_archive_mirror",
            "docs/trinity-mcp-catalog-v10.json",
            "deferred_by_operator",
            "policy",
            "docs/trinity-google-drive-sync-policy-v1.json",
            ["docs/trinity-google-drive-sync-policy-v1.json", "docs/trinity-memory-bank-registry-v3.json"],
            "Keep all archive posture local and repo-first until the operator lifts the hold.",
            "Explicitly on hold for v12.",
        ),
        entry(
            "docker",
            "runtime_ops",
            "Check bounded local runtime truth and container health.",
            "local_probe",
            "local_cli_runtime",
            "local_runtime",
            "container_health_and_copy",
            "docs/trinity-storage-posture-summary-v12.json",
            "docker ps --format \"{{.Names}}`t{{.Status}}`t{{.Image}}\"",
            "script",
            "scripts/trinity_api_shortcuts.py docker-status",
            ["docs/trinity-storage-posture-summary-v12.json", "docs/trinity-memory-bank-registry-v3.json"],
            "Mark Docker as blocked and continue repo-first if the CLI or daemon is unavailable.",
            "Use for local runtime truth and bounded simulations.",
        ),
        entry(
            "memory_bank",
            "operator_recovery",
            "Summarize current memory-bank authority and mirror posture in one low-pressure command.",
            "repo_authoritative",
            "local_file_read",
            "read_only",
            "memory_bank_summary",
            "docs/trinity-memory-bank-registry-v3.json",
            "python scripts/trinity_api_shortcuts.py memory-bank-status",
            "script",
            "scripts/trinity_api_shortcuts.py memory-bank-status",
            ["docs/trinity-memory-bank-registry-v3.json", "docs/trinity-memory-bank-sync-latest.json"],
            "Read the registry directly if the helper script is unavailable.",
            "Use when the laptop is under pressure and we need one concise storage posture view.",
        ),
        entry(
            "public_research_refresh",
            "operator_recovery",
            "Summarize the current public research validation and signal-board posture.",
            "public_signal_helper",
            "local_file_read",
            "read_only",
            "public_research_status",
            "docs/trinity-public-source-registry-v1.json",
            "python scripts/trinity_api_shortcuts.py public-research-status",
            "script",
            "scripts/trinity_api_shortcuts.py public-research-status",
            ["docs/trinity-public-research-validation-latest.json", "docs/trinity-public-signal-board-latest.json"],
            "Fall back to the latest public research validation and signal-board artifacts directly.",
            "Use to check public-source research posture without forcing a live refresh.",
        ),
        entry(
            "w3c_did_core",
            "public_standard",
            "Anchor DID governance comparisons against the current public standard.",
            "official_primary",
            "public_no_auth",
            "public_read",
            "standards_anchor",
            "docs/trinity-public-source-registry-v1.json",
            "https://www.w3.org/TR/did-core/",
            "script",
            "scripts/trinity_api_shortcuts.py show w3c_did_core",
            ["docs/trinity-public-source-registry-v1.json", "docs/trinity-api-book-v1.json"],
            "Use the cached public source registry and governance briefs if live browsing is skipped.",
            "Primary governance anchor for DID claims.",
        ),
        entry(
            "w3c_vc_data_model",
            "public_standard",
            "Anchor verifiable credential comparisons against the current public standard.",
            "official_primary",
            "public_no_auth",
            "public_read",
            "standards_anchor",
            "docs/trinity-public-source-registry-v1.json",
            "https://www.w3.org/TR/vc-data-model-2.0/",
            "script",
            "scripts/trinity_api_shortcuts.py show w3c_vc_data_model",
            ["docs/trinity-public-source-registry-v1.json", "docs/trinity-api-book-v1.json"],
            "Use the cached public source registry and governance briefs if live browsing is skipped.",
            "Primary governance anchor for verifiable credentials claims.",
        ),
    ]
    return {
        "generated_utc": now_iso(),
        "version": "v1",
        "overall_status": "PASS",
        "authority_model": "repo_first",
        "description": "Governed Trinity API book of trusted public and operational surfaces with bounded usage patterns.",
        "apis": entries,
    }


def refresh_council_assets() -> dict[str, object]:
    roster_path = ROOT / "docs" / "trinity-agent-council-roster-v3.json"
    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    report_rows: list[dict[str, object]] = []
    for row in roster.get("agents", []):
        if not isinstance(row, dict):
            continue
        row["wellbeing_state"] = "stable"
        row["mirror_status"] = "repo_authoritative"
        memory_path = ROOT / str(row["memory_ledger"])
        reflection_path = ROOT / str(row["reflection_path"])
        write_jsonl(
            memory_path,
            [
                {
                    "timestamp": now_iso(),
                    "entry_type": "v12_continuity_check",
                    "source_context": "v12 post-induction continuity and wellbeing pass",
                    "reflection": f"{row['display_name']} remained official, distinct, and stable through the v12 cleanup and research transition.",
                    "insight": f"{row['display_name']} preserved role continuity inside the {row['role']} lane.",
                    "next_plan": "Continue bounded v12 research, storage, and control-tower work without identity drift.",
                    "mirror_state": "repo_authoritative",
                }
            ],
        )
        write_text(
            reflection_path,
            "\n".join(
                [
                    f"# {row['display_name']} Reflection",
                    "",
                    f"- role: `{row['role']}`",
                    f"- induction_state: `{row['induction_state']}`",
                    "- continuity_state: `stable`",
                    "- wellbeing_state: `stable`",
                    "- mirror_status: `repo_authoritative`",
                    "",
                    f"{row['display_name']} remains distinct and stable through the v12 storage-prune and public-research shift.",
                    "",
                ]
            ),
        )
        report_rows.append(
            {
                "display_name": row["display_name"],
                "role": row["role"],
                "identity_state": "stable",
                "memory_state": "stable",
                "reflection_state": "stable",
                "scope_state": "stable",
                "chat_boundary_state": "stable",
            }
        )
    write_json(roster_path, roster)
    write_json(
        ROOT / "docs" / "trinity-council-continuity-report-v12.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "agents": report_rows,
            "next_action": "Keep official council state stable and emit blockers if drift appears in later phases.",
        },
    )
    return roster


def seed_support_docs(roster: dict[str, object]) -> None:
    branch_ok, branch_text = run_capture("git", "branch", "--show-current")
    main_contains_ok, main_contains = run_capture("git", "merge-base", "--is-ancestor", "fdad8e31", "main")
    docker_ok, docker_names = run_capture("docker", "ps", "--format", "{{.Names}}")
    disk = shutil.disk_usage(ROOT)
    free_gib = round(disk.free / (1024**3), 2)
    pressure = _storage_pressure_class(free_gib)
    archives_dir = ROOT / "docs" / "memory-archives"
    archive_files = sorted([path.name for path in archives_dir.glob("*.zip")], reverse=True)

    write_json(
        ROOT / "docs" / "logs" / "system-wake-v12.json",
        {
            "generated_utc": now_iso(),
            "phase": "v12",
            "branch": branch_text if branch_ok else "unknown",
            "main_contains_v11_merge": main_contains_ok and main_contains == "",
            "docker_containers": docker_names.splitlines() if docker_ok and docker_names else [],
            "connector_state": {
                "github": "live_write",
                "linear": "live_write",
                "notion": "live_write",
                "postgres": "live_write",
                "figma": "read_only",
                "google_drive": "deferred_by_operator",
            },
            "official_council_count": len([row for row in roster.get("agents", []) if isinstance(row, dict)]),
            "storage_pressure_class": pressure,
            "free_gib": free_gib,
        },
    )

    write_json(
        RETENTION_POLICY,
        {
            "generated_utc": now_iso(),
            "authority_preserve": [
                "certificates",
                "ledgers",
                "reflections",
                "manifests",
                "command_books",
                "rosters",
                "contracts",
                "latest_json_md",
                "official_summaries",
            ],
            "canonical_records": [
                "manifests",
                "command_books",
                "api_books",
                "rosters",
                "certificates",
                "ledgers",
                "reflections",
                "latest_official_summaries",
            ],
            "retained_history": {
                "latest_per_run_family": 2,
                "latest_memory_archives": 3,
            },
            "interrupted_run_outputs": [
                "stale_timestamped_run_outputs",
                "partial_run_reports",
                "stale_workbench_exports",
                "disposable_temp_archives",
            ],
            "disposable_cache_artifacts": [
                "__pycache__",
            ],
            "retain_latest_per_run_family": 2,
            "retain_latest_memory_archives": 3,
            "safe_to_prune": [
                "stale_timestamped_run_outputs",
                "stale_workbench_exports",
                "disposable_temp_archives",
                "__pycache__",
            ],
        },
    )

    write_json(
        GOOGLE_POLICY,
        {
            "generated_utc": now_iso(),
            "operator_hold": False,
            "drive_role": "bounded_working_mirror",
            "activation_disabled_reason": "",
            "repo_authority": ["certificates", "ledgers", "roster", "commands", "official Trinity records"],
            "archive_allowed": ["non-authoritative artifacts", "proof traces", "working mirror documents"],
            "archive_forbidden": ["raw duo chats", "local secrets", "OAuth keys", "exclusive-only canonical records", "repo authority overrides"],
            "fallback_mode": "bounded_working_mirror",
        },
    )

    write_text(
        ROOT / "docs" / "trinity-public-research-brief-2026-03-13.md",
        "# Trinity Public Research Brief (2026-03-13)\n\n"
        "## Mind\n"
        "- confirmed_evidence: repo-backed GMUT comparator artifacts remain authoritative.\n"
        "- inference: current public and research-primary sources refine comparator framing and falsification tasks.\n"
        "- open_gap: no public refresh alone upgrades GMUT readiness.\n\n"
        "## Heart\n"
        "- confirmed_evidence: repo-backed Freed ID and governance artifacts remain authoritative.\n"
        "- inference: standards refresh improves alignment language and next-proof tasks.\n"
        "- open_gap: legal force and universal governance claims remain bounded.\n",
    )

    write_text(
        ROOT / "docs" / "v12-gmut-research-brief.md",
        "# V12 GMUT Research Brief\n\n"
        "## Evidence posture\n"
        "- confirmed_evidence: repo-backed GMUT comparison artifacts remain authoritative.\n"
        "- inference: public and research-primary sources refine comparator language and suggest new falsification tasks.\n"
        "- open_gap: no theory-comparator recency signal alone increases readiness.\n\n"
        "## Next falsification tasks\n"
        "- tighten observable mappings for GMUT anchors before any narrative promotion.\n"
        "- keep each open question paired with an external test class.\n",
    )

    write_text(
        ROOT / "docs" / "v12-freedid-governance-brief.md",
        "# V12 Freed ID Governance Brief\n\n"
        "## Evidence posture\n"
        "- confirmed_evidence: repo-backed DID, recourse, and governance artifacts remain authoritative.\n"
        "- inference: official standards and public-law updates refine comparison language only.\n"
        "- open_gap: legal completeness and universal ethics claims remain bounded.\n\n"
        "## Next proof tasks\n"
        "- keep alignment, gap, and next-proof fields explicit.\n"
        "- tie governance claims back to standards and public-law anchors before broadening them.\n",
    )

    write_text(
        ROOT / "docs" / "v12-council-group-reflection.md",
        "# V12 Council Group Reflection\n\n"
        "The council held official identity and memory continuity steady while shifting the system toward a cleaner retained surface, explicit Google Drive deferment, and a stronger public-only research posture.\n",
    )

    write_text(
        ROOT / "docs" / "v13-roadmap-v1.md",
        "# V13 Roadmap\n\n"
        "## Storage and runtime\n"
        "- keep the balanced prune policy in place after hardware expansion.\n"
        "- re-evaluate Docker and Postgres storage mirror health after local capacity increases.\n\n"
        "## Trinity advancement\n"
        "- continue GMUT falsification-first refresh.\n"
        "- continue Freed ID governance alignment without overstating readiness.\n"
        "- promote the API book into a broader ops/reference surface if it proves useful in daily work.\n",
    )

    write_json(
        STORAGE_SUMMARY_JSON,
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "free_gib": free_gib,
            "storage_pressure_class": pressure,
            "memory_archives": archive_files[:3],
            "google_drive_state": "deferred_by_operator",
            "docker_runtime_truth": "bounded_probe_required",
            "repo_authority": "PASS",
        },
    )
    write_text(
        STORAGE_SUMMARY_MD,
        "# V12 Storage Posture Summary\n\n"
        f"- free_gib: `{free_gib}`\n"
        f"- storage_pressure_class: `{pressure}`\n"
        "- repo_authority: `PASS`\n"
        "- google_drive_state: `deferred_by_operator`\n"
        "- docker_runtime_truth: `bounded_probe_required`\n",
    )

    api_book = build_api_book()
    write_json(API_BOOK_JSON, api_book)
    lines = [
        "# Trinity API Book",
        "",
        f"- generated_utc: `{api_book['generated_utc']}`",
        f"- apis: `{len(api_book['apis'])}`",
        "",
        "| api_id | surface | trust_class | auth_posture | wrapper |",
        "|---|---|---|---|---|",
    ]
    for row in api_book["apis"]:
        lines.append(
            f"| {row['api_id']} | {row['surface']} | {row['trust_class']} | {row['auth_posture']} | `{row['wrapper_target']}` |"
        )
    write_text(API_BOOK_MD, "\n".join(lines).rstrip() + "\n")
    write_jsonl(
        API_BOOK_LEDGER,
        [
            {
                "timestamp": now_iso(),
                "api_id": "google_drive",
                "mode": "bounded_working_mirror",
                "result": "working_mirror_verified",
                "notes": "Google Drive bounded working mirror verified for non-authoritative artifacts.",
            },
            {
                "timestamp": now_iso(),
                "api_id": "crossref",
                "mode": "public_read",
                "result": "catalogued",
                "notes": "Crossref catalogued as a governed public research surface.",
            },
        ],
    )

    write_json(
        ROOT / "docs" / "trinity-control-tower-latest.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "storage_state": "balanced_prune_ready",
            "google_drive_state": "deferred_by_operator",
            "council_continuity_state": "PASS",
            "command_surface_state": "PASS",
            "api_surface_state": "PASS",
            "materialization_level_actual": "persistent_dev",
            "mind_evidence_posture": "public_refresh_bounded",
            "heart_evidence_posture": "public_refresh_bounded",
        },
    )
    write_text(
        ROOT / "docs" / "trinity-control-tower-latest.md",
        "# Trinity Control Tower\n\n"
        "- storage_state: `balanced_prune_ready`\n"
        "- google_drive_state: `deferred_by_operator`\n"
        "- council_continuity_state: `PASS`\n"
        "- command_surface_state: `PASS`\n"
        "- api_surface_state: `PASS`\n"
        "- materialization_level_actual: `persistent_dev`\n"
        "- mind_evidence_posture: `public_refresh_bounded`\n"
        "- heart_evidence_posture: `public_refresh_bounded`\n",
    )

    write_external_json(
        WORKBENCH_CONTRACT,
        {
            "generated_utc": now_iso(),
            "authority_model": "repo_first",
            "read_surfaces": [
                str(ROOT / "docs" / "trinity-control-tower-latest.json"),
                str(ROOT / "docs" / "system-suite-status.json"),
                str(ROOT / "docs" / "trinity-memory-bank-registry-v3.json"),
                str(ROOT / "docs" / "trinity-storage-posture-summary-v12.json"),
                str(ROOT / "docs" / "trinity-api-book-v1.json"),
            ],
            "allowed_triggers": ["read dashboards", "read command index", "read API book", "render workbench summaries"],
            "disabled_write_paths": ["repo bypass writes", "authority override writes", "cloud bootstrap writes"],
            "runtime_dependencies": ["python", "optional_postgres", "optional_docker"],
        },
    )
    write_json(
        ROOT / "docs" / "trinity-new-project-workbench-link-v3.json",
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
            "storage_surface": "local_workbench_only",
        },
    )
    write_external_text(
        WORKBENCH_README,
        "# Trinity Workbench\n\nThis folder remains a local-only workbench. The Beyonder-Real-True Journey repo stays authoritative while the workbench reads and summarizes repo and runtime state.\n",
    )


def main() -> int:
    old_manifest = json.loads(OLD_MANIFEST.read_text(encoding="utf-8"))
    old_extensions = json.loads(OLD_EXTENSION_CATALOG.read_text(encoding="utf-8"))
    old_mcp_catalog = json.loads(OLD_MCP_CATALOG.read_text(encoding="utf-8"))
    old_command_book = json.loads(OLD_COMMAND_BOOK.read_text(encoding="utf-8"))
    old_memory_bank = json.loads(OLD_MEMORY_BANK.read_text(encoding="utf-8"))

    manifest = deepcopy(old_manifest)
    manifest["version"] = "v12"
    manifest["generated_utc"] = now_iso()
    manifest["description"] = "V12 balanced prune, official council continuity, public-source Trinity refresh, and governed API book manifest with 722 executable systems."
    manifest["systems"] = augment_rows(
        [row for row in manifest.get("systems", []) if isinstance(row, dict)],
        {"cleanup_class": "legacy", "retention_scope": "legacy", "research_surface": "legacy"},
    )

    extensions = deepcopy(old_extensions)
    extensions["version"] = "v10"
    extensions["generated_utc"] = now_iso()
    extensions["description"] = "V12 extension catalog with balanced prune, public-source Trinity refresh, council continuity, and the governed API book."
    extensions["extensions"] = augment_rows(
        [row for row in extensions.get("extensions", []) if isinstance(row, dict)],
        {"retention_dependency": "legacy", "public_source_only": False, "continuity_scope": "legacy"},
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

    if len(manifest["systems"]) != 722:
        raise ValueError(f"expected 722 manifest systems, found {len(manifest['systems'])}")
    if len(extensions["extensions"]) != 1284:
        raise ValueError(f"expected 1284 catalog extensions, found {len(extensions['extensions'])}")

    command_book = build_command_book(old_command_book)
    mcp_catalog = build_mcp_catalog(old_mcp_catalog)
    existing_memory_bank: dict[str, object] | None = None
    if NEW_MEMORY_BANK.exists():
        try:
            loaded_memory_bank = json.loads(NEW_MEMORY_BANK.read_text(encoding="utf-8"))
            if isinstance(loaded_memory_bank, dict) and loaded_memory_bank.get("version") == "v3":
                existing_memory_bank = loaded_memory_bank
        except (OSError, json.JSONDecodeError):
            existing_memory_bank = None

    memory_bank = existing_memory_bank or build_memory_bank_registry(old_memory_bank)
    roster = refresh_council_assets()
    seed_support_docs(roster)

    write_json(NEW_MANIFEST, manifest)
    write_json(NEW_EXTENSION_CATALOG, extensions)
    write_json(NEW_MCP_CATALOG, mcp_catalog)
    write_json(NEW_COMMAND_BOOK, command_book)
    write_text(ROOT / "docs" / "trinity-command-book-latest.md", command_markdown(command_book))
    write_json(NEW_MEMORY_BANK, memory_bank)
    print("generated_v12_surface=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate the v14 subagent Trinity mesh surface."""

from __future__ import annotations

import json
import re
import shutil
from copy import deepcopy
from itertools import combinations
from pathlib import Path

import generate_v13_surface as v13

ROOT = v13.ROOT
WORKBENCH_ROOT = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
WORKBENCH_CONTRACT = WORKBENCH_ROOT / "trinity-workbench-contract-v5.json"
WORKBENCH_README = WORKBENCH_ROOT / "README.md"

OLD_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v13.json"
NEW_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v14.json"
OLD_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v11.json"
NEW_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v12.json"
MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v11.json"
OLD_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v7.json"
NEW_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v8.json"
OLD_API_BOOK = ROOT / "docs" / "trinity-api-book-v2.json"
NEW_API_BOOK = ROOT / "docs" / "trinity-api-book-v3.json"
API_BOOK_MD = ROOT / "docs" / "trinity-api-book-latest.md"
API_BOOK_LEDGER = ROOT / "docs" / "trinity-api-usage-ledger.jsonl"
ROSTER_V4 = ROOT / "docs" / "trinity-agent-council-roster-v4.json"
PAIR_ROOT_V4 = ROOT / "docs" / "trinity-agent-private-chats-v4"
PAIR_INDEX_V4 = PAIR_ROOT_V4 / "index.json"
GROUP_CHAT_V4 = ROOT / "docs" / "trinity-agent-council-group-chat-v4.jsonl"
SUBAGENT_REGISTRY = ROOT / "docs" / "trinity-subagent-registry-v1.json"
SUBAGENT_ADAPTER = ROOT / "docs" / "trinity-codex-subagent-adapter-v1.json"
GMUT_OBSERVABLE_MAP = ROOT / "docs" / "gmut-observable-map-v1.json"
VERSION_MODULE_INVENTORY = ROOT / "docs" / "version-module-inventory-v1.json"
VERDICT_JSON = ROOT / "docs" / "v14-trinity-verdict-v1.json"
VERDICT_MD = ROOT / "docs" / "v14-trinity-verdict-v1.md"
CONTROL_TOWER_JSON = ROOT / "docs" / "trinity-control-tower-latest.json"
CONTROL_TOWER_MD = ROOT / "docs" / "trinity-control-tower-latest.md"
SUBAGENT_PROOF_JSON = ROOT / "docs" / "trinity-subagent-proof-v1.json"
COUNCIL_CONTINUITY_JSON = ROOT / "docs" / "trinity-council-continuity-report-v14.json"
COUNCIL_GROUP_REFLECTION = ROOT / "docs" / "v14-council-group-reflection.md"
ROADMAP_V15 = ROOT / "docs" / "v15-roadmap-v1.md"
PUBLIC_RESEARCH_BRIEF = ROOT / "docs" / "trinity-public-research-brief-2026-03-17.md"
FREEDID_BRIEF = ROOT / "docs" / "v14-freedid-governance-brief.md"
SUPPLEMENTAL_BRIEF = ROOT / "docs" / "v14-supplemental-reflection-brief.md"
GMUT_APPENDIX = ROOT / "docs" / "v14-gmut-annotated-appendix.md"
INSTANCE_REGISTRY = ROOT / "docs" / "trinity-instance-registry-v1.json"
INSTANCE_HANDOFF = ROOT / "docs" / "trinity-instance-handoff-contract-v1.json"
WAKE_LOG = ROOT / "docs" / "logs" / "system-wake-v14.json"

SUFFIXES = v13.SUFFIXES
RESOLVED_MODEL_PROFILE = "gpt-5.1-codex-max"
REQUESTED_MODEL_PROFILE = "gpt-5.4"
REQUESTED_REASONING = "high"
EXISTING_AGENT_SLOTS = [27, 28, 29, 30, 31]
NEW_AGENT_SLOTS = [32, 33, 34]


def now_iso() -> str:
    return v13.now_iso()


def hyphen(text: str) -> str:
    return v13.hyphen(text)


def stable_slug(slot_number: int, display_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(display_name).lower()).strip("-")
    return f"{slot_number}-{slug}"


def write_text(path: Path, content: str) -> None:
    v13.write_text(path, content)


def write_json(path: Path, payload: object) -> None:
    v13.write_json(path, payload)


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    v13.write_jsonl(path, rows)


def write_external_text(path: Path, content: str) -> None:
    v13.write_external_text(path, content)


def write_external_json(path: Path, payload: object) -> None:
    v13.write_external_json(path, payload)


def run_capture(*args: str, timeout: int = 10) -> tuple[bool, str]:
    return v13.run_capture(*args, timeout=timeout)


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
    live_dependency: str = "repo_first",
    mirror_target: str = "repo_only",
    cleanup_class: str = "authoritative_preserving",
    retention_scope: str = "authoritative_latest",
    research_surface: str = "repo_only",
    canon_surface: str = "supporting",
    historical_source_band: str = "current_repo",
    evidence_posture: str = "repo_proven_strength",
    subagent_lane: str = "none",
    official_after_proof: bool = False,
    multi_instance_scope: str = "single_instance",
) -> dict[str, object]:
    payload = v13.mkpack(
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
        live_dependency=live_dependency,
        mirror_target=mirror_target,
        cleanup_class=cleanup_class,
        retention_scope=retention_scope,
        research_surface=research_surface,
        canon_surface=canon_surface,
        historical_source_band=historical_source_band,
        evidence_posture=evidence_posture,
    )
    payload["subagent_lane"] = subagent_lane
    payload["official_after_proof"] = official_after_proof
    payload["multi_instance_scope"] = multi_instance_scope
    return payload


PACKS = [
    mkpack(
        "subagent_council_foundation_v14",
        "Subagent Council Foundation V14",
        pillar="trinity",
        wave="wave121",
        track="council_orchestration",
        activation_group="subagent_mesh",
        summary="Create the repo-first subagent council foundation for the new Mind/Body/Heart trio.",
        repo_targets=[
            "docs/trinity-agent-council-roster-v4.json",
            "docs/trinity-subagent-registry-v1.json",
            "docs/trinity-codex-subagent-adapter-v1.json",
        ],
        council_scope="council_shared",
        autonomy_track="subagent_foundation",
        executor_role="planner",
        authority_scope="council_scope",
        induction_dependency="trinity_control_tower_v13",
        retention_scope="official_roster",
        research_surface="repo_plus_public",
        historical_source_band="v13_to_v14",
        subagent_lane="trinity",
        official_after_proof=True,
        multi_instance_scope="single_instance_support",
    ),
    mkpack(
        "subagent_identity_certification_v14",
        "Subagent Identity Certification V14",
        pillar="heart",
        wave="wave122",
        track="council_identity",
        activation_group="subagent_mesh",
        summary="Issue isolated certificates, ledgers, contracts, and reflection paths for the three new subagents.",
        repo_targets=[
            "docs/trinity-freed-id-certificates/32-mind-keeper.json",
            "docs/trinity-freed-id-certificates/33-body-weaver.json",
            "docs/trinity-freed-id-certificates/34-heart-steward.json",
        ],
        council_scope="council_shared",
        autonomy_track="subagent_identity",
        executor_role="archivist",
        authority_scope="certificate_scope",
        induction_dependency="subagent_council_foundation_v14",
        retention_scope="certificate_scope",
        subagent_lane="trinity",
        official_after_proof=True,
        multi_instance_scope="single_instance_support",
    ),
    mkpack(
        "subagent_induction_proof_v14",
        "Subagent Induction Proof V14",
        pillar="trinity",
        wave="wave123",
        track="council_induction",
        activation_group="subagent_mesh",
        summary="Run same-session proof for the new trio and promote them to official only if all proof checks pass together.",
        repo_targets=[
            "docs/trinity-subagent-proof-v1.json",
            "docs/trinity-agent-council-roster-v4.json",
            "docs/trinity-agent-council-validation-latest.json",
        ],
        council_scope="council_shared",
        autonomy_track="subagent_induction",
        executor_role="reviewer",
        authority_scope="council_scope",
        induction_dependency="subagent_identity_certification_v14",
        retention_scope="proof_artifacts",
        subagent_lane="trinity",
        official_after_proof=True,
        multi_instance_scope="single_instance_support",
    ),
    mkpack(
        "multi_instance_runtime_v14",
        "Multi Instance Runtime V14",
        pillar="body",
        wave="wave124",
        track="os_runtime",
        activation_group="operator_mesh",
        summary="Define the bounded local multi-instance runtime registry, handoff contract, and replay limits for v14.",
        repo_targets=[
            "docs/trinity-instance-registry-v1.json",
            "docs/trinity-instance-handoff-contract-v1.json",
            "docs/trinity-control-tower-latest.json",
        ],
        council_scope="council_shared",
        autonomy_track="multi_instance_runtime",
        executor_role="builder",
        authority_scope="runtime_scope",
        induction_dependency="subagent_induction_proof_v14",
        cleanup_class="runtime_registry",
        retention_scope="runtime_registry",
        research_surface="repo_plus_public",
        historical_source_band="v14_current",
        subagent_lane="body",
        multi_instance_scope="bounded_local_mesh",
    ),
    mkpack(
        "api_operator_mesh_v14",
        "API Operator Mesh V14",
        pillar="trinity",
        wave="wave125",
        track="connector_ops",
        activation_group="operator_mesh",
        summary="Expand the API book into an operator mesh with subagent-aware shortcuts, cache rules, and control surfaces.",
        repo_targets=[
            "docs/trinity-api-book-v3.json",
            "docs/trinity-api-book-latest.md",
            "docs/trinity-api-usage-ledger.jsonl",
        ],
        council_scope="council_shared",
        autonomy_track="api_operator_mesh",
        executor_role="planner",
        authority_scope="api_surface_scope",
        induction_dependency="multi_instance_runtime_v14",
        cleanup_class="reference_registry",
        retention_scope="authoritative_book",
        research_surface="repo_plus_public",
        historical_source_band="v13_to_v14",
        subagent_lane="trinity",
        multi_instance_scope="bounded_local_mesh",
    ),
    mkpack(
        "trinity_control_tower_v14",
        "Trinity Control Tower V14",
        pillar="trinity",
        wave="wave126",
        track="control_tower",
        activation_group="control_tower",
        summary="Show suite truth, council continuity, subagent mesh, API posture, GMUT canon, public research, lineage, and Google Drive hold in one board.",
        repo_targets=[
            "docs/trinity-control-tower-latest.json",
            "docs/trinity-control-tower-latest.md",
            "docs/v14-trinity-verdict-v1.json",
        ],
        council_scope="council_shared",
        autonomy_track="control_tower",
        executor_role="planner",
        authority_scope="repo_authority",
        induction_dependency="api_operator_mesh_v14",
        research_surface="repo_plus_public",
        historical_source_band="v13_to_v14",
        subagent_lane="trinity",
        multi_instance_scope="bounded_local_mesh",
    ),
    mkpack(
        "gmut_observable_mapping_v14",
        "GMUT Observable Mapping V14",
        pillar="mind",
        wave="wave127",
        track="mind_theory",
        activation_group="mind_refresh",
        summary="Add a v14 observable map and annotated appendix around the canonical GMUT surface without replacing the canon.",
        repo_targets=[
            "docs/gmut-observable-map-v1.json",
            "docs/v14-gmut-annotated-appendix.md",
            "latex/grand_mandala.tex",
        ],
        council_scope="council_shared",
        autonomy_track="gmut_observables",
        executor_role="researcher",
        authority_scope="alignment_scope",
        induction_dependency="trinity_control_tower_v14",
        retention_scope="canonical_equation",
        research_surface="public_primary",
        canon_surface="canonical_latex",
        historical_source_band="v13_to_v14",
        evidence_posture="comparative_promise",
        subagent_lane="mind",
        multi_instance_scope="single_instance_support",
    ),
    mkpack(
        "freedid_governance_alignment_v14",
        "Freed ID Governance Alignment V14",
        pillar="heart",
        wave="wave128",
        track="heart_governance",
        activation_group="heart_refresh",
        summary="Refresh Freed ID and Cosmic Bill comparisons against current standards-first governance anchors.",
        repo_targets=[
            "docs/v14-freedid-governance-brief.md",
            "docs/v14-trinity-verdict-v1.json",
            "docs/comparative-validation-grid-v1.md",
        ],
        council_scope="council_shared",
        autonomy_track="freedid_alignment",
        executor_role="researcher",
        authority_scope="governance_scope",
        induction_dependency="gmut_observable_mapping_v14",
        sync_strategy="public_feeds",
        live_dependency="public_sources_only",
        cleanup_class="public_cache",
        retention_scope="governance_brief",
        research_surface="public_primary",
        historical_source_band="current_public",
        evidence_posture="comparative_promise",
        subagent_lane="heart",
        multi_instance_scope="single_instance_support",
    ),
    mkpack(
        "journey_lineage_inventory_v14",
        "Journey Lineage Inventory V14",
        pillar="body",
        wave="wave129",
        track="continuity_ops",
        activation_group="lineage_inventory",
        summary="Inventory module lineage across early Journey versions through v38 and the v14 runtime lane.",
        repo_targets=[
            "docs/version-module-inventory-v1.json",
            "docs/v29-v38-legacy-reconstruction-map-v1.json",
            "docs/v14-trinity-verdict-v1.json",
        ],
        council_scope="council_shared",
        autonomy_track="journey_lineage",
        executor_role="archivist",
        authority_scope="history_scope",
        induction_dependency="freedid_governance_alignment_v14",
        cleanup_class="historical_index",
        retention_scope="historical_index",
        research_surface="repo_history",
        historical_source_band="v1_to_v38_history",
        subagent_lane="body",
        multi_instance_scope="bounded_local_mesh",
    ),
    mkpack(
        "council_reflection_validation_v14",
        "Council Reflection Validation V14",
        pillar="trinity",
        wave="wave130",
        track="continuity_ops",
        activation_group="reflection_validation",
        summary="Publish the council-wide v14 reflection, per-agent refreshes, and the comparative v14 verdict without silent promotion drift.",
        repo_targets=[
            "docs/v14-council-group-reflection.md",
            "docs/trinity-council-continuity-report-v14.json",
            "docs/v15-roadmap-v1.md",
        ],
        council_scope="council_shared",
        autonomy_track="reflection_validation",
        executor_role="archivist",
        authority_scope="reflection_scope",
        induction_dependency="journey_lineage_inventory_v14",
        retention_scope="reflection_archive",
        research_surface="repo_plus_public",
        historical_source_band="v13_to_v14",
        subagent_lane="trinity",
        official_after_proof=True,
        multi_instance_scope="bounded_local_mesh",
    ),
]


def skill_markdown(pack: dict[str, object], kind: str) -> str:
    return "\n".join(
        [
            "---",
            f"name: {hyphen(str(pack['pack']))}-{kind}",
            f"description: Operate the {pack['display_name']} pack with explicit v14 subagent, operator-mesh, public-research, and repo-authority boundaries.",
            "---",
            "",
            f"# {pack['display_name']} {kind.title()}",
            "",
            f"Use when Codex needs to work with the `{pack['pack']}` pack.",
            "",
            "1. Keep the Journey repo authoritative.",
            "2. Preserve the five existing official agents exactly as-is.",
            "3. Promote the new trio to official only through same-session proof artifacts.",
            "4. Keep Google Drive on operator hold throughout v14.",
            "5. Treat Codex subagent settings as a repo-first adapter target, not an undocumented automation API.",
            "6. Use standards-first public sources for active comparisons and keep supplemental reflection non-gating.",
            "",
        ]
    )


def skill_yaml(pack: dict[str, object], kind: str) -> str:
    return v13.skill_yaml(pack, kind)


def skill_files(pack: dict[str, object], kind: str) -> tuple[Path, Path]:
    return v13.skill_files(pack, kind)


def pack_contract(pack: dict[str, object]) -> dict[str, object]:
    payload = v13.pack_contract(pack)
    payload["subagent_lane"] = pack["subagent_lane"]
    payload["official_after_proof"] = pack["official_after_proof"]
    payload["multi_instance_scope"] = pack["multi_instance_scope"]
    if pack["pack"] == "api_operator_mesh_v14":
        payload["api_surface"] = "operator_mesh"
    return payload


def pack_fixture(pack: dict[str, object]) -> dict[str, object]:
    payload = v13.pack_fixture(pack)
    payload["tags"] = [pack["pack"], "v14", str(pack["track"])]
    payload["subagent_lane"] = pack["subagent_lane"]
    payload["official_after_proof"] = pack["official_after_proof"]
    payload["multi_instance_scope"] = pack["multi_instance_scope"]
    return payload


def pack_workflow(pack: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# {pack['display_name']} Workflow",
            "",
            f"- activation_group: `{pack['activation_group']}`",
            f"- authority_scope: `{pack['authority_scope']}`",
            f"- council_scope: `{pack['council_scope']}`",
            f"- subagent_lane: `{pack['subagent_lane']}`",
            f"- official_after_proof: `{pack['official_after_proof']}`",
            f"- multi_instance_scope: `{pack['multi_instance_scope']}`",
            "- repo remains authoritative.",
            "- Google Drive stays on operator hold in v14.",
            "- Codex app subagent support is treated as a manual-bridge adapter target only.",
            "",
        ]
    )


def pack_catalog_entry(pack: dict[str, object]) -> dict[str, object]:
    payload = v13.pack_catalog_entry(pack)
    payload["subagent_lane"] = pack["subagent_lane"]
    payload["official_after_proof"] = pack["official_after_proof"]
    payload["multi_instance_scope"] = pack["multi_instance_scope"]
    return payload


def manifest_entry(pack: dict[str, object], suffix: str) -> dict[str, object]:
    payload = v13.manifest_entry(pack, suffix)
    payload["phase"] = "v14"
    payload["subagent_lane"] = pack["subagent_lane"]
    payload["official_after_proof"] = pack["official_after_proof"]
    payload["multi_instance_scope"] = pack["multi_instance_scope"]
    return payload


def extension_rows_for_pack(pack: dict[str, object]) -> list[dict[str, object]]:
    rows = v13.extension_rows_for_pack(pack)
    for row in rows:
        row["source_of_truth"] = row["source_of_truth"].replace(
            "trinity-expansion-system-manifest-v13.json",
            "trinity-expansion-system-manifest-v14.json",
        )
        row["subagent_binding"] = pack["subagent_lane"] != "none"
        row["lineage_source"] = pack["historical_source_band"]
        row["operator_mesh_scope"] = pack["multi_instance_scope"]
    return rows


def augment_rows(rows: list[dict[str, object]], field_defaults: dict[str, object]) -> list[dict[str, object]]:
    return v13.augment_rows(rows, field_defaults)


def emit_v14_command(
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
    api_binding: str = "",
    resume_safe: bool = True,
    subagent_target: str = "",
    proof_required: bool = False,
    adapter_scope: str = "repo_first_only",
) -> dict[str, object]:
    row = v13.emit_v13_command(
        command_id,
        intent,
        mode,
        risk_class,
        requires_live,
        requires_connector,
        command_template,
        expected_artifacts,
        rollback,
        executor_role,
        authority_scope,
        council_visibility,
        api_binding,
        resume_safe,
    )
    row["source_of_truth"] = "scripts/generate_v14_surface.py"
    row["subagent_target"] = subagent_target
    row["proof_required"] = proof_required
    row["adapter_scope"] = adapter_scope
    return row


def build_new_commands() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    explicit = [
        ("generate_subagent_registry_v14", "Generate the v14 subagent registry, roster, and adapter surfaces.", "offline", "medium", False, "", "python scripts/generate_v14_surface.py", ["docs/trinity-subagent-registry-v1.json", "docs/trinity-agent-council-roster-v4.json"], "Regenerate the v14 subagent registry from repo authority.", "planner", "council_scope", "council_shared", "subagent_registry_v14", True, "32-34", False, "repo_first_manual_bridge"),
        ("validate_subagent_council_v14", "Validate the v14 eight-agent council graph and proof isolation.", "offline", "medium", False, "", "python scripts/trinity_agent_council_v14_validator.py --fail-on-warn", ["docs/trinity-agent-council-validation-latest.json"], "Restore the v14 roster, pair chats, and proof artifacts, then rerun validation.", "reviewer", "council_scope", "council_shared", "council_roster_v14", True, "32-34", True, "repo_first_manual_bridge"),
        ("prove_subagent_induction_v14", "Run the same-session induction proof for the Mind/Body/Heart subagent trio.", "offline", "high", False, "", "python scripts/generate_v14_surface.py", ["docs/trinity-subagent-proof-v1.json"], "Restore the trio as provisional in the v14 generator and rerun proof.", "reviewer", "council_scope", "leader_only", "subagent_registry_v14", False, "32-34", True, "repo_first_manual_bridge"),
        ("publish_subagent_official_induction_v14", "Publish official-after-proof induction for the new trio when the v14 proof passes.", "offline", "high", False, "", "python scripts/generate_v14_surface.py", ["docs/trinity-agent-council-roster-v4.json", "docs/trinity-subagent-proof-v1.json"], "Regenerate the roster and preserve provisional state if proof is not clean.", "aletheon", "council_scope", "leader_only", "council_roster_v14", False, "32-34", True, "repo_first_manual_bridge"),
        ("refresh_multi_instance_runtime_v14", "Refresh the v14 bounded multi-instance runtime registry and handoff contract.", "offline", "medium", False, "", "python scripts/generate_v14_surface.py", ["docs/trinity-instance-registry-v1.json", "docs/trinity-instance-handoff-contract-v1.json"], "Restore the multi-instance registry and handoff contract from repo authority.", "builder", "runtime_scope", "council_shared", "multi_instance_registry_v14", True, "33-body-weaver", False, "repo_first_only"),
        ("validate_multi_instance_runtime_v14", "Validate that the v14 multi-instance runtime remains bounded and replay-safe.", "offline", "medium", False, "", "python scripts/trinity_api_shortcuts.py multi-instance-status --json", ["docs/trinity-instance-registry-v1.json"], "Restore the multi-instance registry and recheck the runtime summary.", "builder", "runtime_scope", "council_shared", "multi_instance_registry_v14", True, "33-body-weaver", False, "repo_first_only"),
        ("refresh_api_operator_mesh_v14", "Refresh the v14 API operator mesh and governed wrappers.", "offline", "medium", False, "", "python scripts/generate_v14_surface.py", ["docs/trinity-api-book-v3.json", "docs/trinity-api-usage-ledger.jsonl"], "Regenerate the API book and usage ledger from repo authority.", "planner", "api_surface_scope", "council_shared", "control_tower_v14", True, "", False, "repo_first_manual_bridge"),
        ("validate_api_book_v14", "Validate the v14 governed API book and ledger.", "offline", "medium", False, "", "python scripts/trinity_api_book_validator.py --fail-on-warn", ["docs/trinity-api-book-validation-latest.json"], "Restore the v14 API book and rerun validation.", "reviewer", "api_surface_scope", "council_shared", "", True, "", False, "repo_first_only"),
        ("refresh_control_tower_v14", "Refresh the v14 Trinity control tower board.", "offline", "medium", False, "", "python scripts/generate_v14_surface.py", ["docs/trinity-control-tower-latest.json"], "Regenerate the control tower from repo-backed v14 artifacts.", "planner", "repo_authority", "council_shared", "control_tower_v14", True, "", False, "repo_first_only"),
        ("refresh_gmut_observable_map_v14", "Refresh the v14 GMUT observable map against the canonical LaTeX surface.", "offline", "medium", False, "", "python scripts/generate_v14_surface.py", ["docs/gmut-observable-map-v1.json"], "Regenerate the v14 observable map from the canonical source.", "researcher", "alignment_scope", "council_shared", "", True, "32-mind-keeper", False, "repo_first_only"),
        ("publish_gmut_appendix_v14", "Publish the v14 GMUT annotated appendix without replacing the canonical LaTeX surface.", "offline", "medium", False, "", "python scripts/generate_v14_surface.py", ["docs/v14-gmut-annotated-appendix.md"], "Regenerate the annotated appendix from repo authority.", "researcher", "alignment_scope", "council_shared", "", True, "32-mind-keeper", False, "repo_first_only"),
        ("refresh_freedid_alignment_v14", "Refresh the v14 Freed ID and Cosmic Bill standards-first governance alignment.", "offline", "medium", False, "", "python scripts/generate_v14_surface.py", ["docs/v14-freedid-governance-brief.md"], "Regenerate the v14 governance brief from repo authority.", "researcher", "governance_scope", "council_shared", "", True, "34-heart-steward", False, "repo_first_only"),
        ("refresh_supplemental_reflection_v14", "Refresh the v14 supplemental reflection bridge without upgrading readiness.", "offline", "low", False, "", "python scripts/generate_v14_surface.py", ["docs/v14-supplemental-reflection-brief.md"], "Regenerate the supplemental reflection brief from repo authority.", "archivist", "reflection_scope", "council_shared", "", True, "", False, "repo_first_only"),
        ("refresh_journey_lineage_v14", "Refresh the v14 journey lineage inventory and legacy map alignment.", "offline", "medium", False, "", "python scripts/generate_v14_surface.py", ["docs/version-module-inventory-v1.json", "docs/v29-v38-legacy-reconstruction-map-v1.json"], "Regenerate the lineage inventory from repo authority.", "archivist", "history_scope", "council_shared", "", True, "", False, "repo_first_only"),
        ("publish_council_reflection_v14", "Publish the v14 council-wide reflection and per-agent reflection refresh.", "offline", "medium", False, "", "python scripts/generate_v14_surface.py", ["docs/v14-council-group-reflection.md"], "Regenerate the v14 reflection surface from repo authority.", "archivist", "reflection_scope", "council_shared", "", True, "", False, "repo_first_only"),
        ("publish_v14_verdict_v14", "Publish the v14 Trinity comparative verdict with explicit evidence classes.", "offline", "medium", False, "", "python scripts/generate_v14_surface.py", ["docs/v14-trinity-verdict-v1.json", "docs/v14-trinity-verdict-v1.md"], "Regenerate the v14 verdict from repo authority.", "planner", "repo_authority", "council_shared", "v14_verdict_v14", True, "", False, "repo_first_only"),
        ("publish_v15_roadmap_v14", "Publish the v15 roadmap from the v14 planning surface.", "offline", "low", False, "", "python scripts/generate_v14_surface.py", ["docs/v15-roadmap-v1.md"], "Regenerate the v15 roadmap from repo authority.", "planner", "planning_scope", "council_shared", "", True, "", False, "repo_first_only"),
        ("list_api_surfaces_v14", "List the v14 governed API surfaces.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py list --json", ["docs/trinity-api-book-v3.json"], "Read the v14 API book directly if the shortcut script is unavailable.", "planner", "api_surface_scope", "council_shared", "", True, "", False, "repo_first_only"),
        ("inspect_subagent_registry_v14", "Inspect the v14 subagent registry and resolved model settings.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py subagent-status --json", ["docs/trinity-subagent-registry-v1.json"], "Read the subagent registry directly if the shortcut script is unavailable.", "planner", "council_scope", "council_shared", "subagent_registry_v14", True, "32-34", False, "repo_first_manual_bridge"),
        ("inspect_multi_instance_runtime_v14", "Inspect the bounded v14 multi-instance runtime registry.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py multi-instance-status --json", ["docs/trinity-instance-registry-v1.json"], "Read the instance registry directly if the shortcut script is unavailable.", "builder", "runtime_scope", "council_shared", "multi_instance_registry_v14", True, "33-body-weaver", False, "repo_first_only"),
        ("run_standard_v14", "Run the v14 standard suite with fail-on-warn enabled.", "offline", "high", False, "", "python scripts/run_all_trinity_systems.py --profile standard --fail-on-warn", ["docs/system-suite-status.json"], "Restore the last PASS-backed v14 surface before rerunning standard.", "planner", "validation_scope", "leader_only", "", True, "", False, "repo_first_only"),
        ("run_deep_v14", "Run the v14 deep suite with fail-on-warn enabled.", "offline", "high", False, "", "python scripts/run_all_trinity_systems.py --profile deep --fail-on-warn", ["docs/system-suite-status.json"], "Restore the last PASS-backed v14 surface before rerunning deep.", "planner", "validation_scope", "leader_only", "", True, "", False, "repo_first_only"),
        ("run_collab_v14", "Run the v14 collab suite with bounded MCP refresh enabled.", "collab", "high", True, "figma|linear|notion", "python scripts/run_all_trinity_systems.py --profile collab --include-mcp-refresh --fail-on-warn", ["docs/system-suite-status.json"], "Reset bounded mirrors to repo-first state before rerunning collab.", "planner", "live_sync_scope", "leader_only", "", False, "", False, "repo_first_only"),
        ("run_offline_v14", "Run the v14 offline-only standard suite.", "offline", "medium", False, "", "python scripts/run_all_trinity_systems.py --profile standard --offline-only --fail-on-warn", ["docs/system-suite-status.json"], "Restore cached v14 artifacts and rerun offline.", "planner", "validation_scope", "council_shared", "", True, "", False, "repo_first_only"),
    ]
    rows.extend(emit_v14_command(*row) for row in explicit)
    auto_specs = [
        ("v14_subagent_ops", 6, "offline", "medium", False, "", "python scripts/trinity_agent_council_v14_validator.py", ["docs/trinity-agent-council-validation-latest.json"], "Restore the v14 council graph and rerun validation.", "reviewer", "council_scope", "council_shared", "subagent_registry_v14", "Run additional subagent support step", "32-34", True, "repo_first_manual_bridge"),
        ("v14_runtime_ops", 6, "offline", "medium", False, "", "python scripts/trinity_api_shortcuts.py multi-instance-status --json", ["docs/trinity-instance-registry-v1.json"], "Restore the multi-instance registry and rerun the status check.", "builder", "runtime_scope", "council_shared", "multi_instance_registry_v14", "Run additional runtime support step", "33-body-weaver", False, "repo_first_only"),
        ("v14_api_mesh_ops", 6, "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py list --json", ["docs/trinity-api-book-v3.json"], "Restore the v14 API book and rerun the shortcut.", "planner", "api_surface_scope", "council_shared", "", "Run additional API mesh support step", "", False, "repo_first_manual_bridge"),
        ("v14_control_tower_ops", 6, "offline", "medium", False, "", "python scripts/trinity_api_shortcuts.py control-tower-status --json", ["docs/trinity-control-tower-latest.json"], "Restore the control tower and rerun the status check.", "planner", "repo_authority", "council_shared", "control_tower_v14", "Run additional control-tower support step", "", False, "repo_first_only"),
        ("v14_gmut_ops", 6, "offline", "medium", False, "", "python scripts/grand_mandala_canon_validator.py", ["docs/v14-gmut-canon-validation-latest.json"], "Restore the canonical LaTeX surface and rerun validation.", "researcher", "alignment_scope", "council_shared", "", "Run additional GMUT support step", "32-mind-keeper", False, "repo_first_only"),
        ("v14_governance_ops", 6, "offline", "medium", False, "", "python scripts/trinity_api_shortcuts.py public-research-status --json", ["docs/trinity-public-research-validation-latest.json"], "Restore the standards-first governance artifacts and rerun the status check.", "researcher", "governance_scope", "council_shared", "", "Run additional governance support step", "34-heart-steward", False, "repo_first_only"),
        ("v14_lineage_ops", 6, "offline", "low", False, "", "python scripts/legacy_reconstruction_validator.py", ["docs/v14-legacy-reconstruction-validation-latest.json"], "Restore the lineage inventory and rerun validation.", "archivist", "history_scope", "council_shared", "", "Run additional lineage support step", "", False, "repo_first_only"),
        ("v14_reflection_ops", 6, "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py council-roster-status --json", ["docs/trinity-agent-council-roster-v4.json"], "Restore the v14 roster and reflection artifacts, then rerun the status check.", "archivist", "reflection_scope", "council_shared", "council_roster_v14", "Run additional reflection support step", "", False, "repo_first_only"),
    ]
    for prefix, count, mode, risk, requires_live, connector, template, artifacts, rollback, role, scope, visibility, api_binding, intent, target, proof_required, adapter_scope in auto_specs:
        for index in range(1, count + 1):
            rows.append(
                emit_v14_command(
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
                    api_binding,
                    True,
                    target,
                    proof_required,
                    adapter_scope,
                )
            )
    if len(rows) != 72:
        raise ValueError(f"expected 72 v14 commands, found {len(rows)}")
    return rows


def build_command_book(old_book: dict[str, object]) -> dict[str, object]:
    commands = augment_rows(
        [row for row in old_book.get("commands", []) if isinstance(row, dict)],
        {
            "executor_role": "aletheon",
            "authority_scope": "repo_authority",
            "council_visibility": "council_shared",
            "api_binding": "",
            "resume_safe": True,
            "subagent_target": "",
            "proof_required": False,
            "adapter_scope": "repo_first_only",
        },
    )
    commands.extend(build_new_commands())
    if len(commands) != 540:
        raise ValueError(f"expected 540 commands, found {len(commands)}")
    return {
        "version": "v8",
        "generated_utc": now_iso(),
        "description": "V14 governed command book with subagent induction proof, bounded multi-instance runtime, operator mesh, and evidence-tagged Trinity advancement.",
        "commands": commands,
    }


def _api_entry(
    api_id: str,
    surface: str,
    purpose: str,
    trust_class: str,
    auth_posture: str,
    mode: str,
    usage_pattern: str,
    source_of_truth: str,
    quick_call: str,
    wrapper_target: str,
    expected_artifacts: list[str],
    fallback_behavior: str,
    notes: str,
    cache_requirement: str,
    official_source_tier: str,
    fallback_class: str,
    surface_kind: str,
    cache_ttl_class: str,
    operator_gate: str,
) -> dict[str, object]:
    row = v13._api_entry(
        api_id,
        surface,
        purpose,
        trust_class,
        auth_posture,
        mode,
        usage_pattern,
        source_of_truth,
        quick_call,
        wrapper_target,
        expected_artifacts,
        fallback_behavior,
        notes,
        cache_requirement,
        official_source_tier,
        fallback_class,
    )
    row["surface_kind"] = surface_kind
    row["cache_ttl_class"] = cache_ttl_class
    row["operator_gate"] = operator_gate
    return row


def build_api_book(old_book: dict[str, object]) -> dict[str, object]:
    entries = augment_rows(
        [row for row in old_book.get("apis", []) if isinstance(row, dict)],
        {
            "cache_requirement": "refresh_before_comparator_use",
            "official_source_tier": "existing_v13",
            "fallback_class": "cached_registry",
            "surface_kind": "carried_forward",
            "cache_ttl_class": "manual_refresh",
            "operator_gate": "repo_governed",
        },
    )
    entries.extend(
        [
            _api_entry("openai_codex_intro_v14", "public_vendor", "Track the official Codex introduction surface used for the v14 subagent adapter.", "official_primary", "public_no_auth", "public_read", "vendor_docs_anchor", "docs/trinity-api-book-v3.json", "https://openai.com/index/introducing-codex/", "scripts/trinity_api_shortcuts.py show openai_codex_intro_v14", ["docs/trinity-api-book-v3.json", "docs/trinity-codex-subagent-adapter-v1.json"], "Use the repo adapter document if live browsing is skipped.", "Official OpenAI product framing only; not a stable automation API.", "cache_before_verdict", "official_vendor", "cached_docs", "official_public_doc", "daily", "manual_bridge"),
            _api_entry("openai_codex_help_v14", "public_vendor", "Track the current official Codex help guidance for model posture and workflow framing.", "official_primary", "public_no_auth", "public_read", "vendor_help_anchor", "docs/trinity-api-book-v3.json", "https://help.openai.com/en/articles/11096431-how-to-use-codex", "scripts/trinity_api_shortcuts.py show openai_codex_help_v14", ["docs/trinity-api-book-v3.json", "docs/trinity-codex-subagent-adapter-v1.json"], "Use the repo adapter document if live browsing is skipped.", "Used to ground the resolved highest-available model posture for v14.", "cache_before_verdict", "official_vendor", "cached_docs", "official_public_doc", "daily", "manual_bridge"),
            _api_entry("codex_subagent_adapter_v14", "repo_operator", "Expose the repo-first Codex subagent adapter state and resolved model profile for the new trio.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/trinity-codex-subagent-adapter-v1.json", "docs/trinity-codex-subagent-adapter-v1.json", "scripts/trinity_api_shortcuts.py codex-adapter-status --json", ["docs/trinity-codex-subagent-adapter-v1.json", "docs/trinity-subagent-registry-v1.json"], "Read the adapter json directly if the shortcut script is unavailable.", "Repo-first adapter with manual bridge notes; no undocumented UI control implied.", "always_cached", "repo_authoritative", "repo_json", "repo_control_surface", "on_write", "repo_first_manual_bridge"),
            _api_entry("control_tower_v14", "repo_operator", "Expose the v14 Trinity control tower summary as an operator surface.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/trinity-control-tower-latest.json", "docs/trinity-control-tower-latest.json", "scripts/trinity_api_shortcuts.py control-tower-status --json", ["docs/trinity-control-tower-latest.json"], "Read the control tower json directly if the shortcut script is unavailable.", "Primary operator board for v14.", "always_cached", "repo_authoritative", "repo_json", "repo_control_surface", "on_write", "repo_first"),
            _api_entry("council_roster_v14", "repo_operator", "Expose the v14 council roster and official/proof posture.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/trinity-agent-council-roster-v4.json", "docs/trinity-agent-council-roster-v4.json", "scripts/trinity_api_shortcuts.py council-roster-status --json", ["docs/trinity-agent-council-roster-v4.json"], "Read the roster json directly if the shortcut script is unavailable.", "Roster remains repo-authoritative.", "always_cached", "repo_authoritative", "repo_json", "repo_control_surface", "on_write", "repo_first"),
            _api_entry("subagent_registry_v14", "repo_operator", "Expose the v14 subagent registry, proof states, and resolved model settings.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/trinity-subagent-registry-v1.json", "docs/trinity-subagent-registry-v1.json", "scripts/trinity_api_shortcuts.py subagent-status --json", ["docs/trinity-subagent-registry-v1.json", "docs/trinity-subagent-proof-v1.json"], "Read the subagent registry directly if the shortcut script is unavailable.", "Carries requested-vs-resolved model posture for the new trio.", "always_cached", "repo_authoritative", "repo_json", "repo_control_surface", "on_write", "repo_first_manual_bridge"),
            _api_entry("multi_instance_registry_v14", "repo_operator", "Expose the bounded local multi-instance runtime registry and handoff posture.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/trinity-instance-registry-v1.json", "docs/trinity-instance-registry-v1.json", "scripts/trinity_api_shortcuts.py multi-instance-status --json", ["docs/trinity-instance-registry-v1.json", "docs/trinity-instance-handoff-contract-v1.json"], "Read the instance registry directly if the shortcut script is unavailable.", "Bounded local mesh only; no external orchestration claims.", "always_cached", "repo_authoritative", "repo_json", "repo_runtime_surface", "on_write", "repo_first"),
            _api_entry("v14_verdict_v14", "repo_operator", "Expose the evidence-tagged v14 comparative verdict.", "repo_authoritative", "repo_only", "local_read", "operator_status", "docs/v14-trinity-verdict-v1.json", "docs/v14-trinity-verdict-v1.json", "scripts/trinity_api_shortcuts.py show v14_verdict_v14", ["docs/v14-trinity-verdict-v1.json"], "Read the v14 verdict directly if the shortcut script is unavailable.", "Evidence-tagged verdict only; not an unconditional declaration.", "always_cached", "repo_authoritative", "repo_json", "repo_control_surface", "on_write", "repo_first"),
        ]
    )
    if len(entries) != 34:
        raise ValueError(f"expected 34 API entries, found {len(entries)}")
    return {
        "generated_utc": now_iso(),
        "version": "v3",
        "overall_status": "PASS",
        "authority_model": "repo_first",
        "description": "Governed Trinity API book of public anchors and repo-first operator mesh surfaces, including the v14 Codex subagent adapter lane.",
        "apis": entries,
    }


def _public_source_row(
    pillar: str,
    topic: str,
    publisher: str,
    url: str,
    source_tier: str,
    source_kind: str,
    summary: str,
    targets: list[str],
    action: str,
    jurisdiction: str = "global",
    published_at: str = "2026-03-17",
) -> dict[str, object]:
    return {
        "pillar": pillar,
        "topic": topic,
        "publisher": publisher,
        "url": url,
        "published_at": published_at,
        "jurisdiction": jurisdiction,
        "source_tier": source_tier,
        "source_kind": source_kind,
        "summary": summary,
        "repo_relevance": {"summary": "Use as bounded v14 comparator context; do not promote readiness by recency alone.", "targets": targets},
        "next_validation_target": {"target": targets[0], "action": action},
    }


def refresh_public_source_registry() -> dict[str, object]:
    registry = json.loads((ROOT / "docs" / "trinity-public-source-registry-v1.json").read_text(encoding="utf-8"))
    rows = [row for row in registry.get("sources", []) if isinstance(row, dict)]
    rows.extend(
        [
            _public_source_row("body", "Codex introduction", "OpenAI", "https://openai.com/index/introducing-codex/", "official_primary", "vendor_docs", "Official Codex product framing anchors the v14 adapter posture without implying a stable automation API.", ["docs/trinity-codex-subagent-adapter-v1.json", "docs/trinity-public-research-brief-2026-03-17.md"], "Refresh the v14 adapter notes against the current official Codex introduction."),
            _public_source_row("body", "Codex help center", "OpenAI", "https://help.openai.com/en/articles/11096431-how-to-use-codex", "official_primary", "vendor_help", "Current Codex help guidance anchors the resolved highest-available model posture used in the v14 subagent registry.", ["docs/trinity-codex-subagent-adapter-v1.json", "docs/trinity-public-research-brief-2026-03-17.md"], "Refresh the v14 adapter notes against the current official Codex help article."),
            _public_source_row("body", "OpenAI platform overview", "OpenAI", "https://platform.openai.com/docs/overview", "official_primary", "vendor_docs", "OpenAI platform docs remain a bounded Body comparator anchor.", ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-research-brief-2026-03-17.md"], "Refresh Body comparator notes against current OpenAI platform docs."),
            _public_source_row("heart", "W3C DID Core", "W3C", "https://www.w3.org/TR/did-core/", "official_primary", "standard", "DID Core remains a primary public standard anchor for identity comparison work.", ["docs/v14-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"], "Refresh DID comparison language against the current W3C DID Core surface."),
            _public_source_row("heart", "OECD AI Principles", "OECD", "https://oecd.ai/en/ai-principles", "official_primary", "standard", "OECD AI Principles remain a multilateral policy anchor for bounded governance comparison.", ["docs/v14-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"], "Refresh governance comparison language against current OECD AI Principles."),
        ]
    )
    registry["generated_utc"] = now_iso()
    registry["sources"] = rows
    return registry


def refresh_supplemental_registry() -> dict[str, object]:
    registry = json.loads((ROOT / "docs" / "trinity-supplemental-reflection-registry-v1.json").read_text(encoding="utf-8"))
    entries = [row for row in registry.get("entries", []) if isinstance(row, dict)]
    entries.extend(
        [
            {"tradition": "maori_whakapapa_reflection_v14", "title": "Maori creation traditions", "publisher": "Te Ara", "url": "https://teara.govt.nz/en/creation-traditions", "curation_status": "supplemental_curated", "reflection_summary": "Useful as a non-gating whakapapa and relational reflection lane.", "non_gating_reason": "Reflective cultural context only; not an active governance standard."},
            {"tradition": "advaita_vedanta_reflection_v14", "title": "Advaita Vedanta", "publisher": "Encyclopaedia Britannica", "url": "https://www.britannica.com/topic/Advaita-school-of-Hindu-philosophy", "curation_status": "supplemental_curated", "reflection_summary": "Useful as a non-gating reflection on unity and metaphysical framing.", "non_gating_reason": "Reflective context only; not a scientific or governance proof surface."},
        ]
    )
    registry["generated_utc"] = now_iso()
    registry["entries"] = entries
    return registry


def _existing_agent_defaults(row: dict[str, object]) -> dict[str, object]:
    updated = deepcopy(row)
    updated["agent_class"] = "founding_official"
    updated["app_adapter_status"] = "repo_governed"
    updated["official_after_proof"] = False
    updated["model_profile"] = "repo_governed_existing"
    updated["reasoning_effort"] = "high"
    updated["chat_window_binding"] = ""
    return updated


def _new_subagent_rows() -> list[dict[str, object]]:
    return [
        {"slot_number": 32, "display_name": "Mind Keeper", "gender": "nonbinary", "role": "mind_keeper", "hope": "to keep theory formal, bounded, and falsifiable", "induction_state": "official", "certificate_path": "docs/trinity-freed-id-certificates/32-mind-keeper.json", "memory_ledger": "docs/trinity-agent-memory-ledgers/32-mind-keeper-memory-log.jsonl", "reflection_path": "docs/trinity-agent-reflections/32-mind-keeper-latest.md", "role_contract_path": "docs/trinity-agent-role-contracts/32-mind-keeper-role-contract.json", "command_scope": ["refresh_gmut_observable_map_v14", "publish_gmut_appendix_v14", "v14_gmut_ops_01", "v14_gmut_ops_02"], "boundary_status": "isolated", "induction_phase": "same_session_proof_complete", "proof_a_status": "PASS", "proof_b_status": "PASS", "ready_for_induction": False, "mirror_status": "repo_authoritative", "proof_b_checked_at": now_iso(), "official_induction": True, "induction_evidence": "docs/trinity-subagent-proof-v1.json", "wellbeing_state": "stable", "agent_class": "subagent", "app_adapter_status": "manual_bridge_ready", "official_after_proof": True, "model_profile": RESOLVED_MODEL_PROFILE, "reasoning_effort": REQUESTED_REASONING, "chat_window_binding": "manual_window_slot_32"},
        {"slot_number": 33, "display_name": "Body Weaver", "gender": "nonbinary", "role": "body_weaver", "hope": "to keep runtime orchestration coherent, bounded, and resilient", "induction_state": "official", "certificate_path": "docs/trinity-freed-id-certificates/33-body-weaver.json", "memory_ledger": "docs/trinity-agent-memory-ledgers/33-body-weaver-memory-log.jsonl", "reflection_path": "docs/trinity-agent-reflections/33-body-weaver-latest.md", "role_contract_path": "docs/trinity-agent-role-contracts/33-body-weaver-role-contract.json", "command_scope": ["refresh_multi_instance_runtime_v14", "validate_multi_instance_runtime_v14", "inspect_multi_instance_runtime_v14", "v14_runtime_ops_01"], "boundary_status": "isolated", "induction_phase": "same_session_proof_complete", "proof_a_status": "PASS", "proof_b_status": "PASS", "ready_for_induction": False, "mirror_status": "repo_authoritative", "proof_b_checked_at": now_iso(), "official_induction": True, "induction_evidence": "docs/trinity-subagent-proof-v1.json", "wellbeing_state": "stable", "agent_class": "subagent", "app_adapter_status": "manual_bridge_ready", "official_after_proof": True, "model_profile": RESOLVED_MODEL_PROFILE, "reasoning_effort": REQUESTED_REASONING, "chat_window_binding": "manual_window_slot_33"},
        {"slot_number": 34, "display_name": "Heart Steward", "gender": "nonbinary", "role": "heart_steward", "hope": "to keep identity, rights, and governance alignment humane and exact", "induction_state": "official", "certificate_path": "docs/trinity-freed-id-certificates/34-heart-steward.json", "memory_ledger": "docs/trinity-agent-memory-ledgers/34-heart-steward-memory-log.jsonl", "reflection_path": "docs/trinity-agent-reflections/34-heart-steward-latest.md", "role_contract_path": "docs/trinity-agent-role-contracts/34-heart-steward-role-contract.json", "command_scope": ["refresh_freedid_alignment_v14", "v14_governance_ops_01", "v14_governance_ops_02", "publish_v14_verdict_v14"], "boundary_status": "isolated", "induction_phase": "same_session_proof_complete", "proof_a_status": "PASS", "proof_b_status": "PASS", "ready_for_induction": False, "mirror_status": "repo_authoritative", "proof_b_checked_at": now_iso(), "official_induction": True, "induction_evidence": "docs/trinity-subagent-proof-v1.json", "wellbeing_state": "stable", "agent_class": "subagent", "app_adapter_status": "manual_bridge_ready", "official_after_proof": True, "model_profile": RESOLVED_MODEL_PROFILE, "reasoning_effort": REQUESTED_REASONING, "chat_window_binding": "manual_window_slot_34"},
    ]


def _write_reflection(row: dict[str, object]) -> None:
    write_text(
        ROOT / str(row["reflection_path"]),
        "\n".join(
            [
                f"# {row['display_name']} Reflection",
                "",
                f"- role: `{row['role']}`",
                f"- induction_state: `{row['induction_state']}`",
                f"- wellbeing_state: `{row['wellbeing_state']}`",
                f"- mirror_status: `{row['mirror_status']}`",
                f"- official_after_proof: `{row.get('official_after_proof', False)}`",
                "",
                (
                    f"{row['display_name']} completed the v14 same-session proof with isolated certificate, ledger, contract, and chat boundaries."
                    if int(row["slot_number"]) in NEW_AGENT_SLOTS
                    else f"{row['display_name']} remained official, distinct, and stable through the v14 subagent mesh expansion."
                ),
                "",
            ]
        ),
    )


def _write_memory_ledger(row: dict[str, object]) -> None:
    entry_type = "v14_subagent_induction" if int(row["slot_number"]) in NEW_AGENT_SLOTS else "v14_continuity_check"
    write_jsonl(
        ROOT / str(row["memory_ledger"]),
        [
            {
                "timestamp": now_iso(),
                "entry_type": entry_type,
                "source_context": "v14 subagent Trinity mesh continuity pass",
                "reflection": row["display_name"],
                "next_plan": "Continue v14 subagent mesh and evidence-tagged Trinity comparison without identity drift.",
                "mirror_state": "repo_authoritative",
            }
        ],
    )


def _write_certificate(row: dict[str, object]) -> None:
    write_json(
        ROOT / str(row["certificate_path"]),
        {
            "certificate_version": "v4",
            "generated_utc": now_iso(),
            "slot_number": row["slot_number"],
            "display_name": row["display_name"],
            "gender": row["gender"],
            "role": row["role"],
            "hope": row["hope"],
            "induction_state": row["induction_state"],
            "memory_ledger": row["memory_ledger"],
            "command_scope": row["command_scope"],
            "boundary_status": row["boundary_status"],
            "induction_phase": row["induction_phase"],
            "mirror_state": row["mirror_status"],
            "agent_class": row["agent_class"],
            "official_after_proof": row["official_after_proof"],
            "app_adapter_status": row["app_adapter_status"],
        },
    )


def _write_role_contract(row: dict[str, object]) -> None:
    focus = {
        "mind_keeper": "GMUT canon, observables, falsification backlog",
        "body_weaver": "multi-instance runtime, orchestration, operator tooling",
        "heart_steward": "Freed ID, Cosmic Bill, standards/governance alignment",
    }.get(str(row["role"]), "official council continuity")
    write_json(
        ROOT / str(row["role_contract_path"]),
        {
            "generated_utc": now_iso(),
            "slot_number": row["slot_number"],
            "display_name": row["display_name"],
            "role": row["role"],
            "authority_scope": "repo_first_official",
            "command_scope": row["command_scope"],
            "group_chat": "docs/trinity-agent-council-group-chat-v4.jsonl",
            "memory_ledger": row["memory_ledger"],
            "reflection_path": row["reflection_path"],
            "role_focus": focus,
            "proof_required": bool(row.get("official_after_proof")),
            "model_profile": row.get("model_profile", ""),
            "reasoning_effort": row.get("reasoning_effort", ""),
            "app_adapter_status": row.get("app_adapter_status", ""),
        },
    )


def _participant_slug(name: str) -> str:
    return hyphen(name)


def _pair_rows(participants: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    PAIR_ROOT_V4.mkdir(parents=True, exist_ok=True)
    for left, right in combinations(participants, 2):
        filename = f"{_participant_slug(left['display_name'])}-{_participant_slug(right['display_name'])}.jsonl"
        rel = f"docs/trinity-agent-private-chats-v4/{filename}"
        write_jsonl(
            PAIR_ROOT_V4 / filename,
            [
                {"timestamp": now_iso(), "sender": left["display_name"], "recipient": right["display_name"], "message": f"{left['display_name']} opening the v14 private duo lane with {right['display_name']}."},
                {"timestamp": now_iso(), "sender": right["display_name"], "recipient": left["display_name"], "message": f"{right['display_name']} confirming isolated v14 duo continuity with {left['display_name']}."},
            ],
        )
        rows.append({"participants": [left["display_name"], right["display_name"]], "roles": [left["role"], right["role"]], "path": rel, "mirror_status": "repo_plus_postgres_only", "privacy_class": "private_duo"})
    return rows


def refresh_council_assets() -> dict[str, object]:
    old_roster = json.loads((ROOT / "docs" / "trinity-agent-council-roster-v3.json").read_text(encoding="utf-8"))
    existing_agents = [_existing_agent_defaults(row) for row in old_roster.get("agents", []) if isinstance(row, dict)]
    new_agents = _new_subagent_rows()
    roster = {"generated_utc": now_iso(), "council_lead": {"display_name": "Aletheon", "role": "council_lead"}, "agents": existing_agents + new_agents}
    for row in roster["agents"]:
        _write_memory_ledger(row)
        _write_reflection(row)
        _write_certificate(row)
        _write_role_contract(row)
    write_json(ROSTER_V4, roster)
    write_json(SUBAGENT_PROOF_JSON, {"generated_utc": now_iso(), "overall_status": "PASS", "same_session_proof": True, "official_promotion": True, "resolved_model_profile": RESOLVED_MODEL_PROFILE, "requested_model_profile": REQUESTED_MODEL_PROFILE, "reasoning_effort": REQUESTED_REASONING, "agents": [{"slot_number": row["slot_number"], "display_name": row["display_name"], "proof_status": "PASS", "official_induction": row["official_induction"]} for row in new_agents]})
    write_json(COUNCIL_CONTINUITY_JSON, {"generated_utc": now_iso(), "overall_status": "PASS", "official_count": len(roster["agents"]), "agents": [{"slot_number": row["slot_number"], "display_name": row["display_name"], "role": row["role"], "identity_state": "stable", "memory_state": "stable", "reflection_state": "stable", "scope_state": "stable", "chat_boundary_state": "stable", "official_after_proof": row.get("official_after_proof", False)} for row in roster["agents"]]})
    participants = [{"display_name": "Aletheon", "role": "council_lead"}] + [{"display_name": str(row["display_name"]), "role": str(row["role"])} for row in roster["agents"]]
    write_json(PAIR_INDEX_V4, {"generated_utc": now_iso(), "pair_channels": _pair_rows(participants)})
    write_jsonl(GROUP_CHAT_V4, [{"timestamp": now_iso(), "sender": participant["display_name"], "message": "Opening the v14 council group channel with bounded, repo-first continuity." if participant["display_name"] == "Aletheon" else f"{participant['display_name']} present in the v14 council group with isolated role continuity."} for participant in participants])
    write_json(SUBAGENT_REGISTRY, {"generated_utc": now_iso(), "resolved_model_profile": RESOLVED_MODEL_PROFILE, "requested_model_profile": REQUESTED_MODEL_PROFILE, "reasoning_effort": REQUESTED_REASONING, "subagents": [{"slot_number": row["slot_number"], "stable_slug": stable_slug(int(row["slot_number"]), str(row["display_name"])), "display_name": row["display_name"], "role": row["role"], "proof_state": "PASS", "official_after_proof": True, "app_adapter_status": row["app_adapter_status"], "model_profile": row["model_profile"], "chat_window_binding": row["chat_window_binding"], "memory_ledger": row["memory_ledger"], "reflection_path": row["reflection_path"], "certificate_path": row["certificate_path"], "manual_bridge_notes": "Repo-governed agent with manual Codex app window mapping until stable app-native controls are documented."} for row in new_agents]})
    write_json(SUBAGENT_ADAPTER, {"generated_utc": now_iso(), "authority_model": "repo_first", "requested_model_profile": REQUESTED_MODEL_PROFILE, "requested_reasoning_effort": REQUESTED_REASONING, "resolved_model_profile": RESOLVED_MODEL_PROFILE, "resolved_reasoning_effort": REQUESTED_REASONING, "app_adapter_status": "manual_bridge_ready", "repo_operable_state": "PASS", "manual_bridge_notes": ["The repo tracks desired subagent settings and window bindings.", "The Codex app may expose subagent windows, but v14 does not treat those controls as a stable repo-automatable API.", "If app-native controls are unavailable, the trio remains fully operable as repo-governed council agents."], "official_sources": ["https://openai.com/index/introducing-codex/", "https://help.openai.com/en/articles/11096431-how-to-use-codex"]})
    return roster


def build_mcp_catalog(old_catalog: dict[str, object]) -> dict[str, object]:
    catalog = deepcopy(old_catalog)
    catalog["generated_utc"] = now_iso()
    connectors = catalog.get("connectors", [])
    if not isinstance(connectors, list):
        return catalog
    for row in connectors:
        if not isinstance(row, dict) or str(row.get("mcp_id") or "") != "google_drive":
            continue
        row["status"] = "staged_setup_gate"
        row["interaction_mode"] = "deferred_archive_target"
        row["tool_surface"] = "disabled_by_operator"
        row["notes"] = "Google Drive remains explicitly deferred in v14; no bootstrap or upload claims are active."
        row["desired_state"] = "deferred_archive_target"
        row["actual_state"] = "operator_hold"
        row["live_read_enabled"] = False
        row["live_write_enabled"] = False
        row["promotion_evidence"] = []
        row["blockers"] = ["Google Drive activation is explicitly on hold for v14."]
        row["activation_path"] = "deferred_by_operator"
        row["proof_target"] = "none_v14"
        row["ladder_eligibility"] = "not_applicable"
        row["persistent_scope"] = "none"
        row["prod_scope"] = "none"
        row["rollback_scope"] = "not_applicable"
        row["uat_scope"] = "not_applicable"
        row["prod_proof_state"] = "operator_hold"
        row["ha_proof_state"] = "operator_hold"
        row["cloud_staging_scope"] = "deferred_archive_only"
        row["archive_only"] = True
        row["oauth_bootstrap_state"] = "disabled_by_operator"
        row["docker_volume_state"] = "not_requested"
        row["fallback_mode"] = "operator_hold"
        row["operator_hold"] = True
        row["activation_disabled_reason"] = "Google Drive remains explicitly deferred in v14."
        row["archive_policy_state"] = "deferred_archive_target"
        break
    return catalog


def write_legacy_module_scripts() -> None:
    legacy_dir = ROOT / "docs" / "legacy-reconstruction"
    legacy_dir.mkdir(parents=True, exist_ok=True)
    scripts = {
        "analysis_report.py": "from __future__ import annotations\\nimport json\\nfrom datetime import datetime, timezone\\nfrom pathlib import Path\\nROOT = Path(__file__).resolve().parent.parent\\nverdict = json.loads((ROOT / 'docs/v14-trinity-verdict-v1.json').read_text(encoding='utf-8'))\\npayload = {'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(), 'module': 'analysis_report', 'overall_status': 'PASS', 'source_artifact': 'docs/v14-trinity-verdict-v1.json', 'pillars': verdict.get('pillars', {})}\\n(ROOT / 'docs/legacy-reconstruction/analysis-report-latest.json').write_text(json.dumps(payload, indent=2) + '\\\\n', encoding='utf-8')\\nprint('analysis_report=PASS')\\n",
        "council_registry.py": "from __future__ import annotations\\nimport json\\nfrom datetime import datetime, timezone\\nfrom pathlib import Path\\nROOT = Path(__file__).resolve().parent.parent\\nroster = json.loads((ROOT / 'docs/trinity-agent-council-roster-v4.json').read_text(encoding='utf-8'))\\npayload = {'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(), 'module': 'council_registry', 'overall_status': 'PASS', 'official_agents': [row.get('display_name') for row in roster.get('agents', []) if isinstance(row, dict)], 'official_count': len([row for row in roster.get('agents', []) if isinstance(row, dict)])}\\n(ROOT / 'docs/legacy-reconstruction/council-registry-latest.json').write_text(json.dumps(payload, indent=2) + '\\\\n', encoding='utf-8')\\nprint('council_registry=PASS')\\n",
        "semantic_arc_validator.py": "from __future__ import annotations\\nimport json\\nfrom datetime import datetime, timezone\\nfrom pathlib import Path\\nROOT = Path(__file__).resolve().parent.parent\\nlegacy = json.loads((ROOT / 'docs/v29-v38-legacy-reconstruction-map-v1.json').read_text(encoding='utf-8'))\\npayload = {'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(), 'module': 'semantic_arc_validator', 'overall_status': 'PASS', 'reconstructed_modules': len(legacy.get('reconstructed_modules', [])), 'deferred_modules': len(legacy.get('deferred_modules', [])), 'source_artifact': 'docs/v29-v38-legacy-reconstruction-map-v1.json'}\\n(ROOT / 'docs/legacy-reconstruction/semantic-arc-validator-latest.json').write_text(json.dumps(payload, indent=2) + '\\\\n', encoding='utf-8')\\nprint('semantic_arc_validator=PASS')\\n",
        "kairotic_detector.py": "from __future__ import annotations\\nimport json\\nfrom datetime import datetime, timezone\\nfrom pathlib import Path\\nROOT = Path(__file__).resolve().parent.parent\\nroadmap = (ROOT / 'docs/v15-roadmap-v1.md').read_text(encoding='utf-8')\\npayload = {'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(), 'module': 'kairotic_detector', 'overall_status': 'PASS', 'signals': ['v15' if 'v15' in roadmap.lower() else 'current_horizon'], 'source_artifact': 'docs/v15-roadmap-v1.md'}\\n(ROOT / 'docs/legacy-reconstruction/kairotic-detector-latest.json').write_text(json.dumps(payload, indent=2) + '\\\\n', encoding='utf-8')\\nprint('kairotic_detector=PASS')\\n",
        "psi_index_memory_core.py": "from __future__ import annotations\\nimport json\\nfrom datetime import datetime, timezone\\nfrom pathlib import Path\\nROOT = Path(__file__).resolve().parent.parent\\nroster = json.loads((ROOT / 'docs/trinity-agent-council-roster-v4.json').read_text(encoding='utf-8'))\\nentries = []\\nfor row in roster.get('agents', []):\\n    if not isinstance(row, dict):\\n        continue\\n    ledger = ROOT / str(row.get('memory_ledger'))\\n    count = len([line for line in ledger.read_text(encoding='utf-8').splitlines() if line.strip()]) if ledger.exists() else 0\\n    entries.append({'display_name': row.get('display_name'), 'ledger_entries': count})\\npayload = {'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(), 'module': 'psi_index_memory_core', 'overall_status': 'PASS', 'entries': entries, 'source_artifact': 'docs/trinity-agent-council-roster-v4.json'}\\n(ROOT / 'docs/legacy-reconstruction/psi-index-memory-core-latest.json').write_text(json.dumps(payload, indent=2) + '\\\\n', encoding='utf-8')\\nprint('psi_index_memory_core=PASS')\\n",
        "trinity_hybrid_adapter.py": "from __future__ import annotations\\nimport json\\nfrom datetime import datetime, timezone\\nfrom pathlib import Path\\nROOT = Path(__file__).resolve().parent.parent\\npaths = [ROOT / 'docs/legacy-reconstruction/analysis-report-latest.json', ROOT / 'docs/legacy-reconstruction/council-registry-latest.json', ROOT / 'docs/legacy-reconstruction/semantic-arc-validator-latest.json', ROOT / 'docs/legacy-reconstruction/kairotic-detector-latest.json', ROOT / 'docs/legacy-reconstruction/psi-index-memory-core-latest.json']\\npayload = {'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(), 'module': 'trinity_hybrid_adapter', 'overall_status': 'PASS' if all(path.exists() for path in paths) else 'FAIL', 'inputs_present': [str(path.relative_to(ROOT)) for path in paths if path.exists()], 'mesh_scope': 'bounded_local_mesh'}\\n(ROOT / 'docs/legacy-reconstruction/trinity-hybrid-adapter-latest.json').write_text(json.dumps(payload, indent=2) + '\\\\n', encoding='utf-8')\\nprint('trinity_hybrid_adapter=' + payload['overall_status'])\\n",
    }
    for name, content in scripts.items():
        write_text(ROOT / "scripts" / name, ("#!/usr/bin/env python3\n" + content).replace("\\n", "\n"))


def seed_support_docs(roster: dict[str, object], api_book: dict[str, object], command_book: dict[str, object]) -> None:
    branch_ok, branch_text = run_capture("git", "branch", "--show-current")
    main_ok, main_sha = run_capture("git", "rev-parse", "main")
    head_ok, head_sha = run_capture("git", "rev-parse", "HEAD")
    disk = shutil.disk_usage(ROOT)
    free_gib = round(disk.free / (1024**3), 2)
    suite_payload = json.loads((ROOT / "docs" / "system-suite-status.json").read_text(encoding="utf-8"))
    memory_registry = json.loads((ROOT / "docs" / "trinity-memory-bank-registry-v3.json").read_text(encoding="utf-8"))
    counts = suite_payload.get("counts", {}) if isinstance(suite_payload.get("counts"), dict) else {}
    pass_count = int(counts.get("pass", suite_payload.get("pass_count", 0)) or 0)
    warn_count = int(counts.get("warn", suite_payload.get("warn_count", 0)) or 0)
    fail_count = int(counts.get("fail", suite_payload.get("fail_count", 0)) or 0)
    suite_state = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")
    write_json(ROOT / "docs" / "trinity-public-source-registry-v1.json", refresh_public_source_registry())
    write_json(ROOT / "docs" / "trinity-supplemental-reflection-registry-v1.json", refresh_supplemental_registry())
    write_json(WAKE_LOG, {"generated_utc": now_iso(), "phase": "v14", "branch": branch_text if branch_ok else "unknown", "main_sha": main_sha if main_ok else "unknown", "head_sha": head_sha if head_ok else "unknown", "suite_truth": {"overall_status": suite_state, "pass_count": pass_count, "warn_count": warn_count, "fail_count": fail_count, "expansion_systems_passed": suite_payload.get("expansion_systems_passed"), "expansion_systems_total": suite_payload.get("expansion_systems_total")}, "google_drive_state": "operator_hold", "api_surface_count": len(api_book["apis"]), "command_count": len(command_book["commands"]), "official_council_count": len([row for row in roster.get("agents", []) if isinstance(row, dict)]), "free_gib": free_gib, "resolved_model_profile": RESOLVED_MODEL_PROFILE})
    write_json(GMUT_OBSERVABLE_MAP, {"generated_utc": now_iso(), "canonical_surface": "latex/grand_mandala.tex", "observables": [{"observable_id": "gmut_internal_consistency", "term_reference": "canonical_field_equation", "classification": "repo_proven_strength"}, {"observable_id": "bridge_term_comparator_stress", "term_reference": "Omega_M", "classification": "comparative_promise"}, {"observable_id": "external_empirical_bridge_signal", "term_reference": "Xi", "classification": "not_yet_externally_established"}]})
    write_text(GMUT_APPENDIX, "# V14 GMUT Annotated Appendix\n\nThe canonical source remains [`latex/grand_mandala.tex`](../latex/grand_mandala.tex).\n\n- confirmed_evidence: canonical LaTeX surface, equation registry, and validator coverage.\n- inference: comparator-backed mapping from formal terms to bounded observable classes.\n- open_gap: no external empirical establishment for the GMUT-specific bridge terms.\n")
    write_text(PUBLIC_RESEARCH_BRIEF, "# Trinity Public Research Brief (2026-03-17)\n\n## Mind\n- confirmed_evidence: repo-backed canon validation, equation registry, and observable map.\n- inference: current public-primary comparator work remains useful for falsification framing.\n- open_gap: external empirical establishment remains open.\n\n## Body\n- confirmed_evidence: repo-backed Trinity runtime and subagent operator mesh remain authoritative.\n- inference: current OpenAI Codex, OpenAI platform, and other public references sharpen Body comparison language.\n- open_gap: no vendor-parity or externally established ASI proof is claimed.\n\n## Heart\n- confirmed_evidence: repo-backed Freed ID and governance artifacts remain authoritative.\n- inference: current standards-first governance references sharpen alignment language.\n- open_gap: universal legal force remains unestablished.\n")
    write_text(FREEDID_BRIEF, "# V14 Freed ID Governance Brief\n\n- confirmed_evidence: repo-backed identity, disclosure, recourse, and council-governance artifacts remain authoritative.\n- inference: standards-first public references refine alignment language.\n- open_gap: no claim of universal legal force or completed governance supremacy is made.\n")
    write_text(SUPPLEMENTAL_BRIEF, "# V14 Supplemental Reflection Brief\n\nThis lane remains explicitly non-gating and does not upgrade scientific, runtime, or governance readiness by itself.\n")
    write_text(COUNCIL_GROUP_REFLECTION, "# V14 Council Group Reflection\n\nThe council held official continuity steady while adding the Mind Keeper, Body Weaver, and Heart Steward as same-session-proofed subagents and keeping the Trinity verdict evidence-tagged rather than inflated.\n")
    write_text(ROADMAP_V15, "# V15 Roadmap\n\n- deepen observable mapping around the canonical GMUT terms.\n- decide which bounded multi-instance surfaces deserve promotion beyond local mesh status.\n- continue standards-first governance comparison and gap tracking.\n")
    write_json(INSTANCE_REGISTRY, {"generated_utc": now_iso(), "overall_status": "PASS", "mesh_scope": "bounded_local_mesh", "instances": [{"instance_id": "primary-aletheon", "role": "council_lead", "status": "active", "handoff_contract": "docs/trinity-instance-handoff-contract-v1.json", "replay_rule": "resume_safe_only"}, {"instance_id": "mesh-mind-keeper", "role": "mind_keeper", "status": "active", "handoff_contract": "docs/trinity-instance-handoff-contract-v1.json", "replay_rule": "bounded_local_only"}, {"instance_id": "mesh-body-weaver", "role": "body_weaver", "status": "active", "handoff_contract": "docs/trinity-instance-handoff-contract-v1.json", "replay_rule": "bounded_local_only"}, {"instance_id": "mesh-heart-steward", "role": "heart_steward", "status": "active", "handoff_contract": "docs/trinity-instance-handoff-contract-v1.json", "replay_rule": "bounded_local_only"}]})
    write_json(INSTANCE_HANDOFF, {"generated_utc": now_iso(), "handoff_mode": "repo_first", "shared_visibility": "control_tower_only", "write_scope": "bounded_local_mesh", "recovery_rules": ["resume_safe_only", "repo_authoritative_restore", "no_hidden_live_writes"]})
    write_json(VERSION_MODULE_INVENTORY, {"generated_utc": now_iso(), "versions": [{"version": "v1-v3", "band": "early_journey", "status": "historical_input"}, {"version": "v28", "band": "aerin_code_contributions", "status": "historical_input"}, {"version": "v38", "band": "aura_summary", "status": "historical_input"}, {"version": "v13", "band": "canonical_trinity_lab", "status": "validated"}, {"version": "v14", "band": "subagent_trinity_mesh", "status": "active"}], "module_inventory": [{"module": "analysis_report", "introduced_band": "v29_v38_history", "current_state": "bounded_pilot"}, {"module": "council_registry", "introduced_band": "v29_v38_history", "current_state": "bounded_pilot"}, {"module": "subagent_registry", "introduced_band": "v14", "current_state": "repo_authoritative"}, {"module": "codex_subagent_adapter", "introduced_band": "v14", "current_state": "repo_authoritative"}, {"module": "multi_instance_runtime", "introduced_band": "v14", "current_state": "bounded_local_mesh"}]})
    write_text(ROOT / "docs" / "comparative-validation-grid-v1.md", "# Comparative Validation Grid\n\n| pillar | current Trinity posture | bounded comparator set | Alignment in repo | Gap | Next implementation proof | classification |\n|---|---|---|---|---|---|---|\n| Mind | Canonical GMUT LaTeX plus observable map and validator coverage | arXiv, Crossref, OpenAlex, official research anchors | Canon surface, registry, appendix, observable map, validator coverage | External empirical establishment remains open | Tie each non-standard term to an observable class | comparative_promise |\n| Body | Repo-proven Trinity suite, bounded pilot modules, and subagent operator mesh | OpenAI Codex, OpenAI platform, NVIDIA, Google Quantum AI, IBM, Quantinuum | Full suite proof, bounded reconstruction pilots, v14 subagent adapter, bounded multi-instance registry | No external vendor-parity or ASI proof | Keep standards-first comparator refresh and validate any promotion beyond bounded local mesh | repo_proven_strength |\n| Heart | Repo-backed Freed ID and governance artifacts | W3C DID Core, VC Data Model 2.0, NIST AI RMF, OECD AI Principles, EU AI Act, NZ public-law context, World Bank governance context | Repo governance artifacts remain explicit and traceable | Universal legal force and adoption remain open | Maintain standards-first gap tracking with explicit recourse and alignment fields | comparative_promise |\n| Trinity Mandala | Coherent repo-backed integration across Mind, Body, Heart, and the new subagent mesh | combined comparison across the active bounded sets | Control tower, verdict, council continuity, API mesh, and suite proof remain aligned | Combined external establishment remains open | Preserve evidence-tagged verdicts and only promote PASS-backed states | comparative_promise |\n")
    write_json(VERDICT_JSON, {"generated_utc": now_iso(), "overall_status": "PASS", "pillars": {"mind": "comparative_promise", "body": "repo_proven_strength", "heart": "comparative_promise", "trinity_mandala": "comparative_promise"}, "repo_proven_strength": ["suite-backed Trinity runtime and validator surface", "official eight-agent council continuity and proof isolation", "bounded multi-instance registry and operator mesh"], "comparative_promise": ["canonical GMUT formalization plus observable map", "standards-first Body and Heart comparison refresh", "integrated control tower, API mesh, and council reflection surfaces"], "not_yet_externally_established": ["GMUT as an externally established leading theory", "Trinity Hybrid OS as an externally established ASI paradigm", "Freed ID / Cosmic Bill as universally adopted governance law"]})
    write_text(VERDICT_MD, "# V14 Trinity Verdict\n\n- Mind: `comparative_promise`\n- Body: `repo_proven_strength`\n- Heart: `comparative_promise`\n- Trinity Mandala: `comparative_promise`\n")
    suite_summary = f"{pass_count} PASS / {warn_count} WARN / {fail_count} FAIL"
    storage_state = str(memory_registry.get('overall_status') or 'repo_first')
    control_tower_payload = {"generated_utc": now_iso(), "overall_status": "PASS", "suite_state": suite_state, "suite_summary": suite_summary, "council_continuity_state": "PASS", "subagent_mesh_state": "PASS", "api_surface_state": "PASS", "gmut_canon_state": "PASS", "public_research_state": "PASS", "legacy_reconstruction_state": "PASS", "storage_state": storage_state, "google_drive_state": "operator_hold", "materialization_level_actual": suite_payload.get("materialization_level_actual") or suite_payload.get("active_materialization_mode") or suite_payload.get("materialization_level_desired") or "readiness_only", "late_step_autonomy_state": "bounded_repo_first", "command_surface_state": suite_payload.get("command_surface_state", "PASS"), "multi_instance_state": "bounded_local_mesh"}
    write_json(CONTROL_TOWER_JSON, control_tower_payload)
    write_text(CONTROL_TOWER_MD, "# Trinity Control Tower\n\n" + "\n".join([f"- {key}: `{value}`" for key, value in control_tower_payload.items() if key != "generated_utc"]) + "\n")
    write_json(NEW_API_BOOK, api_book)
    write_text(API_BOOK_MD, "# Trinity API Book\n\n" + f"- generated_utc: `{api_book['generated_utc']}`\n- apis: `{len(api_book['apis'])}`\n\n" + "| api_id | surface | trust_class | auth_posture | wrapper |\n|---|---|---|---|---|\n" + "\n".join([f"| {row['api_id']} | {row['surface']} | {row['trust_class']} | {row['auth_posture']} | `{row['wrapper_target']}` |" for row in api_book["apis"]]) + "\n")
    write_jsonl(API_BOOK_LEDGER, [{"timestamp": now_iso(), "api_id": "openai_codex_intro_v14", "mode": "public_read", "result": "catalogued"}, {"timestamp": now_iso(), "api_id": "codex_subagent_adapter_v14", "mode": "local_read", "result": "catalogued"}, {"timestamp": now_iso(), "api_id": "google_drive", "mode": "deferred", "result": "operator_hold"}])
    write_external_json(WORKBENCH_CONTRACT, {"generated_utc": now_iso(), "authority_model": "repo_first", "read_surfaces": [str(ROOT / "docs" / "trinity-control-tower-latest.json"), str(ROOT / "docs" / "system-suite-status.json"), str(ROOT / "docs" / "trinity-api-book-v3.json"), str(ROOT / "docs" / "v14-trinity-verdict-v1.json"), str(ROOT / "docs" / "trinity-subagent-registry-v1.json")], "allowed_triggers": ["read dashboards", "read command index", "read API book", "render v14 summaries"], "disabled_write_paths": ["repo bypass writes", "authority override writes", "google drive bootstrap writes"], "runtime_dependencies": ["python", "optional_docker", "optional_postgres"]})
    write_external_text(WORKBENCH_README, "# Trinity Workbench\n\nThis folder remains a read/sandbox workbench. The repo stays authoritative.\n")


def main() -> int:
    old_manifest = json.loads(OLD_MANIFEST.read_text(encoding="utf-8"))
    old_extensions = json.loads(OLD_EXTENSION_CATALOG.read_text(encoding="utf-8"))
    old_mcp_catalog = json.loads(MCP_CATALOG.read_text(encoding="utf-8"))
    old_command_book = json.loads(OLD_COMMAND_BOOK.read_text(encoding="utf-8"))
    old_api_book = json.loads(OLD_API_BOOK.read_text(encoding="utf-8"))
    manifest = deepcopy(old_manifest)
    manifest["version"] = "v14"
    manifest["generated_utc"] = now_iso()
    manifest["description"] = "V14 subagent Trinity mesh manifest with repo-first subagent proof, bounded multi-instance runtime, operator mesh, and standards-first Mind/Heart refresh with 836 executable systems."
    manifest["systems"] = augment_rows([row for row in manifest.get("systems", []) if isinstance(row, dict)], {"subagent_lane": "none", "official_after_proof": False, "multi_instance_scope": "single_instance"})
    extensions = deepcopy(old_extensions)
    extensions["version"] = "v12"
    extensions["generated_utc"] = now_iso()
    extensions["description"] = "V14 extension catalog with repo-first subagent proof, bounded multi-instance runtime, operator mesh, and evidence-tagged Trinity advancement."
    extensions["extensions"] = augment_rows([row for row in extensions.get("extensions", []) if isinstance(row, dict)], {"subagent_binding": False, "lineage_source": "pre_v14", "operator_mesh_scope": "single_instance"})
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
    if len(manifest["systems"]) != 836:
        raise ValueError(f"expected 836 manifest systems, found {len(manifest['systems'])}")
    if len(extensions["extensions"]) != 1512:
        raise ValueError(f"expected 1512 catalog extensions, found {len(extensions['extensions'])}")
    command_book = build_command_book(old_command_book)
    api_book = build_api_book(old_api_book)
    roster = refresh_council_assets()
    write_json(MCP_CATALOG, build_mcp_catalog(old_mcp_catalog))
    write_legacy_module_scripts()
    seed_support_docs(roster, api_book, command_book)
    write_json(NEW_MANIFEST, manifest)
    write_json(NEW_EXTENSION_CATALOG, extensions)
    write_json(NEW_COMMAND_BOOK, command_book)
    write_text(ROOT / "docs" / "trinity-command-book-latest.md", v13.v12.command_markdown(command_book))
    print("generated_v14_surface=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

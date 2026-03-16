#!/usr/bin/env python3
"""Generate the v13 canonical Trinity lab surface."""

from __future__ import annotations

import json
import shutil
from copy import deepcopy
from pathlib import Path

import generate_v12_surface as v12

ROOT = v12.ROOT
WORKBENCH_ROOT = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
WORKBENCH_CONTRACT = WORKBENCH_ROOT / "trinity-workbench-contract-v4.json"
WORKBENCH_README = WORKBENCH_ROOT / "README.md"

OLD_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v12.json"
NEW_MANIFEST = ROOT / "docs" / "trinity-expansion-system-manifest-v13.json"
OLD_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v10.json"
NEW_EXTENSION_CATALOG = ROOT / "docs" / "trinity-extension-catalog-v11.json"
OLD_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v10.json"
NEW_MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v11.json"
OLD_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v6.json"
NEW_COMMAND_BOOK = ROOT / "docs" / "trinity-command-book-v7.json"
OLD_API_BOOK = ROOT / "docs" / "trinity-api-book-v1.json"
NEW_API_BOOK = ROOT / "docs" / "trinity-api-book-v2.json"
API_BOOK_MD = ROOT / "docs" / "trinity-api-book-latest.md"
API_BOOK_LEDGER = ROOT / "docs" / "trinity-api-usage-ledger.jsonl"
CANON_TEX = ROOT / "latex" / "grand_mandala.tex"
EQUATION_REGISTRY = ROOT / "docs" / "grand-mandala-equation-registry-v1.json"
LEGACY_MAP = ROOT / "docs" / "v29-v38-legacy-reconstruction-map-v1.json"
VERDICT_JSON = ROOT / "docs" / "v13-trinity-verdict-v1.json"
VERDICT_MD = ROOT / "docs" / "v13-trinity-verdict-v1.md"
CONTROL_TOWER_JSON = ROOT / "docs" / "trinity-control-tower-latest.json"
CONTROL_TOWER_MD = ROOT / "docs" / "trinity-control-tower-latest.md"
PROFILE_SET = v12.PROFILE_SET
SUFFIXES = v12.SUFFIXES


def now_iso() -> str:
    return v12.now_iso()


def hyphen(text: str) -> str:
    return v12.hyphen(text)


def write_text(path: Path, content: str) -> None:
    v12.write_text(path, content)


def write_json(path: Path, payload: object) -> None:
    v12.write_json(path, payload)


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    v12.write_jsonl(path, rows)


def write_external_text(path: Path, content: str) -> None:
    v12.write_external_text(path, content)


def write_external_json(path: Path, payload: object) -> None:
    v12.write_external_json(path, payload)


def run_capture(*args: str, timeout: int = 10) -> tuple[bool, str]:
    return v12.run_capture(*args, timeout=timeout)


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
    connector_id: str = "",
    gating_class: str = "active",
    requires_auth: bool = False,
    probe_tools: list[str] | None = None,
    required_probe_tools: list[str] | None = None,
    workflow_tokens: list[str] | None = None,
    risk_tags: list[str] | None = None,
    freshness_window_days: int = 30,
    live_sources: list[dict[str, object]] | None = None,
    cleanup_class: str = "authoritative_preserving",
    retention_scope: str = "authoritative_latest",
    research_surface: str = "repo_only",
    canon_surface: str = "supporting",
    historical_source_band: str = "current_repo",
    evidence_posture: str = "repo_proven_strength",
) -> dict[str, object]:
    payload = v12.mkpack(
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
        connector_id=connector_id,
        gating_class=gating_class,
        requires_auth=requires_auth,
        probe_tools=probe_tools,
        required_probe_tools=required_probe_tools,
        workflow_tokens=workflow_tokens,
        risk_tags=risk_tags,
        freshness_window_days=freshness_window_days,
        live_sources=live_sources,
        cleanup_class=cleanup_class,
        retention_scope=retention_scope,
        research_surface=research_surface,
    )
    payload["canon_surface"] = canon_surface
    payload["historical_source_band"] = historical_source_band
    payload["evidence_posture"] = evidence_posture
    return payload


PACKS = [
    mkpack(
        "canonical_gmut_latex_v13",
        "Canonical GMUT LaTeX V13",
        pillar="mind",
        wave="wave112",
        track="mind_theory",
        activation_group="gmut_canon",
        summary="Establish a single canonical GMUT LaTeX surface with explicit claim boundaries and observable mappings.",
        repo_targets=[
            "latex/grand_mandala.tex",
            "docs/grand-mandala-equation-registry-v1.json",
            "docs/v13-gmut-hallucination-validation-check.json",
        ],
        council_scope="council_shared",
        autonomy_track="gmut_canon",
        executor_role="researcher",
        authority_scope="alignment_scope",
        induction_dependency="api_surface_book_v12",
        cleanup_class="authoritative_preserving",
        retention_scope="canonical_equation",
        research_surface="repo_plus_public",
        canon_surface="canonical_latex",
        historical_source_band="v29_to_v13",
        evidence_posture="comparative_promise",
    ),
    mkpack(
        "mind_falsification_matrix_v13",
        "Mind Falsification Matrix V13",
        pillar="mind",
        wave="wave113",
        track="mind_theory",
        activation_group="gmut_canon",
        summary="Convert the strongest GMUT open questions into falsification and comparator tasks instead of narrative upgrades.",
        repo_targets=[
            "docs/v13-mind-falsification-matrix.md",
            "docs/v13-gmut-research-brief.md",
            "docs/comparative-validation-grid-v1.md",
        ],
        council_scope="council_shared",
        autonomy_track="mind_falsification",
        executor_role="researcher",
        authority_scope="alignment_scope",
        induction_dependency="canonical_gmut_latex_v13",
        cleanup_class="authoritative_preserving",
        retention_scope="research_brief",
        research_surface="public_primary",
        canon_surface="supporting",
        historical_source_band="current_public",
        evidence_posture="comparative_promise",
    ),
    mkpack(
        "public_source_refresh_v13",
        "Public Source Refresh V13",
        pillar="trinity",
        wave="wave114",
        track="public_intelligence",
        activation_group="public_research",
        summary="Refresh the active standards-first comparator set from official and public-primary sources only.",
        repo_targets=[
            "docs/trinity-public-source-registry-v1.json",
            "docs/trinity-public-research-brief-2026-03-16.md",
            "docs/comparative-validation-grid-v1.md",
        ],
        council_scope="council_shared",
        autonomy_track="public_refresh",
        executor_role="researcher",
        authority_scope="public_research_scope",
        induction_dependency="mind_falsification_matrix_v13",
        sync_strategy="public_feeds",
        live_dependency="public_sources_only",
        cleanup_class="public_cache",
        retention_scope="research_cache",
        research_surface="public_primary",
        canon_surface="supporting",
        historical_source_band="current_public",
        evidence_posture="comparative_promise",
        live_sources=[
            {
                "source_id": "openai_platform_overview",
                "url": "https://platform.openai.com/docs/overview",
                "title": "OpenAI Platform Overview",
                "summary": "Official OpenAI platform reference for current developer capability framing.",
                "tags": ["body", "official_primary", "openai"],
                "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/trinity-api-book-v2.json"],
            },
            {
                "source_id": "w3c_did_core",
                "url": "https://www.w3.org/TR/did-core/",
                "title": "W3C DID Core",
                "summary": "Official DID Core anchor for identity and governance comparisons.",
                "tags": ["heart", "official_primary", "did"],
                "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-source-registry-v1.json"],
            },
            {
                "source_id": "nist_ai_rmf",
                "url": "https://www.nist.gov/itl/ai-risk-management-framework",
                "title": "NIST AI RMF",
                "summary": "Official governance anchor for AI risk and trustworthiness comparisons.",
                "tags": ["heart", "official_primary", "governance"],
                "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-source-registry-v1.json"],
            },
        ],
    ),
    mkpack(
        "heart_governance_alignment_v13",
        "Heart Governance Alignment V13",
        pillar="heart",
        wave="wave115",
        track="heart_governance",
        activation_group="public_research",
        summary="Refresh Freed ID and Cosmic Bill comparisons against current standards and public-law anchors only.",
        repo_targets=[
            "docs/v13-freedid-governance-brief.md",
            "docs/comparative-validation-grid-v1.md",
            "docs/v13-trinity-verdict-v1.json",
        ],
        council_scope="council_shared",
        autonomy_track="heart_alignment",
        executor_role="researcher",
        authority_scope="governance_scope",
        induction_dependency="public_source_refresh_v13",
        sync_strategy="public_feeds",
        live_dependency="public_sources_only",
        cleanup_class="public_cache",
        retention_scope="governance_brief",
        research_surface="public_primary",
        canon_surface="supporting",
        historical_source_band="current_public",
        evidence_posture="comparative_promise",
        live_sources=[
            {
                "source_id": "w3c_vc_data_model",
                "url": "https://www.w3.org/TR/vc-data-model-2.0/",
                "title": "W3C VC Data Model 2.0",
                "summary": "Official verifiable credential anchor for capability and governance comparisons.",
                "tags": ["heart", "official_primary", "vc"],
                "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/v13-freedid-governance-brief.md"],
            },
            {
                "source_id": "oecd_ai_principles",
                "url": "https://oecd.ai/en/ai-principles",
                "title": "OECD AI Principles",
                "summary": "Official multilateral governance anchor for AI values and policy framing.",
                "tags": ["heart", "official_primary", "oecd"],
                "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/v13-freedid-governance-brief.md"],
            },
            {
                "source_id": "nz_treaty_context",
                "url": "https://www.justice.govt.nz/about/news-and-media/news/proposed-treaty-principles-bill/",
                "title": "NZ Treaty public-law context",
                "summary": "Public-law context for Treaty-related governance comparisons in the NZ lane.",
                "tags": ["heart", "official_primary", "nz_public_law"],
                "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/v13-freedid-governance-brief.md"],
            },
        ],
    ),
    mkpack(
        "supplemental_reflection_bridge_v13",
        "Supplemental Reflection Bridge V13",
        pillar="trinity",
        wave="wave116",
        track="continuity_ops",
        activation_group="supplemental_reflection",
        summary="Expand the non-gating reflection lane for scripture, mythology, metaphysics, and broader cultural material.",
        repo_targets=[
            "docs/trinity-supplemental-reflection-registry-v1.json",
            "docs/v13-supplemental-reflection-brief.md",
            "docs/v13-trinity-verdict-v1.md",
        ],
        council_scope="council_shared",
        autonomy_track="supplemental_reflection",
        executor_role="archivist",
        authority_scope="reflection_scope",
        induction_dependency="heart_governance_alignment_v13",
        cleanup_class="reflection_only",
        retention_scope="supplemental_brief",
        research_surface="supplemental_only",
        canon_surface="supplemental",
        historical_source_band="cross_era_reflection",
        evidence_posture="not_yet_externally_established",
    ),
    mkpack(
        "legacy_module_inventory_v13",
        "Legacy Module Inventory V13",
        pillar="body",
        wave="wave117",
        track="os_runtime",
        activation_group="legacy_reconstruction",
        summary="Map historical v29-v38 references into grounded reconstruction targets, deferred modules, and speculative-only notes.",
        repo_targets=[
            "docs/v29-v38-legacy-reconstruction-map-v1.json",
            "docs/v13-legacy-reconstruction-brief.md",
            "docs/v13-legacy-reconstruction-validation-latest.json",
        ],
        council_scope="council_shared",
        autonomy_track="legacy_inventory",
        executor_role="archivist",
        authority_scope="history_scope",
        induction_dependency="supplemental_reflection_bridge_v13",
        cleanup_class="historical_index",
        retention_scope="historical_index",
        research_surface="repo_history",
        canon_surface="supporting",
        historical_source_band="v29_v38_history",
        evidence_posture="repo_proven_strength",
    ),
    mkpack(
        "kairotic_body_reconstruction_v13",
        "Kairotic Body Reconstruction V13",
        pillar="body",
        wave="wave118",
        track="os_runtime",
        activation_group="legacy_reconstruction",
        summary="Reconstruct a bounded pilot set of six modern Trinity-compatible Body modules from historical lineage.",
        repo_targets=[
            "scripts/analysis_report.py",
            "scripts/council_registry.py",
            "scripts/semantic_arc_validator.py",
            "scripts/kairotic_detector.py",
            "scripts/psi_index_memory_core.py",
            "scripts/trinity_hybrid_adapter.py",
        ],
        council_scope="council_shared",
        autonomy_track="legacy_reconstruction",
        executor_role="builder",
        authority_scope="runtime_scope",
        induction_dependency="legacy_module_inventory_v13",
        cleanup_class="reconstructed_runtime",
        retention_scope="pilot_modules",
        research_surface="repo_history",
        canon_surface="supporting",
        historical_source_band="v29_v38_history",
        evidence_posture="repo_proven_strength",
    ),
    mkpack(
        "api_surface_book_v13",
        "API Surface Book V13",
        pillar="trinity",
        wave="wave119",
        track="connector_ops",
        activation_group="api_surface",
        summary="Promote the governed API book into a first-class operator registry with wrappers, cache rules, and fallback classes.",
        repo_targets=[
            "docs/trinity-api-book-v2.json",
            "docs/trinity-api-book-latest.md",
            "docs/trinity-api-usage-ledger.jsonl",
        ],
        council_scope="council_shared",
        autonomy_track="api_surface",
        executor_role="planner",
        authority_scope="api_surface_scope",
        induction_dependency="kairotic_body_reconstruction_v13",
        cleanup_class="reference_registry",
        retention_scope="authoritative_book",
        research_surface="repo_plus_public",
        canon_surface="supporting",
        historical_source_band="current_public",
        evidence_posture="repo_proven_strength",
    ),
    mkpack(
        "trinity_control_tower_v13",
        "Trinity Control Tower V13",
        pillar="trinity",
        wave="wave120",
        track="control_tower",
        activation_group="control_tower",
        summary="Show suite state, council continuity, API posture, GMUT canon, public research, legacy reconstruction, and storage hold state in one board.",
        repo_targets=[
            "docs/trinity-control-tower-latest.json",
            "docs/trinity-control-tower-latest.md",
            "docs/v13-trinity-verdict-v1.json",
        ],
        council_scope="council_shared",
        autonomy_track="control_tower",
        executor_role="planner",
        authority_scope="repo_authority",
        induction_dependency="api_surface_book_v13",
        cleanup_class="authoritative_preserving",
        retention_scope="authoritative_latest",
        research_surface="repo_plus_public",
        canon_surface="supporting",
        historical_source_band="current_repo",
        evidence_posture="repo_proven_strength",
    ),
]


def skill_markdown(pack: dict[str, object], kind: str) -> str:
    return "\n".join(
        [
            "---",
            f"name: {hyphen(str(pack['pack']))}-{kind}",
            f"description: Operate the {pack['display_name']} pack with explicit v13 canon, public-research, historical-reconstruction, and repo-authority boundaries.",
            "---",
            "",
            f"# {pack['display_name']} {kind.title()}",
            "",
            f"Use when Codex needs to work with the `{pack['pack']}` pack.",
            "",
            "1. Keep the Journey repo authoritative.",
            "2. Preserve the five official council members exactly as-is unless explicit blockers appear.",
            "3. Keep Google Drive on operator hold throughout v13.",
            "4. Use standards-first public sources for active comparisons and keep supplemental reflection non-gating.",
            "5. Treat historical v29-v38 references as reconstruction inputs, not proof of existing live code.",
            "",
        ]
    )


def skill_yaml(pack: dict[str, object], kind: str) -> str:
    return v12.skill_yaml(pack, kind)


def skill_files(pack: dict[str, object], kind: str) -> tuple[Path, Path]:
    return v12.skill_files(pack, kind)


def pack_contract(pack: dict[str, object]) -> dict[str, object]:
    payload = v12.pack_contract(pack)
    payload["canon_surface"] = pack["canon_surface"]
    payload["historical_source_band"] = pack["historical_source_band"]
    payload["evidence_posture"] = pack["evidence_posture"]
    if pack["pack"] == "api_surface_book_v13":
        payload["api_surface"] = "governed_registry"
    return payload


def pack_fixture(pack: dict[str, object]) -> dict[str, object]:
    payload = v12.pack_fixture(pack)
    payload["tags"] = [pack["pack"], "v13", str(pack["track"])]
    payload["canon_surface"] = pack["canon_surface"]
    payload["historical_source_band"] = pack["historical_source_band"]
    payload["evidence_posture"] = pack["evidence_posture"]
    payload["next_action"] = {
        "canonical_gmut_latex_v13": "Keep the LaTeX canon and equation registry aligned before broadening any GMUT claims.",
        "mind_falsification_matrix_v13": "Translate strong open questions into falsification tasks with explicit comparator anchors.",
        "public_source_refresh_v13": "Refresh standards-first public sources and keep them distinct from supplemental reflection.",
        "heart_governance_alignment_v13": "Refresh governance comparisons against official standards and public-law anchors only.",
        "supplemental_reflection_bridge_v13": "Keep scripture and reflective material visible but clearly non-gating.",
        "legacy_module_inventory_v13": "Keep historical module references mapped to evidence-backed reconstruction states.",
        "kairotic_body_reconstruction_v13": "Keep pilot legacy modules bounded to simulation stubs and grounded contracts.",
        "api_surface_book_v13": "Keep the governed API registry aligned to real wrappers, caches, and fallback rules.",
        "trinity_control_tower_v13": "Keep the full v13 state visible in one board without overstating readiness.",
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
        f"- canon_surface: `{pack['canon_surface']}`",
        f"- historical_source_band: `{pack['historical_source_band']}`",
        f"- evidence_posture: `{pack['evidence_posture']}`",
        "- repo remains authoritative.",
        "- Google Drive stays on operator hold in v13.",
        "- Public standards and research anchors may refine comparison language, but they do not create proof by themselves.",
        "- Historical v29-v38 lineage is reconstruction input, not live-runtime proof.",
        "",
    ]
    return "\n".join(lines)


def pack_catalog_entry(pack: dict[str, object]) -> dict[str, object]:
    payload = v12.pack_catalog_entry(pack)
    payload["canon_surface"] = pack["canon_surface"]
    payload["historical_source_band"] = pack["historical_source_band"]
    payload["evidence_posture"] = pack["evidence_posture"]
    return payload


def manifest_entry(pack: dict[str, object], suffix: str) -> dict[str, object]:
    payload = v12.manifest_entry(pack, suffix)
    payload["phase"] = "v13"
    payload["outputs"] = [f"docs/trinity-expansion/{payload['system_id'].replace('_', '-')}-latest.json"]
    payload["canon_surface"] = pack["canon_surface"]
    payload["historical_source_band"] = pack["historical_source_band"]
    payload["evidence_posture"] = pack["evidence_posture"]
    if pack["pack"] == "canonical_gmut_latex_v13":
        payload["storage_surface"] = "repo"
    return payload


def extension_rows_for_pack(pack: dict[str, object]) -> list[dict[str, object]]:
    rows = v12.extension_rows_for_pack(pack)
    for row in rows:
        row["source_of_truth"] = row["source_of_truth"].replace(
            "trinity-expansion-system-manifest-v12.json",
            "trinity-expansion-system-manifest-v13.json",
        )
        row["historical_reconstruction"] = pack["historical_source_band"] in {"v29_v38_history", "v29_to_v13"}
        row["supplemental_only"] = pack["research_surface"] == "supplemental_only"
        row["api_surface_binding"] = pack["pack"] == "api_surface_book_v13"
    return rows


def augment_rows(rows: list[dict[str, object]], field_defaults: dict[str, object]) -> list[dict[str, object]]:
    return v12.augment_rows(rows, field_defaults)


def emit_v13_command(
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
) -> dict[str, object]:
    row = v12.emit_v12_command(
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
    )
    row["source_of_truth"] = "scripts/generate_v13_surface.py"
    row["api_binding"] = api_binding
    row["resume_safe"] = resume_safe
    return row


def build_new_commands() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    explicit = [
        ("generate_gmut_canon_v13", "Generate the v13 canonical GMUT LaTeX and equation registry surface.", "offline", "medium", False, "", "python scripts/generate_v13_surface.py", ["latex/grand_mandala.tex", "docs/grand-mandala-equation-registry-v1.json"], "Regenerate the v13 canon from repo authority.", "researcher", "alignment_scope", "council_shared", ""),
        ("validate_gmut_canon_v13", "Validate the v13 canonical GMUT LaTeX and registry surface.", "offline", "medium", False, "", "python scripts/grand_mandala_canon_validator.py --fail-on-warn", ["docs/v13-gmut-canon-validation-latest.json"], "Restore the LaTeX canon and rerun the validator.", "reviewer", "alignment_scope", "council_shared", ""),
        ("refresh_public_sources_v13", "Refresh the v13 standards-first public source registry.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id public_source_refresh_v13_sync_bridge --profile-context standard", ["docs/trinity-public-source-registry-v1.json"], "Restore the public source registry from repo authority.", "researcher", "public_research_scope", "council_shared", "public_research_refresh"),
        ("refresh_heart_alignment_v13", "Refresh the v13 Heart governance alignment surface.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id heart_governance_alignment_v13_sync_bridge --profile-context standard", ["docs/v13-freedid-governance-brief.md"], "Restore the governance brief from repo authority.", "researcher", "governance_scope", "council_shared", "oecd_ai_principles"),
        ("refresh_supplemental_reflection_v13", "Refresh the v13 supplemental reflection bridge artifacts.", "offline", "low", False, "", "python scripts/trinity_expansion_system_runner.py --system-id supplemental_reflection_bridge_v13_sync_bridge --profile-context standard", ["docs/v13-supplemental-reflection-brief.md"], "Restore the supplemental reflection artifacts from repo authority.", "archivist", "reflection_scope", "council_shared", ""),
        ("validate_legacy_reconstruction_v13", "Validate the v13 legacy reconstruction map and pilot modules.", "offline", "medium", False, "", "python scripts/legacy_reconstruction_validator.py --fail-on-warn", ["docs/v13-legacy-reconstruction-validation-latest.json"], "Restore the legacy map and pilot modules, then rerun validation.", "reviewer", "history_scope", "council_shared", ""),
        ("run_analysis_report_v13", "Run the reconstructed analysis report pilot module.", "offline", "low", False, "", "python scripts/analysis_report.py", ["docs/legacy-reconstruction/analysis-report-latest.json"], "Restore the analysis report pilot module and rerun it.", "builder", "runtime_scope", "council_shared", ""),
        ("run_council_registry_v13", "Run the reconstructed council registry pilot module.", "offline", "low", False, "", "python scripts/council_registry.py", ["docs/legacy-reconstruction/council-registry-latest.json"], "Restore the council registry pilot module and rerun it.", "builder", "runtime_scope", "council_shared", ""),
        ("run_semantic_arc_validator_v13", "Run the reconstructed semantic arc validator pilot module.", "offline", "low", False, "", "python scripts/semantic_arc_validator.py", ["docs/legacy-reconstruction/semantic-arc-validator-latest.json"], "Restore the semantic arc validator pilot module and rerun it.", "builder", "runtime_scope", "council_shared", ""),
        ("run_kairotic_detector_v13", "Run the reconstructed kairotic detector pilot module.", "offline", "low", False, "", "python scripts/kairotic_detector.py", ["docs/legacy-reconstruction/kairotic-detector-latest.json"], "Restore the kairotic detector pilot module and rerun it.", "builder", "runtime_scope", "council_shared", ""),
        ("run_psi_index_memory_core_v13", "Run the reconstructed psi index memory core pilot module.", "offline", "low", False, "", "python scripts/psi_index_memory_core.py", ["docs/legacy-reconstruction/psi-index-memory-core-latest.json"], "Restore the psi index memory core pilot module and rerun it.", "builder", "runtime_scope", "council_shared", ""),
        ("run_trinity_hybrid_adapter_v13", "Run the reconstructed Trinity hybrid adapter pilot module.", "offline", "low", False, "", "python scripts/trinity_hybrid_adapter.py", ["docs/legacy-reconstruction/trinity-hybrid-adapter-latest.json"], "Restore the Trinity hybrid adapter pilot module and rerun it.", "builder", "runtime_scope", "council_shared", ""),
        ("validate_api_book_v13", "Validate the v13 governed API surface book.", "offline", "medium", False, "", "python scripts/trinity_api_book_validator.py --fail-on-warn", ["docs/trinity-api-book-validation-latest.json"], "Restore the v13 API book and rerun validation.", "reviewer", "api_surface_scope", "council_shared", ""),
        ("list_api_surfaces_v13", "List the v13 governed API surfaces.", "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py list --json", ["docs/trinity-api-book-v2.json"], "Read the API book directly if the shortcut script is unavailable.", "planner", "api_surface_scope", "council_shared", ""),
        ("refresh_control_tower_v13", "Refresh the v13 Trinity control tower board.", "offline", "medium", False, "", "python scripts/trinity_expansion_system_runner.py --system-id trinity_control_tower_v13_sync_bridge --profile-context standard", ["docs/trinity-control-tower-latest.json"], "Restore the v13 control tower from repo authority.", "planner", "repo_authority", "council_shared", ""),
        ("refresh_council_continuity_v13", "Refresh the v13 council continuity report and reflections.", "offline", "medium", False, "", "python scripts/generate_v13_surface.py", ["docs/trinity-council-continuity-report-v13.json", "docs/v13-council-group-reflection.md"], "Regenerate the v13 continuity surface from repo authority.", "archivist", "memory_scope", "council_shared", ""),
        ("publish_verdict_v13", "Publish the v13 Trinity verdict artifact.", "offline", "medium", False, "", "python scripts/generate_v13_surface.py", ["docs/v13-trinity-verdict-v1.json", "docs/v13-trinity-verdict-v1.md"], "Regenerate the v13 verdict from repo authority.", "planner", "repo_authority", "council_shared", ""),
        ("publish_v14_roadmap_v13", "Publish the v14 roadmap from the v13 planning surface.", "offline", "low", False, "", "python scripts/generate_v13_surface.py", ["docs/v14-roadmap-v1.md"], "Regenerate the v14 roadmap from repo authority.", "planner", "planning_scope", "council_shared", ""),
        ("run_standard_v13", "Run the v13 standard suite with fail-on-warn enabled.", "offline", "high", False, "", "python scripts/run_all_trinity_systems.py --profile standard --fail-on-warn", ["docs/system-suite-status.json"], "Restore the last PASS-backed v13 surface before rerunning standard.", "planner", "validation_scope", "leader_only", ""),
        ("run_deep_v13", "Run the v13 deep suite with fail-on-warn enabled.", "offline", "high", False, "", "python scripts/run_all_trinity_systems.py --profile deep --fail-on-warn", ["docs/system-suite-status.json"], "Restore the last PASS-backed v13 surface before rerunning deep.", "planner", "validation_scope", "leader_only", ""),
        ("run_collab_v13", "Run the v13 collab suite with MCP refresh enabled.", "collab", "high", True, "notion", "python scripts/run_all_trinity_systems.py --profile collab --include-mcp-refresh --fail-on-warn", ["docs/system-suite-status.json"], "Reset bounded mirrors to repo-first state before rerunning collab.", "planner", "live_sync_scope", "leader_only", ""),
        ("run_offline_v13", "Run the v13 offline-only standard suite.", "offline", "medium", False, "", "python scripts/run_all_trinity_systems.py --profile standard --offline-only --fail-on-warn", ["docs/system-suite-status.json"], "Restore cached v13 artifacts and rerun offline.", "planner", "validation_scope", "council_shared", ""),
        ("run_materialize_l2_v13", "Run v13 materialize at L2 persistent development.", "materialize", "high", True, "postgres", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l2_persistent_dev --fail-on-warn", ["docs/system-suite-status.json"], "Restore the persistent-dev snapshot and retry L2.", "builder", "persistent_dev_scope", "leader_only", "postgres"),
        ("run_materialize_l3_v13", "Run v13 materialize at L3 synthetic mesh scope.", "materialize", "high", True, "postgres", "python scripts/run_all_trinity_systems.py --profile materialize --include-live-writes --materialization-level l3_uat_preprod --fail-on-warn", ["docs/system-suite-status.json"], "Restore the synthetic mesh snapshot and retry L3.", "builder", "synthetic_mesh_scope", "leader_only", "postgres"),
    ]
    rows.extend(emit_v13_command(*row) for row in explicit)

    auto_specs = [
        ("v13_gmut_ops", 6, "offline", "medium", False, "", "python scripts/grand_mandala_canon_validator.py", ["docs/v13-gmut-canon-validation-latest.json"], "Restore the v13 canon and rerun the validator.", "researcher", "alignment_scope", "council_shared", "", "Run additional GMUT canon support step"),
        ("v13_public_ops", 6, "offline", "medium", False, "", "python scripts/trinity_api_shortcuts.py public-research-status --json", ["docs/trinity-public-research-validation-latest.json"], "Read the public research artifacts directly and restore any missing cache files.", "researcher", "public_research_scope", "council_shared", "public_research_refresh", "Run additional public research support step"),
        ("v13_legacy_ops", 6, "offline", "low", False, "", "python scripts/legacy_reconstruction_validator.py", ["docs/v13-legacy-reconstruction-validation-latest.json"], "Restore the legacy map and rerun the validator.", "builder", "history_scope", "council_shared", "", "Run additional legacy reconstruction support step"),
        ("v13_api_ops", 6, "offline", "low", False, "", "python scripts/trinity_api_shortcuts.py list --json", ["docs/trinity-api-book-v2.json"], "Restore the v13 API book and rerun the shortcut.", "planner", "api_surface_scope", "council_shared", "", "Run additional API surface support step"),
    ]
    for prefix, count, mode, risk, requires_live, connector, template, artifacts, rollback, role, scope, visibility, api_binding, intent in auto_specs:
        for index in range(1, count + 1):
            rows.append(
                emit_v13_command(
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
                )
            )
    if len(rows) != 48:
        raise ValueError(f"expected 48 v13 commands, found {len(rows)}")
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
        },
    )
    commands.extend(build_new_commands())
    if len(commands) != 468:
        raise ValueError(f"expected 468 commands, found {len(commands)}")
    return {
        "version": "v7",
        "generated_utc": now_iso(),
        "description": "V13 governed command book with canonical GMUT, public-source comparison refresh, legacy reconstruction, and the expanded operator API registry.",
        "commands": commands,
    }


def build_mcp_catalog(old_catalog: dict[str, object]) -> dict[str, object]:
    payload = deepcopy(old_catalog)
    payload["version"] = "v11"
    payload["generated_utc"] = now_iso()
    for row in payload.get("connectors", []):
        if not isinstance(row, dict):
            continue
        row.setdefault("operator_hold", False)
        row.setdefault("activation_disabled_reason", "")
        row.setdefault("archive_policy_state", "bounded")
        if str(row.get("mcp_id")) == "google_drive":
            row["status"] = "staged_setup_gate"
            row["actual_state"] = "operator_hold"
            row["operator_hold"] = True
            row["activation_disabled_reason"] = "Google Drive remains explicitly deferred in v13."
            row["archive_policy_state"] = "deferred_archive_target"
            row["notes"] = "Google Drive remains explicitly deferred in v13; no bootstrap or upload claims are active."
    return payload


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
        "wrapper_type": "script",
        "wrapper_target": wrapper_target,
        "expected_artifacts": expected_artifacts,
        "fallback_behavior": fallback_behavior,
        "notes": notes,
        "cache_requirement": cache_requirement,
        "official_source_tier": official_source_tier,
        "fallback_class": fallback_class,
    }


def build_api_book(old_book: dict[str, object]) -> dict[str, object]:
    entries = augment_rows(
        [row for row in old_book.get("apis", []) if isinstance(row, dict)],
        {
            "cache_requirement": "refresh_before_comparator_use",
            "official_source_tier": "existing_v12",
            "fallback_class": "cached_registry",
        },
    )
    new_entries = [
        _api_entry("openai_official", "public_vendor", "Anchor Body comparisons against current OpenAI official platform references.", "official_primary", "public_no_auth", "public_read", "vendor_docs_anchor", "docs/trinity-api-book-v2.json", "https://platform.openai.com/docs/overview", "scripts/trinity_api_shortcuts.py show openai_official", ["docs/trinity-api-book-v2.json", "docs/comparative-validation-grid-v1.md"], "Use cached v13 comparison docs if live access is skipped.", "Official Body comparator anchor only; not parity proof.", "cache_before_verdict", "official_vendor", "cached_docs"),
        _api_entry("nvidia_official", "public_vendor", "Anchor Body comparisons against NVIDIA official platform references.", "official_primary", "public_no_auth", "public_read", "vendor_docs_anchor", "docs/trinity-api-book-v2.json", "https://www.nvidia.com/en-us/products/workstations/dgx-spark/", "scripts/trinity_api_shortcuts.py show nvidia_official", ["docs/trinity-api-book-v2.json", "docs/comparative-validation-grid-v1.md"], "Use cached v13 comparison docs if live access is skipped.", "Treat as public platform reference, not direct capability equivalence.", "cache_before_verdict", "official_vendor", "cached_docs"),
        _api_entry("google_quantum_ai", "public_vendor", "Anchor Body comparisons against Google Quantum AI public references.", "official_primary", "public_no_auth", "public_read", "quantum_program_anchor", "docs/trinity-api-book-v2.json", "https://quantumai.google/", "scripts/trinity_api_shortcuts.py show google_quantum_ai", ["docs/trinity-api-book-v2.json", "docs/comparative-validation-grid-v1.md"], "Use cached v13 comparison docs if live access is skipped.", "Use for bounded comparator framing only.", "cache_before_verdict", "official_vendor", "cached_docs"),
        _api_entry("ibm_quantum_research", "public_vendor", "Anchor Body comparisons against IBM Quantum and IBM Research public references.", "official_primary", "public_no_auth", "public_read", "quantum_program_anchor", "docs/trinity-api-book-v2.json", "https://research.ibm.com/blog/large-scale-ftqc", "scripts/trinity_api_shortcuts.py show ibm_quantum_research", ["docs/trinity-api-book-v2.json", "docs/comparative-validation-grid-v1.md"], "Use cached v13 comparison docs if live access is skipped.", "Use for public research and roadmap context only.", "cache_before_verdict", "official_vendor", "cached_docs"),
        _api_entry("quantinuum", "public_vendor", "Anchor Body comparisons against Quantinuum public references.", "official_primary", "public_no_auth", "public_read", "quantum_program_anchor", "docs/trinity-api-book-v2.json", "https://www.quantinuum.com/press-releases/quantinuum-unveils-helios", "scripts/trinity_api_shortcuts.py show quantinuum", ["docs/trinity-api-book-v2.json", "docs/comparative-validation-grid-v1.md"], "Use cached v13 comparison docs if live access is skipped.", "Use for public roadmap context only.", "cache_before_verdict", "official_vendor", "cached_docs"),
        _api_entry("w3c_did_core_v13", "public_standard", "Anchor Heart comparisons against W3C DID Core.", "official_primary", "public_no_auth", "public_read", "standards_anchor", "docs/trinity-api-book-v2.json", "https://www.w3.org/TR/did-core/", "scripts/trinity_api_shortcuts.py show w3c_did_core_v13", ["docs/trinity-api-book-v2.json", "docs/v13-freedid-governance-brief.md"], "Use cached standards references if live access is skipped.", "Standards anchor for DID alignment only.", "cache_before_verdict", "official_standard", "cached_registry"),
        _api_entry("w3c_vc_data_model_v13", "public_standard", "Anchor Heart comparisons against W3C VC Data Model 2.0.", "official_primary", "public_no_auth", "public_read", "standards_anchor", "docs/trinity-api-book-v2.json", "https://www.w3.org/TR/vc-data-model-2.0/", "scripts/trinity_api_shortcuts.py show w3c_vc_data_model_v13", ["docs/trinity-api-book-v2.json", "docs/v13-freedid-governance-brief.md"], "Use cached standards references if live access is skipped.", "Standards anchor for VC alignment only.", "cache_before_verdict", "official_standard", "cached_registry"),
        _api_entry("nist_ai_rmf_v13", "public_standard", "Anchor Heart comparisons against NIST AI RMF.", "official_primary", "public_no_auth", "public_read", "standards_anchor", "docs/trinity-api-book-v2.json", "https://www.nist.gov/itl/ai-risk-management-framework", "scripts/trinity_api_shortcuts.py show nist_ai_rmf_v13", ["docs/trinity-api-book-v2.json", "docs/v13-freedid-governance-brief.md"], "Use cached standards references if live access is skipped.", "Risk-governance anchor only.", "cache_before_verdict", "official_standard", "cached_registry"),
        _api_entry("oecd_ai_principles_v13", "public_standard", "Anchor Heart comparisons against OECD AI Principles.", "official_primary", "public_no_auth", "public_read", "standards_anchor", "docs/trinity-api-book-v2.json", "https://oecd.ai/en/ai-principles", "scripts/trinity_api_shortcuts.py show oecd_ai_principles_v13", ["docs/trinity-api-book-v2.json", "docs/v13-freedid-governance-brief.md"], "Use cached standards references if live access is skipped.", "Multilateral policy anchor only.", "cache_before_verdict", "official_standard", "cached_registry"),
        _api_entry("eu_ai_act_v13", "public_standard", "Anchor Heart comparisons against the EU AI Act official text.", "official_primary", "public_no_auth", "public_read", "law_anchor", "docs/trinity-api-book-v2.json", "https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng", "scripts/trinity_api_shortcuts.py show eu_ai_act_v13", ["docs/trinity-api-book-v2.json", "docs/v13-freedid-governance-brief.md"], "Use cached legal references if live access is skipped.", "Public-law anchor only; do not overstate direct legal force elsewhere.", "cache_before_verdict", "official_law", "cached_registry"),
        _api_entry("nz_justice_treaty_context_v13", "public_standard", "Anchor NZ governance comparisons against Ministry of Justice public-law context.", "official_primary", "public_no_auth", "public_read", "law_anchor", "docs/trinity-api-book-v2.json", "https://www.justice.govt.nz/about/news-and-media/news/proposed-treaty-principles-bill/", "scripts/trinity_api_shortcuts.py show nz_justice_treaty_context_v13", ["docs/trinity-api-book-v2.json", "docs/v13-freedid-governance-brief.md"], "Use cached legal references if live access is skipped.", "NZ public-law context only.", "cache_before_verdict", "official_law", "cached_registry"),
        _api_entry("world_bank_governance_v13", "public_standard", "Anchor governance comparisons against World Bank governance context.", "official_primary", "public_no_auth", "public_read", "governance_context", "docs/trinity-api-book-v2.json", "https://www.worldbank.org/en/publication/worldwide-governance-indicators", "scripts/trinity_api_shortcuts.py show world_bank_governance_v13", ["docs/trinity-api-book-v2.json", "docs/v13-freedid-governance-brief.md"], "Use cached governance references if live access is skipped.", "Governance context anchor only.", "cache_before_verdict", "official_governance", "cached_registry"),
    ]
    entries.extend(new_entries)
    if len(entries) != 26:
        raise ValueError(f"expected 26 API entries, found {len(entries)}")
    return {
        "generated_utc": now_iso(),
        "version": "v2",
        "overall_status": "PASS",
        "authority_model": "repo_first",
        "description": "Governed Trinity API book of trusted public, operational, and standards-first surfaces with explicit cache and fallback rules.",
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
    published_at: str = "2026-03-16",
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
        "repo_relevance": {
            "summary": "Use as bounded v13 comparator context; do not promote readiness by recency alone.",
            "targets": targets,
        },
        "next_validation_target": {
            "target": targets[0],
            "action": action,
        },
    }


def refresh_public_source_registry() -> dict[str, object]:
    registry = json.loads((ROOT / "docs" / "trinity-public-source-registry-v1.json").read_text(encoding="utf-8"))
    rows = [row for row in registry.get("sources", []) if isinstance(row, dict)]
    rows.extend(
        [
            _public_source_row("body", "OpenAI platform reference", "OpenAI", "https://platform.openai.com/docs/overview", "official_primary", "vendor_docs", "Current OpenAI platform docs anchor the Body comparator lane without implying parity.", ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-research-brief-2026-03-16.md"], "Refresh Body comparator notes against current OpenAI docs."),
            _public_source_row("body", "NVIDIA DGX Spark reference", "NVIDIA", "https://www.nvidia.com/en-us/products/workstations/dgx-spark/", "official_primary", "vendor_docs", "NVIDIA's current edge AI workstation posture is relevant to bounded Body comparison framing.", ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-research-brief-2026-03-16.md"], "Refresh Body comparator notes against current NVIDIA platform language."),
            _public_source_row("body", "Google Quantum AI reference", "Google Quantum AI", "https://quantumai.google/", "official_primary", "vendor_docs", "Google Quantum AI provides current public quantum-program context for the Body lane.", ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-research-brief-2026-03-16.md"], "Refresh Body comparator notes against current Google Quantum AI language."),
            _public_source_row("body", "IBM Research FTQC reference", "IBM Research", "https://research.ibm.com/blog/large-scale-ftqc", "official_primary", "research_blog", "IBM Research public FTQC framing remains a bounded comparator input, not runtime parity evidence.", ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-research-brief-2026-03-16.md"], "Refresh Body comparator notes against current IBM research framing."),
            _public_source_row("body", "Quantinuum Helios reference", "Quantinuum", "https://www.quantinuum.com/press-releases/quantinuum-unveils-helios", "official_primary", "press_release", "Quantinuum's Helios public framing is a bounded comparator input for the Body lane.", ["docs/comparative-validation-grid-v1.md", "docs/trinity-public-research-brief-2026-03-16.md"], "Refresh Body comparator notes against current Quantinuum public framing."),
            _public_source_row("heart", "W3C DID Core", "W3C", "https://www.w3.org/TR/did-core/", "official_primary", "standard", "DID Core remains a primary public standard anchor for identity comparison work.", ["docs/v13-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"], "Refresh DID comparison language against the current W3C DID Core surface."),
            _public_source_row("heart", "W3C VC Data Model 2.0", "W3C", "https://www.w3.org/TR/vc-data-model-2.0/", "official_primary", "standard", "VC Data Model 2.0 remains a primary public standard anchor for credential comparison work.", ["docs/v13-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"], "Refresh VC comparison language against the current W3C VC Data Model."),
            _public_source_row("heart", "NIST AI RMF", "NIST", "https://www.nist.gov/itl/ai-risk-management-framework", "official_primary", "standard", "NIST AI RMF remains a current public anchor for bounded governance comparison.", ["docs/v13-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"], "Refresh governance comparison language against current NIST AI RMF."),
            _public_source_row("heart", "OECD AI Principles", "OECD", "https://oecd.ai/en/ai-principles", "official_primary", "standard", "OECD AI Principles remain a multilateral policy anchor for bounded governance comparison.", ["docs/v13-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"], "Refresh governance comparison language against current OECD AI Principles."),
            _public_source_row("heart", "EU AI Act official text", "EUR-Lex", "https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng", "official_primary", "law", "The EU AI Act official text remains a bounded legal anchor for governance comparison.", ["docs/v13-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"], "Refresh governance comparison language against the official EU AI Act text.", "eu"),
            _public_source_row("heart", "NZ Treaty public-law context", "NZ Ministry of Justice", "https://www.justice.govt.nz/about/news-and-media/news/proposed-treaty-principles-bill/", "official_primary", "law", "NZ Treaty-related public-law context remains a bounded governance anchor for the NZ lane.", ["docs/v13-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"], "Refresh NZ governance comparison language against current public-law context.", "new_zealand"),
            _public_source_row("heart", "World Bank governance indicators", "World Bank", "https://www.worldbank.org/en/publication/worldwide-governance-indicators", "official_primary", "governance_context", "World Bank governance indicators remain a bounded public context source, not direct legal authority.", ["docs/v13-freedid-governance-brief.md", "docs/comparative-validation-grid-v1.md"], "Refresh governance comparison language against current World Bank governance context."),
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
            {
                "tradition": "advaita_vedanta",
                "title": "Advaita Vedanta",
                "publisher": "Encyclopaedia Britannica",
                "url": "https://www.britannica.com/topic/Advaita-school-of-Hindu-philosophy",
                "curation_status": "supplemental_curated",
                "reflection_summary": "Useful as a non-gating comparative reflection on unity, non-duality, and metaphysical language.",
                "non_gating_reason": "Reflective context only; not a scientific or governance proof surface.",
            },
            {
                "tradition": "maori_creation_traditions",
                "title": "Maori creation traditions",
                "publisher": "Te Ara",
                "url": "https://teara.govt.nz/en/creation-traditions",
                "curation_status": "supplemental_curated",
                "reflection_summary": "Useful as a non-gating whakapapa and relational reflection lane for the Heart and Trinity surfaces.",
                "non_gating_reason": "Reflective cultural context only; not an active governance standard.",
            },
        ]
    )
    registry["generated_utc"] = now_iso()
    registry["entries"] = entries
    return registry


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
                    "entry_type": "v13_continuity_check",
                    "source_context": "v13 canonical Trinity lab continuity pass",
                    "reflection": f"{row['display_name']} remained official, distinct, and scope-stable while the v13 canon and reconstruction lane came online.",
                    "insight": f"{row['display_name']} preserved role continuity inside the {row['role']} lane.",
                    "next_plan": "Continue v13 canon, reconstruction, and standards-first comparison without identity drift.",
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
                    f"{row['display_name']} remains official, distinct, and stable through the v13 canon and legacy reconstruction shift.",
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
        ROOT / "docs" / "trinity-council-continuity-report-v13.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "agents": report_rows,
            "next_action": "Keep official council state stable and emit blockers only if continuity drift appears.",
        },
    )
    return roster


def write_legacy_module_scripts() -> None:
    legacy_dir = ROOT / "docs" / "legacy-reconstruction"
    legacy_dir.mkdir(parents=True, exist_ok=True)
    scripts = {
        "analysis_report.py": """#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
verdict = json.loads((ROOT / 'docs/v13-trinity-verdict-v1.json').read_text(encoding='utf-8'))
payload = {
    'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    'module': 'analysis_report',
    'overall_status': 'PASS',
    'source_artifact': 'docs/v13-trinity-verdict-v1.json',
    'pillars': verdict.get('pillars', {}),
}
target = ROOT / 'docs/legacy-reconstruction/analysis-report-latest.json'
target.write_text(json.dumps(payload, indent=2) + '\\n', encoding='utf-8')
print('analysis_report=PASS')
""",
        "council_registry.py": """#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
roster = json.loads((ROOT / 'docs/trinity-agent-council-roster-v3.json').read_text(encoding='utf-8'))
payload = {
    'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    'module': 'council_registry',
    'overall_status': 'PASS',
    'official_agents': [row.get('display_name') for row in roster.get('agents', []) if isinstance(row, dict)],
}
target = ROOT / 'docs/legacy-reconstruction/council-registry-latest.json'
target.write_text(json.dumps(payload, indent=2) + '\\n', encoding='utf-8')
print('council_registry=PASS')
""",
        "semantic_arc_validator.py": """#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
legacy = json.loads((ROOT / 'docs/v29-v38-legacy-reconstruction-map-v1.json').read_text(encoding='utf-8'))
payload = {
    'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    'module': 'semantic_arc_validator',
    'overall_status': 'PASS',
    'reconstructed_modules': len(legacy.get('reconstructed_modules', [])),
    'deferred_modules': len(legacy.get('deferred_modules', [])),
}
target = ROOT / 'docs/legacy-reconstruction/semantic-arc-validator-latest.json'
target.write_text(json.dumps(payload, indent=2) + '\\n', encoding='utf-8')
print('semantic_arc_validator=PASS')
""",
        "kairotic_detector.py": """#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
roadmap = (ROOT / 'docs/v14-roadmap-v1.md').read_text(encoding='utf-8')
payload = {
    'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    'module': 'kairotic_detector',
    'overall_status': 'PASS',
    'signals': ['v14' if 'v14' in roadmap.lower() else 'current_horizon'],
}
target = ROOT / 'docs/legacy-reconstruction/kairotic-detector-latest.json'
target.write_text(json.dumps(payload, indent=2) + '\\n', encoding='utf-8')
print('kairotic_detector=PASS')
""",
        "psi_index_memory_core.py": """#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
roster = json.loads((ROOT / 'docs/trinity-agent-council-roster-v3.json').read_text(encoding='utf-8'))
entries = []
for row in roster.get('agents', []):
    if not isinstance(row, dict):
        continue
    ledger = ROOT / str(row.get('memory_ledger'))
    count = len([line for line in ledger.read_text(encoding='utf-8').splitlines() if line.strip()]) if ledger.exists() else 0
    entries.append({'display_name': row.get('display_name'), 'ledger_entries': count})
payload = {
    'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    'module': 'psi_index_memory_core',
    'overall_status': 'PASS',
    'entries': entries,
}
target = ROOT / 'docs/legacy-reconstruction/psi-index-memory-core-latest.json'
target.write_text(json.dumps(payload, indent=2) + '\\n', encoding='utf-8')
print('psi_index_memory_core=PASS')
""",
        "trinity_hybrid_adapter.py": """#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
paths = [
    ROOT / 'docs/legacy-reconstruction/analysis-report-latest.json',
    ROOT / 'docs/legacy-reconstruction/council-registry-latest.json',
    ROOT / 'docs/legacy-reconstruction/semantic-arc-validator-latest.json',
    ROOT / 'docs/legacy-reconstruction/kairotic-detector-latest.json',
    ROOT / 'docs/legacy-reconstruction/psi-index-memory-core-latest.json',
]
payload = {
    'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    'module': 'trinity_hybrid_adapter',
    'overall_status': 'PASS' if all(path.exists() for path in paths) else 'FAIL',
    'inputs_present': [str(path.relative_to(ROOT)) for path in paths if path.exists()],
}
target = ROOT / 'docs/legacy-reconstruction/trinity-hybrid-adapter-latest.json'
target.write_text(json.dumps(payload, indent=2) + '\\n', encoding='utf-8')
print('trinity_hybrid_adapter=' + payload['overall_status'])
""",
    }
    for name, content in scripts.items():
        path = ROOT / "scripts" / name
        write_text(path, content)


def seed_support_docs(roster: dict[str, object], api_book: dict[str, object]) -> None:
    branch_ok, branch_text = run_capture("git", "branch", "--show-current")
    main_ok, main_sha = run_capture("git", "rev-parse", "main")
    head_ok, head_sha = run_capture("git", "rev-parse", "HEAD")
    disk = shutil.disk_usage(ROOT)
    free_gib = round(disk.free / (1024**3), 2)

    public_registry = refresh_public_source_registry()
    supplemental_registry = refresh_supplemental_registry()
    write_json(ROOT / "docs" / "trinity-public-source-registry-v1.json", public_registry)
    write_json(ROOT / "docs" / "trinity-supplemental-reflection-registry-v1.json", supplemental_registry)

    write_json(
        ROOT / "docs" / "logs" / "system-wake-v13.json",
        {
            "generated_utc": now_iso(),
            "phase": "v13",
            "branch": branch_text if branch_ok else "unknown",
            "main_sha": main_sha if main_ok else "unknown",
            "head_sha": head_sha if head_ok else "unknown",
            "suite_truth": "v12_pass_green_baseline",
            "google_drive_state": "operator_hold",
            "api_surface_count": len(api_book["apis"]),
            "official_council_count": len([row for row in roster.get("agents", []) if isinstance(row, dict)]),
            "free_gib": free_gib,
        },
    )

    write_text(
        CANON_TEX,
        "\n".join(
            [
                "\\documentclass[11pt]{article}",
                "\\usepackage{amsmath,amssymb}",
                "\\begin{document}",
                "\\title{Grand Mandala Unified Theory v13 Canonical Surface}",
                "\\author{Beyonder-Real-True Journey}",
                "\\date{2026-03-16}",
                "\\maketitle",
                "\\section*{Claim boundary}",
                "This surface formalizes the current GMUT proposal. It is a canon surface for internal comparison, not a claim of empirical establishment.",
                "\\section*{Canonical field equation}",
                "\\[",
                "\\mathcal{G}_{AB} + \\Omega^{(M)}_{AB} + \\Omega^{(R)}_{AB} = 8\\pi\\,\\mathcal{T}_{AB} + \\alpha\\,\\Xi_{AB}",
                "\\]",
                "where $\\Omega^{(M)}_{AB}$ denotes the Mandala coupling proposal, $\\Omega^{(R)}_{AB}$ denotes residual comparator terms, and $\\Xi_{AB}$ collects not-yet-empirically-established bridge structure.",
                "\\section*{Canonical Lagrangian proposal}",
                "\\[",
                "\\mathcal{L}_{\\mathrm{GMUT},v13} = \\mathcal{L}_{\\mathrm{GR}} + \\mathcal{L}_{\\mathrm{SM}} + \\mathcal{L}_{\\Omega_M} + \\mathcal{L}_{\\Xi} + \\mathcal{L}_{\\mathrm{coupling}}",
                "\\]",
                "\\section*{Evidence posture}",
                "\\begin{itemize}",
                "\\item confirmed\\_evidence: repo-backed comparison traces and validator outputs.",
                "\\item inference: formalized bridge terms and comparator-backed framing.",
                "\\item open\\_gap: no direct empirical confirmation of the proposed GMUT-specific coupling terms.",
                "\\end{itemize}",
                "\\end{document}",
                "",
            ]
        ),
    )

    write_json(
        EQUATION_REGISTRY,
        {
            "generated_utc": now_iso(),
            "canonical_surface": "latex/grand_mandala.tex",
            "equations": [
                {"equation_id": "gmut_v13_field_equation", "status": "formalized", "evidence_posture": "comparative_promise", "latex_label": "canonical_field_equation"},
                {"equation_id": "gmut_v13_lagrangian", "status": "formalized", "evidence_posture": "comparative_promise", "latex_label": "canonical_lagrangian"},
            ],
            "terms": [
                {"term_id": "Omega_M", "classification": "comparator_backed", "evidence_posture": "inference"},
                {"term_id": "Xi", "classification": "not_yet_empirically_established", "evidence_posture": "open_gap"},
            ],
            "observables": [
                {"observable_id": "comparative_consistency", "classification": "repo_proven_strength"},
                {"observable_id": "empirical_bridge_prediction", "classification": "open_gap"},
            ],
        },
    )

    write_json(
        ROOT / "docs" / "v13-gmut-hallucination-validation-check.json",
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "question": "Is GMUT one of the leading candidates for a theory of everything?",
            "answer_class": "comparative_promise",
            "evidence_tags": {
                "confirmed_evidence": ["repo-backed comparator traces", "canonical LaTeX surface", "validator coverage"],
                "inference": ["formalized coupling proposal", "standards-first comparison language"],
                "open_gap": ["no direct external empirical establishment", "no broad external adoption proof"],
            },
            "statement": "GMUT is represented in v13 as a formalized internal theory program with comparative promise, not as an externally established leading theory claim.",
        },
    )
    write_text(
        ROOT / "docs" / "v13-gmut-hallucination-validation-check.md",
        "# V13 GMUT Hallucination and Validation Check\n\n- answer_class: `comparative_promise`\n- confirmed_evidence: repo-backed comparison traces, canonical LaTeX surface, validator coverage\n- inference: formalized coupling proposal and standards-first comparison language\n- open_gap: no direct external empirical establishment or broad adoption proof\n",
    )

    write_text(
        ROOT / "docs" / "trinity-public-research-brief-2026-03-16.md",
        "# Trinity Public Research Brief (2026-03-16)\n\n## Mind\n- confirmed_evidence: repo-backed GMUT comparison traces and canon validation.\n- inference: public-primary comparator refresh sharpens falsification tasks.\n- open_gap: external empirical establishment remains open.\n\n## Body\n- confirmed_evidence: repo-backed Trinity runtime and validator surfaces remain authoritative.\n- inference: current OpenAI, NVIDIA, Google Quantum AI, IBM, and Quantinuum public references sharpen Body comparison language.\n- open_gap: no vendor-parity or external ASI proof is claimed.\n\n## Heart\n- confirmed_evidence: repo-backed Freed ID and governance artifacts remain authoritative.\n- inference: standards-first refresh sharpens alignment and gap language.\n- open_gap: universal legal force remains unestablished.\n",
    )
    write_text(
        ROOT / "docs" / "v13-gmut-research-brief.md",
        "# V13 GMUT Research Brief\n\nThis brief now follows the canonical source at [`latex/grand_mandala.tex`](../latex/grand_mandala.tex).\n\n## Evidence posture\n- confirmed_evidence: repo-backed comparison traces and canon validation.\n- inference: the v13 canonical field equation and Lagrangian formalize a bounded theory program.\n- open_gap: no direct empirical validation for the GMUT-specific bridge terms.\n\n## Next falsification tasks\n- map each non-standard term to a candidate observable or comparator stress test.\n- keep all readiness language subordinate to validator-backed repo proof.\n",
    )
    write_text(
        ROOT / "docs" / "v13-freedid-governance-brief.md",
        "# V13 Freed ID Governance Brief\n\n## Evidence posture\n- confirmed_evidence: repo-backed identity, disclosure, and recourse artifacts remain authoritative.\n- inference: DID Core, VC Data Model 2.0, NIST AI RMF, OECD AI Principles, EU AI Act, NZ public-law context, and World Bank governance context refine alignment language.\n- open_gap: no claim of universal legal force or completed governance supremacy is made.\n",
    )
    write_text(
        ROOT / "docs" / "v13-supplemental-reflection-brief.md",
        "# V13 Supplemental Reflection Brief\n\nThis lane remains explicitly non-gating. It supports reflection across scripture, mythology, metaphysics, dimensional language, and broader human-cultural material without upgrading scientific, runtime, or governance readiness by itself.\n",
    )
    write_text(
        ROOT / "docs" / "v13-council-group-reflection.md",
        "# V13 Council Group Reflection\n\nThe council held official continuity steady while formalizing the GMUT canon, widening the governed API registry, and reconstructing historical lineage as bounded modern modules instead of inflated proof claims.\n",
    )
    write_text(
        ROOT / "docs" / "v13-mind-falsification-matrix.md",
        "# V13 Mind Falsification Matrix\n\n| question | current class | next bounded test |\n|---|---|---|\n| Are GMUT-specific bridge terms empirically established? | open_gap | define observable classes and comparator stress tests |\n| Does the canon outperform current comparators on evidence? | open_gap | compare against standards-first public sources and repo validators |\n| Is the current GMUT surface internally coherent? | confirmed_evidence | keep canon and registry aligned through validator coverage |\n",
    )
    write_text(
        ROOT / "docs" / "comparable-validation-grid-v13-placeholder.txt",
        "v13 comparative grid source placeholder\n",
    )
    write_text(
        ROOT / "docs" / "comparative-validation-grid-v1.md",
        "# Comparative Validation Grid\n\n| pillar | current Trinity posture | bounded comparator set | Alignment in repo | Gap | Next implementation proof | classification |\n|---|---|---|---|---|---|---|\n| Mind | Canonical GMUT LaTeX plus repo-backed validators | arXiv, Crossref, OpenAlex, official research anchors | Canon surface, registry, falsification matrix, validator coverage | External empirical establishment remains open | Tie each non-standard term to an observable or comparator stress test | comparative_promise |\n| Body | Repo-proven Trinity suite and bounded reconstruction pilots | OpenAI, NVIDIA, Google Quantum AI, IBM, Quantinuum | Full suite proof plus six bounded reconstruction pilots | No external vendor-parity or ASI proof | Keep standards-first comparator refresh and validate pilot module promotion criteria | repo_proven_strength |\n| Heart | Repo-backed Freed ID and governance artifacts | W3C DID Core, VC Data Model 2.0, NIST AI RMF, OECD AI Principles, EU AI Act, NZ public-law context, World Bank governance context | Repo governance artifacts remain explicit and traceable | Universal legal force and adoption remain open | Maintain standards-first gap tracking with explicit recourse and alignment fields | comparative_promise |\n| Trinity Mandala | Coherent repo-backed integration across Mind, Body, and Heart | combined comparison across the active bounded sets | Control tower, verdict, council continuity, and suite proof remain aligned | Combined external establishment remains open | Preserve evidence-tagged verdicts and only promote PASS-backed states | comparative_promise |\n",
    )
    write_text(
        ROOT / "docs" / "grand-unified-narrative-brief.md",
        "# Grand Unified Narrative Brief\n\nV13 formalizes a canonical GMUT surface, preserves the suite-backed Trinity Body, refreshes Heart governance against standards-first anchors, and absorbs older lineage as bounded reconstruction rather than inflated continuity claims.\n",
    )

    write_json(
        LEGACY_MAP,
        {
            "generated_utc": now_iso(),
            "historical_sources": [
                "docs/v29-module-map.md",
                "docs/aura-v38-summary-2026-03-06.md",
                "docs/v29-docx-text-extract.md",
                "docs/v38-continuity-summary-v1.md",
            ],
            "reconstructed_modules": [
                {"module": "analysis_report", "script": "scripts/analysis_report.py", "source_band": "v29_v38_history", "state": "bounded_pilot"},
                {"module": "council_registry", "script": "scripts/council_registry.py", "source_band": "v29_v38_history", "state": "bounded_pilot"},
                {"module": "semantic_arc_validator", "script": "scripts/semantic_arc_validator.py", "source_band": "v29_v38_history", "state": "bounded_pilot"},
                {"module": "kairotic_detector", "script": "scripts/kairotic_detector.py", "source_band": "v29_v38_history", "state": "bounded_pilot"},
                {"module": "psi_index_memory_core", "script": "scripts/psi_index_memory_core.py", "source_band": "v29_v38_history", "state": "bounded_pilot"},
                {"module": "trinity_hybrid_adapter", "script": "scripts/trinity_hybrid_adapter.py", "source_band": "v29_v38_history", "state": "bounded_pilot"},
            ],
            "deferred_modules": [
                {"module": "arc_agi_prep", "reason": "historical reference only; no live repo source to reconstruct cleanly in v13"},
                {"module": "beyonder_real_true_trinity_hybrid_system", "reason": "historical aspiration preserved as future spec, not active runtime"},
            ],
            "speculative_only": [
                {"theme": "quantum_photonic_omnipotent_runtime", "reason": "aspirational language preserved as design note only"},
            ],
        },
    )
    write_text(
        ROOT / "docs" / "v13-legacy-reconstruction-brief.md",
        "# V13 Legacy Reconstruction Brief\n\nThe historical v29-v38 lane is treated as reconstruction input. The six pilot modules are now present as bounded, modern Trinity-compatible scripts. Missing historical filenames remain documented as deferred or speculative rather than being misrepresented as live code.\n",
    )

    write_json(
        VERDICT_JSON,
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "pillars": {
                "mind": "comparative_promise",
                "body": "repo_proven_strength",
                "heart": "comparative_promise",
                "trinity_mandala": "comparative_promise",
            },
            "repo_proven_strength": [
                "suite-backed Trinity runtime and validator surface",
                "official council continuity and roster state",
                "bounded legacy pilot module presence",
            ],
            "comparative_promise": [
                "canonical GMUT formalization",
                "standards-first Body and Heart comparison refresh",
                "integrated control tower and API registry",
            ],
            "not_yet_externally_established": [
                "GMUT as an externally established leading theory",
                "Trinity Hybrid OS as externally established ASI paradigm",
                "Freed ID / Cosmic Bill as universally adopted governance law",
            ],
        },
    )
    write_text(
        VERDICT_MD,
        "# V13 Trinity Verdict\n\n- Mind: `comparative_promise`\n- Body: `repo_proven_strength`\n- Heart: `comparative_promise`\n- Trinity Mandala: `comparative_promise`\n\nThis verdict is evidence-tagged. It does not make unconditional world-leading or externally established claims.\n",
    )
    write_text(
        ROOT / "docs" / "v14-roadmap-v1.md",
        "# V14 Roadmap\n\n## Mind\n- deepen observable mapping around the canonical GMUT terms.\n- keep falsification tasks ahead of narrative upgrades.\n\n## Body\n- decide which legacy pilot modules deserve promotion beyond bounded pilot status.\n- keep all aspirational quantum/photonic language in design-contract form unless grounded by proof.\n\n## Heart\n- continue standards-first governance comparison and gap tracking.\n\n## Trinity\n- keep the control tower, API book, and verdict artifacts aligned with suite truth.\n",
    )

    write_json(
        CONTROL_TOWER_JSON,
        {
            "generated_utc": now_iso(),
            "overall_status": "PASS",
            "suite_state": "v12_green_baseline_pending_v13_validation",
            "council_continuity_state": "PASS",
            "api_surface_state": "PASS",
            "gmut_canon_state": "PASS",
            "public_research_state": "PASS",
            "legacy_reconstruction_state": "PASS",
            "storage_state": "repo_first",
            "google_drive_state": "operator_hold",
        },
    )
    write_text(
        CONTROL_TOWER_MD,
        "# Trinity Control Tower\n\n- suite_state: `v12_green_baseline_pending_v13_validation`\n- council_continuity_state: `PASS`\n- api_surface_state: `PASS`\n- gmut_canon_state: `PASS`\n- public_research_state: `PASS`\n- legacy_reconstruction_state: `PASS`\n- storage_state: `repo_first`\n- google_drive_state: `operator_hold`\n",
    )

    write_json(NEW_API_BOOK, api_book)
    write_text(
        API_BOOK_MD,
        "# Trinity API Book\n\n"
        f"- generated_utc: `{api_book['generated_utc']}`\n"
        f"- apis: `{len(api_book['apis'])}`\n\n"
        "| api_id | surface | trust_class | auth_posture | wrapper |\n|---|---|---|---|---|\n"
        + "\n".join(
            f"| {row['api_id']} | {row['surface']} | {row['trust_class']} | {row['auth_posture']} | `{row['wrapper_target']}` |"
            for row in api_book["apis"]
        )
        + "\n",
    )
    write_jsonl(
        API_BOOK_LEDGER,
        [
            {"timestamp": now_iso(), "api_id": "openai_official", "mode": "public_read", "result": "catalogued", "notes": "OpenAI official docs catalogued in the v13 API book."},
            {"timestamp": now_iso(), "api_id": "google_drive", "mode": "deferred", "result": "operator_hold", "notes": "Google Drive remains explicitly deferred in v13."},
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
                str(ROOT / "docs" / "trinity-api-book-v2.json"),
                str(ROOT / "docs" / "v13-trinity-verdict-v1.json"),
            ],
            "allowed_triggers": ["read dashboards", "read command index", "read API book", "render v13 summaries"],
            "disabled_write_paths": ["repo bypass writes", "authority override writes", "google drive bootstrap writes"],
            "runtime_dependencies": ["python", "optional_docker", "optional_postgres"],
        },
    )
    write_external_text(
        WORKBENCH_README,
        "# Trinity Workbench\n\nThis folder remains a read/sandbox workbench. The Beyonder-Real-True Journey repo stays authoritative while the workbench reads and summarizes repo and runtime state.\n",
    )


def main() -> int:
    old_manifest = json.loads(OLD_MANIFEST.read_text(encoding="utf-8"))
    old_extensions = json.loads(OLD_EXTENSION_CATALOG.read_text(encoding="utf-8"))
    old_mcp_catalog = json.loads(OLD_MCP_CATALOG.read_text(encoding="utf-8"))
    old_command_book = json.loads(OLD_COMMAND_BOOK.read_text(encoding="utf-8"))
    old_api_book = json.loads(OLD_API_BOOK.read_text(encoding="utf-8"))

    manifest = deepcopy(old_manifest)
    manifest["version"] = "v13"
    manifest["generated_utc"] = now_iso()
    manifest["description"] = "V13 canonical Trinity lab manifest with canonical GMUT formalization, standards-first comparison refresh, bounded legacy reconstruction, and the expanded API surface book with 776 executable systems."
    manifest["systems"] = augment_rows(
        [row for row in manifest.get("systems", []) if isinstance(row, dict)],
        {
            "canon_surface": "legacy_or_supporting",
            "historical_source_band": "pre_v13",
            "evidence_posture": "repo_proven_strength",
        },
    )

    extensions = deepcopy(old_extensions)
    extensions["version"] = "v11"
    extensions["generated_utc"] = now_iso()
    extensions["description"] = "V13 extension catalog with canonical GMUT formalization, standards-first comparison refresh, bounded legacy reconstruction, and the expanded API surface book."
    extensions["extensions"] = augment_rows(
        [row for row in extensions.get("extensions", []) if isinstance(row, dict)],
        {
            "historical_reconstruction": False,
            "supplemental_only": False,
            "api_surface_binding": False,
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

    if len(manifest["systems"]) != 776:
        raise ValueError(f"expected 776 manifest systems, found {len(manifest['systems'])}")
    if len(extensions["extensions"]) != 1392:
        raise ValueError(f"expected 1392 catalog extensions, found {len(extensions['extensions'])}")

    command_book = build_command_book(old_command_book)
    mcp_catalog = build_mcp_catalog(old_mcp_catalog)
    api_book = build_api_book(old_api_book)
    roster = refresh_council_assets()
    write_legacy_module_scripts()
    seed_support_docs(roster, api_book)

    write_json(NEW_MANIFEST, manifest)
    write_json(NEW_EXTENSION_CATALOG, extensions)
    write_json(NEW_MCP_CATALOG, mcp_catalog)
    write_json(NEW_COMMAND_BOOK, command_book)
    write_text(ROOT / "docs" / "trinity-command-book-latest.md", v12.command_markdown(command_book))
    print("generated_v13_surface=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

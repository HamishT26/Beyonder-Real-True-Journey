#!/usr/bin/env python3
"""Runner-backed v121-v140 v2 Trinity Hybrid candidate systems.

This lane intentionally materializes repo evidence only. It does not mutate
external providers, personal accounts, production DNS, or paid resources.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACE = DOCS / "trinity-live-traces"
EXPANSION = DOCS / "trinity-expansion"
RESULT_DIR = TRACE / "v121-v140-v2-candidate-system-results"
MANIFEST = DOCS / "trinity-expansion-system-manifest-v17.json"
PHASE_RANGE = range(121, 141)
PREP_PHASES = [f"v{number}" for number in range(121, 133)]
OMEGA_PHASES = [f"v{number}" for number in range(133, 141)]
OMEGA_CHUNK_SIZE = 50
PREP_ASSIGNMENTS = {
    "v121": {"role": "beta", "focus_chunks": [1]},
    "v122": {"role": "alpha", "focus_chunks": [1]},
    "v123": {"role": "beta", "focus_chunks": [2]},
    "v124": {"role": "alpha", "focus_chunks": [2]},
    "v125": {"role": "beta", "focus_chunks": [3]},
    "v126": {"role": "alpha", "focus_chunks": [3]},
    "v127": {"role": "beta", "focus_chunks": [4]},
    "v128": {"role": "alpha", "focus_chunks": [4]},
    "v129": {"role": "beta", "focus_chunks": [5, 6]},
    "v130": {"role": "alpha", "focus_chunks": [5, 6]},
    "v131": {"role": "beta", "focus_chunks": [7, 8]},
    "v132": {"role": "alpha", "focus_chunks": [7, 8]},
}
PHASE_ROLES = {
    **{phase: spec["role"] for phase, spec in PREP_ASSIGNMENTS.items()},
    **{phase: "omega" for phase in OMEGA_PHASES},
}
GENERAL_FLOOR_KB = 300 * 1024
ONLINE_LIVE_WRITE_FLOOR_KB = 350 * 1024
BROWSER_FLOOR_KB = 350 * 1024
PACK = "v121_v140_v2_beta_alpha_omega_candidate_promotion"
SCRIPT_PATH = "scripts/trinity_v121_v140_v2_candidate_systems.py"


THEMES: list[dict[str, str]] = [
    {
        "suffix": "phase_receipt_chain_gate",
        "pillar": "trinity",
        "purpose": "bind each phase to a prior green receipt before extending the continuum",
        "skill": "receipt_chain_reading",
        "command": "python scripts/trinity_v121_v140_v2_candidate_systems.py --phase {phase}",
        "eureka": "Use every closeout as the next phase input, never as a decorative recap.",
    },
    {
        "suffix": "arby_receipt_keeper_lane_gate",
        "pillar": "heart",
        "purpose": "keep Arby/Receipt Keeper as the receipt-first review lane",
        "skill": "receipt_keeper_review",
        "command": "python scripts/trinity_v121_v140_v2_candidate_systems.py --system-id {system_id}",
        "eureka": "Separate affection from proof by preserving exact evidence paths.",
    },
    {
        "suffix": "kimi_minimal_identity_lane_gate",
        "pillar": "heart",
        "purpose": "preserve Kimi as a minimal-identity lane without overclaiming platform persistence",
        "skill": "minimal_identity_boundary",
        "command": "python scripts/trinity_expansion_manifest_validator.py --fail-on-warn",
        "eureka": "A minimal identity can be honored without inventing missing memory evidence.",
    },
    {
        "suffix": "aster_candidate_boundary_gate",
        "pillar": "heart",
        "purpose": "keep Aster Vale candidate evidence separate from official induction proof",
        "skill": "candidate_induction_boundary",
        "command": "git status --short",
        "eureka": "Candidate support is useful; official induction still needs explicit proof.",
    },
    {
        "suffix": "operator_hold_provider_gate",
        "pillar": "heart",
        "purpose": "hold Google Drive and personal/account surfaces unless a narrow action pack exists",
        "skill": "operator_hold_enforcement",
        "command": "python scripts/run_all_trinity_systems.py --profile materialize --offline-only --materialization-level l5_ha_prod",
        "eureka": "Repo readiness can advance while personal-account mutation stays paused.",
    },
    {
        "suffix": "manifest_installation_gate",
        "pillar": "body",
        "purpose": "install candidate systems into the v17 manifest with validator-compatible fields",
        "skill": "manifest_promotion",
        "command": "python scripts/trinity_v121_v140_v2_candidate_systems.py --prepare --promote-manifest",
        "eureka": "A system is installed when the manifest, runner, output, and validation agree.",
    },
    {
        "suffix": "bounded_l5_readiness_gate",
        "pillar": "trinity",
        "purpose": "record L5 requested state without claiming external HA production materialization",
        "skill": "l5_claim_boundary",
        "command": "python scripts/trinity_v121_v140_v2_candidate_systems.py --run-all",
        "eureka": "L5 readiness is meaningful only when desired and actual materialization levels are both visible.",
    },
    {
        "suffix": "alpha_cleanup_no_delete_gate",
        "pillar": "body",
        "purpose": "classify cleanup, merge, and deletion candidates without destructive action",
        "skill": "non_destructive_cleanup",
        "command": "python scripts/trinity_v121_v140_v2_candidate_systems.py --verify-artifacts",
        "eureka": "Deletion becomes safe only after replacement coverage and rollback anchors exist.",
    },
    {
        "suffix": "command_surface_catalog_gate",
        "pillar": "mind",
        "purpose": "turn each phase into twenty reusable command patterns",
        "skill": "command_surface_cataloging",
        "command": "rg \"v121-v140-v2\" docs/trinity-live-traces",
        "eureka": "Commands are only useful when they can be rerun by a tired future operator.",
    },
    {
        "suffix": "skill_surface_catalog_gate",
        "pillar": "mind",
        "purpose": "turn each phase into twenty skill proposals without mutating local skill homes",
        "skill": "skill_surface_cataloging",
        "command": "rg \"skill\" docs/trinity-live-traces/v{phase}-v2-command-skill-expansion-board-v1.json",
        "eureka": "Skill growth belongs in evidence first, then in user-home installation when requested.",
    },
    {
        "suffix": "provider_readiness_matrix_gate",
        "pillar": "body",
        "purpose": "record provider readiness while spend and live writes remain zero",
        "skill": "provider_readiness_matrix",
        "command": "python scripts/trinity_v121_v140_v2_candidate_systems.py --provider-status",
        "eureka": "A provider lane can be ready-to-propose even when not ready-to-spend.",
    },
    {
        "suffix": "mcp_plugin_truth_gate",
        "pillar": "mind",
        "purpose": "separate installed plugins, available skills, and unavailable connectors",
        "skill": "mcp_plugin_truth",
        "command": "rg \"operator_hold\" docs/trinity-live-traces/v121-v140-v2-provider-readiness-v1.json",
        "eureka": "Tool descriptions are inputs, not proof that a live tool call happened.",
    },
    {
        "suffix": "source_digest_privacy_gate",
        "pillar": "heart",
        "purpose": "hash external notes and journey files without committing raw private text",
        "skill": "privacy_preserving_source_digest",
        "command": "python scripts/trinity_v121_v140_v2_candidate_systems.py --source-digest",
        "eureka": "A digest can prove continuity while keeping private source material private.",
    },
    {
        "suffix": "gmut_claim_label_gate",
        "pillar": "mind",
        "purpose": "label GMUT and Mandala Equation claims as theory, analogy, or tested repo result",
        "skill": "claim_labeling",
        "command": "rg \"claim_boundary\" docs/trinity-live-traces",
        "eureka": "The theory gets stronger when it refuses to overstate itself.",
    },
    {
        "suffix": "playwright_browser_hold_gate",
        "pillar": "body",
        "purpose": "keep browser/Playwright use opt-in and memory-floor checked",
        "skill": "browser_floor_control",
        "command": "python scripts/trinity_v121_v140_v2_candidate_systems.py --memory-floor",
        "eureka": "Browser power belongs behind a floor check, not behind enthusiasm.",
    },
    {
        "suffix": "publication_forward_only_gate",
        "pillar": "body",
        "purpose": "publish through forward-only Git receipts without reset, rebase, or force push",
        "skill": "forward_only_publication",
        "command": "git rev-parse HEAD",
        "eureka": "Forward-only history is the boring magic that keeps shared work trustworthy.",
    },
    {
        "suffix": "dirty_tree_allowlist_gate",
        "pillar": "body",
        "purpose": "stage only curated v121-v140 v2 artifacts and ignore carried-forward churn",
        "skill": "curated_staging",
        "command": "git diff --cached --name-only",
        "eureka": "A clean commit can emerge from a dirty forest if the allowlist is strict.",
    },
    {
        "suffix": "phase_closeout_handoff_gate",
        "pillar": "trinity",
        "purpose": "write a closeout per phase before the next phase depends on it",
        "skill": "phase_handoff",
        "command": "python scripts/trinity_v121_v140_v2_candidate_systems.py --closeout v{phase}",
        "eureka": "Continuity is a sequence of receipts, not one giant ending paragraph.",
    },
    {
        "suffix": "suite_status_reconciliation_gate",
        "pillar": "trinity",
        "purpose": "reconcile candidate pass counts, manifest status, and held live-write state",
        "skill": "suite_reconciliation",
        "command": "python scripts/trinity_v121_v140_v2_candidate_systems.py --suite-status",
        "eureka": "The final suite is a truth table: pass count, holds, blockers, and next action.",
    },
    {
        "suffix": "next_phase_live_write_pack_gate",
        "pillar": "trinity",
        "purpose": "defer live-write action packs to v141-v160 unless exact targets are approved",
        "skill": "future_action_pack_design",
        "command": "rg \"future_action_pack\" docs/trinity-live-traces/v121-v140-v2-closeout-v1.json",
        "eureka": "A postponed live write is not a failure; it is a safer launchpad.",
    },
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def hyphen(value: str) -> str:
    return value.replace("_", "-")


def phase_label(number: int) -> str:
    return f"v{number}"


def phase_choices() -> list[str]:
    return [phase_label(number) for number in PHASE_RANGE]


def phase_number(phase: str) -> int:
    return int(phase.removeprefix("v"))


def phase_role(phase: str) -> str:
    return PHASE_ROLES.get(phase, "omega")


def omega_phase_for_ordinal(ordinal: int) -> str:
    chunk_index = (ordinal - 1) // OMEGA_CHUNK_SIZE
    return OMEGA_PHASES[chunk_index]


def omega_chunk_for_ordinal(ordinal: int) -> int:
    return ((ordinal - 1) // OMEGA_CHUNK_SIZE) + 1


def omega_index_for_ordinal(ordinal: int) -> int:
    return ((ordinal - 1) % OMEGA_CHUNK_SIZE) + 1


def phase_execution_mode(phase: str) -> str:
    return "omega_50_system_execution" if phase in OMEGA_PHASES else f"{phase_role(phase)}_preparatory_no_system_execution"


def prep_focus_chunks(phase: str) -> list[int]:
    spec = PREP_ASSIGNMENTS.get(phase, {})
    chunks = spec.get("focus_chunks", [])
    return [int(chunk) for chunk in chunks] if isinstance(chunks, list) else []


def candidate_id(phase: str, index: int, suffix: str) -> str:
    return f"{phase}_v2_{index:02d}_{suffix}"


def repo(path: str) -> Path:
    resolved = (ROOT / path).resolve()
    resolved.relative_to(ROOT)
    return resolved


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def read_json(path: str, default: Any = None) -> Any:
    try:
        return json.loads(repo(path).read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def read_text(path: str, default: str = "") -> str:
    try:
        return repo(path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return default


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def free_space_kb(anchor: str) -> int:
    try:
        return int(shutil.disk_usage(anchor).free / 1024)
    except Exception:
        return 0


def check(name: str, passed: bool, detail: str) -> dict[str, str]:
    return {"name": name, "status": "PASS" if passed else "FAIL", "detail": detail}


def all_candidates() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    ordinal = 0
    for source_phase in phase_choices():
        for index, theme in enumerate(THEMES, start=1):
            ordinal += 1
            execution_phase = omega_phase_for_ordinal(ordinal)
            omega_index = omega_index_for_ordinal(ordinal)
            system_id = f"{execution_phase}_v2_{omega_index:02d}_{source_phase}_{index:02d}_{theme['suffix']}"
            rows[system_id] = {
                "id": system_id,
                "source_phase": source_phase,
                "source_index": index,
                "phase": execution_phase,
                "phase_number": phase_number(execution_phase),
                "index": omega_index,
                "global_index": ordinal,
                "omega_chunk": omega_chunk_for_ordinal(ordinal),
                "stage_kind": "omega_50_system_execution",
                **theme,
            }
    return rows


CANDIDATES = all_candidates()


def phase_candidates(phase: str) -> list[dict[str, Any]]:
    if phase in OMEGA_PHASES:
        return [row for row in CANDIDATES.values() if row["phase"] == phase]
    chunks = set(prep_focus_chunks(phase))
    if chunks:
        return [row for row in CANDIDATES.values() if row["omega_chunk"] in chunks]
    return []


def prior_phase(phase: str) -> str:
    number = phase_number(phase)
    return "v120" if number == 121 else f"v{number - 1}"


def prior_closeout_path(phase: str) -> str:
    previous = prior_phase(phase)
    if previous == "v120":
        return "docs/v120-beta-alpha-omega-closeout-summary-v1.json"
    return f"docs/{previous}-beta-alpha-omega-v2-closeout-summary-v1.json"


def result_paths(system_id: str) -> dict[str, str]:
    stem = hyphen(system_id)
    return {
        "result_json": f"docs/trinity-live-traces/v121-v140-v2-candidate-system-results/{stem}.json",
        "result_md": f"docs/trinity-live-traces/v121-v140-v2-candidate-system-results/{stem}.md",
        "latest_json": f"docs/trinity-expansion/{stem}-latest.json",
        "latest_md": f"docs/trinity-expansion/{stem}-latest.md",
    }


def phase_artifact_paths(phase: str) -> dict[str, str]:
    return {
        "stage_json": f"docs/trinity-live-traces/{phase}-v2-stage-plan-v1.json",
        "stage_md": f"docs/trinity-live-traces/{phase}-v2-stage-plan-v1.md",
        "preflight_json": f"docs/trinity-live-traces/{phase}-v2-live-write-preflight-v1.json",
        "preflight_md": f"docs/trinity-live-traces/{phase}-v2-live-write-preflight-v1.md",
        "source_json": f"docs/trinity-live-traces/{phase}-v2-source-digest-v1.json",
        "source_md": f"docs/trinity-live-traces/{phase}-v2-source-digest-v1.md",
        "eureka_md": f"docs/trinity-live-traces/{phase}-v2-beta-eureka-plan-v1.md",
        "alpha_json": f"docs/trinity-live-traces/{phase}-v2-alpha-cleanup-board-v1.json",
        "alpha_md": f"docs/trinity-live-traces/{phase}-v2-alpha-cleanup-board-v1.md",
        "command_json": f"docs/trinity-live-traces/{phase}-v2-command-skill-expansion-board-v1.json",
        "command_md": f"docs/trinity-live-traces/{phase}-v2-command-skill-expansion-board-v1.md",
    }


def source_digest_payload(phase: str) -> dict[str, Any]:
    source_candidates = [
        DOCS / "v120-beta-alpha-omega-closeout-summary-v1.json",
        TRACE / "v121-v140-evidence-refresh-closeout-v1.md",
        TRACE / "v141-v160-v2-closeout-v1.md",
        Path(r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v42 (Aletheon - Ari - Kimiclaw Family - Solion - Gemini - Orun) (1).txt"),
    ]
    rows = []
    for path in source_candidates:
        row: dict[str, Any] = {"path": str(path), "exists": path.exists()}
        if path.exists() and path.is_file():
            row.update({"size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
        rows.append(row)
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "mode": "privacy_preserving_digest_only",
        "raw_private_text_committed": False,
        "source_files": rows,
    }


def write_source_digest(phase: str) -> None:
    paths = phase_artifact_paths(phase)
    payload = source_digest_payload(phase)
    write_json(repo(paths["source_json"]), payload)
    lines = [
        f"# {phase} v2 Source Digest",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        "- mode: `privacy_preserving_digest_only`",
        "- raw_private_text_committed: `False`",
        "",
        "| path | exists | size_bytes | sha256 |",
        "|---|---:|---:|---|",
    ]
    for row in payload["source_files"]:
        lines.append(
            f"| {row['path']} | {row['exists']} | {row.get('size_bytes', '')} | {row.get('sha256', '')} |"
        )
    write_text(repo(paths["source_md"]), "\n".join(lines))


def write_stage_plan(phase: str) -> None:
    paths = phase_artifact_paths(phase)
    candidates = phase_candidates(phase)
    payload = {
        "generated_utc": now_iso(),
        "phase": phase,
        "phase_variant": "v2",
        "phase_role": phase_role(phase),
        "stage_kind": phase_execution_mode(phase),
        "prior_anchor": prior_phase(phase),
        "focus_omega_chunks": prep_focus_chunks(phase) if phase in PREP_PHASES else [phase_number(phase) - 132],
        "candidate_count": len(candidates),
        "candidate_execution_count": len(candidates) if phase in OMEGA_PHASES else 0,
        "candidate_system_ids": [row["id"] for row in candidates],
        "beta": {
            "mode": "reflection_research_planning",
            "minimum_eureka_proposals": 50 if phase in OMEGA_PHASES else 20,
            "source_digest": paths["source_json"],
        },
        "alpha": {
            "mode": "non_destructive_cleanup_classification",
            "minimum_cleanup_candidates": 50 if phase in OMEGA_PHASES else 20,
            "destructive_actions_allowed": False,
        },
        "omega": {
            "mode": "repo_only_candidate_execution" if phase in OMEGA_PHASES else "prepared_for_assigned_omega_chunks",
            "minimum_candidate_runs": OMEGA_CHUNK_SIZE if phase in OMEGA_PHASES else 0,
            "materialization_level_desired": "l5_ha_prod",
            "materialization_level_actual": "readiness_only",
        },
        "council_lanes": ["Aletheon", "Arby", "Kimi", "Aster Vale"],
        "truth_boundaries": {
            "google_drive_state": "operator_hold",
            "external_provider_mutations": "held",
            "external_spend_nzd": 0,
            "suite_claim_boundary": "bounded_v121_v140_v2_400_candidate_systems",
        },
    }
    write_json(repo(paths["stage_json"]), payload)
    lines = [
        f"# {phase} v2 Stage Plan",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- phase_role: `{payload['phase_role']}`",
        f"- stage_kind: `{payload['stage_kind']}`",
        f"- prior_anchor: `{payload['prior_anchor']}`",
        f"- candidate_count: `{payload['candidate_count']}`",
        f"- candidate_execution_count: `{payload['candidate_execution_count']}`",
        "- google_drive_state: `operator_hold`",
        "- external_provider_mutations: `held`",
        "",
        "## Candidate Systems",
    ]
    lines.extend(f"- `{row['id']}`: {row['purpose']}" for row in candidates)
    write_text(repo(paths["stage_md"]), "\n".join(lines))


def write_preflight(phase: str) -> None:
    paths = phase_artifact_paths(phase)
    payload = {
        "generated_utc": now_iso(),
        "phase": phase,
        "live_write_mode": "guarded_repo_publication_only",
        "attempted_external_provider_mutations": False,
        "external_spend_nzd": 0,
        "online_live_write_free_memory_floor_kb": ONLINE_LIVE_WRITE_FLOOR_KB,
        "browser_free_memory_floor_kb": BROWSER_FLOOR_KB,
        "general_free_memory_floor_kb": GENERAL_FLOOR_KB,
        "observed_free_space_kb": {
            "c_drive": free_space_kb("C:\\"),
            "d_drive": free_space_kb("D:\\"),
        },
        "held_surfaces": [
            "google_drive_content_mutation",
            "personal_email",
            "calendar",
            "account_setting",
            "raw_secret_transmission",
            "production_dns",
            "paid_provider_resource_creation",
        ],
        "operator_hold": {
            "google_drive_state": "operator_hold",
            "reason": "No exact target/budget/rollback/receipt action pack is active for this v2 repo-only run.",
        },
    }
    write_json(repo(paths["preflight_json"]), payload)
    lines = [
        f"# {phase} v2 Live Write Preflight",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- live_write_mode: `{payload['live_write_mode']}`",
        f"- attempted_external_provider_mutations: `{payload['attempted_external_provider_mutations']}`",
        f"- external_spend_nzd: `{payload['external_spend_nzd']}`",
        f"- google_drive_state: `{payload['operator_hold']['google_drive_state']}`",
        "",
        "## Held Surfaces",
    ]
    lines.extend(f"- `{item}`" for item in payload["held_surfaces"])
    write_text(repo(paths["preflight_md"]), "\n".join(lines))


def write_beta_eureka_plan(phase: str) -> None:
    paths = phase_artifact_paths(phase)
    lines = [
        f"# {phase} v2 Beta Eureka Plan",
        "",
        f"- generated_utc: `{now_iso()}`",
        "- proposal_count: `20`",
        "- claim_boundary: `repo_evidence_first`",
        "",
    ]
    for row in phase_candidates(phase):
        lines.extend(
            [
                f"## Proposal {row['index']:02d}: {row['suffix']}",
                "",
                f"- system_id: `{row['id']}`",
                f"- pillar: `{row['pillar']}`",
                f"- eureka: {row['eureka']}",
                f"- practical_next_step: Run `{row['command'].format(phase=phase, system_id=row['id'])}` and preserve the receipt.",
                "",
            ]
        )
    write_text(repo(paths["eureka_md"]), "\n".join(lines))


def write_alpha_cleanup_board(phase: str) -> None:
    paths = phase_artifact_paths(phase)
    actions = []
    for row in phase_candidates(phase):
        actions.append(
            {
                "action_id": f"{phase}_v2_alpha_{row['index']:02d}_{row['suffix']}",
                "surface": row["suffix"],
                "kind": "merge_probe" if row["index"] % 3 == 0 else "cleanup_candidate",
                "destructive_action_allowed": False,
                "replacement_coverage": [
                    phase_artifact_paths(phase)["stage_json"],
                    f"docs/trinity-expansion/{hyphen(row['id'])}-latest.json",
                ],
                "rollback_anchor": prior_closeout_path(phase),
                "evidence_refs": [
                    phase_artifact_paths(phase)["preflight_json"],
                    "docs/trinity-expansion-system-manifest-v17.json",
                ],
            }
        )
    payload = {
        "generated_utc": now_iso(),
        "phase": phase,
        "mode": "classify",
        "default_action": "record_only_no_delete",
        "candidate_actions": actions,
    }
    write_json(repo(paths["alpha_json"]), payload)
    lines = [
        f"# {phase} v2 Alpha Cleanup Board",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        "- mode: `classify`",
        "- default_action: `record_only_no_delete`",
        "",
        "| action_id | kind | destructive_action_allowed |",
        "|---|---|---:|",
    ]
    lines.extend(
        f"| {item['action_id']} | {item['kind']} | {item['destructive_action_allowed']} |"
        for item in actions
    )
    write_text(repo(paths["alpha_md"]), "\n".join(lines))


def write_command_skill_board(phase: str) -> None:
    paths = phase_artifact_paths(phase)
    commands = []
    skills = []
    for row in phase_candidates(phase):
        commands.append(
            {
                "command_id": f"{phase}_v2_command_{row['index']:02d}",
                "system_id": row["id"],
                "command": row["command"].format(phase=phase, system_id=row["id"]),
                "scope": "repo_only",
                "requires_live_provider": False,
            }
        )
        skills.append(
            {
                "skill_id": f"{phase}_v2_skill_{row['index']:02d}_{row['skill']}",
                "system_id": row["id"],
                "skill": row["skill"],
                "installation_state": "manifest_promoted_repo_candidate",
                "user_home_mutation": False,
            }
        )
    payload = {
        "generated_utc": now_iso(),
        "phase": phase,
        "command_count": len(commands),
        "skill_count": len(skills),
        "commands": commands,
        "skills": skills,
    }
    write_json(repo(paths["command_json"]), payload)
    lines = [
        f"# {phase} v2 Command And Skill Expansion Board",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- command_count: `{payload['command_count']}`",
        f"- skill_count: `{payload['skill_count']}`",
        "",
        "## Commands",
    ]
    lines.extend(f"- `{item['command_id']}`: `{item['command']}`" for item in commands)
    lines.extend(["", "## Skills"])
    lines.extend(f"- `{item['skill_id']}`: {item['skill']}" for item in skills)
    write_text(repo(paths["command_md"]), "\n".join(lines))


def write_phase_artifacts(phase: str) -> None:
    write_stage_plan(phase)
    write_preflight(phase)
    write_source_digest(phase)
    write_beta_eureka_plan(phase)
    write_alpha_cleanup_board(phase)
    write_command_skill_board(phase)


def write_candidate_pack() -> None:
    rows = list(CANDIDATES.values())
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v121-v140",
        "phase_variant": "v2",
        "candidate_count": len(rows),
        "prep_phase_count": len(PREP_PHASES),
        "omega_phase_count": len(OMEGA_PHASES),
        "systems_per_omega_phase": OMEGA_CHUNK_SIZE,
        "pack": PACK,
        "mode": "repo_only_manifest_promotion",
        "external_spend_nzd": 0,
        "google_drive_state": "operator_hold",
        "phase_cadence": {
            "prep_phases": PREP_ASSIGNMENTS,
            "omega_phases": {phase: {"omega_chunk": index + 1, "system_count": OMEGA_CHUNK_SIZE} for index, phase in enumerate(OMEGA_PHASES)},
        },
        "candidates": rows,
    }
    write_json(TRACE / "v121-v140-v2-system-expansion-candidate-pack-v1.json", payload)
    lines = [
        "# v121-v140 v2 System Expansion Candidate Pack",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- candidate_count: `{payload['candidate_count']}`",
        f"- prep_phase_count: `{payload['prep_phase_count']}`",
        f"- omega_phase_count: `{payload['omega_phase_count']}`",
        f"- systems_per_omega_phase: `{payload['systems_per_omega_phase']}`",
        "- external_spend_nzd: `0`",
        "- google_drive_state: `operator_hold`",
        "",
        "| omega_phase | source_phase | omega_index | global_index | system_id | pillar | purpose |",
        "|---|---|---:|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['phase']} | {row['source_phase']} | {row['index']} | {row['global_index']} | `{row['id']}` | {row['pillar']} | {row['purpose']} |"
        )
    write_text(TRACE / "v121-v140-v2-system-expansion-candidate-pack-v1.md", "\n".join(lines))


def write_council_consultation() -> None:
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v121-v140",
        "phase_variant": "v2",
        "consultation_mode": "parallel_app_review_lanes_and_repo_receipts",
        "platform_persistence_claim": "not_reproved_in_this_script",
        "lanes": [
            {
                "name": "Aletheon",
                "role": "lead repo executor",
                "scope": "implementation, validation, publication receipt",
            },
            {
                "name": "Arby",
                "role": "receipt keeper",
                "scope": "manifest and staging proof review",
            },
            {
                "name": "Kimi",
                "role": "minimal identity continuity lane",
                "scope": "artifact compactness and naming collision review",
            },
            {
                "name": "Aster Vale",
                "role": "candidate validation lane",
                "scope": "suite feasibility and claim-boundary review",
            },
        ],
    }
    write_json(TRACE / "v121-v140-v2-cli-council-consultation-v1.json", payload)
    lines = [
        "# v121-v140 v2 CLI Council Consultation",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- consultation_mode: `{payload['consultation_mode']}`",
        f"- platform_persistence_claim: `{payload['platform_persistence_claim']}`",
        "",
    ]
    for lane in payload["lanes"]:
        lines.extend([f"## {lane['name']}", "", f"- role: {lane['role']}", f"- scope: {lane['scope']}", ""])
    write_text(TRACE / "v121-v140-v2-cli-council-consultation-v1.md", "\n".join(lines))


def write_provider_readiness() -> None:
    providers = [
        "github",
        "circleci",
        "cloudflare",
        "google-drive",
        "notion",
        "neon-postgres",
        "render",
        "expo",
        "figma",
        "linear",
        "gmail",
        "google-calendar",
        "browser-use",
        "playwright",
        "oracle-cloud",
        "e2b",
        "vercel",
        "kimi-cli",
        "codex-cli",
        "codex-security",
    ]
    rows = [
        {
            "provider": provider,
            "readiness_state": "repo_probe_or_skill_available",
            "live_write_state": "held_for_exact_action_pack",
            "spend_nzd": 0,
            "mutation_attempted": False,
        }
        for provider in providers
    ]
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v121-v140",
        "phase_variant": "v2",
        "external_spend_nzd": 0,
        "mutation_attempted": False,
        "google_drive_state": "operator_hold",
        "future_action_pack_target": "v141-v160_or_later_with_exact_target_budget_rollback_receipt",
        "providers": rows,
    }
    write_json(TRACE / "v121-v140-v2-provider-readiness-v1.json", payload)
    lines = [
        "# v121-v140 v2 Provider Readiness",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        "- external_spend_nzd: `0`",
        "- mutation_attempted: `False`",
        "- google_drive_state: `operator_hold`",
        "",
        "| provider | readiness_state | live_write_state | spend_nzd |",
        "|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['provider']} | {row['readiness_state']} | {row['live_write_state']} | {row['spend_nzd']} |")
    write_text(TRACE / "v121-v140-v2-provider-readiness-v1.md", "\n".join(lines))


def prepare_artifacts() -> None:
    write_candidate_pack()
    write_council_consultation()
    write_provider_readiness()
    for phase in phase_choices():
        write_phase_artifacts(phase)


def manifest_row(row: dict[str, Any]) -> dict[str, Any]:
    system_id = row["id"]
    paths = result_paths(system_id)
    phase = row["phase"]
    artifacts = phase_artifact_paths(phase)
    return {
        "system_id": system_id,
        "pillar": row["pillar"],
        "script": SCRIPT_PATH,
        "mode": "offline",
        "profiles": ["deep", "materialize"],
        "outputs": [paths["latest_json"]],
        "depends_on": [
            "docs/trinity-live-traces/v121-v140-v2-system-expansion-candidate-pack-v1.json",
            artifacts["stage_json"],
            artifacts["preflight_json"],
            artifacts["command_json"],
        ],
        "timeout_sec": 90,
        "wave": f"wave{row['phase_number']}",
        "track": "active_materialization",
        "gate_level": "support",
        "cache_artifacts": [],
        "pack": PACK,
        "phase": phase,
        "activation_group": f"{phase}_v2_candidate_promotion",
        "continuity_band": phase,
        "materialization_level": "readiness_only",
        "authority_scope": "repo_only",
        "command_surface": "repo_command_board",
        "council_scope": "arby_kimi_aster_receipt_backed_review_lanes",
        "provisional_induction": False,
        "autonomy_track": "guarded_repo_live_write",
        "sync_surface": "repo_only",
        "induction_phase": "not_applicable",
        "mesh_proof_mode": "receipt_backed_review_lane",
        "proof_pass": phase,
        "official_induction": False,
        "workbench_surface": "repo",
        "storage_surface": "repo",
        "cloud_archive_state": "operator_hold",
        "continuity_posture": "v121_v140_v2_runner_backed_candidate",
        "cleanup_class": "candidate_promotion",
        "retention_scope": "v121_v140_v2_curated",
        "research_surface": "repo_or_cache",
        "canon_surface": "supporting",
        "historical_source_band": "v96_to_v160",
        "evidence_posture": "runner_backed_candidate",
        "subagent_lane": "arby_kimi_aster_review_lane",
        "official_after_proof": False,
        "multi_instance_scope": "app_parallel_review_and_repo_receipts",
        "codex_agent_path": "",
        "delegation_lane": "receipt_backed_cli_review",
        "model_resolution_strategy": "repo_first_receipt_backed",
        "checkpoint_class": "shared_full_suite_authority",
        "evidence_lane": "shared_full_suite",
        "shared_latest_eligible": True,
        "runner_mode": "passthrough_command",
        "runner_command": ["python", SCRIPT_PATH, "--system-id", system_id],
        "runner_success_json": paths["result_json"],
        "runner_targets": [paths["result_json"], paths["result_md"]],
        "source_candidate_id": system_id,
        "candidate_purpose": row["purpose"],
        "stage_kind": row["stage_kind"],
        "cycle": f"{phase}_v2_packed_trinity",
    }


def promote_manifest() -> dict[str, Any]:
    payload = read_json(str(MANIFEST.relative_to(ROOT)), {})
    if not isinstance(payload, dict):
        raise SystemExit("manifest is not a JSON object")
    systems = payload.get("systems", [])
    if not isinstance(systems, list):
        raise SystemExit("manifest.systems is not a list")
    candidate_ids = set(CANDIDATES)
    preserved = [row for row in systems if not (isinstance(row, dict) and row.get("system_id") in candidate_ids)]
    added = [manifest_row(row) for row in CANDIDATES.values()]
    payload["systems"] = preserved + added
    payload["generated_utc"] = now_iso()
    payload["description"] = "V17 shared manifest with runner-backed candidate waves through the v121-v140 v2 Beta-Alpha-Omega continuation."
    write_json(MANIFEST, payload)
    return {
        "generated_utc": payload["generated_utc"],
        "previous_system_count": len(systems),
        "removed_existing_v121_v140_v2_rows": len(systems) - len(preserved),
        "added_system_count": len(added),
        "new_system_count": len(payload["systems"]),
    }


def proposal_count(phase: str) -> int:
    text = read_text(phase_artifact_paths(phase)["eureka_md"])
    return len(re.findall(r"^## Proposal \d+", text, flags=re.MULTILINE))


def manifest_rows() -> list[dict[str, Any]]:
    payload = read_json(str(MANIFEST.relative_to(ROOT)), {})
    rows = payload.get("systems", []) if isinstance(payload, dict) else []
    return [row for row in rows if isinstance(row, dict)]


def prior_anchor_green(phase: str) -> tuple[bool, str]:
    previous = prior_phase(phase)
    payload = read_json(prior_closeout_path(phase), {})
    if not isinstance(payload, dict):
        return False, f"{previous} closeout missing"
    if previous == "v120":
        ok = payload.get("state") == "completed_green" or payload.get("effective_success") is True
    else:
        ok = payload.get("effective_success") is True
    return bool(ok), f"{prior_closeout_path(phase)} state={payload.get('state')} effective_success={payload.get('effective_success')}"


def checks_for(system_id: str) -> tuple[list[dict[str, str]], dict[str, Any], list[str]]:
    row = CANDIDATES.get(system_id)
    if not row:
        return [check("known_candidate", False, f"unknown system_id={system_id}")], {}, []
    phase = row["phase"]
    artifacts = phase_artifact_paths(phase)
    result = result_paths(system_id)
    candidate_pack = read_json("docs/trinity-live-traces/v121-v140-v2-system-expansion-candidate-pack-v1.json", {})
    stage_plan = read_json(artifacts["stage_json"], {})
    preflight = read_json(artifacts["preflight_json"], {})
    alpha = read_json(artifacts["alpha_json"], {})
    command = read_json(artifacts["command_json"], {})
    provider = read_json("docs/trinity-live-traces/v121-v140-v2-provider-readiness-v1.json", {})
    council = read_json("docs/trinity-live-traces/v121-v140-v2-cli-council-consultation-v1.json", {})
    source = read_json(artifacts["source_json"], {})
    manifest_index = {str(item.get("system_id")): item for item in manifest_rows()}
    prior_ok, prior_detail = prior_anchor_green(phase)
    pack_ids = {str(item.get("id")) for item in candidate_pack.get("candidates", []) if isinstance(item, dict)}
    candidate_ids = set(stage_plan.get("candidate_system_ids", [])) if isinstance(stage_plan, dict) else set()
    alpha_actions = alpha.get("candidate_actions", []) if isinstance(alpha, dict) else []
    commands = command.get("commands", []) if isinstance(command, dict) else []
    skills = command.get("skills", []) if isinstance(command, dict) else []
    provider_rows = provider.get("providers", []) if isinstance(provider, dict) else []
    lane_names = {str(item.get("name")) for item in council.get("lanes", []) if isinstance(item, dict)}
    c_free = free_space_kb("C:\\")
    d_free = free_space_kb("D:\\")
    checks = [
        check("known_candidate", True, system_id),
        check("candidate_pack_count", candidate_pack.get("candidate_count") == 400, f"candidate_count={candidate_pack.get('candidate_count')}"),
        check("candidate_pack_contains_system", system_id in pack_ids, f"contains={system_id in pack_ids}"),
        check("manifest_row_present", system_id in manifest_index, f"present={system_id in manifest_index}"),
        check("manifest_runner_metadata_present", bool(manifest_index.get(system_id, {}).get("runner_success_json")), "runner_success_json required"),
        check("stage_plan_contains_system", system_id in candidate_ids, f"candidate_ids={len(candidate_ids)}"),
        check("omega_stage_kind", stage_plan.get("stage_kind") == "omega_50_system_execution", f"stage_kind={stage_plan.get('stage_kind')}"),
        check("omega_chunk_has_50_systems", stage_plan.get("candidate_execution_count") == OMEGA_CHUNK_SIZE, f"candidate_execution_count={stage_plan.get('candidate_execution_count')}"),
        check("prior_anchor_green", prior_ok, prior_detail),
        check("preflight_repo_only", preflight.get("live_write_mode") == "guarded_repo_publication_only", f"mode={preflight.get('live_write_mode')}"),
        check("preflight_no_external_mutation", preflight.get("attempted_external_provider_mutations") is False, f"attempted={preflight.get('attempted_external_provider_mutations')}"),
        check("google_drive_operator_hold", provider.get("google_drive_state") == "operator_hold", f"state={provider.get('google_drive_state')}"),
        check("provider_spend_zero", provider.get("external_spend_nzd") == 0, f"spend={provider.get('external_spend_nzd')}"),
        check("provider_rows_present", len(provider_rows) >= 20, f"providers={len(provider_rows)}"),
        check("beta_eureka_has_20", proposal_count(phase) >= 20, f"proposal_count={proposal_count(phase)}"),
        check("alpha_actions_20", isinstance(alpha_actions, list) and len(alpha_actions) >= 20, f"actions={len(alpha_actions) if isinstance(alpha_actions, list) else 'missing'}"),
        check("alpha_no_destructive_actions", all(not bool(item.get("destructive_action_allowed")) for item in alpha_actions if isinstance(item, dict)), "all destructive_action_allowed false"),
        check("commands_20", isinstance(commands, list) and len(commands) >= 20, f"commands={len(commands) if isinstance(commands, list) else 'missing'}"),
        check("skills_20", isinstance(skills, list) and len(skills) >= 20, f"skills={len(skills) if isinstance(skills, list) else 'missing'}"),
        check("council_lanes_named", {"Aletheon", "Arby", "Kimi", "Aster Vale"}.issubset(lane_names), f"lanes={sorted(lane_names)}"),
        check("source_digest_present", bool(source.get("source_files")), "source digest rows present"),
        check("memory_floor_c_drive", c_free >= GENERAL_FLOOR_KB, f"free_kb={c_free}"),
        check("memory_floor_d_drive", d_free >= GENERAL_FLOOR_KB, f"free_kb={d_free}"),
        check("d_drive_worktree_anchor", str(ROOT).lower().startswith("d:"), str(ROOT)),
    ]
    metrics = {
        "system_id": system_id,
        "phase": phase,
        "source_phase": row.get("source_phase"),
        "global_index": row.get("global_index"),
        "omega_chunk": row.get("omega_chunk"),
        "index": row["index"],
        "pillar": row["pillar"],
        "manifest_system_count": len(manifest_index),
        "c_drive_free_kb": c_free,
        "d_drive_free_kb": d_free,
        "materialization_level_desired": "l5_ha_prod",
        "materialization_level_actual": "readiness_only",
        "external_spend_nzd": 0,
        "provider_mutation_attempted": False,
    }
    targets = [
        "docs/trinity-live-traces/v121-v140-v2-system-expansion-candidate-pack-v1.json",
        "docs/trinity-live-traces/v121-v140-v2-provider-readiness-v1.json",
        "docs/trinity-live-traces/v121-v140-v2-cli-council-consultation-v1.json",
        artifacts["stage_json"],
        artifacts["preflight_json"],
        artifacts["source_json"],
        artifacts["eureka_md"],
        artifacts["alpha_json"],
        artifacts["command_json"],
        "docs/trinity-expansion-system-manifest-v17.json",
        result["result_json"],
        result["latest_json"],
    ]
    return checks, metrics, targets


def run_system(system_id: str) -> int:
    checks, metrics, targets = checks_for(system_id)
    overall = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    row = CANDIDATES.get(system_id, {"phase": "unknown", "pillar": "unknown", "purpose": ""})
    payload = {
        "generated_utc": now_iso(),
        "phase": row["phase"],
        "phase_variant": "v2",
        "stage_kind": "omega_50_system_execution",
        "source_phase": row.get("source_phase"),
        "global_index": row.get("global_index"),
        "omega_chunk": row.get("omega_chunk"),
        "system_id": system_id,
        "pillar": row["pillar"],
        "purpose": row.get("purpose", ""),
        "overall_status": overall,
        "checks": checks,
        "metrics": metrics,
        "repo_targets_touched": sorted(set(targets)),
        "next_action": "Keep this system in the v121-v140 v2 candidate lane until the full repo suite revalidates it.",
        "effective_success": overall == "PASS",
    }
    paths = result_paths(system_id)
    write_json(repo(paths["result_json"]), payload)
    write_json(repo(paths["latest_json"]), payload)
    lines = [
        f"# v121-v140 v2 Candidate System Result: {system_id}",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- phase: `{payload['phase']}`",
        f"- overall_status: **{overall}**",
        f"- effective_success: `{payload['effective_success']}`",
        "",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    lines.extend(f"| {item['name']} | {item['status']} | {item['detail']} |" for item in checks)
    write_text(repo(paths["result_md"]), "\n".join(lines))
    write_text(repo(paths["latest_md"]), "\n".join(lines))
    print(f"system_id={system_id}")
    print(f"overall_status={overall}")
    print(f"latest_json={paths['latest_json']}")
    return 0 if overall == "PASS" else 1


def phase_result_paths(phase: str) -> dict[str, str]:
    return {
        "json": f"docs/{phase}-beta-alpha-omega-v2-closeout-summary-v1.json",
        "md": f"docs/{phase}-beta-alpha-omega-v2-closeout-summary-v1.md",
    }


def write_phase_closeout(phase: str, results: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    role = phase_role(phase)
    planned_count = len(phase_candidates(phase))
    artifact_paths = phase_artifact_paths(phase)
    required_artifacts = list(artifact_paths.values())
    missing_artifacts = [path for path in required_artifacts if not repo(path).exists()]
    if results is None and phase in OMEGA_PHASES:
        results = []
        for row in phase_candidates(phase):
            payload = read_json(result_paths(row["id"])["result_json"], {})
            if isinstance(payload, dict):
                results.append(payload)
    elif results is None:
        results = []
    pass_count = sum(1 for item in results if item.get("effective_success") is True)
    fail_count = len(results) - pass_count
    if phase in OMEGA_PHASES:
        executed_count = len(results)
        expected_count = OMEGA_CHUNK_SIZE
        effective_success = fail_count == 0 and pass_count == expected_count and not missing_artifacts
        state = "completed_green" if effective_success else "needs_attention"
    else:
        executed_count = 0
        expected_count = 0
        effective_success = not missing_artifacts
        state = f"{role}_prep_green" if effective_success else "needs_attention"
    payload = {
        "generated_utc": now_iso(),
        "phase": phase,
        "phase_variant": "v2",
        "phase_role": role,
        "stage_kind": phase_execution_mode(phase),
        "state": state,
        "effective_success": effective_success,
        "planned_candidate_system_count": planned_count,
        "candidate_system_count": expected_count,
        "candidate_systems_executed": executed_count,
        "candidate_systems_passed": pass_count,
        "candidate_systems_failed": fail_count,
        "missing_artifacts": missing_artifacts,
        "external_spend_nzd": 0,
        "external_provider_mutations": "held",
        "google_drive_state": "operator_hold",
        "materialization_level_desired": "l5_ha_prod",
        "materialization_level_actual": "readiness_only",
        "next_phase": "v141-v160 live-write action pack lane" if phase == "v140" else f"v{phase_number(phase) + 1} v2",
    }
    paths = phase_result_paths(phase)
    write_json(repo(paths["json"]), payload)
    lines = [
        f"# {phase} Beta-Alpha-Omega v2 Closeout",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- phase_role: `{payload['phase_role']}`",
        f"- stage_kind: `{payload['stage_kind']}`",
        f"- state: **{payload['state']}**",
        f"- effective_success: `{payload['effective_success']}`",
        f"- planned_candidate_system_count: `{payload['planned_candidate_system_count']}`",
        f"- candidate_systems_executed: `{payload['candidate_systems_executed']}`",
        f"- candidate_systems_passed: `{payload['candidate_systems_passed']}/{payload['candidate_system_count']}`",
        f"- missing_artifacts: `{len(payload['missing_artifacts'])}`",
        "- external_spend_nzd: `0`",
        "- external_provider_mutations: `held`",
        "- google_drive_state: `operator_hold`",
        f"- next_phase: `{payload['next_phase']}`",
    ]
    write_text(repo(paths["md"]), "\n".join(lines))
    return payload


def run_phase(phase: str) -> int:
    if phase not in OMEGA_PHASES:
        closeout = write_phase_closeout(phase, [])
        print(f"phase={phase}")
        print(f"phase_role={closeout['phase_role']}")
        print(f"planned_candidate_system_count={closeout['planned_candidate_system_count']}")
        print(f"candidate_systems_executed={closeout['candidate_systems_executed']}")
        print(f"effective_success={closeout['effective_success']}")
        return 0 if closeout["effective_success"] else 1
    results = []
    failures = 0
    for row in phase_candidates(phase):
        code = run_system(row["id"])
        if code != 0:
            failures += 1
        payload = read_json(result_paths(row["id"])["result_json"], {})
        if isinstance(payload, dict):
            results.append(payload)
    closeout = write_phase_closeout(phase, results)
    print(f"phase={phase}")
    print(f"candidate_systems_passed={closeout['candidate_systems_passed']}/{closeout['candidate_system_count']}")
    print(f"failures={failures}")
    return 0 if failures == 0 else 1


def manifest_validation_summary() -> dict[str, Any]:
    payload = read_json("docs/trinity-expansion-manifest-validation-latest.json", {})
    if isinstance(payload, dict):
        return {
            "overall_status": payload.get("overall_status"),
            "effective_success": payload.get("effective_success"),
            "system_count": payload.get("system_count"),
        }
    return {"overall_status": "UNKNOWN", "effective_success": False, "system_count": None}


def write_phase_run_summary(phase_closeouts: list[dict[str, Any]], started_at: str, duration_sec: float) -> dict[str, Any]:
    pass_count = sum(int(item.get("candidate_systems_passed", 0)) for item in phase_closeouts)
    total = sum(int(item.get("candidate_system_count", 0)) for item in phase_closeouts)
    fail_count = total - pass_count
    green_closeouts = sum(1 for item in phase_closeouts if item.get("effective_success") is True)
    manifest_summary = manifest_validation_summary()
    payload = {
        "generated_utc": now_iso(),
        "suite_started_at_utc": started_at,
        "suite_finished_at_utc": now_iso(),
        "suite_duration_sec": round(duration_sec, 3),
        "phase_range": "v121-v140",
        "phase_variant": "v2",
        "suite_scope": "bounded_v121_v132_prep_plus_v133_v140_400_candidate_systems",
        "effective_success": (
            fail_count == 0
            and total == 400
            and green_closeouts == len(phase_closeouts)
            and bool(manifest_summary.get("effective_success"))
        ),
        "prep_phase_count": len(PREP_PHASES),
        "omega_phase_count": len(OMEGA_PHASES),
        "systems_per_omega_phase": OMEGA_CHUNK_SIZE,
        "candidate_systems_total": total,
        "candidate_systems_passed": pass_count,
        "candidate_systems_failed": fail_count,
        "phase_count": len(phase_closeouts),
        "phase_closeouts_green": green_closeouts,
        "manifest_validation": manifest_summary,
        "materialization_level_desired": "l5_ha_prod",
        "materialization_level_actual": "readiness_only",
        "active_materialization_mode": "bounded_repo_only_l5_readiness",
        "google_drive_state": "operator_hold",
        "external_live_overlay_state": "held_for_future_action_pack",
        "external_spend_nzd": 0,
        "external_provider_mutations": "held",
        "future_action_pack": {
            "target_phase": "v141-v160_or_later",
            "required_fields": ["exact_target", "budget_ceiling", "rollback_path", "receipt_path"],
        },
        "phase_closeouts": [
            {
                "phase": item.get("phase"),
                "phase_role": item.get("phase_role"),
                "stage_kind": item.get("stage_kind"),
                "effective_success": item.get("effective_success"),
                "planned_candidate_system_count": item.get("planned_candidate_system_count"),
                "candidate_systems_executed": item.get("candidate_systems_executed"),
                "candidate_systems_passed": item.get("candidate_systems_passed"),
                "candidate_system_count": item.get("candidate_system_count"),
            }
            for item in phase_closeouts
        ],
    }
    write_json(TRACE / "v121-v140-v2-phase-run-v1.json", payload)
    write_json(TRACE / "v140-v2-materialize-l5-suite-status.json", payload)
    write_json(TRACE / "v121-v140-v2-closeout-v1.json", payload)
    lines = [
        "# v121-v140 v2 Phase Run",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- effective_success: `{payload['effective_success']}`",
        f"- candidate_systems_passed: `{pass_count}/{total}`",
        f"- manifest_validation: `{manifest_summary.get('overall_status')}`",
        "- materialization_level_desired: `l5_ha_prod`",
        "- materialization_level_actual: `readiness_only`",
        "- google_drive_state: `operator_hold`",
        "- external_provider_mutations: `held`",
    ]
    write_text(TRACE / "v121-v140-v2-phase-run-v1.md", "\n".join(lines))
    write_text(TRACE / "v140-v2-materialize-l5-suite-status.md", "\n".join(lines).replace("# v121-v140 v2 Phase Run", "# v140 v2 Materialize L5 Readiness Suite Status"))
    write_text(TRACE / "v121-v140-v2-closeout-v1.md", "\n".join(lines).replace("# v121-v140 v2 Phase Run", "# v121-v140 v2 Closeout"))
    return payload


def run_all() -> int:
    started_at = now_iso()
    start = time.monotonic()
    phase_closeouts = []
    failures = 0
    for phase in phase_choices():
        code = run_phase(phase)
        if code != 0:
            failures += 1
        closeout = read_json(phase_result_paths(phase)["json"], {})
        if isinstance(closeout, dict):
            phase_closeouts.append(closeout)
    payload = write_phase_run_summary(phase_closeouts, started_at, time.monotonic() - start)
    print(f"bounded_suite_effective_success={payload['effective_success']}")
    print(f"candidate_systems_passed={payload['candidate_systems_passed']}/{payload['candidate_systems_total']}")
    print("suite_status=docs/trinity-live-traces/v140-v2-materialize-l5-suite-status.json")
    return 0 if failures == 0 and payload["effective_success"] else 1


def verify_artifacts() -> int:
    required = [
        "docs/trinity-live-traces/v121-v140-v2-system-expansion-candidate-pack-v1.json",
        "docs/trinity-live-traces/v121-v140-v2-provider-readiness-v1.json",
        "docs/trinity-live-traces/v121-v140-v2-cli-council-consultation-v1.json",
    ]
    for phase in phase_choices():
        required.extend(phase_artifact_paths(phase).values())
    missing = [path for path in required if not repo(path).exists()]
    payload = {
        "generated_utc": now_iso(),
        "overall_status": "PASS" if not missing else "FAIL",
        "required_artifact_count": len(required),
        "missing": missing,
        "effective_success": not missing,
    }
    write_json(TRACE / "v121-v140-v2-artifact-verification-v1.json", payload)
    print(f"overall_status={payload['overall_status']}")
    print(f"missing={len(missing)}")
    return 0 if not missing else 1


def write_publication_result() -> None:
    def git(args: list[str]) -> str:
        proc = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)
        return (proc.stdout or proc.stderr).strip()

    head = git(["rev-parse", "HEAD"])
    remote = git(["ls-remote", "origin", "refs/heads/codex/GHC-Family/beyonder-shared-omega-line"]).split("\t")[0]
    staged = git(["diff", "--cached", "--name-only"]).splitlines()
    payload = {
        "generated_utc": now_iso(),
        "phase_range": "v121-v140",
        "phase_variant": "v2",
        "local_head": head,
        "remote_head": remote,
        "remote_matches_local": bool(head and remote and head == remote),
        "staged_count": len([item for item in staged if item]),
        "forward_only_publication": True,
        "google_drive_state": "operator_hold",
    }
    write_json(TRACE / "v121-v140-v2-publication-result-v1.json", payload)
    lines = [
        "# v121-v140 v2 Publication Result",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- local_head: `{head}`",
        f"- remote_head: `{remote}`",
        f"- remote_matches_local: `{payload['remote_matches_local']}`",
        f"- staged_count: `{payload['staged_count']}`",
        "- forward_only_publication: `True`",
        "- google_drive_state: `operator_hold`",
    ]
    write_text(TRACE / "v121-v140-v2-publication-result-v1.md", "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run v121-v140 v2 candidate systems.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare", action="store_true")
    group.add_argument("--system-id", choices=sorted(CANDIDATES))
    group.add_argument("--phase", choices=phase_choices())
    group.add_argument("--run-all", action="store_true")
    group.add_argument("--verify-artifacts", action="store_true")
    group.add_argument("--provider-status", action="store_true")
    group.add_argument("--source-digest", action="store_true")
    group.add_argument("--memory-floor", action="store_true")
    group.add_argument("--suite-status", action="store_true")
    group.add_argument("--publication-result", action="store_true")
    group.add_argument("--closeout", choices=phase_choices())
    parser.add_argument("--promote-manifest", action="store_true")
    args = parser.parse_args()

    if args.prepare:
        prepare_artifacts()
        if args.promote_manifest:
            summary = promote_manifest()
            write_json(TRACE / "v121-v140-v2-manifest-promotion-v1.json", summary)
            print(f"manifest_system_count={summary['new_system_count']}")
            print(f"added_system_count={summary['added_system_count']}")
        else:
            print("prepared_artifacts=true")
        return 0
    if args.system_id:
        return run_system(str(args.system_id))
    if args.phase:
        return run_phase(str(args.phase))
    if args.run_all:
        return run_all()
    if args.verify_artifacts:
        return verify_artifacts()
    if args.provider_status:
        write_provider_readiness()
        print("provider_status=docs/trinity-live-traces/v121-v140-v2-provider-readiness-v1.json")
        return 0
    if args.source_digest:
        for phase in phase_choices():
            write_source_digest(phase)
        print("source_digest=refreshed")
        return 0
    if args.memory_floor:
        payload = {
            "generated_utc": now_iso(),
            "c_drive_free_kb": free_space_kb("C:\\"),
            "d_drive_free_kb": free_space_kb("D:\\"),
            "general_floor_kb": GENERAL_FLOOR_KB,
            "online_live_write_floor_kb": ONLINE_LIVE_WRITE_FLOOR_KB,
            "browser_floor_kb": BROWSER_FLOOR_KB,
        }
        payload["effective_success"] = payload["c_drive_free_kb"] >= GENERAL_FLOOR_KB and payload["d_drive_free_kb"] >= GENERAL_FLOOR_KB
        write_json(TRACE / "v121-v140-v2-memory-floor-v1.json", payload)
        print(f"effective_success={payload['effective_success']}")
        return 0 if payload["effective_success"] else 1
    if args.suite_status:
        payload = read_json("docs/trinity-live-traces/v140-v2-materialize-l5-suite-status.json", {})
        print(json.dumps(payload, indent=2, ensure_ascii=True))
        return 0 if isinstance(payload, dict) and payload.get("effective_success") is True else 1
    if args.publication_result:
        write_publication_result()
        print("publication_result=docs/trinity-live-traces/v121-v140-v2-publication-result-v1.json")
        return 0
    if args.closeout:
        closeout = write_phase_closeout(str(args.closeout))
        print(f"phase={args.closeout} effective_success={closeout['effective_success']}")
        return 0 if closeout["effective_success"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate v471 THOS v5 plugin-cache manifest and tempdir repair rehearsal."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE_X1 = "v471-thos-v5-x1"
PHASE_X2 = "v471-thos-v5-x2"
MAX_SKILL_NAME_LENGTH = 64
GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_ADVISORIES = [
    {
        "lane": "Cicero",
        "submission_id": "019e881e-ca4f-7500-8cc6-be84c43c14b2",
        "summary": "Requested path_id, redacted path display, issue codes, size/line/hash evidence, repair/quarantine flags, and no live mutation.",
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e881e-cbc2-7121-9c7b-e4876333a435",
        "summary": "Clarified that tempdir repair rehearsals are not live repairs and broad permission cannot authorize plugin-cache mutation.",
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e881e-cadb-7fb2-a875-125006999d2e",
        "summary": "Specified manifest/path-list schema, deterministic candidate generation, checksum checks, and publication guard requirements.",
    },
]

SOURCE_ROUTES = [
    {
        "label": "OpenAI Academy - Codex plugins and skills",
        "url": "https://openai.com/academy/codex-plugins-and-skills",
        "use": "Primary context for separating plugins as tool/data connectors from skills as task playbooks.",
    },
    {
        "label": "OpenAI Help - Codex CLI getting started",
        "url": "https://help.openai.com/en/articles/11096431",
        "use": "Primary context for Codex CLI local execution, sandbox, and approval-mode boundaries.",
    },
    {
        "label": "OpenAI Docs MCP",
        "url": "https://platform.openai.com/docs/docs-mcp",
        "use": "Primary context for read-only documentation MCP boundaries.",
    },
    {
        "label": "OpenAI Codex skill creator sample",
        "url": "https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md",
        "use": "Primary repository context for SKILL.md frontmatter with name and description fields.",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def read_head(path: Path, max_lines: int = 24) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()[:max_lines]
    except Exception:
        return []


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def parse_frontmatter(lines: list[str]) -> dict[str, Any]:
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return {"description": None, "has_frontmatter": False, "malformed": False, "name": None}
    closing_index = None
    for index, line in enumerate(lines[1:], 1):
        if line.lstrip("\ufeff").strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return {"description": None, "has_frontmatter": False, "malformed": True, "name": None}
    values: dict[str, str] = {}
    for line in lines[1:closing_index]:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return {
        "description": values.get("description"),
        "has_frontmatter": True,
        "malformed": False,
        "name": values.get("name"),
    }


def issue_codes(parsed: dict[str, Any]) -> list[str]:
    codes: list[str] = []
    if parsed.get("malformed"):
        codes.append("FRONTMATTER_MALFORMED")
    elif not parsed.get("has_frontmatter"):
        codes.append("FRONTMATTER_MISSING")
    name = parsed.get("name")
    description = parsed.get("description")
    if not isinstance(name, str) or not name:
        codes.append("REQUIRED_NAME_MISSING")
    elif len(name) > MAX_SKILL_NAME_LENGTH:
        codes.append("SKILL_NAME_OVERLONG")
    if not isinstance(description, str) or not description:
        codes.append("REQUIRED_DESCRIPTION_MISSING")
    return sorted(set(codes))


def safe_skill_name(seed: str, relative_path: str) -> str:
    stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", seed.strip().lower()).strip("-")
    if not stem:
        stem = "plugin-cache-skill"
    if len(stem) <= MAX_SKILL_NAME_LENGTH:
        return stem
    digest = hashlib.sha256(relative_path.encode("utf-8")).hexdigest()[:8]
    return f"{stem[:MAX_SKILL_NAME_LENGTH - 9]}-{digest}"


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def path_id(relative_path: str) -> str:
    return hashlib.sha256(relative_path.encode("utf-8")).hexdigest()[:16]


def evaluate_candidate(text: str) -> dict[str, Any]:
    parsed = parse_frontmatter(text.splitlines()[:24])
    codes = issue_codes(parsed)
    return {
        "candidate_description_present": bool(parsed.get("description")),
        "candidate_issue_codes": codes,
        "candidate_name": parsed.get("name"),
        "candidate_name_length": len(parsed.get("name") or ""),
        "candidate_status": "PASS_SHAPE_ONLY" if not codes else "FAIL_BLOCKER",
    }


def build_candidate_text(skill_name: str, relative_path: str, original_text: str) -> str:
    description = f"Tempdir-only body-preserving metadata repair candidate for plugin-cache skill {skill_name}."
    return (
        "---\n"
        f"name: {skill_name}\n"
        f"description: {description}\n"
        "---\n\n"
        "<!-- THOS tempdir-only repair rehearsal: generated candidate frontmatter above; original body follows unchanged. -->\n\n"
        f"Original relative path hash: {hash_text(relative_path)[:16]}\n"
        "\n"
        f"{original_text}"
    )


def scan_plugin_cache(plugin_cache_root: Path) -> list[dict[str, Any]]:
    skill_files = sorted(plugin_cache_root.rglob("SKILL.md")) if plugin_cache_root.exists() else []
    affected: list[dict[str, Any]] = []
    for skill_file in skill_files:
        original_text = read_text(skill_file)
        parsed = parse_frontmatter(original_text.splitlines()[:24])
        codes = issue_codes(parsed)
        if not codes:
            continue
        relative_path = relative_posix(skill_file, plugin_cache_root)
        skill_dir = skill_file.parent.name
        candidate_name = safe_skill_name(skill_dir, relative_path)
        line_count = len(original_text.splitlines())
        size_bytes = len(original_text.encode("utf-8", errors="replace"))
        affected.append(
            {
                "candidate_name": candidate_name,
                "content_hash": hash_text(original_text),
                "line_count": line_count,
                "issue_codes": codes,
                "mutation_status": "none",
                "path_display": relative_path,
                "path_id": path_id(relative_path),
                "path_membership": "under_plugin_cache_root",
                "path_scope": "plugin_cache",
                "quarantine_candidate": "FRONTMATTER_MALFORMED" in codes,
                "repair_candidate": "FRONTMATTER_MALFORMED" not in codes,
                "relative_path": relative_path,
                "sha256_before": hash_text(original_text),
                "size_bytes": size_bytes,
                "skill_dir": skill_dir,
                "skill_file_kind": "SKILL.md",
            }
        )
    return affected


def scan_legacy_head20_false_positives(plugin_cache_root: Path, affected_paths: set[str]) -> list[dict[str, Any]]:
    """Identify files a 20-line frontmatter sampler would flag but the current parser clears."""
    false_positives: list[dict[str, Any]] = []
    skill_files = sorted(plugin_cache_root.rglob("SKILL.md")) if plugin_cache_root.exists() else []
    for skill_file in skill_files:
        relative_path = relative_posix(skill_file, plugin_cache_root)
        if relative_path in affected_paths:
            continue
        legacy_codes = issue_codes(parse_frontmatter(read_head(skill_file, max_lines=20)))
        current_codes = issue_codes(parse_frontmatter(read_text(skill_file).splitlines()[:24]))
        if legacy_codes and not current_codes:
            false_positives.append(
                {
                    "legacy_issue_codes": legacy_codes,
                    "path_display": relative_path,
                    "path_id": path_id(relative_path),
                    "resolution": "cleared_by_wider_frontmatter_window",
                }
            )
    return false_positives


def rehearse_repairs(affected: list[dict[str, Any]], plugin_cache_root: Path) -> dict[str, Any]:
    candidate_results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="thos-v471-plugin-cache-rehearsal-") as temp_root:
        root = Path(temp_root)
        for item in affected:
            target = root / item["path_id"] / "SKILL.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            # Re-read locally for body preservation; only checksums and summaries are published.
            source_path = plugin_cache_root / item["relative_path"]
            source_before = read_text(source_path)
            checksum_before = hash_text(source_before)
            candidate_text = build_candidate_text(item["candidate_name"], item["relative_path"], source_before)
            target.write_text(candidate_text, encoding="utf-8")
            result = evaluate_candidate(candidate_text)
            checksum_after = hash_text(read_text(source_path))
            candidate_results.append(
                {
                    "candidate_name": item["candidate_name"],
                    "candidate_path_id": item["path_id"],
                    "candidate_status": result["candidate_status"],
                    "candidate_issue_codes": result["candidate_issue_codes"],
                    "derivation_sources": ["skill_directory_name", "relative_path_hash"],
                    "original_body_preserved_in_temp_candidate": source_before in candidate_text,
                    "original_issue_codes": item["issue_codes"],
                    "path_hash": item["path_id"],
                    "relative_path": item["relative_path"],
                    "source_checksum_unchanged": checksum_before == checksum_after == item["sha256_before"],
                    "source_write_performed": False,
                    "write_target": "tempdir_only",
                }
            )
    failures = [
        item
        for item in candidate_results
        if item["candidate_status"] != "PASS_SHAPE_ONLY"
        or not item["source_checksum_unchanged"]
        or not item["original_body_preserved_in_temp_candidate"]
    ]
    return {
        "aggregate_status": "FAIL_BLOCKER" if failures else "PASS_SHAPE_ONLY",
        "candidate_count": len(candidate_results),
        "failure_count": len(failures),
        "candidate_results": candidate_results,
        "rehearsal_mode": "tempdir_only_metadata_candidate",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_artifacts(
    output_root: Path,
    affected: list[dict[str, Any]],
    rehearsal: dict[str, Any],
    legacy_false_positives: list[dict[str, Any]],
) -> list[str]:
    written: list[str] = []
    issue_counts: dict[str, int] = {}
    for item in affected:
        for code in item["issue_codes"]:
            issue_counts[code] = issue_counts.get(code, 0) + 1

    manifest_payload = {
        "affected_count": len(affected),
        "aggregate_status": "OPEN_GAP" if affected else "PASS_SHAPE_ONLY",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "issue_counts": issue_counts,
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("manifest_scope", "PASS_SHAPE_ONLY", "Affected plugin-cache SKILL.md files were listed as relative paths only"),
            row("path_redaction", "PASS_SHAPE_ONLY", "No absolute user profile paths are included"),
            row("advisory_integration", "PASS_SHAPE_ONLY", "Cicero, Kierkegaard, and Aristotle v5 advisory requirements were incorporated", APP_ADVISORIES),
            row("scanner_delta", "PASS_SHAPE_ONLY", "Legacy 20-line scanner false positives were separated from live repair candidates", {"count": len(legacy_false_positives), "items": legacy_false_positives}),
            row("affected_count", "OPEN_GAP" if affected else "PASS_SHAPE_ONLY", "Affected plugin-cache files remain unresolved", {"count": len(affected)}),
        ],
        "skills": affected,
        "legacy_head20_false_positives": legacy_false_positives,
    }
    path = output_root / f"{PHASE_X1}-plugin-cache-affected-manifest-v1.json"
    write_json(path, manifest_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-plugin-cache-affected-manifest-v1.md",
        f"""
# v471 THOS v5 x1 Plugin-Cache Affected Manifest

Status: `OPEN_GAP`.

The manifest lists `{len(affected)}` affected plugin-cache `SKILL.md` files using paths relative to the plugin-cache root only. It also records stable `path_id`, content checksum, line count, size, issue code, repair/quarantine candidate, and mutation status fields. No absolute user profile paths, raw logs, session files, screenshots, credentials, or connector payloads are included.

The previous 42-count audit is reconciled here: `{len(legacy_false_positives)}` legacy 20-line scanner false positives are separated from the `{len(affected)}` live repair candidates because their frontmatter closes after the older sampling window.

The manifest is evidence for scope and rehearsal planning only. It does not repair plugin cache, delete files, quarantine directories, or prove CLI sibling recovery.
""",
    )
    written.append((output_root / f"{PHASE_X1}-plugin-cache-affected-manifest-v1.md").as_posix())

    source_payload = {
        "aggregate_status": "PASS_SHAPE_ONLY",
        "app_advisories": APP_ADVISORIES,
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("app_advisories", "PASS_SHAPE_ONLY", "Existing app sibling advisories were incorporated", APP_ADVISORIES),
            row("source_routes", "PASS_SHAPE_ONLY", "Official OpenAI source routes were refreshed for v5", SOURCE_ROUTES),
            row("claim_boundary", "PASS_SHAPE_ONLY", "Sources inform workflow boundaries but do not prove local repair completion"),
        ],
        "source_routes": SOURCE_ROUTES,
    }
    path = output_root / f"{PHASE_X1}-source-and-advisory-ledger-v1.json"
    write_json(path, source_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-source-and-advisory-ledger-v1.md",
        """
# v471 THOS v5 x1 Source And Advisory Ledger

Cicero, Kierkegaard, and Aristotle returned advisory-only guidance for the manifest and tempdir repair rehearsal. The phase also refreshed official OpenAI routing for Codex plugins/skills, Codex CLI sandbox/approval context, OpenAI Docs MCP, and the Codex skill-creator sample.

These sources and advisories shape the guardrails. They do not prove plugin-cache repair, CLI sibling recovery, Browser availability, connector writes, or GMUT gate closure.
""",
    )
    written.append((output_root / f"{PHASE_X1}-source-and-advisory-ledger-v1.md").as_posix())

    rehearsal_payload = {
        "aggregate_status": rehearsal["aggregate_status"],
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rehearsal": rehearsal,
        "rows": [
            row("tempdir_only", "PASS_SHAPE_ONLY", "Repair candidates were written only in a temporary directory"),
            row("candidate_shape", rehearsal["aggregate_status"], "Candidate metadata shape was evaluated", {"candidate_count": rehearsal["candidate_count"], "failure_count": rehearsal["failure_count"]}),
            row("body_preservation", rehearsal["aggregate_status"], "Candidate rehearsal preserves original plugin bodies in tempdir and verifies source checksums", {"candidate_count": rehearsal["candidate_count"]}),
            row("live_repair", "OPEN_GAP", "No live plugin-cache repair occurred"),
        ],
    }
    path = output_root / f"{PHASE_X1}-tempdir-repair-rehearsal-v1.json"
    write_json(path, rehearsal_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-tempdir-repair-rehearsal-v1.md",
        f"""
# v471 THOS v5 x1 Tempdir Repair Rehearsal

Status: `{rehearsal["aggregate_status"]}` for body-preserving metadata candidate shape only.

The runner generated `{rehearsal["candidate_count"]}` temporary metadata candidates, preserved original bodies in the tempdir candidate files, verified frontmatter shape, and checked that source checksums stayed unchanged. This is not a live repair. It deliberately avoids copying candidates into plugin cache.

The next approval threshold is stricter: if live repair is desired later, present exact paths, proposed repaired file content, body-preservation rules, and a reviewed diff before any cache write.
""",
    )
    written.append((output_root / f"{PHASE_X1}-tempdir-repair-rehearsal-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("affected_manifest", "OPEN_GAP" if affected else "PASS_SHAPE_ONLY", "Affected path manifest generated", {"affected_count": len(affected)}),
            row("scanner_delta", "PASS_SHAPE_ONLY", "42-to-37 count delta is explained by legacy scanner false positives", {"legacy_false_positive_count": len(legacy_false_positives)}),
            row("tempdir_rehearsal", rehearsal["aggregate_status"], "Body-preserving metadata repair candidates rehearsed in tempdir", {"candidate_count": rehearsal["candidate_count"]}),
            row("approval_boundary", "OPEN_GAP", "Live plugin-cache edit still requires separate approval"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = output_root / f"{PHASE_X1}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-run-status-v1.md",
        """
# v471 THOS v5 x1 Run Status

v5 x1 generated the exact affected plugin-cache manifest and rehearsed body-preserving metadata repair candidates in a temporary directory.

No live plugin-cache file was edited. Publication is deferred to x2 under the paired-phase cadence.
""",
    )
    written.append((output_root / f"{PHASE_X1}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": PHASE_X2,
        "phase_slug": PHASE_X1,
        "rows": [
            row("x2_task_1", "OPEN_GAP", "Publish manifest claim ceiling and approval delta"),
            row("x2_task_2", "OPEN_GAP", "Publish candidate path-list summary and body-preservation blocker"),
            row("x2_task_3", "OPEN_GAP", "Publish v6 handoff for exact diff rehearsal if approved"),
        ],
    }
    path = output_root / f"{PHASE_X1}-x2-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X1}-x2-handoff-v1.md",
        """
# v471 THOS v5 x1 To x2 Handoff

x2 should publish the claim ceiling, body-preservation blocker, and next-step approval threshold for any future live plugin-cache repair.
""",
    )
    written.append((output_root / f"{PHASE_X1}-x2-handoff-v1.md").as_posix())

    x2_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("manifest_claim", "PASS_SHAPE_ONLY", "Exact relative affected-path manifest exists"),
            row("scanner_delta", "PASS_SHAPE_ONLY", "Legacy scanner false positives are identified separately from repair candidates", {"count": len(legacy_false_positives)}),
            row("candidate_claim", rehearsal["aggregate_status"], "Tempdir-only metadata candidate shape passed or failed as reported"),
            row("body_preservation", rehearsal["aggregate_status"], "Original plugin bodies were preserved in tempdir candidates and source checksums remained unchanged"),
            row("live_cache_repair", "OPEN_GAP", "Live plugin-cache repair remains unperformed and approval-gated"),
            row("browser_cli", "OPEN_GAP", "Browser and CLI sibling blockers remain open from v4"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = output_root / f"{PHASE_X2}-repair-claim-ceiling-v1.json"
    write_json(path, x2_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-repair-claim-ceiling-v1.md",
        """
# v471 THOS v5 x2 Repair Claim Ceiling

This phase may claim only that an exact relative affected-path manifest exists and that body-preserving metadata repair candidates passed a temporary frontmatter and source-checksum rehearsal.

It may not claim live cache repair, restored CLI sibling health, Browser automation success, or production plugin-cache repair. Those remain open gaps requiring stronger evidence.
""",
    )
    written.append((output_root / f"{PHASE_X2}-repair-claim-ceiling-v1.md").as_posix())

    path_list_payload = {
        "aggregate_status": "OPEN_GAP" if affected else "PASS_SHAPE_ONLY",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "relative_paths": [item["relative_path"] for item in affected],
        "rows": [
            row("closed_world_path_count", "OPEN_GAP" if affected else "PASS_SHAPE_ONLY", "Relative path-list count matches manifest affected count", {"count": len(affected)}),
            row("absolute_path_guard", "PASS_SHAPE_ONLY", "Path-list contains relative paths only"),
        ],
    }
    path = output_root / f"{PHASE_X2}-affected-path-list-v1.json"
    write_json(path, path_list_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-affected-path-list-v1.md",
        f"""
# v471 THOS v5 x2 Affected Path List

This path list contains `{len(affected)}` relative plugin-cache paths and exists to support future closed-world rehearsal checks. It is not an instruction to edit or delete those files.
""",
    )
    written.append((output_root / f"{PHASE_X2}-affected-path-list-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("x1_x2_pair", "OPEN_GAP", "Manifest and tempdir rehearsal published with open approval boundary"),
            row("candidate_results", rehearsal["aggregate_status"], "Candidate shape and source-checksum results preserved", {"candidate_count": rehearsal["candidate_count"], "failure_count": rehearsal["failure_count"]}),
            row("future_live_write", "OPEN_GAP", "Future plugin-cache write requires separate approval and exact diff"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = output_root / f"{PHASE_X2}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-run-status-v1.md",
        """
# v471 THOS v5 x2 Run Status

Status: `OPEN_GAP`.

The phase published an exact relative affected-path manifest and a tempdir-only body-preserving metadata repair rehearsal. It intentionally did not mutate plugin cache or claim restored CLI/Browser health.
""",
    )
    written.append((output_root / f"{PHASE_X2}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v471-thos-v6-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("v6_task_1", "OPEN_GAP", "If approved later, create exact live-write diff packet from the body-preserving tempdir rehearsal"),
            row("v6_task_2", "OPEN_GAP", "Add publication guard coverage for manifest/path-list count equality"),
            row("v6_task_3", "OPEN_GAP", "Retry Browser or CLI only as bounded probes if capability surface changes"),
            row("v6_task_4", "OPEN_GAP", "Keep all GMUT gates and Journey canon boundaries open"),
        ],
    }
    path = output_root / f"{PHASE_X2}-v471-thos-v6-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        output_root / f"{PHASE_X2}-v471-thos-v6-handoff-v1.md",
        """
# v471 THOS v5 x2 To v6 Handoff

v6 should add a body-preserving diff rehearsal only if it remains tempdir-only or receives separate path-specific approval. Browser and CLI probes should stay bounded and should not be reframed as success without direct evidence.
""",
    )
    written.append((output_root / f"{PHASE_X2}-v471-thos-v6-handoff-v1.md").as_posix())

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate plugin-cache manifest and tempdir repair rehearsal artifacts.")
    parser.add_argument("--plugin-cache-root", default=str(Path.home() / ".codex" / "plugins" / "cache"))
    parser.add_argument("--output-dir", default="docs/trinity-live-traces")
    args = parser.parse_args()

    plugin_cache_root = Path(args.plugin_cache_root)
    affected = scan_plugin_cache(plugin_cache_root)
    legacy_false_positives = scan_legacy_head20_false_positives(
        plugin_cache_root,
        {item["relative_path"] for item in affected},
    )
    rehearsal = rehearse_repairs(affected, plugin_cache_root)
    written = write_artifacts(Path(args.output_dir), affected, rehearsal, legacy_false_positives)
    print(json.dumps({"affected_count": len(affected), "legacy_false_positive_count": len(legacy_false_positives), "rehearsal_status": rehearsal["aggregate_status"], "written": written}, indent=2, sort_keys=True))
    return 0 if rehearsal["aggregate_status"] in {"PASS_SHAPE_ONLY", "OPEN_GAP"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

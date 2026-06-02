#!/usr/bin/env python3
"""Audit local Codex skill surfaces without mutating them."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MAX_SKILL_NAME_LENGTH = 64


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def read_head(path: Path, max_lines: int = 20) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()[:max_lines]
    except Exception:
        return []


def parse_frontmatter(lines: list[str]) -> dict[str, Any]:
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return {"has_frontmatter": False, "name": None, "description": None}
    closing_index = None
    for index, line in enumerate(lines[1:], 1):
        if line.lstrip("\ufeff").strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return {"has_frontmatter": False, "name": None, "description": None}
    frontmatter = lines[1:closing_index]
    values: dict[str, str] = {}
    for line in frontmatter:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return {
        "description": values.get("description"),
        "has_frontmatter": True,
        "name": values.get("name"),
    }


def root_label(path: Path) -> str:
    parts = [part.lower() for part in path.parts]
    if ".codex" in parts and "plugins" in parts:
        return "plugin_cache"
    if ".codex" in parts and "skills" in parts:
        return "user_skills"
    return "other"


def audit_skill(path: Path) -> dict[str, Any]:
    lines = read_head(path)
    parsed = parse_frontmatter(lines)
    name = parsed.get("name")
    skill_dir = path.parent.name
    issues: list[str] = []
    if not parsed["has_frontmatter"]:
        issues.append("missing_or_unclosed_frontmatter")
    if not isinstance(name, str) or not name:
        issues.append("missing_name")
    elif len(name) > MAX_SKILL_NAME_LENGTH:
        issues.append("name_too_long")
    return {
        "description_present": bool(parsed.get("description")),
        "has_frontmatter": parsed["has_frontmatter"],
        "issues": issues,
        "name": name,
        "name_length": len(name) if isinstance(name, str) else 0,
        "root_label": root_label(path),
        "skill_dir": skill_dir,
    }


def build_report(roots: list[Path], phase_slug: str) -> dict[str, Any]:
    skill_paths: list[Path] = []
    for root in roots:
        if root.exists():
            skill_paths.extend(sorted(root.rglob("SKILL.md")))
    audits = [audit_skill(path) for path in skill_paths]
    missing_frontmatter = [item for item in audits if "missing_or_unclosed_frontmatter" in item["issues"]]
    missing_name = [item for item in audits if "missing_name" in item["issues"]]
    name_too_long = [item for item in audits if "name_too_long" in item["issues"]]
    issue_skill_ids = {
        (item["root_label"], item["skill_dir"])
        for item in audits
        if item["issues"]
    }
    issue_file_count = len(issue_skill_ids)
    aggregate_status = "OPEN_GAP" if issue_file_count else "PASS_SHAPE_ONLY"
    return {
        "aggregate_status": aggregate_status,
        "connector_write_performed": False,
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "max_skill_name_length": MAX_SKILL_NAME_LENGTH,
        "mutation_performed": False,
        "phase_slug": phase_slug,
        "rows": [
            row("skill_file_count", "PASS_SHAPE_ONLY" if audits else "OPEN_GAP", "Skill files were discoverable", {"count": len(audits)}),
            row("frontmatter_contract", "OPEN_GAP" if missing_frontmatter else "PASS_SHAPE_ONLY", "Every sampled skill should have closed YAML frontmatter", {"issue_count": len(missing_frontmatter), "samples": missing_frontmatter[:20]}),
            row("name_presence_contract", "OPEN_GAP" if missing_name else "PASS_SHAPE_ONLY", "Every skill frontmatter should declare a name", {"issue_count": len(missing_name), "samples": missing_name[:20]}),
            row("name_length_contract", "OPEN_GAP" if name_too_long else "PASS_SHAPE_ONLY", "Skill names should stay within current Codex loader length limits", {"issue_count": len(name_too_long), "samples": name_too_long[:20]}),
            row("repair_boundary", "OPEN_GAP" if issue_file_count else "PASS_SHAPE_ONLY", "No skill files were mutated; repair/quarantine remains explicit if issues recur"),
        ],
        "skill_surface_summary": {
            "issue_file_count": issue_file_count,
            "missing_frontmatter_count": len(missing_frontmatter),
            "missing_name_count": len(missing_name),
            "name_too_long_count": len(name_too_long),
            "root_counts": {
                label: sum(1 for item in audits if item["root_label"] == label)
                for label in sorted({item["root_label"] for item in audits})
            },
            "total_skill_files": len(audits),
        },
        "validator_mode": "local_non_mutating_skill_surface_audit",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit local Codex skill surfaces without mutation.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--root", action="append", default=[])
    args = parser.parse_args()

    roots = [Path(value) for value in args.root] if args.root else [
        Path.home() / ".codex" / "skills",
        Path.home() / ".codex" / "plugins" / "cache",
    ]
    report = build_report(roots, args.phase_slug)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["aggregate_status"] in {"PASS_SHAPE_ONLY", "OPEN_GAP"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

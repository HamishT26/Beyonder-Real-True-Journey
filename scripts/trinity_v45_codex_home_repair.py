#!/usr/bin/env python3
"""Repair reversible local Codex-home issues that directly affect the V45 CLI lane."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

from trinity_v45_common import (
    GLOBAL_CODEX_AUTH,
    GLOBAL_CODEX_BACKUPS,
    GLOBAL_CODEX_HOME,
    GLOBAL_CODEX_SKILLS,
    now_iso,
    write_json,
    write_text,
)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v45-codex-home-repair-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v45-codex-home-repair-v1.md"
UTF8_BOM = b"\xef\xbb\xbf"


def _scan_skill_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not GLOBAL_CODEX_SKILLS.exists():
        return rows
    for path in sorted(GLOBAL_CODEX_SKILLS.rglob("SKILL.md")):
        raw = path.read_bytes()
        has_bom = raw.startswith(UTF8_BOM)
        normalized = raw[len(UTF8_BOM) :] if has_bom else raw
        starts_with_yaml = normalized.startswith(b"---")
        rows.append(
            {
                "path": str(path),
                "has_utf8_bom": has_bom,
                "starts_with_yaml_frontmatter_after_bom_strip": starts_with_yaml,
                "candidate_repair": bool(has_bom and starts_with_yaml),
            }
        )
    return rows


def _repair_bom_files(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    repaired: list[dict[str, Any]] = []
    timestamp = now_iso().replace(":", "").replace("+00:00", "Z")
    backup_root = GLOBAL_CODEX_BACKUPS / "skill-bom-fix" / timestamp
    for row in rows:
        if not row.get("candidate_repair"):
            continue
        path = Path(str(row["path"]))
        relative = path.relative_to(GLOBAL_CODEX_HOME)
        backup_path = backup_root / relative
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_path)
        raw = path.read_bytes()
        path.write_bytes(raw[len(UTF8_BOM) :])
        repaired.append(
            {
                "path": str(path),
                "backup_path": str(backup_path),
            }
        )
    return repaired


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V45 Codex Home Repair",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Local Codex hygiene state: `{payload['local_codex_hygiene_state']}`",
        f"- Skill files scanned: `{payload['skill_file_count']}`",
        f"- BOM-frontmatter candidates: `{payload['bom_frontmatter_candidate_count']}`",
        f"- Files repaired: `{payload['repaired_file_count']}`",
        "",
    ]
    if payload.get("repaired_files"):
        lines.extend(["## Repaired Files", ""])
        lines.extend(f"- `{row['path']}` -> backup `{row['backup_path']}`" for row in payload["repaired_files"])
    if payload.get("auth_file"):
        lines.extend(["", "## Auth Metadata", ""])
        for key, value in payload["auth_file"].items():
            if key == "path":
                lines.append(f"- `{key}`: `{value}`")
            elif key != "sensitive_contents_present":
                lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair reversible local Codex-home issues.")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    scanned = _scan_skill_files()
    candidates = [row for row in scanned if row.get("candidate_repair")]
    repaired = _repair_bom_files(candidates) if args.apply else []
    auth_file = {
        "path": str(GLOBAL_CODEX_AUTH),
        "exists": GLOBAL_CODEX_AUTH.exists(),
        "size_bytes": GLOBAL_CODEX_AUTH.stat().st_size if GLOBAL_CODEX_AUTH.exists() else 0,
        "modified_epoch": int(GLOBAL_CODEX_AUTH.stat().st_mtime) if GLOBAL_CODEX_AUTH.exists() else 0,
        "sensitive_contents_present": GLOBAL_CODEX_AUTH.exists(),
    }

    if repaired:
        hygiene_state = "skill_bom_frontmatter_repaired"
    elif candidates:
        hygiene_state = "repairable_skill_bom_frontmatter_detected"
    else:
        hygiene_state = "no_skill_bom_frontmatter_issue_detected"

    payload = {
        "generated_utc": now_iso(),
        "phase": "v45_omega",
        "overall_status": "PASS",
        "local_codex_hygiene_state": hygiene_state,
        "apply_requested": args.apply,
        "global_codex_home": str(GLOBAL_CODEX_HOME),
        "skill_file_count": len(scanned),
        "bom_frontmatter_candidate_count": len(candidates),
        "repaired_file_count": len(repaired),
        "repaired_files": repaired,
        "skill_scan": scanned,
        "auth_file": auth_file,
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

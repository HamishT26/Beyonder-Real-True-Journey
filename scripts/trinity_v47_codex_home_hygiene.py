#!/usr/bin/env python3
"""Back up and repair reversible Codex-home hygiene issues seen in V46/V47."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from typing import Any

from trinity_v47_common import GLOBAL_CODEX_BACKUP_ROOT, GLOBAL_CODEX_CONFIG, GLOBAL_CODEX_SKILLS, ROOT, now_iso, write_json, write_text

DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v47-codex-home-hygiene-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v47-codex-home-hygiene-v1.md"
SKILL_FIXES = {
    "body-reliability-gating": "Body Reliability Gating",
    "heart-conformance-gating": "Heart Conformance Gating",
    "mind-expansion-systems": "Mind Expansion Systems",
    "trinity-expansion-qa": "Trinity Expansion QA",
    "trinity-expansion-release": "Trinity Expansion Release",
    "trinity-live-gating-operations": "Trinity Live Gating Operations",
}


def _has_top_level_key(text: str, key: str) -> bool:
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("["):
            return False
        if re.match(rf"^{re.escape(key)}\s*=", line):
            return True
    return False


def _insert_top_level_key(text: str, assignment: str) -> str:
    lines = text.rstrip().splitlines()
    for index, raw_line in enumerate(lines):
        if raw_line.strip().startswith("["):
            return "\n".join([*lines[:index], assignment, "", *lines[index:]]) + "\n"
    return "\n".join([*lines, assignment]) + "\n"


def _backup(path: Path, backup_root: Path) -> Path:
    rel = path.relative_to(path.anchor) if path.is_absolute() else path
    dest = backup_root / str(rel).replace(":", "")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)
    return dest


def _frontmatter(text: str, name: str) -> str:
    if text.lstrip().startswith("---"):
        return text
    desc = f"Operate the {name} local Codex skill restored by V47 hygiene."
    return f"---\nname: \"{name.lower().replace(' ', '-')}\"\ndescription: \"{desc}\"\n---\n\n{text.lstrip()}"


def _repair_config(backup_root: Path) -> dict[str, Any]:
    result = {"config_exists": GLOBAL_CODEX_CONFIG.exists(), "backup_path": "", "changed": False, "actions": []}
    if not GLOBAL_CODEX_CONFIG.exists():
        return result
    text = GLOBAL_CODEX_CONFIG.read_text(encoding="utf-8")
    new_text = text
    if re.search(r"(?m)^chronicle\s*=\s*false\s*$", new_text):
        _backup(GLOBAL_CODEX_CONFIG, backup_root)
        new_text = re.sub(r"(?m)^chronicle\s*=\s*false\s*\r?\n?", "", new_text)
        result["actions"].append("removed_unknown_chronicle_false_key")
    suppress_top_level = _has_top_level_key(new_text, "suppress_unstable_features_warning")
    suppress_anywhere = "suppress_unstable_features_warning" in new_text
    if suppress_anywhere and not suppress_top_level:
        if result["actions"] == []:
            _backup(GLOBAL_CODEX_CONFIG, backup_root)
        new_text = re.sub(r"(?m)^\s*suppress_unstable_features_warning\s*=\s*true\s*\r?\n?", "", new_text)
        new_text = _insert_top_level_key(new_text, "suppress_unstable_features_warning = true")
        result["actions"].append("moved_suppress_unstable_features_warning_to_top_level")
    elif not suppress_anywhere:
        if result["actions"] == []:
            _backup(GLOBAL_CODEX_CONFIG, backup_root)
        new_text = _insert_top_level_key(new_text, "suppress_unstable_features_warning = true")
        result["actions"].append("added_suppress_unstable_features_warning_true")
    if new_text != text:
        GLOBAL_CODEX_CONFIG.write_text(new_text, encoding="utf-8")
        result["changed"] = True
        result["backup_path"] = str(backup_root)
    return result


def _repair_skills(backup_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for folder, display in SKILL_FIXES.items():
        path = GLOBAL_CODEX_SKILLS / folder / "SKILL.md"
        row: dict[str, Any] = {"path": str(path), "exists": path.exists(), "changed": False, "backup_path": ""}
        if not path.exists():
            rows.append(row)
            continue
        raw_text = path.read_text(encoding="utf-8")
        text = raw_text.lstrip("\ufeff")
        repaired = _frontmatter(text, display)
        if repaired != raw_text:
            row["backup_path"] = str(_backup(path, backup_root))
            path.write_text(repaired, encoding="utf-8")
            row["changed"] = True
        rows.append(row)
    return rows


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V47 Codex Home Hygiene",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Hygiene state: `{payload['local_codex_hygiene_state']}`",
        f"- Backup root: `{payload['backup_root']}`",
        "",
        "## Actions",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["actions"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair reversible V47 Codex-home hygiene issues.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    backup_root = GLOBAL_CODEX_BACKUP_ROOT / now_iso().replace(":", "").replace("+", "")
    actions: list[str] = []

    if args.dry_run:
        payload = {
            "generated_utc": now_iso(),
            "phase": "v47_omega",
            "overall_status": "PASS",
            "local_codex_hygiene_state": "dry_run_only",
            "backup_root": "",
            "actions": ["dry_run_no_changes"],
            "config_result": {},
            "skill_results": [],
        }
    else:
        config_result = _repair_config(backup_root)
        skill_results = _repair_skills(backup_root)
        actions.extend(config_result.get("actions", []))
        actions.extend(f"repaired_skill_frontmatter:{row['path']}" for row in skill_results if row.get("changed"))
        if not actions:
            actions.append("no_reversible_hygiene_changes_needed")
        payload = {
            "generated_utc": now_iso(),
            "phase": "v47_omega",
            "overall_status": "PASS",
            "local_codex_hygiene_state": "reversible_hygiene_repaired" if any("repaired" in item or "removed" in item or "added" in item for item in actions) else "no_changes_needed",
            "backup_root": str(backup_root) if any("repaired" in item or "removed" in item or "added" in item for item in actions) else "",
            "actions": actions,
            "config_result": config_result,
            "skill_results": skill_results,
            "residuals_classified_not_repaired": [
                "state_db_migration_warning",
                "legacy_log_file_in_use_warning",
                "mcp_token_refresh_residual",
                "powershell_shell_snapshot_unsupported",
            ],
        }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

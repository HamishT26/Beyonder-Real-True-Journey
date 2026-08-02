#!/usr/bin/env python3
"""Additively install the ten validated Ilyra v659-v1 skills."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import ghc_family_v659_v1_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SOURCE_ROOT = PHASE / "skills"
GLOBAL_ROOT = Path.home() / ".codex/skills"
QUICK_VALIDATE = GLOBAL_ROOT / ".system/skill-creator/scripts/quick_validate.py"


def digest_map(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def main() -> None:
    destinations = {name: GLOBAL_ROOT / name for name, _ in d.SELF_SKILL_SPECS}
    existing = sorted(name for name, path in destinations.items() if path.exists())
    if existing:
        raise RuntimeError(f"additive install refused existing skill names: {existing}")
    rows = []
    for skill_name, _ in d.SELF_SKILL_SPECS:
        source = SOURCE_ROOT / skill_name
        destination = destinations[skill_name]
        shutil.copytree(source, destination)
        validation = subprocess.run(
            [sys.executable, "-X", "utf8", str(QUICK_VALIDATE), str(destination)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        source_hashes = digest_map(source)
        destination_hashes = digest_map(destination)
        mismatches = sorted(
            set(source_hashes) ^ set(destination_hashes)
            | {path for path in set(source_hashes) & set(destination_hashes) if source_hashes[path] != destination_hashes[path]}
        )
        rows.append(
            {
                "skill_name": skill_name,
                "valid": validation.returncode == 0 and not mismatches,
                "quick_validate_returncode": validation.returncode,
                "file_count": len(source_hashes),
                "hash_mismatch_count": len(mismatches),
                "hash_mismatch_paths": mismatches,
                "existing_skill_replaced": False,
            }
        )
    payload = {
        "schema": "ghc.family.global-skill-installation.v1",
        "owner": d.OWNER,
        "phase": d.PHASE,
        "skill_count": len(rows),
        "valid_skill_count": sum(row["valid"] for row in rows),
        "all_valid": all(row["valid"] for row in rows),
        "existing_skill_replaced": False,
        "plugin_cache_mutated": False,
        "rows": rows,
        "boundary": "Additive local Codex skill installation only; no plugin, sibling lane, identity, production, authority, or Stage 20 mutation.",
    }
    output = PHASE / "tooling/global-skill-installation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skill_count": len(rows), "valid": payload["all_valid"]}, sort_keys=True))
    if not payload["all_valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

"""Install exactly ten validated skill candidates by byte-preserving additive copy."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def file_map(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates-root", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--validator", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    candidates = sorted(path for path in args.candidates_root.iterdir() if path.is_dir())
    if len(candidates) != 10:
        raise SystemExit(f"expected ten candidates, found {len(candidates)}")

    rows = []
    shared: dict[str, str] = {}
    for candidate in candidates:
        target = args.skill_root / candidate.name
        source_map = file_map(candidate)
        state = "installed_new"
        if target.exists():
            if not target.is_dir() or file_map(target) != source_map:
                raise SystemExit(f"global skill collision: {candidate.name}")
            state = "reused_exact_existing"
        else:
            shutil.copytree(candidate, target)
        installed_map = file_map(target)
        if source_map != installed_map:
            raise SystemExit(f"installed byte parity failed: {candidate.name}")
        validation = subprocess.run(
            [sys.executable, "-X", "utf8", str(args.validator), str(target)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if validation.returncode != 0:
            raise SystemExit(f"installed validation failed: {candidate.name}")
        for rel, digest in installed_map.items():
            if rel.startswith("scripts/") and rel.endswith(".py"):
                prior = shared.setdefault(Path(rel).name, digest)
                if prior != digest:
                    raise SystemExit(f"shared runner collision: {rel}")
        rows.append(
            {
                "skill": candidate.name,
                "state": state,
                "file_count": len(installed_map),
                "byte_parity": True,
                "quick_validate": True,
                "source_manifest_sha256": hashlib.sha256(
                    json.dumps(source_map, sort_keys=True, separators=(",", ":")).encode("utf-8")
                ).hexdigest(),
                "rollback": "Select the retained source guide or prior validated skill; do not delete evidence.",
            }
        )
    shared_rows = [
        {"runner": name, "sha256": digest, "unique_credit": 1}
        for name, digest in sorted(shared.items())
    ]
    passed = len(rows) == 10 and len(shared_rows) == 5 and all(row["byte_parity"] and row["quick_validate"] for row in rows)
    payload = {
        "schema": "ghc.family.elaren-v685-v7.global-promotion-installation.v1",
        "status": "PASS" if passed else "FAIL",
        "installed_skill_count": len(rows),
        "skills": rows,
        "unique_shared_runner_count": len(shared_rows),
        "shared_runners": shared_rows,
        "additive": True,
        "historical_skills_deleted": False,
        "plugin_cache_mutated": False,
        "global_availability_is_not_context_reload_proof": True,
        "same_owner_only": True,
    }
    write_json(args.output, payload)
    print(json.dumps({"status": payload["status"], "skills": len(rows), "unique_shared_runners": len(shared_rows)}, separators=(",", ":")))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Trinity local skill installer system.

Installs local repo skills into the Codex skills directory with optional
verification and machine-readable reporting.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_SRC = ROOT / "skills"
DEFAULT_DEST = Path.home() / ".codex" / "skills"
DEFAULT_REPORT = ROOT / "docs" / "trinity-skill-installer-report.json"


def _repo_path(path_str: str) -> Path:
    p = (ROOT / path_str).resolve()
    p.relative_to(ROOT)
    return p


def _discover_skills(include: list[str]) -> list[Path]:
    names = [p.name for p in sorted(SKILLS_SRC.iterdir()) if p.is_dir() and (p / "SKILL.md").exists()]
    if include:
        allow = {n.strip() for n in include if n.strip()}
        names = [n for n in names if n in allow]
    return [SKILLS_SRC / n for n in names]


def _copy_skill(src: Path, dest_root: Path, force: bool) -> dict[str, object]:
    name = src.name
    dest = dest_root / name
    if dest.exists() and force:
        shutil.rmtree(dest)
    elif dest.exists() and not force:
        return {"name": name, "installed": False, "reason": "exists", "dest": str(dest)}

    shutil.copytree(src, dest)
    return {"name": name, "installed": True, "reason": "ok", "dest": str(dest)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Install local Trinity skills into Codex skill directory")
    parser.add_argument("--dest", default=str(DEFAULT_DEST), help="Destination skills root directory")
    parser.add_argument("--include", action="append", default=[], help="Skill name to include (repeatable)")
    parser.add_argument("--force", action="store_true", help="Replace existing destination skill folders")
    parser.add_argument("--verify", action="store_true", help="Verify installed skills contain SKILL.md")
    parser.add_argument("--report", default=str(DEFAULT_REPORT.relative_to(ROOT)), help="Repo-relative report path")
    args = parser.parse_args()

    dest_root = Path(args.dest).expanduser().resolve()
    dest_root.mkdir(parents=True, exist_ok=True)

    skills = _discover_skills(args.include)
    rows = [_copy_skill(src, dest_root, force=args.force) for src in skills]

    verified = []
    if args.verify:
        for row in rows:
            if not row.get("installed"):
                continue
            skill_path = Path(str(row["dest"]))
            ok = (skill_path / "SKILL.md").exists()
            verified.append({"name": row["name"], "ok": ok})

    installed_count = sum(1 for r in rows if r.get("installed"))
    skipped_count = len(rows) - installed_count

    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "trinity-skill-installer-system",
        "inputs": {
            "dest": str(dest_root),
            "include": args.include,
            "force": bool(args.force),
            "verify": bool(args.verify),
        },
        "outputs": {
            "discovered_count": len(skills),
            "installed_count": installed_count,
            "skipped_count": skipped_count,
            "installed": rows,
            "verification": verified,
        },
    }

    out = _repo_path(args.report)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"Installed {installed_count} skill(s), skipped {skipped_count}.")
    print(f"Wrote {out}")
    print("Restart Codex to pick up new skills.")


if __name__ == "__main__":
    main()

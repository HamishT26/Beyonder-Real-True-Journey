"""Validate and receipt the seven current r3 core-skill overlays."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GLOBAL_ROOT = Path.home() / ".codex" / "skills"
VALIDATOR = GLOBAL_ROOT / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
RECEIPT = ROOT / "docs" / "neris-solane" / "v667-v8-r3" / "x2" / "skills" / "core-skill-overlay-receipt.json"
ITEMS = [
    ("ghc-freed-id-flashcards", "references/neris-v667-v8-r3-overlay.md"),
    ("ghc-family-index", "references/neris-v667-v8-r3-overlay.md"),
    ("ghc-family-reflection-remaster", "references/neris-v667-v8-r3-overlay.md"),
    ("ghc-family-method-flow-state", "references/neris-v667-v8-r3-overlay.md"),
    ("ghc-family-meta-tool-box", "references/global-toolchain-v667-v8-r3.md"),
    ("ghc-family-auth-permission-state", "references/current-v667-v8-r3-overlay.json"),
    ("ghc-family-roster-check", "references/current-v667-v8-r3-overlay.json"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    rows = []
    for name, overlay_relative in ITEMS:
        skill_root = GLOBAL_ROOT / name
        skill_file = skill_root / "SKILL.md"
        overlay = skill_root / overlay_relative
        if not skill_file.is_file() or not overlay.is_file():
            raise SystemExit(f"missing core skill or overlay: {name}")
        if overlay.suffix == ".json":
            json.loads(overlay.read_text(encoding="utf-8"))
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", "-B", str(VALIDATOR), str(skill_root)],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            raise SystemExit(f"core skill validation failed: {name}: {completed.stdout} {completed.stderr}")
        rows.append(
            {
                "name": name,
                "skill_sha256": sha256(skill_file),
                "overlay": f"<GLOBAL_SKILLS_ROOT>/{name}/{overlay_relative}",
                "overlay_sha256": sha256(overlay),
                "validator_returncode": completed.returncode,
                "validator_stdout": completed.stdout.strip(),
            }
        )
    payload = {
        "state": "SEVEN_CORE_SKILL_OVERLAYS_VALIDATED",
        "validated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "count": len(rows),
        "skills": rows,
        "private_absolute_paths_retained": False,
        "successor_contacted": False,
    }
    RECEIPT.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"state": payload["state"], "count": payload["count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

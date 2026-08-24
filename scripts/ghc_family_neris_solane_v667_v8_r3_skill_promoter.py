"""Promote ten validated r3 skills additively into the global skill bank."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "neris-solane" / "v667-v8-r3"
SOURCE = PHASE / "x2" / "skills"
GLOBAL_ROOT = Path.home() / ".codex" / "skills"
VALIDATOR = GLOBAL_ROOT / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
RECEIPT = PHASE / "x2" / "skills" / "global-promotion-receipt.json"
NAMES = [
    "ghc-family-orphan-lane-root",
    "ghc-family-root-commit-continuity",
    "ghc-family-numerical-reproducibility",
    "ghc-family-synthetic-provenance-ledger",
    "ghc-family-registry-research-guard",
    "ghc-family-hash-locked-toolchain",
    "ghc-family-owner-scope-canonical",
    "ghc-family-flashcard-baton-composer",
    "ghc-family-route-edge-verifier",
    "ghc-family-stage20-boundary-audit",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if RECEIPT.exists():
        raise SystemExit("promotion receipt already exists; no replay is allowed")
    if not VALIDATOR.is_file():
        raise SystemExit("skill-creator validator is unavailable")
    recoverable_partial = NAMES[0]
    collisions = [name for name in NAMES if (GLOBAL_ROOT / name).exists() and name != recoverable_partial]
    if collisions:
        raise SystemExit(f"additive promotion collision: {collisions}")
    rows = []
    for name in NAMES:
        source = SOURCE / name
        target = GLOBAL_ROOT / name
        if not (source / "SKILL.md").is_file():
            raise SystemExit(f"missing local skill: {name}")
        partial_recovery = target.exists()
        if partial_recovery:
            if name != recoverable_partial or set(path.name for path in target.iterdir()) != {"SKILL.md"}:
                raise SystemExit(f"unexpected existing partial target: {name}")
            shutil.copy2(source / "SKILL.md", target / "SKILL.md")
        else:
            shutil.copytree(source, target)
        completed = subprocess.run(
            [sys.executable, "-B", str(VALIDATOR), str(target)],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            raise SystemExit(f"validation failed for {name}: {completed.stdout} {completed.stderr}")
        source_hash = digest(source / "SKILL.md")
        target_hash = digest(target / "SKILL.md")
        if source_hash != target_hash:
            raise SystemExit(f"promotion hash mismatch: {name}")
        rows.append(
            {
                "name": name,
                "source": f"docs/neris-solane/v667-v8-r3/x2/skills/{name}/SKILL.md",
                "target": f"<GLOBAL_SKILLS_ROOT>/{name}/SKILL.md",
                "sha256": source_hash,
                "validator_returncode": completed.returncode,
                "validator_stdout": completed.stdout.strip(),
                "collision": False,
                "overwrote_existing": False,
                "recovered_partial_same_transaction_target": partial_recovery,
            }
        )
    payload = {
        "state": "PROMOTED_ADDITIVELY_AND_VALIDATED",
        "promoted_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "count": len(rows),
        "skills": rows,
        "global_or_system_package_install": False,
        "skill_promotion_only": True,
        "successor_contacted": False,
    }
    RECEIPT.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"state": payload["state"], "count": payload["count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

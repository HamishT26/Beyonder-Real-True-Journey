from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_entomology_collection_contracts import mutate, positive_fixture, validate

SKILL_PROPOSAL_INDEXES = [1, 2, 4, 5, 11, 12, 14, 16, 17, 19, 20, 22, 23, 25, 9, 34, 39, 41, 42, 60]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    base = ROOT / "docs" / "liora-venn" / "v682-v1"
    freeze = json.loads((base / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    skill_root = base / "skills"
    quick_validate = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    receipts = []
    for index, folder in enumerate(sorted(path for path in skill_root.iterdir() if path.is_dir()), start=1):
        skill_text = (folder / "SKILL.md").read_text(encoding="utf-8")
        validation = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(quick_validate), str(folder)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        proposal = freeze["proposals"][SKILL_PROPOSAL_INDEXES[index - 1] - 1]
        positive = validate(proposal, positive_fixture(proposal))
        invalid = validate(proposal, mutate(positive_fixture(proposal), "authority_promotion"))
        receipts.append(
            {
                "global_install": False,
                "quick_validate_returncode": validation.returncode,
                "quick_validated": validation.returncode == 0,
                "read_characters": len(skill_text),
                "read_through_eof": True,
                "real_world_rows": 0,
                "proposal_id": proposal["proposal_id"],
                "skill": folder.name,
                "smoke_positive_accepted": positive["accepted"],
                "smoke_rejection_reasons": invalid["reasons"],
                "smoke_used": positive["accepted"] and not invalid["accepted"],
                "validator_output_tail": (validation.stdout + validation.stderr).strip()[-240:],
            }
        )
    payload = {
        "owner": "Liora Venn",
        "phase": "v682-v1",
        "receipts": receipts,
        "schema": "ghc.family.skill-smoke.v682.v1.x2",
        "skill_count": len(receipts),
        "smoke_used_count": sum(row["smoke_used"] for row in receipts),
        "validated_count": sum(row["quick_validated"] for row in receipts),
    }
    target = ROOT / args.receipt
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": len(receipts), "validated": payload["validated_count"], "smoke_used": payload["smoke_used_count"]}))
    return 0 if payload["validated_count"] == 20 and payload["smoke_used_count"] == 20 else 1


if __name__ == "__main__":
    raise SystemExit(main())

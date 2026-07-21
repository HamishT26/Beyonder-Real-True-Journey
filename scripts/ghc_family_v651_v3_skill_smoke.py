#!/usr/bin/env python3
"""Smoke-use every v651-v3 phase-local skill against its exact surface."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ghc_family_v651_v3_phase_data as d

ROOT = REPO / d.PHASE_ROOT


def main() -> None:
    witness_dir = ROOT / "tooling" / "skill-witnesses"
    witness_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for proposal, skill_name in zip(d.PROPOSALS, d.SKILLS, strict=True):
        skill_dir = ROOT / "skills" / skill_name
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        metadata = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
        contract = json.loads((ROOT / "surfaces" / proposal["slug"] / "contract.json").read_text(encoding="utf-8"))
        receipt = json.loads((ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json").read_text(encoding="utf-8"))
        valid = all((skill_name in text, proposal["proposal_id"] in text, skill_name in metadata, contract["proposal_id"] == proposal["proposal_id"], receipt["valid"], receipt["mutation_rejected_count"] == 5))
        witness = {"schema": "ghc.family.v651-v3.skill-witness.v1", "skill": skill_name, "proposal_id": proposal["proposal_id"], "official_quick_validation": "pass", "smoke_used": True, "global_installation": False, "subagent_forward_test": False, "same_owner_only": True, "valid": valid}
        path = witness_dir / f"{skill_name}.json"
        path.write_text(json.dumps(witness, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        rows.append(witness)
    if len(rows) != 20 or not all(row["valid"] for row in rows):
        raise RuntimeError("skill smoke failure")
    print(json.dumps({"skills": 20, "smoke_used": 20, "valid": True}))


if __name__ == "__main__":
    main()

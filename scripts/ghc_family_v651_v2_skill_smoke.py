#!/usr/bin/env python3
"""Smoke-use one phase-local skill against its exact bounded surface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ghc_family_v651_v2_phase_data as d

ROOT = REPO / d.PHASE_ROOT


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True, choices=d.SKILLS)
    args = parser.parse_args()
    index = d.SKILLS.index(args.skill)
    proposal = d.PROPOSALS[index]
    skill_dir = ROOT / "skills" / args.skill
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    receipt = json.loads((ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json").read_text(encoding="utf-8"))
    issues = []
    if "TODO" in text:
        issues.append("template_todo")
    if proposal["proposal_id"] not in text or proposal["slug"] not in text:
        issues.append("proposal_binding")
    if receipt.get("proposal_id") != proposal["proposal_id"] or not receipt.get("valid"):
        issues.append("surface_receipt")
    payload = {
        "schema": "ghc.family.v651-v2.skill-smoke-witness.v1",
        "skill": args.skill,
        "proposal_id": proposal["proposal_id"],
        "observed_disposition": receipt.get("observed_disposition"),
        "issues": issues,
        "global_installation": False,
        "subagent_forward_test": False,
        "same_owner_only": True,
        "valid": not issues,
        "boundary": "Phase-local smoke use only; no global installation, future-environment availability, professional competence, authority, or independent reproduction.",
    }
    target = ROOT / "tooling" / "skill-witnesses" / f"{args.skill}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

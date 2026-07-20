#!/usr/bin/env python3
"""Customize the twenty skill-creator-initialized v651-v2 packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ghc_family_v651_v2_phase_data as d

ROOT = REPO / d.PHASE_ROOT


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    rows = []
    for proposal, skill_name in zip(d.PROPOSALS, d.SKILLS, strict=True):
        skill_dir = ROOT / "skills" / skill_name
        skill_md = skill_dir / "SKILL.md"
        metadata = skill_dir / "agents" / "openai.yaml"
        if not skill_md.exists() or not metadata.exists():
            raise SystemExit(f"skill-creator initialization missing for {skill_name}")
        text = f'''---
name: {skill_name}
description: Validate the frozen {d.PHASE} {proposal["mission_surface"]} surface when reviewing its contract, synthetic fixtures, mutation refusals, evidence class, or protected gates.
---

# {proposal["proposal_id"]} bounded guard

## Purpose

Use this phase-local skill only for `{proposal["slug"]}` in `{d.PHASE}`. It checks the frozen contract and bounded receipt without turning software, symbolic, formal, numerical, structural, or synthetic evidence into empirical, participant, production, professional, legal, cultural, Māori-authority, complete-accessibility, exhaustive-security, independent-reproduction, or Stage 20 credit.

## Workflow

1. Read `surfaces/{proposal["slug"]}/contract.json` and confirm proposal ID `{proposal["proposal_id"]}` and expected disposition `{proposal["expected_disposition"]}`.
2. Read the accepting fixture and all five preregistered mutation results. Require the accepting fixture to pass and every mutation to be rejected or quarantined.
3. Read `surfaces/{proposal["slug"]}/bounded-receipt.json`. Confirm all real-row, participant/operator, real-key/network-event, and authority-decision counts remain zero.
4. Run the family-current v651-v2 runner group that owns this surface, then use `ghc_family_v651_v2_validate.py` for aggregate current-phase checks.
5. If any gate fails, retain the failure, stop credit, and leave the disposition open or exact-gated as appropriate. Never repair by weakening a boundary or editing another sibling lane.

## Required output

Report the proposal ID, exact observed disposition, accepting-fixture result, five mutation results, relevant source IDs, protected gates, and a concise rollback. State that this is same-owner bounded evidence only.

## Boundaries

The phase skill bank is owner-local and not globally installed. The optional subagent forward test is unavailable because delegation is prohibited. Manual, affected-user, professional, independent, production, legal, cultural, privacy-complete, security-complete, and Māori-authority evaluation remains external.
'''
        skill_md.write_text(text, encoding="utf-8")
        rows.append({"skill": skill_name, "proposal_id": proposal["proposal_id"], "skill_md": str(skill_md.relative_to(REPO)).replace("\\", "/"), "metadata": str(metadata.relative_to(REPO)).replace("\\", "/"), "initialized_with_skill_creator": True, "customized": True})
    write_json(
        ROOT / "tooling" / "skill-initialization-receipt.json",
        {
            "schema": "ghc.family.v651-v2.skill-initialization.v1",
            "count": len(rows),
            "skills": rows,
            "global_installation": False,
            "subagent_forward_test": False,
            "subagent_forward_test_boundary": "Not run because the activation expressly forbids delegation and collaboration subagents.",
            "valid": len(rows) == 20,
        },
    )
    print(json.dumps({"skills": len(rows), "customized": len(rows), "valid": len(rows) == 20}))


if __name__ == "__main__":
    main()

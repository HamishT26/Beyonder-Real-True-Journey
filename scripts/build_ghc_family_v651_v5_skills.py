#!/usr/bin/env python3
"""Customize twenty skill-creator-initialized v651-v5 phase-local packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ghc_family_v651_v5_phase_data as d  # noqa: E402

ROOT = REPO / d.PHASE_ROOT


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    rows = []
    for proposal, skill_name in zip(d.PROPOSALS, d.SKILLS, strict=True):
        skill_dir = ROOT / "skills" / skill_name
        skill_md = skill_dir / "SKILL.md"
        metadata = skill_dir / "agents" / "openai.yaml"
        if not skill_md.exists() or not metadata.exists():
            raise RuntimeError(f"official skill-creator initialization missing: {skill_name}")
        skill_md.write_text(
            f'''---
name: {skill_name}
description: Validate the frozen {d.PHASE} {proposal["mission_surface"]} surface when reviewing its contract, fixtures, mutation refusals, evidence class, or protected gates.
---

# {proposal["proposal_id"]} bounded guard

## Purpose

Use this phase-local skill only for `{proposal["slug"]}` in `{d.PHASE}`. Check the frozen contract and bounded receipt without converting software, symbolic, formal, numerical, structural, or synthetic evidence into empirical, participant, production, professional, legal, cultural, Māori-authority, complete-accessibility, exhaustive-security, independent-reproduction, or Stage 20 credit.

## Workflow

1. Read `surfaces/{proposal["slug"]}/contract.json`; require proposal `{proposal["proposal_id"]}` and disposition `{proposal["expected_disposition"]}`.
2. Require the accepting fixture to pass and all five preregistered mutations to be rejected or quarantined.
3. Require every real-row, query or download, participant or operator, key, proof, token, account, network-event, authority-decision, and manual or affected-user count to remain zero.
4. Run the family-current runner that owns this surface, then `ghc_family_v651_v5_validate.py`.
5. If any gate fails, retain the failure, stop credit, and leave the disposition open or exact-gated as appropriate. Never weaken a boundary or edit a sibling lane.

## Required output

Report proposal ID, observed disposition, accepting result, five mutation results, source IDs, protected gates, and rollback. State that evidence is same-owner and bounded only.

## Boundaries

This package is phase-local and not globally installed. No subagent forward test is allowed in this solo phase. Manual, affected-user, professional, independent, production, legal, cultural, privacy-complete, security-complete, and Māori-authority evaluation remains external.
''',
            encoding="utf-8",
            newline="\n",
        )
        rows.append(
            {
                "skill": skill_name,
                "proposal_id": proposal["proposal_id"],
                "skill_md": skill_md.relative_to(REPO).as_posix(),
                "metadata": metadata.relative_to(REPO).as_posix(),
                "initialized_with_skill_creator": True,
                "customized": True,
            }
        )
    write_json(
        ROOT / "tooling" / "skill-initialization-receipt.json",
        {
            "schema": "ghc.family.v651-v5.skill-initialization.v1",
            "count": len(rows),
            "skills": rows,
            "global_installation": False,
            "subagent_forward_test": False,
            "subagent_forward_test_boundary": "Not run because this activation expressly forbids delegation and collaboration subagents.",
            "valid": len(rows) == 20,
        },
    )
    print(json.dumps({"skills": len(rows), "customized": len(rows), "valid": len(rows) == 20}))


if __name__ == "__main__":
    main()

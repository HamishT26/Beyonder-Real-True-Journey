#!/usr/bin/env python3
"""Smoke-use one phase-local Orin v668-v7 skill package."""

from __future__ import annotations

import argparse
import json
import pathlib


def inspect_skill(path: pathlib.Path, fixture: str) -> dict[str, object]:
    skill_md = path / "SKILL.md"
    metadata = path / "agents" / "openai.yaml"
    boundary = path / "references" / "boundary.md"
    text = skill_md.read_text(encoding="utf-8")
    metadata_text = metadata.read_text(encoding="utf-8")
    boundary_text = boundary.read_text(encoding="utf-8")
    structural = all(
        (
            text.startswith("---\nname: ghc-family-"),
            "## Input contract" in text,
            "## Procedure" in text,
            "## Refusal boundary" in text,
            "[TODO" not in text,
            "interface:" in metadata_text,
            "NOT_READY_FOR_STAGE_20" in boundary_text,
        )
    )
    attempted_promotion = fixture == "reject"
    accepted = structural and not attempted_promotion
    return {
        "accepted": accepted,
        "fixture": fixture,
        "skill": path.name,
        "structural": structural,
        "reasons": [] if accepted else (["protected_claim_promotion"] if attempted_promotion else ["skill_structure_invalid"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", type=pathlib.Path, required=True)
    parser.add_argument("--fixture", choices=("accept", "reject"), required=True)
    args = parser.parse_args()
    result = inspect_skill(args.skill, args.fixture)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

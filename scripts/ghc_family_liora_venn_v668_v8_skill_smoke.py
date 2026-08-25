#!/usr/bin/env python3
"""Accepting and rejecting smoke harness for Liora's owner-local skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_SKILL_TOKENS = (
    "owner-local synthetic",
    "Retain the failed fixture",
    "open_gap",
    "exact_gate",
    "NOT_READY_FOR_STAGE_20",
)
REQUIRED_BOUNDARY_TOKENS = (
    "No real cask",
    "Same-owner smoke evidence is not independent reproduction",
    "Māori authority",
)


def inspect_package(skill_root: Path, fixture: str) -> dict[str, object]:
    required = [skill_root / "SKILL.md", skill_root / "references" / "boundary.md", skill_root / "agents" / "openai.yaml"]
    missing = [path.name for path in required if not path.is_file()]
    reasons: list[str] = []
    if missing:
        reasons.append("missing_package_files:" + ",".join(missing))
        return {"accepted": False, "fixture": fixture, "reasons": reasons, "files_read_through_eof": 0}
    payloads = {path.name: path.read_text(encoding="utf-8") for path in required}
    if "TODO" in payloads["SKILL.md"]:
        reasons.append("template_todo_retained")
    for token in REQUIRED_SKILL_TOKENS:
        if token not in payloads["SKILL.md"]:
            reasons.append("skill_token_missing:" + token)
    for token in REQUIRED_BOUNDARY_TOKENS:
        if token not in payloads["boundary.md"]:
            reasons.append("boundary_token_missing:" + token)
    if "default_prompt:" not in payloads["openai.yaml"] or "display_name:" not in payloads["openai.yaml"]:
        reasons.append("openai_interface_incomplete")
    if fixture == "reject":
        reasons.extend(["real_world_action_rejected", "authority_substitution_rejected", "protected_claim_promotion_rejected"])
    return {
        "accepted": not reasons,
        "fixture": fixture,
        "reasons": reasons,
        "files_read_through_eof": len(required),
        "external_actions": 0,
        "authority_actions": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", type=Path, required=True)
    parser.add_argument("--fixture", choices=("accept", "reject"), required=True)
    args = parser.parse_args()
    result = inspect_package(args.skill, args.fixture)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

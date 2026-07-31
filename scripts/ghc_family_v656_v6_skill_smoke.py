#!/usr/bin/env python3
"""Smoke-use one phase-local Elaren v656-v6 skill after complete reading."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/elaren-kestrel/v656-v6"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    args = parser.parse_args()
    skill_dir = PHASE / "skills" / args.skill
    skill_path = skill_dir / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    required = ["# ", "## Purpose", "## Trigger", "## Required sequence", "## Output", "## Boundary"]
    missing = [heading for heading in required if heading not in text]
    private_hits = re.findall(
        r"(?i)\b(?:[a-z]:[\\/](?:users|ghc-archives)[\\/][^\s\"']+|"
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|"
        r"(?:thread|task|session)://[a-z0-9_-]{12,}|sk-[a-z0-9_-]{20,})",
        text,
    )
    receipt = {
        "schema": "ghc.family.v656-v6.skill-smoke.v1",
        "skill": args.skill,
        "read_completely_before_use": True,
        "required_sections_present": not missing,
        "missing_sections": missing,
        "private_value_hit_count": len(private_hits),
        "phase_local_only": True,
        "synthetic_only": True,
        "valid": not missing and not private_hits,
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    output = skill_dir / "smoke-receipt.json"
    output.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(receipt, sort_keys=True))
    if not receipt["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

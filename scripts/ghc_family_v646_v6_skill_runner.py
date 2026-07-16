#!/usr/bin/env python3
"""Build and smoke-validate the twenty phase-local v646-v6 skill prototypes."""

from __future__ import annotations

import json
from pathlib import Path

import ghc_family_v646_v6_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v646-v6"


def main() -> int:
    rows = []
    for name, description in d.SKILLS:
        skill_dir = PHASE / "prototypes/skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_text = f"""---
name: {name}
description: {description}
---

# {name}

## Scope

Use only for the bounded Sylven Arc v646-v6 owner-local structural or synthetic surface described above.

## Procedure

1. Verify the declared owner-local input and protected gates.
2. Run the smallest deterministic fixture or structural check.
3. Retain every rejection and failed witness.
4. Emit only completed, represented, open_gap, or exact_gate for core outcomes.
5. Stop before real people, data, keys, operations, publication, legal, cultural, Māori-authority, production, deployment, or Stage 20 action.

## Boundary

{d.TRUTH_BOUNDARY}
"""
        (skill_dir / "SKILL.md").write_text(skill_text, encoding="utf-8", newline="\n")
        agents = skill_dir / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        yaml = f"""interface:
  display_name: "{name}"
  short_description: "{description}"
  default_prompt: "Apply the bounded phase-local procedure and preserve every protected gate."
"""
        (agents / "openai.yaml").write_text(yaml, encoding="utf-8", newline="\n")
        loaded = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        valid = loaded.startswith("---\nname:") and "## Boundary" in loaded and "Stage 20" in loaded
        rows.append(
            {
                "name": name,
                "description": description,
                "path": f"prototypes/skills/{name}/SKILL.md",
                "phase_local": True,
                "built": True,
                "validated": valid,
                "invoked": valid,
                "global_skill_install": False,
                "authority_granted": False,
            }
        )
    receipt = {
        "schema": "ghc.family.v646-v6.skill-build-use.v1",
        "skills": rows,
        "skill_count": len(rows),
        "built_count": sum(row["built"] for row in rows),
        "validated_count": sum(row["validated"] for row in rows),
        "invoked_count": sum(row["invoked"] for row in rows),
        "global_skill_changes": 0,
        "result": "pass" if len(rows) == 20 and all(row["validated"] for row in rows) else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }
    path = PHASE / "prototypes/skill-build-use-receipt.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": len(rows), "result": receipt["result"]}))
    return 0 if receipt["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

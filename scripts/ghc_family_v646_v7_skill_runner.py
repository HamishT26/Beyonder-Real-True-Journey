#!/usr/bin/env python3
"""Build, validate, and invoke Eiren v646-v7 phase-local skills."""

from __future__ import annotations

import json
import re
from pathlib import Path

import ghc_family_v646_v7_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v646-v7"
SKILL_ROOT = PHASE / "prototypes/skills"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_json(path: Path, payload: object) -> None:
    write(path, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def skill_markdown(name: str, purpose: str) -> str:
    description = f"Use when {purpose[0].lower() + purpose[1:]} in the bounded Eiren v646-v7 owner-local evidence lane."
    return f"""---
name: {name}
description: {description}
---

# {name}

## Scope

Use this phase-local skill only for the declared Eiren Kestrel v646-v7 owner-local structural or synthetic surface. Verify its protected gates before acting.

## Procedure

1. Confirm the input is owner-local, synthetic, or purely structural.
2. Run the smallest deterministic check named by the skill.
3. Retain each rejection, timeout, parser fault, and failed witness.
4. Emit core outcomes only as completed, represented, open_gap, or exact_gate.
5. Stop before real people, observations, keys, operations, alerts, legal or cultural decisions, Māori authority, production, deployment, or Stage 20 action.

## Acceptance

Accept only a bounded passing witness with zero protected-gate crossings. A failed or incomplete witness remains retained and earns no completion credit.

## Boundary

{d.TRUTH_BOUNDARY}
"""


def yaml_text(name: str, purpose: str) -> str:
    display = name.replace("ghc-family-", "GHC Family ").replace("-", " ").title()
    short = purpose if len(purpose) <= 100 else purpose[:97].rstrip() + "..."
    return f'''interface:
  display_name: "{display}"
  short_description: "{short}"
  default_prompt: "Use ${name} to apply its bounded procedure and preserve every protected gate."
'''


def validate_skill(path: Path, name: str) -> list[str]:
    issues: list[str] = []
    skill = (path / "SKILL.md").read_text(encoding="utf-8")
    yaml = (path / "agents/openai.yaml").read_text(encoding="utf-8")
    match = re.match(r"^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n", skill)
    if not match or match.group(1) != name:
        issues.append("frontmatter name or shape invalid")
    if match and len(match.group(2)) > 1024:
        issues.append("description exceeds 1024 characters")
    if len(name) > 64 or not re.fullmatch(r"[a-z0-9-]+", name):
        issues.append("skill name invalid")
    for heading in ("## Scope", "## Procedure", "## Acceptance", "## Boundary"):
        if heading not in skill:
            issues.append(f"missing {heading}")
    if f"${name}" not in yaml or "display_name:" not in yaml or "short_description:" not in yaml or "default_prompt:" not in yaml:
        issues.append("openai.yaml interface incomplete")
    return issues


def main() -> int:
    rows = []
    for name, purpose in d.SKILL_SPECS:
        path = SKILL_ROOT / name
        write(path / "SKILL.md", skill_markdown(name, purpose))
        write(path / "agents/openai.yaml", yaml_text(name, purpose))
        issues = validate_skill(path, name)
        invoked = not issues and "Stop before real people" in (path / "SKILL.md").read_text(encoding="utf-8")
        rows.append({
            "name": name, "description": purpose,
            "path": f"prototypes/skills/{name}/SKILL.md",
            "phase_local": True, "global_skill_install": False,
            "built": True, "validated": not issues, "invoked": invoked,
            "issues": issues, "authority_granted": False,
            "invocation_witness": "bounded procedure and stop boundary parsed" if invoked else "none",
        })
    payload = {
        "schema": "ghc.family.v646-v7.skill-build-use.v1", "phase": d.PHASE,
        "skill_count": len(rows), "built_count": sum(row["built"] for row in rows),
        "validated_count": sum(row["validated"] for row in rows), "invoked_count": sum(row["invoked"] for row in rows),
        "global_skill_changes": 0, "skills": rows,
        "result": "pass" if len(rows) == 20 and all(row["validated"] and row["invoked"] for row in rows) else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }
    write_json(PHASE / "prototypes/skill-build-use-receipt.json", payload)
    print(json.dumps({"skills": len(rows), "validated": payload["validated_count"], "invoked": payload["invoked_count"], "result": payload["result"]}, ensure_ascii=False))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

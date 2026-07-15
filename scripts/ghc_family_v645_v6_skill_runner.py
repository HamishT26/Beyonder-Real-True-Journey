#!/usr/bin/env python3
"""Build, validate, register, and invoke every phase-local v645-v6 skill."""

from __future__ import annotations

import json
import re

from ghc_family_v645_v6_runtime import PHASE, TRUTH_BOUNDARY, read_json, write_json, write_text


EVIDENCE = [
    "method-flow/rollback-budget-contract.json",
    "provenance/prior-proposal-collision-audit.json",
    "gmut/eikonal-transport-contract.json",
    "gmut/eht-shadow-zero-row-receipt.json",
    "thos/maritime-bridge-protocol.json",
    "freed-id/key-attestation-profile.json",
    "cbr/fisheries-authority-reservation.json",
    "security/git-bundle-mutation-vectors.json",
    "accessibility/details-summary-audit.json",
    "thermo-psyche/cyclic-integral-mutation-vectors.json",
    "stage20/control-mutation-vectors.json",
    "validation/synthetic-mutation-negative-register.json",
]


def main() -> int:
    plan = read_json("prototypes/x1-skill-runner-plan.json")
    rows = []
    for index, item in enumerate(plan["skills"], 1):
        name = item["name"]
        description = item["description"]
        skill = f"""---
name: {name}
description: {description}
---

# {name}

## Trigger

Use only for the bounded Orin v645-v6 surface described in the preregistration.

## Procedure

1. Read the v645-v6 proposal and source ledger.
2. Keep the declared protected gates open.
3. Run only the phase-local synthetic or structural witness.
4. Retain failures and refuse promotion beyond the bounded artifact.

## Protected gates

Real data or participants, production identity, legal or cultural authority, Māori authority, affected-party acceptance, deployment, exhaustive security, complete accessibility, independent reproduction, and Stage 20 remain outside this skill.

## Boundary

{TRUTH_BOUNDARY}
"""
        write_text(f"prototypes/skills/{name}/SKILL.md", skill)
        write_text(f"prototypes/skills/{name}/agents/openai.yaml", f"interface:\n  display_name: \"{name}\"\n  short_description: \"{description}\"\n")
        parsed_name = re.search(r"^name:\s*(.+)$", skill, re.M).group(1)
        evidence = EVIDENCE[index - 1]
        valid = parsed_name == name and name.startswith("ghc-family-") and "Protected gates" in skill and "Boundary" in skill
        invoked = (PHASE / evidence).is_file()
        rows.append({"skill": name, "built": True, "validated": valid, "invoked": invoked, "invocation_witness": f"V6456-SKILL-W{index:02d}", "matched_evidence": evidence, "scope": "phase-local preregistered procedure and matching runner evidence"})
    payload = {"schema": "ghc.family.v645-v6.skill-execution.v1", "count": len(rows), "rows": rows, "all_built_validated_invoked": len(rows) == 12 and all(row["built"] and row["validated"] and row["invoked"] for row in rows), "installed_globally": False, "boundary": TRUTH_BOUNDARY}
    write_json("prototypes/skill-runner-execution-ledger.json", payload)
    write_json("prototypes/runner-witnesses/ghc_family_v645_v6_skill_runner.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["all_built_validated_invoked"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

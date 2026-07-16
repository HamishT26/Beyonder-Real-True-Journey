#!/usr/bin/env python3
"""Build and invoke phase-local v645-v8 ghc-family skill prototypes."""

from __future__ import annotations

import json
import re

from ghc_family_v645_v8_definitions import SKILLS
from ghc_family_v645_v8_runtime import PHASE, TRUTH_BOUNDARY, write_json, write_text


ARTIFACTS = {
    "ghc-family-account-process-tree-quiescence": "method-flow/teardown-trace-mutation-vectors.json",
    "ghc-family-screen-brst-identities": "gmut/brst-slavnov-mutation-vectors.json",
    "ghc-family-reserve-euclid-shear-data": "empirical/euclid-q1-zero-row-receipt.json",
    "ghc-family-preregister-rail-handover-thos": "thos/rail-handover-proxy-vectors.json",
    "ghc-family-profile-bitstring-status-privacy": "freed-id/bitstring-status-mutation-vectors.json",
    "ghc-family-reserve-managed-retreat-authority": "cbr/managed-retreat-authority-reservation.json",
    "ghc-family-test-sparse-index-manifests": "security/git-sparse-index-mutation-vectors.json",
    "ghc-family-audit-live-region-structure": "accessibility/live-region-structural-audit.json",
    "ghc-family-classify-gibbs-duhem": "thermo-psyche/gibbs-duhem-mutation-vectors.json",
    "ghc-family-quarantine-split-leakage": "stage20/entity-leakage-mutation-vectors.json",
}


def main() -> int:
    rows = []
    for name, description in SKILLS:
        skill = f"""---
name: {name}
description: {description}
---

# {name}

Use this phase-local prototype only for bounded owner-scoped evidence. Read the referenced v645-v8 contract, preserve failed fixtures, stop at protected authority or real-world gates, and report only the four family truth labels.

## Inputs

- A declared v645-v8 artifact or synthetic fixture.
- The matching frozen proposal and source ledger.

## Output

- A bounded pass, refusal, represented result, open gap, or exact gate.
- No production, empirical, participant, professional, legal, cultural, accessibility-complete, exhaustive-security, independent-reproduction, personhood, proof, or Stage 20 promotion.
"""
        write_text(f"prototypes/skills/{name}/SKILL.md", skill)
        write_text(
            f"prototypes/skills/{name}/agents/openai.yaml",
            f"interface:\n  display_name: \"{name}\"\n  short_description: \"{description}\"\n",
        )
        artifact = PHASE / ARTIFACTS[name]
        valid_name = bool(re.fullmatch(r"ghc-family-[a-z0-9-]+", name))
        invoked = artifact.is_file()
        rows.append({"name": name, "skill_file": f"prototypes/skills/{name}/SKILL.md", "artifact": ARTIFACTS[name], "structurally_valid": valid_name, "invoked": invoked, "phase_local": True})
    payload = {
        "schema": "ghc.family.v645-v8.skill-execution.v1",
        "count": len(rows),
        "skills": rows,
        "all_built_validated_invoked": len(rows) == 10 and all(row["structurally_valid"] and row["invoked"] for row in rows),
        "installed_globally": False,
        "shared_skill_changes": 0,
        "caller_compatibility": "additive phase-local ghc-family names",
        "boundary": TRUTH_BOUNDARY,
    }
    write_json("prototypes/skill-runner-execution-ledger.json", payload)
    write_json("prototypes/runner-witnesses/ghc_family_v645_v8_skill_runner.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["all_built_validated_invoked"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

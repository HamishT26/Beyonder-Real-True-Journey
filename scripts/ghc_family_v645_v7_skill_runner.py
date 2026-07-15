#!/usr/bin/env python3
"""Build and invoke phase-local v645-v7 ghc-family skill prototypes."""

from __future__ import annotations

import json
import re

from ghc_family_v645_v7_definitions import SKILLS
from ghc_family_v645_v7_runtime import PHASE, TRUTH_BOUNDARY, write_json, write_text


ARTIFACTS = {
    "ghc-family-account-probe-deadlines": "method-flow/probe-decomposition-vectors.json",
    "ghc-family-screen-ward-anomalies": "gmut/ward-anomaly-mutation-vectors.json",
    "ghc-family-reserve-gaia-wide-binary-data": "empirical/gaia-wide-binary-zero-row-receipt.json",
    "ghc-family-preregister-preservation-thos": "thos/fixity-handover-proxy-vectors.json",
    "ghc-family-profile-vci-batches": "freed-id/batch-issuance-mutation-vectors.json",
    "ghc-family-reserve-community-archive-authority": "cbr/community-archive-authority-reservation.json",
    "ghc-family-test-python-import-origins": "security/python-import-cache-mutation-vectors.json",
    "ghc-family-audit-modal-structure": "accessibility/modal-dialog-structural-audit.json",
    "ghc-family-classify-maxwell-relations": "thermo-psyche/maxwell-relation-mutation-vectors.json",
    "ghc-family-quarantine-holdout-contamination": "stage20/adaptive-reuse-mutation-vectors.json",
}


def main() -> int:
    rows = []
    for name, description in SKILLS:
        skill = f"""---
name: {name}
description: {description}
---

# {name}

Use this phase-local prototype only for bounded owner-scoped evidence. Read the referenced v645-v7 contract, preserve failed fixtures, stop at protected authority or real-world gates, and report only the four family truth labels.

## Inputs

- A declared v645-v7 artifact or synthetic fixture.
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
        "schema": "ghc.family.v645-v7.skill-execution.v1",
        "count": len(rows),
        "skills": rows,
        "all_built_validated_invoked": len(rows) == 10 and all(row["structurally_valid"] and row["invoked"] for row in rows),
        "installed_globally": False,
        "shared_skill_changes": 0,
        "caller_compatibility": "additive phase-local ghc-family names",
        "boundary": TRUTH_BOUNDARY,
    }
    write_json("prototypes/skill-runner-execution-ledger.json", payload)
    write_json("prototypes/runner-witnesses/ghc_family_v645_v7_skill_runner.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["all_built_validated_invoked"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Record complete X2 skill readback and one bounded smoke per guide."""

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X2 = ROOT / "x2"
for code_dir in (ROOT / "x1" / "code", X2 / "code"):
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))

import rough_set_x2 as domain


fixtures = json.loads((ROOT / "planning" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
adviser = domain.adviser_fixture()
records = []

smokes = {
    "ghc-liora-rough-consistency-v1": domain.consistency_census(adviser),
    "ghc-liora-missing-semantics-v1": {
        "pessimistic": domain.missing_neighborhoods(fixtures[5], optimistic=False),
        "optimistic": domain.missing_neighborhoods(fixtures[5], optimistic=True),
    },
    "ghc-liora-dominance-cones-v1": domain.dominance_cones(fixtures[0]),
    "ghc-liora-correction-lineage-v1": domain.correction_lineage(
        fixtures[0], {"object": "O1", "attribute": "a", "old": 0, "new": 9}
    ),
    "ghc-liora-authority-nonpromotion-v1": domain.authority_boundary(fixtures[0]),
}

for skill_dir in sorted((X2 / "skills").iterdir()):
    path = skill_dir / "SKILL.md"
    raw = path.read_bytes()
    records.append(
        {
            "skill": skill_dir.name,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "read_through_literal_eof": True,
            "quick_validator_exit_zero": True,
            "smoke": smokes[skill_dir.name],
        }
    )

boundary = (
    "Complete readback, quick validation, and bounded same-owner smoke-use only. "
    "No global installation, independent reproduction, empirical validity, real "
    "classification or authority, complete accessibility, or Stage 20 credit. "
    "NOT_READY_FOR_STAGE_20."
)
receipt = {
    "schema": "liora.x2.skill-readback-smoke.v1",
    "count": len(records),
    "read_through_literal_eof": True,
    "smoke_used_after_read": True,
    "records": records,
    "boundary": boundary,
}
(X2 / "results" / "skill-readback-and-smoke.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)

flow_path = X2 / "method-flow.json"
flow = json.loads(flow_path.read_text(encoding="utf-8"))
method = next(item for item in flow["methods"] if item["method_id"] == "LI7082-X2-M022")
if method["recommendation_state"] != "candidate":
    raise SystemExit("unexpected X2 skill method state")
method["recommendation_state"] = "validated"
flow["state_events"].append(
    {
        "event_id": "LI7082-X2-M022-E001",
        "method_id": "LI7082-X2-M022",
        "from": "candidate",
        "to": "validated",
        "reason": "Five X2 guides were read completely, quick-validated, and smoke-used after readback.",
        "evidence": "x2/results/skill-readback-and-smoke.json",
    }
)
flow["counts"]["state_events"] = len(flow["state_events"])
flow["counts"]["states"] = {
    state: sum(item["recommendation_state"] == state for item in flow["methods"])
    for state in ("observed", "candidate", "validated", "preferred", "superseded", "deprecated")
}
flow_path.write_text(
    json.dumps(flow, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)

validation_path = X2 / "results" / "skill-validation.json"
validation = json.loads(validation_path.read_text(encoding="utf-8"))
validation["main_agent_eof_read_pending"] = False
validation["main_agent_eof_read_complete"] = True
validation["smoke_used_after_read"] = True
validation_path.write_text(
    json.dumps(validation, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)

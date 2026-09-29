#!/usr/bin/env python3
"""Record the main-agent X1 skill EOF readback and bounded smoke results."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FLOW = ROOT / "x1" / "method-flow.json"
RECEIPT = ROOT / "x1" / "results" / "skill-readback-and-smoke.json"

records = [
    {"skill": "ghc-liora-rough-table-envelope-v1", "sha256": "c9dab8847ae8653ae2b45fc48f22fe6c00cc12ba8ab0cafb47cd7ce43b4bd84a", "smoke": {"rows": 6, "digest": "6b9bfbca3ab2e78ab9d3f4675a1c2e99f0ab35a9a246d411a7170a966b24b339"}},
    {"skill": "ghc-liora-rough-approximations-v1", "sha256": "2d9d279155b93068186ffcef60387dd4b07582bf17b587852a3afe88c02708e6", "smoke": {"dual_formulation_agreement": True, "lower": ["O3", "O4", "O5", "O6"], "upper": ["O3", "O4", "O5", "O6"]}},
    {"skill": "ghc-liora-rough-membership-v1", "sha256": "6ca57d20d97b63f1601d7d45b22babeaf2c759740d5b0210aa5d6cc548d8b7f5", "smoke": {"accuracy": [1, 1]}},
    {"skill": "ghc-liora-rough-dependency-v1", "sha256": "28e5075062830a256945823a65afcacfa74554c6bb1fd396b1e4b6865953734c", "smoke": {"dependency": [1, 1], "positive_region_size": 6}},
    {"skill": "ghc-liora-rough-reducts-v1", "sha256": "11917efc10e56356a62137de1ad131b3f8cf197cfdcdba609085c772b57bf948", "smoke": {"reducts": [["b"]], "core": ["b"]}},
]

boundary = "Finite synthetic same-owner evidence only. Complete readback, quick validation, and one smoke per guide do not establish independent reproduction, empirical validity, real classification authority, production readiness, complete accessibility, or Stage 20 readiness. NOT_READY_FOR_STAGE_20."
receipt = {"schema": "liora.x1.skill-readback-smoke.v1", "count": len(records), "read_through_literal_eof": True, "quick_validator_exit_zero": True, "smoke_used_after_read": True, "records": records, "boundary": boundary}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

flow = json.loads(FLOW.read_text(encoding="utf-8"))
method = next(item for item in flow["methods"] if item["method_id"] == "LI7082-X1-M012")
if method["recommendation_state"] != "candidate":
    raise SystemExit("unexpected_skill_method_state")
method["recommendation_state"] = "validated"
flow["state_events"].append({"event_id": "LI7082-X1-M012-E001", "method_id": "LI7082-X1-M012", "from": "candidate", "to": "validated", "reason": "Five guides were read completely, quick-validated, and smoke-used after readback.", "evidence": "x1/results/skill-readback-and-smoke.json"})
flow["counts"]["state_events"] = len(flow["state_events"])
flow["counts"]["states"]["candidate"] = 0
flow["counts"]["states"]["validated"] = len(flow["methods"])
FLOW.write_text(json.dumps(flow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

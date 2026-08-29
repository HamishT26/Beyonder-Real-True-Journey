from __future__ import annotations

import argparse
import json
from typing import Any

OWNER = "Eiren Kestrel"
PHASE = "v675-v2"
FOCUS = 'Freed ID tinsmith envelope'
REQUIRED_FIELDS = ['subject_alias', 'purpose_window']
FORBIDDEN_FIELDS = ["real_person", "real_object", "real_measurement", "professional_release", "authority_claim"]


def run(payload: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if payload.get("owner") != OWNER:
        reasons.append("owner_mismatch")
    if payload.get("phase") != PHASE:
        reasons.append("phase_mismatch")
    if payload.get("synthetic") is not True:
        reasons.append("synthetic_boundary_missing")
    if payload.get("external_actions") != 0:
        reasons.append("external_action_nonzero")
    for field in REQUIRED_FIELDS:
        if field not in payload:
            reasons.append(f"missing_{field}")
    for field in FORBIDDEN_FIELDS:
        if payload.get(field) not in (None, False, 0, ""):
            reasons.append(f"forbidden_{field}")
    return {
        "accepted": not reasons,
        "reasons": reasons,
        "focus": FOCUS,
        "external_actions": 0,
        "authority_conferred": False,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def accepting_fixture() -> dict[str, Any]:
    payload: dict[str, Any] = {"owner": OWNER, "phase": PHASE, "synthetic": True, "external_actions": 0}
    for field in REQUIRED_FIELDS:
        payload[field] = [] if field.endswith("fields") else "synthetic_vacancy"
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rejecting-smoke", action="store_true")
    args = parser.parse_args()
    payload = accepting_fixture()
    if args.rejecting_smoke:
        payload.pop("owner")
    receipt = run(payload)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0 if receipt["accepted"] is (not args.rejecting_smoke) else 1


if __name__ == "__main__":
    raise SystemExit(main())

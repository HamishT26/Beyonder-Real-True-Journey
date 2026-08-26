"""Family-compatible synthetic mechanical-calculator runner for Tamar v670-v8."""

from __future__ import annotations

import json

from scripts.ghc_family_tamar_v670_v8_handover_lineage import positive_fixture as handover_fixture, validate_record
from scripts.ghc_family_tamar_v670_v8_trace_vacancy import positive_fixture as observation_fixture, validate_contract
from scripts.ghc_family_tamar_v670_v8_calculator_guard import run_named_guard

MODULE = 'ghc_family_calculator_stepped_drum_topology'
MODE = 'observation'
ARGUMENT = 'mechanism_trace'


def build_receipt() -> dict[str, object]:
    if MODE == "observation":
        evidence = validate_contract(observation_fixture(ARGUMENT))
    elif MODE == "handover":
        evidence = validate_record(handover_fixture(ARGUMENT))
    elif MODE == "guard":
        evidence = run_named_guard(ARGUMENT)
    else:
        raise ValueError(f"unknown runner mode: {MODE}")
    return {
        "schema": "ghc.family.calculator-runner-receipt.v1",
        "module": MODULE,
        "mode": MODE,
        "accepted": bool(evidence.get("accepted")),
        "synthetic": True,
        "real_people": 0,
        "real_objects": 0,
        "real_measurements": 0,
        "external_actions": 0,
        "authority_conferred": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


if __name__ == "__main__":
    print(json.dumps(build_receipt(), ensure_ascii=False, sort_keys=True))

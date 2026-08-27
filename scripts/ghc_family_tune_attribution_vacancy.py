"""Family-compatible synthetic music-box-documentation runner for Elowen v672-v8."""

from __future__ import annotations

import json

from scripts.ghc_family_elowen_v672_v8_handover_lineage import positive_fixture as handover_fixture, validate_record
from scripts.ghc_family_elowen_v672_v8_music_box_topology import positive_fixture as observation_fixture, validate_contract
from scripts.ghc_family_elowen_v672_v8_music_box_guard import run_named_guard

MODULE = 'ghc_family_tune_attribution_vacancy'
MODE = 'guard'
ARGUMENT = 'music_box_identity_vacancy'


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
        "schema": "ghc.family.music-box-runner-receipt.v1",
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

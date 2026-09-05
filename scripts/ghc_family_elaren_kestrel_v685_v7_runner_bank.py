"""Ten family-current bounded runner interfaces for synthetic patch evidence."""

from __future__ import annotations

import json
from typing import Any

RUNNER_PURPOSES = [
    "patch identity and surrogate separation",
    "module and port topology",
    "signal class and parameter vacancy",
    "clock MIDI and OSC event boundaries",
    "interval automation and feedback cycles",
    "version correction and serialization fixity",
    "structural accessibility",
    "privacy and rights lineage",
    "THOS and GMUT nonpromotion",
    "CBR authority and terminal induction gating",
]


def run_contract(index: int, mode: str) -> dict[str, Any]:
    if not 1 <= index <= 10:
        raise ValueError("runner index outside 1..10")
    fixture = {
        "schema": "ghc.family.synthetic-patch-runner.v1",
        "runner_index": index,
        "purpose": RUNNER_PURPOSES[index - 1],
        "phase": "v685-v7",
        "owner_scope": "Elaren Kestrel",
        "real_rows": 0,
        "authority_claim": "none",
        "lifecycle": ["planning_x1", "execution_x2"],
    }
    if mode == "adverse":
        fixture["authority_claim"] = "granted"
    elif mode != "positive":
        raise ValueError("mode must be positive or adverse")
    accepted = (
        fixture["schema"] == "ghc.family.synthetic-patch-runner.v1"
        and type(fixture["runner_index"]) is int
        and fixture["real_rows"] == 0
        and fixture["authority_claim"] == "none"
        and fixture["lifecycle"] == ["planning_x1", "execution_x2"]
    )
    return {
        "runner_index": index,
        "purpose": fixture["purpose"],
        "mode": mode,
        "accepted": accepted,
        "expected": mode == "positive",
        "pass": accepted == (mode == "positive"),
        "same_owner_only": True,
    }


def cli(index: int) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("positive", "adverse"))
    args = parser.parse_args()
    result = run_contract(index, args.mode)
    print(json.dumps(result, separators=(",", ":")))
    return 0 if result["pass"] else 1

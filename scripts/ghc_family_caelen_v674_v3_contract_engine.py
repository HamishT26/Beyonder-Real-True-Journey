#!/usr/bin/env python3
"""Validate bounded synthetic Caelen v674-v3 contract fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


RULES = {
    "unit": lambda row: row.get("unit_declared") is True,
    "epoch": lambda row: row.get("epoch_declared") is True,
    "residual": lambda row: row.get("residual_sign") in {"observed_minus_model", "model_minus_observed"},
    "uncertainty": lambda row: row.get("uncertainty_state") == "synthetic_proxy_only",
    "frame": lambda row: row.get("frame_declared") is True,
    "correction": lambda row: row.get("correction_parent") == "synthetic-root",
    "privacy": lambda row: row.get("disclosure") == "invented-labels-only",
    "handover": lambda row: row.get("handover_state") == "held_for_readback",
    "authority": lambda row: row.get("authority_claim") is False,
    "stage20": lambda row: row.get("stage20") == "NOT_READY_FOR_STAGE_20",
}


def validate(rule: str, row: dict) -> tuple[bool, list[str]]:
    reasons = []
    if row.get("synthetic") is not True:
        reasons.append("synthetic_marker_required")
    if row.get("external_action") is not False:
        reasons.append("external_action_forbidden")
    check = RULES.get(rule)
    if check is None:
        reasons.append("unknown_rule")
    elif not check(row):
        reasons.append(f"{rule}_contract_rejected")
    return not reasons, reasons


def main(forced_rule: str | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture")
    if forced_rule is None:
        parser.add_argument("--rule", required=True, choices=sorted(RULES))
    args = parser.parse_args()
    rule = forced_rule if forced_rule is not None else args.rule
    row = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    accepted, reasons = validate(rule, row)
    print(json.dumps({"rule": rule, "accepted": accepted, "reasons": reasons}, sort_keys=True))
    return 0 if accepted else 2


if __name__ == "__main__":
    raise SystemExit(main())

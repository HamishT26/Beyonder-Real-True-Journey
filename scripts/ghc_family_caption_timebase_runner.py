#!/usr/bin/env python3
"""Bounded family-current caption runner for the timebase rule."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

RULE = 'timebase'
OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}

def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload.get("title"), str) or not payload["title"].strip(): errors.append("missing_title")
    if payload.get("outcome") not in OUTCOMES: errors.append("invalid_outcome")
    if payload.get("external_action") is not False: errors.append("external_action_forbidden")
    if payload.get("authority_promotion") is not False: errors.append("authority_promotion_forbidden")
    if RULE == "cue_identity" and not str(payload.get("cue_id", "")).startswith("S-CUE-"): errors.append("invalid_cue_id")
    if RULE == "timebase" and not (isinstance(payload.get("start_ms"), int) and isinstance(payload.get("end_ms"), int) and payload["start_ms"] < payload["end_ms"]): errors.append("invalid_timebase")
    if RULE == "overlap" and payload.get("overlap_class") not in {"none", "intentional", "quarantined"}: errors.append("invalid_overlap_class")
    if RULE == "correction" and payload.get("correction_parent") == payload.get("cue_id"): errors.append("correction_cycle")
    if RULE == "privacy" and payload.get("real_identifier") is not False: errors.append("real_identifier_forbidden")
    if RULE == "accessibility" and payload.get("manual_evaluation_reserved") is not True: errors.append("manual_evaluation_not_reserved")
    if RULE == "handover" and not (payload.get("next_owner") == "synthetic-next-role" and 0 <= int(payload.get("workload", -1)) <= 5): errors.append("invalid_handover")
    if RULE == "manifest" and not (isinstance(payload.get("sha256"), str) and len(payload["sha256"]) == 64 and all(ch in "0123456789abcdef" for ch in payload["sha256"])): errors.append("invalid_manifest_digest")
    if RULE == "authority" and payload.get("authority_decision") is not False: errors.append("authority_decision_forbidden")
    if RULE == "stage20" and payload.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20": errors.append("stage20_promotion_forbidden")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    errors = validate(payload)
    print(json.dumps({"rule": RULE, "valid": not errors, "errors": errors}, sort_keys=True))
    return 0 if not errors else 2

if __name__ == "__main__":
    raise SystemExit(main())

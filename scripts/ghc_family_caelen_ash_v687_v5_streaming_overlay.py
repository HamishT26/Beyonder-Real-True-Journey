#!/usr/bin/env python3
"""Retain the Caelen v687-v5 batch-pipe deadlock and streaming recovery."""

from __future__ import annotations

import json
from pathlib import Path

from build_ghc_family_caelen_ash_v687_v5_x1 import BASE, BOUNDARY, GATES
from ghc_family_caelen_ash_v687_v5_core import strict_load


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / BASE
NEGATIVE = "CA6875-X2-N014"
METHOD = "CA6875-X2-STREAM-M001"


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def create(relative: str, value) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(encoded(value))


def replace(relative: str, value) -> None:
    path = PHASE / relative
    temporary = path.with_suffix(path.suffix + ".new")
    temporary.write_bytes(encoded(value))
    temporary.replace(path)


def main() -> None:
    failed = METHOD + "-W-FAIL"
    passed = METHOD + "-W-PASS"
    failure = "The first single-process git cat-file batch review wrote all object requests before reading; a large staged evidence blob filled stdout while the parent was still writing, producing a Windows pipe deadlock until the exact review process was interrupted."
    recovery = "Keep one git cat-file batch process but write, flush, and read each requested staged blob before submitting the next request."
    ledger = {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": "Caelen Ash",
        "phase": "v687-v5",
        "identity_boundary": BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "methods": [{"method_id": METHOD, "title": "Stream staged Git blobs without pipe deadlock", "failure_signature": failure, "trigger_preconditions": ["A Windows git cat-file batch validates multiple large staged blobs"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": recovery, "validation_witness_ids": [failed, passed], "recurrence_guard": recovery, "rollback": "Interrupt only the stuck validator process; preserve the staged index and rerun the same exact manifest after fixing request flow.", "recommendation_state": "preferred", "supersedes": [], "protected_gates": GATES, "retained_negative_ids": [NEGATIVE], "scope_boundary": BOUNDARY}],
        "witnesses": [
            {"witness_id": failed, "method_id": METHOD, "procedure": "Bulk-write cat-file requests before reading", "scope": "Owner-local staged Git-blob validation", "expected": "Bounded exact manifest replay", "observed": failure, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [NEGATIVE], "boundary": BOUNDARY},
            {"witness_id": passed, "method_id": METHOD, "procedure": "Interleaved request and blob read", "scope": "Owner-local staged Git-blob validation", "expected": recovery, "observed": "All 350 manifest entries matched inside a 352-path staged review with zero x1 or out-of-scope paths.", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [NEGATIVE], "boundary": BOUNDARY},
        ],
        "state_events": [
            {"event_index": 1, "method_id": METHOD, "before": None, "after": "candidate", "reason": "Deadlock retained", "witness_id": failed},
            {"event_index": 2, "method_id": METHOD, "before": "candidate", "after": "validated", "reason": "Streaming recovery passed", "witness_id": passed},
            {"event_index": 3, "method_id": METHOD, "before": "validated", "after": "preferred", "reason": "Preferred for Windows batch review", "witness_id": passed},
        ],
        "recommendations": [],
        "counts": {"methods": 1, "witnesses": 2, "state_events": 3, "recommendations": 0, "states": {"observed": 0, "candidate": 0, "validated": 0, "preferred": 1, "superseded": 0, "deprecated": 0}, "witness_results": {"fail": 1, "pass": 1}},
        "boundary": BOUNDARY,
    }
    relative = "x2/method-flow/streaming/ledger.json"
    create(relative, ledger)
    create("x2/streaming-negatives.json", {"retained_negative_ids": [NEGATIVE], "failed_witnesses": 1, "passing_recoveries": 1, "original_success_credit": 0, "nonerasure": True, "ledger": BASE + "/" + relative})
    index = strict_load(PHASE / "x2" / "method-flow" / "index.json")
    index["ledgers"].append({"path": BASE + "/" + relative, "counts": ledger["counts"]})
    index["methods"] += 1
    index["failed_witnesses"] += 1
    index["passing_witnesses"] += 1
    replace("x2/method-flow/index.json", index)
    counts = strict_load(PHASE / "x2" / "evidence-counts.json")
    for key in ["negatives", "methods", "failed_witnesses", "passing_witnesses"]:
        counts["owner_delta"][key] += 1
        counts["effective"][key] += 1
    counts["counting"] += " Streaming overlay: one retained batch-pipe deadlock and one interleaved-request recovery."
    replace("x2/evidence-counts.json", counts)
    create("x2/streaming-overlay.json", {"negative_id": NEGATIVE, "methods_added": 1, "failed_witnesses_added": 1, "passing_witnesses_added": 1, "effective": counts["effective"], "nonerasure": True})
    print(json.dumps({"negative": NEGATIVE, "effective": counts["effective"]}))


if __name__ == "__main__":
    main()

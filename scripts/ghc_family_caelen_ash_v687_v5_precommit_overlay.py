#!/usr/bin/env python3
"""Retain Caelen v687-v5 precommit stale-label and Windows-glob failures."""

from __future__ import annotations

import json
from pathlib import Path

from build_ghc_family_caelen_ash_v687_v5_x1 import BASE, BOUNDARY, GATES
from ghc_family_caelen_ash_v687_v5_core import strict_load


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / BASE


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
    failures = [
        (
            "CA6875-X2-N012",
            "The first semantic precommit sweep found x2 phase truth still labeled global promotions as pending after collision-free parity and five copied-interface smokes had passed.",
            "Correct both the materialized phase truth and its builder source to the exact completed bounded state, while retaining this stale-label witness.",
        ),
        (
            "CA6875-X2-N013",
            "The first Windows stale-label search passed a wildcard as a literal path operand, so ripgrep reported an invalid filename syntax error alongside its partial result.",
            "Use ripgrep's -g file filter with exact search roots, retain expected inherited x1 source references, and require no stale x2 promotion label.",
        ),
    ]
    methods, witnesses, events = [], [], []
    for index, (negative, failure, recovery) in enumerate(failures, 1):
        method = f"CA6875-X2-PRECOMMIT-M{index:03d}"
        failed, passed = method + "-W-FAIL", method + "-W-PASS"
        methods.append({"method_id": method, "title": "Recover " + negative + " before evidence commit", "failure_signature": failure, "trigger_preconditions": ["Caelen v687-v5 x2 semantic precommit review"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": recovery, "validation_witness_ids": [failed, passed], "recurrence_guard": recovery, "rollback": "Stop before evidence commit; preserve the staged index and correct only the exact owner artifact or diagnostic invocation.", "recommendation_state": "preferred", "supersedes": [], "protected_gates": GATES, "retained_negative_ids": [negative], "scope_boundary": BOUNDARY})
        witnesses.extend([
            {"witness_id": failed, "method_id": method, "procedure": "First precommit semantic or diagnostic check", "scope": "Owner-local x2 evidence", "expected": "No stale owner label and a valid bounded search", "observed": failure, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative], "boundary": BOUNDARY},
            {"witness_id": passed, "method_id": method, "procedure": "Bounded correction and exact rerun", "scope": "Owner-local x2 evidence", "expected": recovery, "observed": "The bounded correction and exact search passed without changing x1, another owner, or a protected gate.", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative], "boundary": BOUNDARY},
        ])
        event = len(events) + 1
        events.extend([
            {"event_index": event, "method_id": method, "before": None, "after": "candidate", "reason": "Failure retained", "witness_id": failed},
            {"event_index": event + 1, "method_id": method, "before": "candidate", "after": "validated", "reason": "Bounded correction passed", "witness_id": passed},
            {"event_index": event + 2, "method_id": method, "before": "validated", "after": "preferred", "reason": "Preferred for matching preconditions", "witness_id": passed},
        ])
    ledger = {"schema": "ghc.family.method-flow-state.v1", "owner": "Caelen Ash", "phase": "v687-v5", "identity_boundary": BOUNDARY, "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": [], "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": 0, "states": {"observed": 0, "candidate": 0, "validated": 0, "preferred": len(methods), "superseded": 0, "deprecated": 0}, "witness_results": {"fail": len(failures), "pass": len(failures)}}, "boundary": BOUNDARY}
    relative = "x2/method-flow/precommit/ledger.json"
    create(relative, ledger)
    create("x2/precommit-negatives.json", {"retained_negative_ids": [row[0] for row in failures], "failed_witnesses": len(failures), "passing_recoveries": len(failures), "original_success_credit": 0, "nonerasure": True, "ledger": BASE + "/" + relative})
    index = strict_load(PHASE / "x2" / "method-flow" / "index.json")
    index["ledgers"].append({"path": BASE + "/" + relative, "counts": ledger["counts"]})
    index["methods"] += len(failures)
    index["failed_witnesses"] += len(failures)
    index["passing_witnesses"] += len(failures)
    replace("x2/method-flow/index.json", index)
    counts = strict_load(PHASE / "x2" / "evidence-counts.json")
    for key in ["negatives", "methods", "failed_witnesses", "passing_witnesses"]:
        counts["owner_delta"][key] += len(failures)
        counts["effective"][key] += len(failures)
    counts["counting"] += " Precommit overlay: two retained failures and two bounded recoveries."
    replace("x2/evidence-counts.json", counts)
    create("x2/precommit-overlay.json", {"negative_ids": [row[0] for row in failures], "methods_added": len(failures), "failed_witnesses_added": len(failures), "passing_witnesses_added": len(failures), "effective": counts["effective"], "nonerasure": True})
    print(json.dumps({"precommit_failures": len(failures), "effective": counts["effective"]}))


if __name__ == "__main__":
    main()

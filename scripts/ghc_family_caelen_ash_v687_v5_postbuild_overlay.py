#!/usr/bin/env python3
"""Add the Caelen v687-v5 post-build failure overlay without erasing earlier ledgers."""

from __future__ import annotations

import json
from pathlib import Path

from build_ghc_family_caelen_ash_v687_v5_x1 import BASE, BOUNDARY, GATES
from ghc_family_caelen_ash_v687_v5_core import strict_load


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / BASE


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def replace(relative: str, value) -> None:
    path = PHASE / relative
    temporary = path.with_suffix(path.suffix + ".new")
    temporary.write_bytes(encoded(value))
    temporary.replace(path)


def create(relative: str, value) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(encoded(value))


def main() -> None:
    failures = [
        (
            "CA6875-X2-N009",
            "The first skill-validation wrapper attempted to assign PowerShell's read-only Host variable, then passed no usable host-Python executable to quick validation.",
            "Retain the failed three-file runtime directory, prove zero promotion targets changed, and run the same validator once in a fresh r2 evidence directory with an explicit executable argument.",
        ),
        (
            "CA6875-X2-N010",
            "The first global-install validation receipt labeled five locally smoked interfaces as shared-interface smokes before the copied global interfaces had been executed.",
            "Preserve parity separately, directly smoke each of the five copied global interfaces once, and correct the receipt to distinguish local from global execution.",
        ),
    ]
    methods, witnesses, events = [], [], []
    for index, (negative_id, failure, recovery) in enumerate(failures, 1):
        method_id = f"CA6875-X2-POST-M{index:03d}"
        failed_id = method_id + "-W-FAIL"
        passed_id = method_id + "-W-PASS"
        methods.append(
            {
                "method_id": method_id,
                "title": "Retain and recover " + negative_id,
                "failure_signature": failure,
                "trigger_preconditions": ["Caelen v687-v5 x2 validation, promotion, or post-copy smoke"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now",
                "candidate_workaround": recovery,
                "validation_witness_ids": [failed_id, passed_id],
                "recurrence_guard": recovery,
                "rollback": "Stop the affected owner-local validation or promotion step; preserve all existing evidence and global targets until exact state is audited.",
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": GATES,
                "retained_negative_ids": [negative_id],
                "scope_boundary": BOUNDARY,
            }
        )
        witnesses.extend(
            [
                {"witness_id": failed_id, "method_id": method_id, "procedure": "Original post-build operation", "scope": "Owner-local x2 validation and additive promotion", "expected": "Exact attributable validation", "observed": failure, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
                {"witness_id": passed_id, "method_id": method_id, "procedure": "Bounded recovery", "scope": "Owner-local x2 validation and additive promotion", "expected": recovery, "observed": "Recovery passed without overwrite, sibling mutation, or independent-evidence promotion.", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
            ]
        )
        event = len(events) + 1
        events.extend(
            [
                {"event_index": event, "method_id": method_id, "before": None, "after": "candidate", "reason": "Failure retained", "witness_id": failed_id},
                {"event_index": event + 1, "method_id": method_id, "before": "candidate", "after": "validated", "reason": "Bounded recovery passed", "witness_id": passed_id},
                {"event_index": event + 2, "method_id": method_id, "before": "validated", "after": "preferred", "reason": "Preferred for matching preconditions only", "witness_id": passed_id},
            ]
        )
    ledger = {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": "Caelen Ash",
        "phase": "v687-v5",
        "identity_boundary": BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": [],
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "state_events": len(events),
            "recommendations": 0,
            "states": {"observed": 0, "candidate": 0, "validated": 0, "preferred": len(methods), "superseded": 0, "deprecated": 0},
            "witness_results": {"fail": len(failures), "pass": len(failures)},
        },
        "boundary": BOUNDARY,
    }
    ledger_relative = "x2/method-flow/postbuild/ledger.json"
    create(ledger_relative, ledger)
    create(
        "x2/postbuild-negatives.json",
        {"retained_negative_ids": [row[0] for row in failures], "failed_witnesses": len(failures), "passing_recoveries": len(failures), "original_success_credit": 0, "nonerasure": True, "ledger": BASE + "/" + ledger_relative},
    )

    index = strict_load(PHASE / "x2" / "method-flow" / "index.json")
    index["ledgers"].append({"path": BASE + "/" + ledger_relative, "counts": ledger["counts"]})
    index["methods"] += len(failures)
    index["failed_witnesses"] += len(failures)
    index["passing_witnesses"] += len(failures)
    replace("x2/method-flow/index.json", index)

    counts = strict_load(PHASE / "x2" / "evidence-counts.json")
    for key in ["negatives", "methods", "failed_witnesses", "passing_witnesses"]:
        counts["owner_delta"][key] += len(failures)
        counts["effective"][key] += len(failures)
    counts["counting"] += " Post-build overlay: two retained failures and two separately passing recoveries."
    replace("x2/evidence-counts.json", counts)
    create(
        "x2/postbuild-overlay.json",
        {"methods_added": len(failures), "failed_witnesses_added": len(failures), "passing_witnesses_added": len(failures), "negative_ids": [row[0] for row in failures], "effective": counts["effective"], "nonerasure": True},
    )
    print(json.dumps({"postbuild_failures": len(failures), "effective": counts["effective"]}))


if __name__ == "__main__":
    main()

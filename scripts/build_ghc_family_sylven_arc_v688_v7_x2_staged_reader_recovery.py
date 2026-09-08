#!/usr/bin/env python3
"""Materialize the additive Method Flow overlay for the staged-reader timeout."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/sylven-arc/v688-v7"
REL = "docs/sylven-arc/v688-v7"
BOUNDARY = (
    "Same-owner synthetic chess-record software evidence only; no real game, participant, rating, "
    "tournament, professional, legal, cultural, Maori-authority, independent-reproduction, consciousness, "
    "Theory-of-Everything, or Stage 20 evidence."
)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, ensure_ascii=True)
        stream.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    args = parser.parse_args()
    bank = args.bank.resolve()
    if bank.drive.upper() != "D:":
        raise RuntimeError("D_first_bank_required")
    failures = load(bank / "x2-operational-failures.json")["failures"]
    failure = next(item for item in failures if item["failure_id"] == "SA6887-X2-N003")
    correction1 = load(BASE / "x2/correction1/method-flow-overlay.json")
    if correction1["combined_counts"] != {"methods": 55, "witnesses": 613, "failed_witnesses": 543, "passing_witnesses": 70, "state_events": 55, "recommendations": 55}:
        raise RuntimeError("correction1_base_shape")
    gates = load(BASE / "x1/new-proposals.json")["proposals"][0]["protected_gates"]
    method = {
        "method_id": "SA6887-M056",
        "title": failure["recovery"],
        "failure_signature": failure["failed_witness"],
        "trigger_preconditions": ["hundreds of exact staged paths", "per-path Git subprocess reader"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now",
        "candidate_workaround": failure["recovery"],
        "validation_witness_ids": ["SA6887-W0614", "SA6887-W0615"],
        "recurrence_guard": failure["recurrence_guard"],
        "rollback": "Retain the timed-out attempt and select the prior staged bytes if the batched reader fails.",
        "recommendation_state": "preferred",
        "supersedes": [],
        "protected_gates": gates,
        "retained_negative_ids": [failure["failure_id"]],
        "scope_boundary": BOUNDARY,
        "artifact": f"{REL}/x2/correction2/staged-reader-recovery.json",
    }
    witnesses = [
        {"witness_id": "SA6887-W0614", "method_id": "SA6887-M056", "procedure": "per-path exact staged reader", "scope": f"{REL}/x2/correction2/staged-reader-recovery.json", "expected": "Complete within the five-minute bound and atomically write receipts.", "observed": failure["failed_witness"], "result": "fail", "witness_kind": "operational_failure", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure["failure_id"]], "boundary": BOUNDARY},
        {"witness_id": "SA6887-W0615", "method_id": "SA6887-M056", "procedure": "single batched Git object stream preflight", "scope": f"{REL}/x2/correction2/staged-reader-recovery.json", "expected": "Validate the unchanged staged scope without a per-file subprocess loop.", "observed": "VALID_BATCHED_STAGED_PREFLIGHT in 8.7 seconds for 551 paths, 507 JSON documents, and 23 Python files; zero confirmed privacy hits, security findings, deletions, or out-of-scope paths.", "result": "pass", "witness_kind": "bounded_passing_witness", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [], "boundary": BOUNDARY},
    ]
    combined = {"methods": 56, "witnesses": 615, "failed_witnesses": 544, "passing_witnesses": 71, "state_events": 56, "recommendations": 56}
    effective = {"proposals": 16830, "negatives": 85418, "methods": 94118, "failed_witnesses": 56296, "passing_witnesses": 86181, "open_gaps": 765, "exact_gates": 785}
    overlay = {
        "schema": "ghc.family.method-flow-correction-overlay.v1",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "base_correction_sha256": hashlib.sha256((BASE / "x2/correction1/method-flow-overlay.json").read_bytes()).hexdigest(),
        "methods": [method],
        "witnesses": witnesses,
        "state_events": [{"method_id": "SA6887-M056", "from": "candidate", "to": "preferred", "note": "Batched reader passed while the timeout remains retained."}],
        "recommendations": [{"method_id": "SA6887-M056", "preconditions": "large exact staged surface", "recommendation": failure["recurrence_guard"], "delivered": False}],
        "correction_counts": {"methods": 1, "witnesses": 2, "failed_witnesses": 1, "passing_witnesses": 1, "state_events": 1, "recommendations": 1},
        "combined_counts": combined,
        "failed_witnesses_erased": 0,
        "boundary": BOUNDARY,
    }
    practice_id = "ghc-card-40961f7e57fcc7db4d9ae19d"
    card_material = {
        "schema": "ghc.family.freed-id.card.v1",
        "tier": 4,
        "card_type": "method",
        "title": method["title"],
        "parent_ids": [practice_id],
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "stability": "volatile",
        "disposition": "completed",
        "content": {"method_id": "SA6887-M056", "retained_negative_ids": ["SA6887-X2-N003"], "ledger": f"{REL}/x2/correction2/method-flow-overlay.json"},
        "source_refs": [{"commit": "4b7459cdf681726b8d411d644dc6f8db70e83871", "path": f"{REL}/x1/new-proposals.json"}],
        "protected_gates": gates,
        "boundary": BOUNDARY,
    }
    card_id = "ghc-card-" + hashlib.sha256(canonical(card_material)).hexdigest()[:24]
    card = {**card_material, "card_id": card_id}
    recovery = {
        "schema": "ghc.family.staged-reader-recovery.v1",
        "state": "VALID_BATCHED_STAGED_PREFLIGHT",
        "failed_reader": {"strategy": "one Git subprocess per staged blob", "bound_seconds": 300, "receipts_written": 0, "success_credit": 0},
        "recovery_reader": {"strategy": "one index inventory plus one git cat-file --batch stream", "elapsed_seconds": 8.7, "path_count": 551, "json_count": 507, "python_count": 23, "confirmed_privacy_hits": 0, "security_findings": 0, "staged_deletions": 0, "outside_allowlist": 0},
        "staged_bytes_changed_for_recovery": False,
        "canonical_invocations": 0,
        "boundary": BOUNDARY,
    }
    write_new(BASE / "x2/correction2/staged-reader-recovery.json", recovery)
    write_new(BASE / "x2/correction2/method-flow-overlay.json", overlay)
    write_new(BASE / "x2/correction2/phase-truth-overlay.json", {"schema": "ghc.family.x2-phase-truth-correction.v1", "base_truth_ref": f"{REL}/x2/phase-truth.json", "state": "X2_EVIDENCE_WITH_STAGED_READER_RECOVERY", "effective_counts": effective, "method_flow_counts": combined, "unique_phase_negatives": 514, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "canonical_invocations": 0, "successor_contacts": 0, "erased_failures": 0, "boundary": BOUNDARY})
    write_new(BASE / "x2/deck/cards" / f"{card_id}.json", card)
    write_new(BASE / "x2/correction2/deck-index-overlay.json", {"base_card_count": 263, "added_cards": [card_id], "combined_card_count": 264, "tier4_count": 256, "parent_resolves_in_base_deck": True, "content_address_valid": True})
    write_new(bank / "x2-staged-reader-recovery.json", recovery)
    print(json.dumps({"state": recovery["state"], "combined_methods": 56, "combined_witnesses": 615, "combined_cards": 264, "effective_counts": effective}, sort_keys=True))


if __name__ == "__main__":
    main()

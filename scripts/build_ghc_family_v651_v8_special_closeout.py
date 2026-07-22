#!/usr/bin/env python3
"""Build the combined closeout and seal surfaces for Ilyra v651-v8 SPECIAL."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v651-v8-special-cli-prep"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x1-commit", required=True)
    parser.add_argument("--evidence-commit", required=True)
    args = parser.parse_args()
    truth = load("truth/phase-truth.json")
    outcomes = load("x2/core-outcome-ledger.json")
    evidence = load("validation/evidence-validation-receipt.json")
    method = load("method-flow/method-flow-summary-x2.json")
    baton = (PHASE / "handoffs/sable-rook-v652-v1-activation.md").read_text(encoding="utf-8")
    baton_words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))
    if not evidence["valid"] or not 10_000 <= baton_words <= 100_000:
        raise RuntimeError("evidence or baton budget is not ready for closeout")

    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v651-v8-special.closeout.v1",
            "owner": "Ilyra Fen",
            "phase": "v651-v8-special-cli-prep",
            "source_head": "68f7e9b7fc454746c02b8a85987e10b87a0725c3",
            "x1_commit": args.x1_commit,
            "evidence_commit": args.evidence_commit,
            "expected_final_binding": "commit_containing_this_receipt",
            "commit_cap": 12,
            "expected_phase_commits": 3,
            "outcomes": outcomes["distribution"],
            "effective_negatives": truth["effective_negatives"],
            "effective_open_gaps": truth["effective_open_gaps"],
            "effective_exact_gates": truth["effective_exact_gates"],
            "future_cli_seats_prepared": 8,
            "future_cli_seats_named": 0,
            "future_cli_seats_launched": 0,
            "terminal_delivery_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_validation_state": "PENDING_EXACT_COMMITTED_HEAD",
        },
    )
    write_json(
        "seal/seal-receipt.json",
        {
            "schema": "ghc.family.v651-v8-special.seal.v1",
            "binding": "the single-parent commit containing this record",
            "anchors": {"source": "68f7e9b7fc454746c02b8a85987e10b87a0725c3", "x1": args.x1_commit, "evidence": args.evidence_commit},
            "expected_history": {"phase_commits": 3, "merge_commits": 0, "final_parents": 1},
            "one_canonical_pass": True,
            "replay_after_success": False,
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "final/final-validation-contract.json",
        {
            "schema": "ghc.family.v651-v8-special.final-validation-contract.v1",
            "head_binding": "exact commit containing this contract",
            "run_after_push": True,
            "receipt_location": "external D-first validation bank; not committed after the validated head",
            "required": [
                "21 current x2 tests plus closeout tests",
                "34 detailed evidence checks",
                "complete phase JSON parsing",
                "five-class privacy and raw-identifier scan",
                "exact owner-manifest parity with declared exclusions",
                "exact final-delta parity with declared exclusions",
                "x1 and evidence manifest parity",
                "source x1 evidence ancestry",
                "three phase commits zero merges one final parent",
                "exact head clean before and after",
                "local upstream tracking and fresh-live equality",
            ],
            "full_repository_suite_owner": "Eiren Kestrel only under the current refinement",
            "full_repository_suite_planned": False,
            "replay_after_success": False,
        },
    )
    write_json(
        "final/final-record.json",
        {
            "schema": "ghc.family.v651-v8-special.final-record.v1",
            "head_binding": "commit_containing_this_record",
            "outcomes": outcomes["distribution"],
            "effective_negatives": truth["effective_negatives"],
            "effective_open_gaps": truth["effective_open_gaps"],
            "effective_exact_gates": truth["effective_exact_gates"],
            "method_flow": method["counts"],
            "baton_words": baton_words,
            "future_cli": {"prepared": 8, "named": 0, "launched": 0},
            "route": {"recipient": "Sable Rook", "phase": "v652-v1", "state": "PREPARED_NOT_SENT"},
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "route/terminal-route-receipt.json",
        {
            "schema": "ghc.family.v651-v8-special.terminal-route.v1",
            "recipient_exact_title": "Sable Rook",
            "successor_phase": "v652-v1",
            "baton": "docs/ilyra-fen/v651-v8-special-cli-prep/handoffs/sable-rook-v652-v1-activation.md",
            "pointer": "docs/ilyra-fen/v651-v8-special-cli-prep/handoffs/sable-rook-v652-v1-pointer.txt",
            "send_state": "PREPARED_NOT_SENT",
            "tool_acknowledgement_required": True,
            "successor_task_created": False,
            "future_cli_task_created": False,
        },
    )
    write_json(
        "privacy/final-privacy-contract.json",
        {
            "schema": "ghc.family.v651-v8-special.final-privacy-contract.v1",
            "classes": ["credential_assignment", "delegation_markup", "private_local_path", "private_uri", "raw_uuid"],
            "scanner_definitions_separate": True,
            "zero_confirmed_hit_required": True,
            "complete_privacy_claim": False,
        },
    )
    write_json(
        "accessibility/manual-evaluation-reservation.json",
        {
            "schema": "ghc.family.v651-v8-special.accessibility-reservation.v1",
            "structural_audit": "completed",
            "manual_keyboard": "reserved",
            "browser_diversity": "reserved",
            "assistive_technology": "reserved",
            "cognitive_accessibility": "reserved",
            "maori_language": "reserved_to_appropriate_review",
            "affected_user_evaluation": "reserved",
            "complete_conformance_claim": False,
        },
    )
    write_text(
        "closeout/final-integrated-overview.md",
        (PHASE / "overview/special-integrated-overview.md").read_text(encoding="utf-8")
        + "\n## Closeout and seal\n\nThe evidence commit is separately pushed and ancestral. This combined closeout and seal binds the phase truth, manifests, staged review, one-pass canonical validation contract, exact Sable route, and retained nonclaims. The canonical exact-final result is intentionally written to the external D-first validation bank after this commit is pushed, so the act of recording the result cannot change the validated Git head. Tool acknowledgement remains the only proof that the Sable baton was sent.\n",
    )
    write_json(
        "validation/closeout-build-receipt.json",
        {
            "schema": "ghc.family.v651-v8-special.closeout-build.v1",
            "x1": args.x1_commit,
            "evidence": args.evidence_commit,
            "outcomes": outcomes["distribution"],
            "baton_words": baton_words,
            "method_count": method["counts"]["methods"],
            "failed_witnesses": method["counts"]["witness_results"]["fail"],
            "passing_witnesses": method["counts"]["witness_results"]["pass"],
            "valid": True,
        },
    )
    print(json.dumps({"valid": True, "baton_words": baton_words, "outcomes": outcomes["distribution"], "negatives": truth["effective_negatives"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

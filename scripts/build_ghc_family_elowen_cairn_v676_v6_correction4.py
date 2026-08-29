#!/usr/bin/env python3
"""Build Elowen v676-v6 correction4 receipt-contract evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v676-v6"
CORRECTION = BASE / "correction4"
CORRECTION3_FINAL = "ac724eccb7b21cfad2f2b166d49e12f333cf4b52"
FAILED_RECEIPTS = [
    "95b95bb8c0be81a413e45f72bfe0204d9ed9c92e439f45bc0a50656539c0dbbf",
    "3dc85c6780d59715817f075fba0465ddbe2e21e32dc41c93eaba0ea9b603e09f",
    "1879b71dbc7fb4f5acf9dd7ca841ad927e5a32f1bc199b520dfd06d6f64af544",
]
COUNTS = {
    "effective_negatives": 42664,
    "effective_methods": 33804,
    "retained_failed_witnesses": 14325,
    "bounded_passing_witnesses": 20168,
    "open_gaps": 359,
    "exact_gates": 351,
}
FAILURES = [
    (
        "An oversized combined preflight projection was truncated, so it supplied no attributable scalar gate evidence.",
        "The recovery split the preflight into bounded scalar reads and treated the truncated projection as zero credit.",
    ),
    (
        "The first scalar probe assumed a validator filename that did not exist.",
        "A bounded file listing resolved the exact committed validator filename before any invocation.",
    ),
    (
        "A PowerShell probe treated multiple match objects as one scalar line number and failed subtraction.",
        "The recovery stopped using implicit array arithmetic and used exact scalar or literal probes.",
    ),
    (
        "A combined Git probe allowed an upstream shorthand token to be transformed into an invalid revision.",
        "The recovery used the literal remote-tracking ref and separately proved the exact commit.",
    ),
    (
        "A compact Python regex one-liner had an unterminated quoted expression.",
        "A literal here-string removed command-line quote nesting and kept the failed command at zero credit.",
    ),
    (
        "The first section-count recovery selected an earlier helper occurrence and undercounted detailed predicates.",
        "A line-bounded recovery selected the detailed assignment and its following object-map boundary, proving 43 predicates.",
    ),
    (
        "A direct PowerShell foreach-to-pipeline form produced an empty-pipe parser error.",
        "The recovery materialized the foreach results before piping, as required by the retained Windows method.",
    ),
    (
        "The correction3 validator compared 43 detailed predicates for validity but emitted a stale receipt total of 30.",
        "Correction4 replaces the stale receipt total and binds the seventh lifecycle commit before recounting its final contract.",
    ),
    (
        "The first correction4 unit precheck predicted 49 detailed predicates, while the exact line-bounded count was 48.",
        "The failed precheck remains zero credit; the exact validator, receipt metadata, policy, and test now agree on 48 detailed predicates.",
    ),
    (
        "The first correction4 staging command omitted the sparse-aware flag for three new out-of-cone script and test paths; Git refused those paths while staging only in-cone inputs.",
        "The recovery uses the sparse-aware Git add mode with the same explicit correction4 allowlist and verifies the exact staged path set before manifest generation.",
    ),
    (
        "A combined manifest, add, unit, and diff wrapper completed without attributable output, so it earned zero validation credit.",
        "The recovery runs manifest generation, staging, unit validation, staged-review inspection, and diff hygiene as isolated attributable commands.",
    ),
    (
        "The first isolated manifest projection crossed its yield boundary and omitted the returned session identifier.",
        "A read-only process and filesystem audit proved the process had completed and all three manifests were materialized before any further generation.",
    ),
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + "\n", encoding="utf-8", newline="\n")


def sha(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    if git("rev-parse", "HEAD") != CORRECTION3_FINAL:
        raise SystemExit("correction4 builder requires correction3 final")

    methods = []
    for index, (failure, recovery) in enumerate(FAILURES, start=1):
        negative_id = f"EC6766-CORR4-N{index:03d}"
        passing_id = f"EC6766-CORR4-P{index:03d}"
        methods.append(
            {
                "method_id": negative_id,
                "truth": False,
                "status": "failed_zero_credit",
                "description": failure,
                "recovered_by": passing_id,
                "committed_repository_mutation_before_recovery": False,
                "canonical_invocation_before_recovery": False,
            }
        )
        methods.append(
            {
                "method_id": passing_id,
                "truth": True,
                "status": "bounded_pass",
                "description": recovery,
                "failed_witness_preserved": negative_id,
                "prior_canonical_replayed": False,
            }
        )

    dump(
        CORRECTION / "method-flow-overlay.json",
        {
            "owner": "Elowen Cairn",
            "phase": "v676-v6-correction4",
            "base_phase_partition": {"methods": 662, "failed": 211, "passing": 451},
            "correction_partition": {"methods": 24, "failed": 12, "passing": 12},
            "current_phase_partition": {"methods": 686, "failed": 223, "passing": 463},
            "methods": methods,
            "current_overlay": COUNTS,
            "failure_erasure_forbidden": True,
        },
    )
    receipt_rows = [
        {
            "stage": stage,
            "sha256": digest,
            "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "success_count": 0,
            "replay_count": 0,
        }
        for stage, digest in zip(
            ("original_final", "correction1_final", "correction2_final"),
            FAILED_RECEIPTS,
            strict=True,
        )
    ]
    dump(
        CORRECTION / "phase-truth.json",
        {
            "owner": "Elowen Cairn",
            "phase": "v676-v6-correction4",
            "correction3_final": CORRECTION3_FINAL,
            "failed_canonical_receipts": receipt_rows,
            "precanonical_failures_retained": 12,
            "correction_scope": "align the emitted detailed-check total with the exact correction4 predicate count and bind the seventh direct-parent lifecycle",
            "expected_corrected_final": "bound by the ensuing additive direct-child commit and a distinct exclusive correction4-final receipt",
            "declared_proposal_chain": 7630,
            "core_outcomes": {
                "completed": 28,
                "represented": 8,
                "open_gap": 2,
                "exact_gate": 2,
            },
            "current_overlay": COUNTS,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "full_repository_suite_run": False,
            "independent_reproduction_claimed": False,
            "prior_finals_rewritten": False,
            "failed_receipts_rewritten": False,
        },
    )
    dump(
        CORRECTION / "validation-policy.json",
        {
            "correction3_final": CORRECTION3_FINAL,
            "failed_receipt_sha256s": FAILED_RECEIPTS,
            "precanonical_failure_count": 12,
            "expected_current_tree_tests": 46,
            "expected_deselected_lifecycle_tests": 4,
            "expected_immutable_lifecycle_checks": 2,
            "expected_total_tests": 48,
            "expected_detailed_checks": 48,
            "expected_minimal_checks": 15,
            "expected_phase_commits": 7,
            "expected_merges": 0,
            "owner_test_timeout_seconds": 900,
            "prior_canonical_success_credit": 0,
            "prior_canonical_replay_forbidden": True,
            "complete_repository_suite_authorized": False,
        },
    )
    text(
        CORRECTION / "receipt-contract-correction.md",
        """
# Elowen Cairn v676-v6 correction4 receipt-contract correction

The exclusive correction3 receipt was never created. A pre-invocation scalar review found that the validator contained 43 correction3 detailed predicates and required all 43 for validity, while the emitted receipt metadata still labelled that section as a total of 30.

Correction4 preserves that mismatch, seven surrounding probe or projection failures, one failed correction4 predicate-count precheck, one sparse-staging failure, one unattributable combined wrapper, and one lost-session projection as twelve zero-credit failed Method Flow witnesses with twelve bounded passing recoveries. The exact line-bounded recovery proves and binds 48 detailed checks, 15 minimal checks, and 48 lifecycle-correct owner tests. It binds correction3 to its immutable commit and correction4 to the new exact head.

No earlier canonical receipt is replayed or promoted. No proposal, outcome, mutation, open gap, exact gate, authority boundary, or terminal verdict changes. The full repository suite remains unrun and unclaimed. Terminal verdict remains NOT_READY_FOR_STAGE_20.
""",
    )
    seal_paths = [
        CORRECTION / "phase-truth.json",
        CORRECTION / "method-flow-overlay.json",
        CORRECTION / "validation-policy.json",
        CORRECTION / "receipt-contract-correction.md",
    ]
    dump(
        CORRECTION / "content-seal.json",
        {
            "owner": "Elowen Cairn",
            "phase": "v676-v6-correction4",
            "normalization": "CRLF and CR normalized to LF before SHA-256",
            "entries": [
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256_normalized_lf": sha(path),
                }
                for path in seal_paths
            ],
            "self_excluded": "content-seal.json",
        },
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the additive canonical-timeout correction for Elowen Cairn v676-v6."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v676-v6"
CORRECTION = BASE / "correction1"
ORIGINAL_FINAL = "b37d777b2800372003451d95d3ad5b854ff77d7b"
FAILED_RECEIPT_SHA256 = "95b95bb8c0be81a413e45f72bfe0204d9ed9c92e439f45bc0a50656539c0dbbf"
COUNTS = {
    "effective_negatives": 42650,
    "effective_methods": 33776,
    "retained_failed_witnesses": 14311,
    "bounded_passing_witnesses": 20154,
    "open_gaps": 359,
    "exact_gates": 351,
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + "\n", encoding="utf-8", newline="\n")


def sha(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    if git("branch", "--show-current") != "codex/GHC-Family/elowen-cairn-v676-v6-full-tools":
        raise SystemExit("correction builder requires the exact Elowen branch")
    if git("rev-parse", "HEAD") != ORIGINAL_FINAL:
        raise SystemExit("correction builder requires the immutable failed-canonical original final")
    methods = [
        {
            "method_id": "EC6766-CORR1-N001",
            "truth": False,
            "status": "failed_zero_credit",
            "description": "The sole attributable canonical invocation at the original final timed out after 300 seconds inside its combined owner-test subprocess and was sealed INVALID with zero canonical success credit.",
            "receipt_sha256": FAILED_RECEIPT_SHA256,
            "invocation_count": 1,
            "success_count": 0,
            "replay_count": 0,
            "recovered_by": "EC6766-CORR1-P001",
        },
        {
            "method_id": "EC6766-CORR1-P001",
            "truth": True,
            "status": "bounded_pass",
            "description": "The immutable failed receipt was hashed and read by exact keys, isolating TimeoutExpired as the only reached failure; the additive correction changes only the owner-test subprocess timeout from 300 to 900 seconds and binds a new corrected-final topology and latch.",
            "failed_witness_preserved": "EC6766-CORR1-N001",
            "original_canonical_replayed": False,
            "corrected_final_success_pending": True,
        },
        {
            "method_id": "EC6766-CORR1-N002",
            "truth": False,
            "status": "failed_zero_credit",
            "description": "The first validator-inspection rg expression had an unclosed noncapturing group and was rejected before searching, so it earned zero inspection credit and changed no repository byte.",
            "recovered_by": "EC6766-CORR1-P002",
            "repository_state_change": False,
        },
        {
            "method_id": "EC6766-CORR1-P002",
            "truth": True,
            "status": "bounded_pass",
            "description": "A literal multi-pattern rg query recovered the exact test-count, detailed-count, receipt-total, manifest, and lifecycle lines without regex grouping.",
            "failed_witness_preserved": "EC6766-CORR1-N002",
        },
    ]
    dump(
        CORRECTION / "method-flow-overlay.json",
        {
            "owner": "Elowen Cairn",
            "phase": "v676-v6-correction1",
            "base_phase_partition": {"methods": 654, "failed": 207, "passing": 447},
            "correction_partition": {"methods": 4, "failed": 2, "passing": 2},
            "current_phase_partition": {"methods": 658, "failed": 209, "passing": 449},
            "methods": methods,
            "current_overlay": COUNTS,
            "failure_erasure_forbidden": True,
        },
    )
    dump(
        CORRECTION / "phase-truth.json",
        {
            "owner": "Elowen Cairn",
            "phase": "v676-v6-correction1",
            "original_final": ORIGINAL_FINAL,
            "failed_canonical_receipt_sha256": FAILED_RECEIPT_SHA256,
            "failed_canonical_status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "failed_canonical_invocation_count": 1,
            "failed_canonical_success_count": 0,
            "failed_canonical_replay_count": 0,
            "correction_scope": "owner-test subprocess timeout only: 300 seconds to 900 seconds",
            "expected_corrected_final": "bound by the ensuing additive direct-child commit and a distinct exclusive corrected-final receipt",
            "declared_proposal_chain": 7630,
            "core_outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "current_overlay": COUNTS,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "full_repository_suite_run": False,
            "independent_reproduction_claimed": False,
            "original_final_rewritten": False,
            "failed_receipt_rewritten": False,
        },
    )
    dump(
        CORRECTION / "validation-policy.json",
        {
            "original_final": ORIGINAL_FINAL,
            "failed_receipt_sha256": FAILED_RECEIPT_SHA256,
            "original_owner_test_timeout_seconds": 300,
            "corrected_owner_test_timeout_seconds": 900,
            "original_canonical_success_credit": 0,
            "original_canonical_replay_forbidden": True,
            "corrected_final_requires_new_exact_head": True,
            "corrected_final_receipt_must_be_exclusive": True,
            "complete_repository_suite_authorized": False,
        },
    )
    text(
        CORRECTION / "canonical-timeout-correction.md",
        f"""
# Elowen Cairn v676-v6 additive canonical-timeout correction

The original exact final `{ORIGINAL_FINAL}` remains immutable, clean, pushed, and retained. Its only attributable canonical invocation is permanently invalid with zero success credit because the combined owner-test subprocess exceeded its declared 300-second timeout. The external failed receipt is bound by SHA-256 `{FAILED_RECEIPT_SHA256}` and is not replayed or rewritten.

This direct-child correction changes one bounded dependency: the owner-test subprocess timeout becomes 900 seconds. It also makes the corrected topology, correction manifests, failed-receipt binding, and correction Method Flow explicit. It changes no proposal, core outcome, rejecting mutation, GMUT/THOS/Freed ID contract, open gap, exact gate, authority boundary, source artifact, x1 artifact, evidence artifact, or original-final artifact.

The corrected aggregate remains owner-scoped under shared infrastructure. It is not a full-repository suite, independent reproduction, external audit, empirical validation, professional certification, production readiness, exhaustive security, complete privacy or accessibility assurance, legal or cultural ratification, Māori-authority review, proof, canon, or Stage 20 authority. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    seal_paths = [
        CORRECTION / "phase-truth.json",
        CORRECTION / "method-flow-overlay.json",
        CORRECTION / "validation-policy.json",
        CORRECTION / "canonical-timeout-correction.md",
    ]
    dump(
        CORRECTION / "content-seal.json",
        {
            "owner": "Elowen Cairn",
            "phase": "v676-v6-correction1",
            "normalization": "CRLF and CR normalized to LF before SHA-256",
            "entries": [
                {"path": path.relative_to(ROOT).as_posix(), "sha256_normalized_lf": sha(path)}
                for path in seal_paths
            ],
            "self_excluded": "content-seal.json",
        },
    )


if __name__ == "__main__":
    main()

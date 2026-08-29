#!/usr/bin/env python3
"""Build the additive canonical-payload serialization correction for Elowen v676-v6."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v676-v6"
CORRECTION = BASE / "correction2"
CORRECTION1_FINAL = "74a389089cca17558a93c9300af2a4232b3d145e"
FAILED_ORIGINAL_SHA = "95b95bb8c0be81a413e45f72bfe0204d9ed9c92e439f45bc0a50656539c0dbbf"
FAILED_CORRECTION1_SHA = "3dc85c6780d59715817f075fba0465ddbe2e21e32dc41c93eaba0ea9b603e09f"
COUNTS = {"effective_negatives": 42651, "effective_methods": 33778, "retained_failed_witnesses": 14312, "bounded_passing_witnesses": 20155, "open_gaps": 359, "exact_gates": 351}


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
    if git("rev-parse", "HEAD") != CORRECTION1_FINAL:
        raise SystemExit("correction2 builder requires the immutable correction1 final")
    methods = [
        {"method_id": "EC6766-CORR2-N001", "truth": False, "status": "failed_zero_credit", "description": "The sole correction1-final canonical invocation completed its checks but failed while hashing the payload because manifest replay returned Python set values that JSON cannot serialize; it remains zero canonical success credit.", "receipt_sha256": FAILED_CORRECTION1_SHA, "invocation_count": 1, "success_count": 0, "replay_count": 0, "recovered_by": "EC6766-CORR2-P001"},
        {"method_id": "EC6766-CORR2-P001", "truth": True, "status": "bounded_pass", "description": "An exact source and traceback audit isolated replay_manifest paths and exclusions as the only non-JSON values; correction2 returns sorted lists and reconstructs sets only at coverage comparisons, preserving semantics and the failed receipt.", "failed_witness_preserved": "EC6766-CORR2-N001", "prior_canonical_replayed": False, "correction2_success_pending": True},
    ]
    dump(CORRECTION / "method-flow-overlay.json", {"owner": "Elowen Cairn", "phase": "v676-v6-correction2", "base_phase_partition": {"methods": 658, "failed": 209, "passing": 449}, "correction_partition": {"methods": 2, "failed": 1, "passing": 1}, "current_phase_partition": {"methods": 660, "failed": 210, "passing": 450}, "methods": methods, "current_overlay": COUNTS, "failure_erasure_forbidden": True})
    dump(CORRECTION / "phase-truth.json", {"owner": "Elowen Cairn", "phase": "v676-v6-correction2", "correction1_final": CORRECTION1_FINAL, "failed_canonical_receipts": [{"stage": "original_final", "sha256": FAILED_ORIGINAL_SHA, "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "success_count": 0, "replay_count": 0}, {"stage": "correction1_final", "sha256": FAILED_CORRECTION1_SHA, "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "success_count": 0, "replay_count": 0}], "correction_scope": "manifest replay paths and exclusions: Python sets to sorted JSON lists, with set reconstruction only for comparisons", "expected_corrected_final": "bound by the ensuing additive direct-child commit and a distinct exclusive correction2-final receipt", "declared_proposal_chain": 7630, "core_outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}, "current_overlay": COUNTS, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "full_repository_suite_run": False, "independent_reproduction_claimed": False, "prior_finals_rewritten": False, "failed_receipts_rewritten": False})
    dump(CORRECTION / "validation-policy.json", {"correction1_final": CORRECTION1_FINAL, "failed_original_receipt_sha256": FAILED_ORIGINAL_SHA, "failed_correction1_receipt_sha256": FAILED_CORRECTION1_SHA, "replay_manifest_paths_serialization_before": "set", "replay_manifest_paths_serialization_after": "sorted_list", "coverage_comparison_domain": "set reconstructed at comparison only", "owner_test_timeout_seconds": 900, "prior_canonical_success_credit": 0, "prior_canonical_replay_forbidden": True, "complete_repository_suite_authorized": False})
    text(CORRECTION / "canonical-payload-serialization-correction.md", f"""
# Elowen Cairn v676-v6 additive canonical-payload serialization correction

The original canonical receipt `{FAILED_ORIGINAL_SHA}` and correction1 receipt `{FAILED_CORRECTION1_SHA}` remain immutable, invalid, and worth zero canonical success credit. Correction1 reached payload construction but `json.dumps` rejected manifest replay `paths` and `exclusions` because they were Python sets.

Correction2 changes only that representation: replay returns sorted JSON lists, while coverage checks reconstruct sets locally. It retains the 900-second test timeout and all topology, manifest, privacy, security, outcome, gap, gate, and authority boundaries. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

This is bounded same-owner software and documentation correction under shared infrastructure—not a full-repository suite, independent reproduction, empirical validation, professional certification, production readiness, legal or cultural ratification, Māori authority, complete privacy or accessibility assurance, exhaustive security, proof, canon, or Stage 20 authority.
""")
    seal_paths = [CORRECTION / "phase-truth.json", CORRECTION / "method-flow-overlay.json", CORRECTION / "validation-policy.json", CORRECTION / "canonical-payload-serialization-correction.md"]
    dump(CORRECTION / "content-seal.json", {"owner": "Elowen Cairn", "phase": "v676-v6-correction2", "normalization": "CRLF and CR normalized to LF before SHA-256", "entries": [{"path": path.relative_to(ROOT).as_posix(), "sha256_normalized_lf": sha(path)} for path in seal_paths], "self_excluded": "content-seal.json"})


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the additive corrected-head lifecycle-test selection for Elowen v676-v6."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v676-v6"
CORRECTION = BASE / "correction3"
CORRECTION2_FINAL = "674c21f98c115a24d057a71489b759f855b9b69f"
FAILED_RECEIPTS = [
    "95b95bb8c0be81a413e45f72bfe0204d9ed9c92e439f45bc0a50656539c0dbbf",
    "3dc85c6780d59715817f075fba0465ddbe2e21e32dc41c93eaba0ea9b603e09f",
    "1879b71dbc7fb4f5acf9dd7ca841ad927e5a32f1bc199b520dfd06d6f64af544",
]
COUNTS = {"effective_negatives": 42652, "effective_methods": 33780, "retained_failed_witnesses": 14313, "bounded_passing_witnesses": 20156, "open_gaps": 359, "exact_gates": 351}


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
    if git("rev-parse", "HEAD") != CORRECTION2_FINAL:
        raise SystemExit("correction3 builder requires correction2 final")
    methods = [
        {"method_id": "EC6766-CORR3-N001", "truth": False, "status": "failed_zero_credit", "description": "The sole correction2-final canonical invocation passed all 39 detailed checks but the owner-test subprocess exited one: two original-final current-tree tests asserted original-final manifest parity and three-commit topology against a later corrected head. The receipt remains invalid with zero success credit.", "receipt_sha256": FAILED_RECEIPTS[2], "invocation_count": 1, "success_count": 0, "replay_count": 0, "recovered_by": "EC6766-CORR3-P001"},
        {"method_id": "EC6766-CORR3-P001", "truth": True, "status": "bounded_pass", "description": "The full receipt and exact pytest last-failed cache identified only the two stale original-final assertions. Correction3 declares them lifecycle-only exclusions and validates original-final plus every correction manifest and direct-parent edge through explicit detailed checks.", "failed_witness_preserved": "EC6766-CORR3-N001", "failed_tests_replayed": False, "prior_canonical_replayed": False, "correction3_success_pending": True},
    ]
    dump(CORRECTION / "method-flow-overlay.json", {"owner": "Elowen Cairn", "phase": "v676-v6-correction3", "base_phase_partition": {"methods": 660, "failed": 210, "passing": 450}, "correction_partition": {"methods": 2, "failed": 1, "passing": 1}, "current_phase_partition": {"methods": 662, "failed": 211, "passing": 451}, "methods": methods, "current_overlay": COUNTS, "failure_erasure_forbidden": True})
    rows = [{"stage": stage, "sha256": digest, "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "success_count": 0, "replay_count": 0} for stage, digest in zip(("original_final", "correction1_final", "correction2_final"), FAILED_RECEIPTS, strict=True)]
    exclusions = ["test_final_delta_and_owner_manifests_have_exact_set_and_blob_parity", "test_lifecycle_is_direct_single_parent_and_merge_free"]
    dump(CORRECTION / "phase-truth.json", {"owner": "Elowen Cairn", "phase": "v676-v6-correction3", "correction2_final": CORRECTION2_FINAL, "failed_canonical_receipts": rows, "correction_scope": "declare two original-final-only tests as corrected-head lifecycle exclusions; preserve explicit detailed manifest and topology checks", "new_corrected_head_lifecycle_exclusions": exclusions, "expected_corrected_final": "bound by the ensuing additive direct-child commit and a distinct exclusive correction3-final receipt", "declared_proposal_chain": 7630, "core_outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}, "current_overlay": COUNTS, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "full_repository_suite_run": False, "independent_reproduction_claimed": False, "prior_finals_rewritten": False, "failed_receipts_rewritten": False})
    dump(CORRECTION / "validation-policy.json", {"correction2_final": CORRECTION2_FINAL, "failed_receipt_sha256s": FAILED_RECEIPTS, "existing_lifecycle_exclusions": ["test_no_x2_material_and_no_private_payload_in_x1_docs", "test_no_final_closeout_handoff_or_private_payload_exists_at_evidence"], "new_corrected_head_lifecycle_exclusions": exclusions, "replacement_evidence": ["original_final_delta_manifest_replay", "original_final_owner_manifest_replay", "correction1_delta_manifest_replay", "correction1_owner_manifest_replay", "correction2_delta_manifest_replay", "correction2_owner_manifest_replay", "correction3_delta_manifest_replay", "correction3_owner_manifest_replay", "six_phase_commits", "zero_merges", "one_final_parent"], "owner_test_timeout_seconds": 900, "prior_canonical_success_credit": 0, "prior_canonical_replay_forbidden": True, "complete_repository_suite_authorized": False})
    text(CORRECTION / "corrected-head-lifecycle-test-selection.md", f"""
# Elowen Cairn v676-v6 corrected-head lifecycle-test selection

The correction2-final canonical receipt `{FAILED_RECEIPTS[2]}` remains immutable and invalid with zero success credit. It passed all 39 detailed checks but its test subprocess retained two failures because original-final-only tests were executed against a later correction head.

Correction3 does not rewrite those tests or convert their failures into passes. It excludes them from corrected-head current-tree execution and replaces them with explicit Git-tree manifest replay and direct-parent topology checks spanning original final, correction1, correction2, and correction3. The two existing x1/evidence lifecycle exclusions remain unchanged. No proposal, outcome, mutation, gap, gate, authority boundary, or prior receipt changes. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""")
    seal_paths = [CORRECTION / "phase-truth.json", CORRECTION / "method-flow-overlay.json", CORRECTION / "validation-policy.json", CORRECTION / "corrected-head-lifecycle-test-selection.md"]
    dump(CORRECTION / "content-seal.json", {"owner": "Elowen Cairn", "phase": "v676-v6-correction3", "normalization": "CRLF and CR normalized to LF before SHA-256", "entries": [{"path": path.relative_to(ROOT).as_posix(), "sha256_normalized_lf": sha(path)} for path in seal_paths], "self_excluded": "content-seal.json"})


if __name__ == "__main__":
    main()

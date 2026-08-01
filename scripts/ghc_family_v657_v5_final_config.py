#!/usr/bin/env python3
"""Final lifecycle constants for Caelen Ash v657-v5."""

from __future__ import annotations


SOURCE_COMMIT = "1ae8aa07d6b0d5f74dc3c5b29615c79b908e235f"
X1_COMMIT = "7fdae81a188decacbee20c2f2c283b7104c0e91a"
EVIDENCE_COMMIT = "e2f0f3535f968e26fab748385c950cf4b7de085a"
CLOSEOUT_COMMIT = "7f68e945166e6bfb0680a1be83e935513b9768f4"
CLOSEOUT_EFFECTIVE_NEGATIVES = 15965
CLOSEOUT_EFFECTIVE_METHODS = 2241
OPEN_GAPS = 109
EXACT_GATES = 108

FINAL_PREPARATION_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6575-FINAL-N01",
        "slug": "premature-final-test-before-manifest-build",
        "failure_signature": "The final artifact-packet test ran before final-owner-manifest.json had been materialized and failed one of thirteen bounded tests.",
        "candidate_workaround": "Build the final receipt, cap, privacy, and owner-manifest layer before invoking the final and successor-scope modules.",
        "recurrence_guard": "Do not run the final artifact-packet test between the record builder and the receipt builder.",
        "fail_procedure": "Invoke the final and successor-scope modules immediately after the record builder but before the final receipt builder.",
        "fail_observed": "Twelve tests passed and test_final_artifact_packet_exists failed because the prospective final manifest did not yet exist; the attempt earned zero credit.",
        "pass_procedure": "Rebuild the candidate with this failure retained, materialize final receipts and the manifest, then invoke the bounded tests.",
        "pass_observed": "Acceptance is reserved for the post-receipt test run and exact staged review; the premature failure remains retained.",
        "scope_boundary": "Owner-local final-candidate lifecycle ordering only.",
    },
]

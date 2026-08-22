from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_sable_rook_v666_v6_runtime import PHASE_ROOT, X1_SHA, load_json, replay_manifest  # noqa: E402


EVIDENCE_SHA = "f5a211e484e2d1b252c16de7800e568160ae902b"


def load(relative: str) -> dict:
    return load_json(PHASE_ROOT / relative)


class SableRookV666V6CloseoutTests(unittest.TestCase):
    def test_phase_truth_reconciles_exactly(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["proposal_chain_total"], 4290)
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 26758)
        self.assertEqual(truth["effective_methods"], 11645)
        self.assertEqual(truth["open_gaps"], 188)
        self.assertEqual(truth["exact_gates"], 186)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["same_owner_validation_is_independent_reproduction"])

    def test_retained_negative_register_has_no_erasure(self) -> None:
        register = load("closeout/retained-negative-register.json")
        self.assertEqual(sum(row["negative_count"] for row in register["categories"]), 26758)
        self.assertEqual(sum(row["method_count"] for row in register["categories"]), 11645)
        self.assertEqual(len(register["operational_rows"]), 9)
        self.assertTrue(register["all_failures_retained"])
        self.assertFalse(register["failed_witness_converted_to_pass"])
        self.assertFalse(register["predecessor_seal_rewritten"])

    def test_gaps_and_gates_remain_open(self) -> None:
        register = load("closeout/exact-open-gate-register.json")
        self.assertEqual(register["effective_open_gaps"], 188)
        self.assertEqual(register["effective_exact_gates"], 186)
        self.assertEqual(len(register["new_open_gaps"]), 1)
        self.assertEqual(len(register["new_exact_gates"]), 1)
        self.assertEqual(register["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_x1_and_evidence_manifests_replay(self) -> None:
        x1 = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
        evidence = replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", EVIDENCE_SHA)
        self.assertEqual(x1["entry_count"], 20)
        self.assertEqual(evidence["entry_count"], 166)
        self.assertTrue(x1["valid"])
        self.assertTrue(evidence["valid"])

    def test_immutable_evidence_has_no_closeout_paths(self) -> None:
        for relative in ("closeout", "final", "handoffs", "orchestration"):
            output = subprocess.check_output(
                ["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", EVIDENCE_SHA, "--", f"docs/sable-rook/v666-v6/{relative}"]
            ).decode("utf-8")
            self.assertEqual(output, "", relative)

    def test_final_manifests_are_exact_index_bound_structures(self) -> None:
        review = load("validation/final-staged-review.json")
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        self.assertTrue(review["valid"])
        self.assertGreaterEqual(delta["entry_count"], 15)
        self.assertEqual(owner["entry_count"] + 1, owner["exact_final_owner_count_including_self"])
        self.assertEqual(owner["exact_final_owner_count_including_self"], review["exact_final_owner_count"])
        self.assertLessEqual(review["exact_final_owner_count"], 2000)
        self.assertTrue(owner["within_file_ceiling"])
        for manifest in (delta, owner):
            for row in manifest["entries"]:
                self.assertRegex(row["git_blob_oid"], r"^[0-9a-f]{40}$")
                self.assertRegex(row["sha256"], r"^[0-9a-f]{64}$")
                self.assertGreater(row["size_bytes"], 0)

    def test_final_staged_review_preserves_immutability_and_privacy(self) -> None:
        review = load("validation/final-staged-review.json")
        self.assertTrue(review["checks"]["immutable_x1_x2_evidence_deck_skills_unchanged"])
        self.assertTrue(review["checks"]["five_class_scan_zero_confirmed_hits"])
        self.assertTrue(review["checks"]["bounded_changed_python_security_zero_findings"])
        self.assertEqual(review["privacy_confirmed_hits"], 0)
        self.assertEqual(review["changed_python_security_findings"], [])

    def test_route_is_prepared_not_sent(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        receipt = load("handoffs/next-owner-activation-candidate-receipt.json")
        self.assertEqual(route["route"], "PREPARED_NOT_SENT")
        self.assertFalse(route["resolved_live"])
        self.assertFalse(route["recipient_reread"])
        self.assertFalse(route["successor_contacted"])
        self.assertTrue(receipt["prepared"])
        self.assertFalse(receipt["sent"])
        self.assertFalse(receipt["task_created"])
        self.assertFalse(receipt["task_forked"])
        self.assertFalse(receipt["subagent_spawned"])

    def test_baton_is_sanitized_and_bounded(self) -> None:
        baton = (PHASE_ROOT / "handoffs" / "next-owner-activation-candidate.md").read_text(encoding="utf-8")
        for token in (
            "PREPARED NOT SENT",
            "next authorized owner",
            "v666-v6",
            EVIDENCE_SHA,
            "NOT_READY_FOR_STAGE_20",
            "relational working language only",
            "SENT_BY_SABLE_ROOK = false",
        ):
            self.assertIn(token, baton)
        self.assertNotRegex(baton, r"(?i)[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}")
        self.assertNotRegex(baton, r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)")

    def test_canonical_protocol_is_one_shot_and_not_invoked(self) -> None:
        protocol = load("validation/canonical-validation-protocol.json")
        prereq = load("final/final-validation-prerequisites.json")
        candidate = load("final/terminal-candidate.json")
        self.assertTrue(protocol["one_successful_invocation_only"])
        self.assertTrue(protocol["post_success_replay_forbidden"])
        self.assertFalse(protocol["full_repository_suite"])
        self.assertFalse(prereq["canonical_invoked"])
        self.assertFalse(candidate["canonical_invoked"])
        self.assertFalse(candidate["successor_contacted"])

    def test_final_delta_is_additive_direct_child_candidate(self) -> None:
        anchor = load("lifecycle/phase-anchor-contract.json")
        delta = load("validation/final-delta-manifest.json")
        self.assertEqual(anchor["expected_final_parent"], EVIDENCE_SHA)
        self.assertEqual(anchor["expected_new_commit_count"], 3)
        self.assertEqual(anchor["expected_merge_count"], 0)
        self.assertTrue(anchor["x1_and_evidence_immutable"])
        self.assertTrue(delta["additive_only"])
        self.assertEqual(delta["deletion_count"], 0)

    def test_closeout_json_is_utf8_lf_parseable(self) -> None:
        roots = ["closeout", "final", "handoffs", "lifecycle", "orchestration", "validation"]
        paths = sorted({path for root in roots for path in (PHASE_ROOT / root).glob("*.json")})
        self.assertGreaterEqual(len(paths), 12)
        for path in paths:
            raw = path.read_bytes()
            self.assertNotIn(b"\r", raw)
            json.loads(raw.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()

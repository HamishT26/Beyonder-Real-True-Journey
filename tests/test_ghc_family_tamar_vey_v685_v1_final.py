#!/usr/bin/env python3
"""Precommit and exact-final closeout tests for Tamar Vey v685-v1."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "tamar-vey" / "v685-v1"
FINAL = BASE / "final"
VALIDATION = BASE / "validation"
SEAL = BASE / "seal"
SOURCE = "f138d0e9fd37d424a81887bb7a1bafa3eacba860"
X1 = "a640f907d154d6b5c7747c990a3c0b1d6fe987eb"
EVIDENCE = "9484532c6e45c6b3c87d068e06213dc4260cd7e1"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    proc = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        raise AssertionError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout


class TamarVeyV685V1FinalTests(unittest.TestCase):
    def test_phase_truth_and_outcomes(self):
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(truth["source"], SOURCE)
        self.assertEqual(truth["x1"], X1)
        self.assertEqual(truth["evidence"], EVIDENCE)
        self.assertEqual(truth["proposal_chain_after"], 11270)
        self.assertEqual(truth["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(truth["real_rows"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_method_flow_and_negative_arithmetic(self):
        flow = load(FINAL / "method-flow-final.json")
        counts = flow["effective_final_counts"]
        self.assertEqual(counts["effective_negatives"], 61063)
        self.assertEqual(counts["effective_methods"], 76658)
        self.assertEqual(counts["failed_witnesses"], 32124)
        self.assertEqual(counts["bounded_passing_witnesses"], 57193)
        self.assertEqual(counts["open_gaps"], 543)
        self.assertEqual(counts["exact_gates"], 533)
        self.assertEqual(flow["closeout_operational_failure_count"], 4)
        self.assertFalse(flow["failure_erasure"])
        register = load(FINAL / "retained-negative-register.json")
        self.assertEqual(sum(register["categories"].values()), 61063)
        self.assertEqual(register["effective_negative_total"], 61063)

    def test_open_and_exact_gates_remain_open(self):
        gaps = load(FINAL / "open-gap-register.json")
        gates = load(FINAL / "exact-gate-register.json")
        self.assertEqual(gaps["effective_count"], 543)
        self.assertEqual(gates["effective_count"], 533)
        self.assertEqual(gaps["silently_closed_count"], 0)
        self.assertEqual(gates["silently_closed_count"], 0)
        self.assertEqual(len(gaps["phase_new"]), 3)
        self.assertEqual(len(gates["phase_new"]), 3)

    def test_complete_incomplete_and_prepared_route(self):
        checklist = load(FINAL / "complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["complete"]), 9)
        self.assertGreaterEqual(len(checklist["incomplete"]), 8)
        candidate = (BASE / "handoffs" / "elowen-cairn-v685-v2-activation-candidate.md").read_text(encoding="utf-8")
        self.assertIn("SENT_BY_TAMAR_VEY = false", candidate)
        self.assertIn("DELIVERY_STATE = PREPARED_NOT_SENT", candidate)
        self.assertIn("Elowen Cairn", candidate)
        self.assertIn("v725-v8", candidate)

    def test_lifecycle_replay_precommit_boundary(self):
        replay = load(FINAL / "lifecycle-replay.json")
        self.assertEqual(replay["expected_phase_commit_count"], 3)
        self.assertEqual(replay["expected_merge_count"], 0)
        self.assertTrue(replay["strict_x1_before_x2"])
        self.assertEqual(git("rev-parse", f"{X1}^").decode().strip(), SOURCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^").decode().strip(), X1)
        head = git("rev-parse", "HEAD").decode().strip()
        if head == EVIDENCE:
            self.assertEqual(head, EVIDENCE)
        else:
            self.assertEqual(git("rev-parse", "HEAD^").decode().strip(), EVIDENCE)
            self.assertEqual(int(git("rev-list", "--count", f"{SOURCE}..HEAD").decode().strip()), 3)

    def test_final_delta_manifest_replays_index(self):
        manifest = load(VALIDATION / "final-delta-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["declared_self_exclusions"]), 5)
        for entry in manifest["entries"]:
            data = git("show", f":{entry['path']}")
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_final_owner_manifest_replays_index(self):
        manifest = load(VALIDATION / "final-owner-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertGreater(manifest["entry_count"], 90)
        for entry in manifest["entries"]:
            data = git("show", f":{entry['path']}")
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_final_staged_review_and_privacy(self):
        review = load(VALIDATION / "final-staged-review.json")
        privacy = load(VALIDATION / "final-privacy-adjudication.json")
        delta = load(VALIDATION / "final-delta-manifest.json")
        self.assertEqual(set(review["expected_paths"]), {
            row["path"] for row in delta["entries"]
        } | set(delta["declared_self_exclusions"]))
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["deletions"], [])
        self.assertEqual(review["outside_owner_paths"], [])
        self.assertEqual(review["x1_or_x2_mutations"], [])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)

    def test_content_seal_replays_index(self):
        seal = load(SEAL / "content-seal.json")
        self.assertEqual(seal["target_count"], 10)
        self.assertEqual(seal["prepared_successor_state"], "PREPARED_NOT_SENT")
        self.assertFalse(seal["canonical_result_included"])
        for entry in seal["targets"]:
            data = git("show", f":{entry['path']}")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_final_overview_is_three_page_equivalent(self):
        overview = (FINAL / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1500)
        for term in ("THOS Body", "GMUT Mind", "Freed ID", "CBR", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(term, overview)

    def test_environment_receipt_is_verify_only(self):
        receipt = load(FINAL / "environment-version-receipt.json")
        self.assertTrue(receipt["verified_only_no_updates"])
        self.assertFalse(receipt["codex_desktop_updated"])
        self.assertFalse(receipt["privilege_elevation"])
        self.assertFalse(receipt["host_security_weakened"])
        self.assertFalse(receipt["windows_features_changed"])
        self.assertFalse(receipt["rebooted"])

    def test_evidence_closeout_scope(self):
        receipt = load(FINAL / "evidence-closeout.json")
        self.assertEqual(receipt["x1_tests"], 10)
        self.assertEqual(receipt["x2_tests_attributable"], 12)
        self.assertEqual(receipt["mutations_rejected"], 300)
        self.assertEqual(receipt["skills_quick_validated_read_and_smoked"], 20)
        self.assertEqual(receipt["runners_accepting_and_rejecting_smoked"], 10)
        self.assertEqual(receipt["source_rows"], 0)
        self.assertFalse(receipt["independent_reproduction"])
        self.assertFalse(receipt["full_repository_suite"])


if __name__ == "__main__":
    unittest.main()

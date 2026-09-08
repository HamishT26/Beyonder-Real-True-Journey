#!/usr/bin/env python3
"""Owner-scoped final-candidate tests for Sylven Arc v688-v7."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/sylven-arc/v688-v7"
FINAL = BASE / "final"
SOURCE = "e7db6f3be1327de72f93873eb6540aabfc773344"
X1 = "4b7459cdf681726b8d411d644dc6f8db70e83871"
X2 = "3c968db9391583a9e40f0eb8cc0c2f86d9997126"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestSylvenArcV688V7Final(unittest.TestCase):
    def test_01_exact_anchors(self):
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual((truth["source"], truth["x1"], truth["evidence"]), (SOURCE, X1, X2))
        self.assertIsNone(truth["final"])

    def test_02_final_truth_counts(self):
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(truth["effective_counts"], {"proposals": 16830, "negatives": 85419, "methods": 94119, "failed_witnesses": 56297, "passing_witnesses": 86182, "open_gaps": 765, "exact_gates": 785})

    def test_03_outcome_vocabulary_and_counts(self):
        self.assertEqual(load(FINAL / "phase-truth.json")["outcomes"], {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10})

    def test_04_phase_method_counts(self):
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual((truth["phase_methods"], truth["phase_witnesses"], truth["phase_failed_witnesses"], truth["phase_passing_witnesses"]), (57, 617, 545, 72))

    def test_05_method_ids_and_witness_ids_are_unique(self):
        final = load(FINAL / "method-flow-final.json")
        self.assertEqual(len(final["method_ids"]), len(set(final["method_ids"])))
        self.assertEqual(len(final["witness_ids"]), len(set(final["witness_ids"])))
        self.assertEqual((len(final["method_ids"]), len(final["witness_ids"])), (57, 617))

    def test_06_closeout_overlay_preserves_failure(self):
        overlay = load(FINAL / "method-flow-closeout-overlay.json")
        self.assertEqual(overlay["overlay_counts"], {"methods": 1, "witnesses": 2, "failed_witnesses": 1, "passing_witnesses": 1, "state_events": 1, "recommendations": 1})
        self.assertEqual(overlay["failed_witnesses_erased"], 0)
        self.assertEqual(overlay["witnesses"][0]["result"], "fail")

    def test_07_retained_negative_accounting(self):
        receipt = load(FINAL / "retained-negative-register.json")
        self.assertEqual((receipt["inherited"], receipt["phase_unique"], receipt["effective"]), (84904, 515, 85419))
        self.assertEqual(receipt["erased"], 0)

    def test_08_open_and_exact_gates(self):
        receipt = load(FINAL / "open-exact-gate-register.json")
        self.assertEqual(receipt["open_gaps"]["effective"], 765)
        self.assertEqual(receipt["exact_gates"]["effective"], 785)
        self.assertEqual((receipt["exact_packets_unexecuted"], receipt["blocked_packets_unexecuted"]), (50, 30))

    def test_09_package_receipt_is_bounded(self):
        receipt = load(FINAL / "environment-and-package-receipt.json")
        self.assertEqual([item["name"] for item in receipt["direct_packages"]], ["chess", "lark", "networkx"])
        self.assertFalse(receipt["global_python_mutated"])
        self.assertFalse(receipt["exhaustive_security"])

    def test_10_tool_promotion_no_overwrite(self):
        receipt = load(FINAL / "tool-promotion-receipt.json")
        self.assertEqual((receipt["skills"], receipt["runner_interfaces"]), (10, 5))
        self.assertEqual(receipt["overwrites"], 0)
        self.assertEqual((receipt["local_accepting_smokes"], receipt["local_adverse_smokes"]), (40, 40))
        self.assertEqual((receipt["promoted_accepting_smokes"], receipt["promoted_adverse_smokes"]), (40, 40))

    def test_11_four_tier_deck_summary(self):
        receipt = load(FINAL / "four-tier-deck-summary.json")
        self.assertEqual(receipt["effective_card_count"], 264)
        self.assertEqual(receipt["tier_counts"], {"1": 1, "2": 3, "3": 4, "4": 256})
        self.assertTrue(receipt["content_addressed"] and receipt["parent_graph_acyclic"])

    def test_12_integrated_overview_is_three_page_equivalent(self):
        text = (FINAL / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 2200)
        self.assertGreaterEqual(len(re.findall(r"^## ", text, re.MULTILINE)), 8)

    def test_13_baton_budget_modules_and_hash(self):
        index = load(FINAL / "baton-index.json")
        baton = ROOT / index["path"]
        text = baton.read_text(encoding="utf-8")
        self.assertEqual(len(text.split()), index["word_count"])
        self.assertTrue(10000 <= index["word_count"] <= 100000)
        self.assertEqual(len(re.findall(r"^## Module \d\d", text, re.MULTILINE)), 13)
        self.assertEqual(hashlib.sha256(baton.read_bytes()).hexdigest(), index["sha256"])

    def test_14_accessible_report_structure(self):
        text = (FINAL / "accessible-final-report.html").read_text(encoding="utf-8")
        for token in ("<header>", "<main>", "<h1>", "<table>", "<caption>", 'scope="col"', 'scope="row"', "assistive-technology", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, text)

    def test_15_content_seal_replays(self):
        seal = load(BASE / "seal/content-seal.json")
        for item in seal["targets"]:
            path = ROOT / item["path"]
            self.assertEqual(len(path.read_bytes()), item["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])

    def test_16_canonical_policy_is_one_shot(self):
        policy = load(FINAL / "canonical-policy.json")
        self.assertFalse(policy["post_success_replay"])
        self.assertFalse(policy["full_repository_suite"])
        self.assertEqual([item["expected_tests"] for item in policy["test_modules"]], [12, 24, 20])

    def test_17_lifecycle_is_direct_parent_only(self):
        lifecycle = load(FINAL / "lifecycle-replay.json")
        self.assertEqual(lifecycle["expected_phase_commit_count"], 3)
        self.assertEqual(lifecycle["expected_merges"], 0)
        self.assertEqual(lifecycle["expected_direct_parent_chain"][:2], [{"child": X1, "parent": SOURCE}, {"child": X2, "parent": X1}])

    def test_18_future_seat_route_preserves_self_choice(self):
        route = load(FINAL / "terminal-route-checklist.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["prospective_target"], "future seat 14")
        self.assertEqual(route["identity_assignment"], "self_chosen_after_creation")
        self.assertFalse(route["creation_if_absent"]["preassigned_name"])
        self.assertEqual(route["sends_or_creations_already_made"], 0)

    def test_19_terminal_and_authority_boundaries_hold(self):
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual((truth["canonical_invocations"], truth["canonical_successes"], truth["canonical_replays"]), (0, 0, 0))
        self.assertEqual((truth["successor_contacts"], truth["new_tasks_created"], truth["subagents"], truth["forks"]), (0, 0, 0, 0))

    def test_20_baton_contains_no_raw_task_identifier_or_private_path(self):
        index = load(FINAL / "baton-index.json")
        text = (ROOT / index["path"]).read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", text, re.I))
        self.assertNotRegex(text, r"[A-Za-z]:\\Users\\")
        self.assertNotIn("threadId", text)


if __name__ == "__main__":
    unittest.main()

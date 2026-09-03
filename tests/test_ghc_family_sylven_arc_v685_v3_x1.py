#!/usr/bin/env python3
"""Lifecycle-correct tests for Sylven Arc v685-v3 planning-only x1."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sylven-arc" / "v685-v3"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    proc = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if check and proc.returncode:
        raise AssertionError(proc.stderr.decode("utf-8", "replace"))
    return proc


class SylvenArcV685V3X1Tests(unittest.TestCase):
    def test_phase_truth_is_planning_only(self):
        truth = load(X1 / "phase-truth.json")
        self.assertEqual(truth["lifecycle"], "PLANNING_ONLY_X1")
        self.assertEqual(truth["proposal_count"], 60)
        self.assertEqual(truth["observed_outcome_count"], 0)
        self.assertFalse(truth["x2_implementation_present"])
        self.assertEqual(
            truth["expected_disposition_counts"],
            {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12},
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_proposals_are_complete_and_unique(self):
        freeze = load(X1 / "new-proposal-freeze.json")
        rows = freeze["proposals"]
        self.assertEqual(len(rows), 60)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 60)
        self.assertEqual(len({row["title"].casefold() for row in rows}), 60)
        required = {
            "proposal_id",
            "title",
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
            "preregistered_rejecting_mutations",
        }
        for row in rows:
            self.assertTrue(required <= set(row))
            self.assertEqual(len(row["preregistered_rejecting_mutations"]), 5)
            self.assertEqual(
                {item["expected_result"] for item in row["preregistered_rejecting_mutations"]},
                {"rejected_zero_credit"},
            )
        self.assertEqual(
            Counter(row["expected_disposition"] for row in rows),
            Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}),
        )

    def test_source_bounded_novelty_audit_passes(self):
        audit = load(X1 / "proposal-chain-audit.json")
        self.assertEqual(audit["new_proposal_count"], 60)
        self.assertEqual(audit["declared_chain_before"], 11330)
        self.assertEqual(audit["declared_chain_after_if_committed"], 11390)
        self.assertEqual(audit["exact_title_collisions"], [])
        self.assertEqual(audit["quarantined_neighbors"], [])
        self.assertLess(audit["maximum_neighbor_score"], 0.78)
        self.assertFalse(audit["audit_scope"]["universal_11330_row_materialization_claimed"])
        self.assertEqual(len(audit["neighbor_reviews"]), 60)

    def test_inherited_reviews_are_zero_credit(self):
        freeze = load(X1 / "inherited-revalidation-freeze.json")
        self.assertEqual(freeze["review_count"], 60)
        self.assertEqual(len(freeze["reviews"]), 60)
        self.assertEqual(freeze["credit"], "zero_inherited_novelty_execution_and_completion_credit")
        self.assertEqual({row["inherited_credit"] for row in freeze["reviews"]}, {"zero"})

    def test_portfolio_floors_and_holds(self):
        portfolio = load(X1 / "portfolio-freeze.json")
        expected = {
            "safe_now": 120,
            "owner_candidates": 80,
            "successor_candidates": 20,
            "owner_skill_ideas": 20,
            "owner_runner_ideas": 10,
            "successor_skill_ideas": 10,
            "successor_runner_ideas": 10,
            "owner_clean_fix_refine": 100,
            "successor_clean_fix_refine": 30,
            "exact_approval": 20,
            "blocked": 10,
        }
        for key, count in expected.items():
            self.assertEqual(len(portfolio[key]), count, key)
        self.assertEqual(portfolio["commit_cap"], {"total": 3, "x1": 1, "x2": 2})
        self.assertTrue(portfolio["caps_are_ceilings"])
        holds = load(X1 / "approval-hold-register.json")
        self.assertEqual(holds["executed_count"], 0)

    def test_method_flow_preserves_all_startup_failures(self):
        ledger = load(X1 / "method-flow-startup.json")
        self.assertEqual(ledger["new_failure_count"], 12)
        self.assertEqual(len(ledger["new_failures"]), 12)
        self.assertFalse(ledger["failure_erasure"])
        self.assertFalse(ledger["recoveries_promote_failed_witnesses"])
        counts = ledger["effective_x1_startup_counts"]
        self.assertEqual(counts["effective_negatives"], 61432)
        self.assertEqual(counts["effective_methods"], 77417)
        self.assertEqual(counts["failed_witnesses"], 32493)
        self.assertEqual(counts["bounded_passing_witnesses"], 57952)
        self.assertEqual(counts["open_gaps"], 546)
        self.assertEqual(counts["exact_gates"], 536)

    def test_sources_are_vocabulary_only_and_zero_row(self):
        ledger = load(X1 / "official-primary-source-ledger.json")
        self.assertEqual(ledger["source_count"], 11)
        self.assertEqual(ledger["network_rows_ingested"], 0)
        self.assertEqual({row["observation_credit"] for row in ledger["sources"]}, {"zero"})
        self.assertEqual({row["authority_credit"] for row in ledger["sources"]}, {"zero"})

    def test_flashcards_are_content_addressed_navigation_only(self):
        freeze = load(X1 / "flashcard-freeze.json")
        self.assertEqual(freeze["card_count"], 67)
        self.assertFalse(freeze["mutation_or_outcome_present"])
        for card in freeze["cards"]:
            copy = dict(card)
            digest = copy.pop("sha256")
            expected = hashlib.sha256(
                json.dumps(copy, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
            ).hexdigest()
            self.assertEqual(digest, expected)
            self.assertEqual(card["credit_boundary"], "navigation_only_not_authority_or_completion")

    def test_validation_receipts_and_index_manifest(self):
        manifest = load(VALIDATION / "x1-index-manifest.json")
        review = load(VALIDATION / "x1-staged-review.json")
        privacy = load(VALIDATION / "x1-privacy-adjudication.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["declared_self_exclusions"]), 3)
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["x2_paths"], [])
        self.assertTrue(review["planning_only"])
        self.assertEqual(review["expected_path_count"], len(review["expected_paths"]))
        self.assertEqual(set(review["expected_paths"]), {
            entry["path"] for entry in manifest["entries"]
        } | set(manifest["declared_self_exclusions"]))
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        for entry in manifest["entries"]:
            proc = git("show", f":{entry['path']}")
            self.assertEqual(hashlib.sha256(proc.stdout).hexdigest(), entry["sha256"])
            self.assertEqual(len(proc.stdout), entry["bytes"])
            mode = git("ls-files", "-s", "--", entry["path"]).stdout.decode().split()[0]
            self.assertEqual(mode, entry["mode"])

    def test_no_x2_materialization_or_observed_outcome(self):
        review = load(VALIDATION / "x1-staged-review.json")
        for path in review["expected_paths"]:
            self.assertNotIn("/x2/", path)
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(X1.glob("*"))
            if path.suffix in {".json", ".md"}
        )
        self.assertNotIn('"observed_outcome_count": 60', text)


if __name__ == "__main__":
    unittest.main()

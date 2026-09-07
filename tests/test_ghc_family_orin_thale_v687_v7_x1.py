#!/usr/bin/env python3
"""Planning-only x1 tests for Orin Thale v687-v7."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
X1 = PHASE / "x1"
VALIDATION = PHASE / "validation"
SOURCE = "28dfdf1a3e9a1023f1e83f19fb267e57878b9d0b"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def norm(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class OrinThaleV687V7X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.truth = load(X1 / "phase-truth.json")
        cls.proposals = load(X1 / "new-proposals.json")
        cls.portfolio = load(X1 / "portfolio-plan.json")
        cls.manifest = load(VALIDATION / "x1-manifest.json")

    def test_builder_runs_at_source_before_commit(self):
        self.assertEqual(git("rev-parse", "HEAD"), SOURCE)

    def test_planning_only_boundary(self):
        self.assertEqual(self.truth["state"], "PLANNING_ONLY_X1")
        self.assertFalse(self.truth["x2_started"])
        self.assertIsNone(self.truth["observed_outcomes"])
        self.assertEqual(set(self.truth["expected_outcomes"]), LABELS)
        self.assertEqual(self.truth["canonical_state"], "NOT_INVOKED")

    def test_proposals_and_chain(self):
        rows = self.proposals["proposals"]
        self.assertEqual(len(rows), 200)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 200)
        self.assertEqual(self.proposals["chain_before"], 15030)
        self.assertEqual(self.proposals["chain_after"], 15230)
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_primary_source_need", "concrete_artifact", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertTrue(all(required <= set(row) for row in rows))

    def test_expected_outcome_arithmetic(self):
        counts = {label: 0 for label in LABELS}
        for row in self.proposals["proposals"]:
            counts[row["expected_disposition"]] += 1
        self.assertEqual(counts, {"completed": 125, "represented": 39, "open_gap": 20, "exact_gate": 16})

    def test_inherited_review_zero_credit(self):
        review = load(X1 / "inherited-review.json")
        self.assertEqual(review["count"], 200)
        self.assertEqual(review["new_owner_credit"], 0)
        self.assertTrue(all(row["reviewed"] and row["new_owner_credit"] == 0 for row in review["rows"]))

    def test_mutation_plan(self):
        plan = load(X1 / "mutation-plan.json")
        self.assertEqual(plan["count"], 1000)
        self.assertEqual(plan["per_proposal"], 5)
        self.assertEqual(len({row["mutation_id"] for row in plan["rows"]}), 1000)
        self.assertTrue(all(row["original_success_credit"] == 0 for row in plan["rows"]))

    def test_portfolio_profile(self):
        self.assertEqual(len(self.portfolio["safe_now"]), 300)
        self.assertEqual(len(self.portfolio["candidates"]), 250)
        self.assertEqual(len(self.portfolio["clean_fix_refine"]), 300)
        self.assertEqual(len(self.portfolio["exact_packets"]), 50)
        self.assertEqual(len(self.portfolio["blocked_packets"]), 30)
        self.assertFalse(self.portfolio["destructive_cleanup_planned"])
        self.assertTrue(all(row["state"] == "held_unexecuted" for row in self.portfolio["exact_packets"] + self.portfolio["blocked_packets"]))
        receipt = load(VALIDATION / "x1-release-profile-validation.json")
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["execution_credit"], 0)

    def test_skill_runner_and_successor_floors(self):
        plan = load(X1 / "skill-runner-plan.json")
        ideas = load(X1 / "successor-ideas.json")
        self.assertEqual(len(plan["skills"]), 10)
        self.assertEqual(len(plan["runners"]), 5)
        self.assertEqual(len(ideas["skill_ideas"]), 10)
        self.assertEqual(len(ideas["runner_ideas"]), 10)
        self.assertEqual(ideas["successor"], "future-sibling-10-self-chosen")

    def test_package_plan(self):
        plan = load(X1 / "package-plan.json")
        self.assertTrue(plan["planning_only"])
        self.assertEqual([(row["name"], row["version"]) for row in plan["packages"]], [("astropy", "8.0.1"), ("asdf", "5.4.0"), ("uncertainties", "3.2.3")])
        self.assertTrue(all(len(row["sha256"]) == 64 for row in plan["packages"]))

    def test_method_flow_retains_startup_failures(self):
        ledger = load(X1 / "method-flow" / "ledger.json")
        self.assertEqual(ledger["counts"], {"methods": 15, "witnesses": 30, "failed_witnesses": 15, "passing_witnesses": 15})
        self.assertEqual(len({n for row in ledger["methods"] for n in row["retained_negative_ids"]}), 15)
        self.assertEqual(sum(w["result"] == "fail" for w in ledger["witnesses"]), 15)
        self.assertEqual(sum(w["result"] == "pass" for w in ledger["witnesses"]), 15)

    def test_novelty_review_is_bounded(self):
        review = load(X1 / "novelty-review.json")
        self.assertEqual(review["quarantined"], 0)
        self.assertLess(review["max_score"], review["threshold"])
        self.assertIn("no universal novelty proof", review["scope"])

    def test_route_is_held(self):
        route = load(X1 / "route-plan.json")
        self.assertEqual(route["next_owner_placeholder"], "future-sibling-10-self-chosen")
        self.assertEqual(route["next_phase"], "v687-v8")
        self.assertFalse(route["precontacted"])
        self.assertEqual(route["message_count"], 0)

    def test_privacy_and_manifest(self):
        privacy = load(VALIDATION / "x1-privacy.json")
        self.assertEqual(privacy["confirmed_count"], 0)
        exclusions = set(self.manifest["declared_self_exclusions"])
        actual = exclusions.copy()
        for entry in self.manifest["entries"]:
            data = norm(ROOT / entry["path"])
            self.assertEqual(len(data), entry["bytes_normalized_lf"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"], entry["path"])
            actual.add(entry["path"])
        staged = load(VALIDATION / "x1-staged-review.json")
        self.assertEqual(actual, set(staged["expected_paths"]))

    def test_caps_and_boundaries(self):
        contract = load(X1 / "validation-contract.json")
        self.assertEqual(contract["owner_file_cap"], 1999)
        self.assertEqual(contract["commit_caps"], {"x1": 5, "x2": 5, "total": 8})
        self.assertFalse(contract["full_repository_suite"])
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "orin-thale" / "v674-v4" / "x1"
SOURCE_FINAL = "dcdc2921b193516242c93e6ef303f854e9d21264"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class OrinV674V4X1Tests(unittest.TestCase):
    def test_head_is_exact_source_before_x1_commit(self):
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
        self.assertEqual(head, SOURCE_FINAL)

    def test_x2_is_absent_and_route_is_held(self):
        self.assertFalse((REPO / "docs" / "orin-thale" / "v674-v4" / "x2").exists())
        route = load("terminal-route-hold.json")
        self.assertFalse(route["successor_contacted"])
        self.assertEqual(route["state"], "HOLD_UNTIL_OWNER_EXACT_FINAL")

    def test_sixty_new_proposals_and_exact_expected_distribution(self):
        freeze = load("proposals/new-proposal-freeze.json")
        rows = freeze["proposals"]
        self.assertEqual(len(rows), 60)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 60)
        self.assertEqual(len({row["title"] for row in rows}), 60)
        self.assertEqual(
            Counter(row["expected_disposition"] for row in rows),
            Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}),
        )
        self.assertEqual(freeze["planned_chain_rows"], 6790)

    def test_proposal_contracts_are_complete_and_planning_only(self):
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "official_or_primary_source_need",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for row in load("proposals/new-proposal-freeze.json")["proposals"]:
            self.assertTrue(required.issubset(row))
            self.assertEqual(row["x1_state"], "preregistered_not_executed")
            self.assertIsNone(row["observed_outcome"])
            self.assertEqual(row["execution_credit"], 0)
            self.assertEqual(row["expected_disposition_count"], 1)
            self.assertIn(row["expected_disposition"], ALLOWED)

    def test_materialized_neighbor_audit_passes_without_universal_claim(self):
        audit = load("proposals/semantic-neighbor-audit.json")
        self.assertEqual(audit["status"], "passed_bounded_reachable_audit")
        self.assertFalse(audit["universal_novelty_claim"])
        self.assertEqual(audit["exact_collisions"], [])
        self.assertEqual(audit["near_neighbors_at_or_above_threshold"], [])
        self.assertGreater(audit["reachable_proposal_json_paths_examined"], 0)

    def test_inherited_reviews_are_zero_credit(self):
        review = load("proposals/inherited-source-review.json")
        self.assertEqual(review["row_count"], 60)
        for row in review["rows"]:
            self.assertEqual(row["novelty_credit"], 0)
            self.assertEqual(row["execution_credit"], 0)
            self.assertEqual(row["completion_credit"], 0)

    def test_portfolio_floors_are_frozen_but_not_executed(self):
        portfolio = load("portfolios/portfolio-freeze.json")
        expected = {
            "safe_now": 120,
            "candidates": 80,
            "exact_approval_packets": 20,
            "blocked_packets": 10,
            "phase_local_skills": 20,
            "family_current_runners": 10,
            "clean_fix_refine": 100,
            "rejecting_mutations": 240,
            "successor_recommendations": 60,
        }
        for key, count in expected.items():
            self.assertEqual(len(portfolio[key]), count)
            self.assertTrue(all(row["execution_credit"] == 0 for row in portfolio[key]))
        self.assertEqual(len(portfolio["practice_lenses"]), 3)
        self.assertTrue(portfolio["caps_are_ceilings_not_quotas"])

    def test_official_sources_are_vocabulary_only(self):
        ledger = load("sources/official-source-ledger.json")
        self.assertFalse(ledger["citations_are_observations"])
        self.assertGreaterEqual(len(ledger["sources"]), 8)
        for source in ledger["sources"]:
            self.assertEqual(source["observation_count"], 0)
            self.assertIn("only", source["scope"])

    def test_startup_failures_are_retained_at_zero_credit(self):
        ledger = load("method-flow/startup-ledger.json")
        self.assertEqual(ledger["failed_witness_count"], 8)
        self.assertTrue(ledger["recoveries_do_not_rewrite_failures"])
        self.assertTrue(all(row["initial_credit"] == 0 for row in ledger["failed_witnesses"]))

    def test_x1_manifest_matches_current_bytes(self):
        manifest = load("validation/x1-owner-manifest.json")
        for entry in manifest["entries"]:
            raw = (REPO / entry["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_staged_review_is_exact_and_private_surface_is_clean(self):
        review = load("validation/x1-staged-review.json")
        self.assertEqual(review["status"], "passed")
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(len(review["privacy_candidates"]), 3)
        self.assertTrue(all(row["status"] == "scanner_definition_only" for row in review["privacy_candidates"]))
        self.assertEqual(review["unresolved_privacy_candidates"], [])
        self.assertEqual(review["confirmed_privacy_hits"], [])
        self.assertEqual(review["x2_paths_present"], [])
        for entry in review["entries"]:
            raw = subprocess.check_output(["git", "show", f":{entry['path']}"], cwd=REPO)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])

    def test_all_x1_json_parses_and_document_caps_hold(self):
        files = [path for path in ROOT.rglob("*") if path.is_file()]
        self.assertLess(len(files) + 2, 2000)
        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertLessEqual(len(text.split()), 100000, path)
            if path.suffix == ".json":
                json.loads(text)

    def test_activation_baseline_and_terminal_truth_are_preserved(self):
        intake = load("activation-intake.json")
        self.assertEqual(intake["activation_baseline"]["effective_negatives"], 38613)
        self.assertEqual(intake["activation_baseline"]["failed_witnesses"], 10274)
        self.assertEqual(intake["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(intake["planning_only"])
        self.assertFalse(intake["successor_contacted"])


if __name__ == "__main__":
    unittest.main()

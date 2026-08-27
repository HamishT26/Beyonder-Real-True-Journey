from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v672-v3"
X1 = PHASE / "x1"


def load(relative: str):
    return json.loads((X1 / relative).read_text(encoding="utf-8"))


class SableRookV672V3X1Tests(unittest.TestCase):
    def test_x1_is_planning_only(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["lifecycle"], "x1_planning_only")
        self.assertFalse(truth["x2_started"])
        self.assertFalse((PHASE / "x2").exists())

    def test_forty_new_proposals(self):
        freeze = load("proposals/new-proposal-freeze.json")
        self.assertEqual(freeze["proposal_count"], 40)
        self.assertEqual(len(freeze["proposals"]), 40)
        self.assertEqual(len({row["proposal_id"] for row in freeze["proposals"]}), 40)
        self.assertEqual(len({row["title"] for row in freeze["proposals"]}), 40)

    def test_proposal_fields_are_complete(self):
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure_condition",
            "approval_class", "execution_lane", "official_or_primary_source_needs",
            "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery",
            "protected_gates", "expected_disposition", "pillar", "practice_lens",
            "surface", "x1_state",
        }
        for row in load("proposals/new-proposal-freeze.json")["proposals"]:
            self.assertTrue(required.issubset(row), row["proposal_id"])
            self.assertEqual(row["x1_state"], "planning_only_no_x2_credit")

    def test_exact_expected_outcome_distribution(self):
        rows = load("proposals/new-proposal-freeze.json")["proposals"]
        self.assertEqual(
            Counter(row["expected_disposition"] for row in rows),
            Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}),
        )

    def test_only_four_truth_labels(self):
        labels = {
            row["expected_disposition"]
            for row in load("proposals/new-proposal-freeze.json")["proposals"]
        }
        self.assertEqual(labels, {"completed", "represented", "open_gap", "exact_gate"})

    def test_inherited_selection_has_zero_credit(self):
        inherited = load("proposals/inherited-zero-credit-review.json")
        self.assertEqual(inherited["selection_count"], 20)
        self.assertEqual(inherited["completion_credit"], 0)
        self.assertTrue(all(row["credit"] == 0 for row in inherited["rows"]))

    def test_semantic_audit_has_no_quarantine(self):
        audit = load("proposals/semantic-neighbor-audit.json")
        self.assertEqual(audit["declared_source_chain"], 5990)
        self.assertGreaterEqual(audit["proposal_ledger_paths_examined"], 200)
        self.assertGreaterEqual(audit["materialized_title_records_examined"], 4000)
        self.assertEqual(audit["ledger_parse_failures"], [])
        self.assertEqual(audit["exact_collision_count"], 0)
        self.assertEqual(audit["quarantined_count"], 0)
        self.assertFalse(audit["universal_semantic_novelty_claimed"])

    def test_portfolio_floors_and_caps(self):
        portfolio = load("portfolio-freeze.json")
        self.assertEqual(len(portfolio["safe_now_tasks"]), 60)
        self.assertEqual(len(portfolio["candidate_tasks"]), 30)
        self.assertEqual(len(portfolio["owner_skill_builds"]), 20)
        self.assertEqual(len(portfolio["owner_runner_builds"]), 10)
        self.assertEqual(len(portfolio["owner_clean_fix_refine"]), 60)
        self.assertEqual(len(portfolio["successor_clean_fix_refine_recommendations"]), 30)
        self.assertEqual(len(portfolio["exact_approval_packets"]), 20)
        self.assertEqual(len(portfolio["blocked_packets"]), 10)
        self.assertTrue(portfolio["caps_are_ceilings_not_quotas"])

    def test_three_practice_lenses_and_one_successor_recommendation(self):
        portfolio = load("portfolio-freeze.json")
        self.assertEqual(len(portfolio["practice_lenses"]), 3)
        self.assertEqual(portfolio["successor_practice_recommendation"]["credit"], 0)

    def test_source_ledger_is_nonempirical(self):
        ledger = load("source-ledger.json")
        self.assertTrue(ledger["citation_is_not_observation"])
        self.assertEqual(ledger["real_rows_ingested"], 0)
        self.assertEqual(ledger["network_data_downloads"], 0)
        self.assertEqual(len(ledger["sources"]), 5)

    def test_startup_failures_are_retained(self):
        flow = load("method-flow-startup.json")
        failed = [w for w in flow["witnesses"] if w["kind"] == "failed"]
        passing = [w for w in flow["witnesses"] if w["kind"] == "passing"]
        self.assertEqual(len(failed), 6)
        self.assertEqual(len(passing), 6)
        self.assertTrue(all(w["credit"] == 0 for w in failed))
        self.assertEqual(flow["failures_erased"], 0)
        self.assertEqual(flow["recoveries_relabelled_as_original_success"], 0)

    def test_authority_noncompensation_and_verdict(self):
        boundary = load("authority-boundary.json")
        self.assertEqual(boundary["verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertIn("No number", boundary["noncompensation"])
        self.assertIn("maori_authority", boundary["protected_gates"])

    def test_identity_is_relational_and_corrigible(self):
        identity = load("wellbeing-and-identity.json")
        self.assertFalse(identity["identity_evidence"])
        self.assertTrue(identity["corrigible"])
        self.assertEqual(identity["pronouns"], "they/them")

    def test_owner_files_below_rotation_stop(self):
        files = [path for path in PHASE.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)

    def test_documents_below_word_ceiling(self):
        for path in PHASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)

    def test_all_json_parses(self):
        for path in PHASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

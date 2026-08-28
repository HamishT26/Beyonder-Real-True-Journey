from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "caelen-ash" / "v674-v3"
X1 = ROOT / "x1"
SOURCE = "0b9ccf8c74f3b0a5f96b8582162df8e2a06edd05"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(name: str):
    return json.loads((X1 / name).read_text(encoding="utf-8"))


class CaelenV674V3X1Tests(unittest.TestCase):
    def test_head_is_exact_source_before_x1_commit(self):
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
        ).strip()
        self.assertEqual(head, SOURCE)

    def test_x2_is_absent(self):
        self.assertFalse((ROOT / "x2").exists())

    def test_sixty_new_proposals_and_exact_expected_distribution(self):
        freeze = load("new-proposal-freeze.json")
        self.assertEqual(freeze["proposal_count"], 60)
        self.assertEqual(
            freeze["expected_outcomes"],
            {
                "completed": 42,
                "represented": 12,
                "open_gap": 3,
                "exact_gate": 3,
            },
        )
        self.assertFalse(freeze["outcomes_observed"])
        self.assertFalse(freeze["universal_novelty_claim"])

    def test_proposal_contracts_are_complete_and_single_disposition(self):
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "official_or_primary_source_needs",
            "concrete_artifact",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_execution_disposition",
        }
        proposals = load("new-proposal-freeze.json")["proposals"]
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 60)
        self.assertEqual(
            len({row["title"].casefold() for row in proposals}), 60
        )
        for row in proposals:
            self.assertTrue(required.issubset(row))
            self.assertIn(row["expected_execution_disposition"], ALLOWED)
            self.assertIsInstance(
                row["expected_execution_disposition"], str
            )
            self.assertEqual(
                row["x1_state"], "planning_only_not_observed_outcome"
            )

    def test_materialized_neighbor_audit_passes_without_universal_claim(self):
        audit = load("semantic-neighbor-audit.json")
        self.assertEqual(audit["materialized_ledger_paths"], 58)
        self.assertEqual(audit["materialized_title_records"], 1820)
        self.assertEqual(audit["unique_normalized_titles"], 1547)
        self.assertEqual(audit["parse_failures"], [])
        self.assertTrue(audit["internal_unique"])
        self.assertEqual(audit["exact_collisions"], 0)
        self.assertEqual(audit["quarantined_count"], 0)
        self.assertFalse(audit["universal_novelty_claim"])

    def test_inherited_rows_have_zero_credit(self):
        inherited = load("inherited-revalidation-freeze.json")
        self.assertEqual(inherited["row_count"], 60)
        self.assertEqual(inherited["novelty_credit"], 0)
        self.assertEqual(inherited["completion_credit"], 0)
        self.assertTrue(
            all(
                row["novelty_credit"] == 0
                and row["completion_credit"] == 0
                for row in inherited["rows"]
            )
        )

    def test_portfolio_floors_and_holds(self):
        portfolio = load("portfolio-freeze.json")
        expected = {
            "safe_now_packets": 120,
            "owner_candidates": 80,
            "successor_candidates": 20,
            "exact_approval_packets": 20,
            "blocked_packets": 10,
            "owner_skill_ideas": 20,
            "owner_runner_ideas": 10,
            "successor_skill_recommendations": 10,
            "successor_runner_recommendations": 10,
            "owner_clean_fix_refine": 100,
            "successor_clean_fix_refine": 30,
            "successor_practice_recommendations": 1,
        }
        for key, count in expected.items():
            self.assertEqual(len(portfolio[key]), count, key)
        self.assertEqual(
            portfolio["state"], "planning_only_not_executed"
        )
        self.assertTrue(
            all(
                row["state"] == "exact_approval_required_unexecuted"
                for row in portfolio["exact_approval_packets"]
            )
        )
        self.assertTrue(
            all(
                row["state"] == "blocked_unexecuted"
                for row in portfolio["blocked_packets"]
            )
        )

    def test_official_sources_are_vocabulary_only(self):
        ledger = load("source-ledger.json")
        self.assertEqual(len(ledger["entries"]), 5)
        self.assertFalse(ledger["citations_are_observations"])
        self.assertFalse(ledger["endorsement_claimed"])
        self.assertEqual(ledger["real_data_rows"], 0)

    def test_startup_failures_are_retained(self):
        ledger = load("method-flow-startup.json")
        self.assertEqual(ledger["caelen_startup_failure_count"], 8)
        self.assertTrue(
            all(
                row["state"] == "failed_retained_zero_credit"
                for row in ledger["failures"]
            )
        )
        self.assertTrue(
            all(row["success_credit"] == 0 for row in ledger["failures"])
        )

    def test_x1_manifest_matches_current_bytes(self):
        manifest = load("x1-manifest.json")
        self.assertTrue(manifest["x2_absent"])
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = (REPO / entry["path"]).read_bytes()
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(
                hashlib.sha256(data).hexdigest(),
                entry["sha256"],
                entry["path"],
            )

    def test_all_x1_json_parses_and_document_caps_hold(self):
        for path in X1.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))
        for path in X1.rglob("*.md"):
            words = len(path.read_text(encoding="utf-8").split())
            self.assertLessEqual(words, 100000)
        self.assertGreaterEqual(
            len(
                (X1 / "integrated-overview.md")
                .read_text(encoding="utf-8")
                .split()
            ),
            700,
        )

    def test_route_is_held_and_no_contact_occurred(self):
        route = load("route-roster-plan.json")
        self.assertEqual(route["state"], "TERMINAL_HOLD")
        self.assertFalse(route["precontact"])
        self.assertEqual(route["send_attempts"], 0)


if __name__ == "__main__":
    unittest.main()

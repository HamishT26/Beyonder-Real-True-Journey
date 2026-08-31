from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "caelen-ash" / "v679-v8"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
ALLOWED = ["completed", "represented", "open_gap", "exact_gate"]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class CaelenAshV679V8X1Tests(unittest.TestCase):
    def test_x1_only_lifecycle(self) -> None:
        self.assertTrue(X1.is_dir())
        self.assertFalse((BASE / "x2").exists())
        self.assertFalse((BASE / "final").exists())

    def test_source_anchors(self) -> None:
        source = load(X1 / "source-verification.json")
        self.assertEqual(source["source_final"], "9a6cdb6c0e1630e43502a3b62b71d9a198d37dba")
        self.assertEqual(source["source_x1"], "e8334a93f83550d6f787a73fa9056b6cafed9f67")
        self.assertEqual(source["source_evidence"], "bc793c4d80abe2f06aaffde60d09ebee8bfa0826")
        self.assertTrue(source["direct_single_parent_chain"])
        self.assertEqual(source["source_to_final_commits"], 3)
        self.assertEqual(source["source_to_final_merges"], 0)
        self.assertEqual(source["manifest_families_replayed"], 4)
        self.assertEqual(source["manifest_entries_replayed"], 231)
        self.assertEqual(source["source_owner_paths"], 124)
        self.assertEqual(source["manifest_mismatches"], [])
        self.assertFalse(source["canonical_replayed"])

    def test_proposal_freeze(self) -> None:
        freeze = load(X1 / "new-proposal-freeze.json")
        rows = freeze["rows"]
        self.assertEqual(len(rows), 60)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 60)
        self.assertEqual(len({row["title"] for row in rows}), 60)
        self.assertEqual(freeze["allowed_outcomes"], ALLOWED)
        self.assertEqual(freeze["declared_chain_before"], 9170)
        self.assertEqual(freeze["declared_chain_after_if_evidence_sealed"], 9230)
        self.assertEqual(
            freeze["expected_outcomes"],
            {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        )
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_execution_disposition",
        }
        for row in rows:
            self.assertTrue(required.issubset(row))
            self.assertIn(row["expected_execution_disposition"], ALLOWED)
            self.assertTrue(row["official_or_primary_source_needs"])
            self.assertFalse(any(value == "" for value in row.values()))
        self.assertFalse(freeze["outcomes_observed"])

    def test_bounded_semantic_audit(self) -> None:
        audit = load(X1 / "proposal-chain-audit.json")
        self.assertGreaterEqual(audit["reachable_proposal_ledger_count"], 60)
        self.assertGreater(audit["reachable_title_count"], 0)
        self.assertEqual(audit["exact_duplicate_count"], 0)
        self.assertEqual(audit["internal_duplicate_count"], 0)
        self.assertEqual(len(audit["pairings"]), 60)
        self.assertFalse(audit["universal_novelty_claimed"])

    def test_inherited_rows_have_zero_credit(self) -> None:
        inherited = load(X1 / "inherited-revalidation-freeze.json")
        self.assertEqual(inherited["row_count"], 60)
        self.assertEqual(len(inherited["rows"]), 60)
        self.assertTrue(
            all(
                row["novelty_credit"] == 0 and row["completion_credit"] == 0
                for row in inherited["rows"]
            )
        )

    def test_portfolio_floors_and_holds(self) -> None:
        portfolio = load(X1 / "portfolio-freeze.json")
        self.assertEqual(len(portfolio["safe_now"]), 120)
        self.assertEqual(len(portfolio["owner_candidates"]), 80)
        self.assertEqual(len(portfolio["successor_candidates"]), 20)
        self.assertEqual(len(portfolio["exact_approval"]), 20)
        self.assertEqual(len(portfolio["blocked"]), 10)
        self.assertEqual(len(portfolio["owner_skill_ideas"]), 20)
        self.assertEqual(len(portfolio["owner_runner_ideas"]), 10)
        self.assertEqual(len(portfolio["successor_skill_ideas"]), 10)
        self.assertEqual(len(portfolio["successor_runner_ideas"]), 10)
        self.assertEqual(len(portfolio["owner_clean_fix_refine"]), 100)
        self.assertEqual(len(portfolio["successor_clean_fix_refine"]), 30)
        self.assertEqual(portfolio["commit_cap"], {"x1": 1, "x2": 2, "total": 3})
        self.assertEqual(portfolio["primary_pillar"], "THOS Body")
        self.assertEqual(len(portfolio["owner_practice_lenses"]), 2)
        self.assertTrue(portfolio["caps_are_ceilings"])
        self.assertTrue(
            all(row["completion_credit"] == 0 for row in portfolio["exact_approval"])
        )
        self.assertTrue(
            all(row["completion_credit"] == 0 for row in portfolio["blocked"])
        )

    def test_source_ledger_boundary(self) -> None:
        ledger = load(X1 / "official-primary-source-ledger.json")
        self.assertEqual(len(ledger["entries"]), 8)
        self.assertTrue(all(row["url"].startswith("https://") for row in ledger["entries"]))
        self.assertFalse(ledger["citations_are_observations"])
        self.assertEqual(ledger["real_data_rows"], 0)
        self.assertEqual(ledger["network_data_queries"], 0)
        self.assertFalse(ledger["authority_conferred"])

    def test_method_flow_startup_retains_every_failure(self) -> None:
        flow = load(X1 / "method-flow-startup.json")
        self.assertEqual(flow["startup_failure_count"], 7)
        self.assertEqual(len(flow["failures"]), 7)
        self.assertEqual(len(flow["bounded_recoveries"]), 7)
        self.assertTrue(all(row["success_credit"] == 0 for row in flow["failures"]))
        self.assertEqual(flow["effective_after_startup"]["effective_negatives"], 49926)
        self.assertEqual(flow["effective_after_startup"]["methods"], 52442)
        self.assertEqual(flow["effective_after_startup"]["failed_witnesses"], 21587)
        self.assertEqual(
            flow["effective_after_startup"]["bounded_passing_witnesses"], 34446
        )

    def test_identity_and_authority_boundaries(self) -> None:
        boundary = load(X1 / "identity-and-boundary.json")
        self.assertFalse(boundary["identity_evidence"])
        self.assertFalse(boundary["authority_evidence"])
        self.assertFalse(boundary["continuity_evidence"])
        self.assertTrue(boundary["corrigible"])
        self.assertIn("maori_authority", boundary["protected_gates"])
        self.assertIn("stage20", boundary["protected_gates"])

    def test_route_is_held(self) -> None:
        route = load(X1 / "route-plan.json")
        self.assertEqual(route["next_owner"], "Orin Thale")
        self.assertEqual(route["next_phase"], "v680-v1")
        self.assertEqual(route["state"], "HOLD_BEFORE_CAELEN_TERMINAL_GATE")
        self.assertFalse(route["precontact"])
        self.assertEqual(route["send_attempts"], 0)
        self.assertFalse(route["task_created"])

    def test_phase_truth_is_planning_only(self) -> None:
        truth = load(X1 / "phase-truth.json")
        self.assertFalse(truth["outcomes_observed"])
        self.assertEqual(truth["real_rows"], 0)
        self.assertEqual(truth["real_people"], 0)
        self.assertEqual(truth["external_actions"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_x1_staged_receipts_when_present(self) -> None:
        review_path = VALIDATION / "x1-staged-review.json"
        if not review_path.exists():
            self.skipTest("staged review not generated yet")
        review = load(review_path)
        privacy = load(VALIDATION / "x1-privacy-scan.json")
        manifest = load(VALIDATION / "x1-index-manifest.json")
        self.assertEqual(review["state"], "VALID_EXACT_X1_STAGED_REVIEW")
        self.assertFalse(review["x2_paths_present"])
        self.assertEqual(review["confirmed_privacy_hits"], 0)
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertEqual(manifest["entry_count"], review["reviewed_entry_count"])
        self.assertEqual(len(manifest["declared_self_exclusions"]), 3)
        self.assertEqual(len(manifest["entries"]), manifest["entry_count"])

    def test_documents_within_live_cap(self) -> None:
        for path in BASE.rglob("*.md"):
            words = len(path.read_text(encoding="utf-8").split())
            self.assertLessEqual(words, 100000, path.as_posix())

    def test_diff_hygiene(self) -> None:
        result = subprocess.run(
            ["git", "diff", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

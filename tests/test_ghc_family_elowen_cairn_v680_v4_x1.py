from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v680-v4"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "ea9fa3317cdc11ae23dfa0b2cc370070ae1e9529"
BRANCH = "codex/GHC-Family/elowen-cairn-v680-v4-full-tools"
OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class ElowenCairnV680V4X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = load(X1 / "new-proposal-freeze.json")
        cls.proposals = cls.freeze["proposals"]
        cls.portfolio = load(X1 / "portfolio-freeze.json")
        cls.audit = load(X1 / "proposal-chain-audit.json")
        cls.method = load(X1 / "method-flow-startup.json")

    def test_exact_source_and_branch(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD"), SOURCE)
        self.assertEqual(git("branch", "--show-current"), BRANCH)

    def test_x1_only_lifecycle(self) -> None:
        self.assertFalse((BASE / "x2").exists())
        self.assertFalse((ROOT / "scripts" / "build_ghc_family_elowen_cairn_v680_v4_x2.py").exists())
        phase = load(X1 / "phase-truth.json")
        self.assertEqual(phase["execution_state"], "PLANNING_ONLY_X1")
        self.assertFalse(phase["x2_started"])
        self.assertIsNone(phase["observed_outcomes"])

    def test_proposal_count_and_ids(self) -> None:
        self.assertEqual(len(self.proposals), 60)
        self.assertEqual(
            [row["proposal_id"] for row in self.proposals],
            [f"EC6804-N{index:03d}" for index in range(1, 61)],
        )

    def test_exact_expected_disposition_counts(self) -> None:
        counts = Counter(row["expected_disposition"] for row in self.proposals)
        self.assertEqual(counts, Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}))
        self.assertEqual(set(counts), OUTCOMES)

    def test_required_proposal_fields(self) -> None:
        required = {
            "approval_class",
            "concrete_artifacts",
            "execution_lane",
            "expected_disposition",
            "falsifier_or_acceptance_gate",
            "hypothesis",
            "null_or_failure_condition",
            "official_or_primary_source_needs",
            "preregistered_rejecting_mutations",
            "proposal_id",
            "protected_gates",
            "rollback_or_recovery",
            "title",
        }
        for row in self.proposals:
            self.assertTrue(required <= set(row), row["proposal_id"])

    def test_five_rejecting_mutations_per_proposal(self) -> None:
        for row in self.proposals:
            mutations = row["preregistered_rejecting_mutations"]
            self.assertEqual(len(mutations), 5)
            self.assertEqual(len({item["mutation_type"] for item in mutations}), 5)
            self.assertTrue(all(item["expected_result"] == "rejected_zero_credit" for item in mutations))

    def test_novelty_audit_is_bounded_and_clear(self) -> None:
        self.assertFalse(self.audit["audit_scope"]["universal_9410_row_materialization_claimed"])
        self.assertGreater(self.audit["audit_scope"]["proposal_json_paths_parsed"], 0)
        self.assertEqual(self.audit["exact_title_collisions"], [])
        self.assertEqual(self.audit["quarantined_neighbors"], [])
        self.assertLess(self.audit["maximum_neighbor_score"], self.audit["quarantine_threshold_token_jaccard"])

    def test_inherited_reviews_are_zero_credit(self) -> None:
        inherited = load(X1 / "inherited-revalidation-freeze.json")
        self.assertEqual(inherited["count"], 20)
        self.assertTrue(all(row["completion_credit"] == 0 for row in inherited["reviews"]))

    def test_portfolio_floors(self) -> None:
        expected = {
            "safe_now": 120,
            "owner_candidates": 80,
            "owner_clean_fix_refine": 100,
            "exact_approval": 20,
            "blocked": 10,
            "owner_skill_ideas": 20,
            "owner_runner_ideas": 10,
            "successor_candidates": 20,
            "successor_clean_fix_refine": 30,
            "successor_skill_ideas": 10,
            "successor_runner_ideas": 10,
        }
        for key, count in expected.items():
            self.assertEqual(len(self.portfolio[key]), count, key)

    def test_no_portfolio_completion_in_x1(self) -> None:
        for key in ("safe_now", "owner_candidates", "owner_clean_fix_refine", "exact_approval", "blocked"):
            self.assertTrue(all(row["state"] == "preregistered_not_executed" for row in self.portfolio[key]))

    def test_startup_failures_retained(self) -> None:
        failures = self.method["startup_failures"]
        self.assertEqual(len(failures), 10)
        self.assertEqual(
            [row["failure_id"] for row in failures],
            [f"EC6804-ST-N{index:03d}" for index in range(1, 11)],
        )
        self.assertTrue(all(row["initial_credit"] == 0 for row in failures))
        self.assertFalse(self.method["failure_erasure"])

    def test_activation_counts_add_startup_failures(self) -> None:
        baseline = self.method["activation_baseline"]
        current = self.method["current_after_startup"]
        for key in ("effective_negatives", "effective_methods", "failed_witnesses", "bounded_passing_witnesses"):
            self.assertEqual(current[key] - baseline[key], 10)
        self.assertEqual(current["open_gaps"], 449)
        self.assertEqual(current["exact_gates"], 440)

    def test_sources_are_vocabulary_only(self) -> None:
        sources = load(X1 / "official-primary-source-ledger.json")
        self.assertFalse(sources["authority_conferred"])
        self.assertFalse(sources["citations_are_observations"])
        self.assertEqual(sources["real_data_rows"], 0)
        self.assertEqual(sources["network_data_queries"], 0)

    def test_route_is_held(self) -> None:
        route = load(X1 / "route-plan.json")
        self.assertFalse(route["recipient_contacted"])
        self.assertTrue(route["terminal_gate_required"])
        self.assertEqual(route["prospective_successor_title"], "Sylven Arc")

    def test_privacy_scan_has_no_confirmed_hits(self) -> None:
        scan = load(VALIDATION / "x1-privacy-scan.json")
        self.assertEqual(scan["confirmed_hits"], [])
        self.assertEqual(len(scan["privacy_classes"]), 5)

    def test_manifest_replays_worktree_bytes(self) -> None:
        manifest = load(VALIDATION / "x1-index-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_staged_review_has_no_x2_paths(self) -> None:
        review = load(VALIDATION / "x1-staged-review.json")
        self.assertEqual(review["lifecycle"], "planning_only_x1")
        self.assertEqual(review["x2_paths"], [])
        self.assertTrue(all("/x2/" not in path for path in review["expected_paths"]))

    def test_terminal_verdict_and_claim_boundaries(self) -> None:
        phase = load(X1 / "phase-truth.json")
        overview = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
        self.assertEqual(phase["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        for phrase in ("GMUT remains", "THOS remains", "Freed ID remains", "Māori authority remain exact-gated"):
            self.assertIn(phrase, overview)


if __name__ == "__main__":
    unittest.main()


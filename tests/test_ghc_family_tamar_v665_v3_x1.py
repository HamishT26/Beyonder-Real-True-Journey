from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v665-v3"
BUILDER_PATH = ROOT / "scripts/build_ghc_family_v665_v3_x1.py"
SOURCE = "a559ab2dfe46cace97fd03c09f1018477fdc09f4"
BRANCH = "codex/GHC-Family/tamar-vey-v665-v3-full-tools"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load_builder():
    spec = importlib.util.spec_from_file_location(
        "tamar_v665_v3_x1",
        BUILDER_PATH,
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def doc(name: str):
    return json.loads(
        (PHASE / "x1" / name).read_text(encoding="utf-8")
    )


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
    ).stdout.strip()


class TamarV665V3X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_builder()

    def test_01_exact_source_and_branch(self):
        self.assertEqual(git("rev-parse", "HEAD"), SOURCE)
        self.assertEqual(git("branch", "--show-current"), BRANCH)

    def test_02_corpus_and_novelty(self):
        audit = doc("novelty-audit.json")
        self.assertEqual(audit["corpus_row_count"], 4050)
        self.assertEqual(audit["new_title_count"], 20)
        self.assertEqual(audit["new_frozen_total"], 4070)
        self.assertEqual(audit["exact_inherited_collisions"], [])
        self.assertEqual(
            audit["new_pair_collisions_at_or_above_0_70"],
            [],
        )
        self.assertLessEqual(
            audit["maximum_inherited_token_jaccard_similarity"],
            0.50,
        )

    def test_03_exact_twenty_required_fields(self):
        freeze = doc("proposal-freeze.json")
        proposals = freeze["new_proposals"]
        self.assertEqual(len(proposals), 20)
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
            "expected_disposition",
        }
        for proposal in proposals:
            self.assertTrue(required.issubset(proposal))
            self.assertIn(
                proposal["expected_disposition"],
                ALLOWED,
            )
            self.assertEqual(
                proposal["x1_status"],
                "frozen_not_executed",
            )

    def test_04_expected_distribution_only(self):
        freeze = doc("proposal-freeze.json")
        self.assertEqual(
            freeze["expected_disposition_counts"],
            {
                "completed": 14,
                "represented": 4,
                "open_gap": 1,
                "exact_gate": 1,
            },
        )
        self.assertEqual(freeze["x2_implementation_count"], 0)
        self.assertEqual(freeze["x2_outcome_count"], 0)

    def test_05_sources_are_public_and_zero_row(self):
        ledger = doc("source-ledger.json")
        self.assertGreaterEqual(ledger["source_count"], 10)
        self.assertEqual(ledger["real_rows_ingested"], 0)
        self.assertEqual(ledger["network_data_calls"], 0)
        for source in ledger["sources"]:
            self.assertTrue(source["url"].startswith("https://"))
            self.assertIn(
                source["status"],
                {"current", "stable", "draft", "watch"},
            )
            self.assertEqual(source["real_rows_ingested"], 0)

    def test_06_startup_failures_retained(self):
        flow = doc("startup-method-flow.json")
        self.assertEqual(
            flow["startup"]["new_failed_witnesses"],
            13,
        )
        self.assertEqual(
            flow["startup"]["failure_erasure_count"],
            0,
        )
        self.assertEqual(
            flow["effective_after_startup"]["negatives"],
            25320,
        )
        self.assertEqual(
            flow["effective_after_startup"]["methods"],
            9182,
        )
        self.assertTrue(
            all(not row["failure_erased"] for row in flow["methods"])
        )

    def test_07_portfolio_floor_and_gate_separation(self):
        portfolio = doc("portfolio-freeze.json")
        self.assertEqual(
            portfolio["counts"],
            {
                "safe_now": 30,
                "bounded_candidates": 15,
                "exact_approval": 10,
                "blocked": 5,
                "skill_ideas": 10,
                "runner_ideas": 10,
                "clean_fix_refine": 30,
            },
        )
        self.assertEqual(
            portfolio["inherited_completion_credit"],
            0,
        )

    def test_08_source_verification_and_no_replay(self):
        receipt = doc("source-verification.json")
        self.assertTrue(receipt["valid"])
        self.assertTrue(
            receipt["local_upstream_tracking_fresh_live_equal"]
        )
        self.assertFalse(receipt["canonical_replayed"])
        self.assertEqual(
            sum(
                row["entries"]
                for row in receipt[
                    "immutable_manifest_replays"
                ].values()
            ),
            290,
        )

    def test_09_staged_review_and_manifest(self):
        review = doc("x1-staged-review.json")
        manifest = doc("x1-content-manifest.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["x2_paths_present"], 0)
        self.assertEqual(
            review["confirmed_privacy_or_raw_identifier_hits"],
            [],
        )
        self.assertEqual(
            manifest["entry_count"],
            len(self.builder.BASE_PATHS),
        )
        self.assertEqual(
            manifest["declared_self_exclusions"],
            self.builder.SELF_EXCLUSIONS,
        )

    def test_10_builder_exact_staged_audit(self):
        result = self.builder.check_staged()
        self.assertTrue(result["valid"])
        self.assertEqual(result["privacy_confirmed_hits"], 0)
        self.assertEqual(result["x2_paths"], 0)


if __name__ == "__main__":
    unittest.main()

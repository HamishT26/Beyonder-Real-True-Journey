from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_v645_v4_definitions import (  # noqa: E402
    ADOPTED_CANDIDATES,
    ADOPTED_CLEAN,
    ADOPTED_RUNNERS,
    ADOPTED_SAFE_NOW,
    ADOPTED_SKILLS,
    NEW_CANDIDATES,
    NEW_CLEAN,
    NEW_RUNNERS,
    NEW_SAFE_NOW,
    NEW_SKILLS,
    OUTCOME_CLASSES,
    PROPOSALS,
    SOURCES,
)

PHASE_DIR = ROOT / "docs/ilyra-fen/v645-v4"


class V645V4X1Tests(unittest.TestCase):
    def test_exact_core_proposals_and_distribution(self) -> None:
        self.assertEqual(len(PROPOSALS), 10)
        self.assertEqual(len({row["proposal_id"] for row in PROPOSALS}), 10)
        self.assertEqual(len({row["title"].casefold() for row in PROPOSALS}), 10)
        self.assertEqual(
            Counter(row["expected_disposition"] for row in PROPOSALS),
            Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
        )
        self.assertEqual(set(row["expected_disposition"] for row in PROPOSALS), set(OUTCOME_CLASSES))
        required = {
            "hypothesis", "null_or_failure", "approval_class", "execution_lane",
            "authoritative_source_needs", "deliverables", "test_falsifier_or_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        for row in PROPOSALS:
            self.assertTrue(required <= row.keys(), row["proposal_id"])

    def test_expanded_portfolio_cardinalities(self) -> None:
        self.assertEqual((len(ADOPTED_SAFE_NOW), len(NEW_SAFE_NOW)), (15, 15))
        self.assertEqual((len(ADOPTED_CANDIDATES), len(NEW_CANDIDATES)), (10, 10))
        self.assertEqual((len(ADOPTED_SKILLS), len(NEW_SKILLS)), (10, 10))
        self.assertEqual((len(ADOPTED_RUNNERS), len(NEW_RUNNERS)), (5, 5))
        self.assertEqual((len(ADOPTED_CLEAN), len(NEW_CLEAN)), (15, 15))
        for row in ADOPTED_SAFE_NOW + ADOPTED_CANDIDATES:
            self.assertEqual(row["completion_credit"], "none_until_v645_v4_x2_witness")
            self.assertEqual(row["review_state"], "adopted_after_fresh_novelty_safety_compatibility_review")

    def test_primary_source_statuses(self) -> None:
        self.assertEqual(len(SOURCES), 14)
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in SOURCES))
        self.assertTrue(all(row["url"].startswith("https://") for row in SOURCES))

    def test_frozen_artifacts_and_no_x2_outcomes(self) -> None:
        required = [
            "x1-proposals.json", "x1-preregistration.md", "wellbeing-check.md",
            "approval-packets/x1-approval-portfolio.json",
            "prototypes/x1-skill-runner-plan.json", "maintenance/x1-clean-refine-plan.json",
            "sources/source-ledger.json", "provenance/prior-proposal-collision-audit.json",
            "validation/x1-operational-negatives.json", "validation/x1-structural.json",
            "method-flow/method-flow-state.json", "sandbox/x1-sandbox-plan.json",
            "environment/startup-receipt.json", "focus/primary-focus-receipt.json",
            "tooling/ghc-family-index.json", "tooling/ghc-family-index.md",
        ]
        for relative in required:
            self.assertTrue((PHASE_DIR / relative).is_file(), relative)
        self.assertFalse((PHASE_DIR / "x2-proposal-ledger.json").exists())
        self.assertFalse((PHASE_DIR / "phase-truth.json").exists())
        self.assertFalse((PHASE_DIR / "closeout-receipt.json").exists())

    def test_collision_and_method_flow_integrity(self) -> None:
        collision = json.loads((PHASE_DIR / "provenance/prior-proposal-collision-audit.json").read_text(encoding="utf-8"))
        self.assertEqual(collision["prior_frozen_proposal_count"], 340)
        self.assertEqual(collision["exact_title_collision_count"], 0)
        self.assertEqual(len(collision["comparisons"]), 10)
        ledger = json.loads((PHASE_DIR / "method-flow/method-flow-state.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["counts"]["methods"], 7)
        self.assertEqual(ledger["counts"]["witnesses"], 14)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 7, "pass": 7})
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in ledger["methods"]))
        negatives = json.loads((PHASE_DIR / "validation/x1-operational-negatives.json").read_text(encoding="utf-8"))
        self.assertEqual(negatives["inherited_effective_negative_count"], 2003)
        self.assertEqual(negatives["new_operational_negative_count"], 7)
        self.assertTrue(negatives["no_failure_erased"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_v645_v5_definitions import (  # noqa: E402
    CANDIDATES,
    CLEAN_TASKS,
    INHERITED_BLOCKED_PACKETS,
    INHERITED_EXACT_PACKETS,
    OUTCOME_CLASSES,
    PROPOSALS,
    RUNNERS,
    SAFE_NOW,
    SKILLS,
    SOURCES,
)

PHASE_DIR = ROOT / "docs/sable-rook/v645-v5"


def load(relative: str) -> dict:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


class V645V5X1Tests(unittest.TestCase):
    def test_exact_core_proposals_and_distribution(self) -> None:
        self.assertEqual(len(PROPOSALS), 10)
        self.assertEqual(len({row["proposal_id"] for row in PROPOSALS}), 10)
        self.assertEqual(len({row["title"].casefold() for row in PROPOSALS}), 10)
        self.assertEqual(
            Counter(row["expected_disposition"] for row in PROPOSALS),
            Counter(
                {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
            ),
        )
        self.assertEqual(
            set(row["expected_disposition"] for row in PROPOSALS),
            set(OUTCOME_CLASSES),
        )
        required = {
            "hypothesis",
            "null_or_failure",
            "approval_class",
            "execution_lane",
            "authoritative_source_needs",
            "deliverables",
            "test_falsifier_or_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for row in PROPOSALS:
            self.assertTrue(required <= row.keys(), row["proposal_id"])

    def test_new_portfolios_and_inherited_gates(self) -> None:
        self.assertEqual(len(SAFE_NOW), 20)
        self.assertEqual(len(CANDIDATES), 12)
        self.assertEqual(len(SKILLS), 12)
        self.assertEqual(len(RUNNERS), 6)
        self.assertEqual(len(CLEAN_TASKS), 20)
        self.assertEqual(len(INHERITED_EXACT_PACKETS), 10)
        self.assertEqual(len(INHERITED_BLOCKED_PACKETS), 5)
        self.assertTrue(all(row["origin"] == "new_sable_proposal" for row in SAFE_NOW + CANDIDATES))
        self.assertTrue(all(row["completion_credit"] == "none_until_v645_v5_x2_witness" for row in SAFE_NOW + CANDIDATES))
        self.assertTrue(all(name.startswith("ghc-family-") for name, _ in SKILLS))
        self.assertTrue(all(name.startswith("ghc_family_") for name, _ in RUNNERS))

    def test_primary_source_statuses(self) -> None:
        self.assertEqual(len(SOURCES), 16)
        self.assertTrue(
            all(row["status"] in {"current", "stable", "draft", "watch"} for row in SOURCES)
        )
        self.assertTrue(all(row["url"].startswith("https://") for row in SOURCES))

    def test_frozen_artifacts_and_collision_results(self) -> None:
        required = [
            "x1-proposals.json",
            "x1-preregistration.md",
            "wellbeing-check.md",
            "approval-packets/x1-approval-portfolio.json",
            "prototypes/x1-skill-runner-plan.json",
            "maintenance/x1-clean-refine-plan.json",
            "sources/source-ledger.json",
            "provenance/prior-proposal-collision-audit.json",
            "provenance/prior-portfolio-collision-audit.json",
            "provenance/rejected-candidate-register.json",
            "validation/x1-operational-negatives.json",
            "validation/x1-stale-label-review.json",
            "validation/x1-structural.json",
            "method-flow/method-flow-state.json",
            "sandbox/x1-sandbox-plan.json",
            "environment/startup-receipt.json",
            "focus/primary-focus-receipt.json",
            "tooling/ghc-family-index.json",
            "tooling/ghc-family-index.md",
        ]
        for relative in required:
            self.assertTrue((PHASE_DIR / relative).is_file(), relative)
        collision = load("provenance/prior-proposal-collision-audit.json")
        self.assertEqual(collision["prior_frozen_proposal_count"], 350)
        self.assertEqual(collision["exact_title_collision_count"], 0)
        self.assertEqual(len(collision["comparisons"]), 10)
        portfolio_collision = load("provenance/prior-portfolio-collision-audit.json")
        self.assertEqual(portfolio_collision["exact_collision_count"], 0)

    def test_method_flow_and_x1_truth(self) -> None:
        ledger = load("method-flow/method-flow-state.json")
        self.assertEqual(ledger["counts"]["methods"], 6)
        self.assertEqual(ledger["counts"]["witnesses"], 12)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 6, "pass": 6})
        self.assertTrue(
            all(row["recommendation_state"] == "preferred" for row in ledger["methods"])
        )
        negatives = load("validation/x1-operational-negatives.json")
        self.assertEqual(negatives["inherited_effective_negative_count"], 2087)
        self.assertEqual(negatives["new_operational_negative_count"], 6)
        self.assertTrue(negatives["no_failure_erased"])
        structural = load("validation/x1-structural.json")
        self.assertEqual(structural["passed"], structural["check_count"])
        self.assertEqual(structural["failed"], [])


if __name__ == "__main__":
    unittest.main()

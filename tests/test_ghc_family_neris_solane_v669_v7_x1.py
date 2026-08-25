"""Planning-only tests for Neris Solane v669-v7 x1."""

from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import ghc_family_neris_solane_v669_v7_archive as archive  # noqa: E402


class NerisV669V7X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = REPO / archive.OWNER_ROOT
        cls.x1 = cls.root / "x1"
        cls.corpus, cls.source_shards = archive.inherited_title_corpus(REPO)
        cls.proposals = archive.proposal_rows(cls.corpus)

    def load(self, relative: str):
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def test_exact_source_and_chain_constants(self) -> None:
        self.assertEqual(archive.SOURCE_FINAL, "ca3ab84977c44bf1c7934ed10e99e4fb341a5952")
        self.assertEqual(archive.SOURCE_CHAIN_DECLARED, 5150)
        self.assertEqual(archive.CHAIN_AFTER, 5190)

    def test_accessible_corpus_is_schema_aware_and_bounded(self) -> None:
        self.assertEqual(len(self.corpus), 1580)
        self.assertEqual(len({row["proposal_id"] for row in self.corpus}), 1580)
        audit = self.load("x1/semantic-novelty-audit.json")
        self.assertEqual(audit["unrecovered_declared_rows"], 3570)
        self.assertFalse(audit["universal_novelty_claim"])

    def test_forty_new_proposals_and_four_labels(self) -> None:
        self.assertEqual(len(self.proposals), 40)
        counts = Counter(row["expected_disposition"] for row in self.proposals)
        self.assertEqual(counts, Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}))
        self.assertEqual(set(counts), {"completed", "represented", "open_gap", "exact_gate"})

    def test_every_proposal_has_complete_preregistration_fields(self) -> None:
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
            "expected_disposition",
        }
        for row in self.proposals:
            self.assertTrue(required.issubset(row))
            self.assertEqual(row["x1_completion_credit"], 0)
            self.assertIsNone(row["observed_disposition"])
            self.assertEqual(len(row["negative_fixtures"]), 4)

    def test_no_visible_collision_or_similarity_quarantine(self) -> None:
        self.assertFalse([row["proposal_id"] for row in self.proposals if row["visible_title_collision"]])
        self.assertFalse([row["proposal_id"] for row in self.proposals if row["semantic_neighbor_quarantined"]])

    def test_portfolio_counts_are_exact_and_zero_credit(self) -> None:
        payload = self.load("x1/portfolio-freeze.json")
        self.assertEqual(
            payload["counts"],
            {"blocked": 5, "candidate": 15, "clean_fix_refine": 30, "exact_approval": 10, "runner": 10, "safe_now": 30, "skill": 10},
        )
        self.assertEqual(payload["x1_completion_credit"], 0)

    def test_three_tools_are_planned_not_installed(self) -> None:
        payload = self.load("x1/tool-candidate-freeze.json")
        self.assertEqual(payload["target_count"], 3)
        self.assertEqual(payload["installation_state"], "planned_not_installed_in_x1")
        self.assertEqual([row["name"] for row in payload["selected"]], ["pint", "portion", "uncertainties"])

    def test_source_statuses_and_zero_ingestion(self) -> None:
        payload = self.load("x1/source-ledger.json")
        self.assertEqual(set(payload["statuses"]), {"current", "stable", "draft", "watch"})
        self.assertTrue(all(row["data_rows_ingested"] == 0 for row in payload["sources"]))

    def test_startup_failures_are_retained(self) -> None:
        payload = self.load("x1/startup-operational-failures.json")
        self.assertEqual(payload["failure_count"], archive.STARTUP_FAILURE_COUNT)
        self.assertEqual(payload["bounded_recovery_witness_count"], archive.STARTUP_FAILURE_COUNT)
        self.assertTrue(all(row["approval_credit"] == 0 for row in payload["rows"]))

    def test_x1_is_planning_only(self) -> None:
        paths = [path.relative_to(REPO).as_posix() for path in self.root.rglob("*") if path.is_file()]
        self.assertFalse([path for path in paths if "/x2/" in path or "/closeout/" in path or "/seal/" in path or "/final/" in path or "/handoffs/" in path])
        self.assertFalse([path for path in paths if "outcome-ledger" in path or "evidence" in Path(path).name])

    def test_validation_receipt_passes_without_privacy_candidate(self) -> None:
        receipt = self.load("validation/x1-validation-receipt.json")
        self.assertTrue(receipt["passed"])
        self.assertEqual(receipt["checks"]["privacy_candidates"], [])
        self.assertTrue(receipt["strict_planning_only"])

    def test_route_is_prepared_not_sent(self) -> None:
        route = self.load("x1/route-state.json")
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["delivery_acknowledged"])
        self.assertEqual(route["successor_contact_count"], 0)


if __name__ == "__main__":
    unittest.main()

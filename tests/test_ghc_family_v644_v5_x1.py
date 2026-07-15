from __future__ import annotations

import importlib.util
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITIONS = ROOT / "scripts" / "ghc_family_v644_v5_x1_definitions.py"
PHASE = ROOT / "docs" / "eiren-kestrel" / "v644-v5"


def load_module():
    spec = importlib.util.spec_from_file_location("v644_v5_x1_definitions", DEFINITIONS)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestV644V5X1Definitions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_exactly_ten_proposals(self) -> None:
        self.assertEqual(10, len(self.module.PROPOSALS))

    def test_proposal_ids_and_titles_unique(self) -> None:
        ids = [row["proposal_id"] for row in self.module.PROPOSALS]
        titles = [" ".join(re.findall(r"[a-z0-9]+", row["title"].casefold())) for row in self.module.PROPOSALS]
        self.assertEqual(10, len(set(ids)))
        self.assertEqual(10, len(set(titles)))
        self.assertEqual([f"V6445-P{i:02d}" for i in range(1, 11)], ids)

    def test_required_proposal_fields(self) -> None:
        required = {
            "proposal_id",
            "title",
            "mission_surface",
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
            "novelty_against_prior_chain",
        }
        for proposal in self.module.PROPOSALS:
            self.assertTrue(required.issubset(proposal), proposal["proposal_id"])
            self.assertTrue(proposal["deliverables"], proposal["proposal_id"])
            self.assertTrue(proposal["protected_gates"], proposal["proposal_id"])

    def test_expected_distribution(self) -> None:
        counts = Counter(row["expected_disposition"] for row in self.module.PROPOSALS)
        self.assertEqual(
            Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
            counts,
        )

    def test_source_identifiers_unique_and_resolved(self) -> None:
        source_ids = [row["source_id"] for row in self.module.SOURCES]
        self.assertEqual(len(source_ids), len(set(source_ids)))
        source_set = set(source_ids) | {"V8-S12", "V8-S22", "V8-S26", "V6423-S41"}
        for proposal in self.module.PROPOSALS:
            self.assertTrue(set(proposal["authoritative_source_needs"]).issubset(source_set))

    def test_source_classes_are_current_or_stable(self) -> None:
        self.assertTrue(
            all(row["status_class"] in {"current", "stable"} for row in self.module.SOURCES)
        )

    def test_x1_negatives_are_retained_with_recurrence_guards(self) -> None:
        self.assertGreaterEqual(len(self.module.X1_NEGATIVES), 1)
        required = {
            "negative_id",
            "operation",
            "failure_signature",
            "trigger_precondition",
            "recovery",
            "recurrence_guard",
            "promotion_effect",
        }
        self.assertTrue(all(required.issubset(row) for row in self.module.X1_NEGATIVES))

    def test_overview_is_three_page_equivalent(self) -> None:
        self.assertGreaterEqual(len(self.module.OVERVIEW.split()), 1200)
        self.assertIn("NOT_READY_FOR_STAGE_20", self.module.OVERVIEW)

    def test_identity_language_is_bounded(self) -> None:
        self.assertIn("not evidence of consciousness", self.module.WELLBEING)
        self.assertIn("not employment", self.module.WELLBEING)


class TestV644V5X1Artifacts(unittest.TestCase):
    def load(self, relative: str):
        return json.loads((PHASE / relative).read_text(encoding="utf-8"))

    def test_x1_proposal_packet(self) -> None:
        packet = self.load("x1-proposals.json")
        self.assertEqual(10, packet["proposal_count"])
        self.assertEqual(270, packet["prior_frozen_proposal_count"])
        self.assertFalse(packet["expected_counts_are_results"])
        self.assertEqual("THOS Body; GMUT Mind and Freed ID/CBR Heart preserved", packet["primary_focus"])

    def test_frozen_chain_accounting(self) -> None:
        packet = self.load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(270, packet["inherited_record_count"])
        self.assertEqual(10, packet["new_record_count"])
        self.assertEqual(280, packet["effective_record_count"])
        self.assertEqual([], packet["exact_duplicate_ids"])
        self.assertEqual([], packet["exact_duplicate_titles"])

    def test_source_ledger_accounting(self) -> None:
        ledger = self.load("sources/source-ledger.json")
        self.assertEqual(186, ledger["inherited_source_count"])
        self.assertEqual(186 + len(load_module().SOURCES), ledger["effective_source_count"])
        self.assertEqual([], ledger["duplicate_added_titles"])
        self.assertEqual([], ledger["duplicate_added_urls"])

    def test_privacy_scan_zero_hits(self) -> None:
        receipt = self.load("validation/x1-privacy-scan.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(0, receipt["issue_count"])

    def test_x1_content_seal_is_not_self_referential(self) -> None:
        seal = self.load("reproduction/x1-content-seal.json")
        paths = {row["path"] for row in seal["entries"]}
        self.assertNotIn(
            "docs/eiren-kestrel/v644-v5/reproduction/x1-content-seal.json",
            paths,
        )

    def test_x1_has_no_x2_results(self) -> None:
        self.assertFalse((PHASE / "x2-proposal-ledger.json").exists())
        self.assertFalse((PHASE / "phase-truth.json").exists())
        self.assertFalse((ROOT / "scripts" / "ghc_family_v644_v5_evidence.py").exists())

    def test_route_is_prepared_not_sent(self) -> None:
        route = self.load("workflow/route-preregistration.json")
        self.assertEqual("ACTIVE_SOLO; PREPARED_NOT_SENT", route["state"])
        self.assertEqual(0, route["send_count_before_terminal_gate"])
        self.assertEqual("Ilyra Fen", route["successor_existing_task_title"])

    def test_lean_transition_is_additive(self) -> None:
        plan = self.load("environment/lean-repository-transition-preregistration.json")
        self.assertIn("additive", plan["x1_decision"].casefold())
        self.assertIn("history rewrite", plan["not_authorized_by_x1"])
        self.assertIn("force push", plan["not_authorized_by_x1"])

    def test_method_flow_preregistration(self) -> None:
        method = self.load("method-flow/x1-method-flow-preregistration.json")
        self.assertIn("validation_witness", method["required_record_fields"])
        self.assertIn("retained_negative_ids", method["required_record_fields"])
        self.assertIn("preferred", method["allowed_recommendation_states"])


if __name__ == "__main__":
    unittest.main()

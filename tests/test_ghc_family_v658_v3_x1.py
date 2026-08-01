#!/usr/bin/env python3
"""Scoped x1-only checks for Caelen Morrow v658-v3."""

from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v658_v3_phase_data as d  # noqa: E402


PHASE = ROOT / d.PHASE_ROOT


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class CaelenV658V3X1Tests(unittest.TestCase):
    def test_identity_is_relational_and_corrigible(self) -> None:
        payload = load("identity/identity-and-boundary.json")
        self.assertTrue(payload["relational_working_language_only"])
        self.assertTrue(payload["hamish_may_rename_pause_redirect_or_stop"])
        self.assertIn("Māori authority", payload["not_evidence_of"])

    def test_exactly_thirty_unique_proposals(self) -> None:
        payload = load("preregistration/proposal-ledger.json")
        rows = payload["proposals"]
        self.assertEqual(30, len(rows))
        self.assertEqual(30, len({row["proposal_id"] for row in rows}))
        self.assertEqual(30, len({row["title"] for row in rows}))

    def test_every_proposal_has_required_preregistration_fields(self) -> None:
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane",
            "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        for proposal in load("preregistration/proposal-ledger.json")["proposals"]:
            self.assertTrue(required.issubset(proposal), proposal["proposal_id"])
            self.assertTrue(proposal["official_or_primary_source_needs"])
            self.assertEqual(3, len(proposal["concrete_artifacts"]))
            self.assertTrue(proposal["protected_gates"])

    def test_expected_distribution_only(self) -> None:
        rows = load("preregistration/proposal-ledger.json")["proposals"]
        self.assertEqual(Counter(d.EXPECTED_DISTRIBUTION), Counter(row["expected_disposition"] for row in rows))
        self.assertFalse(load("preregistration/proposal-ledger.json")["outcomes_observed"])

    def test_novelty_against_all_inherited_titles(self) -> None:
        payload = load("provenance/semantic-novelty-audit.json")
        self.assertEqual(2710, payload["inherited_count"])
        self.assertEqual(30, payload["new_count"])
        self.assertEqual(2740, payload["effective_count"])
        self.assertTrue(payload["all_pass"])
        self.assertTrue(payload["human_semantic_review_completed"])
        self.assertLess(payload["maximum_similarity"], payload["threshold"])

    def test_frozen_chain_is_additive(self) -> None:
        payload = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(2710, payload["prior_count"])
        self.assertEqual(30, payload["new_count"])
        self.assertEqual(2740, payload["effective_count"])
        self.assertEqual(2710, len(payload["prior_proposals"]))
        self.assertEqual(30, len(payload["new_proposals"]))

    def test_primary_pillar_and_bounded_practice(self) -> None:
        payload = load("preregistration/proposal-ledger.json")
        self.assertIn("Freed ID", payload["primary_focus"])
        self.assertIn("CBR Heart", payload["primary_focus"])
        self.assertIn("archival motion-picture film", payload["bounded_practice"])
        self.assertIn("no real person", payload["bounded_practice"])

    def test_source_ledger_has_only_resolved_primary_ids(self) -> None:
        sources = load("sources/official-source-ledger.json")
        proposal = load("preregistration/proposal-ledger.json")
        known = {row["source_id"] for row in sources["sources"]}
        used = {source_id for row in proposal["proposals"] for source_id in row["official_or_primary_source_needs"]}
        self.assertTrue(used.issubset(known))
        self.assertGreaterEqual(len(known), 15)

    def test_hazard_and_authority_gates_remain_hard(self) -> None:
        proposals = {row["proposal_id"]: row for row in load("preregistration/proposal-ledger.json")["proposals"]}
        self.assertEqual("completed", proposals["V6583-P15"]["expected_disposition"])
        self.assertIn("no-testing or handling instruction", proposals["V6583-P15"]["title"])
        self.assertEqual("exact_gate", proposals["V6583-P30"]["expected_disposition"])
        self.assertEqual("not_executed_authority_reservation", proposals["V6583-P30"]["execution_lane"])

    def test_x1_has_no_x2_outcomes_or_implementation(self) -> None:
        truth = load("truth/x1-phase-truth.json")
        review = load("validation/x1-staged-review.json")
        self.assertFalse(truth["x2_implementation_present"])
        self.assertIsNone(truth["observed_outcome_counts"])
        self.assertEqual([], review["x2_implementation_paths"])
        self.assertEqual([], review["outcome_artifacts"])

    def test_failures_and_recoveries_are_paired(self) -> None:
        negatives = load("truth/retained-negative-register-x1.json")
        flow = load("method-flow/method-flow-state-x1.json")
        current = negatives["current_x1_operational_count"]
        self.assertEqual(current, flow["counts"]["current_methods"])
        self.assertEqual(current, flow["counts"]["current_witness_results"]["fail"])
        self.assertEqual(current, flow["counts"]["current_witness_results"]["pass"])
        self.assertTrue(negatives["all_retained"])

    def test_inherited_truth_is_preserved(self) -> None:
        negatives = load("truth/retained-negative-register-x1.json")
        open_gaps = load("truth/open-gap-register-x1.json")
        exact_gates = load("truth/exact-gate-register-x1.json")
        self.assertEqual(16831, negatives["inherited_effective_count"])
        self.assertEqual(114, open_gaps["inherited_effective_count"])
        self.assertEqual(113, exact_gates["inherited_effective_count"])

    def test_route_is_terminally_gated_and_unsent(self) -> None:
        route = load("orchestration/route-state-x1.json")
        self.assertEqual("Eiren Kestrel", route["next_exact_title"])
        self.assertEqual("v658-v4", route["next_phase"])
        self.assertEqual("Elaren Kestrel", route["next_successor_reminder"]["title"])
        self.assertEqual("ON_STANDBY", route["tavian_sol_state"])
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])

    def test_privacy_and_caps_are_clean(self) -> None:
        privacy = load("validation/x1-privacy-scan.json")
        files = load("validation/owner-file-threshold-x1.json")
        docs = load("validation/document-cap-receipt-x1.json")
        self.assertTrue(privacy["valid"])
        self.assertEqual(0, privacy["hit_count"])
        self.assertTrue(files["below_threshold"])
        self.assertTrue(docs["all_under_limit"])

    def test_manifest_declares_non_self_referential_domain(self) -> None:
        manifest = load("validation/x1-content-manifest.json")
        self.assertEqual("prospective Git-clean blob bytes", manifest["hash_domain"])
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertIn("validation/x1-content-manifest.json", manifest["self_exclusions"])

    def test_terminal_verdict_not_ready(self) -> None:
        truth = load("truth/x1-phase-truth.json")
        receipt = load("validation/x1-validation-receipt.json")
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", receipt["terminal_verdict"])


if __name__ == "__main__":
    unittest.main()

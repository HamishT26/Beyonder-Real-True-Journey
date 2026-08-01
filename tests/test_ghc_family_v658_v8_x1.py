#!/usr/bin/env python3
"""Scoped x1-only checks for Lyren Moss v658-v8."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v658_v8_phase_data as d  # noqa: E402


PHASE = ROOT / d.PHASE_ROOT


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class LyrenV658V8X1Tests(unittest.TestCase):
    def test_identity_is_relational_and_corrigible(self) -> None:
        payload = load("identity/identity-and-boundary.json")
        self.assertTrue(payload["relational_working_language_only"])
        self.assertTrue(payload["hamish_may_rename_pause_redirect_or_stop"])
        self.assertIn("Māori authority", payload["not_evidence_of"])
        self.assertEqual("Lyren Moss", payload["owner"])

    def test_exactly_thirty_unique_proposals(self) -> None:
        rows = load("preregistration/proposal-ledger.json")["proposals"]
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
        self.assertEqual(2860, payload["inherited_count"])
        self.assertEqual(30, payload["new_count"])
        self.assertEqual(2890, payload["effective_count"])
        self.assertTrue(payload["all_pass"])
        self.assertTrue(payload["human_semantic_review_completed"])
        self.assertLess(payload["maximum_similarity"], payload["threshold"])

    def test_frozen_chain_is_additive(self) -> None:
        payload = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(2860, payload["prior_count"])
        self.assertEqual(30, payload["new_count"])
        self.assertEqual(2890, payload["effective_count"])
        self.assertEqual(2860, len(payload["prior_proposals"]))
        self.assertEqual(30, len(payload["new_proposals"]))

    def test_primary_pillar_and_bounded_practice(self) -> None:
        payload = load("preregistration/proposal-ledger.json")
        for pillar in ("GMUT Mind", "THOS Body", "Freed ID", "CBR Heart"):
            self.assertIn(pillar, payload["primary_focus"])
        self.assertIn("brewery ingredient and package-lot records", payload["bounded_practice"])
        self.assertIn("no real person", payload["bounded_practice"])

    def test_source_ledger_has_only_resolved_primary_ids(self) -> None:
        sources = load("sources/official-source-ledger.json")
        proposals = load("preregistration/proposal-ledger.json")
        known = {row["source_id"] for row in sources["sources"]}
        used = {source_id for row in proposals["proposals"] for source_id in row["official_or_primary_source_needs"]}
        self.assertTrue(used.issubset(known))
        self.assertGreaterEqual(len(known), 18)

    def test_brewery_and_authority_gates_remain_hard(self) -> None:
        proposals = {row["proposal_id"]: row for row in load("preregistration/proposal-ledger.json")["proposals"]}
        self.assertEqual("completed", proposals["V6588-P01"]["expected_disposition"])
        self.assertIn("zero real batches", proposals["V6588-P01"]["title"])
        self.assertEqual("exact_gate", proposals["V6588-P30"]["expected_disposition"])
        self.assertEqual("not_executed_authority_reservation", proposals["V6588-P30"]["execution_lane"])

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

    def test_inherited_truth_and_external_route_failure_are_preserved(self) -> None:
        negatives = load("truth/retained-negative-register-x1.json")
        open_gaps = load("truth/open-gap-register-x1.json")
        exact_gates = load("truth/exact-gate-register-x1.json")
        source = load("startup/source-verification.json")
        self.assertEqual(17673, negatives["repository_sealed_source_count"])
        self.assertEqual(1, negatives["inherited_external_route_count"])
        self.assertEqual(17674, negatives["inherited_effective_count"])
        self.assertFalse(negatives["external_route_failure"]["folded_into_pass"])
        self.assertEqual(119, open_gaps["inherited_effective_count"])
        self.assertEqual(118, exact_gates["inherited_effective_count"])
        self.assertEqual(545, source["source_manifest_entries_replayed_read_only"])
        self.assertEqual(3948, source["activation_effective_methods"])

    def test_route_requires_fresh_live_authorization_and_is_unsent(self) -> None:
        route = load("orchestration/route-state-x1.json")
        self.assertEqual("Lyren Moss", route["active_exact_title"])
        self.assertIsNone(route["next_exact_title"])
        self.assertIsNone(route["next_phase"])
        self.assertFalse(route["successor_authorized"])
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
        for entry in manifest["entries"]:
            result = subprocess.run(
                ["git", "cat-file", "-s", entry["git_blob"]],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(int(result.stdout.strip()), entry["bytes"], entry["path"])

    def test_terminal_verdict_not_ready(self) -> None:
        truth = load("truth/x1-phase-truth.json")
        receipt = load("validation/x1-validation-receipt.json")
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", receipt["terminal_verdict"])


if __name__ == "__main__":
    unittest.main()

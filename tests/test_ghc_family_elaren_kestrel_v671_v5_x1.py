"""Planning-only contract tests for Elaren Kestrel v671-v5 x1."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "build_ghc_family_elaren_kestrel_v671_v5_x1.py"
SPEC = importlib.util.spec_from_file_location("elaren_v671_v5_x1", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ElarenV671V5X1Tests(unittest.TestCase):
    def test_identity_is_relational_and_corrigible(self) -> None:
        text = MODULE.IDENTITY_BOUNDARY
        self.assertIn("working language only", text)
        self.assertIn("not evidence of consciousness", text)
        self.assertIn("Hamish may rename, pause, redirect, or stop", text)

    def test_exact_source_chain_is_frozen(self) -> None:
        self.assertEqual(MODULE.SOURCE_START, "37ac80c499d43a90c874876402b262a220a252a1")
        self.assertEqual(MODULE.SOURCE_X1, "1c4d262b14cb8528fb9d72aad40a5e4fb7423b26")
        self.assertEqual(MODULE.SOURCE_EVIDENCE, "000c4c75ccac98794b43a0171f2d330436e6069d")
        self.assertEqual(MODULE.SOURCE_FINAL, "e70391872f07cdcaa13accac44d4330eca75e2b4")

    def test_canonical_failure_and_recovery_digests_are_distinct(self) -> None:
        self.assertNotEqual(MODULE.SOURCE_CANONICAL_SHA256, MODULE.SOURCE_RECOVERY_SHA256)
        self.assertNotEqual(
            MODULE.SOURCE_CANONICAL_PAYLOAD_SHA256,
            MODULE.SOURCE_RECOVERY_PAYLOAD_SHA256,
        )

    def test_new_proposal_count_and_title_uniqueness(self) -> None:
        self.assertEqual(len(MODULE.NEW_TITLES), 40)
        self.assertEqual(len(set(MODULE.NEW_TITLES)), 40)

    def test_new_proposal_rows_have_complete_contract(self) -> None:
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
        rows = MODULE.proposal_rows()
        self.assertEqual(len(rows), 40)
        self.assertTrue(all(required <= set(row) for row in rows))
        self.assertTrue(all(row["x1_state"] == "frozen_not_executed" for row in rows))

    def test_exact_planned_outcome_vector(self) -> None:
        rows = MODULE.proposal_rows()
        observed = {
            label: sum(row["expected_disposition"] == label for row in rows)
            for label in MODULE.CORE_OUTCOMES
        }
        self.assertEqual(observed, MODULE.NEW_OUTCOMES)
        self.assertEqual(set(observed), {"completed", "represented", "open_gap", "exact_gate"})

    def test_inherited_revalidations_are_zero_credit(self) -> None:
        rows = MODULE.inherited_revalidations()
        self.assertEqual(len(rows), 20)
        self.assertTrue(all(row["elaren_novelty_credit"] == 0 for row in rows))
        self.assertTrue(all(row["automatic_completion_credit"] == 0 for row in rows))
        self.assertTrue(all(row["source_commit"] == MODULE.SOURCE_FINAL for row in rows))

    def test_proposal_chain_extends_only_by_new_rows(self) -> None:
        self.assertEqual(MODULE.DECLARED_PROPOSAL_CHAIN, 5710)
        self.assertEqual(MODULE.PROPOSAL_CHAIN_AFTER, 5750)
        self.assertEqual(MODULE.PROPOSAL_CHAIN_AFTER - MODULE.DECLARED_PROPOSAL_CHAIN, 40)

    def test_portfolio_exact_counts(self) -> None:
        rows = MODULE.portfolio()
        self.assertEqual(
            {key: len(value) for key, value in rows.items()},
            {
                "safe_now": 60,
                "candidates": 30,
                "exact_approval": 20,
                "blocked": 10,
                "skill_ideas": 20,
                "runner_ideas": 10,
                "clean_fix_refine": 60,
                "successor_skill_recommendations": 10,
                "successor_runner_recommendations": 10,
                "successor_clean_fix_refine": 30,
            },
        )

    def test_exact_and_blocked_rows_are_held(self) -> None:
        rows = MODULE.portfolio()
        for key in ("exact_approval", "blocked"):
            self.assertTrue(all(row["x1_state"] == "held_unexecuted" for row in rows[key]))
            self.assertTrue(all(row["external_actions"] == 0 for row in rows[key]))

    def test_startup_failures_are_append_only_and_paired(self) -> None:
        flow = MODULE.startup_method_flow()
        self.assertEqual(flow["row_count"], len(MODULE.STARTUP_FAILURES))
        self.assertTrue(flow["all_failures_retained"])
        self.assertTrue(flow["all_recoveries_paired"])
        self.assertTrue(all(row["fail_witness"]["credit"] == 0 for row in flow["rows"]))
        self.assertTrue(all(row["pass_witness"]["credit"] == 1 for row in flow["rows"]))

    def test_startup_overlay_does_not_rewrite_source_layers(self) -> None:
        flow = MODULE.startup_method_flow()
        count = len(MODULE.STARTUP_FAILURES)
        self.assertEqual(
            flow["counts"]["effective_negatives"],
            MODULE.ACTIVATION_OVERLAY["effective_negatives"] + count,
        )
        self.assertEqual(MODULE.REPOSITORY_SEAL["effective_negatives"], 34088)
        self.assertEqual(MODULE.ACTIVATION_OVERLAY["effective_negatives"], 34089)

    def test_source_ledger_is_zero_ingestion(self) -> None:
        ledger = MODULE.public_source_ledger()
        self.assertEqual(ledger["adapter_calls"], 0)
        self.assertEqual(ledger["downloads"], 0)
        self.assertEqual(ledger["ingested_rows"], 0)
        self.assertEqual(ledger["external_writes"], 0)
        self.assertGreaterEqual(len(ledger["sources"]), 8)

    def test_threat_model_retains_route_and_authority_holds(self) -> None:
        payload = MODULE.threat_model()
        threats = {row["threat"] for row in payload["rows"]}
        self.assertIn("premature_route_send", threats)
        self.assertIn("Maori_authority_substitution", threats)
        self.assertIn("canonical_replay", threats)

    def test_x1_builder_source_contains_no_x2_output_path(self) -> None:
        text = MODULE_PATH.read_text(encoding="utf-8")
        self.assertNotIn('write_json("x2/', text)
        self.assertNotIn('write_text("x2/', text)

    def test_boundary_is_fail_closed(self) -> None:
        self.assertIn("NOT_READY_FOR_STAGE_20", MODULE.planning_overview(
            MODULE.proposal_rows(),
            MODULE.inherited_revalidations(),
            {"unique_titles": 1, "unique_proposal_ids": 1, "semantic_occurrences": 1},
            [{"jaccard": 0.0}],
            0.0,
            MODULE.startup_method_flow()["counts"],
        ))


if __name__ == "__main__":
    unittest.main()

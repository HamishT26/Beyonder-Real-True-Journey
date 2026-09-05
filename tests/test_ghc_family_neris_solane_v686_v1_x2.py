"""Behavioral checks for Neris Solane v686-v1 synthetic report evidence."""
from __future__ import annotations

import copy
import hashlib
import importlib
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"


def read(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


class X2Evidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposals = read("x1/new-proposals.json")["proposals"]
        cls.results = read("x2/contract-results.json")["records"]
        cls.invalid = read("x2/invalid-mutations.json")["records"]
        cls.portfolio = read("x2/portfolio-results.json")

    def test_x1_equality_preceded_execution(self):
        equality = read("x2/x1-equality.json")
        self.assertEqual(equality["head"], "d16badcebf9d3b9b7c4ee7b8156d27bfc5a42323")
        self.assertTrue(equality["clean"] and equality["four_way_equal"])
        self.assertEqual(equality["divergence"], "0\t0")

    def test_all_positive_contracts_pass(self):
        self.assertEqual(len(self.results), 200)
        self.assertTrue(all(row["result"]["accepted"] for row in self.results))
        self.assertTrue(all(row["result"]["tribunal"]["input_unchanged"] for row in self.results))

    def test_frozen_oracle_error_is_preserved_and_corrected_additively(self):
        correction = read("x2/oracle-corrections.json")["corrections"]
        self.assertEqual(len(correction), 1)
        self.assertEqual(correction[0]["proposal_id"], "NS6861-N040")
        self.assertEqual(correction[0]["success_credit_for_failed_attempt"], 0)
        self.assertIs(correction[0]["x1_rewritten"], False)
        row = next(item for item in self.results if item["proposal_id"] == "NS6861-N040")
        self.assertTrue(row["oracle_correction_applied"] and row["result"]["accepted"])

    def test_four_outcomes_are_exact(self):
        self.assertEqual(Counter(row["outcome"] for row in self.results), {"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10})

    def test_all_five_mutation_classes_are_retained(self):
        self.assertEqual(len(self.invalid), 1000)
        self.assertTrue(all(not row["result"]["accepted"] and row["completion_credit"] == 0 for row in self.invalid))
        self.assertEqual(Counter(row["mutation"] for row in self.invalid), {name: 200 for name in ["fabricated_report", "stale_definition_digest", "phase_epoch_inversion", "empirical_promotion", "authority_promotion"]})

    def test_portfolio_counts_and_execution(self):
        self.assertEqual(self.portfolio["counts"], {"safe_now": 300, "candidates": 250, "clean_fix_refine": 300, "exact_packets": 50, "blocked_packets": 30})
        self.assertEqual((self.portfolio["executed_count"], self.portfolio["executed_passed"]), (850, 850))

    def test_exact_and_blocked_stay_unexecuted(self):
        for key, outcome in [("exact_packets", "exact_gate"), ("blocked_packets", "open_gap")]:
            self.assertTrue(all(not row["operation_executed"] and row["outcome"] == outcome for row in self.portfolio[key]))

    def test_false_reports_are_retained_then_corrected(self):
        rows = [row for row in self.portfolio["clean_fix_refine"] if row["action"] == "retain_and_correct_false_report"]
        self.assertEqual(len(rows), 100)
        self.assertTrue(all(not row["artifact"]["failed_result"]["accepted"] and row["artifact"]["recovery_result"]["accepted"] for row in rows))
        self.assertTrue(all(row["artifact"]["deletion_count"] == 0 for row in rows))

    def test_minimal_views_exclude_only_working_note(self):
        rows = [row for row in self.portfolio["clean_fix_refine"] if row["action"] == "project_minimal_public_envelope"]
        self.assertEqual(len(rows), 100)
        self.assertTrue(all(row["passed"] and row["artifact"]["removed_field"] == "synthetic_working_note" for row in rows))

    def test_accessible_explanations_preserve_boundary(self):
        rows = [row for row in self.portfolio["clean_fix_refine"] if row["action"] == "derive_accessible_report_explanation"]
        self.assertEqual(len(rows), 100)
        self.assertTrue(all("does not establish" in row["artifact"]["text"] for row in rows))

    def test_trace_report_tribunal_rejects_fabrication(self):
        module = importlib.import_module("ghc_family_report_trace")
        data = {"events": [["a", 0, 0]]}
        self.assertTrue(module.evaluate("schedule", copy.deepcopy(data), ["a"])["accepted"])
        self.assertFalse(module.evaluate("schedule", copy.deepcopy(data), ["b"])["accepted"])

    def test_budget_report_tribunal_is_type_strict(self):
        module = importlib.import_module("ghc_family_report_budget")
        data = {"sequence": ["A"]}
        self.assertTrue(module.evaluate("allocation", copy.deepcopy(data), {"A": 1, "B": 0, "imbalance": 1})["accepted"])
        self.assertFalse(module.evaluate("allocation", copy.deepcopy(data), {"A": True, "B": 0, "imbalance": 1})["accepted"])

    def test_analysis_report_tribunal_preserves_fraction(self):
        module = importlib.import_module("ghc_family_report_analysis")
        data = {"values": [1, 2, 2], "stat": "mean"}
        self.assertTrue(module.evaluate("summary", copy.deepcopy(data), "5/3")["accepted"])
        self.assertFalse(module.evaluate("summary", copy.deepcopy(data), 5 / 3)["accepted"])

    def test_provenance_report_tribunal_preserves_cycles(self):
        module = importlib.import_module("ghc_family_report_provenance")
        data = {"nodes": ["a"], "edges": [["a", "a"]]}
        self.assertTrue(module.evaluate("lineage", copy.deepcopy(data), {"error": "cycle"})["accepted"])
        self.assertFalse(module.evaluate("lineage", copy.deepcopy(data), ["a"])["accepted"])

    def test_export_report_tribunal_preserves_gate_label(self):
        module = importlib.import_module("ghc_family_report_export")
        data = {"obligation": "competent review", "evidence": None, "authority": None, "disposition": "exact_gate"}
        self.assertTrue(module.evaluate("reservation", copy.deepcopy(data), "exact_gate")["accepted"])
        self.assertFalse(module.evaluate("reservation", copy.deepcopy(data), "completed")["accepted"])

    def test_summary_matches_full_evidence(self):
        summary = read("x2/contract-summary.json")
        self.assertEqual((summary["positive_accepted"], summary["invalid_rejected"]), (200, 1000))
        self.assertFalse(summary["independent_reproduction"])
        self.assertEqual(summary["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_method_flow_counts_and_links(self):
        ledger = read("x2/method-flow.json")
        self.assertEqual(ledger["counts"], {"methods": 1094, "failed_witnesses": 1144, "bounded_passing_witnesses": 1094, "retained_negatives": 1144})
        witnesses = {row["witness_id"]: row for row in ledger["witnesses"]}
        self.assertEqual(len(ledger["methods"]), 1094)
        self.assertTrue(all(any(witnesses[item]["result"] == "pass" for item in method["validation_witness_ids"]) for method in ledger["methods"]))
        self.assertTrue(all(method["repository_scan"] is False and method["cross_lane_scan"] is False and method["unchanged_history_scan"] is False and method["sibling_lane_mutation"] is False for method in ledger["methods"]))

    def test_phase_totals_keep_source_and_overlay_separate(self):
        truth = read("x2/phase-truth.json")
        self.assertEqual(truth["source_repository_seal"]["effective_negatives"], 65519)
        self.assertEqual(truth["source_activation_baseline"]["effective_negatives"], 65523)
        self.assertEqual(truth["totals"], {"effective_negatives": 66667, "effective_methods": 83162, "failed_witnesses": 37515, "bounded_passing_witnesses": 65007, "open_gaps": 602, "exact_gates": 589})
        self.assertEqual(truth["declared_proposal_chain"], 12430)

    def test_flashcard_deck_and_manifest(self):
        deck = read("x2/flashcards/deck-index.json")
        self.assertEqual(deck["card_count"], 208)
        self.assertEqual(deck["tier_counts"], {"1": 1, "2": 3, "3": 4, "4": 200})
        manifest = read("x2/flashcards/card-manifest.json")
        for row in manifest["entries"]:
            payload = (ROOT / row["path"]).read_bytes()
            self.assertEqual((len(payload), hashlib.sha256(payload).hexdigest()), (row["bytes"], row["sha256"]), row["path"])

    def test_baton_is_modular_and_within_bounds(self):
        index = read("x2/handoff/baton-index.json")
        self.assertEqual(index["section_count"], 13)
        self.assertTrue(10000 <= index["word_count"] <= 100000)
        self.assertEqual(index["delivery_state"], "PREPARED_NOT_SENT")

    def test_packages_and_smokes_are_exact(self):
        install = read("x2/toolchain/installation-receipt.json")
        smoke = read("x2/toolchain/package-smokes.json")
        self.assertEqual(install["direct_additions"], 3)
        self.assertEqual(len(install["installed_distributions"]), 3)
        self.assertEqual((smoke["positive_passed"], smoke["adverse_rejected"]), (3, 3))
        self.assertEqual(smoke["initial_aggregate_success_credit"], 0)

    def test_skill_promotions_have_byte_parity(self):
        local = read("x2/local-skills-validation.json")
        global_result = read("x2/global-promotion-installation.json")
        self.assertEqual((local["count"], global_result["installed_count"], global_result["unique_shared_report_runners"]), (10, 10, 5))
        self.assertTrue(all(row["byte_parity"] and row["post_copy_validation"]["valid"] and row["post_copy_smoke"]["positive"] and row["post_copy_smoke"]["adverse"] for row in global_result["skills"]))

    def test_operational_failures_are_retained(self):
        failures = read("x2/operational-failures.json")
        self.assertEqual(failures["count"], 13)
        self.assertEqual(failures["success_credit"], 0)
        self.assertTrue(all(row["success_credit"] == 0 and row["recovery_passed"] for row in failures["rows"]))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v644-v5"


def load_module(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODEL = load_module("scripts/ghc_family_v644_v5_model.py", "v644_v5_model")
DEFINITIONS = load_module("scripts/ghc_family_v644_v5_x1_definitions.py", "v644_v5_definitions")


class TestV644V5Models(unittest.TestCase):
    def test_all_ten_models_have_seven_mutations(self) -> None:
        self.assertEqual(10, len(MODEL.BASE_CASES))
        for proposal in DEFINITIONS.PROPOSALS:
            result = MODEL.proposal_cases(proposal["proposal_id"])
            self.assertEqual(7, result["case_count"], proposal["proposal_id"])
            self.assertEqual(7, result["matched_count"], proposal["proposal_id"])

    def test_structural_and_proxy_baselines_pass(self) -> None:
        expected_true = {
            "V6445-P01",
            "V6445-P02",
            "V6445-P04",
            "V6445-P05",
            "V6445-P07",
            "V6445-P08",
            "V6445-P09",
            "V6445-P10",
        }
        for proposal_id in expected_true:
            self.assertTrue(MODEL.proposal_cases(proposal_id)["baseline_accept"], proposal_id)

    def test_open_and_exact_baselines_do_not_cross_gate(self) -> None:
        self.assertFalse(MODEL.proposal_cases("V6445-P03")["baseline_accept"])
        self.assertFalse(MODEL.proposal_cases("V6445-P06")["baseline_accept"])

    def test_status_epoch_rollback_rejected(self) -> None:
        row = dict(MODEL.BASE_CASES["V6445-P05"])
        row["observed_epoch"] = row["issuer_epoch"] - 1
        self.assertFalse(MODEL.evaluate("V6445-P05", row))

    def test_entropy_psyche_conversion_rejected(self) -> None:
        row = dict(MODEL.BASE_CASES["V6445-P09"])
        row["psyche_conversion"] = True
        self.assertFalse(MODEL.evaluate("V6445-P09", row))

    def test_validation_budget_authority_substitution_rejected(self) -> None:
        row = dict(MODEL.BASE_CASES["V6445-P10"])
        row["authority_substitution"] = True
        self.assertFalse(MODEL.evaluate("V6445-P10", row))


class TestV644V5Artifacts(unittest.TestCase):
    def load(self, relative: str):
        return json.loads((PHASE / relative).read_text(encoding="utf-8"))

    def test_x2_distribution(self) -> None:
        ledger = self.load("x2-proposal-ledger.json")
        self.assertEqual(
            {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
            ledger["observed_distribution"],
        )
        self.assertEqual(70, ledger["total_case_count"])
        self.assertEqual(70, ledger["total_matched_count"])

    def test_all_deliverables_exist(self) -> None:
        for proposal in DEFINITIONS.PROPOSALS:
            for relative in proposal["deliverables"]:
                self.assertTrue((PHASE / relative).is_file(), relative)

    def test_negative_retention(self) -> None:
        register = self.load("retained-negative-register.json")
        self.assertEqual(1399, register["inherited_count"])
        self.assertEqual(1488, register["negative_count"])
        self.assertEqual(register["negative_count"], len(register["negatives"]))
        self.assertEqual([], register["duplicate_negative_ids"])
        self.assertTrue(register["all_retained"])
        self.assertFalse(register["erasure_permitted"])

    def test_gate_counts_remain_open(self) -> None:
        gates = self.load("exact-open-gate-register.json")
        self.assertEqual(5, gates["open_gap_count"])
        self.assertEqual(6, gates["exact_gate_count"])
        self.assertTrue(gates["none_silently_closed"])

    def test_method_flow_final_state(self) -> None:
        method = self.load("method-flow/method-flow-state.json")
        self.assertEqual(8, method["counts"]["methods"])
        self.assertEqual(8, method["counts"]["states"]["preferred"])
        self.assertEqual(0, method["counts"]["states"]["candidate"])
        self.assertGreaterEqual(method["counts"]["witness_results"]["fail"], 1)

    def test_method_validation_zero_issues(self) -> None:
        validation = self.load("method-flow/workaround-validation-ledger.json")
        self.assertTrue(validation["validation"]["valid"])
        self.assertEqual([], validation["pending_methods"])

    def test_lean_companion_is_additive(self) -> None:
        lean = self.load("repository/lean-companion-validation.json")
        self.assertTrue(lean["valid"])
        self.assertLess(lean["tracked_file_count"], 15000)
        self.assertFalse(lean["canonical_repository_replaced"])
        self.assertFalse(lean["public_remote_configured"])
        self.assertTrue(lean["targeted_test_passed"])
        self.assertFalse(lean["independent_reproduction"])

    def test_protected_claims_false(self) -> None:
        evidence = self.load("evidence/evidence-ledger.json")
        self.assertTrue(all(value is False for value in evidence["protected_claims"].values()))
        self.assertEqual("NOT_READY_FOR_STAGE_20", evidence["terminal_verdict"])

    def test_report_has_bypass_and_focus_contract(self) -> None:
        report = (PHASE / "deliverables/v644-v5-boundary-evidence-report.html").read_text(
            encoding="utf-8"
        )
        for marker in [
            'href="#main"',
            '<main id="main"',
            ":focus-visible",
            "<caption>",
            "NOT_READY_FOR_STAGE_20",
        ]:
            self.assertIn(marker, report)

    def test_overview_is_three_page_equivalent(self) -> None:
        words = (PHASE / "deliverables/v644-v5-final-integrated-overview.md").read_text(
            encoding="utf-8"
        ).split()
        self.assertGreaterEqual(len(words), 1200)

    def test_phase_truth_has_no_outbound_action(self) -> None:
        truth = self.load("phase-truth.json")
        self.assertEqual(0, truth["outbound_message_count"])
        self.assertEqual(0, truth["successor_task_count"])
        self.assertEqual("ACTIVE_SOLO; PREPARED_NOT_SENT", truth["route_state"])

    def test_source_status_vocabulary_preserved(self) -> None:
        source = self.load("sources/source-ledger.json")
        self.assertEqual(200, source["effective_source_count"])
        self.assertTrue(set(source["effective_status_counts"]).issubset({"current", "stable", "draft", "watch"}))

    def test_dispositions_use_only_allowed_vocabulary(self) -> None:
        ledger = self.load("x2-proposal-ledger.json")
        observed = Counter(row["observed_disposition"] for row in ledger["rows"])
        self.assertEqual(Counter(ledger["observed_distribution"]), observed)
        self.assertTrue(set(observed).issubset({"completed", "represented", "open_gap", "exact_gate"}))


if __name__ == "__main__":
    unittest.main()

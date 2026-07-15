from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v644-v7"
sys.path.insert(0, str(ROOT / "scripts"))


def load_module(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODEL = load_module("scripts/ghc_family_v644_v7_model.py", "v644_v7_model")
DEFINITIONS = load_module("scripts/ghc_family_v644_v7_x1_definitions.py", "v644_v7_definitions")
TRIBUNALS = load_module("scripts/ghc_family_obligation_tribunals.py", "ghc_family_obligation_tribunals_test")


class TestV644V7Models(unittest.TestCase):
    def test_all_ten_models_have_seven_matched_mutations(self) -> None:
        self.assertEqual(10, len(MODEL.BASE_CASES))
        for proposal in DEFINITIONS.PROPOSALS:
            result = MODEL.proposal_cases(proposal["proposal_id"])
            self.assertEqual(7, result["case_count"])
            self.assertEqual(7, result["matched_count"])

    def test_structural_and_proxy_baselines_pass(self) -> None:
        for proposal_id in {"V6447-P01", "V6447-P03", "V6447-P04", "V6447-P05", "V6447-P07", "V6447-P08", "V6447-P09", "V6447-P10"}:
            self.assertTrue(MODEL.proposal_cases(proposal_id)["baseline_accept"], proposal_id)

    def test_open_and_exact_baselines_do_not_cross_gate(self) -> None:
        self.assertFalse(MODEL.proposal_cases("V6447-P02")["baseline_accept"])
        self.assertFalse(MODEL.proposal_cases("V6447-P06")["baseline_accept"])

    def test_disclosure_outside_request_rejected(self) -> None:
        row = dict(MODEL.BASE_CASES["V6447-P05"])
        row["disclosed_elements"] = ["org.iso.18013.5.1.resident_address"]
        self.assertFalse(MODEL.evaluate("V6447-P05", row))

    def test_raw_diagnostic_material_rejected(self) -> None:
        row = dict(MODEL.BASE_CASES["V6447-P08"])
        row["raw_identifiers_present"] = True
        self.assertFalse(MODEL.evaluate("V6447-P08", row))

    def test_psyche_conversion_rejected(self) -> None:
        row = dict(MODEL.BASE_CASES["V6447-P09"])
        row["psyche_conversion"] = True
        self.assertFalse(MODEL.evaluate("V6447-P09", row))

    def test_unknown_reusable_tribunal_rejected(self) -> None:
        with self.assertRaises(KeyError):
            TRIBUNALS.evaluate_tribunal("missing", {})


class TestV644V7Artifacts(unittest.TestCase):
    def load(self, relative: str):
        return json.loads((PHASE / relative).read_text(encoding="utf-8"))

    def test_x2_distribution_and_cases(self) -> None:
        ledger = self.load("x2-proposal-ledger.json")
        self.assertEqual({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, ledger["observed_distribution"])
        self.assertEqual(70, ledger["total_case_count"])
        self.assertEqual(70, ledger["total_matched_count"])

    def test_all_deliverables_exist(self) -> None:
        for proposal in DEFINITIONS.PROPOSALS:
            for relative in proposal["deliverables"]:
                self.assertTrue((PHASE / relative).is_file(), relative)

    def test_negative_retention(self) -> None:
        register = self.load("retained-negative-register.json")
        self.assertEqual(1584, register["inherited_effective_count"])
        self.assertEqual(7, register["x1_operational_count"])
        self.assertEqual(70, register["new_synthetic_count"])
        self.assertGreaterEqual(register["negative_count"], 1661)
        self.assertEqual(
            register["inherited_effective_count"]
            + register["x1_operational_count"]
            + register["x2_operational_count"]
            + register["new_synthetic_count"],
            register["negative_count"],
        )
        self.assertEqual(register["negative_count"], len(register["negatives"]))
        self.assertEqual([], register["duplicate_negative_ids"])
        self.assertTrue(register["all_retained"])

    def test_gate_counts_remain_open(self) -> None:
        gates = self.load("exact-open-gate-register.json")
        self.assertEqual(5, gates["open_gap_count"])
        self.assertEqual(6, gates["exact_gate_count"])
        self.assertTrue(gates["none_silently_closed"])

    def test_protected_claims_false(self) -> None:
        evidence = self.load("evidence/evidence-ledger.json")
        self.assertTrue(all(value is False for value in evidence["protected_claims"].values()))
        self.assertTrue(all(value == 0 for value in evidence["real_or_external_counts"].values()))
        self.assertEqual("NOT_READY_FOR_STAGE_20", evidence["terminal_verdict"])

    def test_static_report_has_figure_equivalents(self) -> None:
        report = (PHASE / "deliverables/v644-v7-boundary-evidence-report.html").read_text(encoding="utf-8")
        for marker in ['href="#main"', '<main id="main"', ":focus-visible", 'role="img"', "<figcaption>", 'id="distribution-long"', "Underlying disposition data"]:
            self.assertIn(marker, report)

    def test_overview_is_three_page_equivalent(self) -> None:
        words = (PHASE / "deliverables/v644-v7-final-integrated-overview.md").read_text(encoding="utf-8").split()
        self.assertGreaterEqual(len(words), 1200)

    def test_phase_truth_has_no_outbound_action(self) -> None:
        truth = self.load("phase-truth.json")
        self.assertEqual(0, truth["outbound_message_count"])
        self.assertEqual(0, truth["successor_task_count"])
        self.assertEqual("ACTIVE_SOLO; PREPARED_NOT_SENT", truth["route_state"])

    def test_source_status_vocabulary_preserved(self) -> None:
        source = self.load("sources/source-ledger.json")
        self.assertEqual(214, source["effective_source_count"])
        self.assertTrue(set(source["effective_status_counts"]) <= {"current", "stable", "draft", "watch"})

    def test_dispositions_use_only_allowed_vocabulary(self) -> None:
        ledger = self.load("x2-proposal-ledger.json")
        observed = Counter(row["observed_disposition"] for row in ledger["rows"])
        self.assertEqual(Counter(ledger["observed_distribution"]), observed)
        self.assertTrue(set(observed) <= {"completed", "represented", "open_gap", "exact_gate"})

    def test_method_flow_retains_final_replay_candidate(self) -> None:
        method = self.load("method-flow/method-flow-state.json")
        states = {row["method_id"]: row["recommendation_state"] for row in method["methods"]}
        self.assertEqual("candidate", states["V6447-M01"])
        self.assertEqual("preferred", states["V6447-M09"])

    def test_manifest_is_same_owner_only(self) -> None:
        manifest = self.load("reproduction/evidence-manifest.json")
        self.assertTrue(manifest["same_owner_repeatability_only"])
        self.assertFalse(manifest["independent_team_reproduction"])


if __name__ == "__main__":
    unittest.main()

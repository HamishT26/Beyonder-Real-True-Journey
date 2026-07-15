from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v645-v2"
sys.path.insert(0, str(ROOT / "scripts"))


def load_module(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODEL = load_module("scripts/ghc_family_v645_v2_model.py", "v645_v2_model")
DEFINITIONS = load_module("scripts/ghc_family_v645_v2_x1_definitions.py", "v645_v2_definitions")
STAGE = load_module("scripts/ghc_family_index_stage_guard.py", "ghc_family_index_stage_guard_test")


class TestV645V2Models(unittest.TestCase):
    def test_all_ten_models_have_seven_matched_mutations(self) -> None:
        self.assertEqual(10, len(MODEL.BASE_CASES))
        for proposal in DEFINITIONS.PROPOSALS:
            result = MODEL.proposal_cases(proposal["proposal_id"])
            self.assertEqual(7, result["case_count"])
            self.assertEqual(7, result["matched_count"])

    def test_completed_and_proxy_baselines_pass(self) -> None:
        for proposal_id in {
            "V6452-P01", "V6452-P02", "V6452-P04", "V6452-P05",
            "V6452-P07", "V6452-P08", "V6452-P09", "V6452-P10",
        }:
            self.assertTrue(MODEL.proposal_cases(proposal_id)["baseline_accept"], proposal_id)

    def test_open_and_exact_baselines_do_not_cross_gate(self) -> None:
        self.assertFalse(MODEL.proposal_cases("V6452-P03")["baseline_accept"])
        self.assertFalse(MODEL.proposal_cases("V6452-P06")["baseline_accept"])

    def test_open_gap_cannot_be_promoted_by_single_field(self) -> None:
        row = dict(MODEL.BASE_CASES["V6452-P03"])
        row["official_strain_rows"] = 1
        self.assertFalse(MODEL.evaluate("V6452-P03", row))

    def test_exact_gate_cannot_be_promoted_by_single_authority_flag(self) -> None:
        row = dict(MODEL.BASE_CASES["V6452-P06"])
        row["competent_legal_authority"] = True
        self.assertFalse(MODEL.evaluate("V6452-P06", row))

    def test_psyche_conversion_rejected(self) -> None:
        row = dict(MODEL.BASE_CASES["V6452-P09"])
        row["psyche_conversion"] = True
        self.assertFalse(MODEL.evaluate("V6452-P09", row))

    def test_unknown_proposal_rejected(self) -> None:
        with self.assertRaises(KeyError):
            MODEL.proposal_cases("missing")

    def stage_record(self, stage: int, path: bytes = b"file.txt") -> bytes:
        return b"100644 " + (b"a" * 40) + b" " + str(stage).encode() + b"\t" + path + b"\0"

    def test_stage_guard_accepts_stage_zero_and_empty_input(self) -> None:
        ordinary = STAGE.classify_stage_bytes(self.stage_record(0))
        empty = STAGE.classify_stage_bytes(b"")
        self.assertTrue(ordinary["accepted"] and empty["accepted"])
        self.assertEqual("stage_zero_only", ordinary["classification"])

    def test_stage_guard_rejects_higher_stages_and_multiplicity(self) -> None:
        data = self.stage_record(1) + self.stage_record(2) + self.stage_record(3)
        result = STAGE.classify_stage_bytes(data)
        self.assertFalse(result["accepted"])
        self.assertEqual(3, result["higher_stage_count"])
        self.assertEqual(1, result["multiplicity_path_count"])
        self.assertEqual(0, result["index_mutation_count"])

    def test_stage_guard_rejects_malformed_streams_without_mutation(self) -> None:
        for data in [b"10064 " + (b"a" * 40) + b" 0\tbad\0", self.stage_record(0)[:-1]]:
            result = STAGE.classify_stage_bytes(data)
            self.assertEqual("malformed_stage_stream", result["classification"])
            self.assertFalse(result["accepted"])
            self.assertEqual(0, result["index_mutation_count"])


class TestV645V2Artifacts(unittest.TestCase):
    def load(self, relative: str):
        return json.loads((PHASE / relative).read_text(encoding="utf-8"))

    def test_x2_distribution_and_cases(self) -> None:
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
        self.assertEqual(1833, register["inherited_effective_count"])
        self.assertEqual(10, register["x1_operational_count"])
        self.assertGreaterEqual(register["x2_operational_count"], 2)
        self.assertEqual(70, register["new_synthetic_count"])
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

    def test_static_report_has_visible_equivalents(self) -> None:
        report = (PHASE / "deliverables/v645-v2-static-report.html").read_text(encoding="utf-8")
        for marker in [
            'href="#main"', '<main id="main"', ":focus-visible", 'role="img"',
            "<figcaption>", 'id="distribution-long"', "Underlying disposition data",
        ]:
            self.assertIn(marker, report)
        self.assertNotIn("::before", report)
        self.assertNotIn("::after", report)
        self.assertIn("<title>Sylven Arc v645-v2 THOS boundary evidence report</title>", report)
        self.assertNotIn("http-equiv=\"refresh\"", report.lower())
        self.assertNotIn("setTimeout(", report)

    def test_overview_is_three_page_equivalent(self) -> None:
        words = (PHASE / "deliverables/v645-v2-final-integrated-overview.md").read_text(encoding="utf-8").split()
        self.assertGreaterEqual(len(words), 1200)

    def test_phase_truth_has_no_outbound_action(self) -> None:
        truth = self.load("phase-truth.json")
        self.assertEqual("THOS Body", truth["primary_focus"])
        self.assertEqual(0, truth["outbound_message_count"])
        self.assertEqual(0, truth["successor_task_count"])
        self.assertEqual("ACTIVE_SOLO; PREPARED_NOT_SENT", truth["route_state"])
        self.assertFalse(truth["full_repository_suite_run"])

    def test_source_status_vocabulary_preserved(self) -> None:
        source = self.load("sources/source-ledger.json")
        self.assertEqual(234, source["effective_source_count"])
        self.assertTrue(set(source["effective_status_counts"]) <= {"current", "stable", "draft", "watch"})

    def test_dispositions_use_only_allowed_vocabulary(self) -> None:
        ledger = self.load("x2-proposal-ledger.json")
        observed = Counter(row["observed_disposition"] for row in ledger["rows"])
        self.assertEqual(Counter(ledger["observed_distribution"]), observed)
        self.assertTrue(set(observed) <= {"completed", "represented", "open_gap", "exact_gate"})

    def test_method_flow_retains_recovery_boundaries(self) -> None:
        method = self.load("method-flow/method-flow-state.json")
        states = {row["method_id"]: row["recommendation_state"] for row in method["methods"]}
        self.assertEqual("validated", states["v6452-m11"])
        self.assertEqual("validated", states["v6452-m12"])
        self.assertNotIn("candidate", states.values())

    def test_index_stage_runner_is_read_only_and_summarized(self) -> None:
        receipt = self.load("tooling/index-stage-guard-runner-receipt.json")
        current = receipt["current_index"]
        self.assertTrue(receipt["all_expected"])
        self.assertTrue(current["accepted"])
        self.assertTrue(current["index_stream_unchanged"])
        self.assertEqual(0, current["index_mutation_count"])
        self.assertNotIn("rows", current)

    def test_manifest_is_same_owner_only(self) -> None:
        manifest = self.load("reproduction/evidence-manifest.json")
        self.assertTrue(manifest["same_owner_repeatability_only"])
        self.assertFalse(manifest["independent_team_reproduction"])


if __name__ == "__main__":
    unittest.main()

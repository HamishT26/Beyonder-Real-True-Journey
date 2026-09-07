"""Owner-scoped tests for Liora v688-v1 caption contracts."""
from __future__ import annotations

import copy
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_caption_evidence_core import altered_output, evaluate, exact_type_equal, output_matches
from ghc_family_liora_venn_v688_v1_fixtures import build_cases


class CaptionContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = build_cases()

    def operation(self, name):
        rows = [row for row in self.cases if row["operation"] == name]
        self.assertEqual(len(rows), 20)
        for row in rows:
            self.assertTrue(output_matches(evaluate(copy.deepcopy(row["input"])), row["expected_output"]), row["proposal_id"])

    def test_01_fixture_count(self):
        self.assertEqual(len(self.cases), 200)

    def test_02_outcomes(self):
        self.assertEqual(Counter(row["expected_execution_disposition"] for row in self.cases), {"completed": 160, "represented": 14, "open_gap": 8, "exact_gate": 18})

    def test_03_distinct_inputs(self):
        self.assertEqual(len({repr(row["input"]) for row in self.cases}), 200)

    def test_04_vtt_timestamp(self): self.operation("vtt_timestamp")
    def test_05_srt_timestamp(self): self.operation("srt_timestamp")
    def test_06_cue_interval(self): self.operation("cue_interval")
    def test_07_frame_timebase(self): self.operation("frame_timebase")
    def test_08_cue_order(self): self.operation("cue_order")
    def test_09_payload_text(self): self.operation("payload_text")
    def test_10_language_tag(self): self.operation("language_tag")
    def test_11_derivative_linkage(self): self.operation("derivative_linkage")
    def test_12_accessibility_claim(self): self.operation("accessibility_claim")
    def test_13_publication_gate(self): self.operation("publication_gate")

    def test_14_input_preservation(self):
        for row in self.cases:
            payload = copy.deepcopy(row["input"])
            before = copy.deepcopy(payload)
            evaluate(payload)
            self.assertTrue(exact_type_equal(payload, before), row["proposal_id"])

    def test_15_missing_accepted_rejected(self): self._mutation("missing_accepted")
    def test_16_accepted_type_rejected(self): self._mutation("accepted_type")
    def test_17_extra_authority_rejected(self): self._mutation("extra_authority")
    def test_18_value_replaced_rejected(self): self._mutation("value_replaced")
    def test_19_external_credit_rejected(self): self._mutation("external_credit_promoted")

    def _mutation(self, name):
        for row in self.cases[::4]:
            self.assertFalse(output_matches(altered_output(row["expected_output"], name), row["expected_output"]), row["proposal_id"])

    def test_20_boolean_is_not_integer(self):
        self.assertFalse(exact_type_equal(True, 1))

    def test_21_dictionary_key_set_is_exact(self):
        self.assertFalse(exact_type_equal({"a": 1}, {"a": 1, "b": 2}))

    def test_22_list_types_are_exact(self):
        self.assertFalse(exact_type_equal([1], [True]))

    def test_23_unknown_operation_is_held(self):
        self.assertEqual(evaluate({"operation": "unknown"})["error"], "OPERATION")

    def test_24_nonrecord_is_held(self):
        self.assertEqual(evaluate([])["error"], "RECORD_TYPE")

    def test_25_no_external_credit(self):
        self.assertTrue(all(evaluate(row["input"])["external_credit"] is False for row in self.cases))

    def test_26_no_authority_promotion(self):
        for row in self.cases:
            result = evaluate(row["input"])
            self.assertNotIn("authority_granted", result)

    def test_27_exact_gate_actions_not_executed(self):
        for row in self.cases:
            if row["expected_execution_disposition"] == "exact_gate":
                self.assertIs(evaluate(row["input"])["value"]["executed_external_action"], False)

    def test_28_terminal_labels_are_closed(self):
        self.assertEqual(set(Counter(row["expected_execution_disposition"] for row in self.cases)), {"completed", "represented", "open_gap", "exact_gate"})


if __name__ == "__main__":
    unittest.main()

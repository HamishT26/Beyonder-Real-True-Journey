from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/lyren-moss/v690-v1"
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_error_control_x1 import _hamming74_encode, run


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class LyrenV690V1X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = load(BASE / "plan/new-proposals.json")["proposals"][:100]
        cls.results = load(BASE / "x1/results.json")["results"]
        cls.candidates = load(BASE / "x1/candidate-subjects.json")["records"]

    def test_exact_frozen_results(self):
        self.assertEqual(len(self.plan), 100)
        self.assertEqual(len(self.results), 100)
        for proposal, report in zip(self.plan, self.results):
            request = copy.deepcopy(proposal["request"])
            before = copy.deepcopy(request)
            self.assertEqual(run(request), proposal["expected"], proposal["proposal_id"])
            self.assertEqual(request, before, proposal["proposal_id"])
            self.assertTrue(report["passed"])
            self.assertEqual(report["observed"], proposal["expected"])

    def test_all_candidates_are_retained_and_refused(self):
        self.assertEqual(len(self.candidates), 100)
        by_id = {row["proposal_id"]: row for row in self.candidates}
        for proposal in self.plan:
            subject = copy.deepcopy(proposal["candidate_subject"])
            before = copy.deepcopy(subject)
            self.assertEqual(run(subject), proposal["candidate_expected"])
            self.assertEqual(subject, before)
            record = by_id[proposal["proposal_id"]]
            self.assertEqual(record["original_success_credit"], 0)
            self.assertTrue(record["refusal_check_passed"])

    def test_hamming_single_bit_correction(self):
        for data in ["0000", "0001", "0110", "1010", "1111"]:
            codeword = _hamming74_encode(data)
            for position in range(7):
                damaged = list(codeword)
                damaged[position] = "1" if damaged[position] == "0" else "0"
                result = run({"operation": "hamming74_correct", "payload": {"codeword": "".join(damaged)}})
                self.assertTrue(result["ok"])
                self.assertEqual(result["value"]["corrected"], codeword)
                self.assertEqual(result["value"]["post_syndrome"], 0)

    def test_hamming_contract_names_assumed_model(self):
        result = run({"operation": "hamming74_correct", "payload": {"codeword": "0000000"}})
        self.assertEqual(result["value"]["assumed_model"], "at_most_one_bit_error")

    def test_repetition_decode_one_error(self):
        encoded = run({"operation": "repetition_encode", "payload": {"bits": "101", "copies": 3}})["value"]["codeword"]
        damaged = list(encoded)
        damaged[4] = "1" if damaged[4] == "0" else "0"
        result = run({"operation": "repetition_decode", "payload": {"codeword": "".join(damaged), "copies": 3}})
        self.assertEqual(result["value"]["decoded"], "101")
        self.assertEqual(result["value"]["disagreement_groups"], [1])

    def test_even_repetition_group_is_refused(self):
        result = run({"operation": "repetition_decode", "payload": {"codeword": "0011", "copies": 2}})
        self.assertFalse(result["ok"])
        self.assertEqual(result["original_success_credit"], 0)

    def test_crc_reference_vector(self):
        remainder = run({"operation": "crc_remainder", "payload": {"data": "1101", "polynomial": "1011"}})
        self.assertEqual(remainder["value"]["remainder"], "001")
        self.assertFalse(remainder["value"]["cryptographic"])

    def test_unknown_payload_field_is_refused(self):
        request = {"operation": "even_parity_append", "payload": {"bits": "101", "authority": True}}
        before = copy.deepcopy(request)
        self.assertEqual(run(request), {"ok": False, "error": "unknown_payload_field", "original_success_credit": 0})
        self.assertEqual(request, before)

    def test_refinements_are_lossless(self):
        rows = load(BASE / "x1/refinements.json")["records"]
        self.assertEqual(len(rows), 100)
        self.assertTrue(all(row["lossless"] for row in rows))
        self.assertTrue(all(row["novelty_credit"] == 0 and row["execution_credit"] == 0 for row in rows))
        self.assertTrue(all(not row["host_cleanup"] for row in rows))

    def test_package_smokes(self):
        receipt = load(BASE / "x1/toolchain/package-smokes.json")
        self.assertTrue(receipt["passed"])
        self.assertEqual(receipt["positive_witnesses"], 3)
        self.assertEqual(receipt["adverse_subjects"], 3)
        self.assertEqual(receipt["versions"]["bitstring"], "4.4.0")
        self.assertEqual(receipt["versions"]["reedsolo"], "1.7.0")
        self.assertEqual(receipt["versions"]["crccheck"], "1.3.1")

    def test_wheel_hashes(self):
        receipt = load(BASE / "x1/toolchain/wheel-manifest.json")
        self.assertEqual(len(receipt["records"]), 5)
        self.assertTrue(receipt["all_hashes_match"])
        self.assertTrue(all(row["hash_match"] for row in receipt["records"]))

    def test_skill_validation(self):
        receipt = load(BASE / "x1/skills-validation.json")
        self.assertEqual(receipt["count"], 10)
        self.assertTrue(receipt["all_passed"])
        self.assertTrue(all(row["passed"] for row in receipt["records"]))
        self.assertEqual(len(list((BASE / "x1/skills").iterdir())), 10)

    def test_runner_smokes(self):
        receipt = load(BASE / "x1/tooling/runner-smokes.json")
        self.assertEqual(receipt["count"], 5)
        self.assertTrue(receipt["all_passed"])

    def test_method_flow_counts_and_unique_ids(self):
        ledger = load(BASE / "x1/method-flow.json")
        self.assertEqual(ledger["counts"], {"methods": 15, "witnesses": 426, "failed_witnesses": 110, "passing_witnesses": 316, "retained_negatives": 110})
        self.assertEqual(len({row["method_id"] for row in ledger["methods"]}), 15)
        self.assertEqual(len({row["witness_id"] for row in ledger["witnesses"]}), 426)
        self.assertTrue(all(not row["independent_reproduction"] for row in ledger["witnesses"]))

    def test_negative_index_preserves_zero_credit(self):
        index = load(BASE / "x1/negative-index.json")
        self.assertEqual(index["count"], 110)
        self.assertTrue(index["all_original_success_credit_zero"])
        self.assertTrue(all(row["original_success_credit"] == 0 and row["retained"] for row in index["records"]))

    def test_post_validation_overlay(self):
        overlay = load(BASE / "x1/post-validation-overlay.json")
        self.assertEqual(len(overlay["retained_negatives"]), 3)
        self.assertEqual(
            overlay["effective_counts"],
            {"methods": 16, "retained_negatives": 113, "witnesses": 430, "failed_witnesses": 113, "passing_witnesses": 317},
        )
        self.assertEqual(overlay["recovery"]["result"], "pass")

    def test_completion_ledger(self):
        ledger = load(BASE / "x1/completion-ledger.json")
        self.assertEqual(ledger["counts"], {"completed": 100, "represented": 0, "open_gap": 0, "exact_gate": 0})
        self.assertEqual(ledger["safe_tasks"], 100)
        self.assertEqual(ledger["candidate_subjects"], 100)
        self.assertEqual(ledger["clean_fix_refine"], 100)

    def test_manifest_raw_bytes(self):
        manifest = load(BASE / "x1/manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            path = ROOT / entry["path"]
            self.assertTrue(path.is_file(), entry["path"])
            self.assertEqual(path.stat().st_size, entry["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry["sha256"])

    def test_strict_x1_before_x2(self):
        truth = load(BASE / "x1/phase-truth.json")
        self.assertFalse(truth["x2_started"])
        self.assertFalse((BASE / "x2").exists())
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()

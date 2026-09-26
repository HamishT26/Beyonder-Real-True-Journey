from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


X1_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(X1_ROOT / "code"))

import event_workflow as ew


class EventWorkflowX1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = ew.load_fixtures()
        cls.contracts = ew.load_contracts("x1")

    def test_01_contract_count(self):
        self.assertEqual(150, len(self.contracts))

    def test_02_fixture_count(self):
        self.assertEqual(15, len(self.fixtures))

    def test_03_fixture_digest(self):
        self.assertTrue(all(row["fixture_sha256"] == ew.fixture_digest(row) for row in self.fixtures.values()))

    def test_04_request_digest(self):
        self.assertTrue(all(row["request_sha256"] == ew.sha256_json(row["request"]) for row in self.contracts))

    def test_05_record_shape(self):
        self.assertTrue(ew.record_shape(self.fixtures["LEW-01"])["record_valid"])

    def test_06_event_sequence(self):
        self.assertTrue(ew.event_sequence(self.fixtures["LEW-02"])["contiguous"])

    def test_07_transition_legality(self):
        self.assertTrue(ew.transition_legality(self.fixtures["LEW-01"])["legal"])

    def test_08_idempotency_consistency(self):
        row = ew.idempotency_consistency(self.fixtures["LEW-07"])
        self.assertEqual(["REQ-07"], row["duplicate_request_ids"])
        self.assertTrue(row["consistent"])

    def test_09_attempt_budget_classifies_violation(self):
        self.assertFalse(ew.attempt_budget(self.fixtures["LEW-03"])["within_budget"])

    def test_10_retry_never_assumes_capability(self):
        self.assertFalse(ew.retry_decision(self.fixtures["LEW-04"])["retry_recommended"])

    def test_11_acknowledgement_requires_explicit_event(self):
        self.assertTrue(ew.acknowledgement_reduce(self.fixtures["LEW-05"])["explicitly_acknowledged"])
        self.assertFalse(ew.acknowledgement_reduce(self.fixtures["LEW-04"])["explicitly_acknowledged"])

    def test_12_duplicate_guard_has_no_external_action(self):
        row = ew.duplicate_guard(self.fixtures["LEW-07"])
        self.assertTrue(row["duplicate_detected"])
        self.assertFalse(row["new_external_action_executed"])

    def test_13_capability_intersection_does_not_widen(self):
        row = ew.capability_intersection(self.fixtures["LEW-08"])
        self.assertIn("send_native", row["denied"])
        self.assertFalse(row["authority_widened"])

    def test_14_authority_vacancy_stays_closed(self):
        row = ew.authority_vacancy(self.fixtures["LEW-13"])
        self.assertFalse(row["authority_gate_open"])
        self.assertIn("competent_review", row["missing_authorities"])

    def test_15_malformed_contracts_are_rejected(self):
        contract = self.contracts[0]
        fixture = self.fixtures[contract["request"]["fixture_id"]]
        for mutation in ("missing_request_schema", "request_digest_mismatch"):
            with self.assertRaises(ew.ContractError):
                ew.execute_contract(ew.mutated_contract(contract, mutation), fixture)


if __name__ == "__main__":
    unittest.main()

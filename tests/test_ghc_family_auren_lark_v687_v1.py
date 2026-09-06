from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_auren_lark_v687_v1_core import OPERATIONS, execute, typed_equal


X1 = ROOT / "docs/auren-lark/v687-v1/x1/new-proposals.json"
PROPOSALS = json.loads(X1.read_text(encoding="utf-8"))["proposals"]


class AurenV687V1Contracts(unittest.TestCase):
    maxDiff = None


def make_case_test(case: dict[str, object]):
    def test(self: AurenV687V1Contracts) -> None:
        before = json.dumps(case["input"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        observed = execute(case["operation"], case["input"])
        after = json.dumps(case["input"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.assertTrue(typed_equal(observed, case["expected_value"]), msg=f"{case['id']}: {observed!r} != {case['expected_value']!r}")
        self.assertEqual(before, after, msg=f"{case['id']} mutated the frozen input")
    return test


for proposal in PROPOSALS:
    setattr(AurenV687V1Contracts, f"test_{proposal['id'].lower().replace('-', '_')}", make_case_test(proposal))


class AurenV687V1CrossContractTests(unittest.TestCase):
    def test_exact_case_count(self) -> None:
        self.assertEqual(len(PROPOSALS), 200)

    def test_exact_operation_count(self) -> None:
        self.assertEqual(len(OPERATIONS), 10)

    def test_twenty_cases_per_operation(self) -> None:
        self.assertEqual({op: sum(row["operation"] == op for row in PROPOSALS) for op in OPERATIONS}, {op: 20 for op in OPERATIONS})

    def test_identifiers_unique(self) -> None:
        self.assertEqual(len({row["id"] for row in PROPOSALS}), 200)

    def test_titles_unique(self) -> None:
        self.assertEqual(len({row["title"] for row in PROPOSALS}), 200)

    def test_unknown_operation_rejected(self) -> None:
        self.assertEqual(execute("unknown", {}), {"error": "UNKNOWN_OPERATION"})

    def test_all_universal_mutations_rejected(self) -> None:
        for row in PROPOSALS:
            observed = execute(row["operation"], {"__invalid_mutation__": row["id"]})
            self.assertIsInstance(observed, dict)
            self.assertIn("error", observed)

    def test_only_four_expected_dispositions(self) -> None:
        allowed = {"completed", "represented", "open_gap", "exact_gate"}
        self.assertTrue(all(row["expected_execution_disposition"] in allowed for row in PROPOSALS))

    def test_stage20_protected_everywhere(self) -> None:
        self.assertTrue(all("stage20" in row["protected_gates"] for row in PROPOSALS))

    def test_same_owner_scope_is_explicit(self) -> None:
        self.assertTrue(all("owner-local" in row["claim_scope"] for row in PROPOSALS))


if __name__ == "__main__":
    unittest.main()

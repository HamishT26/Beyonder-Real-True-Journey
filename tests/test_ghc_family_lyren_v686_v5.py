"""Owner-scoped tests for Lyren Moss v686-v5 only."""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
PHASE = REPO / "docs/lyren-moss/v686-v5"
PROPOSALS = json.loads((PHASE / "x1/new-proposals.json").read_text(encoding="utf-8"))["proposals"]
MODULES = {
    name: importlib.import_module(name)
    for name in {
        Path(row["runner"]).stem
        for row in PROPOSALS
    }
}
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def compact(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def execute(row: dict[str, object]) -> object:
    return MODULES[Path(str(row["runner"])).stem].run(str(row["operation"]), copy.deepcopy(row["input"]))


class FrozenFamilies(unittest.TestCase):
    """Each generated method runs all ten immutable cases in one family."""


def _family_test(family: str):
    def test(self: unittest.TestCase) -> None:
        rows = [row for row in PROPOSALS if row["family"] == family]
        self.assertEqual(len(rows), 10)
        for row in rows:
            with self.subTest(proposal=row["proposal_id"]):
                before = copy.deepcopy(row["input"])
                self.assertEqual(execute(row), row["expected_result"])
                self.assertEqual(row["input"], before)
    return test


for _family in sorted({str(row["family"]) for row in PROPOSALS}):
    setattr(FrozenFamilies, f"test_{_family}", _family_test(_family))


class DefinitionIntegrity(unittest.TestCase):
    def test_exact_proposal_count(self) -> None:
        self.assertEqual(len(PROPOSALS), 200)

    def test_exact_family_count(self) -> None:
        self.assertEqual(len({row["family"] for row in PROPOSALS}), 20)

    def test_definition_hashes(self) -> None:
        for row in PROPOSALS:
            candidate = dict(row)
            declared = candidate.pop("definition_sha256")
            self.assertEqual(hashlib.sha256(compact(candidate)).hexdigest(), declared)

    def test_identifiers_are_unique(self) -> None:
        self.assertEqual(len({row["proposal_id"] for row in PROPOSALS}), 200)

    def test_titles_are_unique(self) -> None:
        self.assertEqual(len({row["title"] for row in PROPOSALS}), 200)

    def test_family_input_pairs_are_unique(self) -> None:
        pairs = {(row["family"], hashlib.sha256(compact(row["input"])).hexdigest()) for row in PROPOSALS}
        self.assertEqual(len(pairs), 200)

    def test_only_four_outcomes(self) -> None:
        self.assertLessEqual({row["expected_execution_disposition"] for row in PROPOSALS}, ALLOWED)

    def test_exact_outcome_distribution(self) -> None:
        self.assertEqual(Counter(row["expected_execution_disposition"] for row in PROPOSALS), Counter({"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10}))

    def test_every_case_is_synthetic(self) -> None:
        self.assertTrue(all(row["synthetic"] is True for row in PROPOSALS))

    def test_every_case_preserves_all_gates(self) -> None:
        self.assertTrue(all("stage20" in row["protected_gates"] and "maori_authority" in row["protected_gates"] for row in PROPOSALS))


class IndependentInvariants(unittest.TestCase):
    pass


ADVERSE_CASES = [
    ("ghc_family_lyren_chronometric_provenance", "missing", {}, {"error": "unknown_operation"}),
    ("ghc_family_lyren_custody_windows", "missing", {}, {"error": "unknown_operation"}),
    ("ghc_family_lyren_correction_lineage", "missing", {}, {"error": "unknown_operation"}),
    ("ghc_family_lyren_accessibility_projection", "missing", {}, {"error": "unknown_operation"}),
    ("ghc_family_lyren_claim_firewall", "missing", {}, {"error": "unknown_operation"}),
    ("ghc_family_lyren_chronometric_provenance", "instant_normalize", [], {"error": "invalid_input"}),
    ("ghc_family_lyren_custody_windows", "custody_at", [], {"error": "invalid_input"}),
    ("ghc_family_lyren_correction_lineage", "transfer_sequence", [], {"error": "invalid_input"}),
    ("ghc_family_lyren_accessibility_projection", "duration_phrase", [], {"error": "invalid_input"}),
    ("ghc_family_lyren_claim_firewall", "evidence_class", [], {"error": "invalid_input"}),
    ("ghc_family_lyren_chronometric_provenance", "uncertainty_envelope", {"center": 0, "minus": -1, "plus": 1}, {"error": "invalid_uncertainty"}),
    ("ghc_family_lyren_chronometric_provenance", "duration_parse", {"value": "P1M"}, {"error": "nonfixed_duration"}),
    ("ghc_family_lyren_custody_windows", "clock_offset", {"observed": True, "reference": 0}, {"error": "invalid_tick"}),
    ("ghc_family_lyren_custody_windows", "embargo_state", {"now": 1, "lo": 0, "hi": 2, "synthetic": False}, {"error": "synthetic_required"}),
    ("ghc_family_lyren_correction_lineage", "disclosure_slice", {"records": [{"record": "a", "lo": 0, "hi": 2, "public": 1}], "now": 1}, {"error": "invalid_public_flag"}),
    ("ghc_family_lyren_correction_lineage", "transfer_sequence", {"transfers": [{"from": None, "to": "a"}, {"from": "x", "to": "b"}]}, {"error": "broken_transfer"}),
    ("ghc_family_lyren_accessibility_projection", "supersession_chain", {"records": [{"record": "a", "parent": "a"}], "tip": "a"}, {"error": "cycle"}),
    ("ghc_family_lyren_accessibility_projection", "accessible_chronology", {"records": [{"record": "a", "instant": "2026-01-01T00:00:00Z", "outcome": "approved"}]}, {"error": "invalid_outcome"}),
    ("ghc_family_lyren_claim_firewall", "evidence_class", {"claim": "local_software", "evidence_class": "synthetic", "external_action": True}, {"error": "external_action_refused"}),
    ("ghc_family_lyren_claim_firewall", "cbr_time_authority_gate", {"obligation": "x", "evidence": "claimed", "authority": None, "external_action": False}, {"error": "unverified_external_binding"}),
]


def _adverse_test(module_name: str, operation: str, data: object, expected: object):
    def test(self: unittest.TestCase) -> None:
        before = copy.deepcopy(data)
        self.assertEqual(MODULES[module_name].run(operation, copy.deepcopy(data)), expected)
        self.assertEqual(data, before)
    return test


for _index, _case in enumerate(ADVERSE_CASES, 1):
    setattr(IndependentInvariants, f"test_adverse_{_index:02}", _adverse_test(*_case))


def _cli_duplicate_test(module_name: str):
    def test(self: unittest.TestCase) -> None:
        module = MODULES[module_name]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text('{"operation":"x","operation":"y","input":{}}', encoding="utf-8")
            with self.assertRaises(ValueError):
                module.read_strict(path)
    return test


for _index, _module in enumerate(sorted(MODULES), 21):
    setattr(IndependentInvariants, f"test_duplicate_json_{_index:02}", _cli_duplicate_test(_module))


def _nonfinite_test(module_name: str):
    def test(self: unittest.TestCase) -> None:
        module = MODULES[module_name]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nonfinite.json"
            path.write_text('{"operation":"x","input":{"value":NaN}}', encoding="utf-8")
            with self.assertRaises(ValueError):
                module.read_strict(path)
    return test


for _index, _module in enumerate(sorted(MODULES), 26):
    setattr(IndependentInvariants, f"test_nonfinite_json_{_index:02}", _nonfinite_test(_module))


if __name__ == "__main__":
    unittest.main()

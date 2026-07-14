from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_evidence_integrity as integrity
import ghc_family_evidence_integrity_minimal as minimal
import ghc_family_evidence_integrity_validator as validator


PHASE = ROOT / "docs/orin-thale/v642-v6"


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TestGhcFamilyV642V6(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.groups = {group["proposal_id"]: group for group in integrity.case_groups()}

    def _run_case(self, proposal_id: str, index: int) -> tuple[str, list[str], str]:
        group = self.groups[proposal_id]
        original = group["cases"][index]
        fixture = {key: value for key, value in original.items() if key not in {"case_id", "expected"}}
        observed, reasons = group["decision"](fixture)
        return observed, reasons, original["expected"]

    def _canonical(self, proposal_id: str) -> None:
        observed, reasons, expected = self._run_case(proposal_id, 0)
        self.assertEqual(expected, observed)
        self.assertEqual([], reasons)

    def _mutation(self, proposal_id: str) -> None:
        observed, reasons, expected = self._run_case(proposal_id, 1)
        self.assertEqual("reject", expected)
        self.assertEqual(expected, observed)
        self.assertTrue(reasons)

    def test_p01_canonical(self): self._canonical("V6426-P01")
    def test_p01_mutation(self): self._mutation("V6426-P01")
    def test_p02_canonical(self): self._canonical("V6426-P02")
    def test_p02_mutation(self): self._mutation("V6426-P02")
    def test_p03_canonical(self): self._canonical("V6426-P03")
    def test_p03_mutation(self): self._mutation("V6426-P03")
    def test_p04_canonical(self): self._canonical("V6426-P04")
    def test_p04_mutation(self): self._mutation("V6426-P04")
    def test_p05_canonical(self): self._canonical("V6426-P05")
    def test_p05_mutation(self): self._mutation("V6426-P05")
    def test_p06_canonical(self): self._canonical("V6426-P06")
    def test_p06_mutation(self): self._mutation("V6426-P06")
    def test_p07_canonical(self): self._canonical("V6426-P07")
    def test_p07_mutation(self): self._mutation("V6426-P07")
    def test_p08_canonical(self): self._canonical("V6426-P08")
    def test_p08_mutation(self): self._mutation("V6426-P08")
    def test_p09_canonical(self): self._canonical("V6426-P09")
    def test_p09_mutation(self): self._mutation("V6426-P09")
    def test_p10_canonical(self): self._canonical("V6426-P10")
    def test_p10_mutation(self): self._mutation("V6426-P10")

    def test_all_eighty_preregistered_cases_match(self):
        results = [integrity.evaluate_group(group) for group in integrity.case_groups()]
        self.assertEqual(80, sum(result["case_count"] for result in results))
        self.assertEqual(80, sum(result["matched_count"] for result in results))
        self.assertEqual(70, sum(result["retained_negative_count"] for result in results))

    def test_packet_distribution(self):
        ledger = read("x2-proposal-ledger.json")
        self.assertEqual({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, ledger["observed_distribution"])
        self.assertTrue(ledger["all_expected_dispositions_matched"])

    def test_negative_register_preserves_inheritance(self):
        register = read("retained-negative-register.json")
        self.assertEqual(147, register["inherited_count"])
        self.assertEqual(register["negative_count"], len(register["negatives"]))
        self.assertTrue(register["all_retained"])
        self.assertFalse(register["erasure_permitted"])

    def test_full_validator_accepts_candidate(self):
        result = validator.validate(ROOT, PHASE, allow_pending_snapshot=True, require_report=True)
        self.assertTrue(result["valid"], result["issues"])

    def test_minimal_validator_accepts_candidate(self):
        result = minimal.verify(PHASE, allow_pending_snapshot=True, require_report=True)
        self.assertTrue(result["valid"], result["issues"])

    def test_report_accessibility_boundary(self):
        report = (PHASE / "deliverables/v642-v6-evidence-integrity-report.html").read_text(encoding="utf-8").lower()
        for token in ["<!doctype html>", 'lang="en"', "skip-link", "<main", "<h1", "focus-visible", "prefers-reduced-motion"]:
            self.assertIn(token, report)
        self.assertIn("manual and user accessibility evaluation remains reserved", report)
        self.assertNotIn("<script", report)


if __name__ == "__main__":
    unittest.main()

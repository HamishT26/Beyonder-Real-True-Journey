from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v653_v7_detailed_validator as detailed
import ghc_family_v653_v7_minimal_validator as minimal
from ghc_family_v653_v7_validation_common import (
    PHASE,
    phase_public_paths,
    scan_privacy_paths,
)


class V653V7ValidationTests(unittest.TestCase):
    def test_detailed_validator(self) -> None:
        result = detailed.validate()
        self.assertTrue(result["valid"])
        self.assertEqual(result["check_count"], 195)
        self.assertEqual(result["passed_count"], 195)

    def test_minimal_validator(self) -> None:
        result = minimal.validate()
        self.assertTrue(result["valid"])
        self.assertEqual(result["check_count"], 22)
        self.assertEqual(result["passed_count"], 22)

    def test_all_phase_json_parse(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 100)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_five_class_privacy_scan(self) -> None:
        result = scan_privacy_paths(phase_public_paths())
        self.assertEqual(result["pattern_class_count"], 5)
        self.assertEqual(result["confirmed_hit_count"], 0)
        self.assertTrue(result["valid"])

    def test_no_external_gate_promoted(self) -> None:
        truth = json.loads(
            (PHASE / "phase-truth.json").read_text(encoding="utf-8")
        )
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(
            truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20"
        )


if __name__ == "__main__":
    unittest.main()

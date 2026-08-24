from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_r3_correction.py"
SPEC = importlib.util.spec_from_file_location("_neris_v667_v8_r3_correction", BUILDER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load correction builder")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class NerisSolaneV667V8R3CorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = builder.validate_tree()
        cls.phase = builder.PHASE
        cls.anchor = json.loads((cls.phase / "correction/canonical-failure-anchor.json").read_text(encoding="utf-8"))
        cls.overlay = json.loads((cls.phase / "correction/method-flow-external-overlay.json").read_text(encoding="utf-8"))
        cls.route = json.loads((cls.phase / "route/vesper-arlen-v668-v1-correction-route.json").read_text(encoding="utf-8"))

    def test_01_correction_content(self) -> None:
        self.assertEqual(self.summary["state"], "CORRECTION_CONTENT_PASS")
        self.assertEqual(self.summary["privacy_candidates"], 0)

    def test_02_failed_canonical_immutable(self) -> None:
        self.assertEqual(self.anchor["canonical_invocation_count"], 1)
        self.assertEqual(self.anchor["canonical_success_count"], 0)
        self.assertFalse(self.anchor["canonical_replayed"])

    def test_03_external_overlay(self) -> None:
        self.assertEqual(self.overlay["repository_sealed_x2"]["effective_negatives"], 28733)
        self.assertEqual(self.overlay["corrected_activation_overlay"]["effective_negatives"], 28734)
        self.assertEqual(self.overlay["corrected_activation_overlay"]["failed_witnesses"], 1035)
        self.assertFalse(self.overlay["repository_seal_rewritten"])

    def test_04_route_still_prepared(self) -> None:
        self.assertEqual(self.route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertFalse(self.route["successor_contacted"])
        self.assertFalse(self.route["canonical_replay_allowed"])

    def test_05_corrected_manifests(self) -> None:
        self.assertGreaterEqual(self.summary["delta_manifest_entries"], 8)
        self.assertGreater(self.summary["owner_manifest_entries"], 75)
        self.assertLess(self.summary["owner_files"], 2000)


if __name__ == "__main__":
    unittest.main()

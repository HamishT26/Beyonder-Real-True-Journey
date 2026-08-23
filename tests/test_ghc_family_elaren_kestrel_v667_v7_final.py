from __future__ import annotations

import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_ghc_family_elaren_kestrel_v667_v7_final.py"
SPEC = importlib.util.spec_from_file_location("elaren_v667_v7_final", BUILDER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load Elaren v667-v7 final builder")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ElarenV667V7FinalTests(unittest.TestCase):
    def doc(self, relative: str):
        return json.loads((mod.PHASE_ROOT / relative).read_text(encoding="utf-8"))

    def test_01_exact_anchors(self):
        self.assertEqual((mod.SOURCE_FINAL, mod.X1_HEAD, mod.EVIDENCE_HEAD), ("dc8d91294b7656ad5e9961bba93ff759af20846c", "b92d8b1b648c4d716ca894b22fda14327baed9b3", "9fde47f17a3c248643a543e0f44460e69191e627"))

    def test_02_final_counts(self):
        self.assertEqual(mod.final_counts(), {"effective_negatives": 28304, "effective_methods": 14445, "open_gaps": 199, "exact_gates": 197, "failed_witnesses": 588, "passing_witnesses": 1015})

    def test_03_outcomes(self):
        rows = self.doc("x2/proposal-outcomes.json")["outcomes"]
        self.assertEqual(Counter(row["outcome"] for row in rows), Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}))

    def test_04_overview_three_page_equivalent(self):
        words = len((mod.PHASE_ROOT / "closeout/final-integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1800)

    def test_05_baton_word_bounds(self):
        words = len((mod.PHASE_ROOT / "handoffs/neris-solane-v667-v8-activation-prepared.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)

    def test_06_baton_integrity(self):
        path = mod.PHASE_ROOT / "handoffs/neris-solane-v667-v8-activation-prepared.md"
        index = self.doc("deck/final-baton-index.json")
        self.assertEqual((index["bytes"], index["sha256"]), (len(path.read_bytes()), mod.sha256(path.read_bytes())))

    def test_07_route_prepared_not_sent(self):
        route = self.doc("route/route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["delivery_claim"])

    def test_08_post_evidence_overlay(self):
        overlay = self.doc("truth/post-evidence-operational-overlay.json")
        self.assertEqual((overlay["row_count"], overlay["negative_additions"], overlay["method_additions"]), (2, 2, 2))

    def test_09_phase_truth_boundary(self):
        truth = self.doc("truth/phase-truth-final.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["real_world_actions"], 0)

    def test_10_x1_manifest_count(self):
        self.assertEqual(self.doc("validation/immutable-x1-manifest.json")["entry_count"], 23)

    def test_11_evidence_manifest_count(self):
        self.assertEqual(self.doc("validation/immutable-evidence-manifest.json")["entry_count"], 385)

    def test_12_successor_not_contacted(self):
        self.assertFalse(self.doc("wellbeing/final-wellbeing-check.json")["successor_contacted"])

    def test_13_final_control_state_known(self):
        state = self.doc("validation/final-staged-review.json")["status"]
        self.assertIn(state, {"PREPARED_REQUIRES_EXACT_STAGING", "PASS"})


if __name__ == "__main__":
    unittest.main()

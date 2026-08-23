from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_final.py"
SPEC = importlib.util.spec_from_file_location("_neris_v667_v8_final", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load Neris final builder")
final = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(final)


class NerisSolaneV667V8FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = final.validate_tree()
        cls.root = final.PHASE_ROOT
        cls.closeout = json.loads((cls.root / "closeout/combined-closeout.json").read_text(encoding="utf-8"))
        cls.flow = json.loads((cls.root / "closeout/method-flow-state-final.json").read_text(encoding="utf-8"))
        cls.seal = json.loads((cls.root / "seal/seal-candidate.json").read_text(encoding="utf-8"))
        cls.route = json.loads((cls.root / "route/terminal-route-state.json").read_text(encoding="utf-8"))

    def test_01_tree_validates(self) -> None:
        self.assertEqual(self.summary["status"], "PASS")

    def test_02_exact_anchors(self) -> None:
        self.assertEqual(self.closeout["anchors"]["source"], final.SOURCE_FINAL)
        self.assertEqual(self.closeout["anchors"]["x1"], final.X1_HEAD)
        self.assertEqual(self.closeout["anchors"]["evidence"], final.EVIDENCE_HEAD)

    def test_03_history_shape(self) -> None:
        history = self.closeout["history"]
        self.assertEqual(history["history_count"], 2)
        self.assertEqual(history["merge_count"], 0)
        self.assertTrue(history["fresh_four_way_equal"])

    def test_04_proposal_chain(self) -> None:
        self.assertEqual(self.closeout["proposal_chain"], {"inherited": 4510, "new": 20, "final_frozen_total": 4530})

    def test_05_outcomes(self) -> None:
        self.assertEqual(self.closeout["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})

    def test_06_mutations_and_revalidations(self) -> None:
        self.assertEqual(self.closeout["rejecting_mutations"], 100)
        self.assertEqual(self.closeout["selected_inherited_revalidations"], 20)

    def test_07_tool_state(self) -> None:
        self.assertEqual(self.closeout["direct_tools"], 3)
        self.assertIn("ZERO_INITIAL_TRANSACTION_SUCCESS_CREDIT", self.closeout["tool_state"])

    def test_08_evidence_counts(self) -> None:
        self.assertEqual(self.flow["evidence_sealed"], {"effective_negatives": 28430, "methods": 14706, "open_gaps": 200, "exact_gates": 198, "failed_witnesses": 714, "passing_witnesses": 1279})

    def test_09_route_overlay_counts(self) -> None:
        self.assertEqual(self.flow["effective_for_future_corrected_route"], {"effective_negatives": 28432, "methods": 14708, "open_gaps": 201, "exact_gates": 198, "failed_witnesses": 716, "passing_witnesses": 1280})

    def test_10_route_conflict(self) -> None:
        self.assertTrue(self.route["name_conflict"])
        self.assertEqual(self.route["state"], "OPEN_ROUTE_GAP")
        self.assertEqual(self.route["delivery"], "PREPARED_NOT_SENT")

    def test_11_no_delivery_or_substitution(self) -> None:
        self.assertFalse(self.route["SENT_BY_NERIS_SOLANE"])
        self.assertFalse(self.route["successor_contacted"])
        self.assertFalse(self.route["substituted"])
        self.assertFalse(self.route["created"])

    def test_12_standby_not_contacted(self) -> None:
        self.assertEqual(self.route["Tavian_state"], "ON_STANDBY")
        self.assertFalse(self.route["Tavian_contacted"])

    def test_13_commit_time_canonical_truth(self) -> None:
        self.assertEqual(self.seal["canonical_invocation_count"], 0)
        self.assertEqual(self.seal["canonical_success_count"], 0)
        self.assertFalse(self.seal["post_success_replay"])

    def test_14_handoff_length(self) -> None:
        self.assertGreaterEqual(self.summary["handoff_words"], 10000)

    def test_15_handoff_state(self) -> None:
        text = (self.root / "handoffs/route-conflict-activation-prepared.md").read_text(encoding="utf-8")
        self.assertIn("SENT_BY_NERIS_SOLANE = false", text)
        self.assertIn("OPEN_ROUTE_GAP", text)
        self.assertIn("PREPARED_NOT_SENT", text)

    def test_16_immutable_evidence(self) -> None:
        self.assertEqual(self.summary["immutable_evidence_entries"], 391)

    def test_17_final_manifests(self) -> None:
        self.assertGreater(self.summary["final_delta_entries"], 0)
        self.assertGreater(self.summary["final_owner_entries"], 400)

    def test_18_privacy_and_ceiling(self) -> None:
        self.assertEqual(self.summary["privacy_candidates"], 0)
        self.assertLess(self.summary["owner_files"], 2000)

    def test_19_terminal_verdict(self) -> None:
        self.assertEqual(self.summary["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(self.closeout["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_20_identity_boundary(self) -> None:
        text = (self.root / "handoffs/route-conflict-activation-prepared.md").read_text(encoding="utf-8")
        self.assertIn("relational working language only", text)
        self.assertIn("not evidence of consciousness", text)


if __name__ == "__main__":
    unittest.main()

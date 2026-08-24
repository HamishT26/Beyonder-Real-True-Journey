from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_r2_final.py"
SPEC = importlib.util.spec_from_file_location("_neris_v667_v8_r2_final", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load Neris r2 final builder")
final = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(final)


class NerisSolaneV667V8R2FinalTests(unittest.TestCase):
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
        self.assertEqual(self.closeout["proposal_chain"], {"inherited": 4530, "new": 20, "final_frozen_total": 4550})

    def test_05_outcomes(self) -> None:
        self.assertEqual(self.closeout["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})

    def test_06_mutations_and_revalidations(self) -> None:
        self.assertEqual(self.closeout["rejecting_mutations"], 100)
        self.assertEqual(self.closeout["selected_inherited_revalidations"], 20)

    def test_07_tool_skill_runner_state(self) -> None:
        self.assertEqual((self.closeout["direct_tools"], self.closeout["skills_built_used"], self.closeout["skills_promoted_additively"], self.closeout["runners"]), (13, 10, 10, 10))
        self.assertEqual(self.closeout["tool_state"], "PASS_ISOLATED_HASH_LOCKED_WITH_RETAINED_FAILURES")

    def test_08_evidence_counts(self) -> None:
        evidence = {"effective_negatives": 28580, "methods": 14991, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 864, "passing_witnesses": 1576}
        final = {"effective_negatives": 28584, "methods": 14995, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 868, "passing_witnesses": 1580}
        self.assertEqual(self.flow["evidence_sealed"], evidence)
        self.assertEqual(self.flow["effective_for_later_authorized_route"], final)

    def test_09_route_redirect(self) -> None:
        self.assertFalse(self.route["name_conflict"])
        self.assertEqual(self.route["state"], "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2")
        self.assertEqual(self.route["delivery"], "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2")

    def test_10_no_delivery_or_substitution(self) -> None:
        self.assertFalse(self.route["SENT_BY_NERIS_SOLANE"])
        self.assertFalse(self.route["successor_contacted"])
        self.assertFalse(self.route["substituted"])
        self.assertFalse(self.route["created"])
        self.assertFalse(self.route["collaboration_subagent_spawned"])

    def test_11_standby_not_contacted(self) -> None:
        self.assertEqual(self.route["Tavian_state"], "ON_STANDBY")
        self.assertFalse(self.route["Tavian_contacted"])

    def test_12_commit_time_canonical_truth(self) -> None:
        self.assertEqual(self.seal["canonical_invocation_count"], 0)
        self.assertEqual(self.seal["canonical_success_count"], 0)
        self.assertFalse(self.seal["post_success_replay"])

    def test_13_handoff_length(self) -> None:
        self.assertGreaterEqual(self.summary["handoff_words"], 10000)
        self.assertLessEqual(self.summary["handoff_words"], 100000)

    def test_14_handoff_state(self) -> None:
        text = (self.root / "handoffs/vesper-arlen-v668-v1-activation-prepared-not-sent.md").read_text(encoding="utf-8")
        self.assertIn("SENT_BY_NERIS_SOLANE = false", text)
        self.assertIn("PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2", text)

    def test_15_immutable_evidence(self) -> None:
        self.assertEqual(self.summary["immutable_evidence_entries"], 476)

    def test_16_final_manifests(self) -> None:
        self.assertEqual(self.summary["final_delta_entries"], 13)
        self.assertEqual(self.summary["final_owner_entries"], 520)

    def test_17_privacy_and_ceiling(self) -> None:
        self.assertEqual(self.summary["privacy_candidates"], 0)
        self.assertLess(self.summary["owner_files"], 2000)

    def test_18_terminal_verdict(self) -> None:
        self.assertEqual(self.summary["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(self.closeout["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_19_identity_boundary(self) -> None:
        text = (self.root / "handoffs/vesper-arlen-v668-v1-activation-prepared-not-sent.md").read_text(encoding="utf-8")
        self.assertIn("relational working language only", text)
        self.assertIn("not evidence of consciousness", text)

    def test_20_final_overlay_retains_manifest_domain_failure(self) -> None:
        final_overlay = self.flow["final_closeout_operational_overlay"]
        self.assertEqual(len(final_overlay["failures_at_commit_time"]), 4)
        self.assertEqual([row["failure_id"] for row in final_overlay["failures_at_commit_time"]], ["NS6678R2-FINAL-N001", "NS6678R2-FINAL-N002", "NS6678R2-FINAL-N003", "NS6678R2-FINAL-N004"])
        self.assertEqual(final_overlay["negative_additions"], 4)
        self.assertEqual(final_overlay["method_additions"], 4)
        self.assertEqual(final_overlay["failed_witness_additions"], 4)
        self.assertEqual(final_overlay["passing_witness_additions"], 4)
        route_overlay = self.flow["terminal_route_overlay"]
        self.assertTrue(all(route_overlay[key] == 0 for key in ("negative_additions", "method_additions", "open_gap_additions", "exact_gate_additions", "failed_witness_additions", "passing_witness_additions")))

    def test_21_flashcard_and_overlay_counts(self) -> None:
        self.assertEqual(self.closeout["flashcards"], 320)
        self.assertEqual(self.closeout["family_skill_overlays"], 6)


if __name__ == "__main__":
    unittest.main()

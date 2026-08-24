from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_r3_final.py"
SPEC = importlib.util.spec_from_file_location("_neris_v667_v8_r3_final", BUILDER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load r3 final builder")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class NerisSolaneV667V8R3FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = builder.validate_tree()
        cls.root = builder.PHASE_ROOT
        cls.route = json.loads((cls.root / "route/vesper-arlen-v668-v1-prepared-route.json").read_text(encoding="utf-8"))
        cls.seal = json.loads((cls.root / "seal/content-seal.json").read_text(encoding="utf-8"))
        cls.method = json.loads((cls.root / "x2/method-flow/method-flow-ledger.json").read_text(encoding="utf-8"))

    def test_01_final_content_validation(self) -> None:
        self.assertEqual(self.summary["status"], "PASS_FINAL_CONTENT")
        self.assertEqual(self.summary["privacy_candidates"], 0)

    def test_02_lifecycle_ancestry(self) -> None:
        head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True, capture_output=True, check=True).stdout.strip()
        if head == builder.EVIDENCE_HEAD:
            parent = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD^"], text=True, capture_output=True, check=True).stdout.strip()
            self.assertEqual(parent, builder.X1_HEAD)
        else:
            parent = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD^"], text=True, capture_output=True, check=True).stdout.strip()
            self.assertEqual(parent, builder.EVIDENCE_HEAD)

    def test_03_baton_minimum(self) -> None:
        self.assertGreaterEqual(self.summary["baton_words"], 10_000)
        self.assertGreater(self.summary["baton_bytes"], 100_000)

    def test_04_prepared_not_sent(self) -> None:
        self.assertEqual(self.route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertFalse(self.route["successor_contacted"])
        self.assertFalse(self.route["created_task"])
        self.assertFalse(self.route["forked_task"])

    def test_05_exact_recipient(self) -> None:
        self.assertEqual(self.route["recipient_exact_title"], "Vesper Arlen")
        self.assertEqual(self.route["recipient_phase"], "v668-v1")
        self.assertEqual(self.route["recipient_next_prospective"], {"title": "Lyren Moss", "phase": "v668-v2"})

    def test_06_terminal_checklist(self) -> None:
        checklist = json.loads((self.root / "closeout/terminal-checklist.json").read_text(encoding="utf-8"))
        self.assertEqual(checklist["count"], 30)
        self.assertTrue(checklist["all_passed"])

    def test_07_manifest_replay_counts(self) -> None:
        self.assertGreater(self.summary["owner_manifest_entries"], 60)
        self.assertGreaterEqual(self.summary["delta_manifest_entries"], 8)

    def test_08_outcome_labels(self) -> None:
        outcomes = json.loads((self.root / "x2/proposals/proposal-outcomes.json").read_text(encoding="utf-8"))
        self.assertEqual(Counter(row["outcome_label"] for row in outcomes["outcomes"]), Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}))
        self.assertEqual(outcomes["allowed_outcomes"], builder.ALLOWED_OUTCOMES)

    def test_09_method_flow(self) -> None:
        self.assertEqual([self.method[key] for key in ("effective_negatives", "methods", "open_gaps", "exact_gates", "failed_witnesses", "passing_witnesses")], [28733, 15319, 203, 201, 1034, 1875])

    def test_10_tool_and_skill_receipts(self) -> None:
        tools = json.loads((self.root / "x2/tooling/thirteen-tool-transaction-receipt.json").read_text(encoding="utf-8"))
        promotion = json.loads((self.root / "x2/skills/global-promotion-receipt.json").read_text(encoding="utf-8"))
        overlays = json.loads((self.root / "x2/skills/core-skill-overlay-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual((tools["direct_tool_count"], tools["positive_smoke_count"], tools["negative_rejection_count"]), (13, 13, 13))
        self.assertEqual((promotion["count"], overlays["count"]), (10, 7))

    def test_11_flashcards(self) -> None:
        cards = json.loads((self.root / "x2/flashcards/four-tier-deck.json").read_text(encoding="utf-8"))
        self.assertEqual(cards["tier_counts"], {"1": 40, "2": 80, "3": 100, "4": 100})

    def test_12_file_ceiling(self) -> None:
        self.assertLess(self.summary["owner_files"], 2000)

    def test_13_canonical_commit_time_truth(self) -> None:
        self.assertEqual(self.seal["canonical_state"], "NOT_YET_INVOKED_AT_COMMIT_TIME")
        self.assertEqual(self.seal["delivery_state"], "PREPARED_NOT_SENT")

    def test_14_terminal_boundaries(self) -> None:
        self.assertEqual(self.seal["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(self.method["same_owner_not_independent_reproduction"])

    def test_15_no_private_paths(self) -> None:
        self.assertEqual(self.summary["privacy_candidates"], 0)


if __name__ == "__main__":
    unittest.main()

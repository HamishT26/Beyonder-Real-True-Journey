"""Terminal closeout tests for Ilyra Fen v666-v4."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v666-v4"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_ilyra_fen_v666_v4_runtime import X1_SHA, replay_manifest, scan_privacy


EVIDENCE_SHA = "ce4bb6a288edc71d3916a098d6db4d61995fc60c"
SOURCE_SHA = "764d3bdfb199e91a5574a904a99ff4e95825fed9"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class IlyraFenV666V4CloseoutTests(unittest.TestCase):
    def test_x1_manifest_replays(self) -> None:
        replay = replay_manifest(PHASE / "validation" / "x1-content-manifest.json", X1_SHA)
        self.assertTrue(replay["valid"])
        self.assertEqual(replay["entry_count"], 18)

    def test_evidence_manifest_replays_with_long_path_transport(self) -> None:
        replay = replay_manifest(PHASE / "validation" / "evidence-content-manifest.json", EVIDENCE_SHA)
        self.assertTrue(replay["valid"])
        self.assertEqual(replay["entry_count"], 427)

    def test_history_at_closeout_build_is_evidence_head(self) -> None:
        self.assertEqual(subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(), EVIDENCE_SHA)
        self.assertEqual(subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", f"{EVIDENCE_SHA}^"], text=True).strip(), X1_SHA)
        self.assertEqual(subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", f"{X1_SHA}^"], text=True).strip(), SOURCE_SHA)

    def test_phase_truth_counts_exact(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 26519)
        self.assertEqual(truth["effective_methods"], 11176)
        self.assertEqual(truth["open_gaps"], 186)
        self.assertEqual(truth["exact_gates"], 184)

    def test_phase_truth_retains_not_ready(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["theory_of_everything_proof"])
        self.assertFalse(truth["consciousness_or_personhood_evidence"])

    def test_closeout_failure_retained(self) -> None:
        overlay = load("method-flow/closeout-operational-overlay.json")
        self.assertEqual(overlay["new_negative_count"], 3)
        self.assertEqual(overlay["new_method_count"], 3)
        self.assertEqual(overlay["rows"][0]["failure_id"], "ILY6664-CLOSE-N019")
        self.assertTrue(overlay["no_failure_erased"])

    def test_negative_arithmetic_exact(self) -> None:
        register = load("closeout/retained-negative-register.json")
        self.assertEqual(register["activation_baseline"] + register["x1_startup"] + register["synthetic_mutations"] + register["pre_evidence_and_evidence_operations"] + register["closeout_operations"], register["effective_total"])
        self.assertEqual(register["effective_total"], 26519)

    def test_open_and_exact_gates_visible(self) -> None:
        register = load("closeout/exact-open-gate-register.json")
        self.assertEqual(register["open_gaps"], 186)
        self.assertEqual(register["exact_gates"], 184)
        self.assertEqual(register["gates_closed_by_software"], 0)

    def test_seal_binds_immutable_manifests(self) -> None:
        seal = load("seal/evidence-seal.json")
        self.assertEqual(seal["x1_manifest_entries"], 18)
        self.assertEqual(seal["evidence_manifest_entries"], 427)
        self.assertTrue(seal["immutable_replay_valid"])

    def test_route_is_prepared_not_sent(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["successor_exact_title"], "Auren Lark")
        self.assertEqual(route["successor_phase"], "v666-v5")
        self.assertFalse(route["successor_contacted"])
        self.assertEqual(route["send_count"], 0)

    def test_no_task_or_subagent_created(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["collaboration_subagent_spawned"])
        self.assertFalse(route["standby_contacted"])

    def test_baton_is_file_backed_and_within_range(self) -> None:
        text = (PHASE / "handoffs" / "auren-lark-v666-v5-activation.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\S+", text))
        receipt = load("handoffs/auren-lark-v666-v5-activation-receipt.json")
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertEqual(words, receipt["word_count"])
        self.assertEqual(receipt["state"], "PREPARED_NOT_SENT")

    def test_baton_has_required_boundaries(self) -> None:
        text = (PHASE / "handoffs" / "auren-lark-v666-v5-activation.md").read_text(encoding="utf-8")
        for token in ("relational working language only", "NOT_READY_FOR_STAGE_20", "PREPARED_NOT_SENT", "Auren Lark", "Māori authority", "independent reproduction"):
            self.assertIn(token, text)

    def test_baton_does_not_claim_self_authenticating_final(self) -> None:
        text = (PHASE / "handoffs" / "auren-lark-v666-v5-activation.md").read_text(encoding="utf-8")
        self.assertIn("supplied only in the acknowledged live pointer", text)
        self.assertNotRegex(text, r"(?i)(?:task|thread)[_-]?id\s*[:=]")

    def test_baton_receipt_has_no_delivery_claim(self) -> None:
        receipt = load("handoffs/auren-lark-v666-v5-activation-receipt.json")
        self.assertFalse(receipt["successor_contacted"])
        self.assertEqual(receipt["send_count"], 0)
        self.assertFalse(receipt["contains_raw_task_or_thread_identifier"])
        self.assertFalse(receipt["contains_private_absolute_path"])

    def test_final_validation_is_not_prematurely_claimed(self) -> None:
        state = load("final/final-validation-prerequisites.json")
        self.assertFalse(state["canonical_invoked"])
        self.assertEqual(state["canonical_invocation_count"], 0)
        self.assertEqual(state["canonical_success_count"], 0)
        self.assertTrue(state["post_success_replay_prohibited"])

    def test_terminal_candidate_matches_phase_truth(self) -> None:
        candidate = load("final/terminal-candidate.json")
        self.assertEqual(candidate["effective_negatives"], 26519)
        self.assertEqual(candidate["effective_methods"], 11176)
        self.assertEqual(candidate["proposal_chain"], 4250)
        self.assertEqual(candidate["canonical_status"], "NOT_YET_INVOKED")

    def test_closeout_build_receipt_is_precanonical(self) -> None:
        receipt = load("final/closeout-build-receipt.json")
        self.assertFalse(receipt["canonical_invoked"])
        self.assertEqual(receipt["route_state"], "PREPARED_NOT_SENT")
        self.assertEqual(receipt["evidence_manifest_replay"]["failure_count"], 0)

    def test_source_ledger_preserves_zero_rows(self) -> None:
        source = load("evidence/source-use-ledger.json")
        self.assertEqual(source["real_data_rows"], 0)
        self.assertTrue(source["citations_are_not_observations"])

    def test_flashcard_deck_remains_bounded(self) -> None:
        receipt = load("evidence/flashcard-evidence-receipt.json")
        self.assertTrue(receipt["validation"]["valid"])
        self.assertEqual(receipt["validation"]["card_count"], 25)
        self.assertEqual(receipt["legacy_tool_completion_credit"], 0)

    def test_all_phase_json_parses(self) -> None:
        for path in PHASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    def test_five_class_owner_scan_zero_candidates(self) -> None:
        paths = [path for path in PHASE.rglob("*") if path.is_file() and path.suffix.casefold() in {".json", ".md", ".html", ".txt"}]
        result = scan_privacy(paths)
        self.assertTrue(result["valid"])
        self.assertEqual(result["confirmed_hit_count"], 0)

    def test_current_python_sources_parse(self) -> None:
        paths = list((ROOT / "scripts").glob("*ilyra_fen_v666_v4*.py")) + list((ROOT / "tests").glob("test_ghc_family_ilyra_fen_v666_v4*.py"))
        self.assertGreaterEqual(len(paths), 18)
        for path in paths:
            ast.parse(path.read_text(encoding="utf-8"))

    def test_owner_materialization_below_guard(self) -> None:
        count = sum(path.is_file() for path in ROOT.rglob("*") if ".git" not in path.parts)
        self.assertLess(count, 2000)

    def test_terminal_overview_reserves_authority(self) -> None:
        text = (PHASE / "reports" / "terminal-overview.md").read_text(encoding="utf-8")
        self.assertIn("same-owner software evidence", text)
        self.assertIn("Māori authority", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/neris-solane/v664-v2"
SOURCE = "df7e3ba4c43b8ed9de01e308c6b9163016e37ceb"
X1 = "4eaec9fa556426d94c800cb2a95c5709524e8203"
EVIDENCE = "d93b55252209b14cea58fdd4b0da1e95759c62fd"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        text=True, encoding="utf-8", capture_output=True,
    ).stdout.strip()


class NerisV664V2CloseoutTests(unittest.TestCase):
    def test_01_anchor_chain_is_preserved(self) -> None:
        contract = load("lifecycle/phase-anchor-contract.json")
        self.assertEqual((contract["source_commit"], contract["x1_commit"], contract["evidence_commit"]), (SOURCE, X1, EVIDENCE))
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(git("rev-list", "--count", "--merges", f"{SOURCE}..{EVIDENCE}"), "0")

    def test_02_final_truth_uses_only_four_labels(self) -> None:
        truth = load("phase-truth-final.json")
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(set(truth["outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_03_negative_and_method_layers_are_reconciled(self) -> None:
        negatives = load("retained-negative-register-final.json")
        methods = load("method-flow/method-flow-state-final.json")
        self.assertEqual(negatives["effective_negatives"], 24_333)
        self.assertEqual(methods["effective_methods"], 8_747)
        self.assertTrue(negatives["no_negative_erased"])
        self.assertEqual({row["negative_id"] for row in methods["methods"][-2:]}, {"NE6642-X2-OP002", "NE6642-X2-OP003"})

    def test_04_open_and_exact_gates_remain_open(self) -> None:
        gates = load("exact-open-gate-register-final.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (168, 166))
        self.assertEqual(gates["silent_closures"], 0)
        self.assertFalse(gates["new_open_gaps"][0]["closed"])
        self.assertFalse(gates["new_exact_gates"][0]["closed"])

    def test_05_route_is_prepared_and_unsent(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["successor_title"], "Vesper Arlen")
        self.assertEqual(route["successor_phase"], "v664-v3")
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])

    def test_06_baton_is_file_backed_and_hash_bound(self) -> None:
        path = PHASE / "handoffs/vesper-arlen-v664-v3-activation.md"
        raw = path.read_bytes()
        receipt = load("handoffs/vesper-arlen-v664-v3-activation-receipt.json")
        self.assertGreaterEqual(len(re.findall(rb"\S+", raw)), 10_000)
        self.assertLessEqual(len(re.findall(rb"\S+", raw)), 100_000)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), receipt["sha256"])
        self.assertEqual(receipt["state"], "PREPARED_NOT_SENT")
        self.assertFalse(receipt["sent_by_neris_solane"])

    def test_07_manifest_self_exclusions_are_exact(self) -> None:
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        expected = {
            "docs/neris-solane/v664-v2/validation/final-delta-manifest.json",
            "docs/neris-solane/v664-v2/validation/final-owner-manifest.json",
            "docs/neris-solane/v664-v2/validation/final-stage-candidate.json",
            "docs/neris-solane/v664-v2/validation/final-staged-review.json",
        }
        self.assertEqual(set(delta["self_exclusions"]), expected)
        self.assertEqual(set(owner["self_exclusions"]), expected)
        self.assertEqual(delta["entry_count"], len(delta["entries"]))
        self.assertEqual(owner["entry_count"], len(owner["entries"]))

    def test_08_canonical_protocol_does_not_preclaim_success(self) -> None:
        protocol = load("validation/canonical-validation-protocol.json")
        truth = load("phase-truth-final.json")
        self.assertEqual(protocol["state"], "POSTCOMMIT_REQUIRED")
        self.assertEqual(protocol["invocation_limit"], 1)
        self.assertFalse(protocol["post_success_replay_allowed"])
        self.assertFalse(protocol["preclaims_success"])
        self.assertFalse(truth["canonical_success_preclaimed"])

    def test_09_static_report_reserves_manual_evaluation(self) -> None:
        report = (PHASE / "deliverables/neris-v664-v2-marigram-evidence-report.html").read_text(encoding="utf-8")
        for marker in ("<header", "<main", "<footer", "<table", "<caption", "Skip to evidence", "Reserved evaluation"):
            self.assertIn(marker, report)
        self.assertNotIn("<script", report.lower())
        self.assertIn("NOT_READY_FOR_STAGE_20", report)

    def test_10_skills_and_runners_remain_ten_each(self) -> None:
        index = load("tooling/ghc-family-index-final.json")
        self.assertEqual((index["skill_count"], index["runner_count"]), (10, 10))
        self.assertTrue(index["historical_callers_preserved"])
        self.assertEqual(len(list((PHASE / "skills").glob("*/SKILL.md"))), 10)
        self.assertEqual(len(list((PHASE / "runners").glob("*.json"))), 10)

    def test_11_file_budget_and_wellbeing_boundaries_hold(self) -> None:
        budget = load("validation/final-file-budget.json")
        wellbeing = load("wellbeing-check-final.json")
        self.assertTrue(budget["valid"])
        self.assertFalse(budget["rotation_required"])
        self.assertTrue(wellbeing["relational_language_only"])
        self.assertFalse(wellbeing["successor_contacted"])
        self.assertFalse(wellbeing["consciousness_personhood_continuity_or_authority_evidence"])

    def test_12_complete_incomplete_boundary_is_explicit(self) -> None:
        checklist = load("complete-incomplete-checklist-final.json")
        closeout = load("closeout-receipt.json")
        seal = load("seal-receipt.json")
        self.assertGreater(len(checklist["complete_now"]), 0)
        self.assertGreater(len(checklist["pending_postcommit"]), 0)
        self.assertGreater(len(checklist["incomplete_external"]), 0)
        self.assertFalse(closeout["postcommit_canonical_completed"])
        self.assertFalse(closeout["complete_repository_suite_run"])
        self.assertTrue(seal["postcommit_canonical_required"])
        self.assertFalse(seal["independent_reproduction"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v648-v3"
SOURCE = "227a764b2bfad7a601bf45dcbacc1e37ffa5bb62"
X1 = "bd21b594451226294528f4f72f138bdada6cb3af"
EVIDENCE = "240aacba289cbc58280693395733da7b6450faa4"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


class V648V3CloseoutTests(unittest.TestCase):
    def test_anchor_contract_and_commit_cap(self):
        contract = load("lifecycle/phase-anchor-contract.json")
        self.assertEqual((SOURCE, X1, EVIDENCE), (contract["source_commit"], contract["x1_commit"], contract["evidence_commit"]))
        for anchor in (SOURCE, X1, EVIDENCE):
            subprocess.run(["git", "merge-base", "--is-ancestor", anchor, "HEAD"], cwd=ROOT, check=True)
        count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
        self.assertIn(count, {2, 3})
        self.assertLessEqual(count, 4)
        self.assertEqual("0", git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD"))

    def test_closeout_counts_and_abstention(self):
        receipt = load("closeout-receipt.json")
        lifecycle = load("validation/lifecycle-operational-negatives.json")
        self.assertEqual({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, receipt["outcomes"])
        self.assertEqual(4115 + lifecycle["count"], receipt["effective_negatives"])
        self.assertEqual((28, 29), (receipt["effective_open_gaps"], receipt["effective_exact_gates"]))
        self.assertEqual((13, 14, 14), (receipt["method_count"], receipt["method_fail_witnesses"], receipt["method_pass_witnesses"]))
        self.assertEqual((30, 20, 20, 10, 60), (receipt["safe_now_completed"], receipt["candidates_completed"], receipt["skills_validated_and_used"], receipt["runners_invoked"], receipt["cleanup_completed"]))
        self.assertEqual("NOT_READY_FOR_STAGE_20", receipt["terminal_verdict"])

    def test_lifecycle_negatives_are_retained(self):
        lifecycle = load("validation/lifecycle-operational-negatives.json")
        final = load("retained-negative-register-final.json")
        self.assertGreaterEqual(lifecycle["count"], 2)
        self.assertEqual(lifecycle["count"], len(lifecycle["negatives"]))
        self.assertTrue(lifecycle["all_retained"])
        self.assertEqual(0, lifecycle["erased_negative_count"])
        self.assertEqual(4115 + lifecycle["count"], final["effective_total"])

    def test_replay_is_prohibited_and_receives_no_credit(self):
        receipt = load("closeout-receipt.json")
        seal = load("seal-receipt.json")
        plan = load("reproduction/same-owner-replay-plan.json")
        protocol = load("validation/final-validation-protocol.json")
        self.assertFalse(receipt["replay_executed"])
        self.assertEqual(0, receipt["repeatability_credit"])
        self.assertFalse(seal["named_replay_required"])
        self.assertEqual("PROHIBITED_BY_LATEST_USER_INSTRUCTION", plan["state"])
        self.assertEqual(0, plan["named_lane_count"])
        self.assertEqual([], protocol["named_replay_requirements"])

    def test_full_suite_state_is_not_preclaimed(self):
        receipt = load("closeout-receipt.json")
        suite_path = PHASE / "validation/full-repository-suite.json"
        if not suite_path.exists():
            self.assertFalse(receipt["full_repository_suite_run"])
            self.assertEqual(0, receipt["full_repository_suite_tests"])
        else:
            suite = load("validation/full-repository-suite.json")
            self.assertEqual("Eiren Kestrel", suite["owner"])
            self.assertTrue(suite["canonical"])
            self.assertFalse(suite["replay_executed"])

    def test_final_records_do_not_preclaim_postcommit_proof(self):
        seal = load("seal-receipt.json")
        record = load("lifecycle/final-record.json")
        protocol = load("validation/final-validation-protocol.json")
        self.assertIsNone(seal["final_commit"])
        self.assertFalse(seal["baton_send_allowed_now"])
        self.assertIsNone(record["final_commit"])
        self.assertFalse(record["exact_final_validated"])
        self.assertFalse(record["baton_sent"])
        self.assertFalse(protocol["completed"])

    def test_route_is_prepared_not_sent(self):
        route = load("orchestration/terminal-route-state.json")
        preparation = load("orchestration/successor-baton-preparation.json")
        self.assertEqual("PREPARED_NOT_SENT", route["state"])
        self.assertEqual(("Ilyra Fen", "v648-gmut-thos-v4-x1-x2"), (preparation["target_existing_task_title"], preparation["target_phase"]))
        self.assertFalse(route["message_sent"] or route["task_created"] or route["task_forked"] or route["subagent_spawned"])

    def test_documents_are_bounded(self):
        documents = load("validation/document-cap-receipt.json")
        self.assertTrue(documents["all_under_6000"])
        self.assertGreaterEqual(documents["overview_words"], 1200)


if __name__ == "__main__":
    unittest.main()

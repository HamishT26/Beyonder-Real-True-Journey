from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/lyren-moss/v657-v1"
SOURCE = "a033d1318920de1beec288f9c5b27e7f73a8ff3b"
X1 = "2e3d51c838caa01d05b0713b6c165bef0be882d5"
EVIDENCE = "91c36c44b6ccecbf73892792e07525cc7577d0c8"
CLOSEOUT = "8ff8a0658e10e2ddec8db77bf1edb2fe9047fedb"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class V657V1FinalTests(unittest.TestCase):
    def test_anchor_chain_and_commit_cap(self) -> None:
        self.assertEqual(git("rev-parse", f"{CLOSEOUT}^"), EVIDENCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", CLOSEOUT, "HEAD"],
            cwd=ROOT,
            check=True,
        )
        count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
        self.assertIn(count, {3, 4})
        self.assertLessEqual(count, 8)
        self.assertEqual(git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD"), "0")

    def test_final_truth_candidate(self) -> None:
        truth = load("truth/phase-truth-final-candidate.json")
        self.assertEqual(
            truth["outcome_counts"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(truth["effective_negatives"], 15248)
        self.assertEqual(
            (truth["effective_open_gaps"], truth["effective_exact_gates"]),
            (105, 104),
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])

    def test_final_method_pair(self) -> None:
        flow = load("method-flow/method-flow-state-final.json")
        self.assertEqual(flow["counts"]["current_methods"], 2)
        self.assertEqual(
            flow["counts"]["current_witness_results"], {"fail": 2, "pass": 2}
        )
        self.assertEqual(flow["counts"]["effective_methods"], 1532)
        self.assertTrue(flow["all_failed_witnesses_retained"])

    def test_terminal_route_is_unsent(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["next_exact_title"], "Ilyra Fen")
        self.assertEqual(route["next_phase"], "v657-v2")
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])
        self.assertEqual(route["tavian_sol_state"], "ON_STANDBY")

    def test_final_record_does_not_preclaim(self) -> None:
        record = load("lifecycle/final-record.json")
        plan = load("validation/canonical-aggregate-plan.json")
        self.assertIsNone(record["final_commit"])
        self.assertEqual(
            record["record_state"],
            "CANDIDATE_TREE_REVIEWED_POSTCOMMIT_PROOF_PENDING",
        )
        self.assertEqual(plan["state"], "POSTCOMMIT_REQUIRED")
        self.assertFalse(plan["completed"])
        self.assertFalse(plan["route_sent"])

    def test_closeout_manifest_replay(self) -> None:
        replay = load("validation/closeout-manifest-commit-replay.json")
        self.assertTrue(replay["valid"])
        manifest = load("validation/closeout-content-manifest.json")
        self.assertEqual(replay["entry_count"], manifest["entry_count"])
        self.assertEqual(replay["mismatches"], [])

    def test_final_artifact_packet_exists(self) -> None:
        required = [
            "lifecycle/final-record.json",
            "truth/phase-truth-final-candidate.json",
            "truth/retained-negative-register-final.json",
            "method-flow/method-flow-state-final.json",
            "orchestration/terminal-route-state.json",
            "validation/canonical-aggregate-plan.json",
            "validation/final-owner-manifest.json",
        ]
        self.assertTrue(all((PHASE / path).is_file() for path in required))

    def test_phase_json_parses(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 185)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

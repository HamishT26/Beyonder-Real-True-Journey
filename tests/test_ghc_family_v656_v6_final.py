from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/elaren-kestrel/v656-v6"
SOURCE = "8a4bb8e8b6a649040c531e8d3dd36925fd0da301"
X1 = "9c0227286b93672a4d98dba305e1c627a2300279"
EVIDENCE = "0744740cc17dfa57b0d151957d1edc7a2bb2c282"
CLOSEOUT = "7fd248f8322e5d8a6c8d8b02bdaa8eab3d5139b1"


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


class V656V6FinalTests(unittest.TestCase):
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
        self.assertIn(count, {4, 5})
        self.assertLessEqual(count, 8)
        self.assertEqual(git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD"), "0")

    def test_final_truth_candidate(self) -> None:
        truth = load("truth/phase-truth-final-candidate.json")
        self.assertEqual(
            truth["outcome_counts"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(truth["effective_negatives"], 14729)
        self.assertEqual(
            (truth["effective_open_gaps"], truth["effective_exact_gates"]),
            (102, 101),
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])

    def test_final_method_pair(self) -> None:
        flow = load("method-flow/method-flow-state-final.json")
        self.assertEqual(flow["counts"]["current_methods"], 4)
        self.assertEqual(
            flow["counts"]["current_witness_results"], {"fail": 4, "pass": 4}
        )
        self.assertEqual(flow["counts"]["effective_methods"], 1015)
        self.assertTrue(flow["all_failed_witnesses_retained"])

    def test_validator_rule_values_do_not_self_match_source(self) -> None:
        source = (
            ROOT / "scripts/ghc_family_v656_v6_final_validator.py"
        ).read_text(encoding="utf-8")
        values = [
            "".join(("PENDING", "_EVIDENCE", "_COMMIT")),
            "".join(("PENDING", "_CLOSEOUT", "_COMMIT")),
            "".join(("FINAL", "_COMMIT", "_PLACEHOLDER")),
        ]
        self.assertTrue(all(value not in source for value in values))
        failure = load("validation/canonical-aggregate-failure-01.json")
        self.assertFalse(failure["valid"])
        self.assertEqual(failure["success_credit"], 0)

    def test_terminal_route_is_unsent(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["next_exact_title"], "Neris Solane")
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
        self.assertEqual(plan["state"], "POSTCORRECTION_COMMIT_REQUIRED")
        self.assertFalse(plan["completed"])
        self.assertFalse(plan["route_sent"])

    def test_closeout_manifest_replay(self) -> None:
        replay = load("validation/closeout-manifest-commit-replay.json")
        self.assertTrue(replay["valid"])
        self.assertEqual(replay["entry_count"], 233)
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

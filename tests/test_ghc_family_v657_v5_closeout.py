from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/caelen-ash/v657-v5"
SOURCE = "1ae8aa07d6b0d5f74dc3c5b29615c79b908e235f"
X1 = "7fdae81a188decacbee20c2f2c283b7104c0e91a"
EVIDENCE = "e2f0f3535f968e26fab748385c950cf4b7de085a"


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


class V657V5CloseoutTests(unittest.TestCase):
    def test_exact_anchor_chain(self) -> None:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", EVIDENCE, "HEAD"],
            cwd=ROOT,
            check=True,
        )
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)

    def test_bounded_truth(self) -> None:
        truth = load("truth/phase-truth-closeout.json")
        self.assertEqual(
            truth["outcome_counts"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(truth["effective_negatives"], 15965)
        self.assertEqual(
            (truth["effective_open_gaps"], truth["effective_exact_gates"]),
            (109, 108),
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])

    def test_closeout_method_parity(self) -> None:
        flow = load("method-flow/method-flow-state-closeout.json")
        self.assertEqual(flow["counts"]["current_methods"], 1)
        self.assertEqual(
            flow["counts"]["current_witness_results"], {"fail": 1, "pass": 1}
        )
        self.assertEqual(flow["counts"]["effective_methods"], 2241)
        self.assertTrue(flow["all_failed_witnesses_retained"])

    def test_evidence_manifest_replay(self) -> None:
        replay = load("validation/evidence-manifest-commit-replay.json")
        self.assertTrue(replay["valid"])
        self.assertEqual(replay["entry_count"], 208)
        self.assertEqual(replay["mismatches"], [])

    def test_route_is_not_sent(self) -> None:
        route = load("orchestration/route-state-closeout.json")
        self.assertEqual(route["state"], "HELD_UNRESOLVED_UNTIL_TERMINAL_GATE")
        self.assertEqual(route["next_exact_title"], "Orin Thale")
        self.assertEqual(route["next_phase"], "v657-v6")
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])
        self.assertEqual(route["tavian_sol_state"], "ON_STANDBY")

    def test_final_protocol_does_not_preclaim(self) -> None:
        protocol = load("validation/final-validation-protocol.json")
        self.assertEqual(protocol["state"], "POST_FINAL_COMMIT_REQUIRED")
        self.assertFalse(protocol["completed"])
        self.assertFalse(protocol["preclaims_exact_final"])
        self.assertFalse(protocol["preclaims_route_sent"])

    def test_successor_baton_is_file_backed_and_bounded(self) -> None:
        receipt = load("validation/successor-baton-word-cap.json")
        text = (
            PHASE / "handoffs/orin-thale-v657-v6-activation.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(receipt["word_count"], len(text.split()))
        self.assertGreaterEqual(receipt["word_count"], 10000)
        self.assertLessEqual(receipt["word_count"], 100000)
        self.assertEqual(
            receipt["state"], "HELD_UNRESOLVED_UNTIL_TERMINAL_GATE"
        )
        self.assertIn(
            "This committed file remains `HELD_UNRESOLVED_UNTIL_TERMINAL_GATE`",
            text,
        )
        self.assertFalse(
            any(
                line.strip() == "SENT_BY_CAELEN_ASH = true"
                for line in text.splitlines()
            )
        )

    def test_closeout_artifacts_exist(self) -> None:
        required = [
            "closeout-receipt.json",
            "seal-receipt.json",
            "lifecycle/phase-anchor-contract.json",
            "truth/retained-negative-register-closeout.json",
            "reflection-remaster/closeout-decision-record.json",
            "workflow/workflow-plan-closeout.json",
            "tooling/ghc-family-index-closeout.json",
            "final-complete-incomplete-checklist.json",
        ]
        self.assertTrue(all((PHASE / path).is_file() for path in required))

    def test_phase_documents_parse_and_stay_bounded(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 170)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))
        documents = [
            path
            for path in PHASE.rglob("*")
            if path.is_file()
            and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}
        ]
        self.assertLessEqual(
            max(len(path.read_text(encoding="utf-8").split()) for path in documents),
            100000,
        )


if __name__ == "__main__":
    unittest.main()

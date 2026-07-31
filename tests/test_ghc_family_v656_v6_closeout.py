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


class V656V6CloseoutTests(unittest.TestCase):
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
        self.assertEqual(truth["effective_negatives"], 14725)
        self.assertEqual(
            (truth["effective_open_gaps"], truth["effective_exact_gates"]),
            (102, 101),
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])

    def test_closeout_method_parity(self) -> None:
        flow = load("method-flow/method-flow-state-closeout.json")
        self.assertEqual(flow["counts"]["current_methods"], 5)
        self.assertEqual(
            flow["counts"]["current_witness_results"], {"fail": 5, "pass": 5}
        )
        self.assertEqual(flow["counts"]["effective_methods"], 1011)
        self.assertTrue(flow["all_failed_witnesses_retained"])

    def test_evidence_manifest_replay(self) -> None:
        replay = load("validation/evidence-manifest-commit-replay.json")
        self.assertTrue(replay["valid"])
        self.assertEqual(replay["entry_count"], 204)
        self.assertEqual(replay["mismatches"], [])

    def test_route_is_not_sent(self) -> None:
        route = load("orchestration/route-state-closeout.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["next_exact_title"], "Neris Solane")
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
            PHASE / "handoffs/neris-solane-v656-v7-activation.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(receipt["word_count"], len(text.split()))
        self.assertGreaterEqual(receipt["word_count"], 10000)
        self.assertLessEqual(receipt["word_count"], 100000)
        self.assertEqual(receipt["state"], "PREPARED_NOT_SENT")
        self.assertIn(
            "This committed file remains `PREPARED_NOT_SENT`", text
        )
        self.assertFalse(
            any(
                line.strip() == "SENT_BY_ELAREN_KESTREL = true"
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

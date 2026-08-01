from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/liora-venn/v657-v7"
SOURCE = "b7f207d4c354dfd2671cd0562a058ac69f83fe35"
FIRST_X1 = "9219708f5a8d16f7faee010f9c7f219f804b59a2"
X1 = "9219708f5a8d16f7faee010f9c7f219f804b59a2"
EVIDENCE = "f10ab507209ce652c645718545054ae237b87962"


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


class V657V7CloseoutTests(unittest.TestCase):
    def test_immutable_anchor_chain(self) -> None:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", EVIDENCE, "HEAD"],
            cwd=ROOT,
            check=True,
        )
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(FIRST_X1, X1)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)

    def test_final_truth_candidate(self) -> None:
        truth = load("truth/phase-truth-final-candidate.json")
        self.assertEqual(
            truth["outcome_counts"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(truth["effective_negatives"], 16313)
        self.assertEqual(truth["effective_methods"], 2588)
        self.assertEqual(
            (truth["effective_open_gaps"], truth["effective_exact_gates"]),
            (111, 110),
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])

    def test_closeout_method_flow_parity(self) -> None:
        flow = load("method-flow/method-flow-state-final.json")
        self.assertEqual(flow["counts"]["current_methods"], 3)
        self.assertEqual(
            flow["counts"]["current_witness_results"], {"fail": 3, "pass": 3}
        )
        self.assertEqual(flow["counts"]["effective_methods"], 2588)
        self.assertEqual(
            flow["counts"]["effective_witness_results"],
            {"fail": 2588, "pass": 2588},
        )
        self.assertTrue(flow["all_failed_witnesses_retained"])

    def test_evidence_manifest_commit_replay(self) -> None:
        replay = load("validation/evidence-manifest-commit-replay.json")
        self.assertTrue(replay["valid"])
        self.assertEqual(replay["entry_count"], 210)
        self.assertEqual(replay["mismatches"], [])

    def test_route_is_held_for_tamar_and_tavian_is_standby(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "HELD_UNRESOLVED_UNTIL_TERMINAL_GATE")
        self.assertEqual(route["next_exact_title"], "Tamar Vey")
        self.assertEqual(route["next_phase"], "v657-v8")
        self.assertFalse(route["later_endpoint_authorized"])
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])
        self.assertEqual(route["tavian_sol_state"], "ON_STANDBY")

    def test_final_records_do_not_preclaim_postcommit_facts(self) -> None:
        final_record = load("lifecycle/final-record.json")
        seal = load("lifecycle/seal-candidate.json")
        plan = load("validation/canonical-aggregate-plan.json")
        self.assertIsNone(final_record["final_commit"])
        self.assertFalse(final_record["canonical_aggregate_passed"])
        self.assertFalse(final_record["fresh_live_equality_passed"])
        self.assertFalse(final_record["route_sent"])
        self.assertIsNone(seal["exact_final"])
        self.assertFalse(seal["canonical_aggregate_passed"])
        self.assertFalse(plan["completed"])
        self.assertEqual(plan["canonical_pass_number"], 0)
        self.assertFalse(plan["replay_after_success_permitted"])

    def test_successor_baton_is_file_backed_and_bounded(self) -> None:
        receipt = load("validation/successor-baton-word-cap.json")
        path = PHASE / "handoffs/tamar-vey-v657-v8-activation.md"
        text = path.read_text(encoding="utf-8")
        self.assertEqual(receipt["word_count"], len(text.split()))
        self.assertGreaterEqual(receipt["word_count"], 10000)
        self.assertLessEqual(receipt["word_count"], 100000)
        self.assertIn("HELD_UNRESOLVED_UNTIL_TERMINAL_GATE", text)
        self.assertFalse(
            any(
                line.strip() in {
                    "SENT_BY_LIORA_VENN = true",
                    "SENT_BY_TAMAR_VEY = true",
                }
                for line in text.splitlines()
            )
        )

    def test_closeout_artifact_packet_exists(self) -> None:
        required = [
            "deliverables/v657-v7-final-candidate-overview.md",
            "final-complete-incomplete-checklist.json",
            "lifecycle/evidence-record.json",
            "lifecycle/closeout-record.json",
            "lifecycle/seal-candidate.json",
            "lifecycle/final-record.json",
            "truth/retained-negative-register-final.json",
            "reflection-remaster/closeout-decision-record.json",
            "workflow/closeout-method-recommendations.json",
            "tooling/ghc-family-index-closeout.md",
            "environment/environment-version-receipt-final.json",
            "wellbeing/wellbeing-check-final.json",
        ]
        self.assertTrue(all((PHASE / path).is_file() for path in required))

    def test_closeout_manifest_contract(self) -> None:
        manifest = load("validation/closeout-content-manifest.json")
        exclusions = {row["path"] for row in manifest["declared_exclusions"]}
        self.assertGreaterEqual(manifest["entry_count"], 220)
        self.assertEqual(manifest["declared_exclusion_count"], 3)
        self.assertIn(
            "docs/liora-venn/v657-v7/validation/closeout-content-manifest.json",
            exclusions,
        )
        self.assertEqual(len(manifest["entries"]), manifest["entry_count"])

    def test_phase_documents_parse_and_stay_bounded(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 180)
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

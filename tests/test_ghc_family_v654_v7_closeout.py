from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/elaren-kestrel/v654-v7"
SOURCE = "fe0dda857137856654566b52875df769ecf781dd"
X1_FREEZE = "6ab0ee98917d4bc912f2d15793cf3f1a81918244"
X1_FINAL = "773528bda8b863218ba4aaed0ce134fcd48abb97"
EVIDENCE = "303e98c74c90c85330343f953784a79e0df5ac70"
CORRECTION = "a904742b9a121da593d19cbd04e3fd826554b655"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class ElarenV654V7CloseoutTests(unittest.TestCase):
    def test_anchor_contract_and_cap(self) -> None:
        contract = load("lifecycle/phase-anchor-contract.json")
        self.assertEqual(
            (
                contract["source"],
                contract["x1_freeze"],
                contract["x1_final"],
                contract["evidence"],
                contract["evidence_correction"],
            ),
            (SOURCE, X1_FREEZE, X1_FINAL, EVIDENCE, CORRECTION),
        )
        self.assertEqual(contract["expected_phase_commits_after_final"], 5)
        self.assertEqual(contract["maximum_phase_commits"], 8)
        self.assertTrue(contract["zero_merges_required"])
        for anchor in (SOURCE, X1_FREEZE, X1_FINAL, EVIDENCE, CORRECTION):
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", anchor, "HEAD"],
                cwd=REPO,
                check=True,
            )

    def test_truth_and_method_flow(self) -> None:
        closeout = load("closeout/closeout-receipt.json")
        self.assertEqual(
            closeout["outcomes"],
            {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            },
        )
        self.assertEqual(closeout["effective_negatives"], 12052)
        self.assertEqual(
            (
                closeout["effective_open_gaps"],
                closeout["effective_exact_gates"],
            ),
            (87, 86),
        )
        self.assertEqual(
            (
                closeout["method_count"],
                closeout["failed_witnesses"],
                closeout["passing_witnesses"],
            ),
            (161, 161, 161),
        )
        self.assertEqual(closeout["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_route_is_prepared_not_sent(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["successor_exact_title"], "Neris Solane")
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])

    def test_final_record_does_not_preclaim_own_commit(self) -> None:
        final = load("lifecycle/final-record.json")
        protocol = load("validation/final-validation-protocol.json")
        seal = load("seal/seal-receipt.json")
        self.assertIsNone(final["final_commit"])
        self.assertEqual(final["route_state"], "PREPARED_NOT_SENT")
        self.assertEqual(protocol["state"], "POSTCOMMIT_REQUIRED")
        self.assertFalse(protocol["completed"])
        self.assertFalse(protocol["preclaims_exact_final_head"])
        self.assertFalse(protocol["preclaims_route_sent"])
        self.assertFalse(seal["exact_final_commit_known_inside_own_tree"])

    def test_baton_is_file_backed_sanitized_and_bounded(self) -> None:
        baton = (
            PHASE / "handoffs/neris-solane-v654-v8-activation.md"
        ).read_text(encoding="utf-8")
        words = len(baton.split())
        self.assertGreaterEqual(words, 10_000)
        self.assertLessEqual(words, 100_000)
        self.assertIn("PREPARED_NOT_SENT", baton)
        self.assertIn("Neris Solane", baton)
        self.assertNotIn("source_thread_id", baton)
        self.assertNotIn("resume_token", baton)
        self.assertNotIn("D:\\", baton)
        self.assertNotIn("C:\\Users", baton)

    def test_owner_manifest_has_exact_prospective_coverage(self) -> None:
        manifest = load("validation/final-owner-manifest.json")
        exclusions = set(manifest["self_exclusions"])
        actual = {
            path.relative_to(REPO).as_posix()
            for path in PHASE.rglob("*")
            if path.is_file()
        }
        entries = {row["path"] for row in manifest["entries"]}
        self.assertEqual(entries, actual - exclusions)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            self.assertEqual(
                row["git_blob"],
                git("hash-object", f"--path={row['path']}", row["path"]),
            )

    def test_document_and_file_caps(self) -> None:
        documents = load("validation/document-word-cap.json")
        files = load("validation/owner-file-threshold.json")
        self.assertTrue(documents["baton_within_bounds"])
        self.assertTrue(files["below_threshold"])
        self.assertLess(
            files["owner_file_count_before_lifecycle_self_exclusions"],
            files["threshold"],
        )
        self.assertFalse(files["inherited_repository_baseline_counted"])

    def test_evidence_correction_is_preserved(self) -> None:
        correction = load("validation/evidence-correction-staged-review.json")
        negatives = load("truth/retained-negative-register-x2.json")
        final_negatives = load("truth/retained-negative-register-final.json")
        self.assertTrue(correction["valid"])
        self.assertEqual(negatives["effective_at_evidence"], 12049)
        self.assertEqual(negatives["x2_operational_count"], 10)
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual(final_negatives["effective_at_final_candidate"], 12052)
        self.assertEqual(final_negatives["final_operational_count"], 3)
        self.assertTrue(final_negatives["no_failure_erased"])


if __name__ == "__main__":
    unittest.main()

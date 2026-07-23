from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/neris-solane/v652-v8"
SOURCE = "c39461888fa4db827616214f11c893fc6b0d40a3"
X1 = "6e5c0e6fbe1bc569bd2eb8971629f2125f1c1984"
EVIDENCE = "b9e3c008492f6ed6235dc60e77282acc71aa736d"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


class V652V8CloseoutTests(unittest.TestCase):
    def test_closeout_truth(self) -> None:
        closeout = load("closeout-receipt.json")
        self.assertEqual(closeout["outcomes"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(closeout["effective_negatives"], 9268)
        self.assertEqual((closeout["effective_open_gaps"], closeout["effective_exact_gates"]), (69, 70))
        self.assertEqual((closeout["method_fail_witnesses"], closeout["method_pass_witnesses"]), (20, 20))
        self.assertEqual(closeout["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(closeout["full_repository_suite_run"])

    def test_route_is_prepared_not_sent(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["recipient_exact_title"], "Vesper Arlen")
        self.assertFalse(route["task_resolved"])
        self.assertFalse(route["activation_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["collaboration_subagent_spawned"])
        self.assertFalse(route["fast_mode_claimed"])

    def test_no_post_commit_preclaim(self) -> None:
        record = load("lifecycle/final-record.json")
        protocol = load("validation/final-validation-protocol.json")
        self.assertIsNone(record["final_commit"])
        self.assertEqual(protocol["state"], "POST_COMMIT_REQUIRED")
        self.assertFalse(protocol["completed"])
        self.assertFalse(protocol["preclaims_final_head"])
        self.assertFalse(protocol["preclaims_task_creation"])
        self.assertFalse(protocol["preclaims_activation_send"])

    def test_baton_is_file_backed_and_bounded(self) -> None:
        receipt = load("handoffs/baton-receipt.json")
        words = len((PHASE / "handoffs/vesper-arlen-v653-v1-activation.md").read_text(encoding="utf-8").split())
        self.assertEqual(words, receipt["word_count"])
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertEqual(receipt["state"], "PREPARED_NOT_SENT")

    def test_owner_manifest_covers_public_surface(self) -> None:
        manifest = load("validation/final-owner-manifest.json")
        exclusions = set(manifest["self_exclusions"])
        phase_paths = {path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()}
        script_paths = {path.relative_to(ROOT).as_posix() for path in (ROOT / "scripts").glob("*v652_v8*.py")}
        test_paths = {path.relative_to(ROOT).as_posix() for path in (ROOT / "tests").glob("test_ghc_family_v652_v8*.py")}
        runners = {
            f"scripts/{row['runner']}"
            for row in load("runners/runner-invocation-receipt.json")["runners"]
        }
        public_paths = phase_paths | script_paths | test_paths | runners
        entry_paths = {row["path"] for row in manifest["entries"]}
        self.assertEqual(entry_paths, public_paths - exclusions)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))

    def test_anchor_history_and_commit_cap(self) -> None:
        for anchor in (SOURCE, X1, EVIDENCE):
            subprocess.run(["git", "merge-base", "--is-ancestor", anchor, "HEAD"], cwd=ROOT, check=True)
        count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
        self.assertIn(count, {2, 3})
        self.assertLessEqual(count, 8)
        self.assertEqual(git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD"), "0")

    def test_external_boundaries_remain_incomplete(self) -> None:
        checklist = load("final-complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["incomplete_external"]), 6)
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()

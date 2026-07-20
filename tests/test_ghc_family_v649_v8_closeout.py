from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "elaren-kestrel" / "v649-v8"
SOURCE = "68f54882fa665f75cb181d9a9a64853802db5554"
X1 = "4664cdb728f0b9c2b11f478b35c1deb2e893f34f"
EVIDENCE = "e514ddfc6dad686ad86858b9fbd0bf1e374b568d"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


class V649V8CloseoutTests(unittest.TestCase):
    def test_anchor_contract_and_commit_cadence(self) -> None:
        for anchor in (SOURCE, X1, EVIDENCE):
            subprocess.run(["git", "merge-base", "--is-ancestor", anchor, "HEAD"], cwd=ROOT, check=True)
        count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
        self.assertIn(count, {2, 3})
        self.assertLessEqual(count, 4)
        self.assertEqual(git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD"), "0")

    def test_truth_and_expanded_portfolios(self) -> None:
        receipt = load("closeout-receipt.json")
        self.assertEqual(receipt["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(receipt["effective_negatives"], 5444)
        self.assertEqual((receipt["effective_open_gaps"], receipt["effective_exact_gates"]), (42, 43))
        self.assertEqual((receipt["safe_completed"], receipt["candidate_completed"]), (40, 30))
        self.assertEqual((receipt["skills_completed"], receipt["runners_completed"], receipt["clean_refine_completed"]), (20, 10, 40))
        self.assertEqual((receipt["method_fail_witnesses"], receipt["method_pass_witnesses"]), (13, 13))
        self.assertFalse(receipt["full_repository_suite_run"])
        self.assertEqual(receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_long_baton_is_bounded_and_route_unsent(self) -> None:
        path = PHASE / "handoffs" / "eiren-kestrel-3-v650-v1-activation.md"
        words = len(path.read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 8000)
        self.assertLessEqual(words, 20000)
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["target_exact_title"], "Eiren Kestrel (3)")
        self.assertFalse(route["message_sent"] or route["task_created"] or route["task_forked"] or route["subagent_spawned"])

    def test_final_protocol_does_not_preclaim_post_commit_proof(self) -> None:
        protocol = load("validation/final-validation-protocol.json")
        record = load("lifecycle/final-record-candidate.json")
        truth = load("phase-truth-closeout-candidate.json")
        self.assertEqual(protocol["state"], "POST_COMMIT_REQUIRED")
        self.assertEqual(protocol["successful_pass_budget"], 1)
        self.assertFalse(protocol["post_success_replay"])
        self.assertFalse(protocol["completed"])
        self.assertIsNone(record["final_commit"])
        self.assertIsNone(truth["final_commit"])
        self.assertEqual(record["route_state"], "PREPARED_NOT_SENT")

    def test_final_owner_manifest_covers_declared_surface(self) -> None:
        manifest = load("validation/final-owner-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["declared_exclusion_count"], 4)
        for row in manifest["entries"]:
            self.assertEqual(row["git_blob"], git("hash-object", f"--path={row['repository_path']}", row["repository_path"]))

    def test_staged_review_and_document_caps(self) -> None:
        review = load("validation/final-staged-review.json")
        privacy = load("validation/final-staged-privacy.json")
        documents = load("validation/final-document-cap-receipt.json")
        self.assertTrue(review["passed"])
        self.assertEqual(review["out_of_scope_paths"], [])
        self.assertEqual(review["evidence_frozen_changes"], [])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(documents["all_under_20000"])
        self.assertTrue(documents["baton_within_8000_20000"])


if __name__ == "__main__":
    unittest.main()

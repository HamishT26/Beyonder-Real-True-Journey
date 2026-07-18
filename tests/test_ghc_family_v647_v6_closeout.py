from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v647-v6"
SOURCE = "3c4fa7ba58362ae39a5aa009fe9a899acc092301"
X1 = "650e9f0e6d17118cf8b2389adf2a984cfc63cf08"
EVIDENCE = "400f5af29759a624bf4f095b50b4c7468e3a25b9"
FINAL = "c02273291edcbe408f28647495183e9ed4641995"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


class V647V6CloseoutTests(unittest.TestCase):
    def test_anchor_contract_and_commit_cap(self) -> None:
        contract = load("lifecycle/phase-anchor-contract.json")
        self.assertEqual((contract["source_commit"], contract["x1_commit"], contract["evidence_commit"]), (SOURCE, X1, EVIDENCE))
        for anchor in (SOURCE, X1, EVIDENCE):
            subprocess.run(["git", "merge-base", "--is-ancestor", anchor, FINAL], cwd=ROOT, check=True)
        count = int(git("rev-list", "--count", f"{SOURCE}..{FINAL}"))
        self.assertIn(count, {2, 3})
        self.assertLessEqual(count, 4)
        self.assertEqual(git("rev-list", "--count", "--merges", f"{SOURCE}..{FINAL}"), "0")

    def test_truth_counts_and_abstention(self) -> None:
        closeout = load("closeout-receipt.json")
        self.assertEqual(closeout["outcomes"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(closeout["effective_negatives"], 3669)
        self.assertEqual((closeout["effective_open_gaps"], closeout["effective_exact_gates"]), (23, 24))
        self.assertEqual((closeout["method_fail_witnesses"], closeout["method_pass_witnesses"]), (18, 18))
        self.assertEqual(closeout["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(closeout["full_repository_suite_run"])

    def test_route_remains_prepared_not_sent(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])

    def test_protocol_does_not_preclaim_post_commit_proof(self) -> None:
        protocol = load("validation/final-validation-protocol.json")
        final_record = load("lifecycle/final-record.json")
        replay = load("reproduction/same-owner-replay-plan.json")
        self.assertEqual(protocol["state"], "POST_COMMIT_REQUIRED")
        self.assertFalse(protocol["completed"])
        self.assertFalse(protocol["preclaims_exact_final_head"])
        self.assertIsNone(final_record["final_commit"])
        self.assertEqual(replay["state"], "PENDING_POST_COMMIT")
        self.assertFalse(replay["independent_reproduction"])

    def test_owner_manifest_covers_exact_phase_surface(self) -> None:
        manifest = load("validation/final-owner-manifest.json")
        exclusions = set(manifest["self_exclusions"])
        owner_paths = {path.relative_to(PHASE).as_posix() for path in PHASE.rglob("*") if path.is_file()}
        entry_paths = {row["path"] for row in manifest["entries"]}
        self.assertEqual(entry_paths, owner_paths - exclusions)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            repository_relative = f"docs/ilyra-fen/v647-v6/{row['path']}"
            self.assertEqual(row["git_blob"], git("hash-object", f"--path={repository_relative}", repository_relative))

    def test_documents_and_owner_growth_are_bounded(self) -> None:
        documents = load("validation/document-cap-receipt.json")
        files = load("validation/owner-file-threshold-receipt.json")
        self.assertTrue(documents["all_under_6000"])
        self.assertLessEqual(documents["maximum_words"], 6000)
        self.assertTrue(files["below_threshold"])
        self.assertFalse(files["inherited_repository_baseline_counted"])

    def test_final_artifact_packet_exists(self) -> None:
        required = [
            "closeout-receipt.json", "seal-receipt.json", "final-complete-incomplete-checklist.json",
            "validation/final-validation-protocol.json", "validation/final-owner-manifest.json",
            "orchestration/applicable-memory-record.json", "orchestration/successor-baton-preparation.json",
            "tooling/ghc-family-index.json", "tooling/ghc-family-index.md",
        ]
        self.assertTrue(all((PHASE / path).is_file() for path in required))


if __name__ == "__main__":
    unittest.main()

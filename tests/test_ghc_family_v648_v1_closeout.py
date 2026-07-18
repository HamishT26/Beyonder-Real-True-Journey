from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v648-v1"
SOURCE = "4ada48d3142a6d33e4c723184edbb84e59e22aa4"
X1 = "3e2904ec02c893d91c16e9a48fbb2485fc5d824f"
EVIDENCE = "b09681afe5a4cac101bab367ef761e4ac1a7b57e"
FINAL = "8755893971135b67322abb4b3acd93f07afc34c9"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


class V648V1CloseoutTests(unittest.TestCase):
    def test_anchor_contract_and_commit_cap(self):
        contract = load("lifecycle/phase-anchor-contract.json")
        self.assertEqual((SOURCE, X1, EVIDENCE), (contract["source_commit"], contract["x1_commit"], contract["evidence_commit"]))
        for anchor in (SOURCE, X1, EVIDENCE):
            subprocess.run(["git", "merge-base", "--is-ancestor", anchor, FINAL], cwd=ROOT, check=True)
        count = int(git("rev-list", "--count", f"{SOURCE}..{FINAL}"))
        self.assertIn(count, {2, 3})
        self.assertLessEqual(count, 4)
        self.assertEqual("0", git("rev-list", "--count", "--merges", f"{SOURCE}..{FINAL}"))

    def test_closeout_counts_and_abstention(self):
        receipt = load("closeout-receipt.json")
        self.assertEqual({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, receipt["outcomes"])
        self.assertEqual((3937, 26, 27), (receipt["effective_negatives"], receipt["effective_open_gaps"], receipt["effective_exact_gates"]))
        self.assertEqual((11, 15, 15), (receipt["method_count"], receipt["method_fail_witnesses"], receipt["method_pass_witnesses"]))
        self.assertEqual("NOT_READY_FOR_STAGE_20", receipt["terminal_verdict"])
        self.assertFalse(receipt["full_repository_suite_run"])

    def test_closeout_operational_negatives_are_retained(self):
        lifecycle = load("validation/lifecycle-operational-negatives.json")
        final = load("retained-negative-register-final.json")
        self.assertEqual(11, lifecycle["count"])
        self.assertTrue(lifecycle["all_retained"])
        self.assertEqual(0, lifecycle["erased_negative_count"])
        self.assertEqual(3937, final["effective_total"])
        self.assertEqual(0, final["erased_negative_count"])

    def test_final_records_do_not_preclaim_postcommit_proof(self):
        seal = load("seal-receipt.json")
        record = load("lifecycle/final-record.json")
        protocol = load("validation/final-validation-protocol.json")
        self.assertIsNone(seal["final_commit"])
        self.assertFalse(seal["baton_send_allowed_now"])
        self.assertIsNone(record["final_commit"])
        self.assertFalse(record["exact_final_validated"])
        self.assertFalse(protocol["completed"])
        self.assertFalse(protocol["preclaims_exact_final_head"])

    def test_route_is_prepared_not_sent(self):
        route = load("orchestration/terminal-route-state.json")
        preparation = load("orchestration/successor-baton-preparation.json")
        self.assertEqual("PREPARED_NOT_SENT", route["state"])
        self.assertEqual(("Sylven Arc", "v648-gmut-thos-v2-x1-x2"), (preparation["target_existing_task_title"], preparation["target_phase"]))
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])

    def test_documents_and_growth_are_bounded(self):
        documents = load("validation/document-cap-receipt.json")
        self.assertTrue(documents["all_under_6000"])
        self.assertGreaterEqual(documents["overview_words"], 1200)
        self.assertLess(sum(1 for p in PHASE.rglob("*") if p.is_file()), 15000)

    def test_owner_manifest_covers_exact_phase_surface(self):
        manifest_path = PHASE / "validation/final-owner-manifest.json"
        if not manifest_path.exists():
            self.skipTest("owner manifest is materialized by exact staged review")
        manifest = load("validation/final-owner-manifest.json")
        exclusions = set(manifest["self_exclusions"])
        owner_paths = {p.relative_to(PHASE).as_posix() for p in PHASE.rglob("*") if p.is_file()}
        entries = {row["path"] for row in manifest["entries"]}
        self.assertEqual(owner_paths - exclusions, entries)
        self.assertTrue(manifest["valid"])


if __name__ == "__main__":
    unittest.main()

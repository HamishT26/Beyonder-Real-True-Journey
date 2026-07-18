from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v648-v5"
SOURCE_COMMIT = "99c22f254672807ee3839142f261d0ab01585a4a"
X1_COMMIT = "8ca83ea35ecbc72b1a993e04bde6a1dde096f4b9"
EVIDENCE_COMMIT = "7675f49a219b845da440cf80256720ec3ba33e87"
SELECTION = [
    "tests.test_ghc_family_v648_v3",
    "tests.test_ghc_family_v648_v3_2",
    "tests.test_ghc_family_v648_v4",
    "tests.test_ghc_family_v648_v5",
    "tests.test_ghc_family_v648_v5_closeout",
]


def load(relative: str):
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


class TestGhcFamilyV648V5Closeout(unittest.TestCase):
    def test_source_x1_and_evidence_are_ancestral(self) -> None:
        for anchor in (SOURCE_COMMIT, X1_COMMIT, EVIDENCE_COMMIT):
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", anchor, "HEAD"],
                cwd=ROOT,
                check=True,
            )
        self.assertEqual(
            git("rev-list", "--count", "--merges", f"{SOURCE_COMMIT}..HEAD"), "0"
        )

    def test_single_pass_selection_is_exact_and_replay_free(self) -> None:
        plan = load("validation/single-pass-selection.json")
        self.assertEqual(plan["selection"], SELECTION)
        self.assertEqual(plan["successful_run_budget"], 1)
        self.assertEqual(plan["successful_runs_used_before_validation"], 0)
        self.assertFalse(plan["full_repository_suite"])
        self.assertFalse(plan["replay"])

    def test_static_closeout_manifest_uses_exact_git_blob_domain(self) -> None:
        manifest = load("validation/final-staged-manifest.json")
        self.assertEqual(manifest["hash_domain"], "git_hash_object_path_filtered_blob")
        self.assertEqual(manifest["evidence_commit"], EVIDENCE_COMMIT)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["self_exclusions"]), 8)
        for row in manifest["entries"]:
            self.assertEqual(
                git("hash-object", f"--path={row['path']}", row["path"]),
                row["git_blob"],
                row["path"],
            )

    def test_durable_orin_baton_is_sanitized_preparation(self) -> None:
        baton_path = PHASE / "handoffs/orin-thale-v648-v6-activation.md"
        baton = baton_path.read_text(encoding="utf-8")
        manifest = load("handoffs/orin-thale-v648-v6-activation-manifest.json")
        words = len(baton.split())
        self.assertGreaterEqual(words, 4000)
        self.assertLessEqual(words, 6000)
        self.assertEqual(manifest["word_count"], words)
        self.assertEqual(manifest["state"], "PREPARED_NOT_SENT")
        self.assertEqual(manifest["source_head"], SOURCE_COMMIT)
        self.assertEqual(manifest["x1_commit"], X1_COMMIT)
        self.assertEqual(manifest["evidence_commit"], EVIDENCE_COMMIT)
        self.assertFalse(manifest["cross_platform_send"])
        self.assertFalse(manifest["task_created"])
        self.assertFalse(manifest["subagent_spawned"])
        forbidden = [
            "source_" + "thread_id",
            "thread_" + "id=",
            "C:" + "\\Users\\",
            "private_" + "route=",
        ]
        self.assertTrue(all(term not in baton for term in forbidden))

    def test_final_overview_report_and_documents_respect_caps(self) -> None:
        overview = (PHASE / "deliverables/v648-v5-final-overview.md").read_text(
            encoding="utf-8"
        )
        report = (PHASE / "deliverables/v648-v5-static-report.html").read_text(
            encoding="utf-8"
        )
        self.assertGreaterEqual(len(overview.split()), 1200)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertIn("<caption>", report)
        self.assertIn('scope="col"', report)
        self.assertIn("affected-user evaluation remain reserved", report)
        for path in list(PHASE.rglob("*.md")) + list(PHASE.rglob("*.html")):
            self.assertLessEqual(
                len(path.read_text(encoding="utf-8").split()), 6000, path.as_posix()
            )

    def test_method_flow_orchestration_and_threshold_candidates(self) -> None:
        flow = load("method-flow/final-method-flow-candidate.json")
        orchestration = load("orchestration/final-phase-state-candidate.json")
        threshold = load("validation/owner-file-threshold-final.json")
        self.assertEqual(
            (flow["methods"], flow["failed_witnesses"], flow["passing_witnesses"]),
            (8, 8, 8),
        )
        self.assertEqual(flow["failures_erased"], 0)
        self.assertEqual(orchestration["tasks_created"], 0)
        self.assertEqual(orchestration["forks_created"], 0)
        self.assertEqual(orchestration["subagents"], 0)
        self.assertEqual(orchestration["cross_platform_messages"], 0)
        self.assertEqual(orchestration["terminal_route"], "PREPARED_NOT_SENT")
        self.assertTrue(threshold["below_threshold"])

    def test_final_family_index_and_required_packet_exist(self) -> None:
        required = [
            "tooling/final/ghc-family-index.json",
            "tooling/final/ghc-family-index.md",
            "deliverables/v648-v5-final-overview.md",
            "deliverables/v648-v5-static-report.html",
            "threat-model.json",
            "wellbeing-check-x2.json",
            "complete-incomplete-checklist-x2.json",
            "retained-negative-register-x2.json",
            "exact-open-gate-register-x2.json",
            "environment/version-receipt.json",
            "sources/source-ledger.json",
        ]
        self.assertTrue(all((PHASE / relative).is_file() for relative in required))

    def test_result_receipts_if_present_remain_truthful(self) -> None:
        canonical = PHASE / "validation/single-pass-canonical-validation.json"
        if not canonical.exists():
            return
        receipt = json.loads(canonical.read_text(encoding="utf-8"))
        if receipt.get("schema") == "pending":
            return
        self.assertEqual(receipt["canonical_validation_runs"], 1)
        self.assertTrue(receipt["valid"])
        self.assertFalse(receipt["full_repository_suite_run"])
        self.assertEqual(receipt["named_replay_runs"], 0)
        self.assertEqual(receipt["detached_replay_runs"], 0)
        self.assertTrue(receipt["test_result"]["successful"])


if __name__ == "__main__":
    unittest.main()

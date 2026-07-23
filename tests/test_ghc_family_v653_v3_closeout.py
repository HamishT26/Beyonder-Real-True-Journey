from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v653-v3"
SOURCE = "c25e70eaae7c338a22ee64270ab574768835b227"
X1 = "7c2cc69203b827dc4b0be18c10931f8e92477b4a"
EVIDENCE = "684ef89d6c9ea28577b93b7df8a071cb557e9221"


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


class V653V3CloseoutTests(unittest.TestCase):
    def test_closeout_truth(self) -> None:
        closeout = load("closeout-receipt.json")
        self.assertEqual(
            closeout["outcomes"],
            {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            },
        )
        self.assertEqual(closeout["effective_negatives"], 9771)
        self.assertEqual(
            (
                closeout["effective_open_gaps"],
                closeout["effective_exact_gates"],
            ),
            (72, 73),
        )
        self.assertEqual(
            (
                closeout["method_fail_witnesses"],
                closeout["method_pass_witnesses"],
            ),
            (13, 13),
        )
        self.assertEqual(closeout["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(closeout["full_repository_suite_run"])

    def test_route_is_held_without_authorized_successor(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(
            route["state"], "PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE"
        )
        self.assertFalse(route["successor_authorized"])
        self.assertIsNone(route["successor_title"])
        self.assertIsNone(route["successor_phase"])
        self.assertFalse(route["task_resolved"])
        self.assertFalse(route["activation_sent"])
        self.assertEqual(route["activation_send_count"], 0)
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["delegation_used"])
        self.assertFalse(route["collaboration_subagent_spawned"])

    def test_no_post_commit_preclaim(self) -> None:
        record = load("lifecycle/final-record.json")
        protocol = load("validation/final-validation-protocol.json")
        self.assertIsNone(record["final_commit"])
        self.assertEqual(protocol["state"], "POST_COMMIT_REQUIRED")
        self.assertFalse(protocol["completed"])
        self.assertFalse(protocol["preclaims_final_head"])
        self.assertFalse(protocol["preclaims_task_creation"])
        self.assertFalse(protocol["preclaims_activation_send"])

    def test_no_successor_baton_was_fabricated(self) -> None:
        handoffs = PHASE / "handoffs"
        self.assertFalse(handoffs.exists())
        receipt = load("validation/final-document-cap-receipt.json")
        self.assertFalse(receipt["successor_baton_required"])

    def test_owner_manifest_covers_public_surface(self) -> None:
        manifest = load("validation/final-owner-manifest.json")
        exclusions = set(manifest["self_exclusions"])
        phase_paths = {
            path.relative_to(ROOT).as_posix()
            for path in PHASE.rglob("*")
            if path.is_file()
        }
        script_paths = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "scripts").glob("*v653_v3*.py")
        }
        test_paths = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "tests").glob("test_ghc_family_v653_v3*.py")
        }
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
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", anchor, "HEAD"],
                cwd=ROOT,
                check=True,
            )
        count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
        self.assertIn(count, {2, 3})
        self.assertLessEqual(count, 8)
        self.assertEqual(
            git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD"), "0"
        )

    def test_overview_and_accessibility_reservation(self) -> None:
        overview = (
            PHASE / "reports/final-integrated-overview.md"
        ).read_text(encoding="utf-8")
        report = (PHASE / "reports/final-static-report.html").read_text(
            encoding="utf-8"
        )
        self.assertGreaterEqual(len(overview.split()), 1500)
        self.assertIn("<caption>", report)
        self.assertIn('scope="col"', report)
        self.assertIn("Manual keyboard", report)
        self.assertIn("affected-user evaluation remain reserved", report)

    def test_external_boundaries_remain_incomplete(self) -> None:
        checklist = load("final-complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["incomplete_external"]), 6)
        self.assertEqual(
            checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20"
        )
        negatives = load("retained-negative-register-final.json")
        self.assertEqual(negatives["post_evidence_operational_count"], 2)
        self.assertEqual(negatives["effective_total"], 9771)
        self.assertTrue(negatives["none_erased"])


if __name__ == "__main__":
    unittest.main()

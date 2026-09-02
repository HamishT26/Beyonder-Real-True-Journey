"""Exact owner-closeout tests for Lyren Moss v683-v2."""

from __future__ import annotations

import hashlib
import json
import subprocess  # nosec B404
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v683-v2"
FINAL = BASE / "final"
VALIDATION = BASE / "validation"
CLOSEOUT = BASE / "closeout"
HANDOFF = BASE / "handoffs" / "ilyra-fen-v683-v3-activation-candidate.md"
SOURCE = "484d44fb8875bf8129143c99e5340d2e2044fbd2"
X1 = "57dcd8a0e6e5a43f87d6f1a5a0d79d2d68b66d8b"
EVIDENCE = "d0240efd7c7369e1468882d62bebddce32cf8b85"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def run_git(*args: str, text: bool = True):
    return subprocess.run(  # nosec B603
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=text,
    )


class LyrenMossV683V2FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = load(FINAL / "phase-truth.json")
        cls.flow = load(FINAL / "method-flow-summary.json")
        cls.negatives = load(FINAL / "retained-negative-register.json")
        cls.gaps = load(FINAL / "open-gap-register.json")
        cls.gates = load(FINAL / "exact-gate-register.json")
        cls.delta = load(VALIDATION / "final-delta-manifest.json")
        cls.owner = load(VALIDATION / "final-owner-manifest.json")
        cls.review = load(VALIDATION / "final-staged-review.json")
        cls.privacy = load(VALIDATION / "final-privacy-scan.json")
        cls.seal = load(CLOSEOUT / "content-seal.json")

    def test_01_identity_is_relational_and_corrigible(self) -> None:
        wellbeing = load(FINAL / "wellbeing-check.json")
        self.assertEqual(wellbeing["name"], "Lyren Moss")
        self.assertIsNone(wellbeing["optional_pronouns"])
        self.assertEqual(
            wellbeing["role"], "acoustic provenance cartographer and non-playback boundary keeper"
        )
        self.assertTrue(wellbeing["relational_working_language_only"])
        self.assertTrue(wellbeing["corrigible"])
        self.assertEqual(wellbeing["pause_redirect_rename_stop_right"], "Hamish")

    def test_02_overview_and_baton_word_bounds(self) -> None:
        overview = (FINAL / "final-integrated-overview.md").read_text(encoding="utf-8")
        baton = HANDOFF.read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1200)
        self.assertLessEqual(len(overview.split()), 100000)
        self.assertGreaterEqual(len(baton.split()), 10000)
        self.assertLessEqual(len(baton.split()), 100000)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertIn("SENT_BY_LYREN_MOSS = false", baton)

    def test_03_phase_truth_has_only_four_outcomes(self) -> None:
        self.assertEqual(
            self.truth["outcomes"],
            {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        )
        self.assertEqual(
            set(self.truth["outcomes"]), {"completed", "represented", "open_gap", "exact_gate"}
        )
        self.assertEqual(self.truth["declared_proposal_chain"], 10790)
        self.assertEqual(self.truth["primary_pillar"], "Freed ID and CBR Heart")
        self.assertEqual(self.truth["real_row_count"], 0)

    def test_04_effective_totals_include_closeout_overlay(self) -> None:
        self.assertEqual(
            self.truth["totals"],
            {
                "bounded_passing_witnesses": 53078,
                "effective_methods": 72159,
                "effective_negatives": 58434,
                "exact_gates": 509,
                "failed_witnesses": 30095,
                "open_gaps": 519,
            },
        )
        self.assertEqual(self.negatives["operational_failure_count"], 20)
        ids = {row["failure_id"] for row in self.negatives["operational_failures"]}
        self.assertIn("LM6832-X1-N014", ids)
        self.assertIn("LM6832-X2-N019", ids)
        self.assertIn("LM6832-FN-N020", ids)
        self.assertTrue(self.negatives["zero_credit_failures_preserved"])

    def test_05_method_flow_never_erases_a_failure(self) -> None:
        self.assertEqual(self.flow["phase_methods"], 774)
        self.assertEqual(self.flow["phase_failed_witnesses"], 320)
        self.assertEqual(self.flow["phase_passing_witnesses"], 714)
        self.assertFalse(self.flow["recovery_erases_failure"])
        self.assertEqual(len(self.flow["closeout_overlay"]), 1)

    def test_06_open_gaps_and_exact_gates_are_additive(self) -> None:
        self.assertEqual(self.gaps["inherited_effective_open_gaps"], 516)
        self.assertEqual(self.gaps["new_open_gap_count"], 3)
        self.assertEqual(self.gaps["total_effective_open_gaps"], 519)
        self.assertTrue(all(row["status"] == "open_gap" for row in self.gaps["new_open_gaps"]))
        self.assertEqual(self.gates["inherited_effective_exact_gates"], 506)
        self.assertEqual(self.gates["new_exact_gate_count"], 3)
        self.assertEqual(self.gates["total_effective_exact_gates"], 509)
        self.assertTrue(all(row["status"] == "exact_gate" for row in self.gates["new_exact_gates"]))

    def test_07_portfolios_preserve_approval_holds(self) -> None:
        summary = load(FINAL / "portfolio-summary.json")
        self.assertEqual(summary["safe_now_completed"], 120)
        self.assertEqual(summary["bounded_candidates_executed_without_core_promotion"], 80)
        self.assertEqual(summary["clean_fix_refine_completed"], 100)
        self.assertEqual(summary["exact_approval_unexecuted"], 20)
        self.assertEqual(summary["blocked_unexecuted"], 10)

    def test_08_skills_and_runners_are_bounded_and_not_global(self) -> None:
        summary = load(FINAL / "skill-runner-summary.json")
        self.assertEqual(summary["skill_count"], 20)
        self.assertEqual(summary["runner_count"], 10)
        self.assertFalse(summary["global_skill_installation"])
        self.assertTrue(
            summary["skills_full_read_quick_validated_accepting_and_rejecting_smoke_passed"]
        )
        self.assertTrue(summary["runners_accepting_and_rejecting_smoke_passed"])

    def test_09_static_report_has_structural_accessibility(self) -> None:
        html = (FINAL / "accessible-static-report.html").read_text(encoding="utf-8").lower()
        for token in (
            '<html lang="en">',
            'href="#main"',
            '<main id="main">',
            "<h1>",
            "<h2",
            "<table",
            "<caption>",
            'scope="col"',
            'scope="row"',
        ):
            self.assertIn(token, html)
        self.assertIn("manual browser-diverse", html)
        self.assertNotIn("<script", html)

    def test_10_versions_were_verified_without_host_mutation(self) -> None:
        receipt = load(FINAL / "environment-version-receipt.json")
        self.assertTrue(receipt["versions_verified_only"])
        self.assertFalse(receipt["codex_desktop_updated"])
        self.assertFalse(receipt["host_security_changed"])
        self.assertFalse(receipt["rebooted"])
        self.assertEqual(receipt["codex_cli"], "0.151.0")
        self.assertEqual(receipt["npm"], "12.0.2")

    def test_11_all_final_json_documents_parse(self) -> None:
        paths = (
            sorted(FINAL.glob("*.json"))
            + sorted(VALIDATION.glob("final-*.json"))
            + [CLOSEOUT / "content-seal.json"]
        )
        self.assertEqual(len(paths), 21)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_12_final_manifests_replay_normalized_worktree_bytes(self) -> None:
        head = run_git("rev-parse", "HEAD").stdout.strip()
        for manifest in (self.delta, self.owner):
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            entries = {row["path"] for row in manifest["entries"]}
            exclusions = set(manifest["declared_self_exclusions"])
            self.assertFalse(entries & exclusions)
            for entry in manifest["entries"]:
                data = (
                    normalized(ROOT / entry["path"])
                    if head == EVIDENCE
                    else run_git("show", f"HEAD:{entry['path']}", text=False).stdout
                )
                self.assertEqual(len(data), entry["bytes"], entry["path"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])
        self.assertEqual(
            set(self.review["expected_paths"]),
            {row["path"] for row in self.delta["entries"]}
            | set(self.delta["declared_self_exclusions"]),
        )

    def test_13_immutable_x1_and_evidence_manifests_replay_git_blobs(self) -> None:
        for commit, path in (
            (X1, "docs/lyren-moss/v683-v2/validation/x1-index-manifest.json"),
            (EVIDENCE, "docs/lyren-moss/v683-v2/validation/evidence-index-manifest.json"),
        ):
            manifest = json.loads(run_git("show", f"{commit}:{path}", text=False).stdout.decode("utf-8"))
            for entry in manifest["entries"]:
                data = run_git("show", f"{commit}:{entry['path']}", text=False).stdout
                self.assertEqual(len(data), entry["bytes"], entry["path"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_14_content_seal_replays(self) -> None:
        self.assertEqual(self.seal["target_count"], 10)
        for entry in self.seal["targets"]:
            data = normalized(ROOT / entry["path"])
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_15_lifecycle_is_direct_and_zero_merge(self) -> None:
        lifecycle = load(FINAL / "lifecycle-replay.json")
        self.assertEqual(lifecycle["source"], SOURCE)
        self.assertEqual(lifecycle["x1"], X1)
        self.assertEqual(lifecycle["evidence"], EVIDENCE)
        self.assertEqual(run_git("rev-parse", f"{X1}^").stdout.strip(), SOURCE)
        self.assertEqual(run_git("rev-parse", f"{EVIDENCE}^").stdout.strip(), X1)
        head = run_git("rev-parse", "HEAD").stdout.strip()
        if head != EVIDENCE:
            self.assertEqual(run_git("rev-parse", "HEAD^").stdout.strip(), EVIDENCE)
            self.assertEqual(
                len(run_git("rev-list", "--reverse", f"{SOURCE}..HEAD").stdout.splitlines()), 3
            )
            self.assertEqual(run_git("rev-list", "--merges", f"{SOURCE}..HEAD").stdout.splitlines(), [])

    def test_16_terminal_verdict_and_delivery_remain_bounded(self) -> None:
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        delivery = load(FINAL / "delivery-state.json")
        self.assertEqual(delivery["candidate_repository_state"], "PREPARED_NOT_SENT")
        self.assertEqual(delivery["send_count"], 0)
        self.assertEqual(delivery["prospective_successor_exact_title"], "Ilyra Fen")
        self.assertEqual(delivery["prospective_successor_phase"], "v683-v3")
        self.assertEqual(delivery["tavian_sol"], "ON_STANDBY")
        self.assertEqual(self.privacy["class_count"], 5)
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertEqual(self.privacy["confirmed_hits"], [])


if __name__ == "__main__":
    unittest.main()

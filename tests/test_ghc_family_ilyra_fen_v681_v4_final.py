from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v681-v4"
FINAL = BASE / "final"
VALIDATION = BASE / "validation"
SOURCE = "883bb81ded9a802d4b220db5aa24974559465cf1"
X1 = "27943a6e5d03812dfa9cae6795b204b0a3237e6b"
EVIDENCE = "aca60506d377f96c7a321b8585fda73668584f64"
BRANCH = "codex/GHC-Family/ilyra-fen-v681-v4-full-tools"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class IlyraFenV681V4FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = load(FINAL / "phase-truth.json")
        cls.method = load(FINAL / "method-flow-final.json")
        cls.owner_manifest = load(VALIDATION / "final-owner-manifest.json")
        cls.delta_manifest = load(VALIDATION / "final-delta-manifest.json")
        cls.review = load(VALIDATION / "final-staged-review.json")

    def test_branch_and_single_parent_lifecycle(self) -> None:
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        head = git("rev-parse", "HEAD")
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        if head == EVIDENCE:
            self.assertEqual(int(git("rev-list", "--count", f"{SOURCE}..HEAD")), 2)
        else:
            self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)
            self.assertEqual(int(git("rev-list", "--count", f"{SOURCE}..HEAD")), 3)
        self.assertEqual(int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")), 0)

    def test_phase_truth(self) -> None:
        self.assertEqual(self.truth["declared_chain"], 9950)
        self.assertEqual(self.truth["proposal_count"], 60)
        self.assertEqual(self.truth["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(self.truth["counts"]["effective_negatives"], 53896)
        self.assertEqual(self.truth["counts"]["effective_methods"], 61503)
        self.assertEqual(self.truth["counts"]["failed_witnesses"], 25557)
        self.assertEqual(self.truth["counts"]["bounded_passing_witnesses"], 43325)
        self.assertEqual(self.truth["counts"]["open_gaps"], 476)
        self.assertEqual(self.truth["counts"]["exact_gates"], 467)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_method_flow_retains_every_layer(self) -> None:
        self.assertFalse(self.method["failure_erasure"])
        self.assertFalse(self.method["independent_reproduction_claimed"])
        self.assertEqual(len(self.method["startup_failures"]), 6)
        self.assertEqual(len(self.method["x1_postcommit_failures"]), 0)
        self.assertEqual(len(self.method["x2_operational_failures"]), 4)
        self.assertEqual(len(self.method["closeout_operational_failures"]), 2)
        self.assertEqual(self.method["counts"], self.truth["counts"])

    def test_gap_and_gate_register(self) -> None:
        register = load(FINAL / "open-gap-and-exact-gate-register.json")
        self.assertEqual(register["open_gaps"]["effective_total"], 476)
        self.assertEqual(register["exact_gates"]["effective_total"], 467)
        self.assertEqual(len(register["open_gaps"]["new"]), 3)
        self.assertEqual(len(register["exact_gates"]["new"]), 3)
        self.assertEqual(register["silently_closed"], 0)

    def test_environment_is_verified_only(self) -> None:
        receipt = load(FINAL / "environment-version-receipt.json")
        self.assertEqual(receipt["codex_cli"], "0.151.0")
        self.assertEqual(receipt["desktop_app"], "26.825.6671.0")
        self.assertTrue(receipt["verified_only"])
        self.assertFalse(receipt["desktop_app_updated"])
        self.assertFalse(receipt["windows_feature_or_security_change"])

    def test_baton_is_large_sanitized_candidate_not_send(self) -> None:
        path = BASE / "handoffs" / "auren-lark-v681-v5-activation-candidate.md"
        text = path.read_text(encoding="utf-8")
        words = len(text.split())
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertIn("PREPARED_NOT_SENT = true", text)
        self.assertIn("PREPARED_BY_ILYRA_FEN = true", text)
        self.assertIn("SENT_BY_ILYRA_FEN = false", text)
        self.assertNotIn("source" + "_thread_id", text)
        self.assertNotIn("codex" + "_delegation", text)

    def test_route_is_held_for_terminal_gate(self) -> None:
        route = load(FINAL / "route-gate.json")
        self.assertEqual(route["exact_title"], "Auren Lark")
        self.assertEqual(route["next_phase"], "v681-v5")
        self.assertTrue(route["prepared_not_sent"])
        self.assertFalse(route["recipient_contacted"])
        self.assertFalse(route["sent_by_ilyra_fen"])
        self.assertTrue(route["send_requires_exact_terminal_gate"])

    def test_overview_is_three_page_equivalent_and_bounded(self) -> None:
        overview = (FINAL / "integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1800)
        for phrase in ("GMUT remains", "THOS remains", "Freed ID remains", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(phrase, overview)
        for path in BASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, str(path))

    def test_content_seal_replays_worktree_bytes(self) -> None:
        seal = load(FINAL / "content-seal.json")
        self.assertEqual(seal["entry_count"], 15)
        for row in seal["entries"]:
            data = normalized(ROOT / row["path"])
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_delta_manifest_replays_worktree_bytes(self) -> None:
        self.assertEqual(self.delta_manifest["entry_count"], len(self.delta_manifest["entries"]))
        for row in self.delta_manifest["entries"]:
            data = normalized(ROOT / row["path"])
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_owner_manifest_replays_and_covers_scope(self) -> None:
        entries = {row["path"]: row for row in self.owner_manifest["entries"]}
        exclusions = set(self.owner_manifest["declared_self_exclusions"])
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in BASE.rglob("*")
            if path.is_file()
        }
        actual.update(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "scripts").glob("*ilyra*681*v4*.py")
            if path.is_file()
        )
        actual.update(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "tests").glob("*ilyra*681*v4*.py")
            if path.is_file()
        )
        self.assertEqual(actual, set(entries) | exclusions)
        self.assertLess(len(actual), 2000)
        for path_text, row in entries.items():
            data = normalized(ROOT / path_text)
            self.assertEqual(len(data), row["bytes"], path_text)
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], path_text)

    def test_privacy_scan_has_zero_confirmed_hits(self) -> None:
        scan = load(VALIDATION / "final-privacy-scan.json")
        self.assertEqual(scan["confirmed_hits"], [])
        self.assertEqual(len(scan["privacy_classes"]), 5)
        self.assertEqual(scan["scanned_files"], self.owner_manifest["entry_count"])

    def test_final_staged_review_is_exact_delta(self) -> None:
        expected = set(self.review["expected_paths"])
        self.assertEqual(expected, {row["path"] for row in self.delta_manifest["entries"]} | set(self.review["declared_self_exclusions"]))
        self.assertEqual(self.review["lifecycle"], "final_closeout_and_content_seal")
        self.assertEqual(len(expected), self.review["path_count"])

    def test_complete_incomplete_and_threat_boundaries(self) -> None:
        checklist = load(FINAL / "complete-incomplete-checklist.json")
        threat = load(FINAL / "threat-model.json")
        self.assertGreaterEqual(len(checklist["completed_bounded"]), 8)
        self.assertGreaterEqual(len(checklist["incomplete_or_gated"]), 9)
        self.assertTrue(threat["synthetic_only"])
        self.assertEqual(threat["real_rows"], 0)
        self.assertEqual(threat["external_actions"], 0)

    def test_closeout_receipt_preserves_scope(self) -> None:
        receipt = load(FINAL / "closeout-receipt.json")
        self.assertEqual(receipt["commit_ceiling"], 3)
        self.assertEqual(receipt["expected_final_parent"], EVIDENCE)
        self.assertFalse(receipt["full_repository_suite_claimed"])
        self.assertTrue(receipt["same_owner_only"])
        self.assertEqual(receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()

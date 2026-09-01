from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v681-v5"
X1_DIR = BASE / "x1"
X2_DIR = BASE / "x2"
FINAL = BASE / "final"
VALIDATION = BASE / "validation"
SOURCE = "d2f8f60dfaa4c7bd825ae04d57ba0e76bbb7a151"
X1 = "188eec11e48f3bf8976c39909010f094502ffc05"
EVIDENCE = "f59d2f9a0a52d9ea9d42eaa0926883ab7d12c0fd"
BRANCH = "codex/GHC-Family/auren-lark-v681-v5-full-tools"
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
COUNTS = {
    "effective_negatives": 54214,
    "effective_methods": 62211,
    "failed_witnesses": 25875,
    "bounded_passing_witnesses": 44033,
    "open_gaps": 479,
    "exact_gates": 470,
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


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


def replay_worktree_manifest(manifest: dict[str, Any]) -> None:
    if manifest["entry_count"] != len(manifest["entries"]):
        raise AssertionError("manifest entry_count mismatch")
    for row in manifest["entries"]:
        data = normalized(ROOT / row["path"])
        if len(data) != row["bytes"]:
            raise AssertionError(f"manifest byte mismatch: {row['path']}")
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise AssertionError(f"manifest digest mismatch: {row['path']}")


class AurenLarkV681V5FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = load(FINAL / "phase-truth.json")
        cls.method = load(FINAL / "method-flow-final.json")
        cls.owner_manifest = load(VALIDATION / "final-owner-manifest.json")
        cls.delta_manifest = load(VALIDATION / "final-delta-manifest.json")
        cls.review = load(VALIDATION / "final-staged-review.json")

    def test_01_branch_and_strict_single_parent_lifecycle(self) -> None:
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        head = git("rev-parse", "HEAD")
        if head == EVIDENCE:
            self.assertEqual(int(git("rev-list", "--count", f"{SOURCE}..HEAD")), 2)
        else:
            self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)
            self.assertEqual(int(git("rev-list", "--count", f"{SOURCE}..HEAD")), 3)
        self.assertEqual(int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")), 0)

    def test_02_exact_truth_counts_outcomes_and_verdict(self) -> None:
        self.assertEqual(self.truth["declared_chain"], 10010)
        self.assertEqual(self.truth["proposal_count"], 60)
        self.assertEqual(self.truth["outcomes"], OUTCOMES)
        self.assertEqual(self.truth["counts"], COUNTS)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(set(self.truth["outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_03_method_flow_retains_every_failure_layer(self) -> None:
        self.assertFalse(self.method["failure_erasure"])
        self.assertFalse(self.method["independent_reproduction_claimed"])
        self.assertTrue(self.method["same_owner_only"])
        self.assertEqual(len(self.method["startup_failures"]), 16)
        self.assertEqual(self.method["x1_postcommit_failures"], [])
        self.assertEqual(self.method["x2_operational_failures"], [])
        self.assertEqual(len(self.method["closeout_operational_failures"]), 2)
        self.assertEqual(self.method["counts"], COUNTS)

    def test_04_retained_negative_register_is_additive(self) -> None:
        register = load(FINAL / "retained-negative-register.json")
        self.assertFalse(register["failure_erasure"])
        self.assertEqual(register["startup_failures"], 16)
        self.assertEqual(register["x1_postcommit_failures"], 0)
        self.assertEqual(register["x2_operational_failures"], 0)
        self.assertEqual(register["closeout_operational_failures"], 2)
        self.assertEqual(register["retained_mutations"], 300)
        self.assertEqual(register["effective_negatives"], COUNTS["effective_negatives"])
        self.assertEqual(register["failed_witnesses"], COUNTS["failed_witnesses"])

    def test_05_all_mutations_remain_rejected_and_zero_credit(self) -> None:
        mutations = load(X2_DIR / "mutation-results.json")
        self.assertEqual(mutations["executed"], 300)
        self.assertEqual(mutations["rejected"], 300)
        self.assertTrue(mutations["zero_completion_credit"])
        self.assertFalse(mutations["failure_erasure"])
        self.assertEqual(len(mutations["mutations"]), 300)
        self.assertTrue(all(row["observed"] == "rejected" for row in mutations["mutations"]))

    def test_06_portfolio_counts_and_held_packets(self) -> None:
        portfolio = load(X2_DIR / "portfolio-results.json")
        self.assertEqual(len(portfolio["safe_now"]), 120)
        self.assertEqual(len(portfolio["owner_candidates"]), 80)
        self.assertEqual(len(portfolio["owner_clean_fix_refine"]), 100)
        self.assertEqual(len(portfolio["exact_approval"]), 20)
        self.assertEqual(len(portfolio["blocked"]), 10)
        self.assertEqual(portfolio["successor_records_executed"], 0)

    def test_07_skill_and_runner_receipts_are_owner_local(self) -> None:
        skills = load(X2_DIR / "skill-validation-receipts.json")
        runners = load(X2_DIR / "runner-smoke-receipts.json")
        self.assertEqual(skills["passed"], 20)
        self.assertEqual(len(skills["receipts"]), 20)
        self.assertFalse(skills["global_installation"])
        self.assertFalse(skills["validator_replayed_after_success"])
        self.assertEqual(runners["passed"], 10)
        self.assertEqual(len(runners["receipts"]), 10)
        self.assertEqual(runners["external_actions"], 0)
        self.assertFalse(runners["replayed_after_success"])

    def test_08_tool_boundary_did_not_install_for_a_quota(self) -> None:
        boundary = load(X2_DIR / "tool-use-boundary.json")
        self.assertEqual(boundary["new_packages_installed"], 0)
        self.assertFalse(boundary["global_or_shared_prefix_mutated"])
        self.assertIn("standard-library contracts are sufficient", boundary["reason"])

    def test_09_gap_and_gate_register_stays_open(self) -> None:
        register = load(FINAL / "open-gap-and-exact-gate-register.json")
        self.assertEqual(register["open_gap_total"], COUNTS["open_gaps"])
        self.assertEqual(register["exact_gate_total"], COUNTS["exact_gates"])
        self.assertEqual(len(register["current_open_gaps"]), 3)
        self.assertEqual(len(register["current_exact_gates"]), 3)
        self.assertTrue(all(row["outcome"] == "open_gap" for row in register["current_open_gaps"]))
        self.assertTrue(all(row["outcome"] == "exact_gate" for row in register["current_exact_gates"]))

    def test_10_handoff_is_large_sanitized_candidate_not_a_send(self) -> None:
        path = BASE / "handoffs" / "sable-rook-v681-v6-activation-candidate.md"
        text = path.read_text(encoding="utf-8")
        word_count = len(text.split())
        self.assertGreaterEqual(word_count, 10000)
        self.assertLessEqual(word_count, 100000)
        self.assertIn("PREPARED NOT SENT", text)
        self.assertIn("PREPARED_BY_AUREN_LARK = true", text)
        self.assertIn("Sable Rook", text)
        self.assertIn("Caelen Ash", text)
        self.assertIn("v681-v7", text)
        self.assertIn("live authority must still be refreshed", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertNotIn("source" + "_thread_id", text)
        self.assertNotIn("codex" + "_delegation", text)

    def test_11_route_is_held_until_terminal_gate(self) -> None:
        route = load(FINAL / "route-gate.json")
        self.assertEqual(route["exact_title"], "Sable Rook")
        self.assertEqual(route["next_phase"], "v681-v6")
        self.assertEqual(route["route_state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["recipient_contacted"])
        self.assertTrue(route["duplicate_guard_required"])
        self.assertTrue(route["send_requires_exact_final_canonical_success"])

    def test_12_overview_is_three_page_equivalent_and_bounded(self) -> None:
        overview = (FINAL / "integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1800)
        for phrase in (
            "Freed ID and CBR Heart is primary",
            "THOS Body remains represented",
            "GMUT Mind remains represented",
            "NOT_READY_FOR_STAGE_20",
            "same-owner validation is not independent reproduction",
        ):
            self.assertIn(phrase.casefold(), overview.casefold())
        for path in BASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, str(path))

    def test_13_content_seal_replays_exactly_fifteen_files(self) -> None:
        seal = load(FINAL / "content-seal.json")
        self.assertEqual(seal["entry_count"], 15)
        replay_worktree_manifest(seal)

    def test_14_all_four_manifests_replay_normalized_lf_bytes(self) -> None:
        for name in (
            "x1-index-manifest.json",
            "x2-index-manifest.json",
            "final-delta-manifest.json",
            "final-owner-manifest.json",
        ):
            replay_worktree_manifest(load(VALIDATION / name))

    def test_15_delta_manifest_and_staged_review_are_exact(self) -> None:
        expected = set(self.review["expected_paths"])
        delta = {row["path"] for row in self.delta_manifest["entries"]}
        exclusions = set(self.review["declared_self_exclusions"])
        self.assertEqual(expected, delta | exclusions)
        self.assertEqual(self.review["lifecycle"], "exact_final_closeout")
        self.assertEqual(len(expected), self.review["path_count"])
        self.assertEqual(exclusions, {
            "docs/auren-lark/v681-v5/validation/final-delta-manifest.json",
            "docs/auren-lark/v681-v5/validation/final-owner-manifest.json",
            "docs/auren-lark/v681-v5/validation/final-privacy-scan.json",
            "docs/auren-lark/v681-v5/validation/final-staged-review.json",
        })

    def test_16_owner_manifest_covers_the_exact_bounded_scope(self) -> None:
        entries = {row["path"]: row for row in self.owner_manifest["entries"]}
        exclusions = set(self.owner_manifest["declared_self_exclusions"])
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in BASE.rglob("*")
            if path.is_file()
        }
        actual.update(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "scripts").glob("*auren_lark_v681_v5*.py")
            if path.is_file()
        )
        actual.update(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "tests").glob("*auren_lark_v681_v5*.py")
            if path.is_file()
        )
        runner_paths = load(X2_DIR / "materialization-receipt.json")["generated_runner_paths"]
        actual.update(runner_paths)
        self.assertEqual(actual, set(entries) | exclusions)
        self.assertLess(len(actual), 2000)
        replay_worktree_manifest(self.owner_manifest)

    def test_17_final_privacy_scan_has_zero_confirmed_hits(self) -> None:
        scan = load(VALIDATION / "final-privacy-scan.json")
        self.assertEqual(scan["confirmed_hits"], [])
        self.assertEqual(len(scan["privacy_classes"]), 5)
        self.assertGreater(scan["scanned_files"], 0)

    def test_18_every_owner_json_document_parses_strictly(self) -> None:
        json_paths = [row["path"] for row in self.owner_manifest["entries"] if row["path"].endswith(".json")]
        json_paths.extend(self.owner_manifest["declared_self_exclusions"])
        for path_text in json_paths:
            load(ROOT / path_text)

    def test_19_complete_incomplete_and_threat_boundaries(self) -> None:
        checklist = load(FINAL / "complete-incomplete-checklist.json")
        threat = load(FINAL / "threat-model.json")
        self.assertGreaterEqual(len(checklist["completed_bounded"]), 8)
        self.assertGreaterEqual(len(checklist["incomplete_or_gated"]), 8)
        self.assertEqual(threat["confirmed_private_material_hits"], 0)
        self.assertEqual(threat["external_actions"], 0)
        self.assertTrue(threat["five_class_privacy_scan_required"])
        self.assertIn("real civic-tree and location data", threat["protected_surfaces"])

    def test_20_closeout_receipt_preserves_scope_and_commit_cap(self) -> None:
        receipt = load(FINAL / "closeout-receipt.json")
        self.assertEqual(receipt["commit_ceiling"], 3)
        self.assertEqual(receipt["commits_before_final"], 2)
        self.assertEqual(receipt["source"], SOURCE)
        self.assertEqual(receipt["x1"], X1)
        self.assertEqual(receipt["evidence"], EVIDENCE)
        self.assertTrue(receipt["prepared_not_sent"])
        self.assertEqual(receipt["canonical_invocations"], 0)
        self.assertEqual(receipt["canonical_successes"], 0)
        self.assertEqual(receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_21_environment_receipt_is_attributable_not_authority(self) -> None:
        receipt = load(FINAL / "environment-version-receipt.json")
        self.assertEqual(receipt["owner"], "Auren Lark")
        self.assertEqual(receipt["phase"], "v681-v5")
        self.assertTrue(receipt["python"])
        self.assertTrue(receipt["git"].startswith("git version"))
        self.assertIn("ruff", receipt["ruff"].casefold())

    def test_22_source_ledger_preserves_immutable_anchors(self) -> None:
        ledger = load(FINAL / "source-and-proposal-ledger.json")
        self.assertEqual(ledger["source"], SOURCE)
        self.assertEqual(ledger["x1"], X1)
        self.assertEqual(ledger["evidence"], EVIDENCE)
        self.assertEqual(ledger["x1_parent"], SOURCE)
        self.assertEqual(ledger["evidence_parent"], X1)
        self.assertEqual(ledger["new_proposals"], 60)
        self.assertEqual(ledger["zero_credit_inherited_reviews"], 20)
        self.assertEqual(ledger["declared_chain"], 10010)

    def test_23_identity_and_authority_boundary_is_explicit(self) -> None:
        overview = (FINAL / "integrated-overview.md").read_text(encoding="utf-8").casefold()
        baton = (BASE / "handoffs" / "sable-rook-v681-v6-activation-candidate.md").read_text(encoding="utf-8").casefold()
        for phrase in (
            "relational working language only",
            "not evidence of consciousness",
            "same-owner software and documentation evidence",
            "not independent reproduction",
            "maori authority",
            "theory-of-everything proof",
            "stage 20",
        ):
            self.assertIn(phrase, overview + "\n" + baton)


if __name__ == "__main__":
    unittest.main()

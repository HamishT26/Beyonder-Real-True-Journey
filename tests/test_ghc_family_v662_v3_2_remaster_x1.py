"""Lifecycle checks for the immutable Neris v662-v3-2 remaster x1 freeze."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = Path("docs/neris-solane/v662-v3-2-remaster")
PHASE = ROOT / PHASE_ROOT
SOURCE_FINAL = "9d35f2c60bc1d124bbc67d000e7f5a4da6d95410"
BRANCH = "codex/GHC-Family/neris-solane-v662-v3-2-remaster"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
X1_RECEIPTS = {
    (PHASE_ROOT / "validation/x1-content-manifest.json").as_posix(),
    (PHASE_ROOT / "validation/x1-privacy-scan.json").as_posix(),
    (PHASE_ROOT / "validation/x1-document-cap.json").as_posix(),
    (PHASE_ROOT / "validation/x1-staged-review.json").as_posix(),
    (PHASE_ROOT / "validation/x1-validation.json").as_posix(),
}


def read_json(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {completed.stderr[-1000:]}")
    return completed.stdout.strip()


def git_bytes(revision: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if completed.returncode:
        raise AssertionError(f"missing Git blob {revision}:{path}")
    return completed.stdout


class TestV662V3RemasterX1(unittest.TestCase):
    """Assert the x1 commit's scope, ancestry, manifests, and protected gates."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = read_json("preregistration/proposal-ledger.json")
        cls.frozen = read_json("provenance/frozen-chain-proposal-index.json")
        cls.novelty = read_json("preregistration/novelty-audit.json")
        cls.portfolios = read_json("preregistration/approval-portfolios.json")
        cls.tooling = read_json("preregistration/skill-and-runner-plan.json")
        cls.cfr = read_json("preregistration/clean-fix-refine-plan.json")
        cls.recovery = read_json("preregistration/ancestry-aware-suite-contract.json")
        cls.failures = read_json("truth/prior-canonical-failures.json")
        cls.methods = read_json("method-flow/method-flow-state-x1.json")
        cls.route = read_json("routing/terminal-route-plan.json")
        cls.manifest = read_json("validation/x1-content-manifest.json")
        cls.privacy = read_json("validation/x1-privacy-scan.json")
        cls.document_cap = read_json("validation/x1-document-cap.json")
        cls.staged = read_json("validation/x1-staged-review.json")
        cls.validation = read_json("validation/x1-validation.json")

    def test_01_exact_single_parent_ancestry(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD^"), SOURCE_FINAL)
        parents = git("rev-list", "--parents", "-n", "1", "HEAD").split()
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents[1], SOURCE_FINAL)
        self.assertEqual(git("rev-list", "--count", f"{SOURCE_FINAL}..HEAD"), "1")
        self.assertEqual(git("rev-list", "--merges", f"{SOURCE_FINAL}..HEAD"), "")

    def test_02_branch_and_phase_identity_are_exact(self) -> None:
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        self.assertEqual(self.ledger["owner"], "Neris Solane")
        self.assertEqual(self.ledger["phase"], "v662-v3-2-remaster")
        self.assertEqual(self.ledger["canonical_phase"], "v662-v3")

    def test_03_selected_inherited_rows_are_zero_credit(self) -> None:
        selected = self.ledger["program"][:20]
        self.assertEqual(len(selected), 20)
        self.assertEqual(self.ledger["selected_inherited_novelty_credit"], 0)
        self.assertEqual(self.ledger["selected_inherited_completion_credit"], 0)
        self.assertTrue(all(row["append_to_frozen_chain"] is False for row in selected))
        self.assertTrue(all(row["novelty_credit"] == 0 for row in selected))
        self.assertTrue(all(row["completion_credit"] == 0 for row in selected))

    def test_04_twenty_new_rows_use_only_four_expected_labels(self) -> None:
        new = self.ledger["program"][20:]
        self.assertEqual(len(new), 20)
        outcomes = Counter(row["expected_disposition"] for row in new)
        self.assertEqual(set(outcomes), ALLOWED_OUTCOMES)
        self.assertEqual(outcomes, Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}))
        self.assertTrue(all(row["append_to_frozen_chain"] is True for row in new))
        self.assertFalse(self.ledger["observed_outcomes_recorded"])

    def test_05_frozen_chain_and_novelty_audit_are_exact(self) -> None:
        self.assertEqual(self.frozen["prior_count"], 3510)
        self.assertEqual(self.frozen["selected_inherited_count"], 20)
        self.assertEqual(self.frozen["selection_rows_reappended"], 0)
        self.assertEqual(self.frozen["new_count"], 20)
        self.assertEqual(self.frozen["effective_count"], 3530)
        self.assertEqual(self.novelty["audited_inherited_rows"], 3510)
        self.assertEqual(self.novelty["new_rows"], 20)
        self.assertEqual(self.novelty["exact_collisions"], [])
        self.assertEqual(self.novelty["duplicate_new_titles"], [])
        self.assertTrue(self.novelty["valid"])

    def test_06_approval_portfolios_match_authorized_quantities(self) -> None:
        self.assertEqual(
            self.portfolios["counts"],
            {
                "owner_safe_now": 30,
                "successor_safe_now": 20,
                "owner_candidates": 15,
                "successor_candidates": 15,
                "owner_exact": 10,
                "owner_blocked": 5,
                "safe_total": 50,
                "candidate_total": 30,
            },
        )
        self.assertTrue(all(row["state"] == "exact_gate" and not row["executed"] for row in self.portfolios["owner_exact"]))
        self.assertTrue(all(row["state"] == "open_gap" and not row["executed"] for row in self.portfolios["owner_blocked"]))

    def test_07_skill_and_runner_plans_are_ten_plus_ten(self) -> None:
        self.assertEqual(
            self.tooling["counts"],
            {"owner_skills": 10, "successor_skills": 10, "owner_runners": 10, "successor_runners": 10},
        )
        self.assertTrue(all(row["state"] == "planned_x1" for row in self.tooling["owner_skill_builds"]))
        self.assertTrue(all(row["state"] == "planned_x1" for row in self.tooling["owner_runner_builds"]))
        self.assertTrue(all(row["state"] == "recommendation_only" for row in self.tooling["successor_skill_ideas"]))
        self.assertTrue(all(row["state"] == "recommendation_only" for row in self.tooling["successor_runner_ideas"]))

    def test_08_clean_fix_refine_plan_is_thirty_plus_thirty(self) -> None:
        self.assertEqual(self.cfr["counts"], {"owner": 30, "successor": 30, "total": 60})
        self.assertEqual(len(self.cfr["owner"]), 30)
        self.assertEqual(len(self.cfr["successor"]), 30)
        self.assertFalse(self.cfr["destructive_cleanup_authorized"])

    def test_09_complete_suite_recovery_contract_is_fail_closed(self) -> None:
        self.assertTrue(self.recovery["complete_repository_requirement"])
        self.assertEqual(self.recovery["selection"]["duplicate_policy"], "reject")
        self.assertEqual(self.recovery["selection"]["omission_policy"], "reject")
        self.assertTrue(self.recovery["definition_anchor"]["blob_equality_required"])
        self.assertEqual(self.recovery["definition_anchor"]["missing_or_ambiguous_anchor"], "fail_closed")
        self.assertFalse(self.recovery["execution"]["historical_test_editing"])
        self.assertTrue(self.recovery["completeness"]["every_current_test_id_mapped_once"])
        self.assertTrue(self.recovery["completeness"]["executed_test_count_equals_discovered_test_count"])
        self.assertTrue(self.recovery["completeness"]["all_current_remaster_lifecycle_tests_included"])
        self.assertEqual(self.recovery["canonical_policy"]["successful_invocation_required"], 1)
        self.assertFalse(self.recovery["canonical_policy"]["replay_after_success"])

    def test_10_prior_failures_remain_zero_credit(self) -> None:
        self.assertEqual(self.failures["failure_count"], 2)
        self.assertEqual(self.failures["success_count"], 0)
        self.assertEqual(len(self.failures["failures"]), 2)
        self.assertTrue(all(row["completion_credit"] == 0 for row in self.failures["failures"]))
        self.assertTrue(all(row["rewrote_repository"] is False for row in self.failures["failures"]))

    def test_11_method_flow_retains_five_failed_and_passing_witnesses(self) -> None:
        self.assertEqual(self.methods["method_count"], 5)
        self.assertEqual(self.methods["failed_witness_count"], 5)
        self.assertEqual(self.methods["passing_witness_count"], 5)
        self.assertEqual(self.methods["provisional_effective_negatives"], 22836)
        self.assertEqual(self.methods["provisional_effective_methods"], 7590)
        self.assertTrue(all(row["failed_credit"] == 0 for row in self.methods["methods"]))

    def test_12_x1_tree_contains_no_observed_x2_outputs(self) -> None:
        tracked = set(git("ls-tree", "-r", "--name-only", "HEAD", "--", PHASE_ROOT.as_posix()).splitlines())
        forbidden_prefixes = tuple((PHASE_ROOT / value).as_posix() + "/" for value in ("evidence", "surfaces", "final", "handoffs"))
        self.assertFalse([path for path in tracked if path.startswith(forbidden_prefixes)])
        self.assertTrue(self.ledger["x1_only"])

    def test_13_manifest_replays_exact_git_blobs(self) -> None:
        manifest_paths = {entry["path"] for entry in self.manifest["entries"]}
        tracked_owner = set(
            git(
                "ls-tree",
                "-r",
                "--name-only",
                "HEAD",
                "--",
                PHASE_ROOT.as_posix(),
                "scripts/ghc_family_v662_v3_2_remaster_data.py",
                "scripts/ghc_family_v662_v3_2_remaster_runtime.py",
                "scripts/build_ghc_family_v662_v3_2_remaster_x1.py",
                "tests/test_ghc_family_v662_v3_2_remaster_x1.py",
            ).splitlines()
        )
        self.assertEqual(manifest_paths, tracked_owner - X1_RECEIPTS)
        self.assertEqual(set(self.manifest["exclusions"]), X1_RECEIPTS)
        self.assertEqual(self.manifest["entry_count"], len(self.manifest["entries"]))
        for entry in self.manifest["entries"]:
            payload = git_bytes("HEAD", entry["path"])
            self.assertEqual(len(payload), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(payload).hexdigest(), entry["sha256"], entry["path"])

    def test_14_privacy_document_and_staged_receipts_are_valid(self) -> None:
        self.assertEqual(len(self.privacy["classes"]), 5)
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertFalse(self.privacy["privacy_complete"])
        self.assertTrue(self.document_cap["valid"])
        self.assertEqual(self.document_cap["over_cap"], [])
        self.assertEqual(self.staged["state"], "EXACT_STAGED_REVIEW")
        self.assertTrue(self.staged["valid"])
        self.assertEqual(self.staged["missing"], [])
        self.assertEqual(self.staged["unexpected"], [])

    def test_15_validation_and_terminal_route_remain_bounded(self) -> None:
        self.assertTrue(self.validation["valid"])
        self.assertEqual(self.validation["passed"], self.validation["total"])
        self.assertEqual(self.route["next"], {"owner": "Vesper Arlen", "phase": "v662-v4", "endpoint_kind": "main_task", "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"})
        self.assertTrue(self.route["one_edge_at_a_time"])
        self.assertFalse(self.route["message_attempted"])
        self.assertFalse(self.route["sent"])
        self.assertFalse(self.route["acknowledged"])
        self.assertFalse(self.route["substitute_endpoint"])

    def test_16_identity_and_evidence_boundaries_reject_overclaim(self) -> None:
        text = " ".join(
            [
                self.ledger["boundary"],
                self.portfolios["boundary"],
                self.tooling["boundary"],
                self.recovery["claim_boundary"],
            ]
        ).lower()
        for token in (
            "not empirical confirmation",
            "not complete privacy assurance",
            "independent reproduction",
            "consciousness or personhood",
            "theory-of-everything",
            "stage 20 authority",
        ):
            if token == "not complete privacy assurance":
                self.assertIn(token, self.privacy["boundary"].lower())
            else:
                self.assertIn(token, text)
        overview = (PHASE / "overview/x1-frozen-overview.md").read_text(encoding="utf-8").lower()
        self.assertIn("relational working language only", overview)
        self.assertIn("māori authority", overview)


if __name__ == "__main__":
    unittest.main()

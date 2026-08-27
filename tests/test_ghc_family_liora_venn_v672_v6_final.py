"""Closeout and pre-canonical exact-final tests for Liora Venn v672-v6."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_liora_venn_v672_v6_final as final


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "liora-venn" / "v672-v6"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_bytes(*args: str) -> bytes:
    return git(*args).stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8", errors="strict").strip()


def index_or_head(path: str) -> bytes:
    staged = git("show", f":{path}", check=False)
    return staged.stdout if staged.returncode == 0 else git_bytes("show", f"HEAD:{path}")


class LioraVennV672V6FinalTests(unittest.TestCase):
    def test_01_exact_owner_phase_branch_and_identity_boundary(self) -> None:
        self.assertEqual(final.OWNER, "Liora Venn")
        self.assertEqual(final.PHASE, "v672-v6")
        self.assertEqual(final.BRANCH, "codex/GHC-Family/liora-venn-v672-v6-full-tools")
        self.assertIn("relational working language", final.x1.IDENTITY_BOUNDARY)

    def test_02_lifecycle_constants_and_direct_parent_chain(self) -> None:
        self.assertEqual(final.SOURCE_FINAL, "e3b49b5ad7d81e09a0d4ba6b306c09623673e5f1")
        self.assertEqual(final.X1_COMMIT, "bbe8eea23928ada9526df78cee758c7d6a20b33f")
        self.assertEqual(final.EVIDENCE_COMMIT, "4ead23fe0b39033d9cb7caa1595a9b4c03741630")
        self.assertEqual(git_text("rev-parse", f"{final.X1_COMMIT}^"), final.SOURCE_FINAL)
        self.assertEqual(git_text("rev-parse", f"{final.EVIDENCE_COMMIT}^"), final.X1_COMMIT)

    def test_03_final_is_or_will_be_direct_child_of_evidence(self) -> None:
        head = git_text("rev-parse", "HEAD")
        if head == final.EVIDENCE_COMMIT:
            self.assertTrue(git_text("diff", "--cached", "--name-only", final.EVIDENCE_COMMIT))
        else:
            self.assertEqual(git_text("rev-parse", "HEAD^"), final.EVIDENCE_COMMIT)
            self.assertEqual(git_text("rev-list", "--count", f"{final.SOURCE_FINAL}..HEAD"), "3")
            self.assertEqual(git_text("rev-list", "--merges", f"{final.SOURCE_FINAL}..HEAD"), "")

    def test_04_phase_truth_has_exact_outcomes(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(set(truth["outcomes"]), set(final.x1.ALLOWED_OUTCOMES))
        self.assertEqual(sum(truth["outcomes"].values()), 40)

    def test_05_phase_truth_has_exact_effective_counts(self) -> None:
        counts = load("closeout/phase-truth.json")["effective_counts"]
        self.assertEqual(
            counts,
            {
                "declared_frozen_proposals": 6150,
                "effective_negatives": 35779,
                "effective_methods": 22041,
                "failed_witnesses": 7440,
                "bounded_passing_witnesses": 9604,
                "open_gaps": 287,
                "exact_gates": 280,
            },
        )

    def test_06_terminal_truth_remains_bounded(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["canonical_state_at_commit"], "NOT_RUN_PENDING_EXACT_FINAL_GATE")
        self.assertEqual(truth["terminal_route_state"], "PREPARED_NOT_SENT")
        self.assertEqual(truth["full_repository_suite"], "not_run_not_claimed")
        self.assertTrue(truth["same_owner_only"])
        self.assertFalse(truth["independent_reproduction"])

    def test_07_retained_negative_arithmetic_is_additive(self) -> None:
        row = load("closeout/retained-negative-register.json")
        self.assertEqual(35602 + 11 + 160 + 1 + 5, row["effective_negatives"])
        self.assertEqual(row["liora_additive_failures"], 177)
        self.assertEqual(row["effective_negatives"], 35779)
        self.assertEqual(row["effective_failed_witnesses"], 7440)
        self.assertEqual(row["failed_witnesses_promoted"], 0)

    def test_08_method_flow_retains_closeout_failures_and_recoveries(self) -> None:
        flow = load("closeout/method-flow-final.json")
        self.assertEqual(len(flow["closeout_failures"]), 5)
        self.assertEqual(len(flow["closeout_methods"]), 5)
        self.assertEqual(len(flow["closeout_recoveries"]), 5)
        self.assertEqual({row["negative_id"] for row in flow["closeout_failures"]}, {f"LV6726-CLOSE-N{i:03d}" for i in range(1, 6)})
        self.assertTrue(all(row["retained_negative_ids"] for row in flow["closeout_methods"]))
        self.assertTrue(flow["failed_witness_non_erasure"])

    def test_09_absent_helper_failures_are_not_rewritten_as_helpers(self) -> None:
        flow = load("closeout/method-flow-final.json")
        names = {row["helper"] for row in flow["closeout_failures"]}
        self.assertEqual(
            names,
            {
                "ghc_family_canonical_aggregate_preflight.py",
                "ghc_family_manifest_privacy_tribunal.py",
                "ghc_family_v662_v3_2_remaster_canonical.py",
                "ghc_family_complete_suite_orchestrator.py",
                "first_staged_seal_process",
            },
        )
        self.assertTrue(all(row["same_owner_only"] for row in flow["closeout_recoveries"]))
        self.assertTrue(all(not row["independent_reproduction"] for row in flow["closeout_recoveries"]))

    def test_10_gate_register_preserves_all_gaps_and_gates(self) -> None:
        gates = load("closeout/gate-register.json")
        self.assertEqual(gates["source_open_gaps"] + len(gates["phase_open_gaps"]), 287)
        self.assertEqual(gates["source_exact_gates"] + len(gates["phase_exact_gates"]), 280)
        self.assertEqual(gates["phase_open_gaps"], ["LV6726-N037", "LV6726-N038"])
        self.assertEqual(gates["phase_exact_gates"], ["LV6726-N039", "LV6726-N040"])
        self.assertTrue(gates["all_inherited_and_phase_gates_retained"])

    def test_11_proposal_outcome_ledger_uses_only_four_labels(self) -> None:
        ledger = load("x2/proposal-outcome-ledger.json")
        outcomes = ledger["outcomes"]
        self.assertEqual(len(outcomes), 40)
        self.assertEqual(Counter(row["outcome"] for row in outcomes), Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}))
        self.assertEqual(ledger["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_12_all_preregistered_mutations_remain_rejected(self) -> None:
        register = load("x2/mutation-register.json")
        self.assertEqual(register["mutation_count"], 160)
        self.assertEqual(register["rejected_count"], 160)
        self.assertEqual(register["failed_witness_count"], 160)
        self.assertTrue(register["failed_witnesses_retained"])
        self.assertEqual(register["failed_witnesses_promoted"], 0)
        self.assertEqual(register["passing_rejection_witness_count"], 160)

    def test_13_portfolio_floors_and_unexecuted_boundaries_are_exact(self) -> None:
        portfolio = load("x2/portfolio-outcome.json")
        self.assertEqual(len(portfolio["safe_now"]), 60)
        self.assertEqual(len(portfolio["bounded_candidates"]), 30)
        self.assertEqual(len(portfolio["clean_fix_refine"]), 60)
        self.assertEqual(len(portfolio["exact_approval"]), 20)
        self.assertEqual(len(portfolio["blocked"]), 10)
        self.assertTrue(portfolio["caps_are_ceilings_not_quotas"])

    def test_14_owner_local_skills_were_initialized_validated_and_smoked(self) -> None:
        quick = load("x2/skill-quick-validation-receipt.json")
        smoke = load("x2/skill-smoke-receipt.json")
        self.assertTrue(quick["initialized_through_official_skill_creator"])
        self.assertEqual(quick["customized_count"], 20)
        self.assertEqual(quick["quick_validated_count"], 20)
        self.assertEqual(quick["global_install_count"], 0)
        self.assertEqual(smoke["skill_count"], 20)
        self.assertEqual(smoke["accepting_passes"], 20)
        self.assertEqual(smoke["rejecting_passes"], 20)

    def test_15_family_current_runners_have_accepting_and_rejecting_smoke(self) -> None:
        smoke = load("x2/runner-smoke-receipt.json")
        self.assertEqual(smoke["runner_count"], 10)
        self.assertEqual(smoke["case_count"], 20)
        self.assertTrue(all(len(row["cases"]) == 2 for row in smoke["runners"]))
        self.assertTrue(all(case["expected_behavior_observed"] for row in smoke["runners"] for case in row["cases"]))
        self.assertTrue(all(row["historical_caller_compatibility"] == "family_current_ghc_family_prefix_preserved" for row in smoke["runners"]))

    def test_16_lifecycle_receipt_preserves_proper_context_results(self) -> None:
        receipt = load("closeout/lifecycle-test-receipt.json")
        self.assertEqual(receipt["x1"]["tests"], 21)
        self.assertEqual(receipt["evidence"]["tests"], 22)
        self.assertEqual(receipt["x1"]["credited_runs"], 1)
        self.assertEqual(receipt["evidence"]["credited_runs"], 1)
        self.assertEqual(receipt["full_repository_suite"], "not_run_not_claimed")
        self.assertFalse(receipt["independent_reproduction"])

    def test_17_lifecycle_replay_preserves_strict_x1_before_x2(self) -> None:
        replay = load("closeout/lifecycle-replay.json")
        self.assertEqual(replay["verified_direct_parents"]["x1_parent"], final.SOURCE_FINAL)
        self.assertEqual(replay["verified_direct_parents"]["evidence_parent"], final.X1_COMMIT)
        self.assertEqual(replay["current_phase_commits"], 2)
        self.assertEqual(replay["current_merges"], 0)
        self.assertTrue(replay["strict_x1_before_x2"])
        self.assertTrue(replay["x1_pushed_clean_four_way_equal_before_x2"])
        self.assertTrue(replay["evidence_pushed_clean_four_way_equal_before_closeout"])

    def test_18_route_is_prepared_not_sent_and_inert(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["prospective_successor_exact_title"], "Tamar Vey")
        self.assertEqual(route["prospective_successor_phase"], "v672-v7")
        self.assertFalse(route["successor_contacted"])
        self.assertFalse(route["task_created_or_forked"])
        self.assertFalse(route["standby_contacted"])
        self.assertEqual(route["send_count"], 0)

    def test_19_handoff_candidate_is_sanitized_and_not_a_delivery_claim(self) -> None:
        text = (OWNER_ROOT / "handoffs" / "tamar-vey-v672-v7-activation-candidate.md").read_text(encoding="utf-8")
        self.assertIn("PREPARED_NOT_SENT", text)
        self.assertIn("neither discovers nor contacts a successor", text)
        self.assertIn("exact Liora final and external canonical receipt do not yet exist", text)
        self.assertNotIn("SENT_BY_LIORA_VENN = true", text)
        self.assertNotIn("<codex_delegation", text)

    def test_20_canonical_state_is_truthfully_pending_and_one_shot(self) -> None:
        state = load("final/canonical-invocation-state.json")
        self.assertEqual(state["state_at_commit"], "NOT_RUN_PENDING_EXACT_FINAL_GATE")
        self.assertEqual(state["attempts_at_commit"], 0)
        self.assertEqual(state["successes_at_commit"], 0)
        self.assertEqual(state["invocation_limit"], 1)
        self.assertFalse(state["replay_after_success"])
        self.assertEqual(state["full_repository_suite"], "not_run_not_claimed")

    def test_21_prereceipt_does_not_invent_final_or_canonical_success(self) -> None:
        receipt = load("validation/final-validation-prereceipt.json")
        self.assertEqual(receipt["final"], "PENDING_FINAL_COMMIT")
        self.assertFalse(receipt["canonical_invoked"])
        self.assertEqual(receipt["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_22_content_seal_replays_exact_index_or_head_bytes(self) -> None:
        seal = load("seal/content-seal-candidate.json")
        self.assertEqual(seal["target_count"], 10)
        self.assertEqual(seal["target_count"], len(seal["targets"]))
        self.assertFalse(seal["canonical_invoked"])
        self.assertFalse(seal["successor_contacted"])
        for row in seal["targets"]:
            data = index_or_head(row["path"])
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_23_x1_manifest_replays_at_immutable_x1(self) -> None:
        manifest_path = "docs/liora-venn/v672-v6/validation/x1-manifest.json"
        manifest = json.loads(git_bytes("show", f"{final.X1_COMMIT}:{manifest_path}").decode("utf-8"))
        self.assertEqual(manifest["entry_count"], 19)
        self.assertEqual(len(manifest["self_exclusions"]), 2)
        for row in manifest["entries"]:
            data = git_bytes("show", f"{final.X1_COMMIT}:{row['path']}")
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()), (row["bytes"], row["sha256"]))

    def test_24_evidence_manifest_replays_at_immutable_evidence(self) -> None:
        manifest_path = "docs/liora-venn/v672-v6/validation/evidence-manifest.json"
        manifest = json.loads(git_bytes("show", f"{final.EVIDENCE_COMMIT}:{manifest_path}").decode("utf-8"))
        self.assertEqual(manifest["entry_count"], 146)
        self.assertEqual(len(manifest["self_exclusions"]), 2)
        for row in manifest["entries"]:
            data = git_bytes("show", f"{final.EVIDENCE_COMMIT}:{row['path']}")
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()), (row["bytes"], row["sha256"]))

    def test_25_final_manifests_replay_exact_index_or_head_blobs(self) -> None:
        for relative in ("validation/final-delta-manifest.json", "validation/final-owner-manifest.json"):
            manifest = load(relative)
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            self.assertEqual(len(manifest["self_exclusions"]), 4)
            for row in manifest["entries"]:
                data = index_or_head(row["path"])
                self.assertEqual(len(data), row["bytes"], row["path"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_26_final_manifest_coverage_matches_delta_and_owner_surface(self) -> None:
        for relative, base in (("validation/final-delta-manifest.json", final.EVIDENCE_COMMIT), ("validation/final-owner-manifest.json", final.SOURCE_FINAL)):
            manifest = load(relative)
            expected = set(git_text("diff", "--cached", "--name-only", base).splitlines())
            if not expected:
                expected = set(git_text("diff", "--name-only", base, "HEAD").splitlines())
            declared = {row["path"] for row in manifest["entries"]} | (set(manifest["self_exclusions"]) & expected)
            self.assertEqual(declared, expected)

    def test_27_staged_review_and_privacy_tribunal_are_valid(self) -> None:
        review = load("validation/final-staged-review.json")
        privacy = load("validation/final-staged-privacy.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["deletions"], [])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["frozen_x1_or_x2_changes"], [])
        self.assertEqual(review["privacy_confirmed_hits"], 0)
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["class_count"], 5)
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(privacy["scanner_definitions_separated"])

    def test_28_x1_and_x2_surfaces_are_immutable_after_evidence(self) -> None:
        changed = git_text(
            "diff", "--cached", "--name-only", final.EVIDENCE_COMMIT, "--",
            "docs/liora-venn/v672-v6/x1", "docs/liora-venn/v672-v6/x2",
            "scripts/build_ghc_family_liora_venn_v672_v6_x1.py",
            "scripts/build_ghc_family_liora_venn_v672_v6_x2.py",
            "tests/test_ghc_family_liora_venn_v672_v6_x1.py",
            "tests/test_ghc_family_liora_venn_v672_v6_x2.py",
        )
        self.assertEqual(changed, "")

    def test_29_all_owner_json_parses_and_documents_fit_caps(self) -> None:
        for path in OWNER_ROOT.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))
        for path in OWNER_ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml", ".yml"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)

    def test_30_accessible_report_file_and_commit_caps_remain_bounded(self) -> None:
        html = (OWNER_ROOT / "closeout" / "accessible-final-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', 'href="#main"', '<main id="main">', 'aria-labelledby="scope"', "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, html)
        files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts]
        self.assertLess(len(files), 2000)
        head = git_text("rev-parse", "HEAD")
        current = int(git_text("rev-list", "--count", f"{final.SOURCE_FINAL}..{head}"))
        self.assertLessEqual(current + (1 if head == final.EVIDENCE_COMMIT else 0), 8)


if __name__ == "__main__":
    unittest.main()

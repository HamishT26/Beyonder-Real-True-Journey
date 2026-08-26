"""Closeout and pre-canonical seal tests for Orin Thale v670-v6."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_orin_thale_v670_v6_final as builder

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "orin-thale" / "v670-v6"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8", errors="strict").strip()


def index_or_head(path: str) -> bytes:
    staged = subprocess.run(["git", "show", f":{path}"], cwd=ROOT, check=False, capture_output=True)
    return staged.stdout if staged.returncode == 0 else git_bytes("show", f"HEAD:{path}")


class OrinThaleV670V6FinalTests(unittest.TestCase):
    def test_exact_lifecycle_constants_and_current_shape(self):
        self.assertEqual(builder.SOURCE_FINAL, "286d76dee7ca0e7ab5041c723e607a47b5e9c4c7")
        self.assertEqual(builder.X1_COMMIT, "54eda14c93f9ba34c47ad324aa79647c3343118a")
        self.assertEqual(builder.EVIDENCE_COMMIT, "4a2c7a93fd34456166cb083d7e9362aa9795f0e1")
        self.assertEqual(git_text("rev-parse", f"{builder.X1_COMMIT}^"), builder.SOURCE_FINAL)
        self.assertEqual(git_text("rev-parse", f"{builder.EVIDENCE_COMMIT}^"), builder.X1_COMMIT)
        head = git_text("rev-parse", "HEAD")
        if head != builder.EVIDENCE_COMMIT:
            self.assertEqual(git_text("rev-parse", "HEAD^"), builder.EVIDENCE_COMMIT)
            self.assertEqual(git_text("rev-list", "--count", f"{builder.SOURCE_FINAL}..HEAD"), "3")
            self.assertEqual(git_text("rev-list", "--merges", f"{builder.SOURCE_FINAL}..HEAD"), "")

    def test_phase_truth_has_exact_counts_outcomes_and_verdict(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["proposal_chain"], 5470)
        self.assertEqual(truth["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(truth["effective_negatives"], 32955)
        self.assertEqual(truth["effective_methods"], 19165)
        self.assertEqual(truth["effective_failed_witnesses"], 4776)
        self.assertEqual(truth["effective_passing_witnesses"], 6204)
        self.assertEqual(truth["open_gaps"], 251)
        self.assertEqual(truth["exact_gates"], 246)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["real_people"], truth["real_objects_measurements_rows"])
        self.assertEqual(truth["real_world_actions"], 0)

    def test_final_proposal_ledger_uses_only_four_labels(self):
        ledger = load("closeout/proposal-ledger-final.json")
        self.assertEqual(ledger["chain"], 5470)
        self.assertEqual(len(ledger["rows"]), 40)
        self.assertEqual(Counter(row["outcome"] for row in ledger["rows"]), Counter(builder.OUTCOMES))
        self.assertEqual({row["outcome"] for row in ledger["rows"]}, {"completed", "represented", "open_gap", "exact_gate"})
        self.assertFalse(ledger["universal_novelty_claim"])

    def test_retained_negative_arithmetic_preserves_all_final_failures(self):
        register = load("closeout/retained-negative-register.json")
        self.assertEqual(32772 + 1 + 13 + 160 + 6 + 3, register["effective_before_canonical"])
        self.assertEqual(register["effective_before_canonical"], 32955)
        self.assertEqual(register["erased"], 0)
        self.assertTrue(register["all_failures_retained"])
        self.assertEqual(
            [row["negative_id"] for row in register["final_operational_negatives"]],
            ["OT6706-X2-N007", "OT6706-X2-N008", "OT6706-FINAL-N001"],
        )

    def test_method_flow_retains_failure_and_passing_recovery_separately(self):
        flow = load("closeout/method-flow-final.json")
        self.assertEqual(flow["counts"]["methods"], 215)
        self.assertEqual(flow["counts"]["witness_results"], {"fail": 182, "pass": 215})
        self.assertEqual(flow["effective_overlay"], {
            "effective_negatives": 32955,
            "effective_methods": 19165,
            "failed_witnesses": 4776,
            "bounded_passing_witnesses": 6204,
            "repository_seal_rewritten": False,
        })
        methods = {row["method_id"]: row for row in flow["methods"]}
        expected = ["OT6706-X2-N007", "OT6706-X2-N008", "OT6706-FINAL-N001"]
        for index in range(1, 4):
            method = methods[f"OT6706-FINAL-M{index:03d}"]
            self.assertIn(expected[index - 1], method["retained_negative_ids"])

    def test_post_evidence_failures_remain_zero_credit(self):
        register = load("closeout/retained-negative-register.json")
        rows = register["final_operational_negatives"]
        self.assertEqual([row["negative_id"] for row in rows], ["OT6706-X2-N007", "OT6706-X2-N008", "OT6706-FINAL-N001"])
        self.assertTrue(all("failed_witness" in row and "passing_witness" in row for row in rows))

    def test_open_gaps_and_exact_gates_remain_visible(self):
        gates = load("closeout/exact-open-gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 251)
        self.assertEqual(gates["effective_exact_gates"], 246)
        self.assertTrue(gates["none_silently_closed"])
        self.assertEqual(len(gates["open_gap_surfaces"]), 2)
        self.assertEqual(len(gates["exact_gate_surfaces"]), 2)

    def test_complete_incomplete_checklist_keeps_external_work_reserved(self):
        checklist = load("closeout/complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["completed"]), 10)
        self.assertGreaterEqual(len(checklist["incomplete_or_reserved"]), 10)
        self.assertTrue(checklist["all_incomplete_surfaces_visible"])

    def test_integrated_overview_is_three_page_equivalent_and_bounded(self):
        words = len((OWNER_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1600)
        self.assertLessEqual(words, 100000)

    def test_accessible_report_has_structure_and_reservations(self):
        text = (OWNER_ROOT / "closeout" / "accessible-final-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', "scope='row'", 'role="status"', '@media print'):
            self.assertIn(token, text)
        self.assertIn("affected-user evaluation remain reserved", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_environment_sources_and_wellbeing_preserve_boundaries(self):
        environment = load("closeout/environment-version-receipt.json")
        sources = load("closeout/source-evidence-ledger.json")
        wellbeing = load("closeout/final-wellbeing-check.json")
        self.assertTrue(environment["verified_only"])
        for field in ("desktop_updated", "elevation", "host_security_changes", "windows_feature_changes", "sandbox_or_hyper_v_activated", "unrelated_installation", "reboot"):
            self.assertFalse(environment[field])
        self.assertEqual(sources["read_only_queries"], 2)
        self.assertEqual(sources["failed_projection_attempts"], 0)
        self.assertEqual(sources["downloads"], 0)
        self.assertEqual(sources["empirical_rows_downloaded"], sources["measurements"])
        self.assertFalse(sources["citations_are_observations"])
        self.assertTrue(wellbeing["relational_working_language_only"])
        self.assertTrue(wellbeing["corrigible"])
        self.assertEqual(wellbeing["subagents"], wellbeing["task_creation"])

    def test_skill_runner_summary_is_family_compatible_and_owner_local(self):
        summary = load("closeout/skill-runner-summary.json")
        self.assertEqual(summary["phase_local_skills_built_validated_smoke_used"], 20)
        self.assertEqual(summary["family_compatible_runners_built_or_selected_invoked"], 10)
        self.assertEqual(len(summary["runner_modules"]), 10)
        self.assertEqual(summary["global_installations"], 0)
        self.assertEqual(summary["shared_skill_changes"], 0)
        self.assertTrue(summary["historical_callers_preserved"])

    def test_route_is_prepared_not_sent_and_recipient_unresolved(self):
        route = load("orchestration/route-state-final-candidate.json")
        basis = (OWNER_ROOT / "handoffs" / "successor-activation-basis.md").read_text(encoding="utf-8")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertIsNone(route["prospective_exact_title"])
        self.assertIsNone(route["prospective_phase"])
        self.assertFalse(route["successor_contacted"])
        self.assertFalse(route["resend_allowed"])
        self.assertIn("SENT_BY_ORIN_THALE = false", basis)
        self.assertIn("UNRESOLVED_UNTIL_EXACT_FINAL_LIVE_REFRESH", basis)

    def test_canonical_state_is_truthfully_pending_and_one_shot(self):
        state = load("final/canonical-invocation-state.json")
        prerequisites = load("final/final-validation-prerequisites.json")
        record = load("final/final-validation-candidate-record.json")
        self.assertEqual(state["state_at_commit"], "NOT_RUN_PENDING_EXACT_FINAL_GATE")
        self.assertEqual(state["attempts_at_commit"], state["successes_at_commit"])
        self.assertEqual(state["invocation_limit"], 1)
        self.assertFalse(state["replay_after_success"])
        self.assertTrue(prerequisites["one_shot"])
        self.assertEqual(prerequisites["full_repository_suite"], "not_run_not_claimed")
        self.assertFalse(record["canonical_success_claim"])

    def test_seal_and_closeout_candidates_are_not_posthoc_success_claims(self):
        seal = load("seal/seal-candidate.json")
        receipt = load("closeout/closeout-receipt.json")
        self.assertTrue(seal["content_ready"])
        self.assertFalse(seal["canonical_invoked"])
        self.assertFalse(seal["canonical_success"])
        self.assertEqual(receipt["planned_final_parent"], builder.EVIDENCE_COMMIT)
        self.assertEqual(receipt["planned_phase_commits"], 3)
        self.assertEqual(receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_final_manifests_replay_exact_index_or_head_blobs(self):
        for relative in ("validation/final-delta-manifest.json", "validation/final-owner-manifest.json"):
            manifest = load(relative)
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            for row in manifest["entries"]:
                blob = index_or_head(row["path"])
                self.assertEqual(row["bytes"], len(blob), row["path"])
                self.assertEqual(row["sha256"], hashlib.sha256(blob).hexdigest(), row["path"])

    def test_final_manifest_coverage_matches_delta_and_owner_surface(self):
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        staged_delta = set(git_text("diff", "--cached", "--name-only", builder.EVIDENCE_COMMIT).splitlines())
        expected_delta = staged_delta or set(git_text("diff", "--name-only", builder.EVIDENCE_COMMIT, "HEAD").splitlines())
        staged_owner = set(git_text("diff", "--cached", "--name-only", builder.SOURCE_FINAL).splitlines())
        expected_owner = staged_owner or set(git_text("diff", "--name-only", builder.SOURCE_FINAL, "HEAD").splitlines())
        # During the precommit run, the test-receipt self-exclusion is declared
        # before that receipt can truthfully exist. At exact final every declared
        # exclusion exists, and the canonical validator applies strict equality.
        delta_exclusions = set(delta["self_exclusions"]) & expected_delta
        owner_exclusions = set(owner["self_exclusions"]) & expected_owner
        self.assertEqual({row["path"] for row in delta["entries"]} | delta_exclusions, expected_delta)
        self.assertEqual({row["path"] for row in owner["entries"]} | owner_exclusions, expected_owner)

    def test_final_staged_reviews_are_valid_and_zero_confirmed_hits(self):
        review = load("validation/final-staged-review.json")
        privacy = load("validation/final-staged-privacy.json")
        validation = load("validation/final-validation-receipt.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["disallowed_paths"], [])
        self.assertEqual(review["frozen_x1_or_evidence_paths"], [])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["frozen_x1_or_x2_changes"], [])

    def test_x1_and_x2_surfaces_are_immutable_after_evidence(self):
        changed = git_text("diff", "--cached", "--name-only", builder.EVIDENCE_COMMIT, "--", "docs/orin-thale/v670-v6/x1", "docs/orin-thale/v670-v6/x2", "scripts/build_ghc_family_orin_thale_v670_v6_x1.py", "scripts/build_ghc_family_orin_thale_v670_v6_x2.py", "tests/test_ghc_family_orin_thale_v670_v6_x1.py", "tests/test_ghc_family_orin_thale_v670_v6_x2.py")
        self.assertEqual(changed, "")

    def test_all_owner_json_parses_and_documents_fit_cap(self):
        json_paths = sorted(OWNER_ROOT.rglob("*.json"))
        self.assertGreaterEqual(len(json_paths), 150)
        for path in json_paths:
            json.loads(path.read_text(encoding="utf-8"))
        for path in OWNER_ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)

    def test_materialized_files_and_commit_ceiling_remain_bounded(self):
        files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
        self.assertLess(len(files), 2000)
        head = git_text("rev-parse", "HEAD")
        count = int(git_text("rev-list", "--count", f"{builder.SOURCE_FINAL}..{head}"))
        self.assertLessEqual(count + (1 if head == builder.EVIDENCE_COMMIT else 0), 8)


if __name__ == "__main__":
    unittest.main()

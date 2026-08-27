"""Closeout and pre-canonical final tests for Orin Thale v672-v5."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_orin_thale_v672_v5_final as builder


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "orin-thale" / "v672-v5"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8", errors="strict").strip()


def index_or_head(path: str) -> bytes:
    staged = subprocess.run(["git", "show", f":{path}"], cwd=ROOT, check=False, capture_output=True)
    return staged.stdout if staged.returncode == 0 else git_bytes("show", f"HEAD:{path}")


class OrinThaleV672V5FinalTests(unittest.TestCase):
    def test_01_lifecycle_constants_and_direct_parent_chain(self):
        self.assertEqual(builder.SOURCE_FINAL, "8f672ef30372b4adf457140c254931dc365e9d31")
        self.assertEqual(builder.X1_COMMIT, "657681df7392f3cd652930d3f834b60ccfa21bcd")
        self.assertEqual(builder.EVIDENCE_COMMIT, "1c6fb43638e79a6bb963839765c519839da12f67")
        self.assertEqual(git_text("rev-parse", f"{builder.X1_COMMIT}^"), builder.SOURCE_FINAL)
        self.assertEqual(git_text("rev-parse", f"{builder.EVIDENCE_COMMIT}^"), builder.X1_COMMIT)
        head = git_text("rev-parse", "HEAD")
        if head != builder.EVIDENCE_COMMIT:
            self.assertEqual(git_text("rev-parse", "HEAD^"), builder.EVIDENCE_COMMIT)
            self.assertEqual(git_text("rev-list", "--count", f"{builder.SOURCE_FINAL}..HEAD"), "3")
            self.assertEqual(git_text("rev-list", "--merges", f"{builder.SOURCE_FINAL}..HEAD"), "")

    def test_02_phase_truth_has_corrected_cumulative_counts(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["proposal_chain"], 6110)
        self.assertEqual(truth["outcomes"], builder.OUTCOMES)
        self.assertEqual(truth["effective_negatives"], 35602)
        self.assertEqual(truth["effective_methods"], 22007)
        self.assertEqual(truth["failed_witnesses"], 7263)
        self.assertEqual(truth["bounded_passing_witnesses"], 9314)
        self.assertEqual(truth["open_gaps"], 285)
        self.assertEqual(truth["exact_gates"], 278)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_03_counter_correction_is_explicit_and_additive(self):
        row = load("closeout/counter-correction-overlay.json")
        components = row["components"]
        corrected = row["corrected"]
        self.assertEqual(components["activation_negatives"] + components["owner_operational_failures"] + components["rejected_mutations"], corrected["effective_negatives"])
        self.assertEqual(components["inherited_open_gaps"] + components["new_open_gaps"], corrected["open_gaps"])
        self.assertEqual(components["inherited_exact_gates"] + components["new_exact_gates"], corrected["exact_gates"])
        self.assertFalse(row["evidence_commit_rewritten"])
        self.assertEqual(row["retained_negative_id"], "OT6725-FINAL-N001")

    def test_04_method_flow_retains_all_failures_and_recoveries(self):
        flow = load("closeout/method-flow-final.json")
        self.assertEqual(flow["counts"]["methods"], 20)
        self.assertEqual(flow["counts"]["witness_results"], {"fail": 25, "pass": 26})
        self.assertEqual(flow["counts"]["witnesses"], 51)
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in flow["methods"]))
        self.assertTrue(all(row["retained_negative_ids"] for row in flow["methods"]))

    def test_05_outcomes_and_gate_register_use_only_authorized_labels(self):
        rows = load("x2/outcome-ledger.json")["rows"]
        self.assertEqual(Counter(row["outcome"] for row in rows), Counter(builder.OUTCOMES))
        gates = load("closeout/gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 285)
        self.assertEqual(gates["effective_exact_gates"], 278)
        self.assertEqual(len(gates["open_gap_proposals"]), 2)
        self.assertEqual(len(gates["exact_gate_proposals"]), 2)
        self.assertTrue(gates["none_silently_closed"])

    def test_06_retained_negative_register_preserves_exact_arithmetic(self):
        row = load("closeout/retained-negative-register.json")
        self.assertEqual(row["activation_baseline"] + row["owner_operational_failures"] + row["rejected_mutations"], row["effective_negatives"])
        self.assertEqual(row["effective_negatives"], 35602)
        self.assertEqual(len(row["new_failure_ids"]), 25)
        self.assertEqual(row["erased"], 0)
        self.assertEqual(row["converted_to_pass"], 0)
        self.assertTrue(row["all_failures_retained"])

    def test_07_integrated_overview_is_three_page_equivalent_and_bounded(self):
        words = len((OWNER_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1800)
        self.assertLessEqual(words, 100000)

    def test_08_accessible_report_has_structure_and_reservations(self):
        text = (OWNER_ROOT / "closeout" / "accessible-final-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', "scope='row'", 'role="status"', "@media print"):
            self.assertIn(token, text)
        self.assertIn("affected-user evaluation remain reserved", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_09_complete_incomplete_checklist_keeps_external_work_reserved(self):
        row = load("closeout/complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(row["completed"]), 10)
        self.assertGreaterEqual(len(row["incomplete_or_reserved"]), 10)
        self.assertTrue(row["all_incomplete_surfaces_visible"])

    def test_10_environment_sources_wellbeing_and_tools_preserve_boundaries(self):
        env = load("closeout/environment-source-wellbeing.json")
        summary = load("closeout/skill-runner-summary.json")
        self.assertTrue(env["versions_verified_only"])
        for field in ("desktop_updated", "elevation", "host_security_changes", "windows_feature_changes", "sandbox_or_hyper_v_activated", "unrelated_installation", "reboot"):
            self.assertFalse(env[field])
        self.assertEqual(env["source_real_rows"], 0)
        self.assertFalse(env["citations_are_observations"])
        self.assertEqual(env["subagents"], 0)
        self.assertEqual(env["tasks_created_or_forked"], 0)
        self.assertEqual(summary["phase_local_skills_built_validated_smoke_used"], 20)
        self.assertEqual(summary["family_current_runners_built_invoked"], 10)
        self.assertEqual(summary["global_installations"], 0)

    def test_11_route_is_prepared_not_sent_for_fresh_terminal_resolution(self):
        route = load("orchestration/terminal-route-state.json")
        basis = (OWNER_ROOT / "handoffs" / "liora-venn-v672-v6-activation-candidate.md").read_text(encoding="utf-8")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["prospective_exact_title"], "Liora Venn")
        self.assertEqual(route["prospective_phase"], "v672-v6")
        self.assertFalse(route["successor_contacted"])
        self.assertFalse(route["resend_allowed"])
        self.assertIn("SENT_BY_ORIN_THALE = false", basis)

    def test_12_canonical_state_is_truthfully_pending_and_one_shot(self):
        state = load("final/canonical-invocation-state.json")
        prerequisites = load("final/final-validation-prerequisites.json")
        self.assertEqual(state["state_at_commit"], "NOT_RUN_PENDING_EXACT_FINAL_GATE")
        self.assertEqual(state["attempts_at_commit"], 0)
        self.assertEqual(state["successes_at_commit"], 0)
        self.assertEqual(state["invocation_limit"], 1)
        self.assertFalse(state["replay_after_success"])
        self.assertTrue(prerequisites["one_shot"])
        self.assertEqual(prerequisites["full_repository_suite"], "not_run_not_claimed")

    def test_13_seal_candidate_replays_exact_index_or_head_bytes(self):
        seal = load("seal/content-seal-candidate.json")
        self.assertEqual(seal["target_count"], len(seal["targets"]))
        self.assertFalse(seal["canonical_invoked"])
        for row in seal["targets"]:
            blob = index_or_head(row["path"])
            self.assertEqual(len(blob), row["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"])

    def test_14_immutable_evidence_manifest_replays_at_evidence_commit(self):
        manifest = json.loads(git_bytes("show", f"{builder.EVIDENCE_COMMIT}:docs/orin-thale/v672-v5/validation/evidence-manifest.json").decode("utf-8"))
        self.assertEqual(manifest["entry_count"], 117)
        for row in manifest["entries"]:
            blob = git_bytes("show", f"{builder.EVIDENCE_COMMIT}:{row['path']}")
            self.assertEqual(len(blob), row["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"])

    def test_15_final_manifests_replay_exact_index_or_head_blobs(self):
        for relative in ("validation/final-delta-manifest.json", "validation/final-owner-manifest.json"):
            manifest = load(relative)
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            for row in manifest["entries"]:
                blob = index_or_head(row["path"])
                self.assertEqual(len(blob), row["bytes"], row["path"])
                self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"], row["path"])

    def test_16_final_manifest_coverage_matches_delta_and_owner_surface(self):
        for relative, base in (("validation/final-delta-manifest.json", builder.EVIDENCE_COMMIT), ("validation/final-owner-manifest.json", builder.SOURCE_FINAL)):
            manifest = load(relative)
            staged = set(git_text("diff", "--cached", "--name-only", base).splitlines())
            expected = staged or set(git_text("diff", "--name-only", base, "HEAD").splitlines())
            exclusions = set(manifest["self_exclusions"]) & expected
            self.assertEqual({row["path"] for row in manifest["entries"]} | exclusions, expected)

    def test_17_final_reviews_validation_and_privacy_are_valid(self):
        review = load("validation/final-staged-review.json")
        privacy = load("validation/final-staged-privacy.json")
        validation = load("validation/final-validation-receipt.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["disallowed_paths"], [])
        self.assertEqual(review["frozen_x1_or_x2_paths"], [])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["frozen_x1_or_x2_changes"], [])

    def test_18_x1_and_x2_surfaces_are_immutable_after_evidence(self):
        changed = git_text("diff", "--cached", "--name-only", builder.EVIDENCE_COMMIT, "--", "docs/orin-thale/v672-v5/x1", "docs/orin-thale/v672-v5/x2", "scripts/build_ghc_family_orin_thale_v672_v5.py", "scripts/build_ghc_family_orin_thale_v672_v5_x2.py", "tests/test_ghc_family_orin_thale_v672_v5_x1.py", "tests/test_ghc_family_orin_thale_v672_v5_x2.py")
        self.assertEqual(changed, "")

    def test_19_all_owner_json_parses_and_documents_fit_cap(self):
        for path in OWNER_ROOT.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))
        for path in OWNER_ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)

    def test_20_materialized_files_and_commit_ceiling_remain_bounded(self):
        files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
        self.assertLess(len(files), 2000)
        head = git_text("rev-parse", "HEAD")
        count = int(git_text("rev-list", "--count", f"{builder.SOURCE_FINAL}..{head}"))
        self.assertLessEqual(count + (1 if head == builder.EVIDENCE_COMMIT else 0), 8)


if __name__ == "__main__":
    unittest.main()

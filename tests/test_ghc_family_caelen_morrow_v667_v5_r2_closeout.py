from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

from scripts.build_ghc_family_caelen_morrow_v667_v5_r2_closeout import staged_blobs


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-morrow" / "v667-v5-r2"
SOURCE = "1b1e453cb015aff20af3236bb64a8ec32b376702"
X1 = "5a5cf4859d791faff854292ed22a7a431ae4b620"
EVIDENCE = "07e929e9dc58d37d105aa198c71c4890b04f942d"


def load(relative: str) -> dict:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()


class CaelenMorrowV667V5R2CloseoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = load("closeout/phase-truth.json")
        cls.post = load("closeout/post-evidence-operational-failures.json")
        cls.methods = load("method-flow/final-method-flow-summary.json")
        cls.gates = load("closeout/exact-open-gate-register.json")
        cls.review = load("validation/final-staged-review.json")

    def test_exact_anchor_chain_and_strict_lifecycle(self) -> None:
        lifecycle = load("closeout/lifecycle-replay.json")
        self.assertEqual(SOURCE, lifecycle["source"])
        self.assertEqual(X1, lifecycle["x1"])
        self.assertEqual(EVIDENCE, lifecycle["evidence"])
        self.assertTrue(lifecycle["x1_direct_from_source"])
        self.assertTrue(lifecycle["evidence_direct_from_x1"])
        self.assertEqual(2, lifecycle["source_to_evidence_commit_count"])
        self.assertEqual(0, lifecycle["source_to_evidence_merge_count"])
        self.assertTrue(lifecycle["strict_x1_before_x2"])

    def test_phase_truth_and_four_outcome_partition(self) -> None:
        self.assertEqual({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}, self.truth["core_outcomes"])
        self.assertEqual(20, self.truth["proposal_count"])
        self.assertEqual(4450, self.truth["effective_frozen_proposal_rows"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", self.truth["terminal_verdict"])
        self.assertFalse(self.truth["independent_reproduction"])
        self.assertFalse(self.truth["full_repository_suite_run"])

    def test_retained_counts_compose_without_erasure(self) -> None:
        additive = self.post["additive_failure_count"]
        self.assertEqual(27905 + additive, self.truth["effective_negatives"])
        self.assertEqual(13737 + additive, self.truth["effective_methods"])
        self.assertEqual(189 + additive, self.truth["phase_failed_witness_count"])
        self.assertEqual(329 + additive, self.truth["phase_bounded_passing_witness_count"])
        self.assertEqual(0, self.post["failure_erased_count"])
        self.assertEqual(0, self.methods["failure_erased_count"])

    def test_open_gap_and_exact_gate_remain_visible(self) -> None:
        self.assertEqual(196, self.gates["effective_open_gaps"])
        self.assertEqual(194, self.gates["effective_exact_gates"])
        self.assertIn("future release drift", self.gates["new_open_gap"])
        self.assertIn("real production dependency release", self.gates["new_exact_gate"])
        self.assertEqual(0, self.gates["gates_erased"])

    def test_zero_real_world_and_external_counts(self) -> None:
        fields = [
            "real_people", "real_organizations", "real_private_packages", "real_production_releases",
            "real_deployments", "real_participants", "keys", "proofs", "external_publications",
            "accounts_or_credentials_mutated",
        ]
        self.assertTrue(all(self.truth[field] == 0 for field in fields))
        self.assertEqual(13, self.truth["new_package_install_count"])
        self.assertEqual(25, self.truth["mandatory_tool_use_count"])
        self.assertEqual(21, self.truth["mandatory_main_skill_use_count"])
        self.assertEqual(3, self.truth["bounded_cli_update_count"])

    def test_closeout_delta_does_not_mutate_immutable_lifecycle(self) -> None:
        self.assertEqual([], self.review["immutable_delta_mutations"])
        final_delta = load("validation/final-delta-manifest.json")
        protected = (
            "docs/caelen-morrow/v667-v5-r2/x1/",
            "docs/caelen-morrow/v667-v5-r2/x2/",
            "docs/caelen-morrow/v667-v5-r2/evidence/",
            "docs/caelen-morrow/v667-v5-r2/deck/",
            "docs/caelen-morrow/v667-v5-r2/skills/",
        )
        self.assertFalse(any(row["path"].startswith(protected) for row in final_delta["entries"]))

    def test_exact_staged_manifests_replay_index_bytes(self) -> None:
        for relative in [
            "validation/closeout-content-manifest.json",
            "validation/final-delta-manifest.json",
            "validation/final-owner-manifest.json",
        ]:
            manifest = load(relative)
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            blobs = staged_blobs([row["path"] for row in manifest["entries"]])
            for row in manifest["entries"]:
                raw = blobs[row["path"]]
                self.assertEqual(row["bytes"], len(raw), row["path"])
                self.assertEqual(row["sha256"], hashlib.sha256(raw).hexdigest(), row["path"])

    def test_final_staged_review_privacy_security_and_caps(self) -> None:
        self.assertTrue(self.review["valid"])
        self.assertEqual([], self.review["out_of_scope_paths"])
        self.assertEqual(0, self.review["privacy_confirmed_hit_count"])
        self.assertEqual(0, self.review["python_compile_error_count"])
        self.assertEqual(0, self.review["security_finding_count"])
        self.assertTrue(self.review["within_file_ceiling"])
        self.assertTrue(load("validation/final-privacy-scan.json")["valid"])
        self.assertTrue(load("validation/final-security-review.json")["valid"])

    def test_overview_is_three_page_equivalent_and_bounded(self) -> None:
        overview = (PHASE_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1800)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertIn("relational working language only", overview)
        budget = load("closeout/owner-file-budget.json")
        self.assertTrue(budget["within_file_ceiling"])
        self.assertTrue(budget["largest_document_below_ceiling"])

    def test_accessibility_evaluation_remains_reserved(self) -> None:
        reserved = load("closeout/accessibility-reservations.json")
        self.assertTrue(reserved["structural_checks_only"])
        self.assertFalse(reserved["accessibility_complete"])
        self.assertEqual("reserved", reserved["manual_browser_evaluation"])
        self.assertEqual("reserved", reserved["assistive_technology_evaluation"])
        self.assertEqual("reserved_under_authority", reserved["maori_language_evaluation"])

    def test_route_is_prepared_not_sent_for_exact_v667_v6_edge(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual("PREPARED_NOT_SENT", route["status"])
        self.assertEqual("Eiren Kestrel", route["prospective_successor_exact_title"])
        self.assertEqual("v667-v6", route["prospective_successor_phase"])
        self.assertFalse(route["send_attempted"])
        self.assertFalse(route["acknowledged"])
        self.assertFalse(route["standby_contacted"])

    def test_authority_and_scientific_boundaries_are_explicit(self) -> None:
        boundaries = load("closeout/authority-boundaries.json")
        self.assertIn("relational working language only", boundaries["relational_identity"])
        self.assertIn("no real likelihood", boundaries["gmut"])
        self.assertIn("Participant-free proxy only", boundaries["thos"])
        self.assertIn("Synthetic and nonproduction", boundaries["freed_id"])
        self.assertIn("Māori authority", boundaries["cbr"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", boundaries["terminal"])

    def test_final_prerequisites_preserve_one_shot_boundary(self) -> None:
        prereq = load("final/final-validation-prerequisites.json")
        self.assertEqual(EVIDENCE, prereq["evidence_head"])
        self.assertEqual(1, prereq["exclusive_canonical_invocation_budget"])
        self.assertEqual(0, prereq["canonical_invocations_so_far"])
        self.assertTrue(prereq["post_success_replay_forbidden"])
        self.assertFalse(prereq["full_repository_suite_authorized"])

    def test_current_head_is_evidence_or_direct_final_child(self) -> None:
        head = git("rev-parse", "HEAD")
        if head != EVIDENCE:
            self.assertEqual(EVIDENCE, git("rev-parse", f"{head}^"))
            self.assertEqual(3, int(git("rev-list", "--count", f"{SOURCE}..{head}")))
            self.assertEqual(0, int(git("rev-list", "--count", "--min-parents=2", f"{SOURCE}..{head}")))


if __name__ == "__main__":
    unittest.main()

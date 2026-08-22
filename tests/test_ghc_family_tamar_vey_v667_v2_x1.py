from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v667-v2"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TamarVeyV667V2X1Tests(unittest.TestCase):
    def test_phase_charter_exact_source_and_lane(self):
        value = load("x1/phase-charter.json")
        self.assertEqual(value["source_sha"], "dde2e23187d13cb334010943a59348330bfb67ca")
        self.assertEqual(value["branch"], "codex/GHC-Family/tamar-vey-v667-v2-full-tools")
        self.assertEqual(value["primary_pillars"], ["Freed ID and CBR Heart"])
        self.assertTrue(value["strict_x1_before_x2"])
        self.assertEqual(value["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_source_verification_anchors_and_manifests(self):
        value = load("provenance/source-verification.json")
        self.assertEqual(value["source_x1_sha"], "f9eec343455f93e0a933a00c8df4ae84f1f7bb86")
        self.assertEqual(value["source_parent_evidence_sha"], "0d9ea03b15d816373b39bcea6ef38575257313db")
        self.assertEqual(value["inherited_orin_sha"], "27a3a3cc332d27384210848d685e3bf16c6b2f0d")
        self.assertEqual(value["lifecycle_manifest_replay"]["total_observed"], 341)
        self.assertTrue(value["lifecycle_manifest_replay"]["valid"])
        self.assertTrue(value["source_validation_not_replayed"])

    def test_proposal_freeze_is_planning_only(self):
        value = load("x1/proposal-freeze.json")
        self.assertEqual(value["inherited_frozen_baseline"], 4350)
        self.assertEqual(value["genuinely_new_proposal_count"], 20)
        self.assertEqual(value["new_frozen_total"], 4370)
        self.assertEqual(value["x2_implementation_count"], 0)
        self.assertEqual(value["x2_outcome_count"], 0)
        self.assertFalse(value["outcomes_observed"])

    def test_proposal_contract_fields_are_complete(self):
        required = {
            "proposal_id",
            "title",
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "current_official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        rows = load("x1/proposal-freeze.json")["new_proposals"]
        self.assertEqual(len(rows), 20)
        self.assertTrue(all(required <= row.keys() for row in rows))
        self.assertTrue(all(len(row["preregistered_mutations"]) == 5 for row in rows))
        self.assertTrue(all(row["participant_count_planned"] == 0 for row in rows))
        self.assertTrue(all(row["real_data_rows_planned"] == 0 for row in rows))
        self.assertTrue(all(row["network_calls_planned"] == 0 for row in rows))

    def test_expected_dispositions_exact(self):
        value = load("x1/proposal-freeze.json")
        self.assertEqual(
            value["expected_disposition_counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(
            {row["expected_disposition"] for row in value["new_proposals"]},
            {"completed", "represented", "open_gap", "exact_gate"},
        )

    def test_selected_inherited_rows_have_zero_credit(self):
        rows = load("x1/proposal-freeze.json")["selected_inherited_revalidations"]
        self.assertEqual(len(rows), 20)
        self.assertTrue(all(row["original_owner"] == "Liora Venn" for row in rows))
        self.assertTrue(all(row["novelty_credit"] == 0 for row in rows))
        self.assertTrue(all(row["automatic_completion_credit"] == 0 for row in rows))

    def test_novelty_audit_covers_full_corpus(self):
        value = load("x1/novelty-audit.json")
        self.assertEqual(value["corpus_row_count"], 4350)
        self.assertEqual(value["new_title_count"], 20)
        self.assertEqual(value["new_frozen_total"], 4370)
        self.assertEqual(value["exact_inherited_collisions"], [])
        self.assertEqual(value["new_pair_collisions_at_or_above_0_70"], [])
        self.assertTrue(value["valid"])

    def test_portfolio_minimums_and_no_x1_execution(self):
        value = load("x1/portfolio-freeze.json")
        self.assertTrue(value["minimums_satisfied"])
        self.assertEqual(value["x1_execution_count"], 0)
        self.assertEqual(value["counts"]["owner_safe_now"], 30)
        self.assertEqual(value["counts"]["successor_safe_now"], 20)
        self.assertEqual(value["counts"]["owner_bounded_candidates"], 15)
        self.assertEqual(value["counts"]["successor_bounded_candidates"], 15)
        self.assertEqual(value["counts"]["exact_approval_packets"], 10)
        self.assertEqual(value["counts"]["blocked_packets"], 5)
        self.assertEqual(value["counts"]["owner_phase_local_skill_plans"], 10)
        self.assertEqual(value["counts"]["owner_family_current_runner_plans"], 10)
        self.assertEqual(value["counts"]["owner_clean_fix_refine"], 30)
        self.assertEqual(value["counts"]["successor_clean_fix_refine"], 30)

    def test_startup_failures_are_all_retained(self):
        value = load("method-flow/startup-method-flow.json")
        self.assertEqual(value["new_startup_negative_count"], 12)
        self.assertEqual(value["new_startup_method_count"], 12)
        self.assertEqual(value["effective_after_x1_startup_negatives"], 27114)
        self.assertEqual(value["effective_after_x1_startup_methods"], 12346)
        self.assertTrue(value["no_failure_erased"])
        self.assertTrue(all(row["failed_witness"]["credit"] == 0 for row in value["rows"]))
        self.assertTrue(all(row["failed_witness"]["retained"] for row in value["rows"]))

    def test_source_profiles_are_bounded(self):
        value = load("provenance/source-profiles.json")
        self.assertEqual(value["source_count"], 12)
        self.assertEqual(len(value["sources"]), 12)
        self.assertTrue(all(row["url"].startswith("https://") for row in value["sources"]))
        self.assertIn("no authorship", value["claim_boundary"])

    def test_identity_and_practice_boundaries(self):
        identity = load("identity/relational-identity.json")
        charter = load("x1/phase-charter.json")
        self.assertIn("not evidence of consciousness", identity["boundary"])
        self.assertIn("zero real people", charter["practice_boundary"])
        self.assertIn("no authorship", charter["practice_boundary"])

    def test_threat_model_reserves_ten_classes(self):
        value = load("x1/threat-model-plan.json")
        self.assertEqual(len(value["threats"]), 10)
        self.assertTrue(value["not_an_external_audit"])

    def test_workflow_has_terminal_only_route(self):
        value = load("x1/workflow-plan.json")
        self.assertEqual(value["steps"][2]["status"], "in_progress")
        self.assertEqual(value["steps"][-1]["status"], "pending")
        self.assertTrue(value["strict_x1_before_x2"])

    def test_no_post_x1_owner_paths_exist(self):
        forbidden = {"x2", "evidence", "closeout", "seal", "final", "handoffs"}
        present = {path.name for path in PHASE.iterdir() if path.is_dir()}
        self.assertFalse(forbidden & present)

    def test_every_phase_json_parses(self):
        paths = sorted(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 12)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_x1_overview_states_nonpromotion(self):
        text = (PHASE / "x1" / "x1-overview.md").read_text(encoding="utf-8")
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("no x2 implementation", text)
        self.assertIn("zero novelty and zero automatic completion credit", text)


if __name__ == "__main__":
    unittest.main()

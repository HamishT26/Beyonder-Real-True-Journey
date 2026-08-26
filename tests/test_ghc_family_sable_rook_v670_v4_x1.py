"""Planning-only tests for Sable Rook v670-v4 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_sable_rook_v670_v4_x1 as builder

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "sable-rook" / "v670-v4"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


class SableRookV670V4X1Tests(unittest.TestCase):
    def test_exact_owner_phase_source_and_branch(self):
        self.assertEqual(builder.OWNER, "Sable Rook")
        self.assertEqual(builder.PHASE, "v670-v4")
        self.assertEqual(builder.SOURCE_FINAL, "fcdc6dc7af9d85b82ef2a185254b7b2b5e43f080")
        self.assertEqual(builder.BRANCH, "codex/GHC-Family/sable-rook-v670-v4-full-tools")

    def test_forty_new_proposals_are_unique_and_four_label_only(self):
        rows = load("x1/new-proposal-freeze.json")["rows"]
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["title"] for row in rows}), 40)
        self.assertEqual(Counter(row["planned_outcome"] for row in rows), Counter(builder.OUTCOMES))
        self.assertEqual({row["planned_outcome"] for row in rows}, set(builder.CORE_LABELS))

    def test_every_proposal_has_full_preregistration_and_four_mutations(self):
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane",
            "official_or_primary_source_needs", "concrete_artifacts",
            "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
            "expected_disposition",
        }
        payload = load("x1/new-proposal-freeze.json")
        self.assertEqual(payload["planned_invalid_mutations_per_proposal"], 4)
        self.assertEqual(payload["planned_invalid_mutations"], 160)
        for row in payload["rows"]:
            self.assertTrue(required <= row.keys())
            self.assertEqual(row["expected_disposition"], row["planned_outcome"])
            self.assertEqual(row["real_people"], 0)
            self.assertEqual(row["real_records_or_objects"], 0)
            self.assertEqual(row["external_actions"], 0)
            self.assertEqual(row["x1_state"], "frozen_not_executed")

    def test_twenty_inherited_rows_have_zero_sable_credit(self):
        payload = load("x1/inherited-proposal-revalidation.json")
        self.assertEqual(payload["selected"], 20)
        self.assertEqual(payload["novelty_credit"], 0)
        self.assertEqual(payload["completion_credit"], 0)
        self.assertEqual(len(payload["rows"]), 20)
        self.assertTrue(all(row["sable_novelty_credit"] == 0 for row in payload["rows"]))
        self.assertTrue(all(row["sable_completion_credit"] == 0 for row in payload["rows"]))

    def test_semantic_audit_preserves_recovery_arithmetic_gap(self):
        audit = load("x1/semantic-neighbor-audit.json")
        self.assertEqual(audit["source_chain"], 5350)
        self.assertEqual(audit["direct_materialized_comparison_titles"], 40)
        self.assertTrue(audit["count_mirror_inconsistency_retained"])
        self.assertEqual(audit["arithmetic_closure_if_auren_rows_added"]["unrecovered"], 3770)
        self.assertEqual(audit["collisions"], 0)
        self.assertFalse(audit["universal_novelty_claim"])
        self.assertLess(audit["max_jaccard"], audit["collision_threshold"])

    def test_proposal_chain_extends_without_universal_novelty_claim(self):
        freeze = load("x1/new-proposal-freeze.json")
        truth = load("x1/phase-truth.json")
        self.assertEqual(freeze["proposal_chain_before"], 5350)
        self.assertEqual(freeze["proposal_chain_after_if_evidence_frozen"], 5390)
        self.assertFalse(truth["universal_novelty_claim"])

    def test_portfolio_counts_are_exact_and_inherited_credit_is_zero(self):
        payload = load("x1/portfolio-freeze.json")
        self.assertEqual(payload["counts"], {
            "blocked": 10,
            "candidates": 30,
            "clean_fix_refine": 60,
            "exact_approval": 20,
            "runners": 10,
            "safe_now": 60,
            "skills": 20,
            "successor_clean_fix_refine": 30,
            "successor_runners": 10,
            "successor_skills": 10,
        })
        self.assertEqual(payload["inherited_portfolio_completion_credit"], 0)
        self.assertEqual(payload["ordinary_phase_new_tool_target"], 3)

    def test_three_practice_lenses_are_synthetic_and_successor_is_unresolved(self):
        payload = load("x1/portfolio-freeze.json")
        self.assertEqual(len(payload["bounded_practice_lenses"]), 3)
        self.assertTrue(all("synthetic" in lens for lens in payload["bounded_practice_lenses"]))
        self.assertEqual(payload["successor_practice_recommendation"], "unresolved until terminal live authority")

    def test_primary_pillar_and_protected_pillars_are_explicit(self):
        truth = load("x1/phase-truth.json")
        self.assertEqual(truth["primary_pillar"], "Freed ID and CBR Heart")
        self.assertEqual(truth["protected_pillars"], ["THOS Body", "GMUT Mind"])
        self.assertFalse(truth["x2_execution_started"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_source_is_exact_direct_single_parent_zero_merge_and_equal(self):
        source = load("x1/activation-intake.json")["source_verification"]
        self.assertTrue(source["all_equal"])
        self.assertTrue(source["parent_chain"]["exact"])
        self.assertEqual(source["phase_commits"], 3)
        self.assertEqual(source["merge_commits"], 0)
        self.assertEqual(source["commit_local_manifest_entries_replayed"], 353)
        self.assertEqual(source["commit_local_manifest_mismatches"], 0)
        self.assertTrue(source["activation_packet"]["integrity_valid"])
        self.assertTrue(source["activation_packet"]["prospective_not_posthoc"])

    def test_failed_canonical_and_composite_are_not_promoted(self):
        source = load("x1/activation-intake.json")["source_verification"]
        failed = source["failed_canonical_receipt"]
        composite = source["dependency_corrected_composite"]
        self.assertEqual(failed["canonical_invocations"], 1)
        self.assertEqual(failed["canonical_successes"], 0)
        self.assertTrue(failed["replay_forbidden"])
        self.assertEqual(composite["canonical_success_credit"], 0)
        self.assertIn("ZERO_CANONICAL_AGGREGATE_CREDIT", composite["status"])
        self.assertFalse(failed["path_supplied"])
        self.assertFalse(composite["path_supplied"])

    def test_count_layers_do_not_rewrite_auren_seal(self):
        payload = load("x1/source-count-overlay.json")
        self.assertEqual(payload["repository_sealed"]["effective_negatives"], 32409)
        self.assertEqual(payload["live_activation_overlay"]["effective_negatives"], 32411)
        x1 = payload["sable_x1_overlay"]
        self.assertEqual(x1["effective_negatives"], 32427)
        self.assertEqual(x1["effective_methods"], 18538)
        self.assertEqual(x1["failed_witnesses"], 4248)
        self.assertEqual(x1["bounded_passing_witnesses"], 5578)
        self.assertFalse(x1["repository_seal_rewritten"])

    def test_method_flow_preserves_each_failure_and_recovery(self):
        ledger = load("x1/method-flow-startup.json")
        self.assertEqual(ledger["schema"], "ghc.family.method-flow-state.v1")
        self.assertEqual(ledger["counts"]["methods"], 16)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 16, "pass": 16})
        self.assertEqual(len(ledger["methods"]), 16)
        self.assertEqual(len(ledger["witnesses"]), 32)
        self.assertEqual(len({row["witness_id"] for row in ledger["witnesses"]}), 32)
        self.assertTrue(all(row["independent_reproduction"] is False for row in ledger["witnesses"]))
        self.assertTrue(all(row["retained_negative_ids"] for row in ledger["methods"]))

    def test_sources_are_official_current_or_stable_and_zero_row(self):
        payload = load("x1/source-ledger.json")
        self.assertEqual(payload["queries"], 0)
        self.assertEqual(payload["downloads"], 0)
        self.assertEqual(payload["real_rows"], 0)
        self.assertEqual({row["status"] for row in payload["sources"]}, {"current", "stable"})
        self.assertTrue(all(row["url"].startswith("https://") for row in payload["sources"]))
        self.assertIn("not observations", payload["boundary"])

    def test_identity_language_is_relational_only(self):
        boundary = load("x1/identity-and-boundary.json")["identity_boundary"].lower()
        self.assertIn("relational working language only", boundary)
        self.assertIn("not evidence of consciousness", boundary)
        self.assertIn("māori authority", boundary)

    def test_route_remains_unresolved_and_no_one_was_contacted(self):
        route = load("x1/route-plan.json")
        self.assertIsNone(route["prospective_recipient_exact_title"])
        self.assertIsNone(route["prospective_phase"])
        self.assertEqual(route["delivery_state"], "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH")
        self.assertEqual(route["successor_contact_count"], 0)
        self.assertEqual(route["standby_contact_count"], 0)
        self.assertEqual(route["task_creation_count"], 0)

    def test_overview_is_three_page_equivalent_and_below_cap(self):
        words = (OWNER_ROOT / "x1" / "integrated-overview.md").read_text(encoding="utf-8").split()
        self.assertGreaterEqual(len(words), 1200)
        self.assertLessEqual(len(words), 100000)

    def test_every_phase_document_is_below_word_cap(self):
        for path in OWNER_ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt", ".html"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)

    def test_no_x2_closeout_final_or_seal_material_exists(self):
        for name in ("x2", "closeout", "final", "seal"):
            self.assertFalse((OWNER_ROOT / name).exists())

    def test_materialized_file_count_stays_below_guard(self):
        files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
        self.assertLess(len(files), 2000)

    def test_public_x1_has_no_private_identifier_route_or_absolute_path(self):
        patterns = [
            re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
            re.compile(r"source_thread_id|<codex_delegation", re.I),
            re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
            re.compile(r"\b(?:app|plugin)://", re.I),
        ]
        for path in (OWNER_ROOT / "x1").rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                self.assertFalse(any(pattern.search(text) for pattern in patterns), path)

    def test_x1_staged_review_and_manifest_are_exact(self):
        review = load("validation/x1-staged-review.json")
        manifest = load("validation/x1-manifest.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["out_of_scope"], [])
        self.assertEqual(review["mixed_lifecycle"], [])
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["hash_domain"], "normalized_lf_exact_git_blob")
        for entry in manifest["entries"]:
            blob = subprocess.run(["git", "show", f":{entry['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])

    def test_x1_validation_receipts_are_valid_and_zero_hit(self):
        receipt = load("validation/x1-validation-receipt.json")
        method_flow = load("validation/x1-method-flow-validation.json")
        staged_privacy = load("validation/x1-staged-privacy.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["json_issues"], [])
        self.assertEqual(receipt["privacy_candidates"], [])
        self.assertEqual(receipt["confirmed_privacy_hits"], 0)
        self.assertEqual(receipt["python_compile_issues"], [])
        self.assertEqual(receipt["diff_hygiene_exit"], 0)
        self.assertLess(receipt["materialized_files"], receipt["file_guard"])
        self.assertTrue(receipt["x2_absent"])
        self.assertTrue(method_flow["valid"])
        self.assertEqual(method_flow["issue_count"], 0)
        self.assertTrue(staged_privacy["valid"])
        self.assertEqual(staged_privacy["confirmed_hit_count"], 0)
        self.assertTrue(all(row["disposition"] == "scanner_definition_or_unit_test" for row in staged_privacy["candidates"]))

    def test_build_receipt_is_planning_only(self):
        receipt = load("x1/build-receipt.json")
        self.assertFalse(receipt["x2_materialized"])
        self.assertEqual(receipt["external_actions"], 0)
        self.assertEqual(receipt["new_rows"], 40)
        self.assertEqual(receipt["inherited_rows"], 20)


if __name__ == "__main__":
    unittest.main()

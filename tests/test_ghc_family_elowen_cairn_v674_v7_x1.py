"""Planning-only tests for Elowen Cairn v674-v7 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_elowen_cairn_v674_v7_x1 as builder

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elowen-cairn" / "v674-v7"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


class ElowenCairnV674V7X1Tests(unittest.TestCase):
    def test_exact_owner_phase_source_and_branch(self):
        self.assertEqual(builder.OWNER, "Elowen Cairn")
        self.assertEqual(builder.PHASE, "v674-v7")
        self.assertEqual(builder.SOURCE_START, "02e989a10ede7e3888381abef6463a82648db443")
        self.assertEqual(builder.SOURCE_X1, "162e8cc0086c78d39ce508151c365fb221e9cd16")
        self.assertEqual(builder.SOURCE_EVIDENCE, "8916259ba31cc6b981181459e273b7540ef8f229")
        self.assertEqual(builder.SOURCE_FINAL, "c7412530cbb3a549ad681ae7b98c29b64e31ad4d")
        self.assertEqual(builder.BRANCH, "codex/GHC-Family/elowen-cairn-v674-v7-full-tools")

    def test_sixty_new_proposals_are_unique_and_four_label_only(self):
        rows = load("x1/new-proposal-freeze.json")["rows"]
        self.assertEqual(len(rows), 60)
        self.assertEqual(len({row["title"] for row in rows}), 60)
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
        self.assertEqual(payload["planned_invalid_mutations"], 240)
        for row in payload["rows"]:
            self.assertTrue(required <= row.keys())
            self.assertEqual(row["expected_disposition"], row["planned_outcome"])
            self.assertEqual(row["real_people"], 0)
            self.assertEqual(row["real_records_or_objects"], 0)
            self.assertEqual(row["external_actions"], 0)
            self.assertEqual(row["x1_state"], "frozen_not_executed")

    def test_sixty_inherited_rows_have_zero_elowen_credit(self):
        payload = load("x1/inherited-proposal-revalidation.json")
        self.assertEqual(payload["selected"], 60)
        self.assertEqual(payload["novelty_credit"], 0)
        self.assertEqual(payload["completion_credit"], 0)
        self.assertEqual(len(payload["rows"]), 60)
        self.assertTrue(all(row["elowen_novelty_credit"] == 0 for row in payload["rows"]))
        self.assertTrue(all(row["elowen_completion_credit"] == 0 for row in payload["rows"]))

    def test_semantic_audit_is_broad_but_preserves_exact_mapping_gap(self):
        audit = load("x1/semantic-neighbor-audit.json")
        corpus = audit["exact_source_tree_corpus"]
        self.assertEqual(audit["declared_source_chain"], 6910)
        self.assertEqual(audit["source_tamar_titles_verified"], 60)
        self.assertEqual(audit["reachable_unique_titles"], 2728)
        self.assertEqual(corpus["candidate_git_blob_paths"], 2109)
        self.assertEqual(corpus["semantic_occurrences"], 8738)
        self.assertEqual(corpus["unique_proposal_ids"], 2855)
        self.assertEqual(corpus["unique_titles"], 2728)
        self.assertFalse(corpus["materialized_ids_cover_declared_chain"])
        self.assertFalse(corpus["exact_canonical_row_mapping"])
        self.assertTrue(corpus["canonical_row_mapping_open_gap"])
        self.assertEqual(corpus["malformed_or_missing_blobs"], 0)
        self.assertRegex(corpus["corpus_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(audit["collisions"], 0)
        self.assertFalse(audit["universal_novelty_claim"])
        self.assertTrue(audit["canonical_row_mapping_open_gap"])
        self.assertLess(audit["max_jaccard"], audit["collision_threshold"])

    def test_proposal_chain_extends_without_universal_novelty_claim(self):
        freeze = load("x1/new-proposal-freeze.json")
        truth = load("x1/phase-truth.json")
        self.assertEqual(freeze["proposal_chain_before"], 6910)
        self.assertEqual(freeze["proposal_chain_after_if_evidence_frozen"], 6970)
        self.assertEqual(truth["proposal_chain"], {"before": 6910, "after_if_frozen": 6970})
        self.assertFalse(truth["universal_novelty_claim"])
        self.assertTrue(truth["canonical_row_mapping_open_gap"])

    def test_portfolio_counts_are_exact_and_credit_boundaries_hold(self):
        payload = load("x1/portfolio-freeze.json")
        self.assertEqual(payload["counts"], {
            "blocked": 10,
            "candidates": 80,
            "clean_fix_refine": 100,
            "exact_approval": 20,
            "inherited_reviews": 60,
            "runners": 10,
            "safe_now": 120,
            "skills": 20,
            "successor_clean_fix_refine": 60,
            "successor_runners": 10,
            "successor_seeds": 60,
            "successor_skills": 10,
        })
        self.assertEqual(payload["inherited_portfolio_completion_credit"], 0)
        self.assertEqual(payload["successor_recommendation_completion_credit"], 0)

    def test_one_bounded_practice_three_object_lenses_and_successor_recommendation(self):
        payload = load("x1/portfolio-freeze.json")
        self.assertEqual(payload["bounded_human_practice"], "synthetic museum collections registration and documentation")
        self.assertEqual(payload["bounded_object_lenses"], ["astrolabe", "music box", "kaleidoscope"])
        self.assertEqual(payload["successor_practice_recommendation_count"], 1)
        self.assertIn("successor", payload["successor_practice_recommendation"])

    def test_primary_pillar_and_protected_pillars_are_explicit(self):
        truth = load("x1/phase-truth.json")
        self.assertEqual(truth["primary_pillar"], "Freed ID and CBR Heart")
        self.assertEqual(truth["protected_pillars"], ["GMUT Mind", "THOS Body"])
        self.assertFalse(truth["x2_execution_started"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_source_is_exact_direct_single_parent_zero_merge_and_equal(self):
        source = load("x1/activation-intake.json")["source_verification"]
        self.assertTrue(source["all_equal"])
        self.assertTrue(source["parent_chain"]["exact"])
        self.assertEqual(source["phase_commits"], 3)
        self.assertEqual(source["merge_commits"], 0)
        self.assertEqual(source["commit_local_manifest_entries_replayed"], 608)
        self.assertTrue(source["expected_manifest_contracts_valid"])
        self.assertEqual(source["manifest_mismatches"], 0)
        self.assertTrue(source["content_seal"]["valid"])
        self.assertTrue(source["activation_packet"]["integrity_valid"])
        self.assertEqual(source["activation_packet"]["sha256"], builder.ACTIVATION_SHA256)

    def test_source_canonical_is_inherited_zero_credit_and_not_replayed(self):
        source = load("x1/activation-intake.json")["source_verification"]
        receipt = source["source_canonical_receipt"]
        self.assertEqual(receipt["canonical_invocations"], 1)
        self.assertEqual(receipt["canonical_successes"], 1)
        self.assertTrue(receipt["replay_forbidden"])
        self.assertEqual(receipt["status"], "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL")
        self.assertEqual(receipt["elowen_validation_credit"], 0)
        overlay = source["source_post_final_overlay"]
        self.assertEqual([row["negative_id"] for row in overlay], ["TV6746-POST-N001"])
        self.assertTrue(all(row["retained_after_recovery"] for row in overlay))

    def test_count_layers_do_not_rewrite_tamar_seal(self):
        payload = load("x1/source-count-overlay.json")
        self.assertEqual(payload["repository_sealed"]["effective_negatives"], 39390)
        self.assertEqual(payload["live_activation_overlay"]["effective_negatives"], 39391)
        x1 = payload["elowen_x1_overlay"]
        count = len(builder.STARTUP_FAILURES)
        self.assertEqual(x1["effective_negatives"], 39391 + count)
        self.assertEqual(x1["effective_methods"], 27577 + count)
        self.assertEqual(x1["failed_witnesses"], 11052 + count)
        self.assertEqual(x1["bounded_passing_witnesses"], 14860 + count)
        self.assertEqual(x1["elowen_startup_failures"], count)
        self.assertFalse(x1["repository_seal_rewritten"])

    def test_method_flow_preserves_each_failure_and_recovery(self):
        ledger = load("x1/method-flow-startup.json")
        self.assertEqual(ledger["schema"], "ghc.family.method-flow-state.v1")
        count = len(builder.STARTUP_FAILURES)
        self.assertEqual(ledger["counts"]["methods"], count)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": count, "pass": count})
        self.assertEqual(len(ledger["methods"]), count)
        self.assertEqual(len(ledger["witnesses"]), count * 2)
        self.assertEqual(len({row["witness_id"] for row in ledger["witnesses"]}), count * 2)
        self.assertTrue(all(row["independent_reproduction"] is False for row in ledger["witnesses"]))
        self.assertTrue(all(row["retained_negative_ids"] for row in ledger["methods"]))

    def test_sources_are_official_current_or_stable_and_zero_row(self):
        payload = load("x1/source-ledger.json")
        self.assertEqual(payload["read_only_source_page_checks"], 6)
        self.assertEqual(payload["api_calls"], 0)
        self.assertEqual(payload["dataset_or_media_downloads"], 0)
        self.assertEqual(payload["real_rows"], 0)
        self.assertEqual(payload["external_writes"], 0)
        self.assertEqual(len(payload["sources"]), 6)
        self.assertTrue(all("current" in row["status"] or "stable" in row["status"] for row in payload["sources"]))
        self.assertTrue(all(row["url"].startswith("https://") for row in payload["sources"]))
        self.assertIn("not observations", payload["boundary"])

    def test_identity_language_is_relational_only(self):
        identity = load("x1/identity-and-boundary.json")
        boundary = identity["identity_boundary"].lower()
        self.assertEqual(identity["relational_role"], "relational boundary cartographer and evidence steward")
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
        self.assertEqual(receipt["external_writes"], 0)
        self.assertEqual(receipt["read_only_source_page_checks"], 6)
        self.assertEqual(receipt["new_rows"], 60)
        self.assertEqual(receipt["inherited_rows"], 60)


if __name__ == "__main__":
    unittest.main()

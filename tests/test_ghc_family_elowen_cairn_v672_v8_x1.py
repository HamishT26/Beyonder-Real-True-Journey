"""Planning-only tests for Elowen Cairn v672-v8 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_elowen_cairn_v672_v8_x1 as builder

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elowen-cairn" / "v672-v8"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


class ElowenCairnV672V8X1Tests(unittest.TestCase):
    def test_exact_owner_phase_source_and_branch(self):
        self.assertEqual(builder.OWNER, "Elowen Cairn")
        self.assertEqual(builder.PHASE, "v672-v8")
        self.assertEqual(builder.SOURCE_START, "e3aad89f695a62d5997b129e260e62267cb145ab")
        self.assertEqual(builder.SOURCE_X1, "34e33ee699e6cba5c17c0eafd847e2b86d7a91c4")
        self.assertEqual(builder.SOURCE_EVIDENCE, "6a5379632013cfcb4288845ec78ab9cc6901c449")
        self.assertEqual(builder.SOURCE_FINAL, "23110f2bb3a8b111626e2af56b6343bbc15a9496")
        self.assertEqual(builder.BRANCH, "codex/GHC-Family/elowen-cairn-v672-v8-full-tools")

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

    def test_twenty_inherited_rows_have_zero_elowen_credit(self):
        payload = load("x1/inherited-proposal-revalidation.json")
        self.assertEqual(payload["selected"], 20)
        self.assertEqual(payload["novelty_credit"], 0)
        self.assertEqual(payload["completion_credit"], 0)
        self.assertEqual(len(payload["rows"]), 20)
        self.assertTrue(all(row["elowen_novelty_credit"] == 0 for row in payload["rows"]))
        self.assertTrue(all(row["elowen_completion_credit"] == 0 for row in payload["rows"]))

    def test_semantic_audit_is_broad_but_preserves_exact_mapping_gap(self):
        audit = load("x1/semantic-neighbor-audit.json")
        corpus = audit["exact_source_tree_corpus"]
        self.assertEqual(audit["declared_source_chain"], 6190)
        self.assertEqual(audit["source_tamar_titles_verified"], 40)
        self.assertEqual(audit["reachable_unique_titles"], 2009)
        self.assertEqual(corpus["candidate_git_blob_paths"], 1752)
        self.assertEqual(corpus["semantic_occurrences"], 7318)
        self.assertEqual(corpus["unique_proposal_ids"], 2135)
        self.assertEqual(corpus["unique_titles"], 2009)
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
        self.assertEqual(freeze["proposal_chain_before"], 6190)
        self.assertEqual(freeze["proposal_chain_after_if_evidence_frozen"], 6230)
        self.assertEqual(truth["proposal_chain"], {"before": 6190, "after_if_frozen": 6230})
        self.assertFalse(truth["universal_novelty_claim"])
        self.assertTrue(truth["canonical_row_mapping_open_gap"])

    def test_portfolio_counts_are_exact_and_credit_boundaries_hold(self):
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
        self.assertEqual(payload["successor_recommendation_completion_credit"], 0)
        self.assertEqual(payload["ordinary_phase_new_tool_target"], 3)

    def test_three_practice_lenses_and_one_successor_recommendation_are_synthetic(self):
        payload = load("x1/portfolio-freeze.json")
        self.assertEqual(len(payload["bounded_practice_lenses"]), 3)
        self.assertTrue(all("synthetic" in lens for lens in payload["bounded_practice_lenses"]))
        self.assertEqual(payload["successor_practice_recommendation_count"], 1)
        self.assertIn("synthetic", payload["successor_practice_recommendation"])
        self.assertIn("terminally authorized successor", payload["successor_practice_recommendation"])

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
        self.assertEqual(source["commit_local_manifest_entries_replayed"], 488)
        self.assertEqual(source["commit_local_manifest_mismatches"], 0)
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
        self.assertEqual(overlay["negative_id"], "TV6727-POST-N001")
        self.assertTrue(overlay["retained_after_recovery"])

    def test_count_layers_do_not_rewrite_tamar_seal(self):
        payload = load("x1/source-count-overlay.json")
        self.assertEqual(payload["repository_sealed"]["effective_negatives"], 35967)
        self.assertEqual(payload["live_activation_overlay"]["effective_negatives"], 35968)
        x1 = payload["elowen_x1_overlay"]
        count = len(builder.STARTUP_FAILURES)
        self.assertEqual(x1["effective_negatives"], 35968 + count)
        self.assertEqual(x1["effective_methods"], 22263 + count)
        self.assertEqual(x1["failed_witnesses"], 7629 + count)
        self.assertEqual(x1["bounded_passing_witnesses"], 9826 + count)
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
        self.assertEqual(payload["read_only_source_page_checks"], 8)
        self.assertEqual(payload["failed_projection_attempts"], 1)
        self.assertEqual(payload["api_calls"], 0)
        self.assertEqual(payload["dataset_or_media_downloads"], 0)
        self.assertEqual(payload["real_rows"], 0)
        self.assertEqual(payload["external_writes"], 0)
        self.assertEqual(len(payload["sources"]), 8)
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
        self.assertEqual(receipt["read_only_source_page_checks"], 8)
        self.assertEqual(receipt["new_rows"], 40)
        self.assertEqual(receipt["inherited_rows"], 20)


if __name__ == "__main__":
    unittest.main()

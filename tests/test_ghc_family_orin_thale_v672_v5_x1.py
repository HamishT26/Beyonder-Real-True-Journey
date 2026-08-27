"""Planning-only tests for Orin Thale v672-v5 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_orin_thale_v672_v5 as builder


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "orin-thale" / "v672-v5"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


class OrinThaleV672V5X1Tests(unittest.TestCase):
    def test_exact_owner_phase_source_and_branch(self):
        self.assertEqual(builder.OWNER, "Orin Thale")
        self.assertEqual(builder.PHASE, "v672-v5")
        self.assertEqual(builder.SOURCE_START, "2d76e3120bd8f2f2fd70f3ff164ef80e19be3031")
        self.assertEqual(builder.SOURCE_X1, "0ebc12367f26a7d6cf5cca9466843f2cbaade293")
        self.assertEqual(builder.SOURCE_EVIDENCE, "581f0be723d65c685ba388ce61a707d42ab784e2")
        self.assertEqual(builder.SOURCE_FINAL, "8f672ef30372b4adf457140c254931dc365e9d31")
        self.assertEqual(builder.BRANCH, "codex/GHC-Family/orin-thale-v672-v5-full-tools")

    def test_forty_new_proposals_are_unique_and_four_label_only(self):
        rows = load("x1/new-proposal-freeze.json")["rows"]
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["title"] for row in rows}), 40)
        self.assertEqual(Counter(row["planned_outcome"] for row in rows), Counter(builder.OUTCOMES))
        self.assertEqual({row["planned_outcome"] for row in rows}, set(builder.CORE_LABELS))

    def test_every_proposal_has_full_preregistration_and_four_mutations(self):
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
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

    def test_twenty_inherited_rows_have_zero_orin_credit(self):
        payload = load("x1/inherited-proposal-revalidation.json")
        self.assertEqual(payload["selected"], 20)
        self.assertEqual(payload["novelty_credit"], 0)
        self.assertEqual(payload["completion_credit"], 0)
        self.assertEqual(len(payload["rows"]), 20)
        self.assertTrue(all(row["orin_novelty_credit"] == 0 for row in payload["rows"]))
        self.assertTrue(all(row["orin_completion_credit"] == 0 for row in payload["rows"]))

    def test_semantic_audit_is_source_bounded_and_refuses_universal_claim(self):
        audit = load("x1/semantic-neighbor-audit.json")
        corpus = audit["corpus"]
        self.assertEqual(audit["source_chain"], 6070)
        self.assertGreaterEqual(corpus["unique_proposal_ids"], 1900)
        self.assertGreaterEqual(corpus["unique_titles"], 1800)
        self.assertFalse(corpus["id_superset_covers_declared_chain"])
        self.assertFalse(corpus["exact_canonical_row_mapping"])
        self.assertTrue(corpus["canonical_row_mapping_open_gap"])
        self.assertEqual(corpus["malformed_or_missing_blobs"], 0)
        self.assertRegex(corpus["corpus_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(audit["collisions"], 0)
        self.assertFalse(audit["universal_novelty_claim"])
        self.assertLess(audit["max_jaccard"], audit["collision_threshold"])

    def test_proposal_chain_extends_without_universal_novelty_claim(self):
        freeze = load("x1/new-proposal-freeze.json")
        truth = load("x1/phase-truth.json")
        self.assertEqual(freeze["proposal_chain_before"], 6070)
        self.assertEqual(freeze["proposal_chain_after_if_evidence_frozen"], 6110)
        self.assertEqual(truth["proposal_chain"], {"before": 6070, "after_if_frozen": 6110})
        self.assertFalse(truth["universal_novelty_claim"])
        self.assertTrue(truth["canonical_row_mapping_open_gap"])

    def test_portfolio_counts_are_exact_and_credit_boundaries_hold(self):
        payload = load("x1/portfolio-freeze.json")
        self.assertEqual(
            payload["counts"],
            {
                "blocked": 10,
                "candidates": 30,
                "clean_fix_refine": 60,
                "exact_approval": 20,
                "runners": 10,
                "safe_now": 60,
                "skills": 20,
                "successor_candidates": 10,
                "successor_clean_fix_refine": 30,
                "successor_runners": 5,
                "successor_safe_now": 20,
                "successor_skills": 10,
            },
        )
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
        self.assertTrue(source["valid"])
        self.assertTrue(source["all_equal"])
        self.assertTrue(source["source_worktree_clean"])
        self.assertTrue(source["parent_chain"]["exact"])
        self.assertEqual(source["phase_commits"], 3)
        self.assertEqual(source["merge_commits"], 0)
        self.assertEqual(source["commit_local_manifest_entries_replayed"], 436)
        self.assertEqual(source["commit_local_manifest_mismatches"], 0)
        self.assertTrue(all(row["valid"] for row in source["manifests"]))
        self.assertTrue(source["content_seal"]["valid"])

    def test_source_canonical_is_inherited_zero_credit_and_not_replayed(self):
        receipt = load("x1/activation-intake.json")["source_verification"]["source_canonical_receipt"]
        self.assertEqual(receipt["sha256"], builder.SOURCE_CANONICAL_SHA256)
        self.assertEqual(receipt["canonical_invocations"], 1)
        self.assertEqual(receipt["canonical_successes"], 1)
        self.assertEqual(receipt["selected_tests"], 51)
        self.assertEqual(receipt["detailed_checks"]["passed"], 915)
        self.assertEqual(receipt["minimal_checks"]["passed"], 26)
        self.assertTrue(receipt["replay_forbidden"])
        self.assertFalse(receipt["private_locator_retained"])
        self.assertEqual(receipt["orin_validation_credit"], 0)

    def test_count_layers_do_not_rewrite_caelen_seal(self):
        payload = load("x1/source-count-overlay.json")
        self.assertEqual(payload["repository_sealed"]["effective_negatives"], 35416)
        self.assertEqual(payload["live_activation_overlay"]["effective_negatives"], 35417)
        x1 = payload["orin_x1_overlay"]
        self.assertEqual(x1["effective_negatives"], 35431)
        self.assertEqual(x1["effective_methods"], 22000)
        self.assertEqual(x1["failed_witnesses"], 7252)
        self.assertEqual(x1["bounded_passing_witnesses"], 9303)
        self.assertEqual(x1["orin_startup_failures"], 14)
        self.assertEqual(x1["orin_startup_methods"], 13)
        self.assertFalse(x1["repository_seal_rewritten"])

    def test_method_flow_preserves_each_failure_and_recovery(self):
        ledger = load("x1/method-flow-startup.json")
        self.assertEqual(ledger["schema"], "ghc.family.method-flow-state.v1")
        self.assertEqual(ledger["counts"]["methods"], 13)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 14, "pass": 15})
        self.assertEqual(len(ledger["methods"]), 13)
        self.assertEqual(len(ledger["witnesses"]), 29)
        self.assertEqual(len({row["witness_id"] for row in ledger["witnesses"]}), 29)
        self.assertTrue(all(row["independent_reproduction"] is False for row in ledger["witnesses"]))
        self.assertTrue(all(row["retained_negative_ids"] for row in ledger["methods"]))
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in ledger["methods"]))

    def test_sources_are_official_and_zero_row(self):
        payload = load("x1/source-ledger.json")
        self.assertEqual(payload["read_only_query_attempts"], 2)
        self.assertEqual(payload["failed_projection_attempts"], 0)
        self.assertEqual(payload["downloads"], 0)
        self.assertEqual(payload["real_rows"], 0)
        self.assertEqual(payload["external_writes"], 0)
        self.assertEqual(len(payload["sources"]), 7)
        self.assertTrue(all(row["url"].startswith("https://") for row in payload["sources"]))
        self.assertIn("not observations", payload["boundary"])

    def test_identity_language_is_relational_only(self):
        identity = load("x1/identity-and-boundary.json")
        boundary = identity["identity_boundary"].lower()
        self.assertEqual(identity["relational_role"], "relational provenance-and-access-boundary cartographer")
        self.assertIn("relational working language only", boundary)
        self.assertIn("not evidence of consciousness", boundary)
        self.assertIn("māori authority", boundary)

    def test_route_is_terminally_gated_and_no_one_was_contacted(self):
        route = load("x1/route-plan.json")
        self.assertEqual(route["live_provisional_recipient_exact_title"], "Liora Venn")
        self.assertEqual(route["live_provisional_phase"], "v672-v6")
        self.assertEqual(route["delivery_state"], "TERMINALLY_GATED_NO_CONTACT")
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

    def test_x1_method_flow_validation_is_exact(self):
        payload = load("validation/x1-method-flow-validation.json")
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["issue_count"], 0)
        self.assertEqual(payload["method_count"], 13)
        self.assertEqual(payload["witness_count"], 29)
        self.assertFalse(payload["runner_private_locator_retained"])

    def test_x1_validation_receipt_and_privacy_are_valid(self):
        receipt = load("validation/x1-validation-receipt.json")
        privacy = load("validation/x1-staged-privacy.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["json_issues"], [])
        self.assertEqual(receipt["python_compile_issues"], [])
        self.assertTrue(receipt["x2_absent"])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)

    def test_x1_staged_review_and_manifest_are_exact(self):
        review = load("validation/x1-staged-review.json")
        manifest = load("validation/x1-manifest.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["out_of_scope"], [])
        self.assertEqual(review["mixed_lifecycle"], [])
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["hash_domain"], "normalized_lf_exact_git_blob")
        for entry in manifest["entries"]:
            blob = subprocess.run(
                ["git", "show", f":{entry['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            oid = subprocess.run(
                ["git", "rev-parse", f":{entry['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ).stdout.strip()
            self.assertEqual(oid, entry["git_blob_oid"])
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])
        staged = set(
            subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ).stdout.splitlines()
        )
        declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
        self.assertEqual(staged, declared)


if __name__ == "__main__":
    unittest.main()

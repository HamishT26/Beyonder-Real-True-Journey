"""Owner-scoped tests for Tamar Vey v688-v3 only."""
from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/tamar-vey/v688-v3"
sys.path.insert(0, str(ROOT / "scripts/tamar_vey_v688_v3"))

from ghc_family_font_evidence_core import canonical, evaluate, evaluate_raw  # noqa: E402


def load(relative):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


class TamarFontEvidenceTests(unittest.TestCase):
    def test_001_all_frozen_complete_outputs_match(self):
        proposals = load("x1/new-proposals.json")["proposals"]
        self.assertEqual(len(proposals), 200)
        for proposal in proposals:
            self.assertEqual(evaluate(proposal["input"]), proposal["expected_output"], proposal["proposal_id"])

    def test_002_frozen_input_objects_remain_unchanged(self):
        proposals = load("x1/new-proposals.json")["proposals"]
        for proposal in proposals:
            before = canonical(proposal["input"])
            evaluate(proposal["input"])
            self.assertEqual(canonical(proposal["input"]), before)

    def test_003_only_four_outcomes_are_used(self):
        proposals = load("x1/new-proposals.json")["proposals"]
        counts = collections.Counter(row["expected_execution_disposition"] for row in proposals)
        self.assertEqual(counts, {"completed": 178, "represented": 17, "open_gap": 2, "exact_gate": 3})

    def test_004_proposal_identifiers_titles_and_inputs_are_unique(self):
        proposals = load("x1/new-proposals.json")["proposals"]
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 200)
        self.assertEqual(len({row["title"] for row in proposals}), 200)
        self.assertEqual(len({hashlib.sha256(canonical(row["input"]).encode("ascii")).hexdigest() for row in proposals}), 200)

    def test_005_source_bounded_novelty_has_no_quarantine(self):
        novelty = load("x1/novelty-review.json")
        self.assertFalse(novelty["universal_novelty_claimed"])
        self.assertEqual(len(novelty["reviews"]), 200)
        self.assertFalse(any(row["exact_title_collision"] or row["exact_input_collision"] or row["token_jaccard"] >= 0.78 for row in novelty["reviews"]))

    def test_006_inherited_reviews_have_zero_credit(self):
        inherited = load("x1/inherited-review.json")
        self.assertEqual(len(inherited["rows"]), 200)
        self.assertTrue(all(row["novelty_credit"] == 0 and row["completion_credit"] == 0 for row in inherited["rows"]))

    def test_007_contract_results_bind_each_definition(self):
        proposals = load("x1/new-proposals.json")["proposals"]
        results = load("x2/contract-results.json")["rows"]
        self.assertEqual(len(results), 200)
        for proposal, result in zip(proposals, results):
            self.assertEqual(proposal["proposal_id"], result["proposal_id"])
            self.assertTrue(result["pass"] and result["complete_match"] and result["input_unchanged"])

    def test_008_all_altered_output_candidates_are_rejected(self):
        mutation = load("x2/mutation-results.json")
        self.assertEqual(mutation["count"], 250)
        self.assertTrue(all(row["rejected"] and row["candidate_success_credit"] == 0 for row in mutation["rows"]))

    def test_009_safe_and_cfr_procedures_pass(self):
        portfolio = load("x2/portfolio-results.json")
        self.assertEqual(len(portfolio["safe"]), 300)
        self.assertEqual(len(portfolio["clean_fix_refine"]), 300)
        self.assertTrue(all(row["pass"] for row in portfolio["safe"] + portfolio["clean_fix_refine"]))

    def test_010_exact_and_blocked_packets_remain_unexecuted(self):
        portfolio = load("x2/portfolio-results.json")
        self.assertEqual(len(portfolio["exact_packets"]), 50)
        self.assertEqual(len(portfolio["blocked_packets"]), 30)
        self.assertTrue(all(not row["executed"] for row in portfolio["exact_packets"] + portfolio["blocked_packets"]))

    def test_011_duplicate_and_nonfinite_json_are_refused(self):
        self.assertEqual(evaluate_raw('{"operation":"unicode_scalar","operation":"unicode_scalar"}')["error"], "DUPLICATE_KEY")
        self.assertEqual(evaluate_raw('{"operation":"unicode_scalar","probe":NaN}')["error"], "NONFINITE")

    def test_012_metric_semantic_discrepancy_is_retained(self):
        correction = load("x2/metric-semantic-correction.json")
        self.assertEqual(correction["frozen_expected_rsb"], 0)
        self.assertEqual(correction["standard_formula_result"], 20)
        self.assertFalse(correction["open_type_conformance_claimed"])
        self.assertFalse(correction["failure_erased"])

    def test_013_ten_initialized_skill_packages_are_complete(self):
        folders = sorted(path for path in (BASE / "skills").iterdir() if path.is_dir())
        self.assertEqual(len(folders), 10)
        for folder in folders:
            manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["member_count"], len(manifest["members"]))
            for member in manifest["members"]:
                raw = (folder / member["path"]).read_bytes()
                self.assertEqual(len(raw), member["bytes"])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), member["sha256"])

    def test_014_skill_use_preserves_read_validate_then_smoke_order(self):
        receipt = load("x2/skill-use.json")
        self.assertEqual(receipt["count"], 10)
        self.assertTrue(all(row["complete_guide_read_before_use"] and row["validator_pass"] and row["positive_pass"] and row["adverse_refused"] for row in receipt["rows"]))

    def test_015_five_runners_cover_twenty_operations(self):
        receipt = load("x2/runner-use.json")
        self.assertEqual(receipt["count"], 5)
        self.assertEqual(receipt["positive_operations"], 20)
        self.assertTrue(all(item["pass"] for row in receipt["rows"] for item in row["operations"]))
        self.assertTrue(all(row["adverse_refused"] for row in receipt["rows"]))

    def test_016_three_package_smokes_and_adverse_cases_pass(self):
        receipt = load("x2/package-smokes.json")
        self.assertEqual(receipt["distribution_count"], 3)
        self.assertEqual(receipt["versions"], {"fonttools": "4.64.0", "uharfbuzz": "0.56.1", "unicodedata2": "17.0.1"})
        self.assertTrue(all(row["refused"] for row in receipt["adverse"].values()))
        self.assertEqual(receipt["real_fonts"], 0)

    def test_017_package_audit_is_bounded_not_exhaustive(self):
        receipt = load("x2/package-audit.json")
        self.assertEqual(len(receipt["rows"]), 3)
        self.assertFalse(receipt["exhaustive_security"])
        self.assertFalse(receipt["future_security_assurance"])
        self.assertEqual(receipt["independent_security_review"], "open_gap")

    def test_018_promotion_is_collision_free_and_byte_equal(self):
        receipt = load("x2/promotion-receipt.json")
        self.assertEqual(receipt["skills"], 10)
        self.assertEqual(receipt["runners"], 5)
        self.assertEqual(receipt["overwrites"], 0)
        self.assertEqual(receipt["caches_copied"], 0)
        self.assertTrue(receipt["all_source_global_bytes_equal"])

    def test_019_method_flow_is_complete_and_nonerasing(self):
        ledger = load("x2/method-flow/ledger.json")
        self.assertEqual(len(ledger["methods"]), ledger["counts"]["methods"])
        self.assertEqual(len(ledger["witnesses"]), ledger["counts"]["witnesses"])
        self.assertEqual(len(ledger["state_events"]), ledger["counts"]["state_events"])
        self.assertEqual(collections.Counter(row["result"] for row in ledger["witnesses"]), ledger["counts"]["witness_results"])
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in ledger["methods"]))
        self.assertTrue(all(row["retained_negative_ids"] for row in ledger["witnesses"] if row["result"] == "fail"))

    def test_020_four_tier_deck_has_valid_parent_edges(self):
        index = load("x2/deck/deck-index.json")
        cards = {card_id: load("x2/deck/cards/" + card_id + ".json") for card_id in index["cards"]}
        self.assertEqual(len(cards), 286)
        self.assertEqual(index["counts"], {"1": 1, "2": 3, "3": 4, "4": 278})
        self.assertEqual(index["unresolved_parents"], 0)
        for row in cards.values():
            if row["tier"] == 1:
                self.assertEqual(row["parent_ids"], [])
            else:
                self.assertEqual(len(row["parent_ids"]), 1)
                self.assertEqual(cards[row["parent_ids"][0]]["tier"], row["tier"] - 1)

    def test_021_deck_manifest_binds_every_other_deck_file(self):
        deck = BASE / "x2/deck"
        manifest = load("x2/deck/card-manifest.json")
        self.assertEqual(manifest["count"], len(manifest["entries"]))
        self.assertEqual(len({row["path"] for row in manifest["entries"]}), manifest["count"])
        for row in manifest["entries"]:
            raw = (deck / row["path"]).read_bytes()
            self.assertEqual(len(raw), row["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row["sha256"])

    def test_022_meta_tool_collisions_have_disjoint_operation_scopes(self):
        review = load("x2/tooling/meta-tool-box/collision-review.json")
        self.assertEqual(review["finding_count"], 45)
        self.assertTrue(review["all_operation_intersections_empty"])
        self.assertTrue(all(not row["silent_winner_selected"] for row in review["findings"]))

    def test_023_open_and_exact_gates_are_additive(self):
        open_gap = load("x2/open-gap-register.json")
        exact_gate = load("x2/exact-gate-register.json")
        self.assertEqual((open_gap["inherited"], open_gap["added"], open_gap["closed_by_software"]), (750, 2, 0))
        self.assertEqual((exact_gate["inherited"], exact_gate["added"], exact_gate["closed_by_software"]), (750, 3, 0))

    def test_024_effective_counts_preserve_source_overlay(self):
        truth = load("x2/phase-truth.json")
        self.assertEqual(truth["effective_counts"], {"proposals": 16030, "negatives": 83453, "methods": 93448, "failed_witnesses": 54301, "passing_witnesses": 84879, "open_gaps": 752, "exact_gates": 753})

    def test_025_release_profile_passes_and_legacy_floor_stays_failed(self):
        release = load("x1/tooling/release-profile-validation.json")
        reconcile = load("x1/tooling/workflow-plan-current-release-reconciliation.json")
        self.assertEqual(release["status"], "PASS")
        self.assertFalse(reconcile["legacy_workflow_audit"]["valid"])
        self.assertEqual(reconcile["current_release_profile"]["runner_build_minimum"], 5)

    def test_026_environment_receipt_preserves_isolation(self):
        receipt = load("x2/environment-receipt.json")
        self.assertEqual(receipt["distribution_count"], 3)
        self.assertFalse(receipt["environment_pip_present"])
        self.assertFalse(receipt["host_python_mutated"])
        self.assertTrue(receipt["wheel_only"] and receipt["no_index"] and receipt["no_deps"] and receipt["require_hashes"])

    def test_027_workload_receipt_avoids_subjective_or_employment_claim(self):
        receipt = load("x2/workload-wellbeing.json")
        self.assertFalse(receipt["subjective_wellbeing_measured"])
        self.assertFalse(receipt["employment_claimed"])
        self.assertEqual(receipt["handover_state"], "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED")

    def test_028_terminal_truth_remains_not_ready(self):
        truth = load("x2/phase-truth.json")
        self.assertFalse(truth["full_repository_suite"])
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(truth["canonical_invocations"], 0)
        self.assertEqual(truth["successor_contacts"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()

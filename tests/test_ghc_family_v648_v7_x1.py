from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v648-v7"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V648V7X1Tests(unittest.TestCase):
    def test_identity_is_relational_and_corrigible(self):
        data = load("identity-receipt.json")
        self.assertEqual(data["owner"], "Tamar Vey")
        self.assertIn("Relational working language only", data["identity_boundary"])
        self.assertIn("pause", data["corrigibility"])

    def test_exact_source_and_lane_contract(self):
        data = load("environment/startup-receipt.json")
        self.assertEqual(data["source_head"], "38e3fe7bc710239337f831617ced97bec51d7d7a")
        self.assertTrue(data["source_ancestry"])
        self.assertEqual(data["source_phase_commits"], 3)
        self.assertEqual(data["source_merges"], 0)
        self.assertTrue(data["owner_fast_forwarded_only"])

    def test_source_manifests_preserve_domains(self):
        data = load("environment/source-manifest-verification.json")
        self.assertEqual([data[k]["path_blob_entries_verified"] for k in ("x1", "evidence", "final")], [79, 183, 66])
        self.assertEqual(data["final"]["checkout_byte_entries_verified"], 66)
        self.assertFalse(data["historical_checkout_bytes_recreated"])
        self.assertFalse(data["replay_created"])

    def test_exactly_ten_proposals_with_required_fields(self):
        data = load("x1-proposals.json")
        self.assertEqual(data["prior_frozen_proposal_count"], 620)
        self.assertEqual(data["frozen_total_after_x1"], 630)
        self.assertEqual(len(data["proposals"]), 10)
        required = {"proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "source_needs", "artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        for proposal in data["proposals"]:
            self.assertTrue(required <= set(proposal))

    def test_expected_distribution_and_vocabulary(self):
        data = load("x1-proposals.json")
        counts = {name: 0 for name in data["outcome_classes"]}
        for proposal in data["proposals"]:
            counts[proposal["expected_disposition"]] += 1
        self.assertEqual(counts, {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})

    def test_novelty_audit_covers_all_prior_titles(self):
        data = load("provenance/proposal-collision-audit.json")
        self.assertEqual(data["prior_count"], 620)
        self.assertEqual(len(data["rows"]), 10)
        self.assertLess(data["maximum_observed_jaccard"], data["threshold"])
        self.assertTrue(all(row["manual_review"] for row in data["rows"]))

    def test_frozen_chain_index_is_630(self):
        data = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(data["prior_count"], 620)
        self.assertEqual(data["new_count"], 10)
        self.assertEqual(data["count"], 630)

    def test_source_statuses_are_explicit(self):
        data = load("sources/source-ledger.json")
        self.assertEqual(set(data["allowed_statuses"]), {"current", "stable", "draft", "watch"})
        self.assertTrue(all(row["status"] in data["allowed_statuses"] for row in data["sources"]))
        self.assertTrue(all(row["not_observation"] for row in data["sources"]))
        self.assertTrue(all(data["status_counts"][name] > 0 for name in data["allowed_statuses"]))

    def test_portfolio_floors_are_new_and_frozen(self):
        safe = load("approval-packets/x1-safe-now-portfolio.json")
        candidates = load("prototypes/x1-candidate-plan.json")
        skills = load("prototypes/x1-skill-runner-plan.json")
        clean = load("maintenance/x1-clean-refine-plan.json")
        self.assertEqual((safe["count"], candidates["count"], skills["skill_count"], skills["runner_count"], clean["count"]), (30, 20, 20, 10, 30))
        self.assertEqual(safe["inherited_completion_credit"], 0)
        self.assertEqual(candidates["inherited_completion_credit"], 0)
        self.assertEqual(clean["destructive_actions"], 0)

    def test_exact_and_blocked_packets_remain_unexecuted(self):
        exact = load("approval-packets/inherited-exact-approvals.json")
        blocked = load("approval-packets/inherited-blocked-packets.json")
        self.assertEqual((exact["count"], exact["executed_count"]), (10, 0))
        self.assertEqual((blocked["count"], blocked["executed_count"]), (5, 0))

    def test_negatives_and_method_flow_are_retained(self):
        negatives = load("retained-negative-register.json")
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertEqual(negatives["inherited_effective"], 4482)
        self.assertEqual(negatives["x1_operational"], 17)
        self.assertEqual(negatives["effective_at_x1"], 4499)
        self.assertFalse(negatives["negative_erased"])
        self.assertEqual(len(ledger["methods"]), 13)
        self.assertEqual(sum(w["result"] == "fail" for w in ledger["witnesses"]), 17)
        self.assertEqual(sum(w["result"] == "pass" for w in ledger["witnesses"]), 19)

    def test_x1_has_no_x2_implementation_or_outcome(self):
        truth = load("phase-truth.json")
        review = load("validation/x1-review.json")
        self.assertEqual(truth["stage"], "x1_frozen_not_executed")
        self.assertFalse(truth["x2_started"])
        self.assertIsNone(truth["observed_distribution"])
        self.assertEqual(review["x2_implementation_count"], 0)
        self.assertEqual(review["x2_observed_outcome_count"], 0)

    def test_single_pass_and_route_are_unused(self):
        plan = load("validation/single-pass-validation-plan.json")
        truth = load("phase-truth.json")
        self.assertEqual(plan["canonical_successful_pass_budget"], 1)
        self.assertEqual(plan["successful_passes_used"], 0)
        self.assertFalse(plan["full_repository_suite"])
        self.assertFalse(plan["replay_permitted"])
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")

    def test_privacy_and_manifest_are_clean(self):
        privacy = load("validation/x1-staged-privacy.json")
        manifest = load("validation/x1-staged-manifest.json")
        self.assertEqual(len(privacy["pattern_classes"]), 5)
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["self_exclusions"]), 3)

    def test_documents_respect_word_cap_and_no_private_path(self):
        for path in PHASE.rglob("*"):
            if path.suffix.casefold() in {".md", ".html"}:
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(re.findall(r"\b\w+\b", text)), 6000, str(path.relative_to(ROOT)))
                self.assertIsNone(re.search(r"(?i)[A-Z]:\\Users\\", text), str(path.relative_to(ROOT)))

    def test_family_index_and_reflection_are_phase_scoped(self):
        receipt = load("reflection-remaster/reviewed-current-receipt.json")
        self.assertTrue((PHASE / "tooling" / "ghc-family-index.json").is_file())
        self.assertEqual(receipt["global_skill_changes"], 0)
        self.assertTrue(receipt["compatibility_preserved"])
        self.assertEqual(receipt["historical_surfaces_removed"], 0)


if __name__ == "__main__":
    unittest.main()

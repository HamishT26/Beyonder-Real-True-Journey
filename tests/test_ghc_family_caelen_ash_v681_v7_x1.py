from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "caelen-ash" / "v681-v7"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe"
BRANCH = "codex/GHC-Family/caelen-ash-v681-v7-full-tools"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class CaelenAshV681V7X1Tests(unittest.TestCase):
    def test_01_exact_source_branch_and_planning_only_lifecycle(self):
        self.assertEqual(subprocess.check_output(["git", "-C", ROOT, "rev-parse", "HEAD"], text=True).strip(), SOURCE)
        self.assertEqual(subprocess.check_output(["git", "-C", ROOT, "branch", "--show-current"], text=True).strip(), BRANCH)
        self.assertTrue(X1.is_dir())
        self.assertFalse((BASE / "x2").exists())
        self.assertFalse((BASE / "final").exists())

    def test_02_proposal_contract_and_four_labels(self):
        freeze = load(X1 / "new-proposal-freeze.json")
        self.assertEqual(freeze["proposal_count"], 60)
        self.assertEqual(freeze["declared_chain_after_if_committed"], 10130)
        self.assertFalse(freeze["x2_outcomes_present"])
        self.assertEqual(Counter(p["expected_disposition"] for p in freeze["proposals"]), Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}))
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition", "rejecting_mutations"}
        for proposal in freeze["proposals"]:
            self.assertTrue(required <= proposal.keys())
            self.assertEqual(len(proposal["rejecting_mutations"]), 5)

    def test_03_exact_source_novelty_audit(self):
        audit = load(X1 / "proposal-chain-audit.json")
        self.assertEqual(audit["audit_scope"]["proposal_json_paths_parsed"], 10075)
        self.assertEqual(audit["audit_scope"]["reachable_id_title_records"], 34861)
        self.assertEqual(audit["external_preflight_receipt_sha256"], "9c475b9eec50a0988d33fc79ba1341137fc3386b5edac7a0b7a9ad6f326c4a23")
        self.assertLess(audit["maximum_neighbor_score"], 0.78)
        self.assertEqual(audit["exact_title_collisions"], [])
        self.assertEqual(audit["quarantined_neighbors"], [])

    def test_04_startup_failures_are_retained_and_additive(self):
        flow = load(X1 / "method-flow-startup.json")
        self.assertEqual(len(flow["startup_failures"]), 18)
        self.assertFalse(flow["failure_erasure"])
        self.assertFalse(flow["recoveries_retroactively_promote_failure"])
        self.assertEqual(flow["current_after_startup"]["effective_negatives"], 54546)
        self.assertEqual(flow["current_after_startup"]["effective_methods"], 62933)
        self.assertEqual(flow["current_after_startup"]["failed_witnesses"], 26207)
        self.assertEqual(flow["current_after_startup"]["bounded_passing_witnesses"], 44755)

    def test_05_portfolio_is_frozen_not_executed(self):
        portfolio = load(X1 / "portfolio-freeze.json")
        self.assertEqual(len(portfolio["safe_now"]), 120)
        self.assertEqual(len(portfolio["owner_candidates"]), 80)
        self.assertEqual(len(portfolio["owner_clean_fix_refine"]), 100)
        self.assertEqual(len(portfolio["exact_approval"]), 20)
        self.assertEqual(len(portfolio["blocked"]), 10)
        self.assertEqual(len(portfolio["owner_skill_ideas"]), 20)
        self.assertEqual(len(portfolio["owner_runner_ideas"]), 10)
        self.assertEqual(portfolio["primary_pillar"], "GMUT Mind")
        self.assertTrue(all(not row["executed_in_x1"] for key in ("safe_now", "owner_candidates", "owner_clean_fix_refine", "exact_approval", "blocked") for row in portfolio[key]))

    def test_06_source_and_authority_boundaries(self):
        source = load(X1 / "source-verification.json")
        self.assertEqual(source["final"], SOURCE)
        self.assertEqual(source["manifest_entries_replayed"], 242)
        self.assertEqual(source["content_seal_entries_replayed"], 15)
        self.assertTrue(source["four_way_fresh_live_equal"])
        ledger = load(X1 / "official-primary-source-ledger.json")
        self.assertFalse(ledger["authority_conferred"])
        self.assertFalse(ledger["citations_are_observations"])
        self.assertEqual(ledger["real_data_rows"], 0)

    def test_07_identity_and_truth_are_bounded(self):
        identity = load(X1 / "identity-and-boundary.json")
        self.assertTrue(identity["relational_working_language_only"])
        self.assertEqual(identity["optional_pronouns"], "they/she")
        truth = load(X1 / "phase-truth.json")
        self.assertEqual(truth["execution_state"], "PLANNING_ONLY_X1")
        self.assertIsNone(truth["observed_outcomes"])
        self.assertFalse(truth["x2_started"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_08_privacy_scan_has_zero_confirmed_hits(self):
        privacy = load(VALIDATION / "x1-privacy-scan.json")
        self.assertEqual(privacy["confirmed_hits"], [])
        self.assertEqual(len(privacy["privacy_classes"]), 5)

    def test_09_staged_review_is_exact_and_has_no_x2_paths(self):
        staged = load(VALIDATION / "x1-staged-review.json")
        self.assertEqual(staged["lifecycle"], "planning_only_x1")
        self.assertEqual(staged["x2_paths"], [])
        self.assertEqual(staged["path_count"], len(staged["expected_paths"]))
        self.assertEqual(len(staged["expected_paths"]), len(set(staged["expected_paths"])))

    def test_10_normalized_lf_manifest_replays(self):
        manifest = load(VALIDATION / "x1-index-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = normalized(ROOT / entry["path"])
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_11_inherited_reviews_have_zero_credit(self):
        inherited = load(X1 / "inherited-revalidation-freeze.json")
        self.assertEqual(inherited["count"], 20)
        self.assertTrue(all(row["completion_credit"] == 0 for row in inherited["reviews"]))

    def test_12_route_is_held(self):
        route = load(X1 / "route-plan.json")
        self.assertTrue(route["terminal_gate_required"])
        self.assertTrue(route["successor_not_precontacted"])
        self.assertFalse(route["recipient_contacted"])


if __name__ == "__main__":
    unittest.main()

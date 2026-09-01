from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "eiren-kestrel" / "v682-v6"


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class EirenKestrelV682V6X1Tests(unittest.TestCase):
    def test_01_identity_is_relational_and_corrigible(self):
        identity = load("x1/identity-and-boundary.json")
        self.assertEqual(identity["name"], "Eiren Kestrel")
        self.assertTrue(identity["relational_working_language_only"])
        self.assertFalse(identity["consciousness_personhood_or_continuity_claimed"])
        self.assertEqual(identity["owner_rename_pause_redirect_stop_right"], "Hamish")

    def test_02_exact_source_anchors_and_manifest_replay(self):
        source = load("x1/source-verification.json")
        self.assertEqual(source["final"], "621ea4f832e9fda5549ed2f97dbfd9b539ef1f69")
        self.assertEqual(source["x1"], "2b27d47bea8c183f3c6c9a927c7daed79a51f5b3")
        self.assertEqual(source["evidence"], "6fe9faac17255942d9ca440aa5e21b70c1a5ceff")
        self.assertEqual(source["source"], "3cbffaa8b76a04a4c382545526658c2e8aaa256c")
        self.assertEqual(source["phase_commits"], 3)
        self.assertEqual(source["merges"], 0)
        self.assertTrue(source["clean"] and source["four_way_equal"])
        self.assertEqual(source["manifest_replay"]["mismatches"], 0)
        self.assertEqual(source["manifest_replay"]["total"], 232)
        self.assertEqual(source["content_seal_targets"], 10)

    def test_03_sixty_complete_proposal_contracts(self):
        freeze = load("x1/new-proposal-freeze.json")
        proposals = freeze["proposals"]
        self.assertEqual(len(proposals), 60)
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 60)
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
        for row in proposals:
            self.assertTrue(required.issubset(row))
            self.assertEqual(len(row["preregistered_rejecting_mutations"]), 5)
        counts = Counter(row["expected_disposition"] for row in proposals)
        self.assertEqual(
            counts,
            Counter(
                {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
            ),
        )

    def test_04_x1_contains_no_x2_outcome_or_completion_claim(self):
        freeze = load("x1/new-proposal-freeze.json")
        truth = load("x1/phase-truth.json")
        self.assertFalse(freeze["x2_outcomes_present"])
        self.assertEqual(truth["execution_state"], "PLANNING_ONLY_X1")
        self.assertIsNone(truth["observed_outcomes"])
        self.assertFalse(truth["x2_started"])

    def test_05_source_bounded_novelty_audit(self):
        audit = load("x1/proposal-chain-audit.json")
        self.assertEqual(audit["new_proposal_count"], 60)
        self.assertGreater(audit["audit_scope"]["proposal_json_paths_parsed"], 10000)
        self.assertGreater(audit["audit_scope"]["reachable_id_title_records"], 35000)
        self.assertEqual(audit["exact_title_collisions"], [])
        self.assertEqual(audit["quarantined_neighbors"], [])
        self.assertLess(
            audit["maximum_neighbor_score"], audit["quarantine_threshold_token_jaccard"]
        )
        self.assertFalse(
            audit["audit_scope"]["universal_declared_chain_materialization_claimed"]
        )

    def test_06_portfolio_floors_and_three_lenses(self):
        p = load("x1/portfolio-freeze.json")
        self.assertEqual(len(p["safe_now"]), 120)
        self.assertEqual(len(p["owner_candidates"]), 80)
        self.assertEqual(len(p["owner_clean_fix_refine"]), 100)
        self.assertEqual(len(p["owner_skill_ideas"]), 20)
        self.assertEqual(len(p["owner_runner_ideas"]), 10)
        self.assertEqual(len(p["exact_approval"]), 20)
        self.assertEqual(len(p["blocked"]), 10)
        self.assertEqual(len(p["owner_practice_lenses"]), 3)
        self.assertEqual(p["primary_pillar"], "GMUT Mind")
        self.assertIn(
            "exactly one zero-credit seed", p["successor_practice_recommendation"]
        )

    def test_07_exact_and_blocked_work_is_unexecuted(self):
        holds = load("x1/approval-hold-register.json")
        self.assertFalse(holds["executed"])
        self.assertEqual(holds["exact_approval_count"], 20)
        self.assertEqual(holds["blocked_count"], 10)

    def test_08_current_sources_are_vocabulary_only(self):
        ledger = load("x1/official-primary-source-ledger.json")
        self.assertEqual(ledger["real_data_rows"], 0)
        self.assertEqual(ledger["network_data_queries"], 0)
        self.assertFalse(ledger["authority_conferred"])
        self.assertFalse(ledger["citations_are_observations"])
        self.assertGreaterEqual(len(ledger["entries"]), 11)

    def test_09_method_flow_retains_every_startup_failure(self):
        flow = load("x1/method-flow-startup.json")
        self.assertEqual(len(flow["startup_failures"]), 15)
        self.assertEqual(
            len({row["failure_id"] for row in flow["startup_failures"]}), 15
        )
        self.assertFalse(flow["failure_erasure"])
        self.assertFalse(flow["recoveries_retroactively_promote_failure"])
        before = flow["activation_baseline"]
        after = flow["current_after_startup"]
        for key in (
            "effective_negatives",
            "effective_methods",
            "failed_witnesses",
            "bounded_passing_witnesses",
        ):
            self.assertEqual(after[key] - before[key], 15)

    def test_10_route_is_prospective_only(self):
        route = load("x1/route-plan.json")
        self.assertTrue(route["prepared_not_sent"])
        self.assertFalse(route["send_before_terminal_gate"])
        self.assertEqual(route["prospective_successor_exact_title"], "Elaren Kestrel")
        self.assertEqual(route["prospective_successor_phase"], "v682-v7")
        self.assertEqual(route["tavian_sol"], "ON_STANDBY")

    def test_11_manifest_replays_normalized_worktree_bytes(self):
        manifest = load("validation/x1-index-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(
            len({row["path"] for row in manifest["entries"]}), manifest["entry_count"]
        )
        for row in manifest["entries"]:
            data = normalized(ROOT / row["path"])
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(
                hashlib.sha256(data).hexdigest(), row["sha256"], row["path"]
            )

    def test_12_staged_review_and_exclusions_are_exact(self):
        manifest = load("validation/x1-index-manifest.json")
        review = load("validation/x1-staged-review.json")
        entries = {row["path"] for row in manifest["entries"]}
        exclusions = set(manifest["declared_self_exclusions"])
        self.assertFalse(entries & exclusions)
        self.assertEqual(set(review["expected_paths"]), entries | exclusions)
        self.assertEqual(review["path_count"], len(entries | exclusions))
        self.assertEqual(review["x2_paths"], [])

    def test_13_five_class_privacy_scan_has_zero_confirmed_hits(self):
        receipt = load("validation/x1-privacy-scan.json")
        self.assertEqual(receipt["class_count"], 5)
        self.assertEqual(receipt["confirmed_hit_count"], 0)
        self.assertEqual(receipt["confirmed_hits"], [])

    def test_14_terminal_verdict_remains_not_ready(self):
        truth = load("x1/phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()

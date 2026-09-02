from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v684-v4"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "0134e277a7f573e24e697037749d61d577163637"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(name: str):
    return json.loads((X1 / name).read_text(encoding="utf-8"))


class AurenV684V4X1Tests(unittest.TestCase):
    def test_activation_and_identity(self) -> None:
        activation = load("activation-intake.json")
        identity = load("identity-and-boundary.json")
        self.assertEqual(activation["source"], SOURCE)
        self.assertEqual(activation["work_mode"], "solo")
        self.assertTrue(activation["planning_only_x1"])
        self.assertTrue(identity["relational_working_language_only"])
        self.assertIn("not evidence of consciousness", identity["boundary"])
        self.assertIn("Maori authority", identity["boundary"])

    def test_source_verification(self) -> None:
        source = load("source-verification.json")
        self.assertEqual(source["exact_final"], SOURCE)
        self.assertTrue(source["clean"])
        self.assertTrue(source["local_equals_upstream_equals_tracking_equals_fresh_live"])
        self.assertEqual(source["divergence"], {"ahead": 0, "behind": 0})
        self.assertEqual(source["new_commit_count"], 3)
        self.assertEqual(source["merge_count"], 0)
        self.assertEqual(sum(v[0] for v in source["manifest_replay"].values()), 232)
        self.assertEqual(source["content_seal_replay"], [10, 10])

    def test_route_discontinuity_and_no_precontact(self) -> None:
        route = load("route-plan.json")
        self.assertEqual(route["historical_projection_owner"], "Vesper Arlen")
        self.assertFalse(route["historical_projection_activation_authority"])
        self.assertEqual(route["newest_live_owner"], "Auren Lark")
        self.assertTrue(route["route_discontinuity_retained"])
        self.assertEqual(route["prospective_successor"]["status"], "not_contacted_terminally_gated")

    def test_inherited_revalidation_zero_credit(self) -> None:
        data = load("inherited-revalidation-freeze.json")
        self.assertEqual(data["entry_count"], 60)
        self.assertEqual(len(data["entries"]), 60)
        self.assertTrue(all(row["current_novelty_credit"] == 0 for row in data["entries"]))
        self.assertTrue(all(row["automatic_completion_credit"] == 0 for row in data["entries"]))

    def test_new_proposals_and_expected_labels(self) -> None:
        data = load("new-proposal-freeze.json")
        self.assertTrue(data["planning_only"])
        self.assertEqual(data["entry_count"], 60)
        ids = [row["proposal_id"] for row in data["entries"]]
        self.assertEqual(len(ids), len(set(ids)))
        counts = Counter(row["expected_execution_disposition"] for row in data["entries"])
        self.assertEqual(set(counts), ALLOWED)
        self.assertEqual(counts, Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}))

    def test_rejecting_mutation_freeze(self) -> None:
        data = load("new-proposal-freeze.json")
        mutations = [m for row in data["entries"] for m in row["preregistered_rejecting_mutations"]]
        self.assertEqual(len(mutations), 300)
        self.assertEqual(len({m["mutation_id"] for m in mutations}), 300)
        self.assertTrue(all(m["expected_result"] == "reject_and_retain_zero_credit" for m in mutations))

    def test_proposal_chain(self) -> None:
        chain = load("proposal-chain-audit.json")
        self.assertEqual(chain["declared_chain_before"], 10850)
        self.assertEqual(chain["inherited_novelty_credit"], 0)
        self.assertEqual(chain["declared_chain_after_x1_freeze"], 10910)
        self.assertFalse(chain["universal_novelty_claim"])

    def test_portfolio_counts_and_caps(self) -> None:
        p = load("portfolio-freeze.json")
        self.assertEqual(p["counts"], {"safe_now": 120, "owner_candidates": 80, "successor_candidates": 20, "exact": 20, "blocked": 10})
        self.assertLessEqual(p["counts"]["safe_now"], p["caps"]["safe_now"])
        self.assertLessEqual(p["counts"]["owner_candidates"] + p["counts"]["successor_candidates"], p["caps"]["combined_candidates"])
        self.assertTrue(all(row["status"] == "held_unexecuted" for row in p["exact_approval_holds"]))
        self.assertTrue(all(row["status"] == "blocked_unexecuted" for row in p["blocked_holds"]))

    def test_skill_runner_plan(self) -> None:
        plan = load("skill-runner-plan.json")
        self.assertEqual(len(plan["owner_skill_ideas"]), 20)
        self.assertEqual(len(plan["owner_runner_ideas"]), 10)
        self.assertEqual(len(plan["successor_skill_ideas"]), 10)
        self.assertEqual(len(plan["successor_runner_ideas"]), 10)
        self.assertIn("not_authorized", plan["global_installation"])

    def test_clean_fix_refine_plan(self) -> None:
        plan = load("clean-fix-refine-plan.json")
        self.assertEqual(len(plan["owner_rows"]), 100)
        self.assertEqual(len(plan["successor_rows"]), 30)
        self.assertFalse(plan["deletion_authority"])
        self.assertFalse(plan["sibling_lane_mutation_authority"])

    def test_primary_sources_are_bounded(self) -> None:
        ledger = load("official-primary-source-ledger.json")
        self.assertEqual(ledger["source_count"], 7)
        self.assertTrue(ledger["citation_is_not_endorsement_or_artifact_validation"])
        self.assertTrue(all(row["url"].startswith("https://") for row in ledger["sources"]))
        self.assertTrue(all("No " in row["boundary"] for row in ledger["sources"]))

    def test_practice_lenses_are_not_qualifications(self) -> None:
        plan = load("profession-practice-plan.json")
        self.assertEqual(plan["primary_pillar"], "GMUT Mind")
        self.assertEqual(len(plan["owner_practices"]), 2)
        self.assertFalse(plan["employment_or_qualification_claim"])
        self.assertFalse(plan["real_practice_performed"])

    def test_method_failures_are_retained(self) -> None:
        flow = load("method-flow-startup.json")
        self.assertEqual(flow["phase_start_failure_count"], 19)
        self.assertEqual(len(flow["failures"]), 19)
        self.assertTrue(flow["failed_witnesses_are_zero_credit"])
        self.assertTrue(all(row["retained_zero_credit"] and not row["state_change"] for row in flow["failures"]))
        self.assertEqual(flow["activation_overlay_negatives"], flow["inherited_sealed_negatives"] + 19)

    def test_phase_truth_keeps_every_gate(self) -> None:
        truth = load("phase-truth.json")
        self.assertEqual(truth["state"], "PLANNING_ONLY_X1_FROZEN")
        self.assertEqual(set(truth["allowed_labels"]), ALLOWED)
        self.assertFalse(truth["outcomes_claimed"])
        for key, value in truth.items():
            if key in {"schema", "owner", "phase", "state", "terminal_verdict", "allowed_labels", "outcomes_claimed"}:
                continue
            if isinstance(value, bool):
                self.assertFalse(value, key)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_privacy_scan(self) -> None:
        scan = json.loads((VALIDATION / "x1-privacy-scan.json").read_text(encoding="utf-8"))
        self.assertEqual(scan["confirmed_hit_count"], 0)
        self.assertTrue(scan["bounded_not_complete_privacy_assurance"])

    def test_manifest_replays_worktree_bytes(self) -> None:
        manifest = json.loads((VALIDATION / "x1-index-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertGreaterEqual(manifest["entry_count"], 20)
        for row in manifest["entries"]:
            data = (ROOT / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_strict_x1_before_x2(self) -> None:
        self.assertFalse((BASE / "x2").exists())
        self.assertFalse((BASE / "final").exists())
        self.assertFalse((BASE / "closeout").exists())

    def test_overview_carries_boundaries(self) -> None:
        text = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
        self.assertIn("planning only", text)
        self.assertIn("relational working language only", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("Same-owner software or synthetic evidence is not independent reproduction", text)


if __name__ == "__main__":
    unittest.main()

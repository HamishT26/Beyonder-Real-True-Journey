import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5-2-remaster"
SOURCE = "2bb6aa2d5e8003c4cb522f798d59e7b7f123742c"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class EirenV651V5RemasterX1Tests(unittest.TestCase):
    def test_source_and_identity_boundaries(self):
        source = load("source/source-truth.json")
        self.assertEqual(source["source_head"], SOURCE)
        identity = load("identity/relational-identity.json")
        self.assertIn("Relational working language only", identity["identity_boundary"])
        self.assertEqual(identity["pronouns"], "she/they")

    def test_exactly_thirty_complete_proposals(self):
        packet = load("preregistration/proposals.json")
        self.assertEqual(packet["inherited_frozen_rows"], 1000)
        self.assertEqual(packet["new_proposal_count"], 30)
        self.assertEqual(packet["frozen_rows_after_x1"], 1030)
        self.assertEqual(len(packet["proposals"]), 30)
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertEqual(len({row["proposal_id"] for row in packet["proposals"]}), 30)
        self.assertTrue(all(required <= set(row) for row in packet["proposals"]))

    def test_expected_outcome_vocabulary(self):
        packet = load("preregistration/proposals.json")
        self.assertEqual(packet["expected_outcomes"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual({row["expected_disposition"] for row in packet["proposals"]}, {"completed", "represented", "open_gap", "exact_gate"})

    def test_x1_has_no_x2_implementation_or_outcome(self):
        truth = load("truth/x1-phase-truth.json")
        self.assertTrue(truth["strict_x1_before_x2"])
        self.assertEqual(truth["x2_implementations"], 0)
        self.assertEqual(truth["observed_core_outcomes"], 0)
        self.assertEqual(truth["cli_siblings_spawned"], 0)

    def test_portfolio_floors_and_caps(self):
        plan = load("portfolios/x1-portfolio-plan.json")
        self.assertEqual({key: len(plan[key]) for key in ("safe_now", "candidate", "skill_ideas", "runner_ideas", "clean_fix_refine")}, {"safe_now": 40, "candidate": 30, "skill_ideas": 20, "runner_ideas": 10, "clean_fix_refine": 40})
        self.assertEqual(plan["caps"], {"safe_candidate_per_subphase": 1000, "skills_per_subphase": 200, "runners_per_subphase": 200})
        self.assertEqual(plan["x1_implementation_count"], 0)

    def test_meta_toolbox_is_only_preregistered(self):
        contract = load("tooling/meta-tool-box-build-contract.json")
        self.assertEqual(contract["skill_name"], "ghc-family-meta-tool-box")
        self.assertEqual(contract["runner_name"], "ghc_family_meta_tool_box.py")
        self.assertEqual(contract["x1_state"], "preregistered_not_built")

    def test_immediate_route_only(self):
        issue = load("workflow/long-route-issue.json")
        self.assertEqual(issue["immediate_route_unambiguous"], {"target": "Elaren Kestrel", "phase": "v651-v6"})
        self.assertEqual(issue["long_route_state"], "candidate_requires_later_sequential_normalization")
        request = load("workflow/workflow-plan-request.json")
        self.assertEqual(request["route"]["phase_assignments"], [{"phase": "v651-v6", "seat": "Elaren Kestrel"}])
        self.assertEqual(len(request["route"]["future_identity_placeholders"]), 8)
        compatibility = load("workflow/workflow-plan-runner-compatible-request.json")
        self.assertEqual(compatibility["live_overrides_not_validated_by_legacy_runner"]["commit_cap"]["total"], 6)

    def test_held_approvals_remain_unexecuted(self):
        approvals = load("approvals/held-packets.json")
        self.assertEqual(len(approvals["exact_approval"]), 10)
        self.assertEqual(len(approvals["blocked"]), 5)
        self.assertTrue(all(not row["executed"] for lane in ("exact_approval", "blocked") for row in approvals[lane]))

    def test_primary_focus_preserves_all_pillars(self):
        focus = load("focus/primary-focus.json")
        self.assertEqual(focus["primary_pillar"], "THOS Body")
        self.assertEqual(set(focus["visible_pillars"]), {"GMUT Mind", "THOS Body", "Freed ID and CBR Heart"})
        self.assertIn("digital preservation", focus["bounded_human_practice"])

    def test_stage20_abstains(self):
        self.assertEqual(load("truth/x1-phase-truth.json")["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_novelty_and_negative_accounting(self):
        novelty = load("provenance/semantic-novelty-audit.json")
        self.assertEqual(novelty["inherited_rows_compared"], 1000)
        self.assertEqual(novelty["new_rows_compared"], 30)
        self.assertEqual(novelty["exact_title_collisions"], [])
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual(negatives["effective_after_x1"], 7099)
        self.assertEqual(negatives["failures_erased"], 0)

    def test_version_and_route_receipts(self):
        environment = load("environment/environment-version-receipt.json")
        self.assertEqual(environment["codex_cli"], "0.144.5")
        self.assertTrue(environment["versions_verified_only"])
        route = load("orchestration/x1-phase-state.json")
        self.assertFalse(route["x2_started"])
        self.assertEqual(route["terminal_route"], "prepared_not_sent")


if __name__ == "__main__":
    unittest.main()

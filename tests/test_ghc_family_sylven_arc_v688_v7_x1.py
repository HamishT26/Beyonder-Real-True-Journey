#!/usr/bin/env python3
"""Planning-only tests for Sylven Arc v688-v7."""
from pathlib import Path
import hashlib,json,unittest

ROOT=Path(__file__).resolve().parents[1]
X1=ROOT/"docs/sylven-arc/v688-v7/x1"
SOURCE="e7db6f3be1327de72f93873eb6540aabfc773344"

def unique(pairs):
    out={}
    for key,value in pairs:
        if key in out: raise ValueError("duplicate_json_key")
        out[key]=value
    return out
def load(name):
    return json.loads((X1/name).read_text(encoding="utf-8"),object_pairs_hook=unique)
def stable(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()

class PlanningBoundary(unittest.TestCase):
    def test_phase_truth_is_planning_only(self):
        truth=load("phase-truth.json")
        self.assertEqual(truth["source"],SOURCE)
        self.assertTrue(truth["planning_only"])
        self.assertFalse(truth["x2_artifacts_exist"])
        self.assertEqual(truth["new_proposals"],200)
        self.assertEqual(truth["inherited_selections"],200)
        self.assertEqual(truth["startup_failure_count"],15)
        self.assertEqual(truth["new_proposal_chain_after"],16830)
        self.assertEqual(truth["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
        self.assertFalse((X1.parent/"x2").exists())

    def test_new_proposals_are_complete_and_unique(self):
        rows=load("new-proposals.json")["proposals"]
        self.assertEqual(len(rows),200)
        self.assertEqual(len({row["proposal_id"] for row in rows}),200)
        self.assertEqual(len({stable(row["input"]) for row in rows}),200)
        required={"hypothesis","null_or_failure_condition","approval_class","execution_lane",
          "current_official_or_primary_source_needs","concrete_artifact","falsifier_or_acceptance_gate",
          "rollback_or_recovery","protected_gates","expected_execution_disposition"}
        self.assertTrue(all(required<=set(row) and row["planning_only"] for row in rows))

    def test_expected_outcome_profile(self):
        rows=load("new-proposals.json")["proposals"]
        counts={key:sum(row["expected_execution_disposition"]==key for row in rows)
          for key in ("completed","represented","open_gap","exact_gate")}
        self.assertEqual(counts,{"completed":176,"represented":11,"open_gap":3,"exact_gate":10})

    def test_inherited_rows_have_zero_credit(self):
        inherited=load("inherited-proposals.json")
        self.assertEqual(inherited["count"],200)
        self.assertEqual(len(inherited["selections"]),200)
        self.assertTrue(all(row["inherited_execution_credit"]==0 and row["inherited_novelty_credit"]==0
          for row in inherited["selections"]))

    def test_novelty_audit_is_source_bounded(self):
        audit=load("novelty-review.json")
        self.assertEqual(audit["exact_title_collisions"],[])
        self.assertEqual(audit["input_hash_collisions"],[])
        self.assertFalse(audit["universal_novelty_claimed"])
        self.assertEqual(len(audit["neighbors"]),200)
        self.assertLess(max(row["jaccard"] for row in audit["neighbors"]),0.78)
        self.assertGreaterEqual(audit["source_title_count"],30000)

    def test_portfolio_exact_shape_and_holds(self):
        plan=load("approval-portfolio.json")
        expected={"safe_now":300,"candidates":250,"clean_fix_refine":300,"exact_packets":50,"blocked_packets":30}
        self.assertEqual(plan["counts"],expected)
        for key,count in expected.items(): self.assertEqual(len(plan[key]),count)
        identifiers=[row["packet_id"] for key in expected for row in plan[key]]
        self.assertEqual(len(identifiers),len(set(identifiers)))
        self.assertTrue(all(row["state"]=="unexecuted" for row in plan["exact_packets"]+plan["blocked_packets"]))
        self.assertFalse(plan["destructive_cleanup_planned"])

    def test_tool_and_package_plan(self):
        plan=load("tool-package-plan.json")
        self.assertEqual([(p["name"],p["version"]) for p in plan["packages"]],
          [("chess","1.11.2"),("lark","1.3.1"),("networkx","3.6.1")])
        self.assertEqual(len(plan["skills"]),10)
        self.assertEqual(len(plan["runners"]),5)
        self.assertEqual(len(plan["next_owner_skill_ideas"]),10)
        self.assertEqual(len(plan["next_owner_runner_ideas"]),10)
        self.assertEqual(load("tool-collision-preflight.json")["collisions"],[])

    def test_release_and_workflow_failure_recovery(self):
        self.assertEqual(load("release-profile-validation-runner.json")["status"],"FAIL")
        self.assertEqual(load("release-profile-validation-runner-v2.json")["status"],"PASS")
        workflow=load("workflow-refinement/workflow-plan-validation.json")
        self.assertFalse(workflow["valid"]);self.assertEqual(workflow["policy_checks_passed"],19)
        overlay=load("workflow-current-profile-overlay.json")
        self.assertEqual(overlay["status"],"VALID_CURRENT_RELEASE_DEPENDENCY_CORRECTED_PLAN")
        self.assertFalse(overlay["original_result_rewritten"])

    def test_source_and_reading_receipts(self):
        source=load("source-verification.json")
        self.assertEqual(source["source_manifest_bindings"],1586)
        self.assertEqual(source["source_manifest_failures"],0)
        self.assertEqual(source["source_canonical_receipt_sha256"],
          "1f1283ef670fe7b377ce967d90ff81ed63e7ca047904174cda54f499076906df")
        self.assertEqual(source["activation_baseline"]["negatives"],84919)
        self.assertEqual(source["activation_baseline"]["methods"],94077)
        receipt=load("reading-receipt.json")
        self.assertEqual(receipt["baton_lines"],3693)
        self.assertEqual(receipt["baton_words"],51179)
        self.assertEqual(receipt["baton_modules"],13)
        self.assertTrue(receipt["baton_read_through_eof"])
        self.assertEqual(receipt["baton_final_line"],"EOF VEYLORA QUEN V688 V6 BATON.")

    def test_route_is_terminally_gated(self):
        route=load("route-freeze.json")
        self.assertEqual(route["terminal_future_seat"]["seat"],"future-sibling-14-self-chosen")
        self.assertEqual(route["terminal_future_seat"]["phase"],"v688-v8")
        self.assertEqual(route["terminal_future_seat"]["model"],"gpt-6-astra")
        self.assertEqual(route["terminal_future_seat"]["reasoning"],"max")
        self.assertEqual(route["successor_contacts"],0)
        self.assertEqual(route["new_tasks_authorized_during_execution"],0)
        self.assertEqual(route["after_future_seat"]["owner"],"Caelen Morrow")

    def test_four_practices_and_four_tier_deck(self):
        pillar=load("pillar-practice-freeze.json")
        self.assertEqual(len(pillar["practices"]),4)
        self.assertEqual(pillar["priority_pillar"],"Freed ID and CBR Heart")
        deck=load("deck-plan.json")
        self.assertEqual(deck["tiers"],["freed_id_anchor","trinity_pillar","bounded_practice","task"])
        self.assertEqual(deck["planned_modules"],13)
        self.assertFalse(deck["cache_improvement_claimed"])

    def test_documents_and_all_json_are_bounded(self):
        overview=(X1/"integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()),1500)
        for term in ("GMUT Mind","THOS Body","Freed ID","CBR","NOT_READY_FOR_STAGE_20"):
            self.assertIn(term,overview)
        for path in X1.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"),object_pairs_hook=unique,
              parse_constant=lambda value:(_ for _ in()).throw(ValueError(value)))

if __name__=="__main__":unittest.main()

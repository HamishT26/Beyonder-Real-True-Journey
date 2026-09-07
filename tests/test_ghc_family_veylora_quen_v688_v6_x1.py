"""Structural tests for the immutable planning boundary; no execution evaluator."""
from pathlib import Path
import hashlib,json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
X1=ROOT/"docs/veylora-quen/v688-v6/x1"
def read(name):return json.loads((X1/name).read_text(encoding="utf-8"))
class PlanningBoundary(unittest.TestCase):
    def test_01_exact_source_and_corrected_name(self):
        t=read("phase-truth.json")
        self.assertEqual((t["owner"],t["phase"],t["source"]),("Veylora Quen","v688-v6","d72ba9a9ebefc1e18cb89d2c8b90c661ba8aaf14"))
        self.assertEqual(t["execution_credit"],0)
        self.assertTrue(t["planning_only"])
    def test_02_proposal_inventory(self):
        p=read("new-proposals.json")
        self.assertEqual((p["chain_before"],p["chain_after"],p["count"]),(16430,16630,200))
        rows=p["proposals"]
        self.assertEqual(len({x["proposal_id"] for x in rows}),200)
        self.assertEqual(len({json.dumps(x["input"],sort_keys=True) for x in rows}),200)
        self.assertEqual(len({x["operation"] for x in rows}),20)
    def test_03_complete_frozen_expectations(self):
        for p in read("new-proposals.json")["proposals"]:
            self.assertIs(type(p["expected_acceptance"]),bool)
            self.assertEqual(p["expected_acceptance"],p["expected_error"] is None)
            self.assertIn(p["expected_execution_disposition"],["completed","represented","open_gap","exact_gate"])
            self.assertIn("expected_value",p)
            self.assertEqual(p["input"]["operation"],p["operation"])
            self.assertEqual(p["execution_credit"],0)
    def test_04_inherited_credit_and_binding(self):
        p=read("inherited-proposals.json")
        self.assertEqual(len(p["selections"]),200)
        for x in p["selections"]:
            self.assertEqual(x["inherited_execution_credit"],0)
            self.assertEqual(x["inherited_novelty_credit"],0)
            self.assertTrue(x["source_proposal"]["proposal_id"].startswith("EC6885-"))
    def test_05_portfolios_are_plans(self):
        p=read("approval-portfolio.json");ids=[]
        for k,n in {"safe_now":300,"candidates":250,"clean_fix_refine":300,"exact_packets":50,"blocked_packets":30}.items():
            self.assertEqual(len(p[k]),n)
            ids += [x.get("task_id",x.get("packet_id")) for x in p[k]]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertFalse(p["destructive_cleanup_planned"])
        self.assertTrue(all(x["state"]=="unexecuted" for k in ["exact_packets","blocked_packets"] for x in p[k]))
    def test_06_no_x2_artifacts(self):
        self.assertFalse((X1.parent/"x2").exists())
        self.assertFalse((ROOT/"scripts/ghc_family_firmware_records_core.py").exists())
        self.assertEqual(read("phase-truth.json")["canonical_invocations"],0)
    def test_07_packages_frozen_before_installation(self):
        p=read("tool-package-plan.json")
        self.assertEqual(sum(x["direct"] for x in p["packages"]),3)
        self.assertEqual(len(p["packages"]),7)
        for x in p["packages"]:
            self.assertRegex(x["sha256"],r"^[a-f0-9]{64}$")
            self.assertTrue(x["url"].startswith("https://files.pythonhosted.org/"))
            self.assertTrue(x["wheel"].endswith(".whl"))
        self.assertTrue(p["planning_only"])
    def test_08_tool_collision_and_budget(self):
        p=read("tool-package-plan.json")
        self.assertEqual((len(p["skills"]),len(p["runners"])),(10,5))
        self.assertEqual(len(p["next_owner_skill_ideas"]),10)
        self.assertEqual(len(p["next_owner_runner_ideas"]),10)
        self.assertEqual(read("tool-collision-preflight.json")["collisions"],[])
    def test_09_source_recovery_is_not_erased(self):
        s=read("source-verification.json")
        self.assertEqual(s["source_corrected_truth"]["failed_canonical_success_credit"],0)
        self.assertEqual(s["latest_external_route_release"]["route_state"],"CREATED_ONCE_ACKNOWLEDGED_ACTIVE")
        self.assertEqual(s["retained_external_route_gap"]["route_state"],"OPEN_ROUTE_GAP")
        self.assertFalse(s["prior_canonical_replayed"])
        self.assertEqual(s["activation_baseline"]["negatives"],84371)
    def test_10_route_remains_terminally_gated(self):
        r=read("route-freeze.json")
        self.assertEqual((r["current_next"]["owner"],r["current_next"]["phase"]),("Sylven Arc","v688-v7"))
        self.assertEqual(r["after_sylven"]["creation_controller"],"Sylven Arc")
        self.assertEqual(r["new_tasks_authorized_here"],0)
        self.assertEqual(r["successor_contacts"],0)
    def test_11_novelty_screen_has_no_quarantine(self):
        n=read("novelty-review.json")
        self.assertEqual(n["exact_title_collisions"],[])
        self.assertEqual(n["input_hash_collisions"],[])
        self.assertEqual(n["source_parse_failures"],[])
        self.assertTrue(all(x["jaccard"]<n["threshold"] for x in n["neighbors"]))
        self.assertFalse(n["universal_novelty_claimed"])
    def test_12_source_reads_and_authority_boundaries(self):
        r=read("reading-receipt.json")
        self.assertEqual((r["baton_modules"],r["source_manifest_bindings"],r["source_manifest_failures"]),(13,1304,0))
        self.assertTrue(r["baton_read_through_eof"])
        for p in read("new-proposals.json")["proposals"]:
            self.assertFalse(p["external_credit"])
            self.assertIn("stage20",p["protected_gates"])
            self.assertIn("maori_authority",p["protected_gates"])
        profile=read("profile-contract.json")
        self.assertEqual(profile["image_byte_limit"],4096)
        self.assertIn("refuse address wrap",profile["ihex_profile"])
if __name__=="__main__": unittest.main()

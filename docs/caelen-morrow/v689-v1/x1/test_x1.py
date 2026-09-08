import json,pathlib,unittest
R=pathlib.Path(__file__).resolve().parent
def load(name): return json.loads((R/name).read_text(encoding="utf-8"))
class Plan(unittest.TestCase):
 def test_counts(self): self.assertEqual(len(load("new-proposals.json")["proposals"]),200)
 def test_unique(self): self.assertEqual(len({r["proposal_id"] for r in load("new-proposals.json")["proposals"]}),200)
 def test_inherited_zero(self): self.assertEqual(load("inherited-proposals.json")["execution_credit"],0)
 def test_planning_only(self): self.assertFalse(load("phase-truth.json")["implementation_executed"])
 def test_novelty(self): self.assertEqual(load("novelty-review.json")["exact_collisions"],[])
 def test_tools(self): self.assertEqual((len(load("tool-plan.json")["skills"]),len(load("tool-plan.json")["runners"])),(10,5))
 def test_portfolio(self): self.assertEqual([len(load("approval-portfolio.json")[k]) for k in ["safe_now","candidates","clean_fix_refine","exact_packets","blocked_packets"]],[300,250,300,50,30])
 def test_dispositions(self): self.assertEqual({r["expected"]["disposition"] for r in load("new-proposals.json")["proposals"]},{"completed","represented","open_gap","exact_gate"})
 def test_route(self): self.assertEqual(load("route-freeze.json")["send_count"],0); self.assertEqual(load("route-freeze.json")["next_phase"],"v689-v2")
 def test_packages(self): self.assertFalse(load("tool-plan.json")["installation_executed"]); self.assertEqual(len(load("tool-plan.json")["packages"]["direct"]),3)
 def test_eof(self): self.assertTrue(load("reading-receipt.json")["baton"]["read_through_eof"])
 def test_retained(self):
  flow=load("method-flow-startup.json"); self.assertEqual(len(flow["witnesses"]),2*len(flow["methods"]))
if __name__=="__main__": unittest.main()

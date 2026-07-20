"""X2 evidence tests for Sable Rook v651-v1."""
import json,unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"docs/sable-rook/v651-v1"
def load(rel): return json.loads((ROOT/rel).read_text(encoding="utf-8"))
class TestV651V1X2(unittest.TestCase):
    def test_outcomes(self):
        o=load("outcomes/outcome-ledger.json")["outcomes"]
        self.assertEqual(len(o),20)
        self.assertEqual(Counter(x["observed_outcome"] for x in o),Counter(completed=14,represented=4,open_gap=1,exact_gate=1))
    def test_all_mutations_execute_and_reject(self):
        m=load("validation/mutation-execution.json")
        self.assertEqual((m["executed"],m["rejected_or_quarantined"]),(100,100))
        self.assertTrue(all(x["passed"] for x in m["mutations"]))
    def test_surface_receipts(self):
        for p in load("preregistration/proposals.json")["proposals"]:
            r=load(f"surfaces/{p['slug']}/bounded-receipt.json")
            self.assertTrue(r["valid"]); self.assertEqual(r["mutation_rejections"],5)
    def test_zero_row_and_proxies(self):
        alma=load("empirical/alma-zero-row-readiness.json")
        self.assertTrue(all(v==0 for v in alma["zero_real_world_counts"].values()))
        for rel in ["thos/baggage-reconciliation-proxy.json","thos/ground-deicing-proxy.json","freed-id/openid-ciba-profile.json","freed-id/openid4vp-dcql-profile.json"]:
            self.assertEqual(load(rel)["outcome"],"represented")
    def test_authority_gate(self):
        c=load("cbr/airport-authority-matrix.json")
        self.assertEqual(c["outcome"],"exact_gate"); self.assertTrue(all(v==0 for v in c["zero_real_world_counts"].values()))
    def test_portfolios(self):
        p=load("portfolios/expanded-portfolio-execution.json")
        self.assertEqual(p["completed_counts"],{"safe_now":40,"candidate":30,"skills":20,"runners":10,"clean_fix_refine":40})
    def test_skill_and_runner_use(self):
        s=load("validation/skill-execution.json"); r=load("validation/runner-execution.json")
        self.assertTrue(s["valid"]); self.assertEqual((s["validated"],s["smoke_used"]),(20,20))
        self.assertTrue(r["valid"]); self.assertEqual(r["invoked"],10)
    def test_negative_and_gate_truth(self):
        t=load("truth/evidence-phase-truth.json")
        self.assertEqual(t["effective_negatives"],6548); self.assertEqual(t["negative_erasures"],0)
        self.assertEqual((t["effective_open_gaps"],t["effective_exact_gates"]),(51,52))
    def test_terminal_abstention(self):
        t=load("truth/evidence-phase-truth.json")
        self.assertEqual(t["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
        self.assertEqual(t["terminal_route"],"PREPARED_NOT_SENT")
        self.assertFalse(t["independent_reproduction_claimed"])
if __name__=="__main__": unittest.main()

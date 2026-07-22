"""Combined closeout tests for Ilyra Fen v651-v8."""
import json, unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]; ROOT=REPO/"docs/ilyra-fen/v651-v8"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
class TestV651V8Closeout(unittest.TestCase):
    def test_final_truth(self):
        d=load("final/phase-truth.json"); self.assertEqual(d["outcome_counts"],{"completed":23,"represented":5,"open_gap":1,"exact_gate":1}); self.assertEqual(d["effective_negatives"],7744); self.assertEqual(d["effective_open_gaps"],60); self.assertEqual(d["effective_exact_gates"],61); self.assertEqual(d["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
    def test_receipts(self):
        self.assertEqual(load("final/closeout-receipt.json")["state"],"closeout_candidate_complete"); self.assertEqual(load("final/seal-receipt.json")["state"],"seal_candidate_complete"); self.assertEqual(load("final/final-receipt.json")["canonical_exact_final_state"],"pending_postcommit_single_pass")
    def test_route_and_seats(self):
        r=load("route/final-route-state.json"); self.assertEqual(r["delivery_state"],"PREPARED_NOT_SENT"); self.assertFalse(r["successor_exactly_resolved"]); self.assertEqual(r["messages_sent"],0)
        s=load("provenance/future-cli-x2-invariant.json"); self.assertEqual((s["named_count"],s["created_count"],s["launched_count"]),(0,0,0))
    def test_baton_range(self):
        words=len((ROOT/"handoffs/v651-v8-route-clarification-baton.md").read_text(encoding="utf-8").split()); self.assertGreaterEqual(words,10000); self.assertLessEqual(words,100000)
    def test_document_caps(self):
        for path in ROOT.rglob("*.md"):
            if path.name=="v651-v8-route-clarification-baton.md": continue
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()),6000,path)
    def test_future_and_full_suite_boundaries(self):
        d=load("final/final-receipt.json"); self.assertFalse(d["full_repository_suite_run"]); self.assertFalse(d["independent_reproduction_claimed"]); self.assertEqual(d["future_seats_launched"],0)
if __name__=="__main__": unittest.main()

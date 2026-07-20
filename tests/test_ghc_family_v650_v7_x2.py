"""Bounded x2 evidence tests for Eiren Kestrel v650-v7."""
import json
import unittest
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/"docs/eiren-kestrel/v650-v7"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))

class TestV650V7X2(unittest.TestCase):
    def test_outcomes(self):
        d=load("outcomes/outcome-ledger.json")
        self.assertEqual(d["counts"],{"completed":14,"represented":4,"open_gap":1,"exact_gate":1})
        self.assertEqual(d["count"],20)
        self.assertTrue(all(r["accepted"] for r in d["outcomes"]))
    def test_mutations(self):
        d=load("validation/mutation-execution.json")
        self.assertEqual(d["count"],100); self.assertEqual(d["rejected"],100); self.assertTrue(d["all_rejected"])
    def test_skills_and_runners(self):
        s=load("validation/skill-validation.json"); r=load("validation/runner-validation.json")
        self.assertEqual(s["count"],20); self.assertTrue(all(x["smoke_accepted"] for x in s["skills"])); self.assertTrue(all(not x["global_install"] for x in s["skills"]))
        self.assertEqual(r["count"],10); self.assertTrue(all(x["all_accepted"] for x in r["runners"]))
        for row in s["skills"]:
            p=REPO/row["skill_path"]; self.assertTrue((p/"SKILL.md").is_file()); self.assertTrue((p/"agents/openai.yaml").is_file())
    def test_portfolios(self):
        d=load("portfolios/expanded-portfolio-execution.json")
        self.assertEqual(d["counts"],{"safe_now":40,"candidate":30,"skills":20,"runners":10,"clean_fix_refine":40}); self.assertTrue(d["all_resolved"])
    def test_zero_row_proxy_and_authority(self):
        z=load("empirical/4xmm-dr14-zero-row.json"); self.assertEqual(z["rows"],0); self.assertEqual(z["downloads"],0); self.assertEqual(z["likelihoods"],0)
        t=load("truth/evidence-phase-truth.json"); self.assertEqual(t["terminal_verdict"],"NOT_READY_FOR_STAGE_20"); self.assertFalse(t["independent_reproduction_claimed"])
        self.assertEqual(t["effective_open_gaps"],49); self.assertEqual(t["effective_exact_gates"],50)
    def test_method_failures_and_privacy(self):
        m=load("method-flow/method-flow-summary.json")["counts"]; self.assertGreaterEqual(m["witness_results"]["fail"],17); self.assertGreaterEqual(m["witness_results"]["pass"],16)
        p=load("validation/evidence-staged-privacy.json"); self.assertEqual(p["confirmed_hit_count"],0)

if __name__=="__main__": unittest.main()

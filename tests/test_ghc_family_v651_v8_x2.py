"""Bounded x2 evidence tests for Ilyra Fen v651-v8."""
import json, unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]; ROOT=REPO/"docs/ilyra-fen/v651-v8"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
class TestV651V8X2(unittest.TestCase):
    def test_outcomes(self):
        d=load("outcomes/x2-outcome-ledger.json"); self.assertEqual(d["count"],30); self.assertEqual(d["counts"],{"completed":23,"represented":5,"open_gap":1,"exact_gate":1}); self.assertTrue(all(x["accepted"] for x in d["outcomes"])); self.assertEqual(set(d["counts"]),{"completed","represented","open_gap","exact_gate"})
    def test_mutations(self):
        d=load("validation/mutation-execution.json"); self.assertEqual(d["count"],150); self.assertEqual(d["rejected"],150); self.assertTrue(d["all_rejected"])
    def test_skills(self):
        d=load("validation/skill-validation.json"); self.assertEqual(d["count"],20); self.assertTrue(d["valid"]); self.assertEqual(d["global_install_count"],0)
        for row in d["skills"]: self.assertTrue((REPO/row["skill_path"]/"SKILL.md").is_file()); self.assertTrue((REPO/row["skill_path"]/"agents/openai.yaml").is_file()); self.assertTrue(row["smoke_accepted"]); self.assertTrue(row["reject_witness"])
    def test_runners(self):
        d=load("validation/runner-validation.json"); self.assertEqual(d["count"],12); self.assertTrue(d["valid"]); self.assertTrue(all(x["used"] for x in d["runners"]))
    def test_portfolios(self):
        d=load("portfolios/expanded-portfolio-execution.json"); self.assertEqual(d["counts"],{"safe_now":40,"candidate":30,"skills":20,"runners":12,"clean_fix_refine":40}); self.assertTrue(d["all_resolved"]); self.assertFalse(d["unsafe_work_manufactured"])
    def test_truth(self):
        d=load("truth/evidence-phase-truth.json"); self.assertEqual(d["effective_negatives"],7736); self.assertEqual(d["effective_open_gaps"],60); self.assertEqual(d["effective_exact_gates"],61); self.assertEqual(d["terminal_verdict"],"NOT_READY_FOR_STAGE_20"); self.assertFalse(d["independent_reproduction_claimed"]); self.assertEqual(d["full_suite_state"],"not_run_by_non_eiren_owner")
    def test_zero_proxy_authority(self):
        z=load("empirical/askap-racs-mid-zero-row.json"); self.assertEqual(z["downloads"],0); self.assertEqual(z["catalogue_rows"],0); self.assertEqual(z["likelihood_calls"],0)
        c=load("cbr/radio-astronomy-authority-matrix.json"); self.assertEqual(c["real_decisions"],0); self.assertFalse(c["maori_authority_claimed"])
        s=load("provenance/future-cli-x2-invariant.json"); self.assertEqual((s["named_count"],s["created_count"],s["launched_count"]),(0,0,0))
    def test_method_privacy_and_report(self):
        m=load("method-flow/method-flow-summary.json")["counts"]; self.assertGreaterEqual(m["witness_results"]["fail"],14); self.assertGreaterEqual(m["witness_results"]["pass"],14)
        self.assertEqual(load("validation/evidence-staged-privacy.json")["confirmed_hit_count"],0); self.assertTrue((ROOT/"reports/accessible-static-report.html").is_file())
if __name__=="__main__": unittest.main()

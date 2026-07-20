"""Bounded closeout packet tests for Eiren Kestrel v650-v7."""
import json
import unittest
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/"docs/eiren-kestrel/v650-v7"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))

class TestEirenV650V7Closeout(unittest.TestCase):
    def test_final_truth(self):
        d=load("final/phase-truth.json")
        self.assertEqual(d["outcomes"],{"completed":14,"represented":4,"open_gap":1,"exact_gate":1})
        self.assertEqual(d["effective_negatives"],6311)
        self.assertEqual((d["effective_open_gaps"],d["effective_exact_gates"]),(49,50))
        self.assertEqual(d["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
    def test_full_suite_truth(self):
        f=load("validation/full-repository-suite-failed.json"); r=load("validation/full-repository-suite-recovery.json")
        self.assertEqual((f["tests_run"],f["failures"],f["successful_pass_credit"]),(2191,6,0))
        self.assertEqual((r["tests_run"],r["failures"],r["errors"],r["skipped"]),(2185,0,0,0))
        self.assertTrue(r["successful"]); self.assertFalse(r["post_success_replay"])
        self.assertEqual((r["inherited_exclusion_count"],r["recovery_exclusion_count"]),(14,6))
    def test_method_flow(self):
        m=load("method-flow/method-flow-summary.json")["counts"]
        self.assertEqual(m["methods"],28); self.assertEqual(m["witness_results"],{"fail":29,"pass":28})
        self.assertEqual(m["states"]["preferred"],28)
    def test_documents_and_route(self):
        d=load("validation/final-document-cap-receipt.json"); r=load("orchestration/final-phase-state.json")
        self.assertTrue(d["all_ordinary_documents_under_6000"]); self.assertTrue(d["baton_within_8000_20000"])
        self.assertEqual(r["terminal_route"],"PREPARED_NOT_SENT"); self.assertFalse(r["message_sent"] or r["task_created"] or r["subagent_spawned"])
    def test_portfolios_and_tools(self):
        p=load("portfolios/expanded-portfolio-execution.json")
        self.assertEqual(p["counts"],{"safe_now":40,"candidate":30,"skills":20,"runners":10,"clean_fix_refine":40})
        self.assertTrue(p["all_resolved"])
        s=load("validation/skill-validation.json"); r=load("validation/runner-validation.json")
        self.assertEqual((s["count"],r["count"]),(20,10)); self.assertEqual(s["global_install_count"],0)
    def test_final_manifests_and_privacy(self):
        o=load("validation/final-owner-manifest.json"); s=load("validation/final-staged-manifest.json")
        self.assertEqual(o["entry_count"],len(o["entries"])); self.assertEqual(len(o["self_exclusions"]),5)
        self.assertEqual(s["entry_count"],len(s["entries"])); self.assertEqual(len(s["self_exclusions"]),3)
        self.assertEqual(load("validation/final-owner-privacy.json")["confirmed_hit_count"],0)
        self.assertEqual(load("validation/final-staged-privacy.json")["confirmed_hit_count"],0)
    def test_owner_threshold_and_accessibility(self):
        t=load("validation/final-owner-file-threshold.json")
        self.assertLess(t["owner_generated_file_count"],15000); self.assertFalse(t["rotation_required"])
        report=(ROOT/"reports/final-accessible-static-report.html").read_text(encoding="utf-8")
        for token in ("href='#main'","<header>","<nav aria-label='Final report'>","<main id='main'>","<footer>"): self.assertIn(token,report)
    def test_terminal_contract(self):
        c=load("final/final-validation-contract.json")
        self.assertEqual(c["state"],"POST_COMMIT_REQUIRED"); self.assertFalse(c["post_success_replay"])
        self.assertEqual(c["expected_parent"],"6fe9cd18f870f93c65a4a0a7992add3781d7fe01")

if __name__=="__main__": unittest.main()

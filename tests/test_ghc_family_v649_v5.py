from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v649-v5"
X1 = "e4d241300fd23ca09dc1889d7e84bc494a96f387"


def load(relative): return json.loads((PHASE / relative).read_text(encoding="utf-8"))
def git(*args): return subprocess.run(["git",*args],cwd=ROOT,check=True,capture_output=True,text=True,encoding="utf-8").stdout.strip()


class TestV649V5Evidence(unittest.TestCase):
    def test_core_distribution(self):
        row=load("x2/core-outcome-ledger.json"); self.assertEqual(row["distribution"],{"completed":6,"represented":2,"open_gap":1,"exact_gate":1}); self.assertEqual(row["proposal_count"],10)
    def test_every_proposal_has_two_artifacts(self):
        for row in load("x2/core-outcome-ledger.json")["outcomes"]:
            self.assertEqual(len(row["artifact_paths"]),2); self.assertTrue(all((PHASE/p).is_file() for p in row["artifact_paths"]))
    def test_all_mutations_rejected(self):
        row=load("validation/x2-synthetic-mutation-results.json"); self.assertEqual((row["count"],row["executed_count"],row["rejected_count"]),(70,70,70)); self.assertTrue(all(x["retained_negative"] for x in row["mutations"]))
    def test_http_cache_is_bounded(self):
        row=load("method-flow/http-cache-contract.json"); self.assertIn("duplicate_credit",{x["check"] for x in row["checks"]}); self.assertIn("production_cache",row["absent_or_reserved"])
    def test_bw_is_formal_not_empirical(self):
        row=load("gmut/bisognano-wichmann-obligations.json"); self.assertIn("observation_firewall",{x["check"] for x in row["checks"]}); self.assertIn("empirical_confirmation",row["absent_or_reserved"])
    def test_jwst_is_zero_row_open_gap(self):
        row=load("empirical/jwst-mast-study-contract.json"); self.assertEqual(row["outcome"],"open_gap"); self.assertEqual((row["downloads"],row["real_rows"],row["likelihood_evaluations"]),(0,0,0))
    def test_concrete_lab_remains_proxy(self):
        row=load("thos/concrete-laboratory-contract.json"); self.assertEqual(row["outcome"],"represented"); self.assertEqual((row["real_people"],row["real_specimens"],row["real_tests"]),(0,0,0))
    def test_oauth_remains_nonproduction(self):
        row=load("freed-id/oauth-refresh-security-profile.json"); self.assertEqual(row["outcome"],"represented"); self.assertTrue({"real_keys","accounts","trust_governance"}.issubset(row["absent_or_reserved"]))
    def test_cbr_stays_exact_gate(self):
        row=load("cbr/concrete-testing-risk-gate.json"); self.assertEqual(row["outcome"],"exact_gate"); self.assertIn("maori_authority",row["absent_or_reserved"])
    def test_zarr_is_not_exhaustive_security(self):
        row=load("formats/zarr-v3-contract.json"); self.assertIn("resource_budget",{x["check"] for x in row["checks"]}); self.assertIn("exhaustive_security",row["absent_or_reserved"])
    def test_tooltip_reserves_manual_evaluation(self):
        row=load("accessibility/tooltip-contract.json"); self.assertFalse(row["complete_accessibility"]); self.assertFalse(row["affected_user_evaluation"])
    def test_kirchhoff_rejects_psyche_conversion(self):
        row=load("thermo-psyche/kirchhoff-radiation-contract.json"); self.assertIn("agency_nonconversion",{x["check"] for x in row["checks"]}); self.assertIn("consciousness",row["absent_or_reserved"])
    def test_tmle_does_not_promote(self):
        row=load("stage20/tmle-contract.json"); self.assertEqual(row["participants"],0); self.assertFalse(row["stage20_ready"])
    def test_expanded_portfolios(self):
        self.assertEqual(load("approval-packets/x2-safe-now-results.json")["completed_count"],30); self.assertEqual(load("prototypes/x2-candidate-results.json")["completed_count"],20); self.assertEqual(load("maintenance/x2-clean-refine-results.json")["completed_count"],30)
    def test_skills_are_phase_local_and_used(self):
        row=load("x2/skill-use-ledger-final.json"); self.assertEqual((row["skill_count"],row["completed_count"],row["pending_count"]),(20,20,0)); self.assertFalse(row["global_installation"]); self.assertFalse(row["subagent_forward_test"])
    def test_runners_have_one_terminal_pending(self):
        row=load("x2/runner-use-ledger.json"); self.assertEqual((row["runner_count"],row["completed_count"],row["pending_closeout_count"]),(10,9,1))
    def test_negatives_preserved(self):
        row=load("x2/retained-negative-register.json"); self.assertEqual(row["effective_at_evidence"],5104); self.assertFalse(row["negative_erased"])
    def test_gates_preserved(self):
        row=load("x2/gate-register.json"); self.assertEqual((row["effective_open_gaps"],row["effective_exact_gates"]),(39,40)); self.assertEqual(row["silently_closed"],0)
    def test_method_flow_parity(self):
        row=load("method-flow/method-flow-ledger.json"); self.assertEqual((len(row["methods"]),len(row["witnesses"])),(9,18)); self.assertEqual(sum(x["result"]=="fail" for x in row["witnesses"]),9)
    def test_x1_commit_is_ancestral_and_immutable(self):
        self.assertEqual(git("merge-base","--is-ancestor",X1,"HEAD"),""); manifest=load("validation/x1-staged-manifest.json"); self.assertEqual(len(manifest["self_exclusions"]),3)
    def test_evidence_manifest_matches_head(self):
        manifest=load("validation/evidence-staged-manifest.json"); self.assertGreater(manifest["entry_count"],100)
        for entry in manifest["entries"]: self.assertEqual(git("rev-parse",f"HEAD:{entry['path']}"),entry["git_blob"])
    def test_overview_is_three_page_equivalent(self):
        words=len((PHASE/"integrated-overview.md").read_text(encoding="utf-8").split()); self.assertGreaterEqual(words,1200); self.assertLessEqual(words,6000)
    def test_accessible_report_structure(self):
        text=(PHASE/"accessible-report.html").read_text(encoding="utf-8"); self.assertTrue(all(token in text for token in ["<main","<nav","<table","<caption",'scope="col"','scope="row"',":focus","Skip to evidence","NOT_READY_FOR_STAGE_20"]))
    def test_threat_model_nonexhaustive(self):
        row=load("threat-model.json"); self.assertFalse(row["exhaustive"]); self.assertGreaterEqual(len(row["threats"]),8)
    def test_handoff_is_prepared_and_sanitized(self):
        text=(PHASE/"handoffs/sylven-arc-v649-v6-activation.md").read_text(encoding="utf-8"); self.assertGreaterEqual(len(text.split()),1200); self.assertIn("PREPARED_NOT_SENT",text); self.assertNotRegex(text,r"(?i)(source_thread_id|thread_id)\s*[:=]")
    def test_no_platform_or_task_action(self):
        row=load("orchestration/final-phase-state.json"); env=load("environment/x2-version-receipt.json"); self.assertEqual((row["subagents"],row["tasks_created"],row["cross_platform_messages"]),(0,0,0)); self.assertFalse(env["sandbox_or_hyperv_action"])


if __name__ == "__main__": unittest.main()

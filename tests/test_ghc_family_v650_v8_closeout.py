"""Closeout contract tests for Ilyra Fen v650-v8."""
import json,re,subprocess,unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]; ROOT=REPO/"docs/ilyra-fen/v650-v8"
SOURCE="f566d4b67bce4457cf5207f5409bbaa3427428a0"; X1="d8726faad1ae416ef31f98a8744901eeedfe3c56"; EVIDENCE="325c410a16241cd8fa21706f82ab2bfd8ed47531"; ORIGINAL_FINAL="4dc0a911415cc19b871008cb903e03605a7bfca5"; PREVIOUS_FINAL="549e39d8020955188cdf49618a1e60ce4df205ba"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
def git(*a): return subprocess.check_output(["git",*a],cwd=REPO).decode().strip()
class TestV650V8Closeout(unittest.TestCase):
 def test_truth(self):
  t=load("final/phase-truth.json"); self.assertEqual(t["outcome_counts"],{"completed":14,"represented":4,"open_gap":1,"exact_gate":1}); self.assertEqual(t["effective_negatives"],6443); self.assertEqual((t["effective_open_gaps"],t["effective_exact_gates"]),(50,51)); self.assertEqual(t["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
 def test_chain_contract(self):
  self.assertEqual(git("rev-parse","HEAD^"),PREVIOUS_FINAL); self.assertEqual(int(git("rev-list","--count",f"{SOURCE}..HEAD")),5); self.assertEqual(int(git("rev-list","--merges","--count",f"{SOURCE}..HEAD")),0); self.assertEqual(len(git("show","-s","--format=%P","HEAD").split()),1)
 def test_manifests_cover(self):
  owner=load("validation/final-owner-manifest.json"); delta=load("validation/final-delta-manifest.json"); self.assertEqual(set(git("diff","--name-only",f"{SOURCE}..HEAD").splitlines()),{r["path"] for r in owner["entries"]}|set(owner["self_exclusions"])); self.assertEqual(set(git("diff","--name-only",f"{EVIDENCE}..HEAD").splitlines()),{r["path"] for r in delta["entries"]}|set(delta["self_exclusions"]))
 def test_privacy_and_route(self):
  self.assertEqual(load("validation/final-owner-privacy.json")["confirmed_hit_count"],0); self.assertEqual(load("validation/final-delta-privacy.json")["confirmed_hit_count"],0); self.assertEqual(load("route/final-phase-state.json")["terminal_route"],"PREPARED_NOT_SENT")
 def test_overview_and_baton(self):
  overview=(ROOT/"deliverables/final-integrated-overview.md").read_text(encoding="utf-8"); baton=(ROOT/"handoffs/sable-rook-v651-v1-activation.md").read_text(encoding="utf-8"); self.assertGreaterEqual(len(re.findall(r"\b\w+\b",overview)),1500); self.assertLessEqual(len(re.findall(r"\b\w+\b",overview)),6000); self.assertGreaterEqual(len(re.findall(r"\b\w+\b",baton)),8000); self.assertLessEqual(len(re.findall(r"\b\w+\b",baton)),20000)
 def test_skills_runners_and_mutations(self):
  self.assertEqual(load("validation/skill-validation.json")["count"],20); self.assertEqual(load("validation/runner-validation.json")["count"],10); self.assertEqual(load("validation/mutation-execution.json")["rejected"],100)
 def test_environment_and_accessibility_reservations(self):
  e=load("environment/version-receipt.json"); self.assertTrue(all(v is False for v in e["actions"].values())); report=(ROOT/"deliverables/static-report.html").read_text(encoding="utf-8"); self.assertIn("Skip to content",report); self.assertIn("affected-user evaluation remain reserved",report)
 def test_method_flow(self):
  m=load("method-flow/method-flow-summary.json")["counts"]; self.assertEqual(m["witness_results"],{"fail":33,"pass":31}); self.assertEqual(m["states"]["candidate"],1); self.assertEqual(m["states"]["preferred"],20); self.assertEqual(sum(m["states"].values()),21); self.assertEqual(set(m["states"]),{"observed","candidate","validated","preferred","superseded","deprecated"})
if __name__=="__main__": unittest.main()

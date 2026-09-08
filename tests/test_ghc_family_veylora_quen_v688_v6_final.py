"""Final owner-package predicates. Exact Git head truth is bound by the external canonical."""
from pathlib import Path
import hashlib,json,re,unittest
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"docs/veylora-quen/v688-v6";FINAL=BASE/"final"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def norm(p):return p.read_bytes().replace(b"\r\n",b"\n")
class FinalEvidence(unittest.TestCase):
 def test_01_source_and_three_direct_lifecycle_slots(self):
  p=load(FINAL/"canonical-policy.json")
  self.assertEqual(p["source"],"d72ba9a9ebefc1e18cb89d2c8b90c661ba8aaf14")
  self.assertEqual(p["x1"],"6d7f5b0fc67f78a22463d3c3c9cec21aade35d92")
  self.assertEqual(p["evidence"],"2cbe1c85f358bbed533dab79a22ffec9dd795f30")
  self.assertEqual(p["expected_phase_commits"],3)
 def test_02_outcomes_and_retention(self):
  p=load(FINAL/"phase-truth.json")
  self.assertEqual(p["outcomes"],{"completed":176,"represented":11,"open_gap":3,"exact_gate":10})
  self.assertEqual(sum(p["outcomes"].values()),200)
  ledger=load(FINAL/"method-flow-ledger.json")
  self.assertEqual(p["retained_negative_groups"],sum(w["result"]=="fail" for w in ledger["witnesses"]))
  self.assertEqual(p["retained_adverse_admission_failures"]+p["retained_operational_failure_groups"],p["retained_negative_groups"])
  self.assertEqual(p["source_failed_canonical_credit"],0)
 def test_03_all_protected_gates_preserved(self):
  p=load(FINAL/"complete-incomplete-checklist.json")
  self.assertEqual(p["open_gap"]["retained_record_count"],762)
  self.assertEqual(p["exact_gate"]["retained_record_count"],775)
  self.assertEqual(p["exact_gate"]["exact_packets_unexecuted"],50)
  self.assertEqual(p["exact_gate"]["blocked_packets_unexecuted"],30)
 def test_04_one_sylven_edge_only(self):
  p=load(FINAL/"terminal-route-checklist.json")
  self.assertEqual((p["recipient_title"],p["recipient_phase"]),("Sylven Arc","v688-v7"))
  self.assertEqual((p["later_creation_controller"],p["later_phase"]),("Sylven Arc","v688-v8"))
  self.assertEqual(p["authorized_sends"],1);self.assertEqual(p["sends_already_made"],0)
  self.assertFalse(p["resend_authorized"]);self.assertFalse(p["precontact_authorized"])
  self.assertFalse(p["new_task_creation_authorized_here"]);self.assertFalse(p["post_send_monitoring"])
 def test_05_baton_modules_word_budget_and_eof(self):
  index=load(FINAL/"baton-index.json");text=(ROOT/index["path"]).read_text(encoding="utf-8")
  self.assertEqual(len(re.findall(r"^## Module \d\d",text,re.M)),13)
  self.assertEqual(len(text.split()),index["word_count"])
  self.assertTrue(10000<=index["word_count"]<=100000)
  self.assertTrue(text.rstrip().endswith("EOF VEYLORA QUEN V688 V6 BATON."))
  self.assertIn("gpt-6-astra",text);self.assertIn("max",text)
 def test_06_baton_preparation_is_not_delivery(self):
  index=load(FINAL/"baton-index.json");text=(ROOT/index["path"]).read_text(encoding="utf-8")
  self.assertEqual(index["delivery_state"],"PREPARED_NOT_SENT")
  self.assertIn("SENT_BY_VEYLORA_QUEN = false",text)
  self.assertIn("No precontact, second send",text)
 def test_07_overview_and_print_sections(self):
  md=(FINAL/"final-integrated-overview.md").read_text()
  self.assertGreaterEqual(len(md.split()),1500)
  self.assertIn("same-owner",md.casefold())
  doc=(FINAL/"static-report.html").read_text()
  self.assertEqual(doc.count('<section class="print-page">'),3)
  self.assertIn("break-before:page",doc)
 def test_08_html_structure_has_headers_and_reserves_manual_review(self):
  doc=(FINAL/"static-report.html").read_text()
  self.assertIn("lang='en'",doc);self.assertIn("<caption>",doc);self.assertIn("<thead>",doc)
  self.assertEqual(doc.count("<th scope='row'>"),200)
  self.assertIn("affected-user accessibility review remains reserved",doc)
 def test_09_package_and_promotion_totals(self):
  e=load(FINAL/"environment-final.json")
  self.assertEqual((e["installed_skill_count"],e["runner_interfaces"],e["parity_files"]),(10,5,96))
  p=load(BASE/"x2/promotion-receipt.json")
  self.assertEqual(p["state"],"PROMOTED_VALIDATED_BYTE_EQUAL")
  self.assertTrue(all(r["byte_equal"] for r in p["source_global_parity"]))
 def test_10_content_seal(self):
  seal=load(BASE/"seal/content-seal.json");self.assertGreaterEqual(len(seal["targets"]),6)
  for row in seal["targets"]:
   b=norm(ROOT/row["path"])
   self.assertEqual(hashlib.sha256(b).hexdigest(),row["sha256_normalized_lf"])
   self.assertEqual(len(b),row["bytes_normalized_lf"])
 def test_11_failed_definitions_are_recoverable(self):
  f=load(BASE/"x2/retained-attempts/x2-tests-first-failure.json")
  self.assertEqual(hashlib.sha256((BASE/"x2/retained-attempts/x2-tests-v1.py.txt").read_bytes()).hexdigest(),f["test_sha256_at_failure"])
  self.assertEqual(hashlib.sha256((BASE/"x2/retained-attempts/firmware-core-v1.py.txt").read_bytes()).hexdigest(),f["core_sha256_before"])
  self.assertEqual(f["test_passes"],14);self.assertEqual(len(f["failed_tests"]),2)
  self.assertTrue(load(BASE/"x2/oracle-recovery-receipt.json")["primary_evaluator_function_bodies_unchanged"])
 def test_12_scope_and_terminal_verdict(self):
  p=load(FINAL/"canonical-policy.json")
  self.assertFalse(p["post_success_replay"]);self.assertFalse(p["independent_reproduction"])
  self.assertFalse(p["unchanged_history_scan"]);self.assertFalse(p["sibling_lane_mutation"])
  self.assertEqual([r["expected_tests"] for r in p["test_modules"]],[12,16,12])
  self.assertEqual(load(FINAL/"phase-truth.json")["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
if __name__=="__main__":unittest.main()

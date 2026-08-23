from __future__ import annotations

import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "build_ghc_family_elaren_kestrel_v667_v7_x2.py"
SPEC = importlib.util.spec_from_file_location("elaren_v667_v7_x2", PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load Elaren x2 builder")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ElarenV667V7X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (mod.PHASE_ROOT / "x2/x2-build-receipt.json").is_file():
            raise RuntimeError("run x2 builder before x2 tests")

    def doc(self, relative):
        return json.loads((mod.PHASE_ROOT / relative).read_text(encoding="utf-8"))

    def test_01_x1_anchor(self): self.assertEqual(mod.X1_COMMIT, "b92d8b1b648c4d716ca894b22fda14327baed9b3")
    def test_02_source_anchor(self): self.assertEqual(mod.SOURCE_FINAL, "dc8d91294b7656ad5e9961bba93ff759af20846c")
    def test_03_outcome_count(self): self.assertEqual(len(self.doc("x2/proposal-outcomes.json")["outcomes"]), 20)
    def test_04_outcome_distribution(self): self.assertEqual(Counter(row["outcome"] for row in self.doc("x2/proposal-outcomes.json")["outcomes"]), Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}))
    def test_05_outcomes_allowed(self): self.assertTrue(all(row["outcome"] in mod.ALLOWED_OUTCOMES for row in self.doc("x2/proposal-outcomes.json")["outcomes"]))
    def test_06_completed_credit_bounded(self): self.assertEqual(sum(row["completion_credit"] for row in self.doc("x2/proposal-outcomes.json")["outcomes"]), 14)
    def test_07_positive_contracts(self): self.assertTrue(all(row["positive_passed"] for row in self.doc("x2/proposal-outcomes.json")["outcomes"]))
    def test_08_mutation_count(self): self.assertEqual(self.doc("x2/rejecting-mutations.json")["mutation_count"], 100)
    def test_09_mutations_rejected(self): self.assertEqual(self.doc("x2/rejecting-mutations.json")["rejected_count"], 100)
    def test_10_mutation_credit_zero(self): self.assertTrue(all(row["completion_credit"] == 0 for row in self.doc("x2/rejecting-mutations.json")["mutations"]))
    def test_11_revalidation_count(self): self.assertEqual(self.doc("x2/selected-revalidation-summary.json")["count"], 20)
    def test_12_revalidation_pass(self): self.assertEqual(self.doc("x2/selected-revalidation-summary.json")["passing_count"], 20)
    def test_13_revalidation_credit_zero(self): self.assertEqual(self.doc("x2/selected-revalidation-summary.json")["completion_credit"], 0)
    def test_14_tool_count(self): self.assertEqual(len(self.doc("x2/tooling/three-tool-transaction-receipt.json")["tools"]), 3)
    def test_15_tool_transaction_pass(self): self.assertTrue(self.doc("x2/tooling/three-tool-transaction-receipt.json")["status"].startswith("PASS"))
    def test_16_tool_smokes(self):
        row=self.doc("x2/tooling/three-tool-transaction-receipt.json"); self.assertEqual((row["positive_smoke_count"],row["negative_rejection_count"]),(3,3))
    def test_17_tool_audit(self): self.assertEqual(self.doc("x2/tooling/three-tool-transaction-receipt.json")["known_vulnerability_count"], 0)
    def test_18_flashcards(self): self.assertEqual(self.doc("deck/deck-index.json")["card_count"], 235)
    def test_19_sections(self): self.assertEqual(self.doc("deck/section-index.json")["section_count"], 15)
    def test_20_skills(self):
        row=self.doc("x2/skills-summary.json"); self.assertEqual((row["built"],row["validated"],row["used"]),(10,10,10))
    def test_21_runners(self):
        row=self.doc("x2/runners-summary.json"); self.assertEqual((row["built"],row["validated"],row["used"]),(10,10,10))
    def test_22_method_flow_layers(self):
        row=self.doc("method-flow/x2-method-flow-ledger.json"); self.assertEqual(row["activation_baseline"]["effective_negatives"],28175); self.assertGreater(row["evidence_candidate"]["effective_negatives"],28175)
    def test_23_gates_advance_only_by_one(self):
        row=self.doc("evidence/exact-open-gate-register.json"); self.assertEqual((row["open_gaps"],row["exact_gates"]),(199,197))
    def test_24_report_structure(self):
        text=(mod.PHASE_ROOT/"report/x2-accessible-report.html").read_text(encoding="utf-8"); self.assertIn("<caption>",text); self.assertIn('scope="col"',text); self.assertIn("NOT_READY_FOR_STAGE_20",text)
    def test_25_accessibility_reserved(self): self.assertFalse(self.doc("report/accessibility-reservation.json")["accessibility_complete"])
    def test_26_portfolio_exact_blocked_unexecuted(self):
        row=self.doc("x2/portfolio-execution.json"); self.assertEqual(row["exact_and_blocked_executed"],0); self.assertEqual(row["successor_recommendations_executed"],0)
    def test_27_successor_not_contacted(self): self.assertFalse(self.doc("x2/x2-build-receipt.json")["successor_contacted"])
    def test_28_manifest_replays(self):
        manifest=self.doc("validation/x2-content-manifest.json")
        for entry in manifest["entries"]:
            data=(ROOT/entry["path"]).read_bytes(); self.assertEqual(len(data),entry["bytes"]); self.assertEqual(mod.hashlib.sha256(data).hexdigest(),entry["sha256"])
    def test_29_privacy_zero(self):
        hits=[]
        for path in mod.owned_paths(): hits.extend(mod.x1.privacy_candidates(path,path.read_text(encoding="utf-8")))
        self.assertEqual(hits,[])
    def test_30_x2_build_receipt(self): self.assertEqual(self.doc("x2/x2-build-receipt.json")["status"],"PASS_EVIDENCE_CANDIDATE")


if __name__ == "__main__":
    unittest.main()

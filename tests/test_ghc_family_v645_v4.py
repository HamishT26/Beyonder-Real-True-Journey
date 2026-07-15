from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/ilyra-fen/v645-v4"


def load(relative: str) -> dict:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


class V645V4EvidenceTests(unittest.TestCase):
    def test_core_outcomes_and_artifacts(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(len(ledger["proposals"]), 10)
        self.assertEqual(
            Counter(row["outcome"] for row in ledger["proposals"]),
            Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
        )
        for row in ledger["proposals"]:
            for artifact in row["artifacts"]:
                self.assertTrue((PHASE_DIR / artifact).is_file(), artifact)

    def test_empirical_and_authority_boundaries(self) -> None:
        siren = load("gmut/standard-siren-zero-row-receipt.json")
        self.assertEqual(siren["real_rows_ingested"], 0)
        self.assertEqual(siren["likelihood_evaluations"], 0)
        self.assertEqual(siren["outcome"], "open_gap")
        thos = load("thos/measurement-invariance-contract.json")
        self.assertEqual(thos["real_participants"], 0)
        self.assertFalse(thos["blind_matched_budget_arms"])
        freed = load("freed-id/digital-credentials-request-profile.json")
        self.assertEqual(freed["real_keys"], 0)
        self.assertFalse(freed["production_ready"])
        cbr = load("cbr/collections-provenance-reservation.json")
        self.assertFalse(cbr["recommendation_made"])
        self.assertFalse(cbr["maori_authority"])

    def test_portfolio_execution(self) -> None:
        ledger = load("approval-packets/x2-execution-ledger.json")
        self.assertEqual(ledger["counts"], {"safe_now_completed": 30, "candidate_completed": 20, "exact_unexecuted": 10, "blocked_unexecuted": 5})
        self.assertEqual(ledger["inherited_completion_credit_before_owner_witness"], 0)
        self.assertEqual(len(ledger["safe_now"]), 30)
        self.assertEqual(len(ledger["candidates"]), 20)
        self.assertTrue(all(row["outcome"] == "completed" for row in ledger["safe_now"] + ledger["candidates"]))

    def test_skills_and_runners_built_validated_used(self) -> None:
        ledger = load("prototypes/skill-runner-execution-ledger.json")
        self.assertEqual(ledger["counts"], {"skills_built": 20, "skills_validated": 20, "skills_used": 20, "runners_built": 10, "runners_used": 10})
        self.assertTrue(all(row["built"] and row["validated"] and row["used"] for row in ledger["skills"]))
        self.assertTrue(all(row["built"] and row["used"] and row["bounded_test"] == "pass" for row in ledger["runners"]))
        for row in ledger["skills"]:
            skill_dir = PHASE_DIR / "prototypes/skills" / row["name"]
            self.assertTrue((skill_dir / "SKILL.md").is_file())
            self.assertTrue((skill_dir / "agents/openai.yaml").is_file())
        receipts = list((PHASE_DIR / "prototypes/runner-witnesses").glob("*.json"))
        self.assertEqual(len(receipts), 10)
        self.assertTrue(all(json.loads(path.read_text(encoding="utf-8"))["result"] == "pass" for path in receipts))

    def test_cleanup_and_negative_retention(self) -> None:
        clean = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual(clean["counts"]["completed"], 30)
        self.assertEqual(clean["destructive_change_count"], 0)
        synthetic = load("validation/synthetic-mutation-negative-register.json")
        self.assertEqual(synthetic["count"], 70)
        self.assertTrue(synthetic["all_rejected"])
        retained = load("retained-negative-register.json")
        self.assertEqual(retained["counts"], {"inherited_effective": 2003, "v645_v4_x1_operational": 7, "v645_v4_x2_operational": 7, "v645_v4_synthetic": 70, "effective_total": 2087})
        self.assertEqual(retained["negative_erasure_count"], 0)

    def test_method_flow_is_append_only_and_balanced(self) -> None:
        ledger = load("method-flow/method-flow-state.json")
        self.assertEqual(ledger["counts"]["methods"], 14)
        self.assertEqual(ledger["counts"]["witnesses"], 28)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 14, "pass": 14})
        self.assertEqual(ledger["counts"]["states"]["preferred"], 14)
        self.assertEqual(len({row["method_id"] for row in ledger["methods"]}), 14)

    def test_gates_and_terminal_truth(self) -> None:
        gates = load("exact-open-gate-register.json")
        self.assertEqual(gates["effective"], {"open_gaps": 6, "exact_gates": 7})
        self.assertTrue(gates["none_silently_closed"])
        truth = load("phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_team_reproduction"])
        for key in ["empirical_gmut_confirmation", "thos_effectiveness", "freed_id_production_completion", "cbr_or_maori_authority", "complete_accessibility", "exhaustive_security", "agi_or_asi", "consciousness_or_personhood", "theory_of_everything"]:
            self.assertFalse(truth[key], key)

    def test_documents_and_static_report(self) -> None:
        overview = (PHASE_DIR / "v645-v4-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1500)
        self.assertLessEqual(len(overview.split()), 6000)
        for path in PHASE_DIR.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 6000, str(path))
        report = (PHASE_DIR / "deliverables/v645-v4-static-report.html").read_text(encoding="utf-8")
        for marker in ['<html lang="en">', 'href="#main"', '<main id="main">', '<caption>', 'lang="mi"', 'Manual and affected-user evaluation remain reserved']:
            self.assertIn(marker, report)


if __name__ == "__main__":
    unittest.main()

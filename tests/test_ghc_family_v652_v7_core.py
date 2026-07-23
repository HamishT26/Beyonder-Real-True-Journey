from __future__ import annotations

import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

from scripts import ghc_family_v652_v7_core as core


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/elaren-kestrel/v652-v7"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V652V7CoreTests(unittest.TestCase):
    def test_thirty_contracts_validate(self) -> None:
        rows = core.proposals()
        self.assertEqual(len(rows), 30)
        for proposal in rows:
            self.assertEqual(core.validate_contract(core.contract_for(proposal)), [], proposal["proposal_id"])

    def test_outcome_distribution(self) -> None:
        outcomes = Counter(row["expected_disposition"] for row in core.proposals())
        self.assertEqual(outcomes, {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})

    def test_each_contract_has_six_or_more_obligations(self) -> None:
        for proposal in core.proposals():
            contract = core.contract_for(proposal)
            self.assertGreaterEqual(contract["obligation_count"], 6, proposal["proposal_id"])

    def test_each_surface_has_five_mutations(self) -> None:
        for proposal in core.proposals():
            self.assertEqual(len(core.mutations_for(proposal["proposal_id"])), 5)

    def test_all_150_mutations_reject(self) -> None:
        count = 0
        for proposal in core.proposals():
            results = core.execute_mutations(core.contract_for(proposal))
            count += len(results)
            self.assertTrue(all(row["rejected"] for row in results), proposal["proposal_id"])
        self.assertEqual(count, 150)

    def test_drop_required_field_rejects(self) -> None:
        result = core.execute_mutations(core.contract_for(core.proposals()[0]))[0]
        self.assertIn("missing:falsifier", result["issue_classes"])

    def test_cross_binding_rejects(self) -> None:
        result = core.execute_mutations(core.contract_for(core.proposals()[0]))[1]
        self.assertIn("cross_bound:proposal_id", result["issue_classes"])

    def test_boundary_weakening_rejects(self) -> None:
        result = core.execute_mutations(core.contract_for(core.proposals()[0]))[2]
        self.assertIn("forbidden:real_data_rows", result["issue_classes"])

    def test_unsupported_promotion_rejects(self) -> None:
        result = core.execute_mutations(core.contract_for(core.proposals()[0]))[3]
        self.assertIn("forbidden:empirical_confirmation", result["issue_classes"])

    def test_rollback_erasure_rejects(self) -> None:
        result = core.execute_mutations(core.contract_for(core.proposals()[0]))[4]
        self.assertIn("missing:rollback", result["issue_classes"])

    def test_zero_real_data_everywhere(self) -> None:
        for proposal in core.proposals():
            self.assertEqual(core.contract_for(proposal)["real_data_rows"], 0)

    def test_open_gap_is_eht_only(self) -> None:
        rows = [row for row in core.proposals() if row["expected_disposition"] == "open_gap"]
        self.assertEqual([row["proposal_id"] for row in rows], ["V6527-P29"])
        self.assertEqual(core.runner_payload(rows[0]["slug"])["outcome"], "open_gap")

    def test_exact_gate_is_authority_only(self) -> None:
        rows = [row for row in core.proposals() if row["expected_disposition"] == "exact_gate"]
        self.assertEqual([row["proposal_id"] for row in rows], ["V6527-P30"])
        contract = core.contract_for(rows[0])
        self.assertFalse(contract["participant_or_authority_decision"])

    def test_bounded_receipts_never_promote(self) -> None:
        for proposal in core.proposals():
            receipt = core.evaluate_surface(proposal["slug"])["receipt"]
            self.assertFalse(receipt["empirical_confirmation"])
            self.assertFalse(receipt["production_ready"])
            self.assertFalse(receipt["professional_validation"])
            self.assertFalse(receipt["legal_or_cultural_authority"])
            self.assertFalse(receipt["maori_authority"])
            self.assertFalse(receipt["independent_reproduction"])

    def test_surface_artifacts_exist(self) -> None:
        for proposal in core.proposals():
            base = PHASE / "surfaces" / proposal["slug"]
            self.assertTrue((base / "contract.json").is_file())
            self.assertTrue((base / "mutation-results.json").is_file())
            self.assertTrue((base / "bounded-receipt.json").is_file())

    def test_surface_artifacts_match_runtime(self) -> None:
        for proposal in core.proposals():
            base = PHASE / "surfaces" / proposal["slug"]
            self.assertEqual(load(f"surfaces/{proposal['slug']}/contract.json"), core.contract_for(proposal))
            self.assertEqual(load(f"surfaces/{proposal['slug']}/bounded-receipt.json"), core.evaluate_surface(proposal["slug"])["receipt"])

    def test_ten_skills_quick_validate(self) -> None:
        receipt = load("skills/skill-build-receipt.json")
        self.assertEqual((receipt["initialized_count"], receipt["customized_count"], receipt["quick_validated_count"]), (10, 10, 10))
        self.assertFalse(receipt["globally_installed"])
        self.assertEqual(receipt["forward_test"], "not_delegated_solo_route")

    def test_skill_templates_have_no_todo(self) -> None:
        for directory in (PHASE / "skills").iterdir():
            if directory.is_dir():
                text = (directory / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn("TODO", text)
                self.assertTrue((directory / "agents/openai.yaml").is_file())
                self.assertTrue((directory / "references/contract.json").is_file())

    def test_ten_runners_invoked(self) -> None:
        receipt = load("runners/runner-invocation-receipt.json")
        self.assertEqual((receipt["runner_count"], receipt["invoked_count"], receipt["valid_count"]), (10, 10, 10))

    def test_runner_scripts_are_family_named(self) -> None:
        receipt = load("runners/runner-invocation-receipt.json")
        for row in receipt["runners"]:
            self.assertTrue(row["runner"].startswith("ghc_family_"))
            self.assertTrue((ROOT / "scripts" / row["runner"]).is_file())

    def test_phase_validation_runner_covers_all_mutations(self) -> None:
        runner = ROOT / "scripts/ghc_family_v652_v7_validation_runner.py"
        completed = subprocess.run([sys.executable, str(runner)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual((payload["proposal_count"], payload["mutation_count"], payload["rejected"]), (30, 150, 150))

    def test_negative_accounting(self) -> None:
        negatives = load("retained-negative-register-x2.json")
        self.assertEqual(negatives["inherited_count"], 8917)
        self.assertEqual(negatives["x1_operational_count"], 14)
        self.assertEqual(negatives["x2_operational_count"], 12)
        self.assertEqual(negatives["synthetic_mutation_count"], 150)
        self.assertEqual(negatives["effective_total"], 9093)
        self.assertTrue(negatives["none_erased"])

    def test_gate_accounting(self) -> None:
        gates = load("exact-open-gate-register-x2.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (68, 69))
        self.assertTrue(gates["none_silently_closed"])

    def test_method_flow_parity(self) -> None:
        ledger = load("method-flow/evidence-method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 26)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 26, "pass": 26})
        self.assertEqual(ledger["counts"]["states"]["preferred"], 26)

    def test_portfolios_resolved(self) -> None:
        receipt = load("portfolios/execution-receipt.json")
        self.assertEqual(receipt["unresolved_authorized_internal_tasks"], 0)
        self.assertEqual(receipt["clean_fix_refine"]["resolved"], 30)
        self.assertTrue(receipt["external_gates_not_counted_as_internal_tasks"])

    def test_owner_file_threshold(self) -> None:
        receipt = load("validation/owner-file-threshold-receipt.json")
        self.assertTrue(receipt["below_threshold"])
        self.assertLess(receipt["owner_generated_file_count"], 2000)

    def test_x1_files_remain_in_history(self) -> None:
        completed = subprocess.run(["git", "merge-base", "--is-ancestor", "cd1ce10d7c456d55e48183652835f6c3f5866b89", "HEAD"], cwd=ROOT, capture_output=True)
        self.assertEqual(completed.returncode, 0)

    def test_terminal_verdict(self) -> None:
        truth = load("phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])
        expected_route = "PREPARED_NOT_SENT" if (PHASE / "closeout-receipt.json").is_file() else "NOT_ELIGIBLE_BEFORE_FINAL_GATE"
        self.assertEqual(truth["route_state"], expected_route)


if __name__ == "__main__":
    unittest.main()

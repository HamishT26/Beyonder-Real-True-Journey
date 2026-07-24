from __future__ import annotations

import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

from scripts import ghc_family_v653_v8_core as core


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/liora-venn/v653-v8"
X1_COMMIT = "ee3a0c035c9821ebad1561e94afb11daf9bdc028"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V653V8CoreTests(unittest.TestCase):
    def test_thirty_contracts_validate(self) -> None:
        rows = core.proposals()
        self.assertEqual(len(rows), 30)
        for proposal in rows:
            self.assertEqual(
                core.validate_contract(core.contract_for(proposal)),
                [],
                proposal["proposal_id"],
            )

    def test_outcome_distribution(self) -> None:
        outcomes = Counter(
            row["expected_disposition"] for row in core.proposals()
        )
        self.assertEqual(
            outcomes,
            {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            },
        )

    def test_contract_obligations_and_zero_real_data(self) -> None:
        for proposal in core.proposals():
            contract = core.contract_for(proposal)
            self.assertGreaterEqual(
                contract["obligation_count"], 6, proposal["proposal_id"]
            )
            self.assertEqual(contract["real_data_rows"], 0)
            self.assertFalse(contract["empirical_confirmation"])
            self.assertFalse(contract["participant_or_authority_decision"])

    def test_all_150_mutations_reject(self) -> None:
        count = 0
        for proposal in core.proposals():
            results = core.execute_mutations(core.contract_for(proposal))
            count += len(results)
            self.assertEqual(len(results), 5)
            self.assertTrue(
                all(
                    row["rejected"]
                    and row["credit"] == "retained_negative"
                    for row in results
                ),
                proposal["proposal_id"],
            )
        self.assertEqual(count, 150)

    def test_mutation_classes_reject_for_declared_reasons(self) -> None:
        results = core.execute_mutations(
            core.contract_for(core.proposals()[0])
        )
        self.assertIn("missing:falsifier", results[0]["issue_classes"])
        self.assertIn("cross_bound:proposal_id", results[1]["issue_classes"])
        self.assertIn("forbidden:real_data_rows", results[2]["issue_classes"])
        self.assertIn(
            "forbidden:empirical_confirmation", results[3]["issue_classes"]
        )
        self.assertIn("missing:rollback", results[4]["issue_classes"])

    def test_open_gap_is_faostat_zero_row_only(self) -> None:
        rows = [
            row
            for row in core.proposals()
            if row["expected_disposition"] == "open_gap"
        ]
        self.assertEqual([row["proposal_id"] for row in rows], ["V6538-P29"])
        payload = core.runner_payload(rows[0]["slug"])
        self.assertEqual(payload["outcome"], "open_gap")
        self.assertTrue(payload["valid"])

    def test_exact_gate_is_apiary_authority_only(self) -> None:
        rows = [
            row
            for row in core.proposals()
            if row["expected_disposition"] == "exact_gate"
        ]
        self.assertEqual([row["proposal_id"] for row in rows], ["V6538-P30"])
        contract = core.contract_for(rows[0])
        self.assertFalse(contract["participant_or_authority_decision"])

    def test_bounded_receipts_never_promote(self) -> None:
        for proposal in core.proposals():
            receipt = core.evaluate_surface(proposal["slug"])["receipt"]
            for field in (
                "empirical_confirmation",
                "production_ready",
                "professional_validation",
                "legal_or_cultural_authority",
                "maori_authority",
                "complete_accessibility",
                "exhaustive_security",
                "independent_reproduction",
            ):
                self.assertFalse(receipt[field], (proposal["proposal_id"], field))
            self.assertEqual(
                receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20"
            )

    def test_surface_artifacts_match_runtime(self) -> None:
        for proposal in core.proposals():
            target = PHASE / "surfaces" / proposal["slug"]
            self.assertEqual(
                sorted(path.name for path in target.iterdir()),
                ["bounded-receipt.json", "contract.json", "mutation-results.json"],
            )
            self.assertEqual(
                load(f"surfaces/{proposal['slug']}/contract.json"),
                core.contract_for(proposal),
            )
            self.assertEqual(
                load(f"surfaces/{proposal['slug']}/bounded-receipt.json"),
                core.evaluate_surface(proposal["slug"])["receipt"],
            )

    def test_ten_phase_local_skills_are_complete(self) -> None:
        receipt = load("skills/skill-build-receipt.json")
        self.assertEqual(
            (
                receipt["initialized_count"],
                receipt["customized_count"],
                receipt["quick_validated_count"],
            ),
            (10, 10, 10),
        )
        self.assertFalse(receipt["globally_installed"])
        self.assertEqual(receipt["forward_test"], "not_delegated_solo_route")
        directories = [
            path for path in (PHASE / "skills").iterdir() if path.is_dir()
        ]
        self.assertEqual(len(directories), 10)
        for directory in directories:
            text = (directory / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            self.assertLess(len(text.splitlines()), 500)
            self.assertTrue((directory / "agents/openai.yaml").is_file())
            self.assertTrue((directory / "references/contract.json").is_file())

    def test_ten_family_compatible_runners_invoked(self) -> None:
        receipt = load("runners/runner-invocation-receipt.json")
        self.assertEqual(
            (
                receipt["runner_count"],
                receipt["invoked_count"],
                receipt["valid_count"],
            ),
            (10, 10, 10),
        )
        for row in receipt["runners"]:
            self.assertTrue(row["runner"].startswith("ghc_family_"))
            self.assertTrue((ROOT / "scripts" / row["runner"]).is_file())
            self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_authority_runner_remains_exact_gated(self) -> None:
        runner = (
            ROOT / "scripts/ghc_family_apiary_authority_reservation.py"
        )
        completed = subprocess.run(
            [sys.executable, str(runner)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["outcome"], "exact_gate")
        self.assertEqual(payload["mutation_count"], 5)
        self.assertEqual(payload["rejected"], 5)

    def test_negative_and_gate_accounting(self) -> None:
        negatives = load("retained-negative-register-x2.json")
        self.assertEqual(negatives["inherited_count"], 10447)
        self.assertEqual(negatives["activation_negative_baseline"], 10447)
        self.assertEqual(negatives["x1_operational_count"], 8)
        self.assertEqual(negatives["x2_operational_count"], 4)
        self.assertEqual(negatives["synthetic_mutation_count"], 150)
        self.assertEqual(negatives["effective_total"], 10609)
        self.assertTrue(negatives["none_erased"])
        gates = load("exact-open-gate-register-x2.json")
        self.assertEqual(
            (
                gates["effective_open_gaps"],
                gates["effective_exact_gates"],
            ),
            (77, 78),
        )
        self.assertTrue(gates["none_silently_closed"])

    def test_method_flow_preserves_fail_pass_parity(self) -> None:
        ledger = load("method-flow/evidence-method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 12)
        self.assertEqual(
            ledger["counts"]["witness_results"],
            {"fail": 12, "pass": 12},
        )
        self.assertEqual(ledger["counts"]["states"]["preferred"], 12)
        text = json.dumps(ledger, ensure_ascii=False)
        self.assertIn("V6538-X2-N01", text)
        self.assertNotIn("V6532-", text)

    def test_portfolios_and_owner_threshold(self) -> None:
        receipt = load("portfolios/execution-receipt.json")
        self.assertEqual(receipt["unresolved_authorized_internal_tasks"], 0)
        self.assertEqual(receipt["safe_now"]["resolved"], 30)
        self.assertEqual(receipt["candidate"]["resolved"], 30)
        self.assertEqual(receipt["clean_fix_refine"]["resolved"], 30)
        self.assertTrue(
            receipt["external_gates_not_counted_as_internal_tasks"]
        )
        threshold = load("validation/owner-file-threshold-receipt.json")
        self.assertTrue(threshold["below_threshold"])
        self.assertLess(threshold["owner_generated_file_count"], 2000)

    def test_x1_commit_is_ancestral(self) -> None:
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", X1_COMMIT, "HEAD"],
            cwd=ROOT,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 0)

    def test_route_and_terminal_verdict(self) -> None:
        truth = load("phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertEqual(truth["route_state"], "INELIGIBLE_EVIDENCE_NOT_FINAL")
        overlay = load("workflow/x2-refinement/authorization-overlay.json")
        self.assertEqual(overlay["target_title"], "Tamar Vey")
        self.assertFalse(overlay["target_task_created"])
        self.assertFalse(overlay["sent"])
        self.assertFalse(overlay["route_authorization_changed"])


if __name__ == "__main__":
    unittest.main()

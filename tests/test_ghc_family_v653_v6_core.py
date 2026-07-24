from __future__ import annotations

import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

from scripts import ghc_family_v653_v6_core as core


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/caelen-ash/v653-v6"
X1_COMMIT = "5be148f1171a449550ce73dd524cb866db7632e3"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V653V6CoreTests(unittest.TestCase):
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

    def test_each_contract_has_six_or_more_obligations(self) -> None:
        for proposal in core.proposals():
            contract = core.contract_for(proposal)
            self.assertGreaterEqual(
                contract["obligation_count"], 6, proposal["proposal_id"]
            )

    def test_each_surface_has_five_mutations(self) -> None:
        for proposal in core.proposals():
            self.assertEqual(
                len(core.mutations_for(proposal["proposal_id"])), 5
            )

    def test_all_150_mutations_reject(self) -> None:
        count = 0
        for proposal in core.proposals():
            results = core.execute_mutations(core.contract_for(proposal))
            count += len(results)
            self.assertTrue(
                all(row["rejected"] for row in results),
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

    def test_zero_real_data_everywhere(self) -> None:
        for proposal in core.proposals():
            self.assertEqual(
                core.contract_for(proposal)["real_data_rows"], 0
            )

    def test_open_gap_is_gaia_dr4_only(self) -> None:
        rows = [
            row
            for row in core.proposals()
            if row["expected_disposition"] == "open_gap"
        ]
        self.assertEqual([row["proposal_id"] for row in rows], ["V6536-P29"])
        self.assertEqual(
            core.runner_payload(rows[0]["slug"])["outcome"], "open_gap"
        )

    def test_exact_gate_is_authority_only(self) -> None:
        rows = [
            row
            for row in core.proposals()
            if row["expected_disposition"] == "exact_gate"
        ]
        self.assertEqual([row["proposal_id"] for row in rows], ["V6536-P30"])
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

    def test_surface_artifacts_exist_and_match_runtime(self) -> None:
        for proposal in core.proposals():
            target = PHASE / "surfaces" / proposal["slug"]
            self.assertTrue((target / "contract.json").is_file())
            self.assertTrue((target / "mutation-results.json").is_file())
            self.assertTrue((target / "bounded-receipt.json").is_file())
            self.assertEqual(
                load(f"surfaces/{proposal['slug']}/contract.json"),
                core.contract_for(proposal),
            )
            self.assertEqual(
                load(f"surfaces/{proposal['slug']}/bounded-receipt.json"),
                core.evaluate_surface(proposal["slug"])["receipt"],
            )

    def test_ten_skills_quick_validate_and_local(self) -> None:
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
        self.assertEqual(
            receipt["forward_test"], "not_delegated_solo_route"
        )

    def test_skill_packages_are_complete_and_concise(self) -> None:
        for directory in (PHASE / "skills").iterdir():
            if not directory.is_dir():
                continue
            text = (directory / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            self.assertLess(len(text.splitlines()), 500)
            self.assertTrue((directory / "agents/openai.yaml").is_file())
            self.assertTrue(
                (directory / "references/contract.json").is_file()
            )

    def test_ten_family_current_runners_invoked(self) -> None:
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

    def test_av_authority_runner_remains_exact_gated(self) -> None:
        runner = (
            ROOT
            / "scripts/ghc_family_av_cultural_authority_guard.py"
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

    def test_negative_accounting(self) -> None:
        negatives = load("retained-negative-register-x2.json")
        self.assertEqual(negatives["inherited_count"], 10110)
        self.assertEqual(negatives["external_post_seal_count"], 1)
        self.assertEqual(negatives["activation_negative_baseline"], 10111)
        self.assertEqual(negatives["x1_operational_count"], 12)
        self.assertEqual(negatives["x2_operational_count"], 3)
        self.assertEqual(negatives["synthetic_mutation_count"], 150)
        self.assertEqual(negatives["effective_total"], 10276)
        self.assertTrue(negatives["none_erased"])

    def test_gate_accounting(self) -> None:
        gates = load("exact-open-gate-register-x2.json")
        self.assertEqual(
            (
                gates["effective_open_gaps"],
                gates["effective_exact_gates"],
            ),
            (75, 76),
        )
        self.assertTrue(gates["none_silently_closed"])

    def test_method_flow_parity(self) -> None:
        ledger = load("method-flow/evidence-method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 15)
        self.assertEqual(
            ledger["counts"]["witness_results"],
            {"fail": 15, "pass": 15},
        )
        self.assertEqual(ledger["counts"]["states"]["preferred"], 15)

    def test_portfolios_resolved(self) -> None:
        receipt = load("portfolios/execution-receipt.json")
        self.assertEqual(receipt["unresolved_authorized_internal_tasks"], 0)
        self.assertEqual(receipt["clean_fix_refine"]["resolved"], 30)
        self.assertTrue(
            receipt["external_gates_not_counted_as_internal_tasks"]
        )

    def test_owner_file_threshold(self) -> None:
        receipt = load("validation/owner-file-threshold-receipt.json")
        self.assertTrue(receipt["below_threshold"])
        self.assertLess(receipt["owner_generated_file_count"], 2000)

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
        self.assertIn(
            truth["route_state"],
            {
                "NOT_ELIGIBLE_EVIDENCE_NOT_FINAL",
                "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            },
        )


if __name__ == "__main__":
    unittest.main()

"""Owner-scoped evidence tests for Elaren Kestrel v671-v5 x2."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "docs" / "elaren-kestrel" / "v671-v5"


def load(relative: str):
    return json.loads((OWNER / relative).read_text(encoding="utf-8"))


CORE_SPEC = importlib.util.spec_from_file_location(
    "ghc_family_mechanical_music_core",
    ROOT / "scripts" / "ghc_family_mechanical_music_core.py",
)
assert CORE_SPEC and CORE_SPEC.loader
CORE = importlib.util.module_from_spec(CORE_SPEC)
CORE_SPEC.loader.exec_module(CORE)


class ElarenV671V5X2Tests(unittest.TestCase):
    def test_x1_gate_is_exact_and_manifest_replayed(self) -> None:
        gate = load("x2/x1-gate-receipt.json")
        self.assertEqual(gate["x1_commit"], "048f85cf945f9900095ca2a160561591a966aabe")
        self.assertEqual(gate["manifest_entries"], 20)
        self.assertEqual(gate["manifest_replay_issues"], [])
        self.assertTrue(all(gate["checks"].values()))

    def test_contract_suite_has_forty_rows(self) -> None:
        payload = load("x2/contract-suite.json")
        self.assertEqual(payload["row_count"], 40)
        self.assertEqual(len(payload["contracts"]), 40)

    def test_all_contracts_validate(self) -> None:
        rows = load("x2/contract-suite.json")["contracts"]
        self.assertEqual([CORE.validate_contract(row) for row in rows], [[] for _ in rows])

    def test_bounded_positive_and_hold_counts(self) -> None:
        payload = load("x2/contract-suite.json")
        self.assertEqual(payload["bounded_positive_controls"], 36)
        self.assertEqual(payload["held_open_gap"], 2)
        self.assertEqual(payload["held_exact_gate"], 2)

    def test_exact_four_label_outcome_vector(self) -> None:
        payload = load("x2/outcome-ledger.json")
        self.assertEqual(
            payload["counts"],
            {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        )
        self.assertEqual(payload["unknown_labels"], [])
        self.assertEqual({row["outcome"] for row in payload["rows"]}, CORE.CORE_OUTCOMES)

    def test_all_mutations_are_rejected_and_zero_credit(self) -> None:
        contracts = load("x2/contract-suite.json")["contracts"]
        payload = load("x2/mutation-ledger.json")
        self.assertEqual(payload["row_count"], 160)
        self.assertEqual(payload["rejected"], 160)
        self.assertEqual(CORE.validate_mutations(contracts, payload["rows"]), [])
        self.assertTrue(all(row["completion_credit"] == 0 for row in payload["rows"]))

    def test_twenty_inherited_revalidations_have_zero_credit(self) -> None:
        payload = load("x2/revalidation-results.json")
        self.assertEqual(payload["row_count"], 20)
        self.assertEqual(payload["bounded_integrity_passes"], 20)
        self.assertEqual(payload["elaren_novelty_credit"], 0)
        self.assertEqual(payload["elaren_completion_credit"], 0)
        self.assertTrue(all(row["integrity_result"] == "bounded_pass" for row in payload["rows"]))

    def test_portfolio_execution_counts(self) -> None:
        payload = load("x2/portfolio-execution.json")
        self.assertEqual(payload["completed_owner_safe_now"], 60)
        self.assertEqual(payload["completed_owner_candidates"], 30)
        self.assertEqual(payload["held_exact_approval"], 20)
        self.assertEqual(payload["held_blocked"], 10)
        self.assertEqual(payload["selected_owner_skills"], 10)
        self.assertEqual(payload["built_owner_runners"], 10)
        self.assertEqual(payload["completed_owner_clean_fix_refine"], 60)

    def test_exact_and_blocked_portfolios_remain_unexecuted(self) -> None:
        rows = load("x2/portfolio-execution.json")["rows"]
        for key in ("exact_approval", "blocked"):
            self.assertTrue(all(row["execution_state"] == "held_unexecuted" for row in rows[key]))
            self.assertTrue(all(row["completion_credit"] == 0 for row in rows[key]))

    def test_method_flow_retains_every_operational_and_mutation_failure(self) -> None:
        payload = load("x2/method-flow-evidence.json")
        self.assertEqual(payload["operational_failure_rows"], 9)
        self.assertEqual(payload["mutation_rows"], 160)
        self.assertEqual(payload["row_count"], 169)
        self.assertTrue(payload["all_failures_retained"])
        self.assertTrue(payload["all_recoveries_paired"])

    def test_evidence_counts_are_layered_and_exact(self) -> None:
        counts = load("x2/method-flow-evidence.json")["counts"]
        self.assertEqual(
            counts,
            {
                "effective_negatives": 34279,
                "effective_methods": 20822,
                "failed_witnesses": 6100,
                "bounded_passing_witnesses": 7969,
                "open_gaps": 265,
                "exact_gates": 260,
            },
        )

    def test_open_and_exact_gates_are_not_silently_closed(self) -> None:
        payload = load("x2/open-and-exact-gate-register.json")
        self.assertEqual(payload["effective_open_gaps"], 265)
        self.assertEqual(payload["effective_exact_gates"], 260)
        self.assertEqual(payload["silently_closed"], 0)
        self.assertEqual(len(payload["new_open_gaps"]), 2)
        self.assertEqual(len(payload["new_exact_gates"]), 2)

    def test_three_tools_pass_without_install_or_update(self) -> None:
        payload = load("x2/tool-evaluation.json")
        self.assertEqual(payload["result"], "VALID_BOUNDED_THREE_TOOL_SMOKE")
        self.assertEqual({row["name"] for row in payload["tools"]}, {"jsonschema", "pydantic", "referencing"})
        self.assertEqual(payload["install_count"], 0)
        self.assertEqual(payload["update_count"], 0)

    def test_ten_skills_are_local_validated_and_used(self) -> None:
        payload = load("x2/skill-use-receipt.json")
        self.assertEqual(payload["skill_count"], 10)
        self.assertEqual(payload["quick_validations_passed"], 10)
        self.assertEqual(payload["actual_owner_local_uses"], 10)
        self.assertEqual(payload["global_install_count"], 0)
        self.assertTrue(all((ROOT / row["path"]).is_file() for row in payload["rows"]))

    def test_ten_runners_pass_self_test_and_actual_use(self) -> None:
        payload = load("x2/runner-use-receipt.json")
        self.assertEqual(payload["runner_count"], 10)
        self.assertEqual(payload["self_tests_passed"], 10)
        self.assertEqual(payload["actual_uses_passed"], 10)
        self.assertEqual(payload["global_install_count"], 0)

    def test_static_report_passes_structural_accessibility(self) -> None:
        report = (OWNER / "x2" / "static-report.html").read_text(encoding="utf-8")
        observed = CORE.check_accessibility_html(report)
        self.assertEqual(observed["result"], "VALID_STRUCTURAL_ACCESSIBILITY")
        self.assertEqual(observed["passed"], observed["total"])
        self.assertFalse(observed["complete_accessibility_claim"])

    def test_source_adapter_is_zero_call_open_gap(self) -> None:
        payload = load("x2/source-adapter.json")
        self.assertEqual(payload["outcome"], "open_gap")
        self.assertEqual(payload["network_calls"], 0)
        self.assertEqual(payload["downloads"], 0)
        self.assertEqual(payload["ingested_rows"], 0)
        self.assertEqual(payload["external_writes"], 0)

    def test_trinity_evidence_preserves_zero_real_evidence(self) -> None:
        payload = load("x2/trinity-evidence.json")
        self.assertEqual(payload["primary_pillar"], "THOS Body")
        self.assertEqual(payload["THOS"]["participants"], 0)
        self.assertEqual(payload["THOS"]["operators"], 0)
        self.assertEqual(payload["GMUT"]["observations"], 0)
        self.assertEqual(payload["GMUT"]["predictions"], 0)
        self.assertEqual(payload["Freed_ID"]["keys"], 0)
        self.assertEqual(payload["Freed_ID"]["proofs"], 0)
        self.assertEqual(payload["CBR"]["Maori_authority_decisions"], 0)

    def test_route_is_held_without_successor_precontact(self) -> None:
        payload = load("x2/route-hold.json")
        self.assertEqual(payload["successor_resolution_count"], 0)
        self.assertEqual(payload["successor_reread_count"], 0)
        self.assertEqual(payload["contact_during_execution"], 0)
        self.assertEqual(payload["delivery_state"], "NOT_ELIGIBLE_BEFORE_EXACT_FINAL")

    def test_version_receipt_is_read_only(self) -> None:
        payload = load("x2/environment-version-receipt.json")
        self.assertFalse(payload["codex_app"]["updated"])
        self.assertFalse(payload["codex_cli"]["updated"])
        self.assertTrue(all(value is False for value in payload["host_changes"].values()))

    def test_evidence_overview_is_three_page_equivalent(self) -> None:
        text = (OWNER / "x2" / "integrated-evidence-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1800)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("zero aggregate-success credit", text)

    def test_complete_incomplete_keeps_protected_work_open(self) -> None:
        payload = load("x2/complete-incomplete.json")
        self.assertGreaterEqual(len(payload["incomplete_protected"]), 8)
        self.assertEqual(payload["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_retained_negative_register_matches_method_counts(self) -> None:
        negatives = load("x2/retained-negative-register.json")
        counts = load("x2/method-flow-evidence.json")["counts"]
        self.assertEqual(negatives["effective_negatives"], counts["effective_negatives"])
        self.assertEqual(negatives["failures_erased"], 0)
        self.assertTrue(negatives["layers_preserved_separately"])


if __name__ == "__main__":
    unittest.main()

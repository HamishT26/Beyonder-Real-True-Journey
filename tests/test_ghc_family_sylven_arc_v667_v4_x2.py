"""Owner-local bounded evidence checks for Sylven Arc v667-v4 x2."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "sylven-arc" / "v667-v4"
X1 = "0eb52121251e3e8ee6da0c3c472626640cde96a3"
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_sylven_arc_v667_v4_core import validate_contract


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class TestSylvenArcV667V4X2(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = load("x1/proposal-freeze.json")
        cls.outcomes = load("x2/proposal-outcomes.json")
        cls.mutations = load("x2/rejecting-mutations.json")
        cls.portfolio = load("x2/portfolio-execution.json")
        cls.registry = load("x2/skill-runner-registry.json")
        cls.flashcards = load("x2/flashcards/execution-receipts.json")
        cls.deck_mutations = load("x2/flashcards/mutation-receipt.json")
        cls.method_flow = load("method-flow/x2-method-flow-ledger.json")
        cls.negatives = load("evidence/retained-negative-register.json")
        cls.gaps = load("evidence/open-gap-register.json")
        cls.gates = load("evidence/exact-gate-register.json")
        cls.evidence = load("evidence/immutable-evidence-candidate.json")
        cls.versions = load("environment/version-receipt.json")
        cls.build = load("validation/x2-build-receipt.json")

    def test_frozen_x1_is_ancestral_and_unchanged(self) -> None:
        result = subprocess.run(["git", "merge-base", "--is-ancestor", X1, "HEAD"], cwd=ROOT, check=False)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.freeze["genuinely_new_proposal_count"], 20)
        self.assertTrue(self.freeze["x1_planning_only"])

    def test_twenty_positive_contracts_validate(self) -> None:
        proposal_ids = [row["proposal_id"] for row in self.freeze["new_proposals"]]
        self.assertEqual(len(proposal_ids), 20)
        for proposal_id in proposal_ids:
            root = PHASE_ROOT / "x2" / "proposals" / proposal_id.casefold()
            contract = json.loads((root / "contract.json").read_text(encoding="utf-8"))
            receipt = json.loads((root / "bounded-receipt.json").read_text(encoding="utf-8"))
            mutation_result = json.loads((root / "mutation-results.json").read_text(encoding="utf-8"))
            self.assertEqual(validate_contract(contract), [], proposal_id)
            self.assertTrue(receipt["positive_contract_valid"])
            self.assertEqual(receipt["protected_gates_crossed"], [])
            self.assertEqual(mutation_result["mutation_count"], 5)
            self.assertEqual(mutation_result["accepted_mutation_count"], 0)

    def test_outcomes_use_exactly_four_labels_and_partition(self) -> None:
        expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
        self.assertEqual(self.outcomes["counts"], expected)
        self.assertEqual(Counter(row["final_disposition"] for row in self.outcomes["outcomes"]), Counter(expected))
        self.assertEqual(set(self.outcomes["allowed_labels"]), set(expected))
        self.assertEqual(self.outcomes["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(all(row["inherited_completion_credit"] == 0 for row in self.outcomes["outcomes"]))

    def test_one_hundred_preregistered_mutations_are_rejected(self) -> None:
        self.assertEqual(self.mutations["mutation_count"], 100)
        self.assertEqual(self.mutations["accepted_mutation_count"], 0)
        self.assertEqual(self.mutations["retained_zero_credit_count"], 100)
        rows = self.mutations["mutations"]
        self.assertEqual(len({row["mutation_id"] for row in rows}), 100)
        self.assertTrue(all(not row["accepted"] for row in rows))
        self.assertTrue(all(row["validator_failures"] for row in rows))
        self.assertTrue(all(row["failed_witness_retained"] for row in rows))

    def test_portfolio_executes_ninety_five_and_holds_one_hundred(self) -> None:
        self.assertEqual(self.portfolio["executed_count"], 95)
        self.assertEqual(self.portfolio["held_count"], 100)
        executed = Counter(row["portfolio"] for row in self.portfolio["executed_rows"])
        self.assertEqual(executed, Counter({"owner_safe_now": 30, "owner_candidates": 15, "owner_skill_ideas": 10, "owner_runner_ideas": 10, "owner_clean_fix_refine": 30}))
        held = Counter(row["portfolio"] for row in self.portfolio["held_rows"])
        self.assertEqual(held, Counter({"successor_safe_now_recommendations": 20, "successor_candidate_recommendations": 15, "successor_skill_recommendations": 10, "successor_runner_recommendations": 10, "successor_clean_fix_refine_recommendations": 30, "exact_approval_packets": 10, "blocked_packets": 5}))
        self.assertTrue(all(row["external_action_count"] == 0 for row in self.portfolio["executed_rows"]))
        self.assertTrue(all(row["completion_credit"] == 0 for row in self.portfolio["held_rows"]))

    def test_ten_skills_and_ten_runners_are_bounded_and_smoke_used(self) -> None:
        self.assertEqual(self.registry["skill_count"], 10)
        self.assertEqual(self.registry["runner_count"], 10)
        self.assertEqual(self.registry["skill_smoke_passes"], 10)
        self.assertEqual(self.registry["runner_smoke_passes"], 10)
        self.assertEqual(self.registry["global_install_count"], 0)
        for row in self.registry["skills"]:
            self.assertFalse(row["global_install"])
            self.assertTrue(row["smoke_used"])
            self.assertTrue((ROOT / row["path"]).is_file())
            self.assertTrue((ROOT / row["runner_path"]).is_file())
        runner_smokes = list((PHASE_ROOT / "x2" / "runner-smoke").glob("*.json"))
        skill_smokes = list((PHASE_ROOT / "x2" / "skill-smoke").glob("*.json"))
        self.assertEqual(len(runner_smokes), 10)
        self.assertEqual(len(skill_smokes), 10)
        self.assertTrue(all(json.loads(path.read_text(encoding="utf-8"))["passed"] for path in runner_smokes + skill_smokes))

    def test_freed_id_flashcard_deck_passes_all_bounded_surfaces(self) -> None:
        self.assertTrue(self.flashcards["prebuild_smoke"]["valid"])
        self.assertFalse(self.flashcards["prebuild_smoke"]["replayed"])
        commands = {"build", "validate", "manifest", "graph", "privacy", "render_html", "diff", "compact_message", "mutations"}
        self.assertTrue(commands.issubset(self.flashcards))
        for command in commands:
            self.assertTrue(self.flashcards[command]["passed"], command)
            self.assertEqual(self.flashcards[command]["exit_code"], 0)
        self.assertEqual(self.flashcards["build"]["result"]["card_count"], 233)
        self.assertEqual(self.flashcards["build"]["result"]["section_count"], 13)
        self.assertTrue(self.flashcards["validate"]["result"]["valid"])
        self.assertEqual(self.flashcards["privacy"]["result"]["candidate_count"], 0)
        self.assertTrue(self.flashcards["render_html"]["result"]["manual_evaluation_reserved"])
        compact = (PHASE_ROOT / "deck" / "compact-activation.md").read_text(encoding="utf-8")
        self.assertIn("Dear Caelen Morrow", compact)
        self.assertIn("Sylven Arc's frozen x1", compact)
        self.assertNotIn("frozen Lyren x1", compact)

    def test_sixty_flashcard_mutations_are_rejected(self) -> None:
        self.assertEqual(self.deck_mutations["mutation_count"], 60)
        self.assertEqual(self.deck_mutations["rejected_count"], 60)
        self.assertEqual(self.deck_mutations["failure_credit"], 0)
        self.assertTrue(self.deck_mutations["valid"])
        self.assertTrue(all(row["rejected"] for row in self.deck_mutations["cases"]))

    def test_method_flow_and_negative_accounting_are_exact(self) -> None:
        self.assertEqual(self.method_flow["inherited_method_count"], 12799)
        self.assertEqual(self.method_flow["phase_method_count"], 310)
        self.assertEqual(self.method_flow["effective_method_count"], 13109)
        self.assertEqual(self.method_flow["phase_failed_witness_count"], 195)
        self.assertEqual(len(self.method_flow["rows"]), 310)
        self.assertTrue(self.method_flow["valid"])
        self.assertTrue(all(not row["failure_erased"] for row in self.method_flow["rows"]))
        self.assertEqual(self.negatives["inherited_repository_and_external_activation_count"], 27337)
        self.assertEqual(self.negatives["phase_additive_count"], 195)
        self.assertEqual(self.negatives["effective_count"], 27532)
        self.assertEqual(self.negatives["failure_erased_count"], 0)
        self.assertEqual(len(self.negatives["rows"]), 195)

    def test_gap_gate_and_adapter_remain_unexecuted(self) -> None:
        adapter = load("x2/adapter/smithsonian-open-access-zero-row.json")
        self.assertFalse(adapter["transport_enabled"])
        self.assertEqual(adapter["request_count"], 0)
        self.assertEqual(adapter["row_count"], 0)
        self.assertEqual(adapter["media_count"], 0)
        self.assertEqual(adapter["status"], "open_gap")
        self.assertEqual(self.gaps["effective_count"], 194)
        self.assertEqual(self.gates["effective_count"], 192)
        self.assertFalse(self.gates["new_rows"][0]["executed"])

    def test_evidence_boundary_counts_are_zero_and_verdict_is_closed(self) -> None:
        self.assertEqual(self.evidence["proposal_outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        for field in ("real_people", "real_objects", "real_measurements", "network_calls", "keys", "proofs", "external_actions"):
            self.assertEqual(self.evidence[field], 0, field)
        self.assertEqual(self.evidence["effective_negatives"], 27532)
        self.assertEqual(self.evidence["effective_methods"], 13109)
        self.assertEqual(self.evidence["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(self.evidence["same_owner_only"])

    def test_versions_were_verified_without_install_or_host_change(self) -> None:
        self.assertEqual(self.versions["action"], "verify_only_no_updates_or_installs")
        self.assertEqual(self.versions["packages_installed"], [])
        self.assertFalse(self.versions["codex_desktop_updated"])
        self.assertFalse(self.versions["sandbox_or_hyper_v_changed"])
        self.assertFalse(self.versions["host_security_weakened"])
        self.assertFalse(self.versions["rebooted"])
        self.assertEqual({row["label"] for row in self.versions["versions"]}, {"python", "git", "node", "codex"})

    def test_accessible_report_has_structural_landmarks_and_reservations(self) -> None:
        report = (PHASE_ROOT / "reports" / "accessible-report.html").read_text(encoding="utf-8")
        lowered = report.casefold()
        for token in ("<!doctype html>", '<html lang="en">', '<main id="main">', "<nav", "<table>", "<caption>"):
            self.assertIn(token, lowered)
        self.assertGreaterEqual(lowered.count("<h2>"), 10)
        self.assertIn("manual browser", lowered)
        self.assertIn("māori-authority", lowered)
        self.assertIn("not_ready_for_stage_20", lowered)

    def test_build_receipt_is_the_bounded_evidence_candidate(self) -> None:
        self.assertEqual(self.build["contracts"], 20)
        self.assertEqual(self.build["proposal_mutations"], 100)
        self.assertEqual(self.build["flashcard_mutations"], 60)
        self.assertEqual(self.build["accepted_mutations"], 0)
        self.assertEqual(self.build["skills"], 10)
        self.assertEqual(self.build["runners"], 10)
        self.assertEqual(self.build["portfolio_executions"], 95)
        self.assertEqual(self.build["method_flow_rows"], 310)
        self.assertEqual(self.build["status"], "VALID_TWO_STAGE_DEPENDENCY_CORRECTED_X2_COMPOSITE_WITH_ZERO_FAILED_AGGREGATE_CREDIT")


if __name__ == "__main__":
    unittest.main()

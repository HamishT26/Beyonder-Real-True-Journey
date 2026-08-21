from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_v664_v7_evidence as evidence


PHASE = ROOT / "docs/sable-rook/v664-v7"


def load(relative: str):
    return evidence.strict_json((PHASE / relative).read_bytes(), relative)


class SableV664V7X2Tests(unittest.TestCase):
    def test_x1_boundary_is_immutable(self):
        receipt = load("x2/x1-boundary-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["x1_commit"], evidence.X1_COMMIT)
        self.assertEqual(receipt["x1_parent"], evidence.SOURCE_FINAL)
        self.assertEqual(receipt["x1_path_changes_before_x2"], 0)
        result = subprocess.run(
            ["git", "diff", "--quiet", evidence.X1_COMMIT, "--", f"{evidence.PREFIX}x1"],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(result.returncode, 0)

    def test_outcomes_use_only_four_labels(self):
        ledger = load("x2/outcome-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertEqual(ledger["proposal_count"], 20)
        self.assertEqual(ledger["outcomes"], {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4})
        self.assertEqual({row["disposition"] for row in ledger["rows"]}, evidence.ALLOWED_OUTCOMES)
        self.assertEqual(ledger["positive_fixtures_passed"], 20)

    def test_all_one_hundred_mutations_are_retained_rejections(self):
        ledger = load("x2/outcome-ledger.json")
        ids = []
        for row in ledger["rows"]:
            mutation = load(Path(row["mutation_results"]).relative_to(evidence.PREFIX).as_posix())
            self.assertEqual(mutation["executed"], 5)
            self.assertEqual(mutation["rejected"], 5)
            self.assertEqual(mutation["accepted"], 0)
            self.assertTrue(all(item["accepted"] is False for item in mutation["results"]))
            ids.extend(item["negative_id"] for item in mutation["results"])
        self.assertEqual(len(ids), 100)
        self.assertEqual(len(set(ids)), 100)

    def test_surface_contracts_are_zero_row(self):
        ledger = load("x2/outcome-ledger.json")
        for row in ledger["rows"]:
            relative = Path(row["contract"]).relative_to(evidence.PREFIX).as_posix()
            contract = load(relative)
            self.assertTrue(contract["valid"])
            self.assertTrue(contract["zero_row"])
            self.assertEqual(contract["real_rows"], 0)
            self.assertEqual(contract["claims"], [])
            self.assertEqual(contract["protected_gate_promotions"], 0)
            self.assertEqual(len(contract["mutation_results"]), 5)

    def test_inherited_revalidation_has_zero_credit(self):
        receipt = load("x2/inherited-contract-integrity.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["selected_count"], 20)
        self.assertEqual(receipt["valid_count"], 20)
        self.assertEqual(receipt["novelty_credit"], 0)
        self.assertEqual(receipt["automatic_completion_credit"], 0)
        self.assertEqual(receipt["new_outcome_credit"], 0)

    def test_skills_are_local_validated_and_smoke_used(self):
        skills = load("x2/skill-build-receipt.json")
        runners = load("x2/runner-invocation-receipt.json")
        self.assertTrue(skills["valid"])
        self.assertEqual(skills["skill_count"], 10)
        self.assertEqual(skills["initialized"], 10)
        self.assertEqual(skills["customized"], 10)
        self.assertEqual(skills["quick_validated"], 10)
        self.assertEqual(skills["globally_installed"], 0)
        self.assertEqual(skills["subagent_forward_tests"], 0)
        self.assertTrue(runners["valid"])
        self.assertEqual(runners["runner_count"], 10)
        self.assertEqual(runners["passing"], 10)
        self.assertEqual(runners["skill_smoke_use_count"], 10)
        self.assertTrue(runners["family_current_naming"])

    def test_expanded_portfolios_execute_only_safe_bounds(self):
        portfolio = load("x2/portfolio-execution.json")
        self.assertTrue(portfolio["valid"])
        self.assertEqual(portfolio["counts"], {
            "safe_completed": 30,
            "candidate_prototypes": 15,
            "skills_built": 10,
            "runners_built": 10,
            "clean_fix_refine_completed": 30,
            "exact_unexecuted": 10,
            "blocked_unexecuted": 5,
        })
        self.assertTrue(all(row["status"] == "unexecuted_exact_approval_required" for row in portfolio["exact_approval_packets"]))
        self.assertTrue(all(row["status"] == "unexecuted_blocked" for row in portfolio["blocked_packets"]))
        self.assertEqual(portfolio["destructive_actions"], 0)
        self.assertEqual(portfolio["sibling_lane_mutations"], 0)

    def test_negatives_methods_and_gates_preserve_arithmetic(self):
        negatives = load("x2/retained-negative-register.json")
        methods = load("x2/method-flow-state.json")
        gates = load("x2/exact-open-gate-register.json")
        self.assertTrue(negatives["valid"])
        self.assertEqual(negatives["effective_negatives"], 24_933)
        self.assertEqual(negatives["erased"], 0)
        self.assertEqual(negatives["converted_failed_witnesses_to_pass"], 0)
        self.assertTrue(methods["valid"])
        self.assertEqual(methods["effective_methods"], 8_947)
        self.assertEqual(methods["failure_erasure_count"], 0)
        self.assertEqual(gates["effective_open_gaps"], 173)
        self.assertEqual(gates["effective_exact_gates"], 171)
        self.assertEqual(gates["silent_closures"], 0)

    def test_pillar_boundaries(self):
        gmut = load("x2/pillars/gmut-model-family.json")
        thos = load("x2/pillars/thos-matched-budget-proxy.json")
        freed = load("x2/pillars/freed-id-nonproduction-profile.json")
        cbr = load("x2/pillars/cbr-authority-matrix.json")
        self.assertEqual(gmut["real_rows"], 0)
        self.assertEqual(gmut["likelihood_evaluations"], 0)
        self.assertFalse(gmut["empirical_confirmation"])
        self.assertFalse(gmut["theory_of_everything"])
        self.assertEqual(thos["real_participants"], 0)
        self.assertEqual(thos["blind_matched_budget_real_arms"], 0)
        self.assertFalse(thos["operational_effectiveness_claim"])
        self.assertEqual(freed["real_keys"], 0)
        self.assertEqual(freed["real_proofs"], 0)
        self.assertFalse(freed["production_ready"])
        self.assertEqual(cbr["maori_authority_decisions"], 0)
        self.assertTrue(cbr["maori_concepts_remain_under_maori_authority"])

    def test_stage20_board_fails_closed(self):
        board = load("x2/stage20-evidence-board.json")
        self.assertTrue(board["valid"])
        self.assertEqual(board["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(all(value == 0 for value in board["evidence_vector"].values()))
        self.assertFalse(any(row["decision"] == "pass" for row in board["decisions"]))

    def test_environment_and_shared_skills_are_nonmutating(self):
        environment = load("x2/environment-version-receipt.json")
        reviewed = load("x2/reviewed-current-receipt.json")
        self.assertTrue(environment["valid"])
        self.assertFalse(environment["desktop_updated"])
        self.assertFalse(environment["elevation"])
        self.assertFalse(environment["sandbox_or_hyper_v_activated"])
        self.assertFalse(environment["host_security_changed"])
        self.assertFalse(environment["reboot"])
        self.assertTrue(reviewed["valid"])
        self.assertEqual(reviewed["shared_user_skill_changes"], 0)
        self.assertTrue(reviewed["historical_compatibility_preserved"])

    def test_reports_and_cards_have_accessible_structure(self):
        overview = (PHASE / "reports/integrated-overview.md").read_text(encoding="utf-8")
        report = (PHASE / "reports/accessible-static-report.html").read_text(encoding="utf-8")
        words = len(overview.split())
        self.assertGreaterEqual(words, 1_500)
        self.assertLessEqual(words, 100_000)
        for phrase in ("NOT_READY_FOR_STAGE_20", "not evidence of consciousness", "Maori concepts remain under Maori authority", "zero real data"):
            self.assertIn(phrase, overview)
        for fragment in ("<main>", "<nav aria-label=", "<caption>", "Manual keyboard", "no motion"):
            self.assertIn(fragment, report)
        cards = load("deck/card-manifest.json")
        self.assertTrue(cards["valid"])
        self.assertGreaterEqual(cards["card_count"], 10)

    def test_phase_truth_and_route_hold(self):
        truth = load("phase-truth-evidence.json")
        route = load("orchestration/terminal-route-state.json")
        self.assertTrue(truth["valid"])
        self.assertEqual(truth["frozen_proposal_count"], 3_990)
        self.assertEqual(truth["outcomes"], {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4})
        self.assertEqual(truth["canonical_exact_final_validation"], "pending_after_clean_pushed_final")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertIsNone(route["successor_title"])
        self.assertEqual(route["send_count"], 0)

    def test_all_phase_json_is_strict(self):
        paths = sorted(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 100)
        for path in paths:
            evidence.strict_json(path.read_bytes(), str(path.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()

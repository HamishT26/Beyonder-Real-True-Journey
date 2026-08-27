from __future__ import annotations

import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v672-v4"
X1 = PHASE / "x1"
X2 = PHASE / "x2"


def load(relative: str):
    return json.loads((X2 / relative).read_text(encoding="utf-8"))


class CaelenAshV672V4X2Tests(unittest.TestCase):
    def test_x1_frozen_surfaces_are_unchanged(self):
        protected = [
            "docs/caelen-ash/v672-v4/x1",
            "scripts/build_ghc_family_caelen_ash_v672_v4.py",
            "tests/test_ghc_family_caelen_ash_v672_v4_x1.py",
        ]
        changed = subprocess.run(
            ["git", "-C", str(ROOT), "diff", "--name-only", "HEAD", "--", *protected],
            text=True, capture_output=True, check=True,
        ).stdout.splitlines()
        self.assertEqual(changed, [])

    def test_one_shot_latch_is_spent_once(self):
        state = load("generation-state.json")
        self.assertEqual(state["state"], "one_shot_smoke_succeeded_do_not_replay")
        self.assertEqual(state["runner_smoke_invocations"], 1)
        self.assertEqual(state["runner_smoke_successes"], 1)
        self.assertEqual(state["skill_smoke_invocations"], 1)
        self.assertEqual(state["skill_smoke_successes"], 1)

    def test_ten_runner_receipts_and_sixty_checks(self):
        receipts = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((X2 / "runner-witnesses").glob("*.json"))]
        self.assertEqual(len(receipts), 10)
        self.assertEqual(sum(row["checks"] for row in receipts), 60)
        self.assertEqual(sum(row["passed_checks"] for row in receipts), 60)
        self.assertTrue(all(row["valid"] and row["invocation_count"] == 1 for row in receipts))

    def test_fixture_distribution(self):
        fixtures = [json.loads(path.read_text(encoding="utf-8")) for path in (X2 / "fixtures").rglob("*.json")]
        self.assertEqual(len(fixtures), 60)
        self.assertEqual(sum(row["expected_valid"] is True for row in fixtures), 10)
        self.assertEqual(sum(row["expected_valid"] is False for row in fixtures), 50)

    def test_outcome_distribution_and_labels(self):
        ledger = load("proposals/outcome-ledger.json")
        counts = Counter(row["outcome"] for row in ledger["outcomes"])
        self.assertEqual(counts, Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}))
        self.assertEqual(set(counts), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual(ledger["proposal_chain"], 6070)

    def test_all_forty_proposal_cards_have_outcomes(self):
        cards = [json.loads(path.read_text(encoding="utf-8")) for path in (X2 / "proposals").glob("ca6724-p*.json")]
        self.assertEqual(len(cards), 40)
        self.assertTrue(all(card["state"] == "executed_as_evidence_permitted" for card in cards))
        self.assertTrue(all(card["broader_credit"] == 0 for card in cards))

    def test_twenty_skill_packages_and_witnesses(self):
        packages = list((X2 / "skills").glob("*/SKILL.md"))
        metadata = list((X2 / "skills").glob("*/agents/openai.yaml"))
        witnesses = [json.loads(path.read_text(encoding="utf-8")) for path in (X2 / "skill-witnesses").glob("*.json")]
        self.assertEqual((len(packages), len(metadata), len(witnesses)), (20, 0, 20))
        self.assertTrue(all(row["valid"] and row["invocation_count"] == 1 for row in witnesses))
        self.assertTrue(all(row["globally_installed"] is False for row in witnesses))

    def test_skill_creator_quick_validation(self):
        receipt = load("skill-creator-quick-validation.json")
        self.assertEqual(receipt["packages"], 20)
        self.assertEqual(receipt["initial_failures"], 20)
        self.assertEqual(receipt["recovery_passes"], 20)
        self.assertEqual(receipt["final_failures"], 0)
        self.assertEqual(receipt["invocations_per_package"], 2)
        self.assertFalse(receipt["installed_skill_mutated"])
        self.assertFalse(receipt["persistent_environment_change"])

    def test_portfolio_execution_preserves_exact_and_blocked(self):
        execution = load("portfolio-execution.json")
        self.assertEqual(len(execution["safe_now"]), 60)
        self.assertEqual(len(execution["candidates"]), 30)
        self.assertEqual(len(execution["skills"]), 20)
        self.assertEqual(len(execution["runners"]), 10)
        self.assertEqual(len(execution["clean_fix_refine"]), 60)
        self.assertEqual(len(execution["exact_approval_packets"]), 20)
        self.assertEqual(len(execution["blocked_packets"]), 10)
        self.assertTrue(all(row["state"] == "retained_unexecuted" for row in execution["exact_approval_packets"] + execution["blocked_packets"]))

    def test_method_flow_non_erasure_and_counts(self):
        flow = load("method-flow/ledger.json")
        self.assertEqual(flow["failures_erased"], 0)
        self.assertEqual(flow["recoveries_relabelled_as_original_success"], 0)
        self.assertEqual(len(flow["expected_rejections"]), 50)
        self.assertEqual(flow["current_delta"], {"effective_negatives": 85, "failed_witnesses": 85, "methods": 46, "passing_witnesses": 61})
        self.assertEqual(flow["effective_counts"]["effective_negatives"], 35416)
        self.assertEqual(flow["effective_counts"]["effective_methods"], 21986)
        self.assertEqual(flow["effective_counts"]["effective_failed_witnesses"], 7237)
        self.assertEqual(flow["effective_counts"]["effective_passing_witnesses"], 9287)

    def test_negative_register_arithmetic(self):
        negatives = load("retained-negative-register.json")
        self.assertEqual(
            negatives["activation_baseline"] + negatives["startup_failures"] + negatives["preregistered_invalid_mutations"] + negatives["x2_unexpected_operational_failures"],
            negatives["effective_total"],
        )
        self.assertEqual(negatives["effective_total"], 35416)
        self.assertEqual(negatives["erased"], 0)

    def test_gate_register_is_additive(self):
        gates = load("gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], gates["inherited_open_gaps"] + len(gates["new_open_gaps"]))
        self.assertEqual(gates["effective_exact_gates"], gates["inherited_exact_gates"] + len(gates["new_exact_gates"]))
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (283, 276))
        self.assertEqual(gates["silently_closed"], 0)

    def test_phase_truth_and_terminal_verdict(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(truth["real_rows"], 0)
        self.assertEqual(truth["external_actions"], 0)

    def test_pillar_boundaries(self):
        pillars = load("pillar-boundaries.json")
        self.assertEqual(pillars["primary"], "thos_body")
        self.assertIn("nonproduction", pillars["freed_id"])
        self.assertIn("proxy", pillars["thos"])
        self.assertIn("firewall", pillars["gmut"])

    def test_environment_was_verify_only(self):
        receipt = load("environment-and-version-receipt.json")
        self.assertTrue(receipt["versions_verified_only"])
        for key in ("desktop_update_performed", "elevation_performed", "host_security_weakened", "reboot_performed", "unrelated_software_installed", "windows_feature_changed", "windows_sandbox_or_hyper_v_activated"):
            self.assertFalse(receipt[key])

    def test_accessible_report_structure_and_reservations(self):
        report = (X2 / "accessible-report.html").read_text(encoding="utf-8")
        for token in ("<h1>", "<main>", "<nav", "<table>", "<caption>", 'scope="col"', 'scope="row"'):
            self.assertIn(token, report)
        self.assertIn("assistive-technology", report)
        self.assertNotIn("<script", report.casefold())

    def test_overview_is_three_page_equivalent_and_bounded(self):
        words = (X2 / "integrated-overview.md").read_text(encoding="utf-8").split()
        self.assertGreaterEqual(len(words), 1400)
        self.assertLessEqual(len(words), 100000)

    def test_owner_file_ceiling(self):
        self.assertLess(len([path for path in PHASE.rglob("*") if path.is_file()]), 2000)

    def test_every_json_parses(self):
        for path in PHASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    def test_no_document_exceeds_word_ceiling(self):
        for path in PHASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)


if __name__ == "__main__":
    unittest.main()

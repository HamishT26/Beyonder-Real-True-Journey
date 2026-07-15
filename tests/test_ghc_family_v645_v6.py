"""Bounded x2 tests for Orin Thale v645-v6."""

from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v645-v6"
sys.path.insert(0, str(ROOT / "scripts"))


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V645V6EvidenceTests(unittest.TestCase):
    def test_ten_core_proposals(self):
        self.assertEqual(len(load("x2-proposal-ledger.json")["proposals"]), 10)

    def test_outcome_distribution(self):
        rows = load("x2-proposal-ledger.json")["proposals"]
        self.assertEqual(Counter(row["outcome"] for row in rows), Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))

    def test_only_allowed_outcomes(self):
        rows = load("x2-proposal-ledger.json")["proposals"]
        self.assertLessEqual(set(row["outcome"] for row in rows), {"completed", "represented", "open_gap", "exact_gate"})

    def test_every_core_artifact_exists(self):
        for row in load("x2-proposal-ledger.json")["proposals"]:
            for artifact in row["artifacts"]:
                self.assertTrue((PHASE / artifact).is_file(), artifact)

    def test_eht_zero_row_and_likelihood(self):
        row = load("gmut/eht-shadow-zero-row-receipt.json")
        self.assertEqual((row["real_rows"], row["downloads"], row["likelihood_evaluations"], row["constraints"]), (0, 0, 0, 0))

    def test_thos_remains_proxy(self):
        row = load("thos/challenge-response-proxy-vectors.json")
        self.assertEqual((row["real_participants"], row["real_operators"], row["real_arms"], row["disposition"]), (0, 0, 0, "represented"))

    def test_freed_id_nonproduction(self):
        row = load("freed-id/key-attestation-mutation-vectors.json")
        self.assertEqual((row["real_keys"], row["live_issuance"], row["interoperability_events"], row["disposition"]), (0, 0, 0, "represented"))

    def test_cbr_authority_reserved(self):
        row = load("cbr/fisheries-authority-reservation.json")
        self.assertFalse(row["maori_authority_claimed"] or row["legal_interpretation"] or row["case_findings"])
        self.assertEqual(row["disposition"], "exact_gate")

    def test_bundle_lab_bounded(self):
        row = load("security/git-bundle-mutation-vectors.json")
        self.assertTrue(row["disposable_lab"] and row["expected_results_passed"])
        self.assertFalse(row["canonical_repository_mutated"] or row["remote_mutated"])

    def test_accessibility_structural_only(self):
        row = load("accessibility/details-summary-audit.json")
        self.assertTrue(row["valid"])
        self.assertEqual((row["manual_keyboard_evaluation"], row["assistive_technology_evaluation"], row["affected_user_evaluation"]), ("reserved", "reserved", "reserved"))

    def test_thermo_category_barrier(self):
        row = load("thermo-psyche/cyclic-integral-mutation-vectors.json")
        self.assertTrue(row["valid"])
        self.assertFalse(next(v for v in row["vectors"] if v["case"] == "psyche_justice_conversion")["accepted"])

    def test_stage20_abstains(self):
        self.assertEqual(load("stage20/control-mutation-vectors.json")["stage20_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_seventy_synthetic_negatives(self):
        row = load("validation/synthetic-mutation-negative-register.json")
        self.assertEqual((row["count"], len(row["negatives"]), row["valid"]), (70, 70, True))

    def test_method_flow_append_only(self):
        row = load("prototypes/runner-witnesses/ghc_family_v645_v6_method_flow_runner.json")
        self.assertTrue(row["family_runner_used"])
        self.assertEqual(row["failure_erasure_count"], 0)
        self.assertEqual(row["failed_witnesses"], row["passing_witnesses"])

    def test_all_portfolios_executed(self):
        row = load("approval-packets/x2-execution-ledger.json")
        self.assertEqual((row["safe_now_executed"], row["candidates_executed"]), (20, 12))
        self.assertTrue(row["all_acceptance_passed"])

    def test_inherited_packets_not_executed(self):
        row = load("approval-packets/x2-execution-ledger.json")
        self.assertEqual((row["inherited_exact_preserved"], row["inherited_blocked_preserved"], row["inherited_packets_executed"]), (10, 5, 0))

    def test_twelve_skills_built_validated_used(self):
        row = load("prototypes/skill-runner-execution-ledger.json")
        self.assertEqual(row["count"], 12)
        self.assertTrue(row["all_built_validated_invoked"])
        self.assertFalse(row["installed_globally"])

    def test_six_runner_witnesses(self):
        for name in ("core", "portfolio", "skill", "boundary", "method_flow", "validation"):
            self.assertTrue((PHASE / f"prototypes/runner-witnesses/ghc_family_v645_v6_{name}_runner.json").is_file(), name)

    def test_cleanup_twenty_non_destructive(self):
        row = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((row["completed"], len(row["tasks"])), (20, 20))
        self.assertTrue(all(not task["destructive"] and task["acceptance_passed"] for task in row["tasks"]))

    def test_negative_register(self):
        row = load("retained-negative-register.json")
        self.assertEqual(row["counts"]["inherited_effective"], 2172)
        self.assertEqual(row["counts"]["preregistered_synthetic"], 70)
        self.assertEqual(row["erased"], 0)
        self.assertEqual(row["counts"]["effective_total"], sum(value for key, value in row["counts"].items() if key not in {"effective_total"}))

    def test_gate_register(self):
        row = load("exact-open-gate-register.json")
        self.assertGreaterEqual(row["counts"]["effective_open_gaps"], 8)
        self.assertGreaterEqual(row["counts"]["effective_exact_gates"], 9)
        self.assertEqual(row["silently_closed"], 0)

    def test_source_status_vocabulary(self):
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in load("sources/source-ledger.json")["sources"]))

    def test_phase_truth_boundaries(self):
        row = load("phase-truth.json")
        self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(any(row["claims"].values()))

    def test_static_report_markers(self):
        text = (PHASE / "deliverables/v645-v6-static-report.html").read_text(encoding="utf-8")
        for marker in ['lang="en"', '<title>', 'href="#main"', '<main id="main"', '<caption>', '<details>', '<summary>', 'Manual, assistive-technology, Māori-language, and affected-user evaluation remain reserved']:
            self.assertIn(marker, text)

    def test_overview_word_range(self):
        words = len((PHASE / "v645-v6-integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1500)
        self.assertLessEqual(words, 6000)

    def test_all_markdown_under_cap(self):
        for path in PHASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 6000, path)

    def test_all_json_parses(self):
        for path in PHASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    def test_sandbox_fail_closed(self):
        row = load("sandbox/sandbox-readonly-audit.json")
        self.assertFalse(row["launched"] or row["elevated"] or row["feature_changed"] or row["rebooted"])

    def test_same_owner_not_independent(self):
        row = load("reproduction/same-owner-repeatability-boundary.json")
        self.assertTrue(row["same_owner_shared_infrastructure"])
        self.assertFalse(row["independent_team"] or row["scientific_reproduction"])

    def test_owner_footprint_below_rotation(self):
        row = load("validation/owner-footprint-receipt.json")
        self.assertLess(row["owner_generated_files"], 15000)
        self.assertGreater(row["full_checkout_files"], 15000)
        self.assertFalse(row["rotation_triggered"])


if __name__ == "__main__":
    unittest.main()

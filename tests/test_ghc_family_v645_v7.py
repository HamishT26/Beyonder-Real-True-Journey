"""Bounded x2 tests for Tamar Vey v645-v7."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v645-v7"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V645V7EvidenceTests(unittest.TestCase):
    def test_ten_core_proposals(self):
        self.assertEqual(len(load("x2-proposal-ledger.json")["proposals"]), 10)

    def test_outcome_distribution(self):
        rows = load("x2-proposal-ledger.json")["proposals"]
        self.assertEqual(Counter(row["outcome"] for row in rows), Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))

    def test_only_four_truth_labels(self):
        rows = load("x2-proposal-ledger.json")["proposals"]
        self.assertLessEqual(set(row["outcome"] for row in rows), {"completed", "represented", "open_gap", "exact_gate"})

    def test_x1_ids_preserved(self):
        x1 = load("x1-proposals.json")["proposals"]
        x2 = load("x2-proposal-ledger.json")["proposals"]
        self.assertEqual([row["proposal_id"] for row in x1], [row["proposal_id"] for row in x2])

    def test_every_proposal_artifact_exists(self):
        for row in load("x2-proposal-ledger.json")["proposals"]:
            for artifact in row["artifacts"]:
                self.assertTrue((PHASE / artifact).is_file(), artifact)

    def test_gaia_zero_row(self):
        row = load("empirical/gaia-wide-binary-zero-row-receipt.json")
        self.assertEqual((row["real_rows"], row["downloads"], row["likelihood_evaluations"], row["constraints"], row["force_claims"]), (0, 0, 0, 0, 0))

    def test_thos_proxy_only(self):
        row = load("thos/fixity-handover-proxy-vectors.json")
        self.assertEqual((row["real_participants"], row["real_staff"], row["real_collections"], row["real_arms"], row["disposition"]), (0, 0, 0, 0, "represented"))

    def test_freed_id_nonproduction(self):
        row = load("freed-id/batch-issuance-mutation-vectors.json")
        self.assertEqual((row["real_keys"], row["real_proofs"], row["live_issuance"], row["interoperability_events"], row["disposition"]), (0, 0, 0, 0, "represented"))

    def test_cbr_authority_reserved(self):
        row = load("cbr/community-archive-authority-reservation.json")
        self.assertFalse(row["maori_authority_claimed"] or row["legal_interpretation"] or row["cultural_ratification"] or row["access_decisions"] or row["remedies_decided"])
        self.assertEqual(row["disposition"], "exact_gate")

    def test_python_cache_lab_bounded(self):
        row = load("security/python-import-cache-mutation-vectors.json")
        self.assertTrue(row["disposable_lab"] and row["temporary_root_removed"] and row["expected_results_passed"])
        self.assertFalse(row["installed_packages_changed"] or row["canonical_repository_mutated"] or row["remote_mutated"])

    def test_modal_structural_only(self):
        row = load("accessibility/modal-dialog-structural-audit.json")
        self.assertTrue(row["valid"])
        self.assertEqual((row["manual_keyboard_evaluation"], row["assistive_technology_evaluation"], row["affected_user_evaluation"]), ("reserved", "reserved", "reserved"))
        self.assertFalse(row["complete_wcag_claim"])

    def test_maxwell_category_barrier(self):
        row = load("thermo-psyche/maxwell-relation-mutation-vectors.json")
        self.assertTrue(row["valid"])
        self.assertFalse(next(v for v in row["vectors"] if v["case"] == "psyche_reciprocity_conversion")["accepted"])

    def test_stage20_abstains(self):
        self.assertEqual(load("stage20/adaptive-reuse-mutation-vectors.json")["stage20_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_seventy_synthetic_negatives(self):
        row = load("validation/synthetic-mutation-negative-register.json")
        self.assertEqual((row["count"], len(row["negatives"]), row["valid"]), (70, 70, True))

    def test_method_flow_append_only(self):
        row = load("prototypes/runner-witnesses/ghc_family_v645_v7_method_flow_runner.json")
        self.assertTrue(row["family_runner_used"])
        self.assertEqual(row["failure_erasure_count"], 0)
        self.assertEqual(row["failed_witnesses"], row["passing_witnesses"])

    def test_ten_skills_built_and_used(self):
        row = load("prototypes/skill-runner-execution-ledger.json")
        self.assertEqual(row["count"], 10)
        self.assertTrue(row["all_built_validated_invoked"])
        self.assertFalse(row["installed_globally"])

    def test_family_runners_registered(self):
        row = load("tooling/runner-registration-execution.json")
        self.assertGreaterEqual(row["registered_count"], 6)
        self.assertTrue(row["all_available_runners_invoked"])

    def test_negative_register(self):
        row = load("retained-negative-register.json")
        self.assertEqual(row["counts"]["inherited_effective"], 2272)
        self.assertEqual(row["counts"]["preregistered_synthetic"], 70)
        self.assertEqual(row["counts"]["x1_operational"], 9)
        self.assertEqual(row["erased"], 0)
        self.assertEqual(row["counts"]["effective_total"], sum(value for key, value in row["counts"].items() if key != "effective_total"))

    def test_gate_register(self):
        row = load("exact-open-gate-register.json")
        self.assertEqual((row["counts"]["effective_open_gaps"], row["counts"]["effective_exact_gates"]), (9, 10))
        self.assertEqual(row["silently_closed"], 0)

    def test_source_status_vocabulary(self):
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in load("sources/source-ledger.json")["sources"]))

    def test_phase_truth_boundaries(self):
        row = load("phase-truth.json")
        self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(any(row["claims"].values()))

    def test_static_report_markers(self):
        text = (PHASE / "deliverables/v645-v7-static-report.html").read_text(encoding="utf-8")
        for marker in ('lang="en"', '<title>', 'href="#main"', '<main id="main"', '<caption>', '<details>', '<summary>'):
            self.assertIn(marker, text)
        self.assertIn("Manual keyboard, browser, assistive-technology, Maori-language, and affected-user evaluation remain reserved", text)

    def test_overview_word_range(self):
        words = len((PHASE / "v645-v7-integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1500)
        self.assertLessEqual(words, 6000)

    def test_all_json_parses(self):
        for path in PHASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    def test_sandbox_fail_closed(self):
        row = load("environment/sandbox-readonly-audit.json")
        self.assertFalse(row["sandbox_launched"] or row["elevation"] or row["feature_changed"] or row["rebooted"])

    def test_same_owner_not_independent(self):
        row = load("reproduction/same-owner-repeatability-boundary.json")
        self.assertTrue(row["same_owner_shared_infrastructure"])
        self.assertFalse(row["independent_team"] or row["scientific_reproduction"])

    def test_owner_footprint_below_rotation(self):
        row = load("validation/owner-footprint-receipt.json")
        self.assertLess(row["owner_generated_files"], 15000)
        self.assertGreater(row["full_checkout_files"], 15000)
        self.assertFalse(row["rotation_triggered"])

    def test_commit_cap_declared(self):
        row = load("reproduction/commit-cap-contract.json")
        self.assertEqual(row["maximum_phase_commits"], 4)
        self.assertLessEqual(row["planned_phase_commits"], 3)

    def test_full_suite_not_run(self):
        row = load("validation/evidence-scoped-test-receipt.json")
        self.assertFalse(row["full_repository_suite"])
        self.assertEqual(row["full_repository_suite_owner"], "Eiren Kestrel")

    def test_route_not_sent_during_evidence(self):
        row = load("orchestration/terminal-route-plan-x2.json")
        self.assertEqual((row["state"], row["send_count"]), ("PREPARED_NOT_SENT", 0))


if __name__ == "__main__":
    unittest.main()

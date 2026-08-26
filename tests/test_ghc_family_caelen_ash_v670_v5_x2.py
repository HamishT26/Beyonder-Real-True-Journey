"""Bounded x2 tests for Caelen Ash v670-v5."""

from __future__ import annotations

import hashlib
import importlib
import json
import subprocess
import unittest
from collections import Counter
from copy import deepcopy
from pathlib import Path

from scripts import build_ghc_family_caelen_ash_v670_v5_x2 as builder
from scripts.ghc_family_caelen_v670_v5_plate_lineage import (
    HandoverError,
    positive_fixture as handover_fixture,
    rejecting_fixtures as handover_rejecting,
    validate_record,
)
from scripts.ghc_family_caelen_v670_v5_measurement_vacancy import (
    EnvironmentContractError,
    positive_fixture as environment_fixture,
    rejecting_fixtures as environment_rejecting,
    validate_contract,
)
from scripts.ghc_family_caelen_v670_v5_plate_guard import (
    EvidenceGuardError,
    canonical_json_bytes,
    five_class_scan,
    run_named_guard,
    validate_proposal,
)

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "caelen-ash" / "v670-v5"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


class CaelenAshV670V5X2Tests(unittest.TestCase):
    def test_measurement_vacancy_accepts_three_synthetic_lenses(self):
        for lens in ("photographic_plate", "night_log", "planetarium_projector"):
            result = validate_contract(environment_fixture(lens))
            self.assertTrue(result["accepted"])
            self.assertFalse(result["real_measurement"])
            self.assertFalse(result["authority_conferred"])

    def test_measurement_vacancy_rejects_four_mutations(self):
        for row in environment_rejecting():
            with self.assertRaises(EnvironmentContractError):
                validate_contract(row)

    def test_plate_lineage_accepts_three_synthetic_lenses(self):
        for lens in ("photographic_plate", "night_log", "planetarium_projector"):
            result = validate_record(handover_fixture(lens))
            self.assertTrue(result["accepted"])
            self.assertTrue(result["correction_non_erasure"])
            self.assertFalse(result["authority_conferred"])

    def test_plate_lineage_rejects_four_mutations(self):
        for row in handover_rejecting():
            with self.assertRaises(HandoverError):
                validate_record(row)

    def test_canonical_json_sorts_and_rejects_duplicate_and_nonfinite(self):
        self.assertEqual(canonical_json_bytes('{"b":2,"a":1}'), b'{"a":1,"b":2}')
        with self.assertRaises(EvidenceGuardError):
            canonical_json_bytes('{"a":1,"a":2}')
        with self.assertRaises(EvidenceGuardError):
            canonical_json_bytes('{"value":NaN}')

    def test_all_frozen_proposals_pass_structure_guard(self):
        rows = load("x1/new-proposal-freeze.json")["rows"]
        self.assertEqual(len(rows), 40)
        self.assertTrue(all(validate_proposal(row)["accepted"] for row in rows))

    def test_proposal_guard_rejects_external_action_and_missing_gates(self):
        row = deepcopy(load("x1/new-proposal-freeze.json")["rows"][0])
        row["external_actions"] = 1
        with self.assertRaises(EvidenceGuardError):
            validate_proposal(row)
        row["external_actions"] = 0
        row["protected_gates"] = []
        with self.assertRaises(EvidenceGuardError):
            validate_proposal(row)

    def test_mutation_receipt_is_exact_and_zero_credit(self):
        payload = load("x2/mutation-receipt.json")
        self.assertEqual(payload["preregistered"], 160)
        self.assertEqual(payload["executed"], 160)
        self.assertEqual(payload["rejected"], 160)
        self.assertEqual(payload["unexpected_accepts"], 0)
        self.assertEqual(payload["completion_credit"], 0)
        self.assertTrue(all(row["rejected"] for row in payload["rows"]))

    def test_positive_controls_are_exactly_thirty_six(self):
        payload = load("x2/positive-control-receipt.json")
        self.assertEqual(payload["planned"], 36)
        self.assertEqual(payload["executed"], 36)
        self.assertEqual(payload["passed"], 36)
        self.assertTrue(all(row["accepted"] and row["external_actions"] == 0 for row in payload["rows"]))

    def test_outcome_distribution_uses_only_four_labels(self):
        payload = load("x2/outcome-ledger.json")
        self.assertEqual(len(payload["rows"]), 40)
        self.assertEqual(Counter(row["observed_outcome"] for row in payload["rows"]), Counter(builder.OUTCOMES))
        self.assertEqual({row["observed_outcome"] for row in payload["rows"]}, {"completed", "represented", "open_gap", "exact_gate"})

    def test_open_and_exact_rows_have_no_positive_control(self):
        rows = load("x2/outcome-ledger.json")["rows"]
        held = [row for row in rows if row["observed_outcome"] in {"open_gap", "exact_gate"}]
        self.assertEqual(len(held), 4)
        self.assertTrue(all(row["positive_control"] is None for row in held))

    def test_three_substantive_tools_have_accepting_and_rejecting_evidence(self):
        payload = load("x2/tool-evidence.json")
        self.assertEqual(len(payload["tools"]), 3)
        self.assertEqual(payload["measurement_vacancy"]["rejecting"], 4)
        self.assertEqual(payload["plate_lineage"]["rejecting"], 4)
        self.assertTrue(payload["plate_guard"]["duplicate_rejected"])
        self.assertTrue(payload["plate_guard"]["nonfinite_rejected"])
        self.assertEqual(payload["external_actions"], 0)

    def test_ten_family_runners_were_executed_and_passed(self):
        payload = load("x2/runner-evidence.json")
        self.assertEqual(payload["planned"], 10)
        self.assertEqual(payload["built_new"], 9)
        self.assertEqual(payload["selected_inherited_read_only"], 1)
        self.assertEqual(payload["executed"], 10)
        self.assertEqual(payload["passed"], 10)
        self.assertTrue(all(row["accepted"] and row["exit_code"] == 0 for row in payload["rows"]))
        for module_name in builder.RUNNER_MODULES:
            module = importlib.import_module(f"scripts.{module_name}")
            self.assertTrue(module.run()["accepted"])

    def test_twenty_phase_local_skills_are_complete_and_not_installed(self):
        payload = load("x2/skill-evidence.json")
        self.assertEqual(payload["planned"], 20)
        self.assertEqual(payload["built"], 20)
        self.assertEqual(payload["quick_validated"], 20)
        self.assertEqual(payload["smoke_used"], 20)
        self.assertFalse(payload["global_install"])
        self.assertTrue(all(row["quick_validated"] and row["smoke_used"] and not row["global_install"] for row in payload["rows"]))
        for row in payload["rows"]:
            self.assertTrue((ROOT / row["skill_path"]).is_file())
            self.assertTrue((ROOT / row["agent_path"]).is_file())

    def test_portfolio_completed_bounded_work_and_held_approval_work(self):
        payload = load("x2/portfolio-outcome.json")
        self.assertEqual(payload["counts"]["safe_now"], 60)
        self.assertEqual(payload["counts"]["candidates"], 30)
        self.assertEqual(payload["counts"]["skills"], 20)
        self.assertEqual(payload["counts"]["runners"], 10)
        self.assertEqual(payload["counts"]["clean_fix_refine"], 60)
        self.assertEqual(payload["exact_and_blocked_executed"], 0)
        self.assertEqual(payload["inherited_completion_credit"], 0)

    def test_clean_fix_refine_is_additive_only(self):
        payload = load("x2/clean-fix-refine-evidence.json")
        self.assertEqual(len(payload["completed"]), 60)
        self.assertEqual(len(payload["successor_recommendations"]), 30)
        self.assertEqual(payload["destructive_cleanup"], 0)
        self.assertEqual(payload["sibling_mutation"], 0)

    def test_exact_and_blocked_packets_remain_unexecuted(self):
        payload = load("x2/exact-and-blocked-register.json")
        self.assertEqual(len(payload["exact_approval"]), 20)
        self.assertEqual(len(payload["blocked"]), 10)
        self.assertEqual(payload["executed"], 0)

    def test_method_flow_retains_failures_mutations_and_recoveries(self):
        ledger = load("x2/method-flow-evidence.json")
        self.assertEqual(ledger["schema"], "ghc.family.method-flow-state.v1")
        self.assertEqual(ledger["counts"]["methods"], 205)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 172, "pass": 205})
        self.assertEqual(ledger["effective_overlay"], {
            "bounded_passing_witnesses": 5983,
            "effective_methods": 18944,
            "effective_negatives": 32767,
            "failed_witnesses": 4588,
            "repository_seal_rewritten": False,
        })
        self.assertTrue(all(row["retained_negative_ids"] for row in ledger["methods"]))

    def test_phase_truth_preserves_incremental_gaps_gates_and_terminal_verdict(self):
        truth = load("x2/phase-truth-evidence.json")
        self.assertEqual(truth["proposal_chain"], 5430)
        self.assertEqual(truth["open_gaps"], 249)
        self.assertEqual(truth["exact_gates"], 244)
        self.assertEqual(truth["real_people"], 0)
        self.assertEqual(truth["real_objects_measurements_rows"], 0)
        self.assertEqual(truth["real_world_actions"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_environment_receipt_has_no_update_install_or_host_change(self):
        payload = load("x2/environment-receipt.json")
        self.assertEqual(payload["codex_cli"], "0.149.0")
        self.assertEqual(payload["codex_desktop"], "26.820.7780.0")
        for field in ("desktop_updated", "elevation", "host_security_changes", "windows_feature_changes", "sandbox_or_hyper_v_activated", "unrelated_installation", "reboot"):
            self.assertFalse(payload[field])
        self.assertEqual(payload["real_data_downloads"], 0)

    def test_family_index_review_avoids_shared_churn(self):
        payload = load("x2/family-index-review.json")
        self.assertEqual(payload["shared_skill_changes"], 0)
        self.assertEqual(payload["global_memory_changes"], 0)
        self.assertEqual(payload["phase_local_skills"], 20)
        self.assertEqual(payload["family_compatible_runners"], 10)
        self.assertTrue(payload["historical_callers_preserved"])

    def test_accessible_report_has_structural_features_and_reservations(self):
        text = (OWNER_ROOT / "x2" / "accessible-evidence-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', "scope='row'", 'role="status"', '@media print'):
            self.assertIn(token, text)
        self.assertIn("affected-user evaluation remain reserved", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_five_class_guard_accepts_safe_text_and_rejects_synthetic_identifier(self):
        self.assertTrue(five_class_scan("bounded synthetic fixture only")["valid"])
        synthetic = "12345678-1234-4123-8123-123456789abc"
        self.assertFalse(five_class_scan(synthetic)["valid"])

    def test_guard_states_preserve_zero_credit_and_nonadmission(self):
        self.assertEqual(run_named_guard("canonical_nonpromotion")["canonical_credit"], 0)
        self.assertTrue(run_named_guard("proposal_corpus_gap")["canonical_row_mapping_open_gap"])
        self.assertFalse(run_named_guard("authority_vacancy")["authority_conferred"])
        self.assertFalse(run_named_guard("stage20_nonadmission")["admission"])

    def test_x1_paths_are_unmodified(self):
        changed = builder.git_text("diff", "--name-only", builder.X1_COMMIT, "--", "docs/caelen-ash/v670-v5/x1", "scripts/build_ghc_family_caelen_ash_v670_v5_x1.py", "tests/test_ghc_family_caelen_ash_v670_v5_x1.py")
        self.assertEqual(changed, "")

    def test_all_x2_json_parses_and_documents_are_below_cap(self):
        paths = sorted((OWNER_ROOT / "x2").rglob("*.json"))
        self.assertGreaterEqual(len(paths), 130)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))
        for path in (OWNER_ROOT / "x2").rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)

    def test_materialized_file_guard_remains_below_two_thousand(self):
        files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
        self.assertLess(len(files), 2000)

    def test_evidence_staged_review_manifest_and_receipts_are_exact(self):
        review = load("validation/evidence-staged-review.json")
        manifest = load("validation/evidence-manifest.json")
        privacy = load("validation/evidence-staged-privacy.json")
        receipt = load("validation/evidence-validation-receipt.json")
        method = load("validation/evidence-method-flow-validation.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["out_of_scope"], [])
        self.assertEqual(review["x1_frozen_path_mutations"], [])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(receipt["valid"])
        self.assertTrue(method["valid"])
        self.assertEqual(method["issue_count"], 0)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            blob = subprocess.run(["git", "show", f":{entry['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])


if __name__ == "__main__":
    unittest.main()

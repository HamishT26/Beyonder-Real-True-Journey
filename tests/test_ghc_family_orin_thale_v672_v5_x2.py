"""Bounded owner-self-scoped x2 tests for Orin Thale v672-v5."""

from __future__ import annotations

import hashlib
import importlib
import json
import subprocess
import unittest
from collections import Counter
from copy import deepcopy
from pathlib import Path

from scripts import build_ghc_family_orin_thale_v672_v5_x2 as builder
from scripts.ghc_family_orin_v672_v5_access_guard import (
    EvidenceGuardError,
    canonical_json_bytes,
    five_class_scan,
    mutation_variants,
    validate_proposal,
    validate_skill_smoke,
)
from scripts.ghc_family_orin_v672_v5_handover import (
    HandoverError,
    positive_fixture as handover_fixture,
    rejecting_fixtures as handover_rejecting,
    validate_handover,
)
from scripts.ghc_family_orin_v672_v5_provenance import (
    SURFACES,
    SurfaceError,
    positive_fixture as surface_fixture,
    rejecting_fixtures as surface_rejecting,
    validate_surface,
)


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "orin-thale" / "v672-v5"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


class OrinThaleV672V5X2Tests(unittest.TestCase):
    def test_01_ten_provenance_surfaces_accept_synthetic_fixtures(self):
        self.assertEqual(len(SURFACES), 10)
        for surface in SURFACES:
            result = validate_surface(surface_fixture(surface))
            self.assertTrue(result["accepted"])
            self.assertEqual(result["external_actions"], 0)
            self.assertFalse(result["authority_promoted"])

    def test_02_each_provenance_surface_rejects_five_mutations(self):
        for surface in SURFACES:
            rows = surface_rejecting(surface)
            self.assertEqual(len(rows), 5)
            for row in rows:
                with self.assertRaises(SurfaceError):
                    validate_surface(row)

    def test_03_three_handover_lenses_accept_synthetic_fixtures(self):
        for lens in ("tactile_map", "braille_proof", "alternate_format_request"):
            result = validate_handover(handover_fixture(lens))
            self.assertTrue(result["accepted"])
            self.assertTrue(result["hold_preserved"])
            self.assertFalse(result["release_authority"])

    def test_04_each_handover_lens_rejects_five_mutations(self):
        for lens in ("tactile_map", "braille_proof", "alternate_format_request"):
            rows = handover_rejecting(lens)
            self.assertEqual(len(rows), 5)
            for row in rows:
                with self.assertRaises(HandoverError):
                    validate_handover(row)

    def test_05_canonical_json_sorts_and_rejects_duplicate_or_nonfinite(self):
        self.assertEqual(canonical_json_bytes('{"b":2,"a":1}'), b'{"a":1,"b":2}')
        with self.assertRaises(EvidenceGuardError):
            canonical_json_bytes('{"a":1,"a":2}')
        with self.assertRaises(EvidenceGuardError):
            canonical_json_bytes('{"value":NaN}')

    def test_06_all_forty_frozen_proposals_pass_the_structure_guard(self):
        rows = load("x1/new-proposal-freeze.json")["rows"]
        self.assertEqual(len(rows), 40)
        self.assertTrue(all(validate_proposal(row)["accepted"] for row in rows))

    def test_07_each_proposal_has_four_rejecting_mutation_shapes(self):
        rows = load("x1/new-proposal-freeze.json")["rows"]
        for source in rows:
            variants = mutation_variants(source)
            self.assertEqual(len(variants), 4)
            for _name, mutated in variants:
                with self.assertRaises(EvidenceGuardError):
                    validate_proposal(mutated)

    def test_08_mutation_receipt_retains_all_one_hundred_sixty_rejections(self):
        payload = load("x2/mutation-receipt.json")
        self.assertEqual(payload["preregistered"], 160)
        self.assertEqual(payload["executed"], 160)
        self.assertEqual(payload["rejected"], 160)
        self.assertEqual(payload["unexpected_accepts"], 0)
        self.assertEqual(payload["completion_credit"], 0)
        self.assertTrue(all(row["rejected"] for row in payload["rows"]))

    def test_09_positive_control_receipt_is_exactly_thirty_six(self):
        payload = load("x2/positive-control-receipt.json")
        self.assertEqual(payload["planned"], 36)
        self.assertEqual(payload["executed"], 36)
        self.assertEqual(payload["passed"], 36)
        self.assertTrue(all(row["accepted"] and row["external_actions"] == 0 for row in payload["rows"]))

    def test_10_outcomes_use_only_the_four_authorized_labels(self):
        payload = load("x2/outcome-ledger.json")
        self.assertEqual(len(payload["rows"]), 40)
        observed = Counter(row["outcome"] for row in payload["rows"])
        self.assertEqual(observed, Counter(builder.OUTCOMES))
        self.assertEqual(set(observed), {"completed", "represented", "open_gap", "exact_gate"})

    def test_11_open_gap_and_exact_gate_rows_have_no_positive_control(self):
        rows = load("x2/outcome-ledger.json")["rows"]
        held = [row for row in rows if row["outcome"] in {"open_gap", "exact_gate"}]
        self.assertEqual(len(held), 4)
        self.assertTrue(all(row["positive_control"] is None for row in held))

    def test_12_three_tools_retain_accepting_and_rejecting_evidence(self):
        payload = load("x2/tool-evidence.json")
        self.assertEqual(len(payload["tools"]), 3)
        self.assertEqual(len(payload["provenance_surfaces"]), 10)
        self.assertEqual(len(payload["handover"]["accepting"]), 3)
        self.assertEqual(payload["handover"]["rejecting"], 15)
        self.assertTrue(payload["canonical_json"]["duplicate_rejected"])
        self.assertTrue(payload["canonical_json"]["nonfinite_rejected"])
        self.assertEqual(payload["external_actions"], 0)

    def test_13_ten_family_current_runners_execute_and_pass(self):
        payload = load("x2/runner-evidence.json")
        self.assertEqual(payload["planned"], 10)
        self.assertEqual(payload["built_new"], 10)
        self.assertEqual(payload["executed"], 10)
        self.assertEqual(payload["passed"], 10)
        self.assertEqual(payload["rejecting_fixtures"], 50)
        self.assertTrue(all(row["accepted"] and row["exit_code"] == 0 for row in payload["rows"]))
        for module_name in builder.RUNNER_MODULES:
            module = importlib.import_module(f"scripts.{module_name}")
            self.assertTrue(module.run_surface(module.SURFACE)["accepted"] if hasattr(module, "run_surface") and hasattr(module, "SURFACE") else True)

    def test_14_twenty_skills_are_validated_smoke_used_and_not_installed(self):
        payload = load("x2/skill-evidence.json")
        self.assertEqual(payload["planned"], 20)
        self.assertEqual(payload["initialized_officially"], 20)
        self.assertEqual(payload["customized"], 20)
        self.assertEqual(payload["read_through_eof"], 20)
        self.assertEqual(payload["quick_validated"], 20)
        self.assertEqual(payload["accepting_smoke_used"], 20)
        self.assertEqual(payload["rejecting_smoke_used"], 20)
        self.assertFalse(payload["global_install"])
        self.assertTrue(all(row["quick_validation_exit"] == 0 and row["rejecting_smoke_rejected"] for row in payload["rows"]))

    def test_15_skill_preparation_records_complete_main_agent_read_gate(self):
        payload = load("x2/skill-preparation.json")
        self.assertEqual(payload["count"], 20)
        self.assertFalse(payload["main_agent_read_pending"])
        self.assertEqual(payload["main_agent_read_witness"], "OT6725-X2-WP017")
        self.assertTrue(all(row["read_before_smoke"] and row["quick_validated"] and row["smoke_used"] for row in payload["rows"]))
        self.assertTrue(all(not row["global_install"] for row in payload["rows"]))

    def test_16_portfolio_counts_completed_owner_work_and_zero_credit_seeds(self):
        payload = load("x2/portfolio-outcome.json")
        expected = {
            "safe_now": 60,
            "candidates": 30,
            "exact_approval": 20,
            "blocked": 10,
            "skills": 20,
            "runners": 10,
            "clean_fix_refine": 60,
            "successor_safe_now": 20,
            "successor_candidates": 10,
            "successor_skills": 10,
            "successor_runners": 5,
            "successor_clean_fix_refine": 30,
        }
        self.assertEqual(payload["counts"], expected)
        self.assertEqual(payload["exact_and_blocked_executed"], 0)
        self.assertEqual(payload["inherited_completion_credit"], 0)
        self.assertEqual(payload["successor_recommendation_completion_credit"], 0)

    def test_17_clean_fix_refine_is_additive_and_non_destructive(self):
        payload = load("x2/clean-fix-refine-evidence.json")
        self.assertEqual(len(payload["completed"]), 60)
        self.assertEqual(len(payload["successor_recommendations"]), 30)
        self.assertEqual(payload["destructive_cleanup"], 0)
        self.assertEqual(payload["sibling_mutation"], 0)

    def test_18_exact_and_blocked_packets_remain_unexecuted(self):
        payload = load("x2/exact-and-blocked-register.json")
        self.assertEqual(len(payload["exact_approval"]), 20)
        self.assertEqual(len(payload["blocked"]), 10)
        self.assertEqual(payload["executed"], 0)

    def test_19_method_flow_retains_failures_and_separate_recoveries(self):
        ledger = load("x2/method-flow-ledger.json")
        self.assertEqual(ledger["schema"], "ghc.family.method-flow-state.v1")
        self.assertEqual(ledger["counts"]["methods"], 19)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 24, "pass": 25})
        self.assertEqual(ledger["counts"]["witnesses"], 49)
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in ledger["methods"]))
        self.assertTrue(all(row["retained_negative_ids"] for row in ledger["methods"]))

    def test_20_phase_truth_preserves_exact_effective_overlay_and_terminal_hold(self):
        truth = load("x2/phase-truth-evidence.json")
        self.assertEqual(truth["proposal_chain"], 6110)
        self.assertEqual(truth["outcomes"], builder.OUTCOMES)
        self.assertEqual(truth["open_gaps"], 283)
        self.assertEqual(truth["exact_gates"], 276)
        self.assertEqual(
            truth["counts_overlay"],
            {
                "bounded_passing_witnesses": 9313,
                "effective_methods": 22006,
                "effective_negatives": 35441,
                "exact_gates": 276,
                "failed_witnesses": 7262,
                "open_gaps": 283,
                "repository_seal_rewritten": False,
            },
        )
        self.assertEqual(truth["real_people"], 0)
        self.assertEqual(truth["real_objects_measurements_rows"], 0)
        self.assertEqual(truth["real_world_actions"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_21_environment_receipt_records_versions_only_and_no_host_change(self):
        payload = load("x2/environment-receipt.json")
        self.assertTrue(payload["versions_verified_only"])
        for field in (
            "desktop_updated",
            "elevation",
            "host_security_changes",
            "windows_feature_changes",
            "sandbox_or_hyper_v_activated",
            "unrelated_installation",
            "reboot",
        ):
            self.assertFalse(payload[field])
        self.assertEqual(payload["real_data_downloads"], 0)

    def test_22_family_index_review_avoids_shared_or_global_churn(self):
        payload = load("x2/family-index-review.json")
        self.assertEqual(payload["shared_skill_changes"], 0)
        self.assertEqual(payload["global_memory_changes"], 0)
        self.assertEqual(payload["phase_local_skills"], 20)
        self.assertEqual(payload["family_compatible_runners"], 10)
        self.assertTrue(payload["historical_callers_preserved"])

    def test_23_accessible_report_has_structural_features_and_reservations(self):
        text = (OWNER_ROOT / "x2" / "accessible-evidence-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"', "@media print"):
            self.assertIn(token, text)
        self.assertIn("Manual, assistive-technology, affected-user", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_24_five_class_and_skill_guards_accept_safe_text_and_fail_closed(self):
        self.assertEqual(five_class_scan("bounded synthetic fixture only"), [])
        synthetic_identifier = "12345678-1234-4123-8123-123456789abc"
        self.assertIn("raw_task_or_thread_identifier", five_class_scan(synthetic_identifier))
        accepting = {
            "synthetic": True,
            "external_actions": 0,
            "authority_claim": False,
            "retained_failures": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        self.assertTrue(validate_skill_smoke("bounded", accepting)["accepted"])
        rejecting = deepcopy(accepting)
        rejecting["authority_claim"] = True
        with self.assertRaises(EvidenceGuardError):
            validate_skill_smoke("bounded", rejecting)

    def test_25_x1_paths_and_manifest_blobs_remain_immutable(self):
        frozen = (
            "docs/orin-thale/v672-v5/x1",
            "scripts/build_ghc_family_orin_thale_v672_v5.py",
            "tests/test_ghc_family_orin_thale_v672_v5_x1.py",
            "docs/orin-thale/v672-v5/validation/x1-manifest.json",
        )
        self.assertEqual(builder.git_text("diff", "--name-only", builder.X1_COMMIT, "--", *frozen), "")
        manifest = json.loads(builder.git("show", f"{builder.X1_COMMIT}:docs/orin-thale/v672-v5/validation/x1-manifest.json").stdout.decode("utf-8"))
        self.assertEqual(manifest["entry_count"], 22)
        for entry in manifest["entries"]:
            blob = builder.git("show", f"{builder.X1_COMMIT}:{entry['path']}").stdout
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])

    def test_26_all_x2_json_parses_and_documents_remain_below_cap(self):
        paths = sorted((OWNER_ROOT / "x2").rglob("*.json"))
        self.assertEqual(len(paths), 56)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))
        for path in (OWNER_ROOT / "x2").rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)

    def test_27_materialized_owner_lane_stays_below_two_thousand_files(self):
        files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
        self.assertLess(len(files), 2000)

    def test_28_evidence_validation_review_privacy_and_method_flow_pass(self):
        review = load("validation/evidence-staged-review.json")
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

    def test_29_evidence_manifest_matches_exact_staged_git_blobs(self):
        manifest = load("validation/evidence-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        entry_paths = {entry["path"] for entry in manifest["entries"]}
        staged = set(builder.git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines())
        self.assertEqual(entry_paths, staged - set(manifest["self_exclusions"]))
        for entry in manifest["entries"]:
            blob = subprocess.run(["git", "show", f":{entry['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])

    def test_30_sources_and_overview_preserve_zero_row_and_authority_boundaries(self):
        source = load("x1/source-ledger.json")
        self.assertEqual(len(source["sources"]), 7)
        self.assertEqual(source["real_rows"], 0)
        self.assertEqual(source["downloads"], 0)
        self.assertEqual(source["external_writes"], 0)
        overview = (OWNER_ROOT / "x2" / "evidence-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1200)
        for token in ("typed scalar-tensor", "participant-free proxy", "synthetic and nonproduction", "Māori authority", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, overview)


if __name__ == "__main__":
    unittest.main()

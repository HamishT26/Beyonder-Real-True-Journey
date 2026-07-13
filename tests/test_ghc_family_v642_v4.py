from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v642-v4"


def read_json(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load_module("ghc_family_claim_coherence", "scripts/ghc_family_claim_coherence.py")
validator = load_module("ghc_family_claim_coherence_validator", "scripts/ghc_family_claim_coherence_validator.py")
minimal = load_module("ghc_family_claim_coherence_minimal", "scripts/ghc_family_claim_coherence_minimal.py")


class TestGhcFamilyV642V4(unittest.TestCase):
    def test_01_x1_freeze_and_x2_truth_are_separate(self) -> None:
        x2 = read_json("x2-proposal-ledger.json")
        x1_commit = x2["x1_commit"]
        names = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", "--pretty=", "--name-only", x1_commit],
            text=True,
            encoding="utf-8",
        ).splitlines()
        self.assertTrue(names)
        self.assertTrue(all(name.startswith("docs/ilyra-fen/v642-v4/") for name in names))
        forbidden = re.compile(r"(^scripts/|^tests/|x2-|phase-truth|closeout|seal|final-validation|deliverables/)")
        self.assertFalse([name for name in names if forbidden.search(name)])

    def test_02_frozen_chain_has_one_hundred_ten_unique_titles(self) -> None:
        chain = read_json("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(chain["proposal_count"], 110)
        self.assertEqual(len(chain["records"]), 110)
        self.assertEqual(len({row["proposal_id"] for row in chain["records"]}), 110)
        self.assertEqual(len({row["title"] for row in chain["records"]}), 110)
        self.assertEqual(chain["exact_duplicate_titles"], [])

    def test_03_atomic_publication_barrier_rejects_races_and_stale_inputs(self) -> None:
        base = {
            "required_dependencies": ["build"],
            "completed_dependencies": ["build"],
            "declared_input_digest": "same",
            "observed_input_digest": "same",
            "producer_exit_code": 0,
            "temporary_receipt_complete": True,
            "wrapper_consumed_complete_output": True,
            "same_filesystem_replace": True,
        }
        self.assertEqual(builder.publication_barrier(base), (True, []))
        valid, reasons = builder.publication_barrier({**base, "completed_dependencies": []})
        self.assertFalse(valid)
        self.assertIn("dependency_frontier_incomplete", reasons)
        valid, reasons = builder.publication_barrier({**base, "observed_input_digest": "changed"})
        self.assertFalse(valid)
        self.assertIn("stale_input_digest", reasons)

    def test_04_worktree_lease_refuses_foreign_and_quarantines_partial(self) -> None:
        accepted, reasons = builder.worktree_lease_decision({"owner": "Ilyra Fen", "expected_owner": "Ilyra Fen", "state": "complete", "head_matches": True, "clean": True, "detached": True, "locked": False})
        self.assertEqual((accepted, reasons), ("accept", []))
        foreign, reasons = builder.worktree_lease_decision({"owner": "other", "expected_owner": "Ilyra Fen", "state": "missing"})
        self.assertEqual(foreign, "refuse_foreign")
        self.assertIn("owner_scope_mismatch", reasons)
        partial, _ = builder.worktree_lease_decision({"owner": "Ilyra Fen", "expected_owner": "Ilyra Fen", "state": "timed_out", "head_matches": False, "clean": False, "detached": True, "locked": True})
        self.assertEqual(partial, "quarantine_owned")

    def test_05_field_redefinition_is_structural_and_redundancy_aware(self) -> None:
        base = {"invertible": True, "order_consistent": True, "input_dimension": "mass^2", "output_dimension": "mass^2", "observable_before": 2.0, "observable_after": 2.0, "gauge_redundancy": True, "claims_unique_identification": False, "empirical_claim": False}
        self.assertEqual(builder.field_redefinition_decision(base), (True, []))
        valid, reasons = builder.field_redefinition_decision({**base, "claims_unique_identification": True})
        self.assertFalse(valid)
        self.assertIn("redundancy_promoted_to_identifiability", reasons)
        boundary = read_json("physics/identifiability-claim-boundary.json")
        self.assertFalse(boundary["detected_force"])
        self.assertFalse(boundary["proof_or_canon"])

    def test_06_posterior_predictive_checks_distinguish_misfit_without_real_data(self) -> None:
        good = builder.posterior_predictive_assessment([1, 1.1, 0.9, 1.0], [1.02, 1.08, 0.92, 1.0])
        bad = builder.posterior_predictive_assessment([1, 1.1, 0.9, 1.0], [3, 3.1, 2.9, 3.0])
        self.assertTrue(good["passes"])
        self.assertFalse(bad["passes"])
        lock = read_json("empirical/real-row-promotion-lock.json")
        self.assertEqual(lock["real_measurement_rows"], 0)
        self.assertFalse(lock["promotion_allowed"])

    def test_07_thos_interference_protocol_keeps_real_arm_gap_open(self) -> None:
        case = {"exposure_mapping_preregistered": True, "network_frozen_before_outcomes": True, "direct_and_spillover_estimands_distinct": True, "blind": True, "matched_budget": True, "real_arm_count": 0, "independent_review": False}
        self.assertEqual(builder.thos_interference_decision(case)[0], "open_gap")
        self.assertEqual(builder.thos_interference_decision({**case, "network_frozen_before_outcomes": False})[0], "reject_protocol")
        gap = read_json("thos/real-arm-gap.json")
        self.assertEqual(gap["blind_matched_budget_real_arms"], 0)
        self.assertFalse(gap["real_thos_superiority"])

    def test_08_freed_id_downgrade_resistance_is_synthetic_only(self) -> None:
        case = {"offered": ["strong", "weak"], "supported": ["strong", "weak"], "deprecated": [], "selected": "weak", "known_identifiers": ["strong", "weak"], "preference": ["strong", "weak"], "holder_binding": True, "status_fresh": True}
        decision, reasons = builder.cryptosuite_decision(case)
        self.assertEqual(decision, "reject")
        self.assertIn("forced_downgrade", reasons)
        boundary = read_json("freed-id/production-assurance-boundary.json")
        self.assertEqual(boundary["real_keys"], 0)
        self.assertFalse(boundary["production_assurance"])

    def test_09_maori_data_governance_remains_exact_gated(self) -> None:
        case = {"purpose_changed": True, "fresh_collective_authority": False, "maori_authority_present": False, "affected_party_authority_present": False, "benefit_terms_authorized": False, "withdrawn": False, "competent_legal_review": False}
        decision, reasons = builder.secondary_use_authority_decision(case)
        self.assertEqual(decision, "exact_gate")
        self.assertIn("maori_authority_absent", reasons)
        gate = read_json("cbr/maori-data-governance-gate.json")
        self.assertFalse(gate["technical_artifact_can_grant_maori_authority"])
        self.assertEqual(gate["authorized_participants_present"], 0)

    def test_10_blind_challenge_packet_is_not_independent_reproduction(self) -> None:
        ready = {"expectations_hidden": True, "content_hashes_complete": True, "return_schema_present": True, "environment_disclosure_required": True, "deviation_log_required": True, "independent_executor_present": False, "returned_evidence": False, "executor_owner": None, "packet_owner": "Ilyra Fen"}
        self.assertEqual(builder.challenge_packet_decision(ready)[0], "packet_ready_only")
        self.assertEqual(builder.challenge_packet_decision({**ready, "expectations_hidden": False})[0], "reject_packet")
        gap = read_json("reproduction/independent-team-gap.json")
        self.assertEqual(gap["independent_team_count"], 0)
        self.assertFalse(gap["independent_reproduction_established"])

    def test_11_accessibility_map_reserves_manual_and_user_evaluation(self) -> None:
        features = ["lang", "title", "skip_link", "main_landmark", "heading_order", "table_headers", "focus_visible", "reduced_motion"]
        valid, reasons = builder.accessibility_decision({"features": features, "manual_evaluation_reserved": True, "user_participation_reserved": True, "claims_complete_conformance": False})
        self.assertEqual((valid, reasons), (True, []))
        valid, reasons = builder.accessibility_decision({"features": features, "manual_evaluation_reserved": False, "user_participation_reserved": False, "claims_complete_conformance": True})
        self.assertFalse(valid)
        self.assertIn("complete_conformance_overclaim", reasons)

    def test_12_claim_lattice_blocks_promotion_and_negative_erasure(self) -> None:
        protected = {name: False for name in builder.PROTECTED_CLAIMS}
        boundary = "No protected scientific authority production identity deployment accessibility security or reproduction claim is established."
        base = {"truth_labels": builder.TRUTH_LABELS, "protected_claims": protected, "negative_count": 118, "inherited_negative_count": 96, "open_gap_count": 5, "exact_gate_count": 6, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary_phrase": boundary, "expected_boundary_phrase": boundary}
        self.assertEqual(builder.claim_lattice_decision(base), (True, []))
        self.assertFalse(builder.claim_lattice_decision({**base, "negative_count": 95})[0])
        self.assertFalse(builder.claim_lattice_decision({**base, "protected_claims": {**protected, "empirical_gmut_confirmation": True}})[0])

    def test_13_all_inherited_and_phase_negatives_are_retained(self) -> None:
        register = read_json("retained-negative-register.json")
        ids = [row["negative_id"] for row in register["negatives"]]
        self.assertEqual(register["inherited_count"], 96)
        self.assertGreaterEqual(register["new_count"], 22)
        self.assertEqual(register["negative_count"], len(ids))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(f"V6423-N{value}" in ids for value in range(21, 29)))
        self.assertTrue(all(f"V6424-N{value:02d}" in ids for value in range(1, 21)))

    def test_14_gate_register_preserves_five_plus_six(self) -> None:
        gates = read_json("exact-open-gate-register.json")
        self.assertEqual(gates["open_gap_count"], 5)
        self.assertEqual(gates["exact_gate_count"], 6)
        self.assertEqual(gates["silently_closed"], 0)
        self.assertEqual(len(gates["gates"]), 11)

    def test_15_normalized_manifest_hashes_match(self) -> None:
        manifest = read_json("reproduction/manifest.json")
        self.assertEqual(manifest["file_count"], len(manifest["files"]))
        for row in manifest["files"]:
            value = hashlib.sha256((PHASE / row["path"]).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
            self.assertEqual(value, row["normalized_sha256"], row["path"])

    def test_16_overview_and_static_report_meet_bounded_floor(self) -> None:
        overview = (PHASE / "v642-v4-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 1800)
        report = (PHASE / "deliverables/v642-v4-claim-coherence-report.html").read_text(encoding="utf-8")
        for token in ['<html lang="en">', 'href="#main"', '<main id="main">', '<th scope="col">', 'prefers-reduced-motion', ':focus-visible', 'Automated structure is not complete accessibility conformance.', 'NOT_READY_FOR_STAGE_20']:
            self.assertIn(token, report)

    def test_17_source_statuses_and_references_close(self) -> None:
        sources = read_json("sources/source-ledger.json")
        self.assertEqual(sources["effective_source_count"], 54)
        self.assertEqual(sum(sources["effective_status_counts"].values()), 54)
        self.assertEqual(set(sources["effective_status_counts"]), {"current", "stable", "draft", "watch"})
        added_ids = {row["source_id"] for row in sources["added_sources"]}
        self.assertEqual(added_ids, {f"V6424-S{value}" for value in range(47, 55)})

    def test_18_versions_are_observational_and_windows_sandbox_is_bounded(self) -> None:
        receipt = read_json("environment/version-receipt.json")
        self.assertTrue(receipt["versions_verified_only"])
        self.assertFalse(receipt["desktop_updated"])
        self.assertFalse(receipt["host_features_changed"])
        self.assertEqual(receipt["windows_sandbox"], "unavailable_read_only_audit")

    def test_19_protected_claims_and_route_remain_fail_closed(self) -> None:
        truth = read_json("phase-truth.json")
        self.assertTrue(all(value is False for value in truth["protected_claims"].values()))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        route = read_json("workflow/route-preregistration.json")
        self.assertEqual(route["terminal_route"]["state"], "PLANNED_NOT_SENT")
        self.assertEqual(route["outbound_messages"], 0)

    def test_20_full_and_minimal_validators_accept_candidate(self) -> None:
        full = validator.validate(PHASE, allow_pending_snapshot=True, require_report=True)
        mini = minimal.verify(PHASE, allow_pending_snapshot=True)
        self.assertTrue(full["valid"], full["issues"])
        self.assertTrue(mini["valid"], mini["issues"])


if __name__ == "__main__":
    unittest.main()

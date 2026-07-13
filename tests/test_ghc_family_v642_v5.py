from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v642-v5"


def read_json(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load_module("ghc_family_evidence_noncompensation", "scripts/ghc_family_evidence_noncompensation.py")
validator = load_module("ghc_family_evidence_noncompensation_validator", "scripts/ghc_family_evidence_noncompensation_validator.py")
minimal = load_module("ghc_family_evidence_noncompensation_minimal", "scripts/ghc_family_evidence_noncompensation_minimal.py")


class TestGhcFamilyV642V5(unittest.TestCase):
    def test_01_x1_freeze_and_x2_are_separate(self) -> None:
        x1_commit = read_json("x2-proposal-ledger.json")["x1_commit"]
        names = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", "--pretty=", "--name-only", x1_commit],
            text=True,
            encoding="utf-8",
        ).splitlines()
        self.assertEqual(len(names), 15)
        self.assertTrue(all(name.startswith("docs/sable-rook/v642-v5/") for name in names))
        forbidden = re.compile(r"(^scripts/|^tests/|x2-|phase-truth|closeout|seal|final-validation|deliverables/)")
        self.assertFalse([name for name in names if forbidden.search(name)])

    def test_02_frozen_chain_has_120_unique_proposals(self) -> None:
        chain = read_json("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(chain["proposal_count"], len(chain["records"]))
        self.assertEqual(chain["proposal_count"], 120)
        self.assertEqual(len({row["proposal_id"] for row in chain["records"]}), 120)
        self.assertEqual(len({row["title"] for row in chain["records"]}), 120)
        self.assertEqual(chain["exact_duplicate_titles"], [])

    def test_03_citation_entailment_rejects_scope_and_root_inflation(self) -> None:
        base = {"claim_polarity": "positive", "source_polarity": "positive", "claim_modality": "bounded", "source_modality": "bounded", "claim_scope": ["local"], "source_scope": ["local", "structural"], "claim_evidence_type": "structural", "source_evidence_type": "structural", "claimed_independent_roots": 1, "unique_authority_roots": 1, "empirical_promotion": False}
        self.assertEqual(builder.citation_entailment_decision(base), (True, []))
        valid, reasons = builder.citation_entailment_decision({**base, "claim_scope": ["local", "global"]})
        self.assertFalse(valid)
        self.assertIn("claim_scope_exceeds_source", reasons)
        self.assertFalse(builder.citation_entailment_decision({**base, "claimed_independent_roots": 2})[0])

    def test_04_hyperbolicity_obligations_do_not_promote_scaffold(self) -> None:
        base = {"principal_symbol_declared": True, "eigenvalues_real": True, "diagonalizable": True, "gauge_declared": True, "constraint_growth_rate": -0.1, "dimensions_consistent": True, "empirical_claim": False}
        self.assertEqual(builder.hyperbolicity_obligation(base), (True, []))
        valid, reasons = builder.hyperbolicity_obligation({**base, "diagonalizable": False, "constraint_growth_rate": 0.2})
        self.assertFalse(valid)
        self.assertIn("principal_symbol_defective", reasons)
        boundary = read_json("physics/well-posedness-claim-boundary.json")
        self.assertFalse(boundary["gmut_well_posedness_established"])
        self.assertFalse(boundary["empirical_confirmation"])

    def test_05_prior_sensitivity_is_synthetic_and_zero_row(self) -> None:
        base = {"prior_families_frozen_before_outcomes": True, "conflict_threshold_preregistered": True, "posterior_means": [0.1, 0.11], "sensitivity_threshold": 0.05, "prior_predictive_tail_probability": 0.4, "conflict_threshold": 0.05, "real_measurement_rows": 0, "likelihood_executed": False, "empirical_confirmation": False}
        self.assertEqual(builder.prior_sensitivity_decision(base), ("represented", []))
        self.assertEqual(builder.prior_sensitivity_decision({**base, "empirical_confirmation": True})[0], "reject")
        lock = read_json("empirical/zero-row-inference-lock.json")
        self.assertEqual(lock["real_measurement_rows"], lock["likelihood_executions"])
        self.assertEqual(lock["fits"], 0)
        self.assertFalse(lock["promotion_allowed"])

    def test_06_thos_scorer_reliability_keeps_real_arm_gap_open(self) -> None:
        base = {"blind": True, "training_parity": True, "original_ratings_retained": True, "adjudication_separate": True, "matched_budget": True, "exclusion_rule_preregistered": True, "real_rater_count": 0, "blind_matched_budget_real_arms": 0, "independent_review": False}
        self.assertEqual(builder.scorer_reliability_decision(base)[0], "open_gap")
        self.assertEqual(builder.scorer_reliability_decision({**base, "original_ratings_retained": False})[0], "reject_protocol")
        gap = read_json("thos/real-rater-arm-gap.json")
        self.assertEqual(gap["real_raters"], gap["blind_matched_budget_real_arms"])
        self.assertFalse(gap["real_thos_superiority"])

    def test_07_freed_id_resolver_is_synthetic_and_fail_closed(self) -> None:
        base = {"endpoint": "https://resolver.example/resource", "redirects": ["https://service.example/final"], "max_redirects": 2, "allowed_request_metadata": ["accept"], "emitted_request_metadata": ["accept"], "query_normalized": True}
        self.assertEqual(builder.resolver_egress_decision(base), ("represented", []))
        decision, reasons = builder.resolver_egress_decision({**base, "endpoint": "https://127.0.0.1/private"})
        self.assertEqual(decision, "reject")
        self.assertIn("unsafe_network_target", reasons)
        boundary = read_json("freed-id/production-resolution-boundary.json")
        self.assertEqual(boundary["real_keys"], 0)
        self.assertFalse(boundary["production_assurance"])

    def test_08_cbr_dissent_retention_cannot_grant_authority(self) -> None:
        base = {"dissent_retained": True, "conflicts_disclosed": True, "conflicted_representative_voted": False, "silence_counted_as_consent": False, "remedy_rights_preserved": True, "affected_party_authority_present": False, "maori_authority_present": False, "cultural_authority_present": False, "competent_legal_review": False}
        self.assertEqual(builder.dissent_recusal_decision(base)[0], "exact_gate")
        decision, reasons = builder.dissent_recusal_decision({**base, "dissent_retained": False})
        self.assertEqual(decision, "reject_technical_process")
        self.assertIn("minority_report_erased", reasons)
        gate = read_json("cbr/dissent-recusal-authority-gate.json")
        self.assertFalse(gate["technical_artifact_can_grant_maori_authority"])

    def test_09_oracle_integrity_preserves_failure_class(self) -> None:
        base = {"oracle_digest": "same", "expected_oracle_digest": "same", "original_fixture_retained": True, "seed": 6425, "failure_signature_before": "reject", "failure_signature_after": "reject", "exception_scope_before": "none", "exception_scope_after": "none", "claims_exhaustive_security": False}
        self.assertEqual(builder.oracle_integrity_decision(base), (True, []))
        valid, reasons = builder.oracle_integrity_decision({**base, "failure_signature_after": "pass"})
        self.assertFalse(valid)
        self.assertIn("failure_class_changed_by_minimization", reasons)

    def test_10_determinism_envelope_is_same_owner_only(self) -> None:
        base = {"source_epoch_pinned": True, "timezone_utc": True, "locale_declared": True, "filesystem_order_sorted": True, "seed_pinned": True, "dependencies_declared": True, "semantic_change_normalized_away": False, "claims_independent_reproduction": False}
        self.assertEqual(builder.determinism_decision(base), (True, []))
        self.assertFalse(builder.determinism_decision({**base, "filesystem_order_sorted": False})[0])
        gap = read_json("reproduction/hermeticity-gap.json")
        self.assertEqual(gap["independent_team_count"], 0)
        self.assertFalse(gap["independent_reproduction_established"])

    def test_11_measurement_scale_barrier_rejects_category_crossing(self) -> None:
        base = {"scale": "ordinal", "operation": "median", "interval_zero_treated_as_absolute": False, "cross_domain_units_equated": False, "entropy_domains_conflated": False, "claims_fundamental_law": False}
        self.assertEqual(builder.measurement_scale_decision(base), (True, []))
        valid, reasons = builder.measurement_scale_decision({**base, "operation": "mean", "cross_domain_units_equated": True})
        self.assertFalse(valid)
        self.assertIn("operation_not_admissible_for_scale", reasons)
        boundary = read_json("thermo-psyche/category-barrier.json")
        self.assertFalse(boundary["fundamental_thermo_psyche_law"])

    def test_12_noncompensatory_board_rejects_score_laundering(self) -> None:
        protected = {name: False for name in builder.PROTECTED_CLAIMS}
        base = {"dimensions": {"engineering": 1, "empirical": 0, "authority": 0, "production": 0, "independence": 0}, "veto_dimensions": ["empirical", "authority", "production", "independence"], "missing_scored_as_neutral": False, "weighted_promotion_requested": False, "negative_count": 145, "inherited_negative_count": 120, "protected_claims": protected}
        self.assertEqual(builder.noncompensatory_decision(base)[0], "defer")
        decision, reasons = builder.noncompensatory_decision({**base, "weighted_promotion_requested": True})
        self.assertEqual(decision, "fail")
        self.assertIn("weighted_score_attempted_to_offset_veto", reasons)
        terminal = read_json("stage20/terminal-verdict.json")
        self.assertEqual(terminal["verdict"], "NOT_READY_FOR_STAGE_20")

    def test_13_all_inherited_and_phase_negatives_are_retained(self) -> None:
        current = read_json("retained-negative-register.json")
        prior = json.loads((ROOT / "docs/ilyra-fen/v642-v4/retained-negative-register.json").read_text(encoding="utf-8"))
        ids = [row["negative_id"] for row in current["negatives"]]
        self.assertEqual(current["inherited_count"], 120)
        self.assertEqual(ids[:120], [row["negative_id"] for row in prior["negatives"]])
        self.assertGreaterEqual(current["new_count"], 25)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(row["retained"] for row in current["negatives"]))

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
            actual = hashlib.sha256((PHASE / row["path"]).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
            self.assertEqual(actual, row["normalized_sha256"], row["path"])

    def test_16_overview_and_static_report_meet_bounded_floor(self) -> None:
        overview = (PHASE / "v642-v5-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 1800)
        report = (PHASE / "deliverables/v642-v5-noncompensation-report.html").read_text(encoding="utf-8")
        for token in ['<html lang="en">', 'href="#main"', '<main id="main">', '<th scope="col">', 'prefers-reduced-motion', ':focus-visible', 'Automated structure is not complete accessibility conformance.', 'NOT_READY_FOR_STAGE_20']:
            self.assertIn(token, report)

    def test_17_sources_and_draft_status_are_explicit(self) -> None:
        sources = read_json("sources/source-ledger.json")
        self.assertEqual(sources["effective_source_count"], 62)
        self.assertEqual(sum(sources["effective_status_counts"].values()), 62)
        self.assertEqual(set(sources["effective_status_counts"]), {"current", "stable", "draft", "watch"})
        added = {row["source_id"]: row for row in sources["added_sources"]}
        self.assertEqual(set(added), {f"V6425-S{n}" for n in range(55, 63)})
        self.assertEqual(added["V6425-S62"]["status_class"], "draft")

    def test_18_versions_sandbox_and_shared_tools_remain_bounded(self) -> None:
        receipt = read_json("environment/version-receipt.json")
        self.assertTrue(receipt["versions_verified_only"])
        self.assertFalse(receipt["desktop_updated"])
        self.assertFalse(receipt["host_features_changed"])
        self.assertEqual(receipt["windows_sandbox"], "unavailable_read_only_audit")
        tools = read_json("tooling/executed-toolchain.json")
        self.assertTrue(tools["inherited_tools_byte_stable"])
        self.assertFalse(tools["shared_skill_changed"])

    def test_19_protected_claims_and_route_remain_fail_closed(self) -> None:
        truth = read_json("phase-truth.json")
        self.assertTrue(all(value is False for value in truth["protected_claims"].values()))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["route_state"], "NO_SUCCESSOR_AUTHORIZED")
        route = read_json("workflow/route-preregistration.json")
        self.assertEqual(route["terminal_route"]["state"], "NO_SUCCESSOR_AUTHORIZED")
        self.assertEqual(route["tasks_created"], route["outbound_messages"])
        self.assertEqual(route["tasks_created"], 0)

    def test_20_full_and_minimal_validators_accept_candidate(self) -> None:
        full = validator.validate(PHASE, allow_pending_snapshot=True, require_report=True)
        mini = minimal.verify(PHASE, allow_pending_snapshot=True)
        self.assertTrue(full["valid"], full["issues"])
        self.assertTrue(mini["valid"], mini["issues"])


if __name__ == "__main__":
    unittest.main()

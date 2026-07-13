from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v642-v3"
SOURCE = "577af4c7f4c71d1e93cccac4b36686388a48989e"
X1 = "3056f7936f407e0a300ef735fa818b06ea20a347"
EXPECTED = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}


def load(rel: str) -> dict:
    return json.loads((PHASE / rel).read_text(encoding="utf-8"))


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def import_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not import {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestGhcFamilyV642V3(unittest.TestCase):
    def test_01_x1_freeze_and_x2_truth_are_separate(self) -> None:
        x1 = load("x1-proposals.json")
        x2 = load("x2-proposal-ledger.json")
        self.assertEqual(x1["source_revision"], SOURCE)
        self.assertEqual(x2["source_revision"], SOURCE)
        self.assertEqual(x2["x1_commit"], X1)
        self.assertFalse(x1["expected_counts_are_results"])
        self.assertEqual(Counter(row["expected_disposition"] for row in x1["proposals"]), Counter(EXPECTED))
        self.assertEqual(x2["disposition_counts"], EXPECTED)

    def test_02_frozen_chain_has_one_hundred_unique_titles(self) -> None:
        chain = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(chain["proposal_count"], len(chain["records"]))
        self.assertEqual(chain["proposal_count"], 100)
        self.assertEqual(chain["version_counts"]["v642-v3"], 10)
        self.assertEqual(len({row["title"] for row in chain["records"]}), 100)

    def test_03_project_context_keeps_future_and_projectless_lanes_bounded(self) -> None:
        context = load("workflow/project-context-capability-register.json")
        vectors = load("workflow/project-boundary-mutation-vectors.json")
        self.assertEqual(context["active"][0]["project"], "codex.")
        self.assertTrue(all(row["route_state"] == "STANDBY" for row in context["standby_projectless"]))
        self.assertEqual({row["task_label"] for row in context["standby_projectless"]}, {"Elian Voss", "Nima Calder"})
        self.assertTrue(all(row["exists"] is False for row in context["future_not_existing"]))
        self.assertEqual(context["task_creation_by_this_phase"], 0)
        self.assertEqual(context["outbound_messages_before_terminal_validation"], 0)
        self.assertEqual(vectors["invalid_vectors_rejected"], 5)
        self.assertEqual(vectors["raw_task_identifiers"], 0)

    def test_04_scheduler_is_six_seat_eight_phase_and_terminal(self) -> None:
        schedule = load("workflow/six-seat-round-robin.json")
        horizon = load("workflow/terminal-horizon-receipt.json")
        self.assertEqual(len(schedule["seats"]), 6)
        self.assertEqual(schedule["assignment_count"], len(schedule["assignments"]))
        self.assertEqual(schedule["assignment_count"], 150)
        self.assertEqual(schedule["assignments"][0]["phase_id"], "v642-v3")
        self.assertEqual(schedule["assignments"][-1]["phase_id"], "v660-v8")
        self.assertTrue(schedule["assignments"][-1]["terminal"])
        self.assertTrue(all(1 <= row["phase"] <= 8 for row in schedule["assignments"]))
        self.assertFalse(schedule["v9_permitted"])
        self.assertEqual(horizon["terminal_rows"], 1)
        self.assertFalse(horizon["post_terminal_authorized"])

    def test_05_permission_intersection_rejects_privilege_union(self) -> None:
        model = load("security/permission-envelope-model.json")
        vectors = load("security/least-authority-vectors.json")
        receipt = load("security/effective-authority-receipt.json")
        self.assertEqual(model["composition"], "intersection")
        self.assertFalse(model["permission_union_allowed"])
        self.assertTrue(model["deny_precedence"])
        self.assertTrue(model["exact_gate_precedence"])
        self.assertEqual((vectors["allowed_count"], vectors["rejected_count"]), (1, 5))
        self.assertTrue(receipt["owned_write_allowed"])
        self.assertFalse(receipt["sibling_write_allowed"])
        self.assertFalse(receipt["elevation"] or receipt["host_security_changed"] or receipt["destructive_action"])

    def test_06_gmut_exchange_current_is_structural_only(self) -> None:
        contract = load("physics/sector-exchange-current-contract.json")
        vectors = load("physics/bianchi-residual-vectors.json")
        boundary = load("physics/gmut-claim-boundary.json")
        self.assertEqual(contract["model_class"], "typed scalar-tensor EFT research scaffold")
        self.assertTrue(contract["pair_exchange_antisymmetry_required"])
        self.assertFalse(contract["empirically_confirmed"])
        self.assertTrue(vectors["vectors"][0]["accepted"])
        self.assertFalse(any(row["accepted"] for row in vectors["vectors"][1:]))
        self.assertFalse(any(boundary[key] for key in ["detected_force", "unique_prediction", "empirical_gmut_confirmation", "theory_of_everything", "proof_or_canon"]))

    def test_07_builder_exchange_helper_rejects_nonclosure(self) -> None:
        builder = import_script("project_round_robin", "ghc_family_project_round_robin.py")
        valid = {"sector_divergences": {"a": 1.0, "b": -1.0}, "pair_exchange": {"a->b": 1.0, "b->a": -1.0}}
        invalid = {"sector_divergences": {"a": 1.0, "b": -0.5}, "pair_exchange": {"a->b": 1.0, "b->a": -1.0}}
        self.assertEqual(builder.exchange_current_result(valid), (True, 0.0))
        self.assertFalse(builder.exchange_current_result(invalid)[0])

    def test_08_calibration_distinguishes_synthetic_failures(self) -> None:
        contract = load("empirical/synthetic-calibration-contract.json")
        vectors = load("empirical/calibration-vectors.json")
        boundary = load("empirical/calibration-claim-boundary.json")
        self.assertEqual(contract["mode"], "deterministic_synthetic_only")
        self.assertTrue(contract["shared_generator_evaluator_common_mode_possible"])
        self.assertEqual([row["passes_bounded_uniformity_fixture"] for row in vectors["vectors"]], [True, False, False])
        self.assertTrue(vectors["expected_classifications_correct"])
        self.assertEqual(boundary["disposition"], "represented")
        self.assertEqual(boundary["real_measurement_rows"], boundary["real_likelihoods"])
        self.assertEqual(boundary["real_likelihoods"], boundary["real_fits"])
        self.assertEqual(boundary["real_fits"], 0)
        self.assertFalse(boundary["empirical_gmut_confirmation"])

    def test_09_thos_is_cluster_aware_but_has_zero_real_arms(self) -> None:
        protocol = load("thos/cluster-randomized-protocol.json")
        budget = load("thos/multiplicity-sequential-budget.json")
        vectors = load("thos/cluster-mutation-vectors.json")
        gap = load("thos/real-arm-gap.json")
        self.assertTrue(protocol["intracluster_correlation_required"])
        self.assertEqual(protocol["real_clusters"], protocol["real_arm_runs"])
        self.assertEqual(protocol["real_arm_runs"], 0)
        self.assertAlmostEqual(sum(budget["alpha_spending"]), budget["familywise_alpha"])
        self.assertFalse(budget["post_hoc_outcomes_allowed"])
        self.assertEqual(vectors["mutations_rejected"], 6)
        self.assertEqual(gap["state"], "open_gap")
        self.assertFalse(any(gap[key] for key in ["superiority_established", "agi", "asi", "consciousness", "personhood"]))

    def test_10_freed_id_races_fail_closed_without_production_claim(self) -> None:
        machine = load("freed-id/key-status-holder-state-machine.json")
        vectors = load("freed-id/revocation-race-vectors.json")
        boundary = load("freed-id/production-boundary.json")
        self.assertEqual(machine["mode"], "synthetic_structural_only")
        self.assertTrue(machine["revocation_precedence"])
        self.assertEqual(machine["real_cryptographic_operations"], 0)
        self.assertEqual((vectors["synthetic_accepts"], vectors["synthetic_rejections"]), (1, 6))
        self.assertTrue(all(boundary[key] == 0 for key in ["real_keys", "real_proofs", "live_resolvers", "live_status_or_revocation_services", "interoperability_partners", "independent_security_reviews"]))
        self.assertFalse(boundary["privacy_assurance"] or boundary["trust_governance_established"] or boundary["cryptographic_assurance"])

    def test_11_cbr_sunset_defers_to_exact_authority(self) -> None:
        sunset = load("cbr/delegated-authority-sunset-register.json")
        appeals = load("cbr/intergenerational-appeal-vectors.json")
        gate = load("cbr/authority-legitimacy-gate.json")
        self.assertEqual(sunset["default_on_expiry"], "defer")
        self.assertFalse(sunset["silent_renewal_allowed"])
        self.assertFalse(sunset["system_may_appoint_representative"])
        self.assertTrue(sunset["maori_authority_nontransferable"])
        self.assertTrue(appeals["all_defer"] and appeals["all_remedies_preserved"])
        self.assertEqual(gate["state"], "exact_gate")
        self.assertIn("Māori authority", gate["boundary"])
        self.assertFalse(any(gate[key] for key in ["affected_party_authority_present", "future_generation_authorized_representative_present", "maori_authority_present", "cultural_ratification_present", "competent_legal_authority_present", "enacted_law"]))

    def test_12_entropy_categories_and_intervention_ladder_do_not_collapse(self) -> None:
        categories = load("thermo-psyche/entropy-category-map.json")
        ladder = load("thermo-psyche/intervention-ladder.json")
        vectors = load("thermo-psyche/non-equivalence-vectors.json")
        boundary = load("thermo-psyche/law-claim-boundary.json")
        self.assertFalse(categories["automatic_equivalence"])
        self.assertFalse(categories["telemetry_is_subjective_experience"])
        self.assertEqual(len(ladder["levels"]), 7)
        self.assertFalse(ladder["temporal_precedence_alone_proves_causation"])
        self.assertEqual(ladder["real_intervention_runs"], 0)
        self.assertEqual(vectors["invalid_equivalences_rejected"], 6)
        self.assertFalse(any(boundary[key] for key in ["fundamental_law_established", "consciousness_tensor", "consciousness", "personhood", "empirical_confirmation"]))

    def test_13_stage20_route_evidence_cannot_substitute(self) -> None:
        escrow = load("stage20/evidence-escrow-ledger.json")
        vectors = load("stage20/route-evidence-separation-vectors.json")
        reservation = load("stage20/independent-reproduction-reservation.json")
        terminal = load("stage20/terminal-verdict.json")
        self.assertFalse(escrow["route_receipt_is_scientific_evidence"])
        self.assertFalse(escrow["technical_score_may_override_exact_gate"])
        self.assertEqual(vectors["invalid_vectors_rejected"], 5)
        self.assertEqual(reservation["state"], "open")
        self.assertFalse(reservation["independent_team_present"])
        self.assertFalse(reservation["same_owner_snapshots_satisfy"])
        self.assertEqual(terminal["verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(terminal["deployment_authorized"] or terminal["successor_authorized_by_artifact"])

    def test_14_all_ninety_two_negatives_are_retained(self) -> None:
        negatives = load("retained-negative-register.json")
        self.assertEqual((negatives["inherited_count"], negatives["new_count"], negatives["negative_count"]), (68, 24, 92))
        self.assertEqual(negatives["negative_count"], len(negatives["negatives"]))
        self.assertTrue(negatives["all_retained"])
        self.assertFalse(negatives["erasure_permitted"])
        self.assertTrue(all(row["retained"] for row in negatives["negatives"]))
        execution = load("validation/execution-negative-log.json")
        self.assertEqual(execution["negative_count"], 4)
        self.assertEqual([row["negative_id"] for row in execution["negatives"]], ["V6423-N21", "V6423-N22", "V6423-N23", "V6423-N24"])
        self.assertTrue(all(row["preserved"] for row in execution["negatives"]))

    def test_15_gate_register_preserves_five_plus_six(self) -> None:
        gates = load("exact-open-gate-register.json")
        self.assertEqual((gates["open_gap_count"], gates["exact_gate_count"]), (5, 6))
        self.assertEqual(Counter(row["gate_class"] for row in gates["gates"]), Counter({"open_gap": 5, "exact_gate": 6}))
        self.assertEqual(gates["silently_closed"], 0)
        self.assertTrue(all(row["state"] in {"open", "deferred"} for row in gates["gates"]))

    def test_16_normalized_manifest_hashes_match(self) -> None:
        manifest = load("reproduction/semantic-normalization-manifest.json")
        actual = {rel: normalized_sha256(PHASE / rel) for rel in manifest["hashes"]}
        self.assertEqual(actual, manifest["hashes"])
        aggregate = hashlib.sha256("".join(f"{rel}:{actual[rel]}\n" for rel in sorted(actual)).encode()).hexdigest()
        self.assertEqual(aggregate, manifest["aggregate_sha256"])
        self.assertEqual(manifest["artifact_count"], len(actual))
        self.assertFalse(manifest["absolute_paths_required"])
        self.assertFalse(manifest["independent_team_reproduction"])

    def test_17_overview_and_report_meet_structural_floor(self) -> None:
        overview = (PHASE / "v642-v3-integrated-overview.md").read_text(encoding="utf-8")
        report = (PHASE / "deliverables/v642-v3-project-round-robin-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b\w+[\w'-]*\b", overview)), 1800)
        for token in ['lang="en"', 'class="skip-link"', "<main", "<nav", "<caption>", 'scope="col"']:
            self.assertIn(token, report)
        self.assertIn("not a complete WCAG conformance assessment", report)

    def test_18_source_statuses_and_references_close(self) -> None:
        source = load("sources/source-ledger.json")
        inherited = json.loads((ROOT / source["inherited_ledger"]).read_text(encoding="utf-8"))
        ids = {row["source_id"] for row in inherited["sources"]} | {row["source_id"] for row in source["added_sources"]}
        refs = {ref for proposal in load("x1-proposals.json")["proposals"] for ref in proposal["authoritative_source_needs"]}
        self.assertEqual(source["effective_source_count"], len(ids))
        self.assertEqual(source["effective_source_count"], 46)
        self.assertFalse(refs - ids)
        self.assertEqual(source["effective_status_counts"], {"current": 23, "stable": 19, "draft": 3, "watch": 1})

    def test_19_builder_decision_helpers_fail_closed(self) -> None:
        builder = import_script("project_round_robin_helpers", "ghc_family_project_round_robin.py")
        allowed, reason = builder.effective_authority({"action": "write", "actor_owner": "Eiren", "required_owner": "Eiren", "envelopes": [["write"], ["write"]]})
        self.assertTrue(allowed)
        self.assertEqual(reason, "intersection_allows")
        rejected, reason = builder.effective_authority({"action": "write", "actor_owner": "Eiren", "required_owner": "Eiren", "envelopes": [["write"], ["read"]]})
        self.assertFalse(rejected)
        self.assertEqual(reason, "permission_intersection_empty")
        decision, reasons = builder.credential_decision({"status": "revoked", "presented_key": "new", "allowed_keys": ["new"], "holder_binding": True, "replay_seen": False, "clock_skew_seconds": 0, "max_clock_skew_seconds": 30, "resolver_freshness_seconds": 1, "max_resolver_freshness_seconds": 60})
        self.assertEqual(decision, "reject")
        self.assertIn("status_revoked", reasons)

    def test_20_full_and_minimal_validators_accept_candidate(self) -> None:
        full = import_script("project_round_robin_validator", "ghc_family_project_round_robin_validator.py")
        minimal = import_script("project_round_robin_minimal", "ghc_family_project_round_robin_minimal.py")
        state = load("x2-proposal-ledger.json")["snapshot_state"]
        allow_pending = state != "verified"
        full_result = full.validate(PHASE, allow_pending_snapshot=allow_pending, require_report=True)
        minimal_result = minimal.verify(PHASE, allow_pending_snapshot=allow_pending)
        self.assertTrue(full_result["valid"], full_result["issues"])
        self.assertTrue(minimal_result["valid"], minimal_result["issues"])


if __name__ == "__main__":
    unittest.main()

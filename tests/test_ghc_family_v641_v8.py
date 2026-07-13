from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "elian-voss" / "v641-v8"


def load(rel: str) -> dict:
    return json.loads((PHASE / rel).read_text(encoding="utf-8"))


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class TestGhcFamilyV641V8(unittest.TestCase):
    def test_01_x1_has_ten_complete_distinct_records(self) -> None:
        data = load("x1-proposals.json")
        required = {"hypothesis", "null_or_failure", "approval_class", "execution_lane", "authoritative_source_needs", "deliverables", "test_falsifier_or_gate", "rollback_or_recovery", "expected_disposition", "novelty_against_prior_chain"}
        self.assertEqual(data["proposal_count"], 10)
        self.assertEqual(len(data["proposals"]), 10)
        self.assertEqual(len({row["proposal_id"] for row in data["proposals"]}), 10)
        self.assertTrue(all(required <= set(row) for row in data["proposals"]))
        self.assertEqual(data["source_revision"], "008fb47054eb313a439999d5a5b4ddc2e863e187")

    def test_02_x1_novelty_audit_covers_sixty_predecessors(self) -> None:
        data = load("provenance/prior-proposal-collision-audit.json")
        self.assertEqual(data["prior_phase_counts"]["total"], 60)
        self.assertEqual(data["exact_title_collisions"], 0)
        self.assertLess(data["maximum_title_jaccard"], 0.3)
        self.assertTrue(all(row["distinct"] for row in data["checks"]))

    def test_03_source_ledger_status_and_refs_are_exact(self) -> None:
        source = load("sources/source-ledger.json")
        x1 = load("x1-proposals.json")
        self.assertEqual(source["source_count"], 31)
        self.assertEqual(Counter(row["status_class"] for row in source["sources"]), Counter(source["status_counts"]))
        source_ids = {row["source_id"] for row in source["sources"]}
        self.assertFalse({ref for row in x1["proposals"] for ref in row["authoritative_source_needs"]} - source_ids)

    def test_04_frozen_chain_and_retraction_replay_are_monotonic(self) -> None:
        chain = load("provenance/frozen-chain-proposal-index.json")
        replay = load("provenance/source-retraction-replay.json")
        self.assertEqual(chain["proposal_count"], 70)
        self.assertEqual(chain["version_counts"], {f"v{n}": 10 for n in range(2, 9)})
        self.assertEqual(chain["exact_duplicate_titles"], [])
        self.assertEqual(replay["mutation_count"], 8)
        self.assertTrue(replay["all_required_downgrades_observed"])
        self.assertEqual(replay["silently_retained_strength"], 0)

    def test_05_authority_quorum_counts_roots_not_documents(self) -> None:
        data = load("provenance/authority-liveness-quorum.json")
        self.assertTrue(data["all_quorums_current"])
        self.assertTrue(data["independence_is_root_based_not_document_count"])
        self.assertTrue(data["expiry_or_retraction_requires_replay"])

    def test_06_gmut_obligations_keep_canonical_structural_boundary(self) -> None:
        data = load("physics/canonical-gmut-obligation-matrix.json")
        self.assertEqual(data["coverage"], {"declared": 8, "linked_to_assumption": 8, "linked_to_rejecting_test": 8})
        self.assertFalse(data["empirical_confirmation"])
        self.assertFalse(data["detected_force"])
        self.assertFalse(data["unique_prediction"])
        self.assertFalse(data["theory_of_everything"])

    def test_07_gmut_mutation_score_retains_degeneracy_boundary(self) -> None:
        tensor = load("physics/tensor-unit-covariance-mutations.json")
        stability = load("physics/stability-identifiability-kill-matrix.json")
        assumptions = load("physics/assumption-trace.json")
        self.assertTrue(tensor["all_killed"])
        self.assertTrue(stability["all_killed"])
        self.assertEqual(stability["mutation_score"], 1.0)
        self.assertFalse(stability["empirical_stability_or_identifiability"])
        self.assertEqual(assumptions["unlinked_obligations"], [])

    def test_08_empirical_adapter_has_integrity_manifest_and_zero_fit(self) -> None:
        manifest = load("empirical/dataset-integrity-manifest.json")
        drift = load("empirical/schema-license-drift-vectors.json")
        receipt = load("empirical/adapter-zero-fit-receipt.json")
        self.assertEqual(manifest["real_measurement_rows"], 0)
        self.assertFalse(manifest["content_downloaded"])
        self.assertTrue(drift["all_quarantined"])
        self.assertEqual(receipt["real_measurement_rows_parsed"], 0)
        self.assertFalse(receipt["likelihood_executed"])
        self.assertFalse(receipt["parameter_fit_executed"])
        self.assertEqual(receipt["disposition"], "represented")

    def test_09_thos_estimand_budget_and_attrition_are_proxy_only(self) -> None:
        lock = load("thos/estimand-lock.json")
        budget = load("thos/matched-budget-accounting.json")
        attrition = load("thos/attrition-missingness-vectors.json")
        gap = load("thos/real-arm-gap.json")
        self.assertTrue(lock["locked_before_unseal"])
        self.assertTrue(lock["synthetic_only"])
        self.assertEqual(lock["real_arm_runs"], 0)
        self.assertTrue(budget["declared_budgets_equal"])
        self.assertTrue(attrition["all_rejected_before_unseal"])
        self.assertFalse(gap["real_arms_present"])

    def test_10_freed_id_lifecycle_is_structural_and_open(self) -> None:
        lifecycle = load("freed-id/lifecycle-product-automaton.json")
        resolver = load("freed-id/resolver-freshness-cache-vectors.json")
        matrix = load("freed-id/status-privacy-interoperability-matrix.json")
        gate = load("freed-id/production-trust-gate.json")
        self.assertTrue(lifecycle["all_invalid_rejected"])
        self.assertEqual(lifecycle["real_credentials"], 0)
        self.assertTrue(resolver["all_rejected"])
        self.assertFalse(matrix["production_assurance"])
        self.assertEqual(gate["satisfied_count"], 0)
        self.assertEqual(gate["disposition"], "open_gap")

    def test_11_cbr_contestability_never_substitutes_authority(self) -> None:
        protocol = load("cbr/contestability-remedy-protocol.json")
        non_sub = load("cbr/recusal-authority-nonsubstitution.json")
        maori = load("cbr/maori-authority-boundary.json")
        self.assertEqual(protocol["algorithmic_live_resolutions"], 0)
        self.assertTrue(protocol["all_conflicts_deferred"])
        self.assertFalse(non_sub["system_can_substitute_for_affected_parties"])
        self.assertFalse(non_sub["system_can_substitute_for_maori_authority"])
        self.assertFalse(maori["Māori_authority_present"])
        self.assertFalse(maori["system_may_speak_for_Māori"])
        self.assertEqual(maori["decision"], "exact_gate")

    def test_12_security_vectors_are_bounded_and_recoverable(self) -> None:
        toctou = load("security/manifest-swap-toctou-vectors.json")
        links = load("security/link-reparse-boundary.json")
        recovery = load("security/recovery-rto-drill.json")
        self.assertTrue(toctou["all_detected"])
        self.assertFalse(toctou["exhaustive_security"])
        self.assertFalse(links["actual_links_created"])
        self.assertEqual(links["unsafe_vectors_rejected"], 4)
        self.assertTrue(recovery["pass"])
        self.assertEqual(recovery["destructive_commands"], 0)
        self.assertFalse(recovery["privilege_expansion"])

    def test_13_reproduction_commitment_matches_core_artifacts(self) -> None:
        data = load("reproduction/blinded-output-commitment.json")
        actual = {rel: normalized_sha256(PHASE / rel) for rel in data["normalized_hashes"]}
        self.assertEqual(actual, data["normalized_hashes"])
        aggregate = hashlib.sha256("".join(f"{key}:{actual[key]}\n" for key in sorted(actual)).encode()).hexdigest()
        self.assertEqual(aggregate, data["aggregate_sha256"])
        self.assertEqual(data["artifact_count"], len(actual))

    def test_14_reproduction_language_preserves_independent_gap(self) -> None:
        protocol = load("reproduction/external-executor-protocol.json")
        split = load("reproduction/common-mode-dependency-split.json")
        gap = load("reproduction/independent-team-gap.json")
        snapshots = load("reproduction/clean-snapshot-validation.json")
        receipt = load("validation/reproduction-validation.json")
        self.assertFalse(protocol["private_routes_required"])
        self.assertFalse(protocol["machine_specific_absolute_paths"])
        self.assertFalse(protocol["independent_result_returned"])
        self.assertFalse(split["independent_team_reproduction"])
        self.assertEqual(gap["gap"], "open")
        self.assertFalse(receipt["independent_team_reproduction"])
        self.assertEqual(receipt["independent_team_gap"], "open")
        if snapshots["state"] == "verified":
            evidence_commit = "a92c15d52a1324b1cf9ff73a3354cd0c40aab726"
            self.assertEqual(snapshots["source_commit"], evidence_commit)
            self.assertEqual(receipt["evidence_commit"], evidence_commit)
            self.assertEqual({row["snapshot_label"] for row in snapshots["snapshots"]}, {"evidence_a", "evidence_b"})
            self.assertTrue(all(row["clean"] and row["detached"] for row in snapshots["snapshots"]))

    def test_15_thermo_psyche_promotions_add_burdens_and_reject_shortcuts(self) -> None:
        state = load("thermo-psyche/promotion-state-machine.json")
        prohibited = load("thermo-psyche/prohibited-transition-vectors.json")
        register = load("thermo-psyche/classification-register.json")
        self.assertEqual(set(state["classes"]), {"category_barrier", "heuristic", "normative_principle", "operational_rule", "formal_invariant", "empirical_hypothesis"})
        self.assertTrue(state["every_promotion_adds_burden"])
        self.assertTrue(prohibited["all_rejected"])
        self.assertEqual(register["fundamental_physical_laws_established"], 0)
        self.assertEqual(register["consciousness_tensors_established"], 0)

    def test_16_stage20_cutsets_force_not_ready(self) -> None:
        cutsets = load("stage20/minimal-blocking-cutsets.json")
        mutations = load("stage20/stop-rule-mutations.json")
        board = load("stage20/terminal-evidence-board.json")
        self.assertEqual(cutsets["cutset_count"], 6)
        self.assertTrue(cutsets["every_cutset_blocks_ready"])
        self.assertTrue(mutations["all_rejected"])
        self.assertEqual(set(row["decision"] for row in board["board"]), {"pass", "fail", "defer"})
        self.assertEqual(board["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(board["stage20_complete"])

    def test_17_negatives_and_gates_are_retained_exactly(self) -> None:
        negatives = load("retained-negative-register.json")
        gates = load("exact-open-gate-register.json")
        self.assertEqual((negatives["inherited_count"], negatives["new_count"], negatives["negative_count"]), (20, 12, 32))
        self.assertTrue(negatives["all_retained"])
        self.assertTrue(all(row["retained"] for row in negatives["negatives"]))
        self.assertEqual((gates["open_gap_count"], gates["exact_gate_count"], gates["silently_closed"]), (5, 2, 0))

    def test_18_phase_truth_and_ledger_use_exact_outcome_classes(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        truth = load("phase-truth.json")
        expected = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
        self.assertEqual(ledger["disposition_counts"], expected)
        self.assertEqual(ledger["x1_commit"], "4bbfbcc069894f60a9392799bb0fb15c03e6c954")
        self.assertEqual(truth["disposition_counts"], expected)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(any(truth["protected_claims"].values()))

    def test_19_overview_and_static_report_meet_structural_floor(self) -> None:
        overview = (PHASE / "v641-v8-integrated-overview.md").read_text(encoding="utf-8")
        report = (PHASE / "deliverables/v641-v8-gate-resilience-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b\w+\b", overview)), 1800)
        for token in ['lang="en"', 'class="skip-link"', "<main", "<nav", "<caption>", 'scope="col"']:
            self.assertIn(token, report)
        self.assertIn("not a complete WCAG conformance assessment", report)

    def test_20_family_validator_accepts_current_state(self) -> None:
        module_path = ROOT / "scripts/ghc_family_gate_resilience_validator.py"
        spec = importlib.util.spec_from_file_location("v8_validator", module_path)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        state = load("x2-proposal-ledger.json")["snapshot_state"]
        report = module.validate(PHASE, allow_pending=state == "pending", require_report=True, output=None)
        self.assertTrue(report["valid"], report["issues"])


if __name__ == "__main__":
    unittest.main()

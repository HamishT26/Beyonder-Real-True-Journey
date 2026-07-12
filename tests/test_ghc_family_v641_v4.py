from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from scripts.ghc_family_evidence_lineage import (
    build_category_barrier_mutations,
    build_cbr_v4,
    build_claim_source_matrix,
    build_empirical_v4,
    build_equation_test_lineage,
    build_freed_id_v4,
    build_freshness_lineage_audit,
    build_metamorphic_scale_audit,
    build_security_v4,
    build_stage20_v4,
    build_thos_v4,
    build_tool_integrity_manifest,
)
from scripts.ghc_family_phase_evidence_validator import validate_phase


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "nima-calder" / "v641-v4"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class FrozenX1AndSourceLineageTests(unittest.TestCase):
    def test_x1_has_ten_frozen_independent_proposals(self) -> None:
        x1 = load("x1-proposals.json")
        required = {
            "proposal_id",
            "lane",
            "prior_v3_input",
            "hypothesis",
            "null",
            "authoritative_source_ids",
            "internal_inputs",
            "deliverables",
            "tests_and_falsifiers",
            "approval_class",
            "recovery",
            "protected_gates",
            "decision_rule",
            "x1_status",
        }
        proposals = x1["proposals"]
        self.assertEqual(x1["source_revision"], "01fd716b5f36a39cdc7763481459e75a09fcb077")
        self.assertEqual(len(proposals), 10)
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 10)
        self.assertTrue(all(required <= row.keys() for row in proposals))
        self.assertEqual({row["x1_status"] for row in proposals}, {"preregistered"})
        self.assertEqual(x1["active_and_standby"]["active_owner"], "Nima Calder")
        self.assertEqual(x1["active_and_standby"]["collaboration_subagents"], "not_authorized_and_not_spawned")

    def test_current_source_distinctions_are_explicit(self) -> None:
        ledger = load("sources/source-ledger.json")
        by_id = {row["source_id"]: row for row in ledger["sources"]}
        self.assertEqual(ledger["source_count"], 35)
        self.assertIn("4.7", by_id["V4-S02"]["version_or_date"])
        self.assertIn("2026", by_id["V4-S10"]["title"])
        self.assertIn("12 December 2024", by_id["V4-S33"]["version_or_date"])
        self.assertEqual(by_id["V4-S11"]["status"], "stable_recommendation")
        self.assertIn("watch_item", by_id["V4-S16"]["status"])
        self.assertIn("DR1 public spectroscopy", by_id["V4-S05"]["version_or_date"])

    def test_claim_source_and_freshness_artifacts_rebuild(self) -> None:
        x1 = load("x1-proposals.json")
        sources = load("sources/source-ledger.json")
        self.assertEqual(
            build_claim_source_matrix(x1, sources),
            load("provenance/claim-source-matrix.json"),
        )
        self.assertEqual(
            build_freshness_lineage_audit(sources),
            load("provenance/freshness-lineage-audit.json"),
        )
        audit = load("provenance/freshness-lineage-audit.json")
        self.assertTrue(audit["passed"])
        self.assertTrue(
            all(not row["adds_independent_vote"] for row in audit["current_version_corrections"])
        )


class MindAndEmpiricalTests(unittest.TestCase):
    def test_equation_lineage_and_mutations_rebuild(self) -> None:
        lineage = build_equation_test_lineage(ROOT)
        mutations = build_category_barrier_mutations(ROOT)
        self.assertEqual(lineage, load("physics/equation-test-lineage.json"))
        self.assertEqual(mutations, load("physics/category-barrier-mutations.json"))
        self.assertTrue(lineage["passed"])
        self.assertTrue(mutations["passed"])
        self.assertEqual(mutations["fixture_count"], 6)
        self.assertFalse(mutations["raw_mutations_retained"])

    def test_metamorphic_scale_audit_rebuilds(self) -> None:
        artifact = build_metamorphic_scale_audit()
        self.assertEqual(artifact, load("physics/metamorphic-scale-audit.json"))
        self.assertTrue(artifact["passed"])
        self.assertGreaterEqual(artifact["case_count"], 13)
        self.assertGreater(artifact["convergence"]["observed_order"], 2.5)

    def test_empirical_smoke_stops_before_fit(self) -> None:
        adapters, smoke, leak = build_empirical_v4()
        self.assertEqual(adapters, load("empirical/adapter-readiness.json"))
        self.assertEqual(smoke, load("empirical/baseline-smoke-manifest.json"))
        self.assertEqual(leak, load("empirical/inference-leak-audit.json"))
        self.assertTrue(smoke["all_no_download"])
        self.assertTrue(smoke["all_baselines_pending"])
        self.assertEqual(smoke["disposition"], "open_gap")
        self.assertFalse(leak["fit_complete_receipt_present"])
        self.assertFalse(leak["empirical_gmut_confirmation"])


class BodyHeartAndSecurityTests(unittest.TestCase):
    def test_thos_allocation_is_outcome_blind_and_synthetic(self) -> None:
        protocol, allocation, paired, proxy = build_thos_v4()
        self.assertEqual(protocol, load("thos/matched-budget-protocol.json"))
        self.assertEqual(allocation, load("thos/allocation-missingness-audit.json"))
        self.assertEqual(paired, load("thos/synthetic-paired-analysis.json"))
        self.assertEqual(proxy, load("thos/synthetic-scorer-proxy.json"))
        self.assertTrue(allocation["outcome_blind"])
        self.assertEqual(allocation["live_arm_output_count"], 0)
        self.assertEqual(allocation["disposition"], "represented")
        self.assertFalse(paired["winner_declared"])

    def test_freed_id_transitions_fail_closed(self) -> None:
        generated = build_freed_id_v4()
        relative = [
            "freed-id/minimum-profile.json",
            "freed-id/conformance-vectors.json",
            "freed-id/conformance-report.json",
            "freed-id/cryptographic-assurance-boundary.json",
            "freed-id/assurance-transition-model.json",
            "freed-id/transition-vectors.json",
            "freed-id/transition-report.json",
        ]
        self.assertEqual(list(generated), [load(path) for path in relative])
        model = generated[4]
        report = generated[6]
        self.assertEqual(model["highest_local_state"], "proof_shaped")
        self.assertFalse(model["cryptographic_verification_performed"])
        self.assertFalse(model["deployment_performed"])
        self.assertTrue(report["all_matched"])
        self.assertIn("no_personhood", report["boundary"])

    def test_cbr_non_transfer_preserves_maori_authority(self) -> None:
        generated = build_cbr_v4()
        relative = [
            "cbr/legitimacy-crosswalk.json",
            "cbr/conflict-cases.json",
            "cbr/conflict-report.json",
            "cbr/authority-veto-matrix.json",
            "cbr/consent-authority-graph.json",
            "cbr/non-transfer-invariants.json",
            "cbr/authority-report.json",
        ]
        self.assertEqual(list(generated), [load(path) for path in relative])
        graph, invariants, report = generated[4:]
        self.assertTrue(graph["all_matched"])
        self.assertEqual(report["disposition"], "exact_gate")
        self.assertIn("Māori authority", invariants["maori_authority_boundary"])
        self.assertIn("Māori authority", report["maori_authority_boundary"])

    def test_security_and_tool_integrity_rebuild(self) -> None:
        red_team, recovery, adversarial, manifest = build_security_v4(ROOT)
        self.assertEqual(red_team, load("security/red-team.json"))
        self.assertEqual(recovery, load("security/recovery-drill.json"))
        self.assertEqual(adversarial, load("security/adversarial-fixtures.json"))
        self.assertEqual(manifest, load("security/tool-integrity-manifest.json"))
        self.assertEqual(manifest, build_tool_integrity_manifest(ROOT))
        self.assertTrue(manifest["all_passed"])
        self.assertTrue(red_team["all_matched"])
        self.assertFalse(adversarial["raw_fixture_retained"])
        self.assertIn("not an exhaustive security scan", red_team["boundary"])


class Stage20ReproductionAndReportTests(unittest.TestCase):
    def test_stage20_lineage_and_promotion_rules_rebuild(self) -> None:
        status = load("reproduction/reproduction-report.json")["status"]
        board, lineage, drill, rehearsal = build_stage20_v4("2026-07-13", "Nima Calder", status)
        self.assertEqual(board, load("stage20/evidence-board.json"))
        self.assertEqual(lineage, load("stage20/claim-lineage.json"))
        self.assertEqual(drill, load("stage20/promotion-monotonicity-drill.json"))
        self.assertEqual(rehearsal, load("stage20/decision-rehearsal.json"))
        self.assertTrue(lineage["negative_evidence_retained"])
        self.assertTrue(drill["all_matched"])
        self.assertTrue(rehearsal["no_forbidden_e4"])
        self.assertTrue(rehearsal["all_scenarios_non_predictive"])

    def test_x2_ledger_keeps_all_four_truth_classes(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(
            set(ledger["summary"]),
            {"completed", "represented", "open_gap", "exact_gate"},
        )
        self.assertEqual(
            set(row["disposition"] for row in ledger["outcomes"]),
            {"completed", "represented", "open_gap", "exact_gate"},
        )

    def test_environment_receipt_does_not_update_codex(self) -> None:
        receipt = load("environment/version-receipt.json")
        self.assertFalse(receipt["codex_desktop_updated_by_phase"])
        self.assertTrue(receipt["codex_desktop_version"])
        self.assertTrue(receipt["codex_cli_version"])

    def test_reproduction_never_claims_independent_team(self) -> None:
        report = load("reproduction/reproduction-report.json")
        parity = load("reproduction/hash-parity.json")
        self.assertFalse(report["independent_team"])
        if report["status"] == "verified_local_repeatability":
            self.assertTrue(report["hash_parity_passed"])
            self.assertTrue(parity["all_match"])
        else:
            self.assertEqual(report["status"], "pending_clean_snapshot")

    def test_accessible_report_is_static_and_identity_current(self) -> None:
        report = (PHASE / "deliverables" / "v641-v4-evidence-report.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="en-NZ">', report)
        self.assertIn('class="skip"', report)
        self.assertGreaterEqual(report.count("<caption>"), 6)
        self.assertIn("Nima Calder", report)
        self.assertIn("Evidence lineage extensions", report)
        self.assertNotIn("<script", report.lower())

    def test_required_human_readable_artifacts_exist(self) -> None:
        for relative in (
            "v641-v4-integrated-overview.md",
            "wellbeing-check.md",
            "phase-truth.md",
            "complete-incomplete-checklist.md",
            "closeout-receipt.md",
        ):
            self.assertTrue((PHASE / relative).is_file(), relative)
        overview = (PHASE / "v641-v4-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b\w+\b", overview)), 1500)

    def test_phase_validator_passes(self) -> None:
        result = validate_phase(PHASE)
        self.assertTrue(result["valid"], result["issues"])

    def test_public_phase_has_no_raw_ids_paths_or_secret_shapes(self) -> None:
        patterns = [
            re.compile(
                r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
                re.IGNORECASE,
            ),
            re.compile(r"\b[A-Za-z]:\\"),
            re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
            re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        ]
        for path in PHASE.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".tex"}:
                text = path.read_text(encoding="utf-8", errors="replace")
                for pattern in patterns:
                    self.assertIsNone(pattern.search(text), path)


if __name__ == "__main__":
    unittest.main()

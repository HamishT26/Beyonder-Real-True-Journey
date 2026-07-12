from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from scripts.ghc_family_evidence_cycle import build_source_independence
from scripts.ghc_family_evidence_refresh import (
    build_cbr_v3,
    build_empirical_readiness,
    build_freed_id_v3,
    build_security_v3,
    build_sensitivity_envelope,
    build_source_dedup_audit,
    build_stage20,
    build_thos,
    build_variational_trace,
)
from scripts.ghc_family_phase_evidence_validator import validate_phase


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "elian-voss" / "v641-v3"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class FrozenX1AndProvenanceTests(unittest.TestCase):
    def test_ten_independent_v3_proposals_have_frozen_decision_rules(self) -> None:
        x1 = load("x1-proposals.json")
        proposals = x1["proposals"]
        required = {
            "proposal_id",
            "lane",
            "prior_v2_input",
            "hypothesis",
            "null",
            "authoritative_source_ids",
            "deliverables",
            "tests_and_falsifiers",
            "approval_class",
            "recovery",
            "protected_gates",
            "decision_rule",
            "x1_status",
        }
        self.assertEqual(len(proposals), 10)
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 10)
        self.assertTrue(all(required <= row.keys() for row in proposals))
        self.assertEqual({row["x1_status"] for row in proposals}, {"preregistered"})

    def test_source_refresh_records_material_version_changes(self) -> None:
        ledger = load("sources/source-ledger.json")
        self.assertEqual(ledger["source_count"], 33)
        by_id = {row["source_id"]: row for row in ledger["sources"]}
        self.assertIn("4.7", by_id["V3-S02"]["version_or_date"])
        self.assertIn("2026", by_id["V3-S10"]["title"])
        self.assertEqual(by_id["V3-S11"]["status"], "stable_recommendation")
        self.assertIn("watch_item", by_id["V3-S13"]["status"])

    def test_dependency_and_dedup_artifacts_are_rebuildable(self) -> None:
        ledger = load("sources/source-ledger.json")
        self.assertEqual(
            build_source_independence(ledger),
            load("provenance/source-independence-graph.json"),
        )
        self.assertEqual(
            build_source_dedup_audit(ledger),
            load("provenance/source-dedup-audit.json"),
        )
        audit = load("provenance/source-dedup-audit.json")
        self.assertTrue(audit["passed"])
        self.assertTrue(
            all(not row["adds_independent_vote"] for row in audit["version_corrections"])
        )


class MindAndEmpiricalTests(unittest.TestCase):
    def test_variational_trace_and_negative_matrix_match(self) -> None:
        artifact = load("physics/variational-trace-audit.json")
        self.assertEqual(build_variational_trace(ROOT), artifact)
        self.assertTrue(artifact["passed"])
        self.assertEqual(len(artifact["negative_fixtures"]), 4)

    def test_sensitivity_envelope_rejects_boundary_failures(self) -> None:
        artifact = load("physics/conservation-sensitivity-envelope.json")
        self.assertEqual(build_sensitivity_envelope(), artifact)
        self.assertTrue(artifact["passed"])
        self.assertEqual(artifact["case_count"], 9)

    def test_empirical_readiness_stops_before_data_or_likelihood(self) -> None:
        manifest, readiness = build_empirical_readiness()
        self.assertEqual(manifest, load("empirical/adapter-readiness.json"))
        self.assertEqual(readiness, load("empirical/baseline-readiness-matrix.json"))
        self.assertTrue(readiness["all_no_download"])
        self.assertTrue(readiness["all_baselines_pending"])
        self.assertEqual(manifest["disposition"], "open_gap")


class BodyHeartAndSecurityTests(unittest.TestCase):
    def test_thos_protocol_retains_unrun_blind_arms(self) -> None:
        protocol, audit, proxy = build_thos()
        self.assertEqual(protocol, load("thos/matched-budget-protocol.json"))
        self.assertEqual(audit, load("thos/power-contamination-audit.json"))
        self.assertEqual(proxy, load("thos/synthetic-scorer-proxy.json"))
        self.assertTrue(audit["all_matched"])
        self.assertEqual(audit["blind_arm_count"], 0)
        self.assertTrue(all(row["status"].startswith("pending_") for row in protocol["arms"]))

    def test_freed_id_keeps_crypto_and_personhood_boundaries_open(self) -> None:
        profile, vectors, report, assurance = build_freed_id_v3()
        self.assertEqual(profile, load("freed-id/minimum-profile.json"))
        self.assertEqual(vectors, load("freed-id/conformance-vectors.json"))
        self.assertEqual(report, load("freed-id/conformance-report.json"))
        self.assertEqual(assurance, load("freed-id/cryptographic-assurance-boundary.json"))
        self.assertTrue(report["all_matched"])
        self.assertEqual(report["vector_count"], 10)
        open_layers = {row["layer"]: row["state"] for row in assurance["layers"]}
        self.assertTrue(open_layers["proof_verification"].startswith("open_gap"))
        self.assertTrue(open_layers["deployment"].startswith("exact_gate"))

    def test_cbr_veto_matrix_preserves_maori_authority(self) -> None:
        crosswalk, cases, report, matrix = build_cbr_v3()
        self.assertEqual(crosswalk, load("cbr/legitimacy-crosswalk.json"))
        self.assertEqual(cases, load("cbr/conflict-cases.json"))
        self.assertEqual(report, load("cbr/conflict-report.json"))
        self.assertEqual(matrix, load("cbr/authority-veto-matrix.json"))
        self.assertTrue(matrix["all_matched"])
        self.assertEqual(matrix["disposition"], "exact_gate")
        self.assertIn("Māori authority", matrix["maori_authority_boundary"])

    def test_adversarial_fixtures_are_ephemeral_and_detected(self) -> None:
        red_team, recovery, adversarial = build_security_v3()
        self.assertEqual(red_team, load("security/red-team.json"))
        self.assertEqual(recovery, load("security/recovery-drill.json"))
        self.assertEqual(adversarial, load("security/adversarial-fixtures.json"))
        self.assertTrue(red_team["all_matched"])
        self.assertTrue(adversarial["all_matched"])
        self.assertFalse(adversarial["raw_fixture_retained"])
        self.assertIn("not an exhaustive security scan", red_team["boundary"])


class Stage20ReproductionAndReportTests(unittest.TestCase):
    def test_stage20_expiry_and_contradiction_drill_matches(self) -> None:
        board, rehearsal, drill = build_stage20("2026-07-13", "Elian Voss")
        self.assertEqual(board, load("stage20/evidence-board.json"))
        self.assertEqual(rehearsal, load("stage20/decision-rehearsal.json"))
        self.assertEqual(drill, load("stage20/expiry-contradiction-drill.json"))
        self.assertTrue(drill["all_matched"])
        self.assertTrue(rehearsal["no_forbidden_e4"])
        self.assertTrue(rehearsal["all_scenarios_non_predictive"])

    def test_x2_ledger_retains_all_four_truth_classes(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(
            set(ledger["summary"]),
            {"completed", "represented", "open_gap", "exact_gate"},
        )
        self.assertTrue(all(row["x2_execution_receipt"] for row in ledger["outcomes"]))

    def test_environment_receipt_observes_without_updating_codex(self) -> None:
        receipt = load("environment/version-receipt.json")
        self.assertEqual(receipt["codex_desktop_version"], "26.707.3748.0")
        self.assertFalse(receipt["codex_desktop_updated_by_phase"])

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
        report = (PHASE / "deliverables" / "v641-v3-evidence-report.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('<html lang="en-NZ">', report)
        self.assertIn('class="skip"', report)
        self.assertGreaterEqual(report.count("<caption>"), 5)
        self.assertIn("Elian Voss", report)
        self.assertIn("Evidence refresh extensions", report)
        self.assertNotIn("<script", report.lower())
        self.assertNotIn("Sable Rook", report)

    def test_phase_validator_passes(self) -> None:
        result = validate_phase(PHASE)
        self.assertTrue(result["valid"], result["issues"])

    def test_public_phase_contains_no_raw_ids_paths_or_secret_shapes(self) -> None:
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

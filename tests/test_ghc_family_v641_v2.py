from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from scripts.ghc_family_evidence_cycle import (
    build_source_independence,
    build_stability_sweep,
)
from scripts.ghc_family_phase_evidence_validator import validate_phase


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v641-v2"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class PreregistrationAndProvenanceTests(unittest.TestCase):
    def test_ten_concrete_preregistered_proposals_have_required_fields(self) -> None:
        proposals = load("x1-proposals.json")["proposals"]
        required = {
            "proposal_id",
            "hypothesis",
            "null",
            "authoritative_source_ids",
            "deliverables",
            "tests_and_falsifiers",
            "approval_class",
            "recovery",
            "protected_gates",
            "x1_status",
        }
        self.assertEqual(len(proposals), 10)
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 10)
        self.assertTrue(all(required <= row.keys() for row in proposals))
        self.assertEqual({row["x1_status"] for row in proposals}, {"preregistered"})

    def test_source_independence_graph_is_rebuildable(self) -> None:
        ledger = load("sources/source-ledger.json")
        graph = load("provenance/source-independence-graph.json")
        self.assertEqual(build_source_independence(ledger), graph)
        self.assertEqual(graph["source_count"], 32)
        self.assertEqual(graph["authority_root_count"], 21)
        self.assertLess(graph["authority_root_count"], graph["source_count"])
        self.assertGreater(graph["duplicate_url_group_count"], 0)


class MindAndEmpiricalTests(unittest.TestCase):
    def test_canonical_gmut_audit_passes_but_makes_no_empirical_claim(self) -> None:
        audit = load("physics/canonical-gmut-audit.json")
        self.assertTrue(audit["passed"])
        self.assertTrue(audit["negative_fixture"]["rejected_as_expected"])
        self.assertIn("no empirical GMUT confirmation", audit["boundaries"])

    def test_stability_sweep_retains_healthy_and_unhealthy_cases(self) -> None:
        artifact = load("physics/conservation-stability-sweep.json")
        self.assertEqual(build_stability_sweep(), artifact)
        self.assertTrue(artifact["passed"])
        self.assertEqual(len(artifact["stability_cases"]), 5)
        self.assertTrue(all(row["matched"] for row in artifact["stability_cases"]))

    def test_empirical_adapters_stop_before_likelihood(self) -> None:
        artifact = load("empirical/adapter-readiness.json")
        self.assertTrue(artifact["validation"]["valid"])
        self.assertEqual(len(artifact["adapters"]), 6)
        self.assertEqual(
            artifact["fit_status"], "NO_LIKELIHOOD_RUN_NO_EMPIRICAL_GMUT_CONFIRMATION"
        )
        self.assertNotIn("fit_complete", {row["status"] for row in artifact["adapters"]})
        self.assertEqual(artifact["disposition"], "open_gap")


class BodyHeartAndSecurityTests(unittest.TestCase):
    def test_thos_proxy_cannot_masquerade_as_performance(self) -> None:
        protocol = load("thos/matched-budget-protocol.json")
        proxy = load("thos/synthetic-scorer-proxy.json")
        self.assertTrue(all(row["status"].startswith("pending_") for row in protocol["arms"]))
        self.assertIn("not_agent_or_model_performance", proxy["interpretation_boundary"])
        self.assertEqual(proxy["disposition"], "represented")

    def test_freed_id_structural_vectors_reject_overclaims(self) -> None:
        report = load("freed-id/conformance-report.json")
        self.assertTrue(report["all_matched"])
        self.assertEqual(report["vector_count"], 7)
        rejected = {row["vector_id"] for row in report["results"] if not row["actual_accept"]}
        self.assertIn("consciousness-overclaim", rejected)
        self.assertIn("personhood-overclaim", rejected)
        self.assertIn("no_signature_verification", report["boundary"])

    def test_cbr_rehearsal_preserves_maori_and_legal_authority(self) -> None:
        report = load("cbr/conflict-report.json")
        self.assertTrue(report["all_matched"])
        self.assertEqual(report["case_count"], 6)
        decisions = {row["actual_decision"] for row in report["results"]}
        self.assertEqual(decisions, {"represented_model_clause", "reject", "exact_gate"})
        self.assertIn("Māori authority", report["maori_authority_boundary"])

    def test_security_is_a_bounded_synthetic_rehearsal(self) -> None:
        red_team = load("security/red-team.json")
        recovery = load("security/recovery-drill.json")
        self.assertTrue(red_team["all_matched"])
        self.assertEqual(red_team["fixture_count"], 7)
        self.assertIn("not an exhaustive security scan", red_team["boundary"])
        self.assertTrue(recovery["all_simulated_steps_passed"])
        self.assertEqual(red_team["disposition"], "represented")


class Stage20AndBoundaryTests(unittest.TestCase):
    def test_accessible_report_is_static_and_structured(self) -> None:
        report = (PHASE / "deliverables" / "v641-v2-evidence-report.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('<html lang="en-NZ">', report)
        self.assertIn('class="skip"', report)
        self.assertGreaterEqual(report.count("<caption>"), 5)
        self.assertIn("Claim boundary.", report)
        self.assertNotIn("<script", report.lower())

    def test_stage20_retains_dissent_and_has_no_forbidden_e4(self) -> None:
        board = load("stage20/evidence-board.json")
        rehearsal = load("stage20/decision-rehearsal.json")
        self.assertGreaterEqual(len(board["claims"]), 12)
        self.assertTrue(rehearsal["no_gmut_e4"])
        self.assertTrue(rehearsal["all_dissent_retained"])
        self.assertTrue(rehearsal["all_scenarios_non_predictive"])
        self.assertFalse(
            any(
                row["grade"] == "E4"
                and any(term in row["claim"] for term in ("GMUT", "THOS", "Freed ID", "CBR"))
                for row in board["claims"]
            )
        )

    def test_x2_outcomes_cover_all_truth_classes(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(
            set(ledger["summary"]), {"completed", "represented", "open_gap", "exact_gate"}
        )
        self.assertTrue(all(row["x2_execution_receipt"] for row in ledger["outcomes"]))

    def test_phase_validator_passes(self) -> None:
        report = validate_phase(PHASE)
        self.assertTrue(report["valid"], report["issues"])

    def test_phase_artifacts_contain_no_raw_task_ids_or_local_windows_paths(self) -> None:
        raw_id = re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.IGNORECASE,
        )
        local_path = re.compile(r"\b[A-Za-z]:\\")
        for path in PHASE.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".tex"}:
                text = path.read_text(encoding="utf-8", errors="replace")
                self.assertIsNone(raw_id.search(text), path)
                self.assertIsNone(local_path.search(text), path)


if __name__ == "__main__":
    unittest.main()

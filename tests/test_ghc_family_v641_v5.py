from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path

from scripts.ghc_family_evidence_assurance import (
    audit_accessibility,
    build_cross_solver,
    build_empirical_gate,
    build_freed_id_gate,
    build_minimal_support,
    build_negative_replay,
    build_packaging,
    build_participation_gate,
    build_thos_sentinels,
    build_typed_counterexamples,
)
from scripts.ghc_family_evidence_assurance_validator import validate_assurance_phase


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v641-v5"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class FrozenX1AndSourcesTests(unittest.TestCase):
    def test_x1_is_unique_ten_proposal_packet(self) -> None:
        x1 = load("x1-proposals.json")
        self.assertEqual(x1["source_revision"], "a845c30e9b2b32f4a923d2679b707c1fd6ff6a38")
        self.assertEqual(x1["verified_source_seal"], "594d8159c9fdf39e77ee218c58b4345a374662dd")
        self.assertEqual(len(x1["proposals"]), 10)
        self.assertEqual(len({row["proposal_id"] for row in x1["proposals"]}), 10)
        self.assertEqual(
            set(x1["allowed_truth_labels"]),
            {"completed", "represented", "open_gap", "exact_gate"},
        )
        self.assertEqual(x1["active_and_standby"]["active_owner"], "Tamar Vey")
        self.assertEqual(len(x1["active_and_standby"]["standby"]), 8)
        self.assertEqual(
            x1["active_and_standby"]["collaboration_subagents"],
            "not_authorized_and_not_spawned",
        )

    def test_titles_are_distinct_from_v2_v4(self) -> None:
        current = {row["title"] for row in load("x1-proposals.json")["proposals"]}
        prior = set()
        for relative in (
            "docs/sable-rook/v641-v2/x1-proposals.json",
            "docs/elian-voss/v641-v3/x1-proposals.json",
            "docs/nima-calder/v641-v4/x1-proposals.json",
        ):
            prior.update(
                row["title"]
                for row in json.loads((ROOT / relative).read_text(encoding="utf-8"))["proposals"]
            )
        self.assertEqual(len(prior), 30)
        self.assertFalse(current & prior)

    def test_source_classes_and_references_are_closed(self) -> None:
        x1 = load("x1-proposals.json")
        sources = load("sources/source-ledger.json")
        ids = {row["source_id"] for row in sources["sources"]}
        self.assertEqual(len(ids), 31)
        self.assertEqual(
            Counter(row["status_class"] for row in sources["sources"]),
            Counter({"current": 14, "stable": 14, "draft": 2, "watch": 1}),
        )
        self.assertTrue(
            all(source_id in ids for proposal in x1["proposals"] for source_id in proposal["authoritative_source_ids"])
        )


class EvidenceAssuranceBuilderTests(unittest.TestCase):
    def test_support_minimization_rebuilds(self) -> None:
        expected = build_minimal_support(load("x1-proposals.json"), load("sources/source-ledger.json"))
        actual = (
            load("provenance/minimal-support-sets.json"),
            load("provenance/source-change-impact.json"),
            load("provenance/status-delta-audit.json"),
        )
        self.assertEqual(expected, actual)
        self.assertTrue(actual[0]["passed"])
        self.assertEqual(actual[1]["fixture_count"], 13)

    def test_typed_and_counterexample_artifacts_rebuild(self) -> None:
        expected = build_typed_counterexamples()
        actual = (
            load("physics/typed-expression-contract.json"),
            load("physics/assumption-counterexample-sweep.json"),
            load("physics/observable-identifiability-audit.json"),
        )
        self.assertEqual(expected, actual)
        self.assertGreaterEqual(actual[2]["non_identifiable_mapping_count"], 1)
        self.assertFalse(actual[2]["unique_empirical_prediction_established"])

    def test_cross_solver_artifacts_rebuild(self) -> None:
        expected = build_cross_solver()
        actual = (
            load("physics/cross-solver-envelope.json"),
            load("physics/interval-containment-audit.json"),
            load("physics/tolerance-budget.json"),
        )
        self.assertEqual(expected, actual)
        self.assertTrue(actual[0]["all_healthy_within_tolerance"])
        self.assertTrue(actual[1]["reference_contained"])
        self.assertFalse(actual[2]["post_hoc_widening_permitted"])

    def test_empirical_gate_rebuilds_and_stays_open(self) -> None:
        expected = build_empirical_gate()
        actual = (
            load("empirical/real-data-receipt-contract.json"),
            load("empirical/baseline-to-claim-gate.json"),
            load("empirical/likelihood-negative-vectors.json"),
            load("empirical/adapter-readiness.json"),
        )
        self.assertEqual(expected, actual)
        self.assertFalse(actual[0]["real_data_received"])
        self.assertFalse(actual[1]["claim_allowed"])
        self.assertEqual(actual[1]["disposition"], "open_gap")

    def test_thos_rebuilds_without_real_arms(self) -> None:
        expected = build_thos_sentinels()
        actual = (
            load("thos/matched-budget-protocol.json"),
            load("thos/blindness-sentinel-audit.json"),
            load("thos/rubric-invariance-audit.json"),
            load("thos/analysis-lock.json"),
            load("thos/synthetic-scorer-proxy.json"),
        )
        self.assertEqual(expected, actual)
        self.assertEqual(actual[1]["real_arm_output_count"], 0)
        self.assertFalse(actual[2]["winner_declared"])
        self.assertIn("not_agent_or_model_performance", actual[4]["interpretation_boundary"])

    def test_freed_id_rebuilds_without_real_assurance(self) -> None:
        expected = build_freed_id_gate()
        actual = (
            load("freed-id/cryptographic-evidence-bundle-schema.json"),
            load("freed-id/trust-resolution-gate.json"),
            load("freed-id/absence-and-negative-vectors.json"),
            load("freed-id/minimum-profile.json"),
            load("freed-id/conformance-report.json"),
        )
        self.assertEqual(expected, actual)
        self.assertFalse(actual[1]["cryptographic_completion"])
        self.assertEqual(actual[1]["disposition"], "open_gap")
        self.assertFalse(actual[2]["real_keys_or_proofs_used"])

    def test_participation_gate_rebuilds_and_stays_exact(self) -> None:
        expected = build_participation_gate()
        actual = (
            load("cbr/participation-evidence-contract.json"),
            load("cbr/empty-chair-refusal-audit.json"),
            load("cbr/dissent-remedy-ledger.json"),
            load("cbr/legitimacy-crosswalk.json"),
            load("cbr/conflict-report.json"),
        )
        self.assertEqual(expected, actual)
        self.assertFalse(actual[0]["authorized_affected_party_participation_present"])
        self.assertEqual(actual[0]["disposition"], "exact_gate")
        self.assertFalse(actual[1]["project_filled_empty_authority_roles"])

    def test_packaging_and_retained_negatives_rebuild(self) -> None:
        expected = build_packaging(ROOT)
        actual = (
            load("security/canonical-package-manifest.json"),
            load("security/path-collision-audit.json"),
            load("security/archive-boundary-vectors.json"),
            load("security/red-team.json"),
            load("security/recovery-drill.json"),
        )
        self.assertEqual(expected, actual)
        self.assertTrue(actual[0]["canonical_paths_unique"])
        negative = load("reproduction/negative-replay.json")
        self.assertEqual(build_negative_replay(), negative)
        self.assertEqual([row["negative_id"] for row in negative["negatives"]], ["REPRO-V4-N01", "REPRO-V4-N02"])


class TruthReportAndPrivacyTests(unittest.TestCase):
    def test_final_truth_uses_all_four_labels(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(set(ledger["summary"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual(set(row["disposition"] for row in ledger["outcomes"]), set(ledger["summary"]))
        if load("reproduction/reproduction-report.json")["status"] == "verified_local_repeatability":
            self.assertEqual(
                ledger["summary"],
                {"completed": 6, "exact_gate": 1, "open_gap": 2, "represented": 1},
            )

    def test_report_overview_and_accessibility(self) -> None:
        report_path = PHASE / "deliverables" / "v641-v5-evidence-report.html"
        report = report_path.read_text(encoding="utf-8")
        self.assertIn('<html lang="en-NZ">', report)
        self.assertIn("V5 evidence-assurance extensions", report)
        self.assertNotIn("<script", report.lower())
        self.assertEqual(audit_accessibility(report_path), load("validation/accessibility-audit.json"))
        overview = (PHASE / "v641-v5-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b\w+\b", overview)), 1500)

    def test_phase_validator_passes(self) -> None:
        receipt = validate_assurance_phase(PHASE)
        self.assertTrue(receipt["valid"], receipt["issues"])

    def test_public_phase_has_no_private_shapes(self) -> None:
        patterns = [
            re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
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

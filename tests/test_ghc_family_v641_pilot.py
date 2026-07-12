from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.ghc_family_empirical_adapters import validate_adapter_manifest
from scripts.ghc_family_freed_id_conformance import run_vectors
from scripts.ghc_family_thos_benchmark import score_results


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v641-v1"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class IntegratedLedgerTests(unittest.TestCase):
    def test_eighty_unique_work_units_cover_ten_by_eight(self) -> None:
        ledger = load("80-work-unit-ledger.json")
        units = ledger["work_units"]
        self.assertEqual(len(units), 80)
        self.assertEqual(len({row["work_unit_id"] for row in units}), 80)
        self.assertEqual(len({row["origin_plan_slot"] for row in units}), 80)
        self.assertEqual({row["x1"]["status"] for row in units}, {"completed"})
        self.assertEqual(
            {row["x2"]["execution_receipt"] for row in units},
            {"assessed_and_outcome_recorded"},
        )

    def test_every_unit_preserves_failure_condition_and_artifact(self) -> None:
        for row in load("80-work-unit-ledger.json")["work_units"]:
            self.assertTrue(row["x1"]["null"])
            self.assertTrue(row["x1"]["falsifier"])
            self.assertTrue((ROOT / row["x2"]["artifact"]).is_file())


class AdapterAndProtocolTests(unittest.TestCase):
    def test_empirical_adapters_are_manifest_only_and_valid(self) -> None:
        payload = load("empirical/adapter-manifest.json")
        self.assertEqual(
            payload["fit_status"], "NO_LIKELIHOOD_RUN_NO_EMPIRICAL_GMUT_CONFIRMATION"
        )
        self.assertFalse(validate_adapter_manifest(payload["adapters"]))
        self.assertNotIn("fit_complete", {row["status"] for row in payload["adapters"]})

    def test_thos_synthetic_calibration_cannot_masquerade_as_agent_score(self) -> None:
        fixture = load("thos/synthetic-scorer-calibration-input.json")
        score = score_results(fixture["results"], fixture_kind=fixture["fixture_kind"])
        self.assertIn("not_agent_or_model_performance", score["interpretation_boundary"])
        self.assertEqual(score["task_count"], 5)

    def test_freed_id_vectors_match_and_reject_personhood_overclaim(self) -> None:
        profile = load("freed-id/minimum-profile.json")
        vectors = load("freed-id/conformance-vectors.json")["vectors"]
        report = run_vectors(profile, vectors)
        self.assertTrue(report["all_matched"])
        rejected = {row["vector_id"] for row in report["results"] if not row["actual_accept"]}
        self.assertIn("consciousness-overclaim", rejected)
        self.assertIn("personhood-overclaim", rejected)


class EvidenceBoardTests(unittest.TestCase):
    def test_stage20_claims_have_full_accountability_fields(self) -> None:
        board = load("stage20/evidence-board.json")
        required = {
            "claim_id",
            "claim",
            "grade",
            "state",
            "evidence",
            "owner",
            "review_date",
            "rejection_or_promotion_condition",
        }
        self.assertGreaterEqual(len(board["claims"]), 10)
        self.assertTrue(all(required <= row.keys() for row in board["claims"]))
        self.assertFalse(any(row["grade"] == "E4" and "GMUT" in row["claim"] for row in board["claims"]))

    def test_source_ledger_is_portable_and_independence_is_explicit(self) -> None:
        ledger = load("sources/source-ledger.json")
        self.assertGreaterEqual(ledger["source_count"], 15)
        for source in ledger["sources"]:
            self.assertTrue(source["url"].startswith("https://"))
            self.assertTrue(source["independence_group"])
            self.assertFalse(source["snapshot_embedded"])

    def test_next_proposal_count(self) -> None:
        self.assertEqual(len(load("next-ten-proposals.json")["proposals"]), 10)


if __name__ == "__main__":
    unittest.main()

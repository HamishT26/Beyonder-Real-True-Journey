from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v655-v5"
X1 = "a92d0a6c8a5d2620074c1bc505fa8345c8f90373"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v655_v5_core as core


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class SableV655V5EvidenceTests(unittest.TestCase):
    def test_outcomes_and_mutations(self) -> None:
        ledger = load("x2/proposal-ledger.json")
        self.assertEqual(
            ledger["outcome_counts"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(
            sum(row["rejected_mutation_count"] for row in ledger["proposals"]),
            150,
        )
        self.assertEqual(
            sum(row["accepted_mutation_count"] for row in ledger["proposals"]),
            0,
        )

    def test_all_surface_receipts_exist(self) -> None:
        proposals = load("preregistration/proposals.json")["proposals"]
        for proposal in proposals:
            with self.subTest(proposal=proposal["proposal_id"]):
                base = PHASE / "surfaces" / proposal["slug"]
                self.assertTrue((base / "contract.json").is_file())
                mutation = json.loads(
                    (base / "mutation-results.json").read_text(encoding="utf-8")
                )
                receipt = json.loads(
                    (base / "bounded-receipt.json").read_text(encoding="utf-8")
                )
                self.assertEqual(mutation["rejected_count"], 5)
                self.assertEqual(mutation["accepted_count"], 0)
                self.assertTrue(receipt["valid_fixture_passed"])
                self.assertFalse(receipt["independent_reproduction"])

    def test_ten_skills_and_runners_are_valid_and_used(self) -> None:
        index = load("tooling/ghc-family-index-x2-addendum.json")
        self.assertEqual(len(index["skills"]), 10)
        self.assertEqual(len(index["runners"]), 10)
        self.assertTrue(all(row["valid"] for row in index["runner_rows"]))
        self.assertEqual(index["global_installation_count"], 0)
        for skill in index["skills"]:
            self.assertTrue((PHASE / "skills" / skill / "SKILL.md").is_file())
            self.assertTrue(
                load(f"skills/{skill}/smoke-receipt.json")["valid"]
            )

    def test_all_portfolios_resolved(self) -> None:
        results = load("portfolios/execution-results.json")
        self.assertEqual(results["safe_now"]["pending"], 0)
        self.assertEqual(results["candidate"]["pending"], 0)
        self.assertEqual(results["clean_fix_refine"]["pending"], 0)
        self.assertEqual(results["skills"]["used"], 10)
        self.assertEqual(results["runners"]["used"], 10)
        self.assertTrue(results["no_external_or_sibling_tasks"])

    def test_retained_negatives_and_method_flow(self) -> None:
        negatives = load("truth/retained-negative-register-x2.json")
        methods = load("method-flow/method-flow-ledger-x2.json")
        x2_count = negatives["x2_operational_count"]
        self.assertEqual(x2_count, len(negatives["x2_operational"]))
        self.assertGreaterEqual(x2_count, 0)
        self.assertEqual(
            negatives["effective_at_evidence"],
            negatives["x1_effective"]
            + negatives["synthetic_mutation_negative_count"]
            + x2_count,
        )
        self.assertEqual(negatives["synthetic_mutation_negative_count"], 150)
        self.assertTrue(negatives["no_failure_erased"])
        expected_methods = 267 + negatives["x1_operational_count"] + x2_count
        self.assertEqual(methods["counts"]["methods"], expected_methods)
        self.assertEqual(
            methods["counts"]["witness_results"],
            {"fail": expected_methods, "pass": expected_methods},
        )

    def test_gaps_and_gates_remain_open(self) -> None:
        gaps = load("truth/open-gap-register-x2.json")
        gates = load("truth/exact-gate-register-x2.json")
        self.assertEqual(gaps["effective_count"], 93)
        self.assertEqual(gates["effective_count"], 92)
        self.assertEqual(gaps["closed_count"], 0)
        self.assertEqual(gates["closed_count"], 0)

    def test_external_action_and_promotion_counts(self) -> None:
        truth = load("truth/phase-truth-evidence.json")
        zero_fields = [
            "real_keys_or_proofs",
            "real_identity_resolutions",
            "real_status_or_revocation_events",
        ] + list(core.ZERO_EXTERNAL_COUNTS)
        false_fields = [
            "independent_reproduction_claimed",
            "privacy_complete_claimed",
            "accessibility_complete_claimed",
            "exhaustive_security_claimed",
            "professional_validation_claimed",
            "theory_of_everything_claimed",
            "agi_or_asi_claimed",
            "consciousness_or_personhood_claimed",
        ]
        self.assertTrue(all(truth[field] == 0 for field in zero_fields))
        self.assertTrue(all(truth[field] is False for field in false_fields))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_overview_and_static_report(self) -> None:
        overview = (
            PHASE / "deliverables/v655-v5-integrated-overview.md"
        ).read_text(encoding="utf-8")
        report = (
            PHASE / "deliverables/v655-v5-boundary-evidence-report.html"
        ).read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1800)
        self.assertLessEqual(len(overview.split()), 6000)
        self.assertIn('href="#main"', report)
        self.assertIn("<caption>", report)
        self.assertIn('scope="col"', report)
        self.assertNotIn("<script", report.casefold())

    def test_detailed_and_minimal_validations(self) -> None:
        detailed = load("validation/evidence-validation.json")
        minimal = load("validation/evidence-minimal-validation.json")
        self.assertTrue(detailed["valid"])
        self.assertTrue(minimal["valid"])
        self.assertEqual(detailed["failed_count"], 0)
        self.assertEqual(minimal["failed_count"], 0)
        self.assertEqual(detailed["privacy_confirmed_hits"], [])
        self.assertEqual(detailed["manifest_mismatches"], [])

    def test_x1_packet_is_unchanged(self) -> None:
        result = subprocess.run(
            [
                "git",
                "diff",
                "--quiet",
                X1,
                "--",
                "docs/sable-rook/v655-v5/environment",
                "docs/sable-rook/v655-v5/identity",
                "docs/sable-rook/v655-v5/preregistration",
                "docs/sable-rook/v655-v5/provenance",
                "docs/sable-rook/v655-v5/route",
                "docs/sable-rook/v655-v5/sources",
                "scripts/build_ghc_family_v655_v5_x1.py",
                "scripts/ghc_family_v655_v5_phase_catalogue.py",
                "scripts/ghc_family_v655_v5_phase_data.py",
                "scripts/ghc_family_v655_v5_x1_staged_review.py",
                "tests/test_ghc_family_v655_v5_x1.py",
            ],
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()

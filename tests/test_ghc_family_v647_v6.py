from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path

from scripts.ghc_family_v647_v6_runtime import SURFACES, accepts, baseline, surface_evidence


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v647-v6"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V647V6EvidenceTests(unittest.TestCase):
    def test_all_ten_runtime_surfaces(self) -> None:
        self.assertEqual(len(SURFACES), 10)
        self.assertEqual({spec["proposal_id"] for spec in SURFACES.values()}, {f"V6476-P{i:02d}" for i in range(1, 11)})

    def test_every_baseline_accepts(self) -> None:
        for surface in SURFACES:
            self.assertTrue(accepts(surface, baseline(surface)), surface)

    def test_every_surface_rejects_seven_mutations(self) -> None:
        for surface in SURFACES:
            evidence = surface_evidence(surface)
            self.assertEqual(evidence["mutation_count"], 7, surface)
            self.assertEqual(evidence["rejected_mutation_count"], 7, surface)
            self.assertTrue(all(row["retained"] for row in evidence["mutations"]), surface)

    def test_exact_seventy_synthetic_negatives(self) -> None:
        ledger = load("validation/preregistered-synthetic-negatives.json")
        self.assertEqual((ledger["count"], ledger["rejected_count"], ledger["retained_count"]), (70, 70, 70))
        self.assertEqual(len({row["negative_id"] for row in ledger["negatives"]}), 70)

    def test_core_outcome_distribution(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(Counter(row["outcome"] for row in ledger["proposals"]), Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))
        self.assertEqual(set(row["outcome"] for row in ledger["proposals"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_sdss_remains_zero_row(self) -> None:
        evidence = load("empirical/sdss-dr19-zero-row-receipt.json")
        for field in SURFACES["sdss_dr19"]["required_zero"]:
            self.assertEqual(evidence["baseline"][field], 0)
        self.assertEqual(evidence["outcome"], "open_gap")

    def test_weather_handover_is_proxy(self) -> None:
        evidence = load("thos/weather-warning-handover-vectors.json")
        self.assertEqual(evidence["outcome"], "represented")
        self.assertTrue(evidence["baseline"]["synthetic_only"])
        self.assertFalse(evidence["independent_reproduction"])

    def test_freed_id_is_synthetic(self) -> None:
        evidence = load("freed-id/oauth-token-exchange-mutations.json")
        self.assertEqual(evidence["outcome"], "represented")
        self.assertTrue(evidence["baseline"]["synthetic_only"])

    def test_cbr_authority_is_exact_gate(self) -> None:
        evidence = load("cbr/weather-remedy-matrix.json")
        self.assertEqual(evidence["outcome"], "exact_gate")
        for field in SURFACES["weather_authority"]["required_zero"]:
            self.assertEqual(evidence["baseline"][field], 0)

    def test_symbolic_gmut_has_no_empirical_credit(self) -> None:
        proposal = next(row for row in load("x2-proposal-ledger.json")["proposals"] if row["proposal_id"] == "V6476-P02")
        self.assertEqual(proposal["outcome"], "completed")
        self.assertEqual(proposal["real_rows"], 0)

    def test_safe_and_candidate_portfolios(self) -> None:
        execution = load("approval-packets/x2-portfolio-execution.json")
        self.assertEqual((execution["safe_now_count"], execution["safe_now_completed"]), (30, 30))
        self.assertEqual((execution["candidate_count"], execution["candidates_completed"]), (20, 20))

    def test_exact_and_blocked_packets_unexecuted(self) -> None:
        execution = load("approval-packets/x2-portfolio-execution.json")
        self.assertEqual((execution["exact_approval_count"], execution["exact_executed"]), (10, 0))
        self.assertEqual((execution["blocked_count"], execution["blocked_executed"]), (5, 0))
        self.assertTrue(all(not row["x2_completion_credit"] for row in execution["exact_approval"] + execution["blocked"]))

    def test_candidate_prototypes_built_tested_invoked(self) -> None:
        payload = load("prototypes/x2-candidate-execution.json")
        self.assertEqual((payload["candidate_count"], payload["built_count"], payload["tested_count"], payload["invoked_count"]), (20, 20, 20, 20))
        self.assertTrue(all(row["built"] and row["bounded_tested"] and row["invoked"] for row in payload["candidates"]))

    def test_skills_validated_and_smoke_used(self) -> None:
        payload = load("prototypes/skill-build-use-receipt.json")
        self.assertEqual((payload["skill_count"], payload["validated_count"], payload["smoke_used_count"]), (20, 20, 20))
        self.assertTrue(all(not row["installed_globally"] for row in payload["skills"]))

    def test_runner_inventory(self) -> None:
        payload = load("prototypes/runner-build-use-receipt.json")
        self.assertEqual(payload["runner_count"], 10)
        self.assertGreaterEqual(payload["invoked_count"], 9)

    def test_cleanup_is_additive(self) -> None:
        payload = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((payload["task_count"], payload["completed_count"], payload["destructive_count"]), (30, 30, 0))

    def test_x1_content_seal(self) -> None:
        payload = load("reproduction/x1-content-seal.json")
        self.assertEqual((payload["entry_count"], payload["mismatch_count"]), (8, 0))
        self.assertTrue(all(row["equal_in_git_blob_domain"] for row in payload["entries"]))

    def test_effective_negative_count(self) -> None:
        payload = load("retained-negative-register-x2.json")
        self.assertEqual(payload["effective_total"], 3669)
        self.assertEqual(payload["erased_negative_count"], 0)

    def test_gate_counts(self) -> None:
        payload = load("exact-open-gate-register-x2.json")
        self.assertEqual((payload["effective_open_gaps"], payload["effective_exact_gates"], payload["closed_by_software"]), (23, 24, 0))

    def test_method_flow_preserves_fail_pass_parity(self) -> None:
        payload = load("method-flow/method-flow-state.json")
        self.assertEqual(payload["counts"]["witness_results"], {"fail": 18, "pass": 18})

    def test_static_report_has_structural_accessibility(self) -> None:
        text = (PHASE / "deliverables/v647-v6-static-report.html").read_text(encoding="utf-8")
        for token in ('href="#main"', '<main id="main">', '<caption>', 'scope="col"', '@media print', 'manual keyboard'):
            self.assertIn(token.casefold(), text.casefold())

    def test_overview_is_three_page_equivalent_and_under_cap(self) -> None:
        text = (PHASE / "deliverables/v647-v6-final-integrated-overview.md").read_text(encoding="utf-8")
        words = re.findall(r"\b\w+\b", text)
        self.assertGreaterEqual(len(words), 1200)
        self.assertLessEqual(len(words), 6000)

    def test_phase_truth_remains_not_ready(self) -> None:
        truth = load("phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["route_state"], "PREPARED_NOT_SENT")
        self.assertEqual((truth["real_rows"], truth["real_people_or_operations"], truth["real_keys_or_tokens"], truth["authority_decisions"]), (0, 0, 0, 0))

    def test_no_private_paths_or_raw_identifiers(self) -> None:
        patterns = [
            re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
            re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
            re.compile(r"\b(?:app|plugin)://", re.I),
            re.compile(r"<codex_delegation|source_thread_id", re.I),
        ]
        for path in PHASE.rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                for pattern in patterns:
                    self.assertIsNone(pattern.search(text), path.as_posix())


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts import ghc_family_v650_v4_phase_data as d
from scripts import ghc_family_v650_v4_runtime as runtime

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v650-v4"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V650V4X2Tests(unittest.TestCase):
    def test_twenty_receipts_use_only_allowed_outcomes(self):
        ledger = load("x2-evidence-ledger.json")
        self.assertEqual(ledger["proposal_count"], 20)
        self.assertEqual(
            ledger["outcome_counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(
            set(ledger["allowed_outcomes"]),
            {"completed", "represented", "open_gap", "exact_gate"},
        )
        for proposal in d.PROPOSALS:
            receipt = load(f"surfaces/{proposal['slug']}/bounded-receipt.json")
            self.assertTrue(receipt["passed"])
            self.assertFalse(receipt["independent_reproduction"])

    def test_all_one_hundred_mutations_executed_and_rejected(self):
        results = []
        for proposal in d.PROPOSALS:
            mutation = load(f"surfaces/{proposal['slug']}/mutation-results.json")
            self.assertEqual(mutation["planned"], 5)
            self.assertEqual(mutation["executed"], 5)
            self.assertEqual(mutation["rejected_or_quarantined"], 5)
            self.assertEqual(mutation["accepted"], 0)
            results.extend(mutation["results"])
        self.assertEqual(len(results), 100)
        self.assertEqual(len({row["mutation_id"] for row in results}), 100)
        self.assertTrue(all(row["passed"] for row in results))
        aggregate = load("validation/x2-synthetic-mutation-results.json")
        self.assertEqual(aggregate["executed"], 100)

    def test_open_gap_is_zero_row_and_zero_likelihood(self):
        witness = load("surfaces/twomass-zero-row/bounded-receipt.json")["domain_witness"]
        self.assertFalse(witness["download_attempted"])
        self.assertEqual(witness["real_rows"], 0)
        self.assertEqual(witness["likelihood_evaluations"], 0)
        self.assertEqual(witness["posterior_samples"], 0)
        self.assertFalse(witness["empirical_claim"])

    def test_represented_profiles_have_no_real_operations(self):
        for slug in [
            "jwt-assertion",
            "token-revocation",
            "dynamic-client-registration",
            "ebike-repair-proxy",
        ]:
            receipt = load(f"surfaces/{slug}/bounded-receipt.json")
            self.assertEqual(receipt["outcome"], "represented")
            text = json.dumps(receipt["domain_witness"], sort_keys=True)
            self.assertNotIn('"network_exchange": true', text)
            self.assertNotIn('"live_registration": true', text)
            self.assertNotIn('"live_revocation": true', text)

    def test_exact_gate_makes_zero_authority_decisions(self):
        witness = load("surfaces/ebike-authority-matrix/bounded-receipt.json")["domain_witness"]
        self.assertEqual(witness["authority_decisions"], 0)
        self.assertEqual(witness["real_affected_parties"], 0)
        self.assertTrue(witness["all_reserved"])
        self.assertEqual(set(witness["reservations"].values()), {"reserved"})

    def test_bounded_format_and_protocol_algorithms(self):
        self.assertEqual(runtime.parse_bson_int32_document(b"\x0c\x00\x00\x00\x10a\x00\x01\x00\x00\x00\x00"), {"a": 1})
        with self.assertRaises(ValueError):
            runtime.parse_bson_int32_document(b"\x0c\x00\x00\x00\x10a\x00\x01\x00")
        cues = runtime.parse_webvtt("WEBVTT\n\n00:00.000 --> 00:01.000\nText\n")
        self.assertEqual(len(cues), 1)
        self.assertEqual(cues[0]["end"], 1.0)
        qpack = load("surfaces/qpack/bounded-receipt.json")["domain_witness"]
        self.assertTrue(qpack["passed"])
        self.assertFalse(qpack["network_exchange"])

    def test_count_min_and_clenshaw_numeric_witnesses(self):
        sketch = runtime.CountMinSketch(16, 3)
        sketch.update("item", 4)
        self.assertGreaterEqual(sketch.estimate("item"), 4)
        with self.assertRaises(ValueError):
            sketch.update("item", -1)
        coefficients = [1.0, 0.5, -0.25]
        x = 0.3
        direct = coefficients[0] + coefficients[1] * x + coefficients[2] * (2 * x * x - 1)
        self.assertAlmostEqual(runtime.clenshaw(coefficients, x), direct, places=12)

    def test_formal_and_nonconversion_witnesses_refuse_promotion(self):
        for slug in ["wigner-representation", "coleman-mandula", "stueckelberg"]:
            witness = load(f"surfaces/{slug}/bounded-receipt.json")["domain_witness"]
            self.assertTrue(witness["passed"])
        virial = load("surfaces/virial-nonconversion/bounded-receipt.json")["domain_witness"]
        self.assertFalse(virial["psyche_conversion"])
        self.assertFalse(virial["agency_conversion"])
        self.assertFalse(virial["fundamental_mind_law_claim"])
        stage = load("surfaces/g-formula-nonpromotion/bounded-receipt.json")["domain_witness"]
        self.assertEqual(stage["real_participants"], 0)
        self.assertEqual(stage["empirical_rows"], 0)
        self.assertFalse(stage["stage20_promoted"])

    def test_all_expanded_portfolios_have_bounded_witnesses(self):
        expected = {
            "safe-now-execution.json": 40,
            "candidate-execution.json": 30,
            "skill-execution.json": 20,
            "runner-execution.json": 10,
            "clean-fix-refine-execution.json": 40,
        }
        for name, count in expected.items():
            payload = load(f"portfolios/{name}")
            self.assertEqual(payload["count"], count)
            self.assertEqual(payload["completed"], count)
        self.assertEqual(
            load("portfolios/clean-fix-refine-execution.json")["destructive_actions"], 0
        )

    def test_twenty_phase_local_skills_validate_and_smoke_use(self):
        execution = load("portfolios/skill-execution.json")
        self.assertFalse(execution["global_install"])
        for row in execution["skills"]:
            skill_dir = PHASE / row["package"]
            self.assertTrue((skill_dir / "SKILL.md").is_file())
            self.assertTrue((skill_dir / "agents/openai.yaml").is_file())
            self.assertTrue((skill_dir / "references/contract.md").is_file())
            witness = load(row["witness"])
            self.assertTrue(witness["metadata_generated_with_official_workflow"])
            self.assertTrue(witness["smoke_used"])
            self.assertTrue(witness["smoke_passed"])
            self.assertFalse(witness["global_install"])
            yaml_text = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"${row['name']}", yaml_text)

    def test_ten_family_runners_cover_all_proposals(self):
        execution = load("portfolios/runner-execution.json")
        covered = []
        mutations = 0
        for row in execution["runners"]:
            self.assertTrue(row["invoked"])
            witness = load(row["witness"])
            self.assertTrue(witness["passed"])
            covered.extend(witness["proposal_ids"])
            mutations += witness["rejected_mutation_count"]
        self.assertEqual(Counter(covered), Counter(row["proposal_id"] for row in d.PROPOSALS))
        self.assertEqual(mutations, 100)

    def test_method_flow_retains_failure_and_passing_recovery(self):
        state = load("method-flow/method-flow-state.json")
        method_ids = {row["method_id"] for row in state["methods"]}
        self.assertTrue({f"V6504-M{index:02d}" for index in range(1, 9)} <= method_ids)
        self.assertEqual(len(state["methods"]), len(method_ids))
        failed = state["counts"]["witness_results"]["fail"]
        passed = state["counts"]["witness_results"]["pass"]
        self.assertEqual(failed, passed)
        self.assertEqual(len(state["witnesses"]), failed + passed)
        self.assertEqual(
            {row["recommendation_state"] for row in state["methods"]}, {"preferred"}
        )
        self.assertTrue(load("method-flow/method-flow-validation.json")["valid"])

    def test_negatives_gates_and_terminal_truth_remain_visible(self):
        negatives = load("retained-negative-register.json")
        self.assertEqual(negatives["effective_total"], 5922)
        self.assertEqual(negatives["synthetic_mutations"], 100)
        self.assertEqual(negatives["x2_operational"], 6)
        self.assertEqual(negatives["erased"], 0)
        gates = load("exact-open-gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 46)
        self.assertEqual(gates["effective_exact_gates"], 47)
        truth = load("phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["real_empirical_rows"], 0)
        self.assertEqual(truth["real_participants_or_operators"], 0)
        self.assertEqual(truth["real_keys_or_proofs"], 0)
        self.assertEqual(truth["authority_decisions"], 0)

    def test_static_report_has_structural_accessibility_and_reservations(self):
        text = (PHASE / "report.html").read_text(encoding="utf-8")
        for fragment in [
            'href="#main"',
            '<main id="main">',
            '<caption>',
            'scope="col"',
            'scope="row"',
            "NOT_READY_FOR_STAGE_20",
            "assistive-technology",
            "affected-user evaluation",
        ]:
            self.assertIn(fragment, text)
        self.assertNotIn("complete accessibility conformance", text.casefold())


if __name__ == "__main__":
    unittest.main()

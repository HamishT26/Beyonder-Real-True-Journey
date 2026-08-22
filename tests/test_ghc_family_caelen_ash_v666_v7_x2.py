from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v666-v7"
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_caelen_ash_v666_v7_runtime import validate_contract  # noqa: E402


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class CaelenAshV666V7X2Tests(unittest.TestCase):
    def test_proposal_ledger_exact_truth(self):
        value = load("x2/proposal-ledger.json")
        self.assertEqual(len(value["proposals"]), 20)
        self.assertEqual(value["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(value["unknown_labels"], [])
        self.assertEqual(value["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_phase_truth_counts(self):
        value = load("x2/phase-truth.json")
        self.assertEqual(value["proposal_chain"], 4310)
        self.assertEqual(value["positive_structural_fixtures"], 20)
        self.assertEqual(value["preregistered_mutations"], 100)
        self.assertEqual(value["rejected_mutations"], 100)
        self.assertEqual(value["phase_local_skills"], 10)
        self.assertEqual(value["family_current_runners"], 10)
        self.assertEqual(value["effective_negatives"], 26872)
        self.assertEqual(value["effective_methods"], 11874)
        self.assertEqual(value["open_gaps"], 189)
        self.assertEqual(value["exact_gates"], 187)

    def test_zero_real_world_counts(self):
        value = load("x2/phase-truth.json")
        for key in ("real_rows", "participants", "network_calls_by_generated_phase_software", "external_actions", "exact_or_blocked_execution_count"):
            self.assertEqual(value[key], 0)

    def test_method_flow_exact_and_retained(self):
        value = load("method-flow/x2-method-flow.json")
        self.assertEqual(value["new_negative_count"], 100)
        self.assertEqual(value["new_method_count"], 215)
        self.assertEqual(len(value["rows"]), 215)
        self.assertEqual(value["failed_witness_count"], 100)
        self.assertTrue(value["all_failures_retained"])
        self.assertFalse(value["failed_witness_converted_to_pass"])

    def test_x2_operational_failure_is_retained(self):
        value = load("method-flow/x2-operational-overlay.json")
        self.assertEqual(value["new_negative_count"], 5)
        self.assertEqual(value["new_method_count"], 5)
        self.assertEqual(value["effective_negatives"], 26872)
        self.assertEqual(value["effective_methods"], 11874)
        self.assertTrue(value["all_failures_retained"])
        self.assertFalse(value["failed_witness_converted_to_pass"])
        self.assertEqual(len(value["rows"]), 5)
        self.assertTrue(all(row["failed_witness"]["credit"] == 0 for row in value["rows"]))

    def test_portfolio_execution_is_owner_only(self):
        value = load("x2/portfolio-execution.json")
        self.assertEqual(value["executed_owner_method_count"], 95)
        self.assertEqual(value["successor_recommendation_execution_count"], 0)
        self.assertEqual(value["exact_approval_execution_count"], 0)
        self.assertEqual(value["blocked_packet_execution_count"], 0)

    def test_exact_and_blocked_register(self):
        value = load("x2/exact-and-blocked-register.json")
        self.assertEqual(value["exact_count"], 10)
        self.assertEqual(value["blocked_count"], 5)
        self.assertEqual(value["executed_count"], 0)
        self.assertTrue(value["authority_preserved"])

    def test_open_gap_remains_open(self):
        value = load("x2/open-gate-register.json")
        self.assertEqual(value["phase_open_gap"], "CA6667-N019")
        self.assertEqual(value["cumulative_open_gaps"], 189)
        self.assertEqual(value["status"], "open_gap")

    def test_inherited_revalidation_has_zero_credit(self):
        value = load("x2/revalidation/inherited-contract-integrity.json")
        self.assertEqual(value["row_count"], 20)
        self.assertTrue(value["all_json_valid"])
        self.assertEqual(value["completion_credit"], 0)
        self.assertEqual(value["novelty_credit"], 0)

    def test_skill_catalog(self):
        value = load("x2/skill-catalog.json")
        self.assertEqual(value["skill_count"], 10)
        self.assertTrue(value["all_quick_validated"])
        self.assertTrue(value["all_smoke_used"])
        self.assertEqual(value["global_install_count"], 0)

    def test_runner_catalog_and_smoke(self):
        catalog = load("x2/runner-catalog.json")
        smoke = load("x2/tooling-smoke-receipt.json")
        self.assertEqual(catalog["runner_count"], 10)
        self.assertEqual(catalog["shared_caller_changes"], 0)
        self.assertEqual(smoke["runner_count"], 10)
        self.assertTrue(smoke["all_runners_invoked"])
        self.assertTrue(smoke["all_runners_smoke_used"])
        self.assertTrue(smoke["all_runners_valid"])

    def test_x1_immutability(self):
        value = load("x2/x1-immutability-receipt.json")
        self.assertEqual(value["x1_sha"], "c992b1cea0f702a3e27f8a217d3413438acf9a6b")
        self.assertEqual(value["changed_x1_paths"], [])
        self.assertTrue(value["manifest_replay"]["valid"])
        self.assertTrue(value["immutable"])

    def test_zero_call_adapter(self):
        value = load("x2/source-adapter-zero-call.json")
        self.assertFalse(value["network_enabled"])
        self.assertEqual(value["transport_calls"], 0)
        self.assertEqual(value["real_rows"], 0)
        self.assertEqual(value["outcome"], "open_gap")

    def test_environment_has_no_changes(self):
        value = load("x2/environment-receipt.json")
        self.assertEqual(value["network_changes"], 0)
        self.assertEqual(value["package_installs"], 0)
        self.assertEqual(value["host_security_changes"], 0)
        self.assertEqual(value["reboots"], 0)

    def test_successor_recommendations_are_unsent_zero_credit(self):
        value = load("x2/successor-recommendations.json")
        self.assertEqual(value["recommendation_count"], 20)
        self.assertFalse(value["route_inferred"])
        self.assertFalse(value["successor_contacted"])
        self.assertEqual(value["completion_credit"], 0)
        self.assertEqual(value["novelty_credit"], 0)

    def test_accessible_fixture_reserves_manual_review(self):
        text = (PHASE / "x2" / "accessible-structure-fixture.html").read_text(encoding="utf-8")
        for token in ('lang="en-NZ"', "<main>", "<h1>", "<caption>", 'scope="col"', 'scope="row"'):
            self.assertIn(token, text)
        self.assertIn("reserves manual and affected-user evaluation", text)

    def test_every_phase_json_parses(self):
        paths = sorted(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 100)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))


def make_contract_test(proposal_number: int):
    def test(self):
        proposal_id = f"CA6667-N{proposal_number:03d}"
        value = load(f"x2/proposals/{proposal_id.casefold()}/contract.json")
        self.assertEqual(value["proposal_id"], proposal_id)
        self.assertEqual(validate_contract(value), [])
        self.assertTrue(value["synthetic_only"])
        self.assertFalse(value["positive_fixture"]["real_object"])
    return test


def make_mutation_test(proposal_number: int):
    def test(self):
        proposal_id = f"CA6667-N{proposal_number:03d}"
        value = load(f"x2/proposals/{proposal_id.casefold()}/mutation-results.json")
        self.assertEqual(value["proposal_id"], proposal_id)
        self.assertEqual(value["executed_count"], 5)
        self.assertEqual(value["rejected_count"], 5)
        self.assertEqual(value["accepted_count"], 0)
        self.assertTrue(value["all_rejected_and_retained"])
        self.assertTrue(all(not row["accepted"] and row["credit"] == 0 and row["validator_errors"] for row in value["mutations"]))
    return test


SKILL_NAMES = [
    "horological-component-topology-vacancy",
    "stored-energy-isolation-abstention",
    "timebase-zero-sample-refusal",
    "gear-ratio-synthetic-closure",
    "movement-association-revision-boundary",
    "condition-vocabulary-zero-image",
    "horological-accessibility-structure",
    "clock-rate-gmut-domain-gate",
    "horological-method-flow",
    "horological-closeout-gate",
]


def make_skill_test(name: str):
    def test(self):
        text = (PHASE / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        receipt = load(f"skills/{name}/smoke-receipt.json")
        self.assertTrue(text.startswith("---\nname:"))
        self.assertIn("## Purpose", text)
        self.assertIn("## Use", text)
        self.assertIn("## Boundary", text)
        self.assertTrue(receipt["smoke_used"])
        self.assertTrue(receipt["valid"])
        self.assertFalse(receipt["globally_installed"])
    return test


for number in range(1, 21):
    setattr(CaelenAshV666V7X2Tests, f"test_contract_{number:03d}", make_contract_test(number))
    setattr(CaelenAshV666V7X2Tests, f"test_mutations_{number:03d}", make_mutation_test(number))

for index, skill_name in enumerate(SKILL_NAMES, 1):
    setattr(CaelenAshV666V7X2Tests, f"test_skill_{index:02d}", make_skill_test(skill_name))


if __name__ == "__main__":
    unittest.main()

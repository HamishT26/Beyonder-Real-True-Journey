"""Owner-scoped tests for Ilyra Fen v686-v7 only."""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
import os
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/ilyra-fen/v686-v7"
TOOLCHAIN = Path(os.environ["GHC_ILYRA_V686_V7_TOOLCHAIN"])
sys.path.insert(0, str(TOOLCHAIN))
sys.path.insert(0, str(REPO / "scripts"))

MODULE_NAMES = {
    "ghc_family_policy_resolution.py": "ghc_family_policy_resolution",
    "ghc_family_provenance_chronology.py": "ghc_family_provenance_chronology",
    "ghc_family_accessible_policy_review.py": "ghc_family_accessible_policy_review",
    "ghc_family_correction_custody.py": "ghc_family_correction_custody",
    "ghc_family_claim_reservations.py": "ghc_family_claim_reservations",
}
MODULES = {name: importlib.import_module(module) for name, module in MODULE_NAMES.items()}
COMMON = MODULES["ghc_family_policy_resolution.py"]


def load(relative):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


class IlyraV686V7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposals = load("x1/new-proposals.json")["proposals"]
        cls.reports = load("x2/contract-results.json")["reports"]
        cls.by_id = {row["proposal_id"]: row for row in cls.reports}
        cls.context = {
            "owner": "Ilyra Fen",
            "phase": "v686-v7",
            "source": "33801b707269956af7d267e8fd4ed350a4f9c937",
            "x1": "e5669d7693263f2a90f5e2988f62b1c335c9a4b0",
        }

    def test_exact_proposal_count_and_ids(self):
        self.assertEqual(len(self.proposals), 200)
        self.assertEqual(len({p["proposal_id"] for p in self.proposals}), 200)

    def test_exact_core_outcome_distribution(self):
        self.assertEqual(Counter(p["expected_execution_disposition"] for p in self.proposals), Counter(completed=170, represented=10, open_gap=10, exact_gate=10))

    def test_all_frozen_contracts_and_input_preservation(self):
        for proposal in self.proposals:
            payload = copy.deepcopy(proposal["input"])
            before = COMMON.canonical(payload)
            observed = MODULES[proposal["runner"]].evaluate(proposal["operation"], payload)
            self.assertEqual(observed, proposal["expected_result"], proposal["proposal_id"])
            self.assertEqual(before, COMMON.canonical(payload), proposal["proposal_id"])

    def test_all_definition_hashes(self):
        for proposal in self.proposals:
            definition = dict(proposal)
            digest = definition.pop("definition_sha256")
            self.assertEqual(COMMON.digest(definition), digest)

    def test_all_reports_exactly_bound(self):
        self.assertEqual(len(self.reports), 200)
        for proposal in self.proposals:
            self.assertTrue(COMMON.verify_report(proposal, self.by_id[proposal["proposal_id"]], self.context), proposal["proposal_id"])

    def test_reports_remain_synthetic_and_non_authority(self):
        for report in self.reports:
            self.assertTrue(report["synthetic"])
            self.assertFalse(report["empirical"])
            self.assertFalse(report["authority"])
            self.assertFalse(report["independent_reproduction"])

    def test_safe_task_results(self):
        result = load("x2/safe-task-results.json")
        self.assertEqual(result["count"], 300)
        self.assertEqual(result["passed"], 300)
        self.assertTrue(all(row["passed"] for row in result["results"]))

    def test_candidate_results_are_rejected(self):
        result = load("x2/candidate-results.json")
        self.assertEqual(result["count"], 250)
        self.assertEqual(result["accepted_count"], 0)
        self.assertTrue(all(not row["accepted"] for row in result["results"]))

    def test_clean_fix_refine_pairs(self):
        result = load("x2/clean-fix-refine-results.json")
        self.assertEqual(result["pair_count"], 300)
        self.assertEqual(result["class_counts"], {"CLEAN": 100, "FIX": 100, "REFINE": 100})
        self.assertFalse(result["failed_records_erased"])
        self.assertTrue(all(not row["mutated_report_accepted"] and row["corrected_report_accepted"] for row in result["pairs"]))

    def test_registered_mutations_retained(self):
        result = load("x2/registered-mutations.json")
        self.assertEqual(result["count"], 1000)
        self.assertEqual(result["accepted_count"], 0)
        self.assertTrue(all(not row["accepted"] and row["success_credit"] == 0 for row in result["mutations"]))

    def test_gate_packets_unexecuted(self):
        result = load("x2/gate-packets.json")
        self.assertEqual(len(result["exact_packets"]), 50)
        self.assertEqual(len(result["blocked_packets"]), 30)
        self.assertTrue(all(not row["executed"] for key in ("exact_packets", "blocked_packets") for row in result[key]))

    def test_package_smokes_and_adverse_claims(self):
        result = load("x2/package-smokes.json")
        self.assertEqual(result["direct_packages"], 3)
        self.assertTrue(all(row["positive_passed"] and row["adverse_rejected"] for row in result["results"]))

    def test_method_flow_retains_every_failure(self):
        result = load("x2/method-flow.json")
        self.assertEqual(result["counts"]["methods"], 1579)
        self.assertEqual(result["counts"]["failed_witnesses"], 1579)
        self.assertEqual(result["counts"]["passing_witnesses"], 1579)
        self.assertEqual(result["counts"]["erased_failed_witnesses"], 0)

    def test_deck_manifest_and_graph(self):
        deck = PHASE / "x2/deck"
        manifest = json.loads((deck / "card-manifest.json").read_text(encoding="utf-8"))
        for row in manifest["files"]:
            data = (REPO / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(sha(data), row["sha256"])
        graph = json.loads((deck / "graph-validation.json").read_text(encoding="utf-8"))
        self.assertTrue(graph["valid"])
        self.assertEqual(graph["cycles"], [])

    def test_content_seal_targets(self):
        seal = load("x2/content-seal.json")
        for row in seal["targets"]:
            data = (REPO / row["path"]).read_bytes()
            self.assertEqual(sha(data), row["sha256"])

    def test_phase_truth_boundaries(self):
        truth = load("x2/phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])
        self.assertFalse(truth["complete_repository_suite"])

    def test_frozen_bare_list_window_compatibility_refusal(self):
        proposal = next(p for p in self.proposals if p["operation"] == "validity_window_intersection")
        self.assertEqual(MODULES[proposal["runner"]].evaluate(proposal["operation"], proposal["input"]), proposal["expected_result"])

    def test_well_shaped_portion_interval_regression(self):
        module = MODULES["ghc_family_provenance_chronology.py"]
        payload = {"windows": [{"start": "2026-01-01", "end": "2026-01-10"}, {"start": "2026-01-05", "end": "2026-01-12"}]}
        self.assertEqual(module.evaluate("validity_window_intersection", payload), {"ok": True, "value": {"empty": False, "interval": {"start": "2026-01-05", "end": "2026-01-10", "closed": True}}})

    def test_strict_json_duplicate_key_refusal(self):
        with self.assertRaises(COMMON.ContractError):
            COMMON.strict_loads(b'{"a":1,"a":2}')

    def test_strict_json_nonfinite_refusal(self):
        with self.assertRaises(COMMON.ContractError):
            COMMON.strict_loads(b'{"a":NaN}')

    def test_unknown_operation_refusal(self):
        self.assertEqual(COMMON.evaluate("unknown", {}), {"ok": False, "reason": "UNKNOWN_OPERATION"})

    def test_cli_batches_for_each_runner(self):
        env = dict(os.environ)
        env["PYTHONPATH"] = str(TOOLCHAIN)
        grouped = {}
        for proposal in self.proposals:
            grouped.setdefault(proposal["runner"], []).append({"operation": proposal["operation"], "input": proposal["input"]})
        for runner, requests in grouped.items():
            completed = subprocess.run([sys.executable, str(REPO / "scripts" / runner)], input=COMMON.canonical({"requests": requests}), capture_output=True, env=env, check=True)
            output = json.loads(completed.stdout)
            self.assertEqual(len(output["results"]), len(requests))
            self.assertTrue(all(row["input_unchanged"] for row in output["results"]))


def add_operation_test(operation):
    def test(self):
        rows = [proposal for proposal in self.proposals if proposal["operation"] == operation]
        self.assertEqual(len(rows), 10)
        for proposal in rows:
            self.assertEqual(MODULES[proposal["runner"]].evaluate(operation, copy.deepcopy(proposal["input"])), proposal["expected_result"])
    test.__name__ = "test_operation_" + operation
    setattr(IlyraV686V7Tests, test.__name__, test)


for _operation in (
    "policy_decision_intersection", "scope_conjunction", "revocation_precedence", "authority_abstention",
    "iso_chronology", "validity_window_intersection", "record_expiry", "correction_lineage",
    "provenance_branch_conflict", "coverage_abstention", "negative_evidence_index", "missingness_class",
    "accessible_diff", "canonical_number_policy", "revocation_projection", "custody_chain", "recovery_obligation",
    "cbr_authority_gate", "gmut_evidence_gap", "thos_operational_readback",
):
    add_operation_test(_operation)


if __name__ == "__main__":
    unittest.main()

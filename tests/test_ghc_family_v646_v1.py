from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
PHASE=ROOT/"docs/eiren-kestrel/v646-v1"
sys.path.insert(0,str(ROOT/"scripts"))

from ghc_family_v646_v1_runtime import RUNNERS, run
from ghc_family_v646_v1_minimal_validator import validate as validate_minimal
from ghc_family_v646_v1_validator import validate


def load(name: str): return json.loads((PHASE/name).read_text(encoding="utf-8"))


class V646V1EvidenceTests(unittest.TestCase):
    def test_outcome_distribution_and_stage20(self) -> None:
        ledger=load("x2-proposal-ledger.json"); truth=load("phase-truth.json")
        self.assertEqual(ledger["outcome_distribution"],{"completed":6,"represented":2,"open_gap":1,"exact_gate":1})
        self.assertEqual(truth["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])

    def test_zero_real_evidence_boundaries(self) -> None:
        truth=load("phase-truth.json")
        for field in ("real_data_rows_ingested","likelihood_evaluations","real_participants","real_keys_or_proofs","real_operational_actions"):
            self.assertEqual(truth[field],0)

    def test_runtime_smoke_results(self) -> None:
        results=load("validation/runtime-smoke-results.json")
        self.assertEqual(set(results),set(RUNNERS))
        self.assertTrue(all(x["passed"] for x in results.values()))
        self.assertEqual(results["zero-row-cosmology"]["rows_ingested"],0)
        self.assertFalse(results["accessible-table"]["complete_conformance_claim"])
        self.assertEqual(results["optional-stopping"]["stage20_verdict"],"NOT_READY_FOR_STAGE_20")

    def test_approval_portfolio_execution(self) -> None:
        receipt=load("approval-packets/x2-execution-ledger.json")
        self.assertEqual(receipt["safe_now_executed"],30)
        self.assertEqual(receipt["candidates_executed"],20)
        self.assertEqual(receipt["exact_or_external_packets_executed"],0)
        self.assertEqual(receipt["blocked_packets_executed"],0)
        self.assertTrue(receipt["all_acceptance_passed"])

    def test_skill_runner_and_cleanup_receipts(self) -> None:
        skills=load("prototypes/skill-build-receipt.json"); runners=load("prototypes/runner-build-receipt.json"); clean=load("maintenance/x2-clean-refine-receipt.json")
        self.assertEqual((skills["skill_count"],skills["validated_count"],skills["smoke_use_pass_count"]),(20,20,20))
        self.assertTrue(skills["valid"])
        self.assertEqual((runners["runner_count"],runners["used_count"]),(10,10))
        self.assertTrue(runners["valid"])
        self.assertEqual(clean["completed_count"],30)
        self.assertEqual(clean["destructive_action_count"],0)

    def test_method_flow_preserves_failures(self) -> None:
        summary=load("method-flow/method-flow-summary.json"); negatives=load("retained-negative-register.json")
        self.assertEqual(summary["counts"]["methods"],5)
        self.assertEqual(summary["counts"]["witness_results"],{"fail":5,"pass":5})
        self.assertEqual(len(summary["retained_failed_witnesses"]),5)
        self.assertEqual(negatives["effective_total"],2507)
        self.assertEqual(negatives["erased_count"],0)

    def test_open_and_exact_gates_preserved(self) -> None:
        gates=load("open-exact-gate-register.json")
        self.assertEqual(gates["inherited_open_gap_count"],10)
        self.assertEqual(gates["inherited_exact_gate_count"],11)
        self.assertEqual(gates["silently_closed_count"],0)

    def test_overview_and_accessible_report(self) -> None:
        overview=(PHASE/"v646-v1-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()),1500)
        self.assertLessEqual(len(overview.split()),6000)
        report=(PHASE/"deliverables/v646-v1-evidence-report.html").read_text(encoding="utf-8").casefold()
        for token in ("<main","<table","<caption","scope=","not_ready_for_stage_20","manual"):
            self.assertIn(token,report)

    def test_evidence_manifest(self) -> None:
        manifest=load("validation/evidence-manifest.json")
        self.assertEqual(manifest["entry_count"],len(manifest["entries"]))
        self.assertGreaterEqual(manifest["entry_count"],120)

    def test_detailed_validator_precommit(self) -> None:
        result=validate("evidence",None,False)
        self.assertTrue(result["valid"],result["issues"])
        self.assertEqual(result["privacy"]["confirmed_hit_count"],0)

    def test_minimal_validator_precommit(self) -> None:
        result=validate_minimal(None,False)
        self.assertTrue(result["valid"],result["issues"])
        self.assertEqual(result["check_count"],20)

    def test_lifecycle_receipts_are_bounded_and_prepared(self) -> None:
        suite=load("validation/canonical-evidence-full-suite.json")
        closeout=load("closeout-receipt.json"); seal=load("seal-receipt.json"); final_record=load("final-validation-record.json")
        self.assertEqual((suite["passed"],suite["failed"]),(1011,0))
        self.assertEqual(closeout["route_state"],"PREPARED_NOT_SENT")
        self.assertEqual(seal["named_lane_replay_required_after_push"],1)
        self.assertEqual(final_record["terminal_verdict"],"NOT_READY_FOR_STAGE_20")

    def test_runtime_functions_are_deterministic_except_disposable_git(self) -> None:
        for name in ("cache-provenance","dhost-obligations","zero-row-cosmology","switching-handover","sd-jwt-vc","electricity-care","accessible-table","onsager-domain","optional-stopping"):
            self.assertEqual(run(name),run(name),name)


if __name__=="__main__": unittest.main()

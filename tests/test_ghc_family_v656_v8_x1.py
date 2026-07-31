from __future__ import annotations

import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v656-v8"
SOURCE = "c885a4533b2a73343990039e21d74979acb79c00"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class V656V8X1Tests(unittest.TestCase):
    def test_source_head_and_ancestry(self) -> None:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", SOURCE, "HEAD"],
            cwd=ROOT,
            check=True,
        )
        self.assertLessEqual(int(git("rev-list", "--count", f"{SOURCE}..HEAD")), 8)
        verification = load("startup/source-verification.json")
        self.assertEqual(verification["source_final"], SOURCE)
        self.assertTrue(verification["verified_read_only"])
        self.assertFalse(verification["source_successful_aggregate_replayed"])

    def test_thirty_complete_proposal_contracts(self) -> None:
        ledger = load("preregistration/proposal-ledger.json")
        self.assertEqual(ledger["proposal_count"], 30)
        required = {
            "proposal_id", "title", "slug", "pillar_relation", "mechanism",
            "hypothesis", "null_or_failure_condition", "approval_class",
            "execution_lane", "official_or_primary_source_needs",
            "concrete_artifacts", "falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        for proposal in ledger["proposals"]:
            self.assertTrue(required <= set(proposal))
            self.assertTrue(proposal["official_or_primary_source_needs"])
            self.assertTrue(proposal["concrete_artifacts"])
            self.assertTrue(proposal["protected_gates"])

    def test_expected_dispositions_are_not_outcomes(self) -> None:
        ledger = load("preregistration/proposal-ledger.json")
        counts = Counter(row["expected_disposition"] for row in ledger["proposals"])
        self.assertEqual(
            counts,
            Counter({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}),
        )
        self.assertFalse(ledger["outcomes_observed"])
        truth = load("truth/x1-phase-truth.json")
        self.assertIsNone(truth["observed_outcome_counts"])
        self.assertFalse(truth["x2_implementation_present"])

    def test_novelty_audits_all_inherited_rows(self) -> None:
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertEqual(audit["inherited_count"], 2380)
        self.assertEqual(audit["new_count"], 30)
        self.assertEqual(audit["effective_count"], 2410)
        self.assertTrue(audit["all_pass"])
        self.assertLess(audit["maximum_similarity"], audit["threshold"])
        self.assertEqual(len(audit["rows"]), 30)

    def test_source_ledger_resolves_all_proposal_references(self) -> None:
        sources = load("sources/official-source-ledger.json")
        ledger = load("preregistration/proposal-ledger.json")
        source_ids = {row["source_id"] for row in sources["sources"]}
        requested = {
            source_id
            for proposal in ledger["proposals"]
            for source_id in proposal["official_or_primary_source_needs"]
        }
        self.assertTrue(requested <= source_ids)
        self.assertEqual(set(sources["status_vocabulary"]), {"current", "stable", "draft", "watch"})
        self.assertEqual(set(sources["status_counts"]), {"current", "stable"})

    def test_portfolios_and_tool_plans_are_frozen_only(self) -> None:
        portfolios = load("preregistration/task-portfolios.json")
        tools = load("preregistration/skill-and-runner-plan.json")
        self.assertEqual(portfolios["counts"], {"safe_now": 30, "candidate": 20, "clean": 30, "total": 80})
        self.assertEqual(portfolios["x1_executed_tasks"], 0)
        self.assertEqual(tools["skill_count"], 10)
        self.assertEqual(tools["runner_count"], 10)
        self.assertFalse(tools["implemented_in_x1"])

    def test_every_x1_failure_has_fail_and_pass_witnesses(self) -> None:
        negatives = load("truth/retained-negative-register-x1.json")
        flow = load("method-flow/method-flow-state-x1.json")
        self.assertEqual(negatives["current_x1_operational_count"], 13)
        self.assertEqual(negatives["inherited_sealed_register_count"], 14895)
        self.assertEqual(negatives["inherited_effective_count"], 14895)
        self.assertIsNone(negatives["inherited_postfinal_route_negative"])
        self.assertEqual(flow["counts"]["current_methods"], 13)
        self.assertEqual(flow["counts"]["current_witness_results"], {"fail": 13, "pass": 13})
        witness_counts = Counter(row["result"] for row in flow["witnesses"])
        self.assertEqual(witness_counts, Counter({"fail": 13, "pass": 13}))
        retained_ids = {
            negative_id
            for row in flow["witnesses"]
            for negative_id in row["retained_negative_ids"]
        }
        self.assertEqual(
            retained_ids,
            {row["negative_id"] for row in negatives["current_x1_operational_negatives"]},
        )

    def test_privacy_manifest_and_caps(self) -> None:
        scan = load("validation/x1-privacy-scan.json")
        manifest = load("validation/x1-content-manifest.json")
        documents = load("validation/document-cap-receipt-x1.json")
        files = load("validation/owner-file-threshold-x1.json")
        self.assertTrue(scan["valid"])
        self.assertEqual(scan["hit_count"], 0)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertTrue(documents["all_under_limit"])
        self.assertLessEqual(documents["maximum_words"], 100000)
        self.assertTrue(files["below_threshold"])

    def test_route_is_prepared_not_sent(self) -> None:
        route = load("orchestration/route-state-x1.json")
        self.assertEqual(route["next_exact_title"], "Lyren Moss")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])
        self.assertEqual(route["tavian_sol_state"], "ON_STANDBY")

    def test_no_x2_or_outcome_artifacts_exist(self) -> None:
        paths = [path.relative_to(PHASE).as_posix() for path in PHASE.rglob("*") if path.is_file()]
        forbidden = [
            path for path in paths
            if path.startswith("surfaces/")
            or path.startswith("runners/")
            or "/x2" in path.lower()
            or path.startswith("closeout")
            or path.startswith("seal")
            or path.startswith("final")
        ]
        self.assertEqual(forbidden, [])

    def test_all_phase_json_parses(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 20)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

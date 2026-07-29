from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/ilyra-fen/v655-v3"
SOURCE = "3047039da17578fb74ca4c32f9660eadd433a6b7"
X1_FREEZE = "e98b40654e48f5adb75f8d436256978e4eb51070"
X1_FINAL = X1_FREEZE
EVIDENCE = "009228e1a22ee840f2e13eda2718579136c02335"
CORRECTION = EVIDENCE


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class IlyraV655V3CloseoutTests(unittest.TestCase):
    def test_anchor_contract_and_cap(self) -> None:
        contract = load("lifecycle/phase-anchor-contract.json")
        self.assertEqual(
            (
                contract["source"],
                contract["x1_freeze"],
                contract["x1_final"],
                contract["evidence"],
                contract["evidence_correction"],
            ),
            (SOURCE, X1_FREEZE, X1_FINAL, EVIDENCE, None),
        )
        self.assertEqual(contract["expected_phase_commits_after_final"], 3)
        self.assertTrue(contract["x1_freeze_and_final_same_commit"])
        self.assertEqual(contract["maximum_phase_commits"], 8)
        self.assertTrue(contract["zero_merges_required"])
        for anchor in (SOURCE, X1_FREEZE, X1_FINAL, EVIDENCE):
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", anchor, "HEAD"],
                cwd=REPO,
                check=True,
            )

    def test_truth_and_method_flow(self) -> None:
        closeout = load("closeout/closeout-receipt.json")
        final_negatives = load("truth/retained-negative-register-final.json")
        final_count = final_negatives["final_operational_count"]
        self.assertEqual(
            closeout["outcomes"],
            {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            },
        )
        self.assertEqual(closeout["effective_negatives"], 12720 + final_count)
        self.assertEqual(
            (
                closeout["effective_open_gaps"],
                closeout["effective_exact_gates"],
            ),
            (91, 90),
        )
        self.assertEqual(
            (
                closeout["method_count"],
                closeout["failed_witnesses"],
                closeout["passing_witnesses"],
            ),
            (228 + final_count, 228 + final_count, 228 + final_count),
        )
        self.assertEqual(closeout["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_route_is_prepared_not_sent(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["successor_exact_title"], "Auren Lark")
        self.assertEqual(route["successor_phase"], "v655-v4")
        self.assertEqual(route["blocker"], "TERMINAL_GATE_PENDING")
        self.assertTrue(route["hamish_successor_authorization"])
        self.assertEqual(
            route["authorization_class"], "authorized_with_terminal_conditions"
        )
        self.assertFalse(route["task_lookup_performed"])
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])

    def test_final_record_does_not_preclaim_own_commit(self) -> None:
        final = load("lifecycle/final-record.json")
        protocol = load("validation/final-validation-protocol.json")
        seal = load("seal/seal-receipt.json")
        self.assertIsNone(final["final_commit"])
        self.assertEqual(final["route_state"], "PREPARED_NOT_SENT")
        self.assertEqual(protocol["state"], "POSTCOMMIT_REQUIRED")
        self.assertFalse(protocol["completed"])
        self.assertFalse(protocol["preclaims_exact_final_head"])
        self.assertFalse(protocol["preclaims_route_sent"])
        self.assertFalse(seal["exact_final_commit_known_inside_own_tree"])

    def test_baton_is_file_backed_sanitized_and_bounded(self) -> None:
        baton = (
            PHASE / "handoffs/auren-lark-v655-v4-activation.md"
        ).read_text(encoding="utf-8")
        words = len(baton.split())
        self.assertGreaterEqual(words, 10_000)
        self.assertLessEqual(words, 100_000)
        self.assertIn("PREPARED_NOT_SENT", baton)
        self.assertIn("Auren Lark", baton)
        self.assertIn("TERMINAL_GATE_PENDING", baton)
        self.assertNotIn("HAMISH_SUCCESSOR_AUTHORIZATION_ABSENT", baton)
        self.assertNotIn("source_thread_id", baton)
        self.assertNotIn("resume_token", baton)
        self.assertNotIn("D:\\", baton)
        self.assertNotIn("C:\\Users", baton)

    def test_owner_manifest_has_exact_prospective_coverage(self) -> None:
        manifest = load("validation/final-owner-manifest.json")
        exclusions = set(manifest["self_exclusions"])
        actual = {
            path.relative_to(REPO).as_posix()
            for path in PHASE.rglob("*")
            if path.is_file()
        }
        entries = {row["path"] for row in manifest["entries"]}
        self.assertEqual(entries, actual - exclusions)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            self.assertEqual(
                row["git_blob"],
                git("hash-object", f"--path={row['path']}", row["path"]),
            )

    def test_document_and_file_caps(self) -> None:
        documents = load("validation/document-word-cap.json")
        files = load("validation/owner-file-threshold.json")
        self.assertTrue(documents["baton_within_bounds"])
        self.assertTrue(files["below_threshold"])
        self.assertLess(
            files["owner_file_count_before_lifecycle_self_exclusions"],
            files["threshold"],
        )
        self.assertFalse(files["inherited_repository_baseline_counted"])

    def test_evidence_boundary_is_preserved(self) -> None:
        correction = load("validation/evidence-staged-review.json")
        negatives = load("truth/retained-negative-register-x2.json")
        final_negatives = load("truth/retained-negative-register-final.json")
        self.assertTrue(correction["valid"])
        self.assertEqual(negatives["effective_at_evidence"], 12720)
        self.assertEqual(negatives["x2_operational_count"], 4)
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual(
            final_negatives["effective_at_final_candidate"],
            12720 + final_negatives["final_operational_count"],
        )
        self.assertGreaterEqual(final_negatives["final_operational_count"], 0)
        self.assertTrue(final_negatives["no_failure_erased"])

    def test_proposal_chain_and_mutations_are_exact(self) -> None:
        chain = load("provenance/frozen-chain-proposal-index.json")
        novelty = load("provenance/semantic-novelty-audit.json")
        executed = load("x2/proposal-ledger.json")
        self.assertEqual(
            (chain["prior_count"], chain["new_count"], chain["count"]),
            (1990, 30, 2020),
        )
        self.assertTrue(novelty["valid"])
        self.assertEqual(novelty["manual_mechanism_review_count"], 30)
        self.assertEqual(executed["proposal_count"], 30)
        self.assertEqual(
            sum(row["rejected_mutation_count"] for row in executed["proposals"]),
            150,
        )
        self.assertEqual(
            sum(row["accepted_mutation_count"] for row in executed["proposals"]),
            0,
        )

    def test_external_action_and_promotion_claims_remain_zero(self) -> None:
        for contract_path in sorted((PHASE / "surfaces").glob("*/contract.json")):
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            self.assertTrue(
                all(value == 0 for value in contract["external_action_counts"].values())
            )
            self.assertTrue(
                all(value is False for value in contract["promotion_claims"].values())
            )

    def test_final_method_flow_conserves_witnesses(self) -> None:
        evidence = load("method-flow/method-flow-ledger-x2.json")
        final = load("method-flow/method-flow-ledger-final.json")
        negatives = load("truth/retained-negative-register-final.json")
        final_count = negatives["final_operational_count"]
        self.assertGreaterEqual(final_count, 0)
        self.assertEqual(
            final["counts"]["methods"],
            evidence["counts"]["methods"] + final_count,
        )
        self.assertEqual(
            final["counts"]["witness_results"],
            {
                "fail": evidence["counts"]["witness_results"]["fail"] + final_count,
                "pass": evidence["counts"]["witness_results"]["pass"] + final_count,
            },
        )
        self.assertEqual(
            final["counts"]["witness_results"],
            {"fail": 228 + final_count, "pass": 228 + final_count},
        )

    def test_open_gaps_and_exact_gates_remain_open(self) -> None:
        gaps = load("truth/open-gap-register-x2.json")
        gates = load("truth/exact-gate-register-x2.json")
        self.assertEqual((gaps["effective_count"], gaps["closed_count"]), (91, 0))
        self.assertEqual((gates["effective_count"], gates["closed_count"]), (90, 0))
        self.assertEqual(gaps["new_rows"][0]["state"], "open_gap")
        self.assertEqual(gates["new_rows"][0]["state"], "exact_gate")

    def test_accessibility_and_real_object_boundaries_remain_open(self) -> None:
        report = (
            PHASE / "deliverables/v655-v3-boundary-evidence-report.html"
        ).read_text(encoding="utf-8")
        checklist = load("truth/final-complete-incomplete-checklist.json")
        self.assertIn('lang="en"', report)
        self.assertIn('href="#main"', report)
        self.assertIn("<caption>", report)
        self.assertNotIn("<script", report.casefold())
        joined = " ".join(checklist["incomplete_external"])
        self.assertIn("accessibility", joined)
        self.assertIn("Stage 20", joined)

    def test_final_index_addendum_matches_phase(self) -> None:
        addendum = load("tooling/ghc-family-index-final-addendum.json")
        final_count = load("truth/retained-negative-register-final.json")[
            "final_operational_count"
        ]
        self.assertEqual(addendum["phase"], "v655-v3")
        self.assertEqual(addendum["owner"], "Ilyra Fen")
        self.assertEqual(addendum["primary_pillar"], "Freed ID and CBR Heart")
        self.assertEqual(addendum["method_flow_pairs"], 228 + final_count)
        self.assertTrue(addendum["workflow_continuation_validation_valid"])
        self.assertEqual(addendum["route_blocker"], "TERMINAL_GATE_PENDING")
        self.assertEqual(addendum["route_state"], "PREPARED_NOT_SENT")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v653-v7"
SOURCE_HEAD = "c044464ed940093d59a59686efd4faa61853f341"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V653V7X1Tests(unittest.TestCase):
    def test_identity_boundary(self) -> None:
        identity = load("identity/relational-identity.json")
        self.assertEqual(identity["owner"], "Orin Thale")
        self.assertEqual(identity["pronouns"], "they/them")
        self.assertIn("Relational working language only", identity["boundary"])
        self.assertIn("Māori authority", identity["boundary"])
        self.assertTrue(identity["hamish_may_rename_pause_redirect_or_stop"])

    def test_source_anchor(self) -> None:
        source = load("provenance/source-anchor-ledger.json")
        self.assertEqual(source["source_final"], SOURCE_HEAD)
        self.assertEqual(source["source_to_final_commits"], 3)
        self.assertEqual(source["source_to_final_merges"], 0)
        self.assertTrue(source["all_single_parent"])
        self.assertEqual(source["final_parent_count"], 1)
        self.assertEqual(source["verified_manifest_contracts"], 4)
        self.assertEqual(source["verified_manifest_entries"], 576)
        self.assertEqual(source["inherited_effective_negatives"], 10279)
        self.assertEqual(source["external_post_seal_negative_count"], 1)
        self.assertEqual(source["activation_negative_baseline"], 10280)

    def test_exactly_thirty_proposals(self) -> None:
        ledger = load("preregistration/proposals.json")
        self.assertEqual(ledger["proposal_count"], 30)
        self.assertEqual(len(ledger["proposals"]), 30)

    def test_proposal_identifiers_and_titles_unique(self) -> None:
        rows = load("preregistration/proposals.json")["proposals"]
        self.assertEqual(len({row["proposal_id"] for row in rows}), 30)
        self.assertEqual(len({row["title"] for row in rows}), 30)

    def test_required_proposal_fields(self) -> None:
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for row in load("preregistration/proposals.json")["proposals"]:
            self.assertTrue(required <= set(row), row["proposal_id"])

    def test_only_four_truth_labels_and_distribution(self) -> None:
        ledger = load("preregistration/proposals.json")
        rows = ledger["proposals"]
        self.assertEqual(
            set(ledger["allowed_outcomes"]),
            {"completed", "represented", "open_gap", "exact_gate"},
        )
        self.assertEqual(
            Counter(row["expected_disposition"] for row in rows),
            Counter(
                {
                    "completed": 23,
                    "represented": 5,
                    "open_gap": 1,
                    "exact_gate": 1,
                }
            ),
        )

    def test_frozen_chain_count(self) -> None:
        chain = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(
            (chain["prior_count"], chain["new_count"], chain["count"]),
            (1600, 30, 1630),
        )
        self.assertEqual(len(chain["prior_proposals"]), 1600)
        self.assertEqual(len(chain["new_proposals"]), 30)

    def test_novelty_audit(self) -> None:
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertTrue(audit["all_pass"])
        self.assertTrue(audit["all_manual_mechanism_distinct"])
        self.assertLess(audit["maximum_token_jaccard"], audit["threshold"])
        self.assertEqual(len(audit["rejected_collisions"]), 10)
        self.assertEqual(audit["inherited_unique_identifier_count"], 1580)
        self.assertEqual(audit["inherited_reused_identifier_count"], 20)
        self.assertEqual(audit["inherited_title_count"], 1600)
        self.assertFalse(audit["inherited_rows_rewritten"])

    def test_source_integrity_and_statuses(self) -> None:
        ledger = load("sources/source-ledger.json")
        source_ids = {row["source_id"] for row in ledger["sources"]}
        self.assertEqual(
            set(ledger["allowed_statuses"]),
            {"current", "stable", "draft", "watch"},
        )
        self.assertEqual(sum(ledger["counts"].values()), len(ledger["sources"]))
        for proposal in load("preregistration/proposals.json")["proposals"]:
            self.assertTrue(
                set(proposal["official_or_primary_source_needs"])
                <= source_ids
            )

    def test_exactly_150_unexecuted_mutations(self) -> None:
        plan = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(plan["mutation_count"], 150)
        self.assertEqual(plan["mutations_per_proposal"], 5)
        self.assertEqual(plan["executed_count"], 0)
        self.assertTrue(
            all(
                row["state"] == "preregistered_not_executed"
                for row in plan["mutations"]
            )
        )

    def test_skill_and_runner_plans(self) -> None:
        skills = load("portfolios/skill-plan.json")
        runners = load("portfolios/runner-plan.json")
        self.assertEqual((skills["count"], runners["count"]), (10, 10))
        self.assertEqual(
            (skills["state"], runners["state"]),
            ("frozen_not_built", "frozen_not_built"),
        )
        self.assertTrue(
            all(row["name"].startswith("ghc-family-") for row in skills["skills"])
        )
        self.assertTrue(
            all(
                row["name"].startswith("ghc_family_")
                for row in runners["runners"]
            )
        )

    def test_task_caps_are_not_quotas(self) -> None:
        safe = load("portfolios/safe-now-plan.json")
        candidate = load("portfolios/candidate-plan.json")
        self.assertLessEqual(safe["count"], safe["cap"])
        self.assertLessEqual(candidate["count"], candidate["cap"])
        self.assertEqual((safe["count"], candidate["count"]), (30, 30))
        self.assertEqual(
            load("portfolios/clean-fix-refine-plan.json")["count"], 30
        )

    def test_x1_truth_is_unexecuted(self) -> None:
        truth = load("x1-phase-truth.json")
        self.assertEqual(truth["state"], "FROZEN_X1_NOT_EXECUTED")
        self.assertEqual(truth["mutation_executed_count"], 0)
        self.assertEqual(truth["skill_built_count"], 0)
        self.assertEqual(truth["runner_built_count"], 0)
        self.assertFalse(truth["x2_outcomes_present"])
        self.assertEqual(truth["frozen_chain_count"], 1630)
        self.assertEqual(truth["inherited_negatives"], 10279)
        self.assertEqual(truth["external_post_seal_negatives"], 1)
        self.assertEqual(truth["activation_negative_baseline"], 10280)
        self.assertEqual(truth["x1_operational_negatives"], 7)
        self.assertEqual(truth["effective_negatives"], 10287)
        self.assertEqual(
            (truth["inherited_open_gaps"], truth["inherited_exact_gates"]),
            (75, 76),
        )

    def test_method_flow_pair_preserves_failure(self) -> None:
        ledger = load("method-flow/x1-method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 7)
        self.assertEqual(
            ledger["counts"]["witness_results"],
            {"fail": 7, "pass": 7},
        )
        self.assertEqual(ledger["counts"]["states"]["preferred"], 7)

    def test_route_stops_after_closeout(self) -> None:
        request = load("workflow/workflow-plan-request.json")
        self.assertIn(
            "Stop after Orin Thale",
            request["route"]["terminal_successor_resolution"],
        )
        overlay = load("workflow/current-live-route-overlay.json")
        self.assertEqual(overlay["route_state"], "STOP_AFTER_CLOSEOUT_X1_ONLY")
        self.assertIsNone(overlay["successor_title"])
        self.assertEqual(
            overlay["successor_task_state"],
            "NO_DOWNSTREAM_ROUTE_AUTHORIZED",
        )
        self.assertFalse(overlay["current_task_creation"]["created_by_orin"])
        self.assertFalse(overlay["current_task_creation"]["task_creation_authorized"])
        self.assertFalse(overlay["tool_result_promoted_to_activation_authority"])

    def test_accessible_report_reserves_manual_evaluation(self) -> None:
        report = (PHASE / "reports/x1-accessible-report.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("<main>", report)
        self.assertIn(
            "Manual and affected-user accessibility evaluation is reserved",
            report,
        )
        self.assertIn("prefers-reduced-motion", report)

    def test_overview_is_three_page_equivalent(self) -> None:
        words = len(
            (PHASE / "reports/x1-integrated-overview.md")
            .read_text(encoding="utf-8")
            .split()
        )
        self.assertGreaterEqual(words, 1500)
        self.assertLessEqual(words, 100000)

    def test_no_x2_output_files(self) -> None:
        forbidden = (
            "mutation-results",
            "evidence-receipt",
            "closeout-receipt",
            "seal-receipt",
            "final-validation-record",
        )
        paths = [
            path.relative_to(PHASE).as_posix()
            for path in PHASE.rglob("*")
            if path.is_file()
        ]
        self.assertFalse(
            [
                path
                for path in paths
                if any(token in path for token in forbidden)
            ]
        )

    def test_every_json_parses(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreater(len(paths), 10)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_x1_staged_receipts(self) -> None:
        manifest = load("validation/x1-staged-manifest.json")
        privacy = load("validation/x1-staged-privacy.json")
        review = load("validation/x1-staged-review.json")
        self.assertGreater(manifest["entry_count"], 0)
        self.assertEqual(privacy["pattern_class_count"], 5)
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(review["valid"])
        self.assertEqual(review["mutation_executed_count"], 0)
        self.assertFalse(review["x2_outcomes_present"])

    def test_documents_within_cap(self) -> None:
        for path in PHASE.rglob("*"):
            if path.suffix.lower() not in {".md", ".html", ".txt"}:
                continue
            self.assertLessEqual(
                len(path.read_text(encoding="utf-8").split()),
                100000,
                path.relative_to(ROOT).as_posix(),
            )

    def test_primary_focus_and_practice_are_bounded(self) -> None:
        identity = load("identity/relational-identity.json")
        self.assertEqual(identity["primary_focus"], "GMUT Mind")
        self.assertIn(
            "municipal traffic-signal timing",
            identity["bounded_practice"],
        )
        threat = load("threat-model.json")
        self.assertIn("authority boundaries", threat["assets"])


if __name__ == "__main__":
    unittest.main()

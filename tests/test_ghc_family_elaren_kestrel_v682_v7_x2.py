"""Owner-scoped tests for Elaren Kestrel v682-v7 bounded x2 evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts.ghc_family_elaren_kestrel_v682_v7_contracts import (
    execute_proposal,
    mutated_fixture,
    positive_fixture,
    validate_fixture,
)
from scripts.ghc_family_elaren_kestrel_v682_v7_runner_bank import run_contract
from scripts.ghc_family_elaren_kestrel_v682_v7_skill_bank import (
    SKILL_NAMES,
    smoke_skills,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elaren-kestrel" / "v682-v7"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_SHA = "475febc0140aff210515f1fdb0652f79abdeee1f"
SOURCE = "7442303ebfbea11e7d9e4a9f40a441d5805b3272"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ElarenKestrelV682V7X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.proposals = load(X1 / "new-proposal-freeze.json")["proposals"]
        cls.evidence = load(X2 / "proposal-evidence.json")
        cls.mutations = load(X2 / "rejecting-mutations.json")
        cls.portfolio = load(X2 / "portfolio-execution.json")
        cls.skills = load(X2 / "skill-execution.json")
        cls.runners = load(X2 / "runner-execution.json")
        cls.flow = load(X2 / "method-flow-ledger.json")
        cls.truth = load(X2 / "phase-truth.json")
        cls.flashcards = load(X2 / "flashcards" / "deck.json")
        cls.flashcard_manifest = load(X2 / "flashcards" / "manifest.json")
        cls.tools = load(X2 / "bounded-tools.json")
        cls.manifest = load(VALIDATION / "evidence-index-manifest.json")
        cls.review = load(VALIDATION / "evidence-staged-review.json")
        cls.privacy = load(VALIDATION / "evidence-privacy-scan.json")

    def test_01_x1_is_immutable_and_ancestral(self) -> None:
        self.assertEqual(
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", X1_SHA, "HEAD"],
                cwd=ROOT,
                check=False,
            ).returncode,
            0,
        )
        self.assertEqual(
            subprocess.run(
                ["git", "rev-parse", f"{X1_SHA}^"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip(),
            SOURCE,
        )
        x1_manifest = load(VALIDATION / "x1-index-manifest.json")
        for entry in x1_manifest["entries"]:
            blob = subprocess.run(
                ["git", "show", f"{X1_SHA}:{entry['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])

    def test_02_sixty_positive_contracts_pass(self) -> None:
        self.assertEqual(len(self.proposals), 60)
        for proposal in self.proposals:
            decision = validate_fixture(proposal, positive_fixture(proposal))
            self.assertTrue(decision["accepted"], proposal["proposal_id"])

    def test_03_all_five_mutation_classes_reject(self) -> None:
        expected_types = {
            "missing_required_field",
            "lifecycle_inversion",
            "stale_provenance_digest",
            "safety_status_promotion",
            "authority_promotion",
        }
        for proposal in self.proposals:
            types = {
                row["mutation_type"]
                for row in proposal["preregistered_rejecting_mutations"]
            }
            self.assertEqual(types, expected_types)
            outcome, rejected = execute_proposal(proposal)
            self.assertTrue(outcome["bounded_positive_accepted"])
            self.assertEqual(outcome["invalid_mutations_rejected"], 5)
            self.assertFalse(any(row["accepted"] for row in rejected))
            for row in proposal["preregistered_rejecting_mutations"]:
                self.assertFalse(
                    validate_fixture(
                        proposal, mutated_fixture(proposal, row["mutation_type"])
                    )["accepted"]
                )

    def test_04_outcomes_use_only_four_labels(self) -> None:
        counts = Counter(row["disposition"] for row in self.evidence["evidence"])
        self.assertEqual(
            counts,
            Counter(
                {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
            ),
        )
        self.assertEqual(
            set(counts), {"completed", "represented", "open_gap", "exact_gate"}
        )

    def test_05_three_hundred_mutations_are_retained_zero_credit(self) -> None:
        self.assertEqual(self.mutations["executed_count"], 300)
        self.assertEqual(self.mutations["rejected_count"], 300)
        self.assertEqual(self.mutations["accepted_count"], 0)
        self.assertTrue(self.mutations["zero_credit"])
        self.assertTrue(
            all(row["retained_zero_credit"] for row in self.mutations["mutations"])
        )

    def test_06_zero_real_rows_or_authority_acts(self) -> None:
        zero = load(X2 / "zero-row-evidence.json")
        for key, value in zero.items():
            if key != "schema":
                self.assertEqual(value, 0, key)
        self.assertTrue(
            all(row["real_row_count"] == 0 for row in self.evidence["evidence"])
        )
        self.assertTrue(
            all(
                not row["empirical_or_authority_credit"]
                for row in self.evidence["evidence"]
            )
        )

    def test_07_portfolio_floors_executed_without_core_promotion(self) -> None:
        self.assertEqual(len(self.portfolio["safe_now"]), 120)
        self.assertEqual(len(self.portfolio["owner_candidates"]), 80)
        self.assertEqual(len(self.portfolio["owner_clean_fix_refine"]), 100)
        self.assertTrue(
            all(
                row["state"] == "completed_bounded"
                for row in self.portfolio["safe_now"]
            )
        )
        self.assertTrue(
            all(
                row["state"] == "bounded_executed_no_core_promotion"
                for row in self.portfolio["owner_candidates"]
            )
        )
        self.assertTrue(
            all(
                row["state"] == "completed_bounded"
                for row in self.portfolio["owner_clean_fix_refine"]
            )
        )

    def test_08_exact_and_blocked_holds_remain_unexecuted(self) -> None:
        self.assertEqual(len(self.portfolio["exact_approval"]), 20)
        self.assertEqual(len(self.portfolio["blocked"]), 10)
        self.assertTrue(
            all(
                row["approval_required"]
                and row["state"] == "preregistered_not_executed"
                for row in self.portfolio["exact_approval"] + self.portfolio["blocked"]
            )
        )

    def test_09_twenty_skills_are_initialized_customized_read_and_smoked(self) -> None:
        self.assertEqual(self.skills["skill_count"], 20)
        self.assertFalse(self.skills["global_installation"])
        self.assertTrue(
            all(
                row["official_quick_validate"]
                for row in self.skills["official_quick_validation"]
            )
        )
        self.assertEqual([row["skill"] for row in self.skills["results"]], SKILL_NAMES)
        for row in self.skills["results"]:
            self.assertTrue(row["fully_read_through_eof"])
            self.assertTrue(row["customized"])
            self.assertTrue(row["agent_metadata_present"])
            self.assertTrue(row["accepting_fixture_accepted"])
            self.assertTrue(row["rejecting_fixture_rejected"])
        replay = smoke_skills(X2 / "skills")
        self.assertEqual(len(replay), 20)
        self.assertTrue(
            all(
                row["accepting_fixture_accepted"] and row["rejecting_fixture_rejected"]
                for row in replay
            )
        )

    def test_10_ten_family_current_runners_accept_and_reject(self) -> None:
        self.assertEqual(self.runners["runner_count"], 10)
        self.assertTrue(
            all(
                row["family_current_name"].startswith("ghc_family_")
                for row in self.runners["results"]
            )
        )
        self.assertTrue(
            all(row["accepting_fixture_accepted"] for row in self.runners["results"])
        )
        self.assertTrue(
            all(row["rejecting_fixture_rejected"] for row in self.runners["results"])
        )
        for index in range(1, 11):
            self.assertTrue(run_contract(index, "positive")["accepted"])
            self.assertFalse(run_contract(index, "invalid")["accepted"])

    def test_11_method_flow_retains_failures_and_recoveries(self) -> None:
        self.assertEqual(self.flow["method_count"], 772)
        self.assertEqual(self.flow["failed_witness_count"], 318)
        self.assertEqual(self.flow["passing_witness_count"], 712)
        self.assertFalse(self.flow["recovery_erases_failure"])
        failure_ids = {row["witness_id"] for row in self.flow["failed_witnesses"]}
        self.assertIn("EL6827-ST-N001", failure_ids)
        self.assertIn("EL6827-ST-N007", failure_ids)
        self.assertIn("EL6827-ST-N012", failure_ids)
        self.assertIn("EL6827-X1-N015", failure_ids)
        self.assertIn("EL6827-X1-N016", failure_ids)
        self.assertIn("EL6827-X2-N017", failure_ids)
        self.assertIn("EL6827-X2-N018", failure_ids)
        self.assertEqual(len(failure_ids), 318)

    def test_12_effective_totals_and_gates_are_additive(self) -> None:
        self.assertEqual(
            self.truth["totals"],
            {
                "bounded_passing_witnesses": 50907,
                "effective_methods": 69807,
                "effective_negatives": 57445,
                "exact_gates": 500,
                "failed_witnesses": 29106,
                "open_gaps": 510,
            },
        )
        self.assertEqual(self.truth["declared_proposal_chain"], 10610)
        self.assertEqual(self.truth["primary_pillar"], "Freed ID and CBR Heart")

    def test_13_sources_are_vocabulary_only(self) -> None:
        source = load(X2 / "source-use-receipt.json")
        self.assertEqual(source["network_rows_downloaded"], 0)
        self.assertEqual(source["real_rows_ingested"], 0)
        self.assertFalse(source["citations_are_observations"])
        self.assertEqual(source["use"], "vocabulary_and_refusal_conditions_only")

    def test_14_flashcards_have_exact_four_tiers_and_thirteen_sections(self) -> None:
        self.assertEqual(self.flashcards["card_count"], 67)
        self.assertEqual(self.flashcards["section_count"], 13)
        self.assertEqual(
            self.flashcards["tier_counts"],
            {"owner": 1, "pillar": 3, "practice": 3, "task": 60},
        )
        self.assertEqual(len({row["card_id"] for row in self.flashcards["cards"]}), 67)
        self.assertTrue(all(row["real_rows"] == 0 for row in self.flashcards["cards"]))
        self.assertTrue(
            all(not row["authority_credit"] for row in self.flashcards["cards"])
        )
        self.assertEqual(self.flashcard_manifest["card_count"], 67)
        self.assertEqual(len(self.flashcard_manifest["card_ids"]), 67)

    def test_15_three_existing_tools_accept_and_reject_without_install(self) -> None:
        rows = self.tools["three_bounded_tool_smokes"]
        self.assertEqual(
            [row["name"] for row in rows], ["jsonschema", "pydantic", "numpy"]
        )
        self.assertTrue(all(row["accepting_fixture_accepted"] for row in rows))
        self.assertTrue(all(row["rejecting_fixture_rejected"] for row in rows))
        self.assertTrue(all(row["installation_action"] == "none" for row in rows))
        self.assertEqual(self.tools["new_package_installations"], 0)

    def test_16_all_x2_json_documents_parse(self) -> None:
        paths = sorted((X2).rglob("*.json")) + sorted(
            VALIDATION.glob("evidence-*.json")
        )
        self.assertGreaterEqual(len(paths), 19)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_17_normalized_lf_manifest_replays_worktree(self) -> None:
        self.assertEqual(self.manifest["entry_count"], len(self.manifest["entries"]))
        for entry in self.manifest["entries"]:
            data = (
                (ROOT / entry["path"])
                .read_bytes()
                .replace(b"\r\n", b"\n")
                .replace(b"\r", b"\n")
            )
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(
                hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"]
            )

    def test_18_staged_review_has_exact_self_exclusion_arithmetic(self) -> None:
        entries = {row["path"] for row in self.manifest["entries"]}
        exclusions = set(self.manifest["declared_self_exclusions"])
        self.assertFalse(entries & exclusions)
        self.assertEqual(set(self.review["expected_paths"]), entries | exclusions)
        self.assertEqual(self.review["path_count"], len(entries) + len(exclusions))
        self.assertEqual(self.review["x1_paths"], [])
        self.assertEqual(self.review["x1_sha"], X1_SHA)

    def test_19_five_class_privacy_scan_has_zero_confirmed_hits(self) -> None:
        self.assertEqual(self.privacy["class_count"], 5)
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertEqual(self.privacy["confirmed_hits"], [])
        self.assertTrue(
            all(
                row["adjudication"] == "scanner_definition_or_synthetic_test_only"
                for row in self.privacy["candidates"]
            )
        )

    def test_20_terminal_verdict_and_route_remain_gated(self) -> None:
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        checklist = load(X2 / "complete-incomplete-checklist.json")
        joined = " ".join(checklist["incomplete_or_reserved"])
        self.assertIn("Māori-authority", joined)
        self.assertIn("Stage 20", joined)
        route = load(X1 / "route-plan.json")
        self.assertTrue(route["prepared_not_sent"])
        self.assertFalse(route["send_before_terminal_gate"])
        self.assertEqual(route["tavian_sol"], "ON_STANDBY")


if __name__ == "__main__":
    unittest.main()

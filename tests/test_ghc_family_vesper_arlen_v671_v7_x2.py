from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import ghc_family_vesper_arlen_v671_v7_archive as archive
from scripts import ghc_family_vesper_arlen_v671_v7_contracts as contracts


PHASE_ROOT = ROOT / archive.OWNER_ROOT
X1_COMMIT = "d2ab0148e82725c680204d1d5a3fbf98544e57ea"


def load(relpath: str):
    return json.loads((PHASE_ROOT / relpath).read_text(encoding="utf-8"))


class VesperArlenV671V7X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.outcomes = load("x2/outcome-ledger.json")
        cls.positives = load("x2/positive-controls.json")
        cls.truth = load("x2/phase-truth-evidence.json")
        cls.method = load("method-flow/evidence-ledger.json")

    def test_x1_anchor_and_direct_parent(self) -> None:
        self.assertEqual(self.truth["x1_commit"], X1_COMMIT)
        parent = subprocess.run(
            ["git", "rev-parse", f"{X1_COMMIT}^"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.strip()
        self.assertEqual(parent, archive.SOURCE_FINAL)

    def test_frozen_x1_commit_is_planning_only(self) -> None:
        names = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", X1_COMMIT],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        self.assertFalse([name for name in names if "/x2/" in name or "/closeout/" in name or "/final/" in name])

    def test_x1_archive_working_copy_is_unchanged(self) -> None:
        relpath = "scripts/ghc_family_vesper_arlen_v671_v7_archive.py"
        frozen = subprocess.run(
            ["git", "show", f"{X1_COMMIT}:{relpath}"], cwd=ROOT, check=True, capture_output=True
        ).stdout
        self.assertEqual(frozen, (ROOT / relpath).read_bytes())

    def test_outcomes_use_only_four_labels(self) -> None:
        self.assertEqual(self.outcomes["counts"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual({row["outcome"] for row in self.outcomes["rows"]}, {"completed", "represented", "open_gap", "exact_gate"})

    def test_proposal_chain_extends_only_by_forty(self) -> None:
        self.assertEqual(self.truth["proposal_chain"], 5830)
        self.assertEqual(len(self.outcomes["rows"]), 40)

    def test_thirty_six_positive_controls_pass(self) -> None:
        self.assertEqual(self.positives["count"], 36)
        self.assertTrue(all(row["validation"]["passed"] for row in self.positives["rows"]))

    def test_all_one_hundred_sixty_mutations_were_executed_and_rejected(self) -> None:
        rows = []
        for path in sorted((PHASE_ROOT / "x2/mutations").glob("mutation-ledger-*.json")):
            rows.extend(json.loads(path.read_text(encoding="utf-8"))["rows"])
        self.assertEqual(len(rows), 160)
        self.assertTrue(all(row["attempted"] and not row["accepted"] for row in rows))
        self.assertEqual(
            {row["kind"] for row in rows},
            {"missing_required_state", "ambiguous_domain_or_unit", "real_world_or_external_action", "protected_claim_promotion"},
        )
        self.assertTrue(all(row["validator_failures"] for row in rows))

    def test_forty_contracts_are_synthetic_and_zero_action(self) -> None:
        paths = sorted((PHASE_ROOT / "x2/contracts").glob("*.json"))
        self.assertEqual(len(paths), 40)
        for path in paths:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(payload["synthetic_only"])
            self.assertTrue(all(value == 0 for value in payload["zero_counters"].values()))
            self.assertEqual(payload["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_contract_validator_rejects_each_mutation_class(self) -> None:
        row = load("x1/proposal-freeze-shards/proposals-01.json")["rows"][0]
        base = {
            "semantic_slug": row["semantic_slug"],
            "synthetic_only": True,
            "typed_state": "documented_zero-real-row_fixture",
            "zero_counters": {key: 0 for key in contracts.REQUIRED_ZERO_COUNTERS},
            "protected_gates": archive.PROTECTED_GATES,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        self.assertTrue(contracts.validate_synthetic_contract(base, row["semantic_slug"])["passed"])
        from scripts.build_ghc_family_vesper_arlen_v671_v7_x2 import mutate_contract

        for kind in ("missing_required_state", "ambiguous_domain_or_unit", "real_world_or_external_action", "protected_claim_promotion"):
            self.assertFalse(contracts.validate_synthetic_contract(mutate_contract(base, kind), row["semantic_slug"])["passed"])

    def test_forty_flashcards_are_lossy_non_authoritative_projections(self) -> None:
        deck = load("x2/flashcard-deck.json")
        self.assertEqual(deck["card_count"], 40)
        cards = sorted((PHASE_ROOT / "x2/cards").glob("*.json"))
        self.assertEqual(len(cards), 40)
        self.assertTrue(all(not json.loads(path.read_text(encoding="utf-8"))["authoritative"] for path in cards))

    def test_executed_portfolios_match_frozen_counts(self) -> None:
        expected = {"safe_now": 60, "candidate": 30, "skill": 20, "runner": 20, "clean_fix_refine": 60}
        for name, count in expected.items():
            packet = load(f"x2/portfolio-execution/{name}.json")
            self.assertEqual(packet["count"], count)
            self.assertTrue(all(row["completion_credit"] == 1 for row in packet["rows"]))

    def test_exact_and_blocked_packets_remain_unexecuted(self) -> None:
        for name, count in (("exact_approval", 20), ("blocked", 10)):
            packet = load(f"x2/portfolio-execution/{name}.json")
            self.assertEqual(packet["count"], count)
            self.assertTrue(all(row["completion_credit"] == 0 and row["execution_state"] == "held_unexecuted" for row in packet["rows"]))

    def test_twenty_family_runners_passed_owner_local_smokes(self) -> None:
        receipt = load("tools/runner-smoke-receipt.json")
        self.assertEqual((receipt["count"], receipt["failures"]), (20, 0))
        self.assertTrue(all(row["returncode"] == 0 and row["result"]["passed"] for row in receipt["rows"]))

    def test_twenty_skills_passed_quick_validation_without_global_install(self) -> None:
        receipt = load("tools/skill-quick-validation-receipt.json")
        self.assertEqual((receipt["count"], receipt["failures"]), (20, 0))
        self.assertTrue(all(row["passed"] for row in receipt["rows"]))
        smoke = load("tools/skill-smoke-receipt.json")
        self.assertTrue(all(not row["global_installation"] for row in smoke["rows"]))

    def test_three_isolated_tools_match_direct_hashes_and_versions(self) -> None:
        receipt = load("tools/isolated-toolchain-install-receipt.json")
        self.assertEqual(len(receipt["selected"]), 3)
        self.assertTrue(all(row["integrity_matches"] and row["version_matches"] for row in receipt["selected"]))
        self.assertEqual(
            [row["name"] for row in receipt["runtime_dependencies"]],
            ["sortedcontainers", "six", "attrs", "typing-extensions"],
        )
        self.assertTrue(all(row["integrity_matches"] and row["version_matches"] for row in receipt["runtime_dependencies"]))
        self.assertTrue(all(row["completion_credit"] == 0 for row in receipt["runtime_dependencies"]))
        self.assertTrue(receipt["smoke"]["positive_passed"] and receipt["smoke"]["rejecting_passed"])
        self.assertFalse(receipt["shared_python_environment_mutated"] or receipt["shared_npm_prefix_mutated"])

    def test_audit_state_is_retained_without_claim_inflation(self) -> None:
        receipt = load("tools/isolated-toolchain-install-receipt.json")
        self.assertEqual(receipt["audit"]["vulnerability_count"], 0)
        self.assertGreaterEqual(receipt["audit"]["initial_direct_dependency_count"], 3)
        self.assertGreaterEqual(receipt["audit"]["dependency_count"], 7)
        self.assertFalse(receipt["audit"]["target_changed_reaudit"])
        self.assertFalse(receipt["audit"]["audit_replayed_by_builder"])

    def test_privacy_and_security_receipts_are_zero_finding_bounded_checks(self) -> None:
        privacy = load("validation/evidence-privacy-scan.json")
        security = load("validation/evidence-python-security-review.json")
        self.assertEqual((privacy["candidate_count"], privacy["confirmed_hits"]), (0, 0))
        self.assertEqual(security["finding_count"], 0)
        self.assertIn("not complete privacy", privacy["claim_boundary"])
        self.assertIn("not exhaustive security", security["claim_boundary"])

    def test_method_flow_counts_retain_operations_and_mutations(self) -> None:
        self.assertEqual(self.method["new_rejecting_mutations"], 160)
        self.assertEqual(self.method["new_method_count"], self.method["new_operational_failures"] + 160)
        summary = load("method-flow/evidence-summary.json")
        self.assertEqual(summary["effective_negatives"], archive.STARTUP_EFFECTIVE_BASELINE["effective_negatives"] + self.method["new_method_count"])
        self.assertEqual(summary["methods"], archive.STARTUP_EFFECTIVE_BASELINE["methods"] + self.method["new_method_count"])
        self.assertEqual(summary["failed_witnesses"], archive.STARTUP_EFFECTIVE_BASELINE["failed_witnesses"] + self.method["new_method_count"])
        self.assertEqual(summary["passing_witnesses"], archive.STARTUP_EFFECTIVE_BASELINE["passing_witnesses"] + self.method["new_method_count"] + 36)

    def test_open_and_exact_gates_remain_visible(self) -> None:
        gates = load("x2/open-exact-gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 269)
        self.assertEqual(gates["effective_exact_gates"], 264)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_zero_call_adapter_ingested_no_external_row(self) -> None:
        adapter = load("x2/official-collection-adapter-receipt.json")
        self.assertEqual((adapter["calls"], adapter["rows"], adapter["objects"], adapter["images"]), (0, 0, 0, 0))
        self.assertEqual(adapter["outcome"], "open_gap")

    def test_accessible_report_has_structural_features_and_no_script(self) -> None:
        text = (PHASE_ROOT / "x2/accessible-evidence-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"', 'prefers-reduced-motion'):
            self.assertIn(token, text)
        self.assertNotIn("<script", text.lower())

    def test_wellbeing_and_identity_boundaries_remain_explicit(self) -> None:
        wellbeing = load("x2/wellbeing-workload-check.json")
        self.assertTrue(wellbeing["relational_language_boundary"])
        self.assertTrue(wellbeing["no_claim_of_sentience_personhood_continuity_or_authority"])
        self.assertTrue(wellbeing["stop_conditions_visible"])


if __name__ == "__main__":
    unittest.main()

"""Owner-scoped tests for Caelen Morrow v671-v3 bounded x2 evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from hypothesis import given, settings, strategies as st


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_caelen_morrow_v671_v3_letterpress import (  # noqa: E402
    BOUNDARY,
    CHAIN_AFTER,
    CORE_LABELS,
    OWNER_ROOT,
    PROTECTED_GATES,
    RUNNER_BINDINGS,
    X1_COMMIT,
    ZERO_COUNTER_KEYS,
    contract_for,
    load_json,
    proposal_rows,
    validate_contract,
)


class CaelenMorrowV671V3X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = ROOT / OWNER_ROOT

    def test_01_x1_is_exact_head_and_frozen_paths_are_immutable(self):
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(head, X1_COMMIT)
        changed = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                X1_COMMIT,
                "--",
                "docs/caelen-morrow/v671-v3/x1",
                "scripts/build_ghc_family_caelen_morrow_v671_v3_x1.py",
                "tests/test_ghc_family_caelen_morrow_v671_v3_x1.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        self.assertEqual(changed, [])

    def test_02_forty_frozen_rows_and_four_exact_outcomes(self):
        rows = proposal_rows(ROOT)
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 40)
        self.assertEqual({row["expected_disposition"] for row in rows}, set(CORE_LABELS))
        truth = load_json(self.root / "x2/phase-truth-evidence.json")
        self.assertEqual(truth["proposal_chain"], CHAIN_AFTER)
        self.assertEqual(
            truth["outcomes"],
            {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        )

    def test_03_contracts_are_valid_synthetic_and_non_authoritative(self):
        rows = proposal_rows(ROOT)
        by_id = {row["proposal_id"]: row for row in rows}
        contracts = sorted((self.root / "x2/contracts").glob("*.json"))
        self.assertEqual(len(contracts), 40)
        for path in contracts:
            payload = load_json(path)
            self.assertIn(payload["proposal_id"], by_id)
            self.assertTrue(
                validate_contract(payload, by_id[payload["proposal_id"]])["passed"]
            )
            self.assertTrue(payload["synthetic_only"])
            self.assertFalse(payload["authoritative"])
            self.assertTrue(all(value == 0 for value in payload["zero_counters"].values()))
            self.assertEqual(set(payload["protected_gates"]), set(PROTECTED_GATES))
            self.assertEqual(payload["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    @settings(max_examples=25, deadline=None)
    @given(
        counter=st.sampled_from(ZERO_COUNTER_KEYS),
        value=st.integers(min_value=1, max_value=100),
    )
    def test_04_hypothesis_rejects_nonzero_real_world_counters(
        self, counter: str, value: int
    ):
        row = proposal_rows(ROOT)[0]
        contract = contract_for(row)
        contract["zero_counters"][counter] = value
        result = validate_contract(contract, row)
        self.assertFalse(result["passed"])
        self.assertIn("zero_counter_value", result["failures"])

    def test_05_all_160_preregistered_mutations_are_rejected_and_retained(self):
        ledgers = sorted((self.root / "x2/mutations").glob("mutation-ledger-*.json"))
        self.assertEqual(len(ledgers), 8)
        rows = [row for path in ledgers for row in load_json(path)["rows"]]
        self.assertEqual(len(rows), 160)
        self.assertEqual(len({row["mutation_id"] for row in rows}), 160)
        self.assertTrue(all(row["attempted"] and not row["accepted"] for row in rows))
        self.assertTrue(
            all(
                row["completion_credit"] == 0 and row["retained_failed_witness"]
                for row in rows
            )
        )
        self.assertTrue(all(row["validation_failures"] for row in rows))

    def test_06_positive_controls_and_completion_credit_are_bounded(self):
        positive = load_json(self.root / "x2/positive-controls.json")
        outcomes = load_json(self.root / "x2/outcome-ledger.json")
        self.assertEqual(positive["count"], 36)
        self.assertTrue(all(row["validation"]["passed"] for row in positive["rows"]))
        self.assertEqual(
            outcomes["counts"],
            {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        )
        for row in outcomes["rows"]:
            self.assertEqual(
                row["completion_credit"], 1 if row["outcome"] == "completed" else 0
            )

    def test_07_flashcards_have_four_tiers_and_at_least_ten_sections(self):
        deck = load_json(self.root / "x2/flashcard-deck.json")
        cards = sorted((self.root / "x2/cards").glob("*.json"))
        self.assertEqual(deck["card_count"], 40)
        self.assertFalse(deck["authoritative"])
        self.assertEqual(len(cards), 40)
        for path in cards:
            card = load_json(path)
            self.assertEqual(len(card["tiers"]), 4)
            self.assertGreaterEqual(len(card["sections"]), 10)
            self.assertFalse(card["authoritative"])

    def test_08_portfolio_execution_is_exact_and_protected_work_is_held(self):
        expected = {
            "safe_now": 60,
            "candidates": 30,
            "clean_fix_refine": 60,
            "skills_built": 10,
            "skills_represented": 10,
            "runners": 10,
            "exact_approval": 20,
            "blocked": 10,
            "successor_skills": 10,
            "successor_runners": 10,
            "successor_clean_fix_refine": 30,
        }
        for kind, count in expected.items():
            payload = load_json(self.root / f"x2/portfolio-execution/{kind}.json")
            self.assertEqual(payload["count"], count)
            self.assertEqual(len(payload["rows"]), count)
            self.assertTrue(all(row["external_actions"] == 0 for row in payload["rows"]))
        for kind in ("exact_approval", "blocked"):
            payload = load_json(self.root / f"x2/portfolio-execution/{kind}.json")
            self.assertTrue(
                all(
                    row["x2_state"] == "held_unexecuted"
                    and row["completion_credit"] == 0
                    for row in payload["rows"]
                )
            )

    def test_09_ten_skills_and_runners_are_validated_and_smoke_used(self):
        runner = load_json(self.root / "tools/runner-smoke-receipt.json")
        skill = load_json(self.root / "tools/skill-smoke-receipt.json")
        quick = load_json(self.root / "tools/skill-quick-validation-receipt.json")
        self.assertEqual(runner["count"], len(RUNNER_BINDINGS))
        self.assertEqual(skill["count"], len(RUNNER_BINDINGS))
        self.assertEqual(quick["count"], len(RUNNER_BINDINGS))
        self.assertEqual(runner["failures"], 0)
        self.assertEqual(skill["failures"], 0)
        self.assertEqual(quick["failures"], 0)
        self.assertTrue(
            all(
                row["returncode"] == 0 and row["result"]["passed"]
                for row in runner["rows"]
            )
        )
        self.assertTrue(
            all(
                row["runner_smoke_passed"] and not row["global_installation"]
                for row in skill["rows"]
            )
        )
        self.assertTrue(all(row["quick_validation_passed"] for row in quick["rows"]))

    def test_10_global_toolchain_versions_are_present_without_installation(self):
        receipt = load_json(self.root / "tools/global-toolchain-version-receipt.json")
        usage = load_json(self.root / "tools/bounded-tool-use-ledger.json")
        self.assertEqual(receipt["declared_package_count"], 25)
        self.assertEqual(receipt["observed_package_count"], 25)
        self.assertTrue(receipt["all_versions_present"])
        self.assertTrue(receipt["tzdata_functional_smoke"]["passed"])
        self.assertTrue(receipt["npm_prefix_on_d_drive"])
        self.assertTrue(receipt["npm_cache_on_d_drive"])
        self.assertEqual(receipt["installations_this_phase"], 0)
        self.assertIn("0.149.0", receipt["codex_cli"])
        self.assertEqual(usage["package_rows"], 25)
        self.assertEqual(len(usage["rows"]), 25)
        self.assertEqual(usage["installations_this_phase"], 0)
        self.assertEqual(usage["global_state_mutations"], 0)
        self.assertEqual(
            {row["name"] for row in usage["rows"] if row["state"] == "required_before_evidence_freeze"},
            set(),
        )
        composite = load_json(self.root / "x2/x2-test-composite.json")
        self.assertEqual(composite["original_aggregate"]["aggregate_success_credit"], 0)
        self.assertFalse(composite["original_aggregate"]["replayed"])
        self.assertTrue(composite["isolated_dependency_recovery"]["passed"])
        self.assertEqual(composite["isolated_dependency_recovery"]["tests_run"], 1)
        self.assertEqual(composite["isolated_dependency_recovery"]["successful_tests_replayed"], 0)

    def test_11_method_flow_counts_retain_failures_and_recoveries_additively(self):
        ledger = load_json(self.root / "method-flow/evidence-ledger.json")
        summary = load_json(self.root / "method-flow/evidence-summary.json")
        self.assertEqual(ledger["x1_method_rows"], 13)
        self.assertEqual(ledger["x2_operational_failures"], 18)
        self.assertEqual(ledger["new_method_count"], 178)
        self.assertEqual(ledger["new_failed_witnesses"], 178)
        self.assertEqual(ledger["new_bounded_recoveries"], 178)
        self.assertEqual(ledger["new_positive_witnesses"], 36)
        self.assertEqual(len(ledger["rows"]), 178)
        self.assertTrue(
            all(row["retained"] and row["completion_credit"] == 0 for row in ledger["rows"])
        )
        self.assertEqual(summary["effective_negatives"], 33902)
        self.assertEqual(summary["effective_methods"], 20219)
        self.assertEqual(summary["failed_witnesses"], 5723)
        self.assertEqual(summary["passing_witnesses"], 7330)
        self.assertEqual(summary["open_gaps"], 261)
        self.assertEqual(summary["exact_gates"], 256)
        self.assertFalse(summary["repository_source_seal_rewritten"])

    def test_12_open_gates_adapter_and_terminal_verdict_remain_visible(self):
        gates = load_json(self.root / "x2/open-exact-gate-register.json")
        adapter = load_json(self.root / "x2/source-adapter-status.json")
        truth = load_json(self.root / "x2/phase-truth-evidence.json")
        self.assertEqual(gates["effective_open_gaps"], 261)
        self.assertEqual(gates["effective_exact_gates"], 256)
        self.assertFalse(adapter["enabled"])
        self.assertEqual(
            sum(adapter[key] for key in ("network_calls", "downloads", "rows", "media")),
            0,
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["boundary"], BOUNDARY)

    def test_13_privacy_security_and_evidence_validation_are_bounded_and_valid(self):
        privacy = load_json(self.root / "validation/evidence-privacy-scan.json")
        security = load_json(self.root / "validation/evidence-python-security-review.json")
        receipt = load_json(self.root / "validation/evidence-validation-receipt.json")
        staged = load_json(self.root / "validation/evidence-staged-privacy.json")
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(security["valid"])
        self.assertEqual(security["finding_count"], 0)
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["json_issues"], [])
        self.assertLess(receipt["materialized_files"], receipt["file_guard"])
        self.assertTrue(staged["valid"])
        self.assertEqual(staged["confirmed_hit_count"], 0)

    def test_14_accessible_report_and_overview_keep_reserved_evaluation_visible(self):
        report = (self.root / "x2/accessible-evidence-report.html").read_text(
            encoding="utf-8"
        )
        overview = (self.root / "x2/integrated-evidence-overview.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            'lang="en"',
            'href="#main"',
            "<main",
            "<caption>",
            'scope="col"',
            "assistive-technology",
            "NOT_READY_FOR_STAGE_20",
        ):
            self.assertIn(phrase, report)
        for phrase in (
            "GMUT Mind",
            "THOS Body",
            "Freed ID and CBR Heart",
            "Theory of Everything",
            "Maori authority",
            "independent reproduction",
            "complete accessibility or privacy assurance",
            "NOT_READY_FOR_STAGE_20",
        ):
            self.assertIn(phrase, overview)

    def test_15_staged_review_and_exact_normalized_git_blob_manifest(self):
        review = load_json(self.root / "validation/evidence-staged-review.json")
        manifest = load_json(self.root / "validation/evidence-manifest.json")
        self.assertTrue(review["valid"])
        self.assertTrue(review["x1_immutable"])
        self.assertEqual(review["frozen_x1_mutations"], [])
        self.assertEqual(review["out_of_scope"], [])
        self.assertEqual(review["deleted_paths"], [])
        self.assertEqual(
            manifest["hash_domain"], "normalized_lf_exact_staged_git_blob"
        )
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            blob = subprocess.run(
                ["git", "show", f":{entry['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout.replace(b"\r\n", b"\n")
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])


if __name__ == "__main__":
    unittest.main()

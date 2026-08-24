#!/usr/bin/env python3
"""Bounded tests for the planning-only Orin Thale v668-v7 x1 freeze."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from scripts.ghc_family_orin_thale_v668_v7_archive import (
    ACTIVATION_OVERLAY,
    ALLOWED_OUTCOMES,
    BRANCH,
    INHERITED_FROZEN_PROPOSALS,
    OWNER,
    PHASE,
    PHASE_ROOT,
    PRIMARY_PILLAR,
    PROPOSAL_BLUEPRINTS,
    PROTECTED_GATES,
    ROOT,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_FINAL,
    TERMINAL_VERDICT,
)


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class OrinX1FreezeTests(unittest.TestCase):
    def test_exact_owner_phase_branch_source(self) -> None:
        truth = load("x1/phase-truth.json")
        self.assertEqual((OWNER, PHASE, BRANCH, SOURCE_FINAL), ("Orin Thale", "v668-v7", "codex/GHC-Family/orin-thale-v668-v7-full-tools", "8b4c6de2c4ae00c876ffb1342fc6614ef901ab73"))
        self.assertEqual(truth["owner"], OWNER)
        self.assertEqual(truth["phase"], PHASE)
        self.assertEqual(truth["branch"], BRANCH)

    def test_x1_is_planning_only(self) -> None:
        truth = load("x1/phase-truth.json")
        self.assertEqual(truth["lifecycle"], "x1_planning_only")
        self.assertEqual(truth["x2_implementation_count"], 0)
        self.assertEqual(truth["x2_outcome_claim_count"], 0)
        for name in ("x2", "evidence", "closeout", "final", "seal", "skills", "runners"):
            self.assertFalse((PHASE_ROOT / name).exists(), name)

    def test_primary_pillar_and_truth_labels(self) -> None:
        truth = load("x1/phase-truth.json")
        self.assertEqual(PRIMARY_PILLAR, "GMUT Mind")
        self.assertEqual(tuple(truth["allowed_outcomes"]), ALLOWED_OUTCOMES)
        self.assertEqual(truth["expected_outcome_counts"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertIsNone(truth["observed_outcome_counts"])

    def test_exactly_forty_distinct_proposals(self) -> None:
        freeze = load("x1/proposal-freeze.json")
        self.assertEqual(len(PROPOSAL_BLUEPRINTS), 40)
        self.assertEqual(freeze["inherited_frozen_proposals"], INHERITED_FROZEN_PROPOSALS)
        self.assertEqual(freeze["new_proposal_count"], 40)
        self.assertEqual(freeze["new_frozen_total"], 4870)
        titles = [title.casefold() for title, _, _ in PROPOSAL_BLUEPRINTS]
        slugs = [slug for _, _, slug in PROPOSAL_BLUEPRINTS]
        self.assertEqual(len(set(titles)), 40)
        self.assertEqual(len(set(slugs)), 40)

    def test_every_proposal_has_required_contract(self) -> None:
        rows = []
        for shard in load("x1/proposal-freeze.json")["proposal_shards"]:
            rows.extend(json.loads((ROOT / shard["path"]).read_text(encoding="utf-8"))["new_proposals"])
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
        self.assertEqual(len(rows), 40)
        for row in rows:
            self.assertTrue(required <= set(row))
            self.assertIn(row["expected_disposition"], ALLOWED_OUTCOMES)
            self.assertEqual(len(row["negative_fixtures"]), 4)
            self.assertFalse(row["visible_title_collision"])
            self.assertFalse(row["semantic_neighbor_quarantined"])
            self.assertEqual(row["x2_execution_count"], 0)

    def test_novelty_audit_retains_compressed_gap(self) -> None:
        audit = load("x1/proposal-chain-audit.json")
        self.assertEqual(audit["declared_inherited_chain_count"], 4830)
        self.assertEqual(audit["selected_count"], 20)
        self.assertEqual(audit["selected_novelty_credit"], 0)
        self.assertEqual(audit["selected_completion_credit"], 0)
        self.assertEqual(audit["parse_failures"], [])
        self.assertGreater(audit["compressed_title_gap_count_minimum"], 0)
        self.assertIn("OPEN_GAP", audit["coverage_state"])

    def test_portfolio_floors_and_zero_x1_credit(self) -> None:
        freeze = load("x1/portfolio-freeze.json")
        expected = {"safe_now": 60, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 60, "exact_approval": 20, "blocked": 10}
        self.assertEqual(freeze["category_counts"], expected)
        for category, shards in freeze["category_shards"].items():
            rows = []
            for shard in shards:
                rows.extend(json.loads((ROOT / shard["path"]).read_text(encoding="utf-8"))["rows"])
            self.assertEqual(len(rows), expected[category])
            self.assertTrue(all(row["completion_credit"] == 0 for row in rows))
            self.assertTrue(all(row["x2_execution_count"] == 0 for row in rows))

    def test_family_current_skill_and_runner_names(self) -> None:
        self.assertEqual(len(SKILL_NAMES), 20)
        self.assertEqual(len(RUNNER_NAMES), 10)
        self.assertTrue(all(name.startswith("ghc-family-") for name in SKILL_NAMES))
        self.assertTrue(all(name.startswith("ghc_family_") for name in RUNNER_NAMES))
        inventory = load("x1/compatibility-inventory.json")
        self.assertEqual(inventory["historical_callers_deleted_or_renamed"], 0)
        self.assertEqual(inventory["global_installs_in_x1"], 0)

    def test_source_receipts_preserve_zero_canonical_success(self) -> None:
        intake = load("x1/source-intake.json")
        self.assertEqual(intake["source_canonical_invocation_count"], 1)
        self.assertEqual(intake["source_canonical_success_count"], 0)
        self.assertFalse(intake["source_aggregate_replayed"])
        self.assertEqual(intake["six_manifest_entry_replay"], 976)
        self.assertEqual(intake["manifest_mismatches"], 0)
        self.assertEqual(intake["source_to_final_commits"], 4)
        self.assertEqual(intake["source_to_final_merges"], 0)

    def test_source_ledger_has_zero_empirical_rows(self) -> None:
        ledger = load("x1/source-ledger.json")
        self.assertEqual(ledger["downloads"], 0)
        self.assertEqual(ledger["empirical_rows"], 0)
        self.assertEqual(ledger["empirical_credit"], 0)
        ids = {row["source_id"] for row in ledger["sources"]}
        self.assertTrue({"SRC-LOC-BOOKS", "SRC-MICROLOCAL", "SRC-GWOSC-API", "SRC-PROV-DM", "SRC-VC20", "SRC-WCAG22", "SRC-TMR"} <= ids)

    def test_method_flow_preserves_each_failure_and_recovery(self) -> None:
        ledger = load("method-flow/x1-ledger.json")
        counts = ledger["counts"]
        self.assertGreaterEqual(counts["methods"], 5)
        self.assertEqual(counts["witness_results"]["fail"], counts["methods"])
        self.assertEqual(counts["witness_results"]["pass"], counts["methods"])
        self.assertEqual(len(ledger["methods"]), counts["methods"])
        self.assertEqual(len(ledger["witnesses"]), counts["methods"] * 2)
        self.assertTrue(all(method["retained_negative_ids"] for method in ledger["methods"]))
        summary = load("method-flow/x1-summary.json")
        self.assertTrue(summary["all_failures_retained"])
        self.assertFalse(summary["correction_erases_failure"])

    def test_activation_and_x1_counts_are_additive(self) -> None:
        truth = load("x1/phase-truth.json")
        overlay = truth["x1_overlay"]
        failures = load("method-flow/x1-summary.json")["failure_count"]
        self.assertEqual(ACTIVATION_OVERLAY["effective_negatives"] + failures, overlay["effective_negatives"])
        self.assertEqual(ACTIVATION_OVERLAY["methods"] + failures, overlay["methods"])
        self.assertEqual(ACTIVATION_OVERLAY["failed_witnesses"] + failures, overlay["failed_witnesses"])
        self.assertEqual(ACTIVATION_OVERLAY["passing_witnesses"] + failures, overlay["passing_witnesses"])

    def test_overview_is_three_page_equivalent_and_bounded(self) -> None:
        text = (PHASE_ROOT / "x1/integrated-overview.md").read_text(encoding="utf-8")
        words = re.findall(r"\b\w+[\w'-]*\b", text)
        self.assertGreaterEqual(len(words), 1500)
        self.assertLessEqual(len(words), 6000)
        for required in ("GMUT Mind", "THOS Body", "Freed ID/CBR Heart", "NOT_READY_FOR_STAGE_20", "zero network requests"):
            self.assertIn(required, text)

    def test_route_remains_unsent_and_terminally_gated(self) -> None:
        route = load("x1/route-plan.json")
        self.assertFalse(route["successor_contacted"])
        self.assertFalse(route["successor_precontacted"])
        self.assertTrue(route["terminal_gate_required"])
        self.assertEqual(route["maximum_sends"], 1)
        self.assertFalse(route["standby_substitution"])

    def test_terminal_and_authority_boundaries(self) -> None:
        truth = load("x1/phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], TERMINAL_VERDICT)
        self.assertEqual(set(truth["protected_gates"]), set(PROTECTED_GATES))
        self.assertIn("Maori-authority", truth["protected_gates"])

    def test_x1_manifest_and_allowlist_cover_exact_surface(self) -> None:
        manifest = load("x1/x1-manifest.json")
        allowlist = load("validation/x1-staged-allowlist.json")
        paths = {row["path"] for row in manifest["entries"]}
        paths.update(manifest["self_exclusions"])
        intended = set(allowlist["intended_paths_before_manifest"])
        self.assertEqual(paths, intended | {f"docs/orin-thale/v668-v7/x1/x1-manifest.json"})
        self.assertEqual(allowlist["x2_paths"], 0)
        self.assertEqual(len(paths), len(manifest["entries"]) + 1)

    def test_public_x1_surface_has_no_raw_private_markers(self) -> None:
        patterns = (
            "source_" + "thread_id",
            "<codex_" + "delegation>",
            "session_meta" + ".payload.id",
            "response" + "_item",
            "C:" + "\\Users\\",
        )
        for path in PHASE_ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".txt", ".html"}:
                text = path.read_text(encoding="utf-8")
                self.assertFalse(any(marker.casefold() in text.casefold() for marker in patterns), path)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Dependency-scoped x2 checks for Neris Solane v658-v6."""

from __future__ import annotations

import json
import re
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v658_v6_phase_data as d  # noqa: E402
from ghc_family_v658_v6_runtime import evaluate_surface  # noqa: E402


PHASE = ROOT / d.PHASE_ROOT
X1 = "1591612c83feb7f47fb0b044525bf4b37f71bfb7"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class NerisV658V6EvidenceTests(unittest.TestCase):
    def test_outcome_distribution_is_exact(self) -> None:
        ledger = load("x2/proposal-ledger.json")
        self.assertEqual(d.EXPECTED_DISTRIBUTION, ledger["outcome_counts"])
        self.assertEqual(30, ledger["proposal_count"])
        self.assertEqual(Counter(d.EXPECTED_DISTRIBUTION), Counter(row["outcome"] for row in ledger["rows"]))

    def test_all_surface_artifacts_exist(self) -> None:
        for proposal in d.PROPOSALS:
            root = PHASE / "surfaces" / proposal["slug"]
            self.assertTrue((root / "contract.json").is_file(), proposal["slug"])
            self.assertTrue((root / "mutation-results.json").is_file(), proposal["slug"])
            self.assertTrue((root / "bounded-receipt.json").is_file(), proposal["slug"])

    def test_all_150_mutations_are_rejected_and_retained(self) -> None:
        total = rejected = 0
        for proposal in d.PROPOSALS:
            payload = load(f"surfaces/{proposal['slug']}/mutation-results.json")
            total += payload["mutation_count"]
            rejected += payload["rejected_count"]
            self.assertTrue(payload["all_rejected"])
            self.assertFalse(payload["authority_action_executed"])
            self.assertTrue(all(row["retained"] and row["credit"] == 0 for row in payload["results"]))
        self.assertEqual(150, total)
        self.assertEqual(150, rejected)

    def test_truth_totals_and_method_flow(self) -> None:
        truth = load("truth/phase-truth-x2.json")
        negatives = load("truth/retained-negative-register-x2.json")
        flow = load("method-flow/method-flow-state-x2.json")
        self.assertEqual(d.SOURCE_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES) + 150 + negatives["x2_operational_count"], truth["effective_negatives"])
        self.assertEqual(truth["effective_negatives"], negatives["effective_count"])
        self.assertEqual(d.SOURCE_METHODS + len(d.X1_OPERATIONAL_NEGATIVES) + 150 + negatives["x2_operational_count"], truth["effective_methods"])
        self.assertEqual(truth["effective_methods"], flow["counts"]["effective_methods"])
        self.assertTrue(flow["all_failed_witnesses_retained"])

    def test_open_gap_and_exact_gate_are_preserved(self) -> None:
        open_gap = load("truth/open-gap-register-x2.json")
        exact_gate = load("truth/exact-gate-register-x2.json")
        self.assertEqual(118, open_gap["effective_count"])
        self.assertEqual(["V6586-P29"], open_gap["proposal_ids"])
        self.assertEqual(117, exact_gate["effective_count"])
        self.assertEqual(["V6586-P30"], exact_gate["proposal_ids"])
        self.assertFalse(exact_gate["authority_action_executed"])

    def test_no_real_rows_network_calls_or_authority_actions(self) -> None:
        truth = load("truth/phase-truth-x2.json")
        self.assertFalse(truth["real_data_used"])
        self.assertFalse(truth["network_called"])
        self.assertFalse(truth["authority_action_executed"])
        for proposal in d.PROPOSALS:
            receipt = load(f"surfaces/{proposal['slug']}/bounded-receipt.json")
            self.assertFalse(receipt["real_data_used"])
            self.assertFalse(receipt["network_called"])
            self.assertFalse(receipt["authority_granted"])
            self.assertFalse(receipt["authority_action_executed"])

    def test_skills_are_owner_local_validated_and_smoke_used(self) -> None:
        payload = load("tooling/skill-creator-receipts.json")
        self.assertEqual(10, payload["skill_count"])
        self.assertEqual(10, payload["quick_validate_passed"])
        self.assertEqual(0, payload["globally_installed"])
        self.assertEqual(0, payload["subagent_forward_tests"])
        for name, _ in d.SKILL_SPECS:
            self.assertTrue((PHASE / "skills" / name / "SKILL.md").is_file())
            self.assertTrue((PHASE / "skills" / name / "agents/openai.yaml").is_file())
            self.assertTrue(load(f"skills/{name}/smoke-receipt.json")["valid"])

    def test_family_current_runners_partition_surfaces(self) -> None:
        payload = load("tooling/runner-receipts.json")
        self.assertEqual(10, payload["runner_count"])
        self.assertEqual(10, payload["valid_count"])
        self.assertEqual(30, payload["surface_count"])
        self.assertEqual(150, payload["rejected_mutation_count"])
        covered = [slug for row in payload["rows"] for slug in row["surfaces"]]
        self.assertEqual(sorted(row["slug"] for row in d.PROPOSALS), sorted(covered))

    def test_all_task_portfolios_are_completed_boundedly(self) -> None:
        tasks = load("x2/task-execution.json")
        self.assertEqual({"safe_now": 30, "candidate": 20, "clean": 30, "total": 80}, tasks["counts"])
        self.assertTrue(tasks["all_bounded"])
        self.assertTrue(all(row["state"] == "bounded_surface_recorded" for row in tasks["safe_now"]))
        self.assertEqual(d.EXPECTED_DISTRIBUTION, dict(Counter(row["outcome"] for row in tasks["safe_now"])))
        self.assertTrue(all(row["state"] == "completed_bounded_reversible_prototype" for row in tasks["candidate"]))
        self.assertTrue(all(row["state"] == "completed_additive_cleanup" for row in tasks["clean"]))

    def test_static_report_has_accessible_structure(self) -> None:
        text = (PHASE / "deliverables/v658-v6-volcanic-observatory-assurance-report.html").read_text(encoding="utf-8")
        for token in ["<html lang=\"en\">", "<title>", "href=\"#main\"", "<main id=\"main\">", "<caption>", "scope=\"col\"", "scope=\"row\"", "tabindex=\"0\"", "@media print"]:
            self.assertIn(token, text)
        self.assertEqual(30, len(re.findall(r"<tr><th scope=\"row\">V6586-P", text)))

    def test_privacy_manifest_stale_labels_and_caps(self) -> None:
        privacy = load("validation/evidence-privacy-scan.json")
        manifest = load("validation/evidence-content-manifest.json")
        stale = load("validation/stale-label-hygiene-x2.json")
        file_cap = load("validation/evidence-owner-file-cap.json")
        document_cap = load("validation/evidence-document-cap.json")
        self.assertTrue(privacy["valid"])
        self.assertEqual(0, privacy["hit_count"])
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertTrue(stale["valid"])
        self.assertEqual(0, stale["confirmed_stale_count"])
        self.assertTrue(file_cap["within_cap"])
        self.assertTrue(document_cap["all_under_limit"])

    def test_x1_frozen_paths_remain_unchanged(self) -> None:
        review = load("validation/evidence-staged-review.json")
        provenance = load("provenance/evidence-provenance.json")
        seal = load("reproduction/x1-content-seal.json")
        self.assertEqual([], review["x1_changed_paths"])
        self.assertFalse(provenance["x1_bytes_changed"])
        self.assertEqual(40, provenance["x1_paths_preserved"])
        self.assertEqual(X1, seal["x1_commit"])
        self.assertEqual(40, seal["entry_count"])
        self.assertEqual(0, seal["mismatch_count"])

    def test_route_is_unsent_and_terminally_gated(self) -> None:
        route = load("orchestration/route-state-x2.json")
        self.assertEqual("Vesper Arlen", route["next_exact_title"])
        self.assertEqual("v658-v7", route["next_phase"])
        self.assertEqual("ON_STANDBY", route["tavian_sol_state"])
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])

    def test_terminal_verdict_is_not_ready(self) -> None:
        self.assertEqual("NOT_READY_FOR_STAGE_20", load("truth/phase-truth-x2.json")["terminal_verdict"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", load("validation/evidence-validation.json")["terminal_verdict"])


def _surface_test(slug: str):
    def test(self: NerisV658V6EvidenceTests) -> None:
        result = evaluate_surface(slug)
        self.assertEqual([], result["valid_errors"])
        self.assertTrue(result["valid_fixture_passed"])
        self.assertEqual(5, result["rejected_mutation_count"])
        self.assertTrue(result["all_mutations_rejected"])
        self.assertFalse(result["authority_action_executed"])
    return test


for _proposal in d.PROPOSALS:
    setattr(NerisV658V6EvidenceTests, f"test_surface_{_proposal['proposal_id'].lower().replace('-', '_')}", _surface_test(_proposal["slug"]))


if __name__ == "__main__":
    unittest.main()

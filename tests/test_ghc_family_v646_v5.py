"""Bounded x2 evidence tests for Tamar Vey v646-v5."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v646_v5_runtime as runtime


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V646V5EvidenceTests(unittest.TestCase):
    def test_core_runtime(self):
        rows = runtime.run_all()
        self.assertEqual(len(rows), 10)
        self.assertTrue(all(row["passed"] for row in rows))

    def test_distribution(self):
        rows = load("x2-proposal-ledger.json")["proposals"]
        self.assertEqual(Counter(row["outcome"] for row in rows), Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))

    def test_expected_matches_observed(self):
        self.assertTrue(all(row["expected_disposition"] == row["outcome"] for row in load("x2-proposal-ledger.json")["proposals"]))

    def test_exactly_70_synthetic_mutations(self):
        row = load("validation/x2-synthetic-negative-register.json")
        self.assertEqual((row["count"], row["executed"], row["rejected"]), (70, 70, 70))
        self.assertTrue(all(item["retained"] for item in row["rows"]))

    def test_negative_continuity(self):
        row = load("retained-negative-register.json")
        self.assertEqual((row["inherited_sealed"], row["inherited_external_count"], row["inherited_effective"]), (2797, 3, 2800))
        self.assertEqual((row["x1_operational"], row["synthetic_executed_and_rejected"], row["x2_operational"], row["effective_total"]), (4, 70, 10, 2884))
        self.assertTrue(row["no_negative_erased"])

    def test_method_flow_failure_and_recovery(self):
        counts = load("method-flow/method-flow-state.json")["counts"]
        self.assertEqual((counts["methods"], counts["witness_results"]["fail"], counts["witness_results"]["pass"], counts["states"]["preferred"]), (13, 14, 13, 13))

    def test_gates_preserved_and_extended(self):
        row = load("exact-open-gate-register.json")
        self.assertEqual((row["effective_open_gaps"], row["effective_exact_gates"], row["silently_closed"]), (14, 15, 0))

    def test_zero_row_rubin(self):
        row = next(item for item in load("x2-proposal-ledger.json")["proposals"] if item["proposal_id"] == "V6465-P03")
        self.assertEqual((row["outcome"], row["real_rows"]), ("open_gap", 0))
        self.assertEqual(sum(load("empirical/rubin-dp1-study-contract.json")["zero_counts"].values()), 0)

    def test_thos_proxy_zero_real_entities(self):
        row = next(item for item in load("x2-proposal-ledger.json")["proposals"] if item["proposal_id"] == "V6465-P04")
        self.assertEqual((row["outcome"], row["real_participants_or_animals"]), ("represented", 0))

    def test_freed_id_proxy_zero_real_events(self):
        row = next(item for item in load("x2-proposal-ledger.json")["proposals"] if item["proposal_id"] == "V6465-P05")
        self.assertEqual((row["outcome"], row["real_keys_or_transactions"]), ("represented", 0))

    def test_cbr_authority_remains_exact(self):
        row = next(item for item in load("x2-proposal-ledger.json")["proposals"] if item["proposal_id"] == "V6465-P06")
        self.assertEqual(row["outcome"], "exact_gate")
        self.assertFalse(row["authority_delegated"])

    def test_reftable_fixture_is_disposable(self):
        row = runtime.reftable_tribunal()
        self.assertTrue(row["passed"] and row["fixture_removed"] and row["fixture_header_valid"])
        self.assertEqual((row["canonical_repository_mutations"], row["sibling_lane_mutations"]), (0, 0))

    def test_portfolio_counts(self):
        safe = load("approval-packets/x2-safe-now-execution.json")
        candidate = load("prototypes/x2-candidate-execution.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((safe["count"], candidate["count"], cleanup["count"]), (30, 20, 30))
        self.assertTrue(all(row["acceptance_gate_passed"] and not row["protected_gate_executed"] for row in safe["tasks"] + candidate["tasks"] + cleanup["tasks"]))

    def test_protected_packets_unexecuted(self):
        row = load("approval-packets/x2-safe-now-execution.json")
        self.assertEqual((row["inherited_exact_packets_preserved"], row["inherited_blocked_packets_preserved"]), (10, 5))
        self.assertEqual((row["inherited_exact_packets_executed"], row["inherited_blocked_packets_executed"]), (0, 0))

    def test_skill_packages(self):
        planned = load("prototypes/x1-skill-runner-plan.json")["skills"]
        self.assertEqual(len(planned), 20)
        for item in planned:
            self.assertTrue((PHASE / f"prototypes/skills/{item['name']}/SKILL.md").is_file())
            self.assertTrue((PHASE / f"prototypes/skills/{item['name']}/agents/openai.yaml").is_file())

    def test_runner_files(self):
        planned = load("prototypes/x1-skill-runner-plan.json")["runners"]
        self.assertEqual(len(planned), 10)
        self.assertTrue(all((SCRIPTS / row["name"]).is_file() for row in planned))

    def test_source_status_and_nonconversion(self):
        source = load("sources/source-ledger.json")
        use = load("sources/source-use-receipt.json")
        self.assertEqual(len(source["sources"]), 23)
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in source["sources"]))
        self.assertFalse(use["citation_to_observation_conversion"] or use["authority_delegated"])

    def test_static_report_structure(self):
        text = (PHASE / "deliverables/v646-v5-static-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope=\'row\'', 'NOT_READY_FOR_STAGE_20'):
            self.assertIn(token, text)
        self.assertIn("remain reserved", text)

    def test_overview_length_and_boundary(self):
        text = (PHASE / "v646-v5-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1500)
        self.assertLessEqual(len(text.split()), 6000)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("same-owner", text)

    def test_environment_no_host_change(self):
        row = load("environment/x2-environment-receipt.json")
        self.assertFalse(any(row[key] for key in ("desktop_updated", "elevated", "host_security_weakened", "windows_feature_changed", "unrelated_installation", "rebooted")))
        self.assertFalse(row["full_repository_suite_run"])

    def test_route_unsent(self):
        row = load("orchestration/terminal-route-plan.json")
        self.assertEqual((row["current_state"], row["send_count"]), ("PREPARED_NOT_SENT", 0))

    def test_x1_companions_unchanged(self):
        paths = ["docs/tamar-vey/v646-v5/x1-proposals.json", "docs/tamar-vey/v646-v5/approval-packets/x1-approval-portfolio.json", "docs/tamar-vey/v646-v5/provenance/prior-proposal-collision-audit.json", "docs/tamar-vey/v646-v5/reproduction/x1-content-seal.json"]
        for path in paths:
            result = subprocess.run(["git", "diff", "--quiet", "3f6b5302e18c7828d19ffb621da153f6ae173de0", "--", path], cwd=ROOT)
            self.assertEqual(result.returncode, 0, path)

    def test_all_phase_json_parses(self):
        for path in PHASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    def test_phase_markdown_word_caps(self):
        oversized = [(path, len(path.read_text(encoding="utf-8").split())) for path in PHASE.rglob("*.md") if len(path.read_text(encoding="utf-8").split()) > 6000]
        self.assertEqual(oversized, [])


if __name__ == "__main__":
    unittest.main()

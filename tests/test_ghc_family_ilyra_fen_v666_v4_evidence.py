"""Evidence-candidate tests for Ilyra Fen v666-v4."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v666-v4"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_ilyra_fen_v666_v4_flashcards import validate_deck
from ghc_family_ilyra_fen_v666_v4_runtime import X1_SHA, replay_manifest, scan_privacy, scan_python_security


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class IlyraFenV666V4EvidenceTests(unittest.TestCase):
    def test_x1_manifest_replays_exact_commit_blobs(self) -> None:
        replay = replay_manifest(PHASE / "validation" / "x1-content-manifest.json", X1_SHA)
        self.assertTrue(replay["valid"])
        self.assertEqual(replay["entry_count"], 18)

    def test_x1_frozen_paths_unchanged(self) -> None:
        paths = [
            "docs/ilyra-fen/v666-v4/x1",
            "scripts/build_ghc_family_ilyra_fen_v666_v4_x1.py",
            "tests/test_ghc_family_ilyra_fen_v666_v4_x1.py",
        ]
        changed = subprocess.check_output(["git", "-C", str(ROOT), "diff", "--name-only", X1_SHA, "--", *paths], text=True, encoding="utf-8").strip()
        self.assertEqual(changed, "")

    def test_proposal_chain_and_outcomes_exact(self) -> None:
        ledger = load("x2/proposal-ledger.json")
        self.assertEqual(ledger["inherited_frozen_baseline"], 4230)
        self.assertEqual(ledger["new_frozen_total"], 4250)
        self.assertEqual(len(ledger["proposals"]), 20)
        self.assertEqual(ledger["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})

    def test_all_positive_and_mutation_receipts_present(self) -> None:
        proposal_dirs = sorted((PHASE / "x2" / "proposals").iterdir())
        self.assertEqual(len(proposal_dirs), 20)
        for directory in proposal_dirs:
            bounded = json.loads((directory / "bounded-receipt.json").read_text(encoding="utf-8"))
            mutations = json.loads((directory / "mutation-results.json").read_text(encoding="utf-8"))
            self.assertTrue(bounded["positive_fixture_valid"])
            self.assertEqual(mutations["mutation_count"], 5)
            self.assertEqual(mutations["rejected_count"], 5)

    def test_method_flow_retains_one_hundred_synthetic_negatives(self) -> None:
        flow = load("method-flow/x2-method-flow.json")
        self.assertEqual(flow["new_method_count"], 215)
        self.assertEqual(flow["new_negative_count"], 100)
        self.assertEqual(flow["failed_witness_count"], 100)
        self.assertEqual(flow["bounded_passing_witness_count"], 215)

    def test_operational_failures_retained(self) -> None:
        overlay = load("method-flow/x2-operational-overlay.json")
        self.assertEqual(overlay["new_negative_count"], 10)
        self.assertEqual(overlay["new_method_count"], 10)
        self.assertEqual(len(overlay["rows"]), 10)
        self.assertTrue(overlay["no_failure_erased"])

    def test_effective_accounting_exact(self) -> None:
        summary = load("evidence/evidence-summary.json")
        self.assertEqual(summary["effective_negatives"], 26516)
        self.assertEqual(summary["effective_methods"], 11173)
        self.assertEqual(summary["open_gaps"], 186)
        self.assertEqual(summary["exact_gates"], 184)
        self.assertEqual(summary["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_authority_gap_and_gate_are_unexecuted(self) -> None:
        register = load("evidence/authority-and-evidence-gaps.json")
        self.assertEqual(register["new_open_gap_rows"][0]["status"], "open_gap")
        self.assertEqual(register["new_open_gap_rows"][0]["real_rows"], 0)
        self.assertEqual(register["new_exact_gate_rows"][0]["status"], "exact_gate")
        self.assertFalse(register["new_exact_gate_rows"][0]["executed"])

    def test_portfolio_floors_and_protected_counts(self) -> None:
        receipt = load("evidence/portfolio-evidence-receipt.json")
        self.assertEqual(receipt["executed_owner_safe_now"], 30)
        self.assertEqual(receipt["represented_owner_candidates"], 15)
        self.assertEqual(receipt["built_tested_used_phase_local_skills"], 10)
        self.assertEqual(receipt["built_smoke_tested_family_current_runners"], 10)
        self.assertEqual(receipt["completed_owner_clean_fix_refine"], 30)
        self.assertEqual(receipt["exact_approval_packets_unexecuted"], 10)
        self.assertEqual(receipt["blocked_packets_unexecuted"], 5)
        self.assertEqual(receipt["protected_items_executed"], 0)

    def test_all_tooling_smokes_passed_without_canonical(self) -> None:
        smoke = load("x2/tooling-smoke-receipt.json")
        self.assertTrue(smoke["valid"])
        self.assertEqual(smoke["passed_count"], 10)
        self.assertEqual(smoke["skill_passed_count"], 10)
        self.assertFalse(smoke["canonical_aggregate_invoked"])

    def test_phase_local_flashcard_deck_valid(self) -> None:
        result = validate_deck()
        self.assertTrue(result["valid"])
        self.assertEqual(result["card_count"], 25)
        self.assertEqual(result["mutation_rejected_count"], 5)
        self.assertEqual(result["privacy"]["confirmed_hit_count"], 0)

    def test_legacy_flashcard_partial_is_retained(self) -> None:
        retained = PHASE / "x2" / "retained-failures" / "legacy-flashcard-partial"
        self.assertTrue(retained.is_dir())
        self.assertEqual(sum(path.is_file() for path in retained.rglob("*")), 258)

    def test_source_ledger_is_current_and_zero_row(self) -> None:
        ledger = load("evidence/source-use-ledger.json")
        self.assertEqual(ledger["reviewed_at_date"], "2026-08-23")
        self.assertEqual(len(ledger["sources"]), 9)
        self.assertEqual(ledger["real_data_rows"], 0)
        self.assertTrue(ledger["citations_are_not_observations"])

    def test_environment_was_verified_without_update(self) -> None:
        environment = load("evidence/environment-version-receipt.json")
        self.assertIn("codex-cli", environment["codex_cli"])
        self.assertTrue(environment["versions_verified_only"])
        self.assertFalse(environment["software_updated"])
        self.assertFalse(environment["elevation_used"])
        self.assertFalse(environment["host_security_changed"])

    def test_family_index_method_reflection_and_toolbox_receipts(self) -> None:
        self.assertEqual(load("evidence/family-index-update.json")["new_family_current_runners"], 10)
        self.assertEqual(load("evidence/method-flow-recommendations.json")["failed_witness_count"], 18)
        self.assertEqual(len(load("evidence/reflection-remaster-receipt.json")["remastered"]), 3)
        self.assertEqual(load("evidence/meta-toolbox-receipt.json")["globally_installed"], 0)

    def test_all_phase_json_parses(self) -> None:
        paths = sorted(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 350)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_five_class_scan_has_zero_confirmed_candidates(self) -> None:
        paths = [path for path in PHASE.rglob("*") if path.is_file() and path.suffix.casefold() in {".json", ".md", ".html", ".txt"}]
        result = scan_privacy(paths)
        self.assertTrue(result["valid"])
        self.assertEqual(result["confirmed_hit_count"], 0)

    def test_bounded_python_security_scan_has_zero_findings(self) -> None:
        paths = sorted((ROOT / "scripts").glob("*ilyra_fen_v666_v4*.py"))
        result = scan_python_security(paths)
        self.assertTrue(result["valid"])
        self.assertEqual(result["finding_count"], 0)

    def test_materialized_owner_lane_below_guard(self) -> None:
        count = sum(path.is_file() for path in ROOT.rglob("*") if ".git" not in path.parts)
        self.assertLess(count, 2000)

    def test_no_closeout_or_route_delivery_paths_exist(self) -> None:
        for name in ("closeout", "seal", "final", "handoffs", "orchestration"):
            self.assertFalse((PHASE / name).exists())

    def test_identity_and_authority_boundaries_remain_explicit(self) -> None:
        checklist = load("evidence/complete-incomplete-checklist.json")
        text = json.dumps(checklist, ensure_ascii=False)
        self.assertIn("Maori-authority", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertFalse(load("evidence/evidence-summary.json")["independent_reproduction"])


if __name__ == "__main__":
    unittest.main()

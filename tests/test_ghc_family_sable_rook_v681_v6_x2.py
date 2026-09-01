from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v681-v6"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_COMMIT = "7285d38579cdf5e2fce3c6b0b013b49e940f44b5"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class SableX2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.proposals = load(X1 / "new-proposal-freeze.json")["proposals"]
        cls.evidence = load(X2 / "proposal-evidence.json")
        cls.portfolio = load(X2 / "portfolio-results.json")

    def test_head_remains_immutable_x1_before_evidence_commit(self) -> None:
        head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
        self.assertEqual(head, X1_COMMIT)

    def test_x1_immutability_receipt(self) -> None:
        receipt = load(X2 / "x1-immutability-receipt.json")
        self.assertEqual(receipt["commit"], X1_COMMIT)
        self.assertEqual(receipt["entry_count"], 20)
        self.assertEqual(receipt["manifest_mismatches"], [])
        self.assertTrue(receipt["planning_only"])
        self.assertTrue(receipt["direct_parent_is_source"])

    def test_positive_controls(self) -> None:
        positives = load(X2 / "positive-controls.json")
        self.assertEqual(positives["accepted"], 60)
        self.assertEqual(positives["real_rows"], 0)
        self.assertTrue(all(row["result"]["accepted"] for row in positives["controls"]))

    def test_all_mutations_are_rejected_zero_credit(self) -> None:
        mutations = load(X2 / "mutation-results.json")
        self.assertEqual(mutations["executed"], 300)
        self.assertEqual(mutations["rejected"], 300)
        self.assertEqual(Counter(row["mutation_type"] for row in mutations["mutations"]), Counter({
            "missing_required_field": 60,
            "lifecycle_inversion": 60,
            "stale_provenance_digest": 60,
            "evidence_status_promotion": 60,
            "authority_promotion": 60,
        }))
        self.assertTrue(all(row["credit"] == "rejected_zero_credit" for row in mutations["mutations"]))

    def test_four_outcomes_only(self) -> None:
        self.assertEqual(self.evidence["outcome_counts"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual({row["outcome"] for row in self.evidence["outcomes"]}, {"completed", "represented", "open_gap", "exact_gate"})

    def test_tool_library_loan_board_is_wholly_synthetic(self) -> None:
        board = load(X2 / "tool-library-loan-record-board.json")
        self.assertEqual(board["real_rows"], 0)
        self.assertEqual(board["external_actions"], 0)
        self.assertFalse(board["authority_conferred"])
        self.assertEqual(board["invalid_rejected"], 5)
        self.assertTrue(all(row["reasons"] for row in board["invalid_controls"]))
        self.assertEqual(board["record"]["safety_determination"], "not_performed")

    def test_schema_is_closed_and_zero_row(self) -> None:
        schema = load(X2 / "tool-library-loan-record-schema.json")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["real_rows"]["const"], 0)
        self.assertEqual(schema["properties"]["synthetic"]["const"], True)
        self.assertEqual(schema["properties"]["authority_state"]["const"], "exact_gate")

    def test_portfolio_results(self) -> None:
        self.assertEqual(len(self.portfolio["safe_now"]), 120)
        self.assertEqual(len(self.portfolio["owner_candidates"]), 80)
        self.assertEqual(len(self.portfolio["owner_clean_fix_refine"]), 100)
        self.assertEqual(len(self.portfolio["exact_approval"]), 20)
        self.assertEqual(len(self.portfolio["blocked"]), 10)
        self.assertTrue(all(row["state"] == "bounded_owner_local_completed" for row in self.portfolio["safe_now"] + self.portfolio["owner_clean_fix_refine"]))
        self.assertTrue(all(row["state"] == "bounded_fixture_completed" for row in self.portfolio["owner_candidates"]))

    def test_protected_packets_remain_held(self) -> None:
        self.assertTrue(all(row["state"] == "held_unexecuted" for row in self.portfolio["exact_approval"] + self.portfolio["blocked"]))
        self.assertEqual(self.portfolio["successor_records_executed"], 0)

    def test_content_addressed_flashcards(self) -> None:
        deck = load(X2 / "freed-id-flashcards.json")
        self.assertEqual(deck["card_count"], 80)
        self.assertEqual(len({row["content_address"] for row in deck["cards"]}), 80)
        self.assertEqual(Counter(row["tier"] for row in deck["cards"]), Counter({"proposal": 60, "boundary": 13, "pillar": 3, "practice": 3, "owner": 1}))

    def test_twenty_owner_local_skills(self) -> None:
        material = load(X2 / "materialization-receipt.json")
        self.assertEqual(len(material["generated_skill_paths"]), 40)
        skill_files = [path for path in material["generated_skill_paths"] if path.endswith("SKILL.md")]
        self.assertEqual(len(skill_files), 20)
        self.assertTrue(all((ROOT / path).is_file() for path in material["generated_skill_paths"]))
        self.assertFalse(material["shared_or_global_skill_installation"])

    def test_skill_validation_once(self) -> None:
        receipt = load(X2 / "skill-validation-receipts.json")
        self.assertEqual(receipt["passed"], 20)
        self.assertFalse(receipt["global_installation"])
        self.assertFalse(receipt["validator_replayed_after_success"])
        self.assertTrue(all(row["returncode"] == 0 and row["validator_invocations"] == 1 for row in receipt["receipts"]))

    def test_ten_family_current_runners_smoked_once(self) -> None:
        material = load(X2 / "materialization-receipt.json")
        receipt = load(X2 / "runner-smoke-receipts.json")
        self.assertEqual(len(material["generated_runner_paths"]), 10)
        self.assertEqual(receipt["passed"], 10)
        self.assertEqual(receipt["external_actions"], 0)
        self.assertFalse(receipt["replayed_after_success"])
        self.assertTrue(all(row["returncode"] == 0 and row["smoke_invocations"] == 1 for row in receipt["receipts"]))

    def test_no_irrelevant_tool_install(self) -> None:
        receipt = load(X2 / "tool-use-boundary.json")
        self.assertEqual(receipt["new_packages_installed"], 0)
        self.assertFalse(receipt["global_or_shared_prefix_mutated"])
        self.assertEqual(receipt["tool_novelty_credit"], 0)

    def test_source_use_has_no_data_or_authority(self) -> None:
        receipt = load(X2 / "official-source-use-receipt.json")
        self.assertEqual(receipt["network_source_checks"], 11)
        self.assertEqual(receipt["network_data_queries"], 0)
        self.assertEqual(receipt["real_rows"], 0)
        self.assertFalse(receipt["authority_conferred"])

    def test_accessibility_claim_is_reserved(self) -> None:
        audit = load(X2 / "accessibility-structural-audit.json")
        self.assertFalse(audit["wcag_conformance_claimed"])
        self.assertEqual(audit["assistive_technology_evaluation"], "reserved")
        self.assertEqual(audit["affected_user_evaluation"], "reserved")

    def test_cross_pillar_boundaries(self) -> None:
        gmut = load(X2 / "gmut-formal-board.json")
        thos = load(X2 / "thos-proxy-board.json")
        freed = load(X2 / "freed-id-profile.json")
        cbr = load(X2 / "cbr-authority-matrix.json")
        self.assertTrue(gmut["analogy_only"])
        self.assertFalse(gmut["theory_of_everything"])
        self.assertEqual(gmut["empirical_rows"], 0)
        self.assertEqual(thos["external_operations"], 0)
        self.assertFalse(freed["production"])
        self.assertEqual(cbr["decisions_made"], 0)

    def test_method_flow_formula(self) -> None:
        flow = load(X2 / "method-flow-ledger.json")
        failures = load(X2 / "operational-failures.json")["failures"]
        n = len(failures)
        self.assertFalse(flow["failure_erasure"])
        self.assertFalse(flow["independent_reproduction_claimed"])
        self.assertEqual(flow["counts"]["effective_negatives"], 54520 + n)
        self.assertEqual(flow["counts"]["failed_witnesses"], 26181 + n)
        self.assertEqual(flow["counts"]["effective_methods"], 62907 + n)
        self.assertEqual(flow["counts"]["bounded_passing_witnesses"], 44729 + n)
        self.assertEqual(flow["counts"]["open_gaps"], 482)
        self.assertEqual(flow["counts"]["exact_gates"], 473)

    def test_retained_negative_register(self) -> None:
        retained = load(X2 / "retained-negative-register.json")
        self.assertFalse(retained["failure_erasure"])
        self.assertEqual(retained["retained_mutations"], 300)
        self.assertEqual(retained["startup_failures"], 4)
        self.assertEqual(retained["x1_postcommit_failures"], 0)

    def test_accessible_report_structure(self) -> None:
        report = (X2 / "accessible-report.html").read_text(encoding="utf-8")
        self.assertIn('<main id="main">', report)
        self.assertIn('<caption>Sixty proposal outcomes</caption>', report)
        self.assertIn('scope="col"', report)
        self.assertIn("NOT_READY_FOR_STAGE_20", report)

    def test_x2_manifest_replays(self) -> None:
        manifest = load(VALIDATION / "x2-index-manifest.json")
        self.assertGreaterEqual(manifest["entry_count"], 75)
        self.assertEqual(len(manifest["declared_self_exclusions"]), 3)
        for row in manifest["entries"]:
            data = normalized(ROOT / row["path"])
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_x2_privacy_and_staged_review(self) -> None:
        privacy = load(VALIDATION / "x2-privacy-scan.json")
        staged = load(VALIDATION / "x2-staged-review.json")
        self.assertEqual(privacy["confirmed_hits"], [])
        self.assertEqual(staged["lifecycle"], "x2_evidence")
        self.assertEqual(staged["path_count"], privacy["scanned_files"] + 3)

    def test_terminal_truth(self) -> None:
        truth = load(X2 / "phase-truth.json")
        self.assertEqual(truth["declared_chain"], 10070)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})


if __name__ == "__main__":
    unittest.main()

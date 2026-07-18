from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v648_v3_2_definitions as d  # noqa: E402
from ghc_family_v648_v3_2_runtime import SURFACES, validate  # noqa: E402


PHASE = ROOT / "docs/eiren-kestrel/v648-v3-2"
X1 = "723753e1a88427e1f8cd6ee572e3479c721dce84"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V648V3RepeatEvidenceTests(unittest.TestCase):
    def test_source_x1_ancestry_and_zero_merges(self) -> None:
        for anchor in (d.SOURCE_COMMIT, X1):
            subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", anchor, "HEAD"], check=True)
        self.assertEqual(subprocess.check_output(["git", "-C", str(ROOT), "rev-list", "--count", "--merges", f"{d.SOURCE_COMMIT}..HEAD"], text=True).strip(), "0")

    def test_x1_commit_remains_x1_only(self) -> None:
        truth = json.loads(subprocess.check_output(["git", "-C", str(ROOT), "show", f"{X1}:docs/eiren-kestrel/v648-v3-2/phase-truth.json"], text=True, encoding="utf-8"))
        self.assertFalse(truth["x2_started"])
        probe = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{X1}:docs/eiren-kestrel/v648-v3-2/x2-proposal-ledger.json"], capture_output=True)
        self.assertNotEqual(probe.returncode, 0)

    def test_outcomes_are_exact_6_2_1_1(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["outcome_counts"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(set(ledger["outcome_counts"]), set(d.OUTCOME_CLASSES))

    def test_all_ten_positive_contracts_validate(self) -> None:
        for proposal_id, row in SURFACES.items():
            contract = load(row["path"])
            self.assertEqual(validate(proposal_id, contract), [], proposal_id)
            self.assertTrue(contract["valid_fixture_passed"])

    def test_all_seventy_mutations_are_rejected(self) -> None:
        total = 0
        for row in SURFACES.values():
            path = Path(row["path"]).with_name(Path(row["path"]).stem + "-mutations.json")
            payload = load(path.as_posix())
            total += payload["count"]
            self.assertTrue(payload["all_rejected"])
            self.assertTrue(all(item["rejected"] and item["issue_classes"] for item in payload["mutations"]))
        self.assertEqual(total, 70)

    def test_runner_ledger_is_complete_and_used(self) -> None:
        ledger = load("tooling/x2-runner-ledger.json")
        self.assertEqual((ledger["runner_count"], ledger["invoked_count"]), (10, 10))
        self.assertEqual({row["name"] for row in ledger["runners"]}, set(d.RUNNER_IDEAS))
        self.assertEqual(sum(row["rejected_mutations"] for row in ledger["runners"]), 70)

    def test_skill_pack_is_complete_validated_and_used(self) -> None:
        ledger = load("tooling/x2-skill-ledger.json")
        self.assertEqual(ledger["skill_count"], 20)
        self.assertTrue(ledger["all_initialized"])
        self.assertTrue(ledger["all_structure_valid"])
        self.assertTrue(ledger["all_used"])
        self.assertTrue(ledger["global_reflection_remaster_valid"])

    def test_reflection_remaster_is_non_destructive(self) -> None:
        issues = load("reflection-remaster/reflection-remaster-issues.json")
        methods = load("reflection-remaster/reflection-remaster-methods.json")
        self.assertEqual((issues["issue_count"], methods["method_count"]), (54, 54))
        self.assertTrue(methods["all_unpromoted"])
        self.assertNotIn("delete", issues["disposition_counts"])

    def test_safe_and_candidate_portfolios_are_complete(self) -> None:
        safe = load("approval-packets/x2-safe-now-ledger.json")
        candidate = load("prototypes/x2-candidate-ledger.json")
        self.assertEqual((safe["completed_count"], candidate["completed_count"]), (15, 20))
        self.assertEqual(len(list((PHASE / "prototypes/candidates").glob("*.json"))), 20)

    def test_cleanup_reserves_only_terminal_checks(self) -> None:
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((cleanup["count"], cleanup["completed_count"], cleanup["pending_final_count"]), (30, 28, 2))
        self.assertTrue(all(not row["destructive"] and not row["identity_or_memory_downgrade"] for row in cleanup["tasks"]))

    def test_negative_arithmetic_and_non_erasure(self) -> None:
        negative = load("retained-negative-register-x2.json")
        self.assertEqual(negative["effective_total"], 4211)
        self.assertEqual(negative["effective_total"], negative["inherited_effective"] + negative["x1_operational"] + negative["x2_operational"] + negative["synthetic_rejected"])
        self.assertEqual(negative["erased_negative_count"], 0)

    def test_method_flow_retains_recurrence(self) -> None:
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 12)
        self.assertEqual(ledger["counts"]["states"]["preferred"], 12)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 13, "pass": 13})
        method = next(row for row in ledger["methods"] if row["method_id"] == "V6483R2-M02")
        self.assertIn("V6483R2-M02-WFAIL-X2-01", method["validation_witness_ids"])

    def test_open_and_exact_gates_only_increase(self) -> None:
        gates = load("exact-open-gate-register-x2.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (29, 30))
        self.assertEqual(gates["closed_without_exact_evidence"], 0)

    def test_truth_stays_zero_and_not_ready(self) -> None:
        truth = load("phase-truth-x2.json")
        self.assertEqual((truth["real_data_rows"], truth["real_people_or_operations"], truth["real_keys_or_tokens"], truth["authority_decisions"]), (0, 0, 0, 0))
        self.assertEqual((truth["replay_runs"], truth["repeatability_credit"]), (0, 0))
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_threat_model_defers_host_and_cross_platform_work(self) -> None:
        model = load("threat-model.json")
        self.assertEqual(model["sandbox_and_hyper_v"], "deferred_by_user_no_probe_or_activation")
        self.assertEqual(model["cross_platform_chatgpt_messaging"], "deferred_by_user_no_send_attempt")

    def test_overview_is_three_page_equivalent_and_capped(self) -> None:
        text = (PHASE / "deliverables/v648-v3-r2-integrated-overview.md").read_text(encoding="utf-8")
        words = re.findall(r"\b\w+\b", text, re.UNICODE)
        self.assertGreaterEqual(len(words), 1200)
        self.assertLessEqual(len(words), 6000)

    def test_static_report_has_accessible_structure_and_reservation(self) -> None:
        text = (PHASE / "deliverables/v648-v3-r2-static-report.html").read_text(encoding="utf-8").casefold()
        for token in ("<html lang=", "<header>", "<main>", "<footer>", "manual and affected-user evaluation remain reserved"):
            self.assertIn(token, text)

    def test_every_phase_document_is_under_cap(self) -> None:
        for path in PHASE.rglob("*"):
            if path.is_file() and path.suffix.casefold() in {".md", ".html", ".txt"}:
                words = re.findall(r"\b\w+\b", path.read_text(encoding="utf-8"), re.UNICODE)
                self.assertLessEqual(len(words), 6000, path.relative_to(PHASE).as_posix())

    def test_route_remains_prepared_not_sent(self) -> None:
        truth = load("phase-truth-x2.json")
        self.assertEqual(truth["route_state"], "PREPARED_NOT_SENT")
        self.assertIsNone(truth["evidence_commit"])


if __name__ == "__main__":
    unittest.main()

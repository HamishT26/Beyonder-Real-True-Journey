"""Combined closeout contract tests for Sable Rook v651-v1."""

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sable-rook/v651-v1"
SOURCE = "b8d2d25747fcda747f77e6cf788a87e95062de00"
X1 = "1deba4184dfb6d017dff04b11e526a6e3730edb3"
EVIDENCE = "79d6d3675763eb553dc43b64f0e83915c1739655"
CLOSEOUT = "f6c8cd16327ef3c8f474ab94200095ec3620de3a"


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def status_paths():
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=REPO)
    return {row[3:].replace("\\", "/") for row in raw.decode("utf-8").split("\0") if len(row) > 3}


def changed_with_status(base):
    committed = set(filter(None, git("diff", "--name-only", f"{base}..HEAD").splitlines()))
    return committed | status_paths()


class TestV651V1Closeout(unittest.TestCase):
    def test_final_truth_and_distribution(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(truth["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(truth["full_repository_suite_run"])
        self.assertFalse(truth["independent_reproduction_claimed"])

    def test_negative_and_gate_retention(self):
        negatives = load("final/retained-negative-register.json")
        gates = load("final/gate-register.json")
        self.assertEqual(negatives["effective"], 6563)
        self.assertEqual((negatives["x1_operational_count"], negatives["x2_operational_count"], negatives["executed_rejected_synthetic"]), (5, 15, 100))
        self.assertEqual(len(negatives["owner_operational_entries"]), 20)
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (51, 52))
        self.assertEqual(gates["silently_closed"], 0)

    def test_outcomes_and_portfolios(self):
        outcomes = load("outcomes/outcome-ledger.json")
        portfolio = load("portfolios/expanded-portfolio-execution.json")
        self.assertEqual(len(outcomes["outcomes"]), 20)
        self.assertEqual(portfolio["completed_counts"], {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40})
        self.assertFalse(portfolio["unsafe_work_manufactured"])
        self.assertFalse(portfolio["inherited_completion_credit"])

    def test_method_flow_and_environment(self):
        methods = load("method-flow/method-flow-state.json")["counts"]
        environment = load("final/environment-receipt.json")
        self.assertEqual(methods["methods"], 16)
        self.assertEqual(methods["witness_results"], {"fail": 20, "pass": 18})
        self.assertEqual(methods["states"]["preferred"], 16)
        self.assertTrue(all(value is False for value in environment["actions"].values()))
        self.assertFalse(environment["windows_sandbox_executable_present"])

    def test_owner_and_delta_manifest_coverage(self):
        owner = load("validation/final-owner-manifest.json")
        delta = load("validation/final-delta-manifest.json")
        owner_declared = {row["path"] for row in owner["entries"]} | set(owner["self_exclusions"])
        delta_declared = {row["path"] for row in delta["entries"]} | set(delta["self_exclusions"])
        self.assertEqual(owner_declared, changed_with_status(SOURCE))
        self.assertEqual(delta_declared, changed_with_status(EVIDENCE))
        self.assertEqual(owner["entry_count"], len(owner["entries"]))
        self.assertEqual(delta["entry_count"], len(delta["entries"]))

    def test_closeout_staged_manifest_and_privacy(self):
        manifest = load("validation/closeout-staged-manifest.json")
        declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
        observed = set(filter(None, git("diff", "--name-only", f"{EVIDENCE}..{CLOSEOUT}").splitlines()))
        self.assertEqual(declared, observed)
        for row in manifest["entries"]:
            blob = subprocess.check_output(["git", "show", f"{CLOSEOUT}:{row['path']}"], cwd=REPO)
            self.assertEqual((len(blob), hashlib.sha256(blob).hexdigest()), (row["bytes"], row["sha256"]))
        for relative in ("validation/closeout-staged-privacy.json", "validation/final-owner-privacy.json", "validation/final-delta-privacy.json"):
            self.assertEqual(load(relative)["confirmed_hit_count"], 0)

    def test_documents_and_accessible_report(self):
        overview = (ROOT / "deliverables/final-integrated-overview.md").read_text(encoding="utf-8")
        baton = (ROOT / "handoffs/orin-thale-v651-v2-activation.md").read_text(encoding="utf-8")
        report = (ROOT / "deliverables/final-static-report.html").read_text(encoding="utf-8")
        overview_words = len(re.findall(r"\b\w+\b", overview, flags=re.UNICODE))
        baton_words = len(re.findall(r"\b\w+\b", baton, flags=re.UNICODE))
        self.assertGreaterEqual(overview_words, 1500)
        self.assertLessEqual(overview_words, 6000)
        self.assertGreaterEqual(baton_words, 8000)
        self.assertLessEqual(baton_words, 20000)
        self.assertIn("Skip to content", report)
        self.assertIn("affected-user evaluation remain reserved", report)

    def test_route_and_immutability(self):
        route = load("route/final-phase-state.json")
        self.assertEqual(route["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        frozen_proposals = git("show", f"{X1}:docs/sable-rook/v651-v1/preregistration/proposals.json")
        current_proposals = (ROOT / "preregistration/proposals.json").read_text(encoding="utf-8").rstrip("\n")
        frozen_outcomes = git("show", f"{EVIDENCE}:docs/sable-rook/v651-v1/outcomes/outcome-ledger.json")
        current_outcomes = (ROOT / "outcomes/outcome-ledger.json").read_text(encoding="utf-8").rstrip("\n")
        self.assertEqual(frozen_proposals, current_proposals)
        self.assertEqual(frozen_outcomes, current_outcomes)


if __name__ == "__main__":
    unittest.main()

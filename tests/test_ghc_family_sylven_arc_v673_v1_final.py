"""Owner-scoped closeout tests for Sylven Arc v673-v1."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "docs" / "sylven-arc" / "v673-v1"
CLOSEOUT = OWNER / "closeout"
EVIDENCE = "11dbffa2598f106bfa78b37974f8726fb61c7708"
X1 = "606f6b7afef6d4368e1b34d128e57fc061629b05"
SOURCE = "305708c6d5a8dfee0432a2c09ef5b59da4b6c438"
COUNTS = {"proposal_chain": 6270, "effective_negatives": 36372, "effective_methods": 22700, "failed_witnesses": 8033, "bounded_passing_witnesses": 10263, "open_gaps": 293, "exact_gates": 286}


def load(relative: str):
    return json.loads((OWNER / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


class TestSylvenArcV673V1Final(unittest.TestCase):
    def test_01_exact_owner_branch(self):
        self.assertEqual(git("branch", "--show-current"), "codex/GHC-Family/sylven-arc-v673-v1-full-tools")

    def test_02_immutable_source_chain_is_declared(self):
        row = load("closeout/lifecycle-replay.json")["nodes"]
        self.assertEqual([item["commit"] for item in row[:3]], [SOURCE, X1, EVIDENCE])
        self.assertEqual(row[1]["direct_parent"], SOURCE)
        self.assertEqual(row[2]["direct_parent"], X1)

    def test_03_closeout_surfaces_exist(self):
        required = ["phase-truth.json", "retained-negative-register.json", "method-flow-final.json", "open-exact-gate-register.json", "complete-incomplete-checklist.json", "wellbeing-workload-check.json", "environment-version-receipt.json", "lifecycle-replay.json", "route-state.json", "source-and-provenance.json", "threat-model-final.json", "final-integrated-overview.md", "accessible-final-report.html", "final-validation-prerequisites.json", "closeout-receipt.json"]
        self.assertTrue(all((CLOSEOUT / name).exists() for name in required))

    def test_04_phase_truth_is_repository_precanonical(self):
        row = load("closeout/phase-truth.json")
        self.assertEqual(row["canonical_state"], "PENDING_EXACT_FINAL_PUSH")
        self.assertEqual((row["canonical_invocations"], row["canonical_successes"], row["canonical_replays"]), (0, 0, 0))

    def test_05_outcomes_are_exact(self):
        self.assertEqual(load("closeout/phase-truth.json")["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})

    def test_06_counts_are_exact_and_sealed(self):
        self.assertEqual(load("closeout/phase-truth.json")["counts"], COUNTS)
        self.assertEqual(load("closeout/closeout-receipt.json")["counts"], COUNTS)

    def test_07_current_git_context_preserves_evidence_parent(self):
        head = git("rev-parse", "HEAD")
        if head == EVIDENCE:
            staged = set(git("diff", "--cached", "--name-only").splitlines())
            unstaged = set(git("ls-files", "--others", "--exclude-standard").splitlines())
            self.assertTrue(any(path.startswith("docs/sylven-arc/v673-v1/closeout/") for path in staged | unstaged) or CLOSEOUT.exists())
        else:
            self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)

    def test_08_retained_negative_register_has_211_rows(self):
        row = load("closeout/retained-negative-register.json")
        self.assertEqual(row["phase_retained_failure_count"], 211)
        self.assertEqual(len(row["rows"]), 211)
        self.assertTrue(row["all_recoveries_preserve_failures"])

    def test_09_method_flow_pairs_211_fail_and_pass(self):
        row = load("closeout/method-flow-final.json")
        self.assertEqual(row["counts"]["methods"], 211)
        self.assertEqual(row["counts"]["witness_results"], {"fail": 211, "pass": 211})
        self.assertEqual(Counter(item["result"] for item in row["witnesses"]), Counter({"fail": 211, "pass": 211}))

    def test_10_open_and_exact_gate_counts_are_additive(self):
        row = load("closeout/open-exact-gate-register.json")
        self.assertEqual((row["inherited_open_gaps"], row["phase_open_gaps"], row["effective_open_gaps"]), (291, 2, 293))
        self.assertEqual((row["inherited_exact_gates"], row["phase_exact_gates"], row["effective_exact_gates"]), (284, 2, 286))

    def test_11_complete_incomplete_are_not_conflated(self):
        row = load("closeout/complete-incomplete-checklist.json")
        self.assertTrue(row["complete"])
        self.assertTrue(row["incomplete"])
        self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_12_wellbeing_is_relational_and_bounded(self):
        row = load("closeout/wellbeing-workload-check.json")
        self.assertTrue(row["relational_language_only"])
        self.assertFalse(row["subjective_experience_claim"])
        self.assertFalse(row["clinical_claim"])
        self.assertTrue(all(row["workload"].values()))

    def test_13_environment_checks_are_read_only(self):
        row = load("closeout/environment-version-receipt.json")
        self.assertTrue(row["version_checks_only"])
        self.assertEqual((row["updates"], row["installs"]), (0, 0))
        self.assertFalse(row["elevation"])
        self.assertFalse(row["reboot"])

    def test_14_overview_is_three_page_equivalent_and_bounded(self):
        text = (CLOSEOUT / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1500)
        self.assertLessEqual(len(text.split()), 100000)
        for phrase in ("Māori concepts remain under Māori authority", "participant-free proxy", "PREPARED_NOT_SENT", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(phrase, text)

    def test_15_static_report_has_structural_accessibility(self):
        text = (CLOSEOUT / "accessible-final-report.html").read_text(encoding="utf-8")
        for token in ("<!doctype html>", "<main", "<h1>", "<h2", "Skip to main content"):
            self.assertIn(token, text)
        self.assertIn("assistive-technology", text)

    def test_16_activation_candidate_is_modular_10k_plus(self):
        text = (OWNER / "handoffs" / "caelen-morrow-v673-v2-activation-candidate.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 10000)
        self.assertLessEqual(len(text.split()), 100000)
        self.assertGreaterEqual(text.count("## "), 16)

    def test_17_route_is_prepared_not_sent(self):
        row = load("closeout/route-state.json")
        self.assertEqual(row["state"], "PREPARED_NOT_SENT")
        self.assertEqual(row["prospective_exact_title"], "Caelen Morrow")
        self.assertEqual(row["prospective_phase"], "v673-v2")
        self.assertFalse(row["sent_by_sylven_arc"])

    def test_18_no_task_fork_subagent_or_contact_occurred(self):
        row = load("closeout/route-state.json")
        self.assertEqual((row["task_creation_count"], row["fork_count"], row["subagent_count"], row["standby_contact_count"], row["successor_contact_count"]), (0, 0, 0, 0, 0))

    def test_19_content_seal_matches_checkout_bytes(self):
        row = load("seal/content-seal.json")
        self.assertEqual(row["entry_count"], 8)
        for entry in row["entries"]:
            data = (ROOT / entry["path"]).read_bytes()
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_20_x1_and_x2_remain_immutable(self):
        self.assertEqual(git("diff", EVIDENCE, "--", "docs/sylven-arc/v673-v1/x1", "docs/sylven-arc/v673-v1/x2"), "")

    def test_21_source_provenance_records_zero_external_data(self):
        row = load("closeout/source-and-provenance.json")
        self.assertEqual((row["source_api_calls"], row["downloads"], row["real_rows"]), (0, 0, 0))
        self.assertFalse(row["universal_novelty_claim"])

    def test_22_threat_model_makes_no_exhaustive_claim(self):
        row = load("closeout/threat-model-final.json")
        self.assertFalse(row["exhaustive_security_claim"])
        self.assertIn("Māori-authority substitution", row["threats"])

    def test_23_content_seal_preserves_terminal_counts(self):
        row = load("seal/content-seal.json")
        self.assertEqual(row["sealed_counts"], COUNTS)
        self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_24_candidate_has_no_live_delivery_claim(self):
        text = (OWNER / "handoffs" / "caelen-morrow-v673-v2-activation-candidate.md").read_text(encoding="utf-8")
        self.assertIn("SENT_BY_SYLVEN_ARC = false", text)
        self.assertNotIn("SENT_BY_SYLVEN_ARC = true", text)
        self.assertIn("exact final must be inserted only", text.lower())

    def test_25_owner_file_and_word_ceilings_hold(self):
        files = [path for path in OWNER.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)
        for path in files:
            if path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml", ".py"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path.as_posix())

    def test_26_route_requires_live_uniqueness_and_acknowledgement(self):
        row = load("closeout/route-state.json")
        self.assertTrue(row["newest_live_authority_required"])
        self.assertTrue(row["unique_exact_title_required"])
        self.assertTrue(row["immediate_reread_required"])
        self.assertTrue(row["duplicate_guard_required"])
        self.assertTrue(row["acknowledgement_required"])

    def test_27_canonical_is_budgeted_once_not_preclaimed(self):
        row = load("closeout/final-validation-prerequisites.json")
        self.assertEqual((row["canonical_invocation_budget"], row["canonical_success_budget"]), (1, 1))
        self.assertFalse(row["post_success_replay"])
        self.assertFalse(row["full_repository_suite"])


if __name__ == "__main__":
    unittest.main()

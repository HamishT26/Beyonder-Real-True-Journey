from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v649-v6"
X1 = "d82382737868160e1b16c9302ca8a008b6f3153e"
EVIDENCE = "4e5f250f8dbe4f77fadce2dfdccfb7869f06ab30"


def load(relative):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


class TestV649V6Evidence(unittest.TestCase):
    def test_core_distribution(self):
        row = load("x2/core-outcome-ledger.json")
        self.assertEqual(row["distribution"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(row["proposal_count"], 10)

    def test_every_proposal_has_two_artifacts(self):
        for row in load("x2/core-outcome-ledger.json")["outcomes"]:
            self.assertEqual(len(row["artifact_paths"]), 2)
            self.assertTrue(all((PHASE / path).is_file() for path in row["artifact_paths"]))

    def test_all_mutations_rejected(self):
        row = load("validation/x2-synthetic-mutation-results.json")
        self.assertEqual((row["count"], row["executed_count"], row["rejected_count"]), (70, 70, 70))
        self.assertTrue(all(item["retained_negative"] for item in row["mutations"]))

    def test_epoch_reclamation_is_bounded(self):
        row = load("method-flow/epoch-reclamation-contract.json")
        checks = {item["check"] for item in row["checks"]}
        self.assertTrue({"reader_pin", "grace_period", "stalled_reader", "aba_token", "duplicate_credit"}.issubset(checks))
        self.assertIn("production_memory_safety", row["absent_or_reserved"])

    def test_elitzur_is_formal_not_empirical(self):
        row = load("gmut/elitzur-obligations.json")
        self.assertIn("observation_firewall", {item["check"] for item in row["checks"]})
        self.assertIn("empirical_confirmation", row["absent_or_reserved"])

    def test_xmm_is_zero_row_open_gap(self):
        row = load("empirical/xmm-rgs-study-contract.json")
        self.assertEqual(row["outcome"], "open_gap")
        self.assertEqual((row["downloads"], row["real_rows"], row["likelihood_evaluations"]), (0, 0, 0))

    def test_wheelset_remains_proxy(self):
        row = load("thos/wheelset-inspection-contract.json")
        self.assertEqual(row["outcome"], "represented")
        self.assertEqual((row["real_people"], row["real_wheelsets"], row["real_inspections"]), (0, 0, 0))

    def test_jwt_introspection_remains_nonproduction(self):
        row = load("freed-id/jwt-introspection-profile.json")
        self.assertEqual(row["outcome"], "represented")
        self.assertTrue({"real_keys", "accounts", "trust_governance"}.issubset(row["absent_or_reserved"]))

    def test_cbr_stays_exact_gate(self):
        row = load("cbr/wheelset-risk-gate.json")
        self.assertEqual(row["outcome"], "exact_gate")
        self.assertIn("maori_authority", row["absent_or_reserved"])
        self.assertEqual(row["stop_use_or_release_decisions"], 0)

    def test_webp_is_not_exhaustive_security(self):
        row = load("formats/webp-riff-contract.json")
        self.assertIn("resource_budget", {item["check"] for item in row["checks"]})
        self.assertIn("pixel_decoding", row["absent_or_reserved"])
        self.assertIn("exhaustive_security", row["absent_or_reserved"])

    def test_focus_audit_reserves_manual_evaluation(self):
        row = load("accessibility/focus-not-obscured-contract.json")
        self.assertFalse(row["complete_accessibility"])
        self.assertFalse(row["affected_user_evaluation"])
        self.assertFalse(row["responsive_layout_evaluation"])

    def test_tolman_rejects_psyche_conversion(self):
        row = load("thermo-psyche/tolman-ehrenfest-contract.json")
        self.assertIn("agency_nonconversion", {item["check"] for item in row["checks"]})
        self.assertIn("consciousness", row["absent_or_reserved"])

    def test_manski_does_not_promote(self):
        row = load("stage20/manski-bounds-contract.json")
        self.assertEqual(row["participants"], 0)
        self.assertFalse(row["stage20_ready"])

    def test_expanded_portfolios(self):
        self.assertEqual(load("approval-packets/x2-safe-now-results.json")["completed_count"], 30)
        self.assertEqual(load("prototypes/x2-candidate-results.json")["completed_count"], 20)
        self.assertEqual(load("maintenance/x2-clean-refine-results.json")["completed_count"], 30)

    def test_skills_are_phase_local_and_used(self):
        row = load("x2/skill-use-ledger-final.json")
        self.assertEqual((row["skill_count"], row["completed_count"], row["pending_count"]), (20, 20, 0))
        self.assertFalse(row["global_installation"])
        self.assertFalse(row["subagent_forward_test"])

    def test_runners_have_one_terminal_pending(self):
        row = load("x2/runner-use-ledger.json")
        self.assertEqual((row["runner_count"], row["completed_count"], row["pending_closeout_count"]), (10, 9, 1))

    def test_negatives_preserved(self):
        row = load("x2/retained-negative-register.json")
        self.assertEqual(row["effective_at_evidence"], 5197)
        self.assertEqual((row["inherited_effective"], row["x1_operational"], row["synthetic_executed_rejected"], row["x2_operational"]), (5109, 8, 70, 10))
        self.assertFalse(row["negative_erased"])

    def test_gates_preserved(self):
        row = load("x2/gate-register.json")
        self.assertEqual((row["effective_open_gaps"], row["effective_exact_gates"]), (40, 41))
        self.assertEqual(row["silently_closed"], 0)

    def test_method_flow_parity(self):
        row = load("method-flow/method-flow-ledger.json")
        self.assertEqual((len(row["methods"]), len(row["witnesses"])), (26, 44))
        self.assertEqual(sum(item["result"] == "fail" for item in row["witnesses"]), 18)
        self.assertEqual(sum(item["result"] == "pass" for item in row["witnesses"]), 26)

    def test_x1_commit_is_ancestral_and_immutable(self):
        self.assertEqual(git("merge-base", "--is-ancestor", X1, "HEAD"), "")
        manifest = load("validation/x1-staged-manifest.json")
        self.assertEqual(len(manifest["self_exclusions"]), 3)

    def test_evidence_manifest_matches_evidence_commit(self):
        manifest = load("validation/evidence-staged-manifest.json")
        self.assertGreater(manifest["entry_count"], 100)
        for entry in manifest["entries"]:
            self.assertEqual(git("rev-parse", f"{EVIDENCE}:{entry['path']}"), entry["git_blob"], entry["path"])

    def test_overview_is_three_page_equivalent(self):
        words = len((PHASE / "integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1200)
        self.assertLessEqual(words, 6000)

    def test_accessible_report_structure(self):
        text = (PHASE / "accessible-report.html").read_text(encoding="utf-8")
        self.assertTrue(all(token in text for token in ["<main", "<nav", "<table", "<caption", 'scope="col"', 'scope="row"', ":focus", "scroll-margin-top", "Skip to evidence", "NOT_READY_FOR_STAGE_20"]))

    def test_threat_model_nonexhaustive(self):
        row = load("threat-model.json")
        self.assertFalse(row["exhaustive"])
        self.assertGreaterEqual(len(row["threats"]), 10)

    def test_handoff_is_prepared_and_sanitized(self):
        text = (PHASE / "handoffs/eiren-kestrel-v649-v7-activation.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1200)
        self.assertIn("PREPARED_NOT_SENT", text)
        self.assertNotRegex(text, r"(?i)(source_thread_id|thread_id)\s*[:=]")

    def test_no_platform_or_task_action(self):
        row = load("orchestration/final-phase-state.json")
        env = load("environment/x2-version-receipt.json")
        self.assertEqual((row["subagents"], row["tasks_created"], row["cross_platform_messages"]), (0, 0, 0))
        self.assertFalse(env["sandbox_or_hyperv_action"])

    def test_source_statuses_remain_distinct(self):
        row = load("sources/source-ledger.json")
        self.assertEqual(set(row["status_counts"]), {"current", "stable", "draft", "watch"})
        self.assertTrue(all(source["not_observation"] for source in row["sources"]))

    def test_document_caps(self):
        for path in PHASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 6000, path)


if __name__ == "__main__":
    unittest.main()

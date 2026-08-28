"""Owner-scoped final-candidate tests for Elowen Cairn v674-v7."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elowen-cairn" / "v674-v7"
SOURCE_FINAL = "c7412530cbb3a549ad681ae7b98c29b64e31ad4d"
X1_COMMIT = "d293bfaefa278b1d2e5bd086c25625df30dbe3e9"
EVIDENCE_COMMIT = "0c2974df83cdcf558fb63b8354016602ef9415e5"
BRANCH = "codex/GHC-Family/elowen-cairn-v674-v7-full-tools"
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
COUNTS = {
    "effective_negatives": 39648,
    "effective_methods": 27867,
    "failed_witnesses": 11309,
    "bounded_passing_witnesses": 15150,
    "open_gaps": 328,
    "exact_gates": 321,
}


def load(relative: str) -> dict:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git_text(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True
    ).stdout.decode("utf-8", errors="strict").strip()


class ElowenCairnV674V7FinalTests(unittest.TestCase):
    def test_01_exact_branch_and_direct_parent_chain(self) -> None:
        self.assertEqual(git_text("branch", "--show-current"), BRANCH)
        self.assertEqual(git_text("rev-parse", f"{X1_COMMIT}^"), SOURCE_FINAL)
        self.assertEqual(git_text("rev-parse", f"{EVIDENCE_COMMIT}^"), X1_COMMIT)
        self.assertEqual(
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", EVIDENCE_COMMIT, "HEAD"], cwd=ROOT
            ).returncode,
            0,
        )

    def test_02_evidence_manifest_replays_at_immutable_commit(self) -> None:
        manifest = json.loads(
            subprocess.run(
                [
                    "git",
                    "show",
                    f"{EVIDENCE_COMMIT}:docs/elowen-cairn/v674-v7/validation/evidence-manifest.json",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout.decode("utf-8")
        )
        self.assertEqual(manifest["entry_count"], 256)
        self.assertEqual(len(manifest["self_exclusions"]), 3)
        for entry in manifest["entries"][:12] + manifest["entries"][-12:]:
            blob = subprocess.run(
                ["git", "show", f"{EVIDENCE_COMMIT}:{entry['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])

    def test_03_final_phase_truth_has_exact_outcomes_counts_and_verdict(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["outcomes"], OUTCOMES)
        self.assertEqual(truth["proposal_chain"], 6970)
        for key, value in COUNTS.items():
            self.assertEqual(truth[key], value)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_04_retained_negative_register_is_additive(self) -> None:
        register = load("closeout/retained-negative-register.json")
        self.assertEqual(register["tamar_repository_seal"]["effective_negatives"], 39390)
        self.assertEqual(register["tamar_external_activation_overlay"]["effective_negatives"], 39391)
        self.assertEqual(register["elowen_evidence"]["effective_negatives"], 39647)
        self.assertEqual(register["elowen_final"]["effective_negatives"], 39648)
        self.assertEqual(register["phase_failed_witnesses"], 257)
        self.assertEqual(len(register["rows"]), 257)
        self.assertEqual(register["failures_rewritten_as_pass"], 0)

    def test_05_method_flow_final_preserves_every_state_and_witness(self) -> None:
        flow = load("closeout/method-flow-final.json")
        self.assertEqual(flow["counts"]["methods"], 290)
        self.assertEqual(flow["counts"]["witnesses"], 547)
        self.assertEqual(flow["counts"]["witness_results"], {"fail": 257, "pass": 290})
        self.assertEqual(flow["sealed_counts"], COUNTS)
        self.assertEqual(flow["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_06_proposal_ledger_preserves_chain_and_mutations(self) -> None:
        ledger = load("closeout/proposal-ledger-final.json")
        self.assertEqual((ledger["proposal_chain_before"], ledger["proposal_chain_after"]), (6910, 6970))
        self.assertEqual(ledger["counts"], OUTCOMES)
        self.assertEqual(len(ledger["rows"]), 60)
        self.assertEqual(ledger["mutations"], {"preregistered": 240, "executed": 240, "rejected": 240})

    def test_07_open_and_exact_gate_register_is_exact(self) -> None:
        register = load("closeout/exact-open-gate-register.json")
        self.assertEqual(register["open_gap_total"], 328)
        self.assertEqual(register["exact_gate_total"], 321)
        self.assertEqual(len(register["new_open_gaps"]), 3)
        self.assertEqual(len(register["new_exact_gates"]), 3)
        self.assertTrue(register["maori_concepts_remain_under_maori_authority"])

    def test_08_skill_runner_tool_summary_preserves_scope(self) -> None:
        summary = load("closeout/skill-runner-tool-summary.json")
        self.assertEqual(summary["skills"]["initialized"], 20)
        self.assertEqual(summary["skills"]["quick_validated"], 20)
        self.assertEqual(summary["skills"]["smoke_used"], 20)
        self.assertFalse(summary["skills"]["global_install"])
        self.assertEqual(summary["runners"], {"built": 10, "executed": 10, "passed": 10})
        self.assertEqual(summary["tools"]["built"], 3)
        self.assertEqual(summary["inherited_completion_credit"], 0)

    def test_09_complete_incomplete_checklist_keeps_reserved_work_open(self) -> None:
        checklist = load("closeout/complete-incomplete-checklist.json")
        self.assertIn("bounded synthetic x2 execution", checklist["complete"])
        self.assertIn("independent reproduction", checklist["incomplete"])
        self.assertIn("full repository suite", checklist["incomplete"])
        self.assertIn("Stage 20", checklist["incomplete"])
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_10_content_seal_has_exact_immutable_anchors(self) -> None:
        seal = load("seal/content-seal.json")
        self.assertEqual(seal["source_final"], SOURCE_FINAL)
        self.assertEqual(seal["x1_commit"], X1_COMMIT)
        self.assertEqual(seal["evidence_commit"], EVIDENCE_COMMIT)
        self.assertEqual(seal["final_commit"], "DIRECT_CHILD_OF_EVIDENCE_RESOLVES_AFTER_COMMIT")
        self.assertEqual(seal["retained_phase_failures"], 257)
        self.assertEqual(seal["failed_witnesses_erased"], 0)

    def test_11_integrated_overview_preserves_all_three_pillars(self) -> None:
        text = (OWNER_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1500)
        for token in ("GMUT Mind", "THOS Body", "Freed ID/CBR Heart", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, text)
        self.assertIn("PREPARED_NOT_SENT", text)
        self.assertNotIn("READY_FOR_STAGE_20", text.replace("NOT_READY_FOR_STAGE_20", ""))

    def test_12_identity_language_is_relational_only(self) -> None:
        text = (OWNER_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8")
        for token in ("relational working language", "not consciousness", "legal personhood", "Māori authority"):
            self.assertIn(token, text)

    def test_13_route_state_is_prepared_not_sent(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual(route["prospective_recipient_exact_title"], "Sylven Arc")
        self.assertEqual(route["prospective_phase"], "v674-v8")
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        for key in ("successor_contact_count", "task_creation_count", "fork_count", "substitute_endpoint_count", "standby_contact_count"):
            self.assertEqual(route[key], 0)

    def test_14_prepared_baton_is_sanitized_and_not_delivery(self) -> None:
        text = (OWNER_ROOT / "handoffs" / "sylven-arc-v674-v8-activation-candidate.md").read_text(encoding="utf-8")
        self.assertIn("DELIVERY_STATE = PREPARED_NOT_SENT", text)
        self.assertIn("Preparation is not delivery", text)
        self.assertNotIn("SENT_ONCE_ACKNOWLEDGED", text)
        self.assertNotRegex(text, r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b")

    def test_15_canonical_state_is_uninvoked_precommit(self) -> None:
        state = load("final/canonical-invocation-state.json")
        self.assertEqual(state["state"], "NOT_INVOKED_PRECOMMIT")
        self.assertEqual(state["invocation_count"], 0)
        self.assertEqual(state["success_count"], 0)
        self.assertEqual(state["replay_count"], 0)

    def test_16_final_prerequisites_require_clean_pushed_one_shot(self) -> None:
        prerequisites = load("final/final-validation-prerequisites.json")
        self.assertEqual(prerequisites["required_parent"], EVIDENCE_COMMIT)
        self.assertTrue(prerequisites["clean_pushed_final_required"])
        self.assertTrue(prerequisites["fresh_four_way_equality_required"])
        self.assertEqual(prerequisites["canonical_invocation_limit"], 1)
        self.assertEqual(prerequisites["canonical_success_limit"], 1)

    def test_17_full_repository_suite_is_not_run_or_claimed(self) -> None:
        truth = load("closeout/phase-truth.json")
        receipt = load("closeout/closeout-receipt.json")
        prerequisites = load("final/final-validation-prerequisites.json")
        self.assertEqual(truth["full_repository_suite"], "not_run_not_claimed")
        self.assertEqual(receipt["full_repository_suite"], "not_run_not_claimed")
        self.assertEqual(prerequisites["full_repository_suite"], "not_authorized_non_eiren")

    def test_18_closeout_receipt_preserves_three_commit_zero_merge_contract(self) -> None:
        receipt = load("closeout/closeout-receipt.json")
        self.assertEqual(receipt["phase_commits_after_final"], 3)
        self.assertEqual(receipt["merges_after_final"], 0)
        self.assertEqual(receipt["final_parent_required"], EVIDENCE_COMMIT)
        self.assertEqual(receipt["canonical_invocation_count_before_final"], 0)
        self.assertEqual(receipt["canonical_success_count_before_final"], 0)

    def test_19_final_staged_review_is_exact(self) -> None:
        review = load("validation/final-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["out_of_scope"], [])
        self.assertEqual(review["frozen_x1_or_evidence_mutations"], [])
        self.assertEqual(len(review["declared_lifecycle_self_exclusions"]), 4)

    def test_20_final_delta_manifest_has_exact_shape(self) -> None:
        manifest = load("validation/final-delta-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["hash_domain"], "normalized_lf_exact_git_blob")
        self.assertEqual(manifest["source_evidence"], EVIDENCE_COMMIT)
        self.assertEqual(len(manifest["self_exclusions"]), 4)

    def test_21_final_owner_manifest_has_exact_shape(self) -> None:
        manifest = load("validation/final-owner-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["hash_domain"], "normalized_lf_exact_git_blob")
        self.assertEqual(manifest["source_final"], SOURCE_FINAL)
        self.assertEqual(len(manifest["self_exclusions"]), 3)

    def test_22_final_validation_privacy_and_method_receipts_are_valid(self) -> None:
        validation = load("validation/final-validation-receipt.json")
        privacy = load("validation/final-staged-privacy.json")
        method = load("validation/final-method-flow-validation.json")
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["json_issues"], [])
        self.assertEqual(validation["python_compile_issues"], [])
        self.assertEqual(validation["frozen_x1_or_evidence_changes"], [])
        self.assertTrue(validation["stale_label_review_valid"])
        self.assertEqual(validation["stale_label_unexpected"], [])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(method["valid"])
        self.assertEqual(method["issue_count"], 0)

    def test_23_public_final_documents_have_no_private_payload_identifiers(self) -> None:
        patterns = [
            re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
            re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
            re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
            re.compile(r"\b(?:session_stream|private_transcript|private_conversation_dump)\b", re.I),
        ]
        for folder in ("closeout", "final", "seal", "handoffs", "orchestration"):
            for path in (OWNER_ROOT / folder).rglob("*"):
                if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".yaml", ".txt"}:
                    text = path.read_text(encoding="utf-8")
                    self.assertFalse(any(pattern.search(text) for pattern in patterns), path)

    def test_24_frozen_x1_and_x2_content_has_no_final_delta(self) -> None:
        changed = git_text(
            "diff",
            "--name-only",
            EVIDENCE_COMMIT,
            "--",
            "docs/elowen-cairn/v674-v7/x1",
            "docs/elowen-cairn/v674-v7/x2",
            "scripts/build_ghc_family_elowen_cairn_v674_v7_x1.py",
            "scripts/build_ghc_family_elowen_cairn_v674_v7_x2.py",
            "tests/test_ghc_family_elowen_cairn_v674_v7_x1.py",
            "tests/test_ghc_family_elowen_cairn_v674_v7_x2.py",
        )
        self.assertEqual(changed, "")

    def test_25_terminal_candidate_makes_no_canonical_or_delivery_claim(self) -> None:
        candidate = load("final/final-validation-candidate-record.json")
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual(candidate["final_commit"], "DIRECT_CHILD_OF_EVIDENCE_RESOLVES_AFTER_COMMIT")
        self.assertEqual(candidate["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertFalse(load("closeout/phase-truth.json")["same_owner_independent_reproduction"])


if __name__ == "__main__":
    unittest.main()

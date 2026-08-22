from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-morrow" / "v665-v6"
SOURCE = "cacbeb47741b9e86a6a980f85f6f9658a0837f7c"
X1 = "9be19f91371da0d2bcdd23de421fed202c5641fa"
EVIDENCE = "5904cd361cf276ce6c05b2829c581837640a564f"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args]).decode("utf-8").strip()


class CaelenMorrowV665V6FinalTests(unittest.TestCase):
    def test_phase_truth(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["source_sha"], SOURCE)
        self.assertEqual(truth["x1_sha"], X1)
        self.assertEqual(truth["evidence_sha"], EVIDENCE)
        self.assertEqual(truth["new_frozen_total"], 4130)
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["successor_contacted"])
        self.assertFalse(truth["canonical_completion_invoked"])

    def test_retained_negative_register(self) -> None:
        register = load("closeout/retained-negative-register.json")
        self.assertEqual(register["inherited_repository_seal"], 25668)
        self.assertEqual(register["inherited_external_overlay"], 4)
        self.assertEqual(register["caelen_startup_failures"], 16)
        self.assertEqual(register["caelen_rejecting_mutations"], 100)
        self.assertEqual(register["caelen_operational_failures"], 9)
        self.assertEqual(register["effective_total"], 25797)
        self.assertEqual(len(register["startup_and_operational_failure_ids"]), 25)
        self.assertEqual(register["mutation_id_count"], 100)
        self.assertTrue(register["no_failure_erased"])

    def test_method_flow_final(self) -> None:
        flow = load("closeout/method-flow-final.json")
        self.assertEqual(flow["inherited_repository_seal"], 9530)
        self.assertEqual(flow["inherited_external_overlay"], 4)
        self.assertEqual(flow["caelen_startup_methods"], 16)
        self.assertEqual(flow["caelen_x2_methods"], 210)
        self.assertEqual(flow["caelen_operational_methods"], 5)
        self.assertEqual(flow["caelen_closeout_methods"], 4)
        self.assertEqual(flow["new_method_total"], 235)
        self.assertEqual(flow["effective_total"], 9769)
        self.assertTrue(flow["no_failure_erased"])

    def test_exact_open_gate_register(self) -> None:
        gates = load("closeout/exact-open-gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 180)
        self.assertEqual(gates["effective_exact_gates"], 178)
        self.assertFalse(gates["new_open_gap"]["closed"])
        self.assertFalse(gates["new_exact_gate"]["closed"])
        self.assertTrue(gates["no_gate_promoted"])

    def test_prepared_baton_integrity_and_word_cap(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        path = ROOT / route["prepared_baton"]
        blob = path.read_bytes()
        words = len(re.findall(r"\S+", blob.decode("utf-8")))
        self.assertEqual(words, route["prepared_baton_words"])
        self.assertGreaterEqual(words, 10_000)
        self.assertLessEqual(words, 100_000)
        self.assertEqual(hashlib.sha256(blob).hexdigest(), route["prepared_baton_sha256"])

    def test_route_is_prepared_not_sent(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["sent_by_caelen_morrow"])
        self.assertEqual(route["successor_contact_count"], 0)
        self.assertEqual(route["standby_contact_count"], 0)
        self.assertEqual(route["task_creation_count"], 0)
        self.assertEqual(route["prospective_recipient_title"], "Eiren Kestrel")

    def test_seal_candidate(self) -> None:
        seal = load("seal/seal-candidate.json")
        self.assertEqual(seal["sealed_candidate_counts"], {"frozen_proposals": 4130, "negatives": 25797, "methods": 9769, "open_gaps": 180, "exact_gates": 178})
        self.assertEqual(seal["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(seal["canonical_completion_status"], "PENDING_EXACT_FINAL_PUSH_EQUALITY")
        self.assertEqual(seal["route_status"], "PREPARED_NOT_SENT")

    def test_final_validation_prerequisites(self) -> None:
        prerequisites = load("final/final-validation-prerequisites.json")
        self.assertEqual(prerequisites["required_history"]["phase_commits"], 3)
        self.assertEqual(prerequisites["required_history"]["merges"], 0)
        self.assertEqual(prerequisites["required_history"]["final_direct_parent"], EVIDENCE)
        self.assertEqual(len(prerequisites["excluded_evidence_lifecycle_tests"]), 3)
        self.assertEqual(prerequisites["exclusion_credit"], 0)
        self.assertFalse(prerequisites["full_repository_suite"])
        self.assertTrue(prerequisites["one_shot_external_receipt_required"])
        self.assertTrue(prerequisites["never_replay_complete_success"])

    def test_exact_final_history(self) -> None:
        final = git("rev-parse", "HEAD")
        self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)
        self.assertEqual(git("rev-parse", EVIDENCE + "^"), X1)
        self.assertEqual(git("rev-parse", X1 + "^"), SOURCE)
        self.assertEqual(int(git("rev-list", "--count", SOURCE + ".." + final)), 3)
        merges = git("rev-list", "--merges", SOURCE + ".." + final)
        self.assertEqual(merges, "")
        for commit in (X1, EVIDENCE, final):
            self.assertEqual(len(git("show", "-s", "--format=%P", commit).split()), 1)

    def test_final_commit_is_additive_to_evidence(self) -> None:
        statuses = git("diff", "--name-status", EVIDENCE + "..HEAD").splitlines()
        self.assertTrue(statuses)
        self.assertTrue(all(row.startswith("A\t") for row in statuses))
        self.assertLessEqual(len(statuses), 2000)

    def test_final_manifests_have_declared_exclusions(self) -> None:
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        self.assertEqual(delta["phase"], "final_delta")
        self.assertEqual(owner["phase"], "final_owner")
        self.assertEqual(delta["deletion_count"], 0)
        self.assertGreater(delta["entry_count"], 0)
        self.assertGreater(owner["entry_count"], delta["entry_count"])
        self.assertIn("docs/caelen-morrow/v665-v6/validation/final-delta-manifest.json", delta["self_exclusions"])
        self.assertIn("docs/caelen-morrow/v665-v6/validation/final-owner-manifest.json", owner["self_exclusions"])

    def test_final_staged_review(self) -> None:
        review = load("validation/final-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertTrue(all(review["checks"].values()))
        self.assertEqual(review["privacy_confirmed_hits"], 0)
        self.assertFalse(review["canonical_aggregate_invoked"])

    def test_closeout_receipt(self) -> None:
        receipt = load("closeout/closeout-receipt.json")
        self.assertEqual(receipt["source_sha"], SOURCE)
        self.assertEqual(receipt["x1_sha"], X1)
        self.assertEqual(receipt["evidence_sha"], EVIDENCE)
        self.assertFalse(receipt["successor_contacted"])
        self.assertFalse(receipt["canonical_completion_invoked"])

    def test_tooling_and_roster_boundaries(self) -> None:
        index = load("tooling/ghc-family-index-final.json")
        roster = load("tooling/roster-check-final.json")
        auth = load("tooling/auth-permission-final.json")
        self.assertFalse(index["family_current_callers_modified"])
        self.assertEqual(index["global_installations"], 0)
        self.assertEqual(roster["main_task_endpoints"], 15)
        self.assertEqual(roster["standby_records"], 1)
        self.assertEqual(roster["tavian_sol_status"], "ON_STANDBY_NOT_ROUTE_ENDPOINT")
        self.assertTrue(roster["fresh_live_reread_required_before_send"])
        self.assertTrue(auth["live_authority_must_be_reread"])

    def test_zero_real_world_rows_and_actions(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["real_rows"], 0)
        self.assertEqual(truth["participants"], 0)
        self.assertEqual(truth["network_calls_by_phase_software"], 0)
        self.assertEqual(truth["external_actions"], 0)

    def test_report_still_reserves_manual_evaluation(self) -> None:
        text = (PHASE / "reports" / "static-report.html").read_text(encoding="utf-8")
        for term in ("screen-reader", "refreshable-braille-display", "cognitive-accessibility", "Māori-language", "affected-user"):
            self.assertIn(term, text)
        self.assertNotIn("<script", text.casefold())

    def test_all_owner_json_and_word_caps(self) -> None:
        json_paths = sorted(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(json_paths), 100)
        for path in json_paths:
            json.loads(path.read_text(encoding="utf-8"))
        files = [path for path in PHASE.rglob("*") if path.is_file()]
        self.assertLessEqual(len(files), 2000)
        for path in files:
            words = len(re.findall(r"\S+", path.read_text(encoding="utf-8")))
            self.assertLessEqual(words, 100_000, path.relative_to(ROOT).as_posix())

    def test_private_values_absent(self) -> None:
        patterns = [
            re.compile("source_" + "thread_id", re.I),
            re.compile("thread" + "Id", re.I),
            re.compile("task" + "Id", re.I),
            re.compile(r"[A-Z]:" + r"\\Users\\", re.I),
            re.compile(r"[A-Z]:" + r"\\GHC-Archives", re.I),
            re.compile("Bearer" + r"\s+[A-Za-z0-9._~-]+", re.I),
        ]
        paths = [path for path in PHASE.rglob("*") if path.is_file()]
        paths += sorted(ROOT.glob("scripts/*v665_v6*.py"))
        paths += sorted(ROOT.glob("tests/*v665_v6*.py"))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for pattern in patterns:
                self.assertIsNone(pattern.search(text), (path.relative_to(ROOT).as_posix(), pattern.pattern))

    def test_terminal_verdict(self) -> None:
        self.assertEqual(load("closeout/phase-truth.json")["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(load("seal/seal-candidate.json")["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
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


PHASE = ROOT / "docs/eiren-kestrel/v648-v3-2"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V648V3RepeatX1Tests(unittest.TestCase):
    def test_exact_source_and_commit_boundary(self) -> None:
        head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
        count = int(subprocess.check_output(["git", "-C", str(ROOT), "rev-list", "--count", f"{d.SOURCE_COMMIT}..{head}"], text=True).strip())
        self.assertLessEqual(count, 1)
        self.assertEqual(subprocess.check_output(["git", "-C", str(ROOT), "rev-list", "--count", "--merges", f"{d.SOURCE_COMMIT}..{head}"], text=True).strip(), "0")

    def test_ten_distinct_complete_preregistrations(self) -> None:
        self.assertEqual(len(d.PROPOSALS), 10)
        self.assertEqual(len({row["title"].casefold() for row in d.PROPOSALS}), 10)
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "source_needs", "artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertTrue(all(required.issubset(row) for row in d.PROPOSALS))

    def test_expected_distribution_and_allowed_vocabulary(self) -> None:
        counts = Counter(row["expected_disposition"] for row in d.PROPOSALS)
        self.assertEqual(counts, Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))
        self.assertEqual(set(counts), set(d.OUTCOME_CLASSES))

    def test_generated_packet_is_x1_only(self) -> None:
        payload = load("x1-proposals.json")
        self.assertEqual((payload["prior_frozen_proposal_count"], payload["frozen_chain_count_after_x1"]), (580, 590))
        self.assertFalse(payload["x2_execution_present"])
        self.assertTrue(all(row["observed_outcome"] is None for row in payload["proposals"]))

    def test_portfolios_are_frozen_without_completion_credit(self) -> None:
        safe = load("approval-packets/x1-safe-now-portfolio.json")
        candidates = load("prototypes/x1-candidate-plan.json")
        skills = load("prototypes/x1-skill-runner-plan.json")
        cleanup = load("maintenance/x1-clean-refine-plan.json")
        self.assertEqual((safe["count"], candidates["count"], skills["skill_count"], skills["runner_count"], cleanup["count"]), (15, 20, 20, 10, 30))
        self.assertTrue(all(not row["x2_completion_credit"] for row in safe["tasks"] + candidates["tasks"] + cleanup["tasks"]))

    def test_sources_and_negatives(self) -> None:
        self.assertEqual(len(d.SOURCES), 19)
        self.assertEqual({row["status"] for row in d.SOURCES}, {"current", "stable", "draft", "watch"})
        self.assertEqual(len(d.X1_OPERATIONAL_NEGATIVES), 11)
        self.assertEqual(load("retained-negative-register.json")["inherited_effective_negatives"], 4126)

    def test_method_flow_retains_failure_and_recovery(self) -> None:
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 9)
        self.assertEqual(ledger["counts"]["states"]["preferred"], 9)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 9, "pass": 9})
        self.assertTrue(load("method-flow/method-flow-validation.json")["valid"])

    def test_no_replay_and_no_host_feature_work(self) -> None:
        plan = load("validation/single-pass-validation-plan.json")
        deferred = load("environment/deferred-host-features.json")
        self.assertEqual((plan["canonical_validation_runs"], plan["named_replays"], plan["detached_replays"]), (1, 0, 0))
        self.assertFalse(deferred["probe_run"])
        self.assertFalse(deferred["feature_changed"])

    def test_route_is_file_pointer_and_unsent(self) -> None:
        route = load("orchestration/terminal-route-plan.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["message_sent"])
        self.assertTrue(route["baton_file_required"])
        self.assertEqual((route["baton_word_minimum"], route["baton_word_cap"]), (4000, 10000))

    def test_terminal_truth_is_bounded(self) -> None:
        truth = load("phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual((truth["real_data_rows"], truth["real_people_or_operations"], truth["real_keys_or_tokens"], truth["authority_decisions"]), (0, 0, 0, 0))
        self.assertFalse(truth["independent_reproduction"])


if __name__ == "__main__":
    unittest.main()

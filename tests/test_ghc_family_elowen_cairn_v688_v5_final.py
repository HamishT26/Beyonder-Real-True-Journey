from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v688-v5"
FINAL = BASE / "final"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
SEAL = BASE / "seal"
HANDOFF = BASE / "handoffs" / "future-seat-13-v688-v6-activation-candidate.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class ElowenCairnV688V5FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = load(FINAL / "phase-truth.json")
        cls.flow = load(FINAL / "method-flow-final.json")
        cls.negative = load(FINAL / "retained-negative-register.json")
        cls.gaps = load(FINAL / "open-gap-register.json")
        cls.gates = load(FINAL / "exact-gate-register.json")
        cls.route = load(FINAL / "terminal-route-checklist.json")
        cls.baton = HANDOFF.read_text(encoding="utf-8")

    def test_01_exact_anchors_and_branch(self) -> None:
        self.assertEqual(self.truth["source"], "adadd367036e49cfb5c480f2aa0b598c164cac1c")
        self.assertEqual(self.truth["x1"], "a4fffe1213f944e0017a8dd81f227d98785d43d1")
        self.assertEqual(self.truth["evidence"], "1b0574be8cebf6b44107fbd1e7005d1b3dddb6ef")
        self.assertEqual(self.truth["branch"], "codex/GHC-Family/elowen-cairn-v688-v5-full-tools")

    def test_02_only_authorized_outcome_vocabulary_and_counts(self) -> None:
        self.assertEqual(
            self.truth["outcomes"],
            {"completed": 165, "represented": 26, "open_gap": 3, "exact_gate": 6},
        )
        self.assertEqual(set(self.truth["outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_03_effective_counts_are_additive(self) -> None:
        self.assertEqual(
            self.truth["effective_counts"],
            {
                "proposals": 16430,
                "negatives": 84363,
                "methods": 94015,
                "failed_witnesses": 55211,
                "passing_witnesses": 86064,
                "open_gaps": 758,
                "exact_gates": 765,
            },
        )

    def test_04_method_flow_retains_fail_and_pass_pairs(self) -> None:
        self.assertEqual(self.flow["counts"]["methods"], 70)
        self.assertEqual(self.flow["counts"]["witnesses"], 1018)
        self.assertEqual(self.flow["counts"]["witness_results"], {"fail": 509, "pass": 509})
        ids = {row["witness_id"] for row in self.flow["witnesses"]}
        for suffix in ("001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012"):
            self.assertIn(f"EC6885-FINAL-M{suffix}-FAIL", ids)
            self.assertIn(f"EC6885-FINAL-M{suffix}-PASS", ids)

    def test_05_closeout_failures_are_not_erased(self) -> None:
        self.assertEqual(self.negative["post_evidence_closeout_failure_count"], 12)
        self.assertEqual(
            {row["negative_id"] for row in self.negative["post_evidence_closeout_failures"]},
            {
                "EC6885-CL-N001",
                "EC6885-CL-N002",
                "EC6885-CL-N003",
                "EC6885-CL-N004",
                "EC6885-CL-N005",
                "EC6885-CL-N006",
                "EC6885-CL-N007",
                "EC6885-CL-N008",
                "EC6885-CL-N009",
                "EC6885-CL-N010",
                "EC6885-CL-N011",
                "EC6885-CL-N012",
            },
        )
        self.assertFalse(self.negative["failure_erasure"])
        self.assertFalse(self.negative["recovery_promotes_failure"])

    def test_06_open_gaps_and_exact_gates_remain_open(self) -> None:
        self.assertEqual(self.gaps["effective_count"], 758)
        self.assertEqual(self.gates["effective_count"], 765)
        self.assertEqual(self.gaps["silently_closed"], 0)
        self.assertEqual(self.gates["silently_closed"], 0)
        self.assertEqual(len(self.gaps["phase_new"]), 3)
        self.assertEqual(len(self.gates["phase_new"]), 6)

    def test_07_proposal_chain_and_execution_counts(self) -> None:
        self.assertEqual(self.truth["proposal_chain_before"], 16230)
        self.assertEqual(self.truth["proposal_chain_after"], 16430)
        self.assertEqual(self.truth["new_proposal_count"], 200)
        self.assertEqual(self.truth["contracts_passed"], 200)
        self.assertEqual(self.truth["altered_outputs_detected"], 200)

    def test_08_portfolio_counts_and_unexecuted_gates(self) -> None:
        self.assertEqual(self.truth["safe_tasks_passed"], 300)
        self.assertEqual(self.truth["candidate_field_injections_rejected"], 250)
        self.assertEqual(self.truth["clean_fix_refine_passed"], 300)
        self.assertEqual(self.truth["exact_packets_unexecuted"], 50)
        self.assertEqual(self.truth["blocked_packets_unexecuted"], 30)

    def test_09_package_skill_and_runner_receipts(self) -> None:
        package = load(X2 / "package-transaction.json")
        promotion = load(X2 / "promotion-receipt.json")
        self.assertEqual(package["status"], "COMPLETE")
        self.assertTrue(package["smoke_valid"])
        self.assertEqual(promotion["status"], "COMPLETE")
        self.assertEqual(promotion["skills_promoted"], 10)
        self.assertEqual(promotion["runners_promoted"], 5)

    def test_10_overview_is_three_page_equivalent_and_bounded(self) -> None:
        text = (FINAL / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1800)
        for literal in (
            "GMUT Mind",
            "THOS Body",
            "Freed ID and CBR Heart",
            "NOT_READY_FOR_STAGE_20",
            "Same-owner",
            "Maori authority",
        ):
            self.assertIn(literal, text)

    def test_11_static_report_has_accessible_structure_and_reservations(self) -> None:
        text = (FINAL / "static-report.html").read_text(encoding="utf-8")
        for literal in ('lang="en"', "<title>", "<main>", "<h1>", "<caption>", 'scope="col"'):
            self.assertIn(literal, text)
        self.assertIn("affected-user evaluation remain reserved", text)

    def test_12_baton_budget_modules_and_prepared_state(self) -> None:
        words = len(self.baton.split())
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertEqual(self.baton.count("\n## Module "), 13)
        self.assertIn("SENT_BY_ELOWEN_CAIRN = false", self.baton)
        self.assertIn("DELIVERY_STATE = PREPARED_NOT_SENT", self.baton)

    def test_13_future_owner_identity_and_route_are_not_preassigned(self) -> None:
        self.assertFalse(self.truth["future_seat_13_resolved"])
        self.assertFalse(self.route["relational_identity_preassigned"])
        self.assertEqual(self.route["designated_phase"], "v688-v6")
        self.assertEqual(self.route["creation_if_absent"]["model"], "gpt-6-astra")
        self.assertEqual(self.route["creation_if_absent"]["reasoning_effort"], "max")
        self.assertEqual(self.route["next_after_future_owner_terminal_gate"], {"exact_title": "Sylven Arc", "phase": "v688-v7"})

    def test_14_lifecycle_and_no_canonical_self_claim(self) -> None:
        lifecycle = load(FINAL / "lifecycle-replay.json")
        self.assertEqual(lifecycle["expected_phase_commits"], 3)
        self.assertEqual(lifecycle["expected_merges"], 0)
        self.assertEqual(lifecycle["final_direct_parent"], self.truth["evidence"])
        self.assertEqual(self.truth["canonical_invocations_in_repository"], 0)
        self.assertEqual(self.truth["prepared_successor_state"], "PREPARED_NOT_SENT")

    def test_15_manifests_privacy_and_content_seal_are_structured(self) -> None:
        delta = load(VALIDATION / "final-delta-manifest.json")
        owner = load(VALIDATION / "final-owner-manifest.json")
        privacy = load(VALIDATION / "final-privacy-adjudication.json")
        review = load(VALIDATION / "final-staged-review.json")
        seal = load(SEAL / "content-seal.json")
        self.assertGreater(delta["entry_count"], 0)
        self.assertGreater(owner["entry_count"], delta["entry_count"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertEqual(review["outside_owner_paths"], [])
        self.assertEqual(review["x1_or_x2_mutations"], [])
        self.assertEqual(seal["target_count"], 12)
        for entry in seal["targets"]:
            data = normalized((ROOT / entry["path"]).read_bytes())
            self.assertEqual(len(data), entry["bytes_normalized_lf"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_16_no_real_world_or_stage20_promotion(self) -> None:
        self.assertEqual(self.truth["real_people_or_records"], 0)
        self.assertEqual(self.truth["network_game_rows"], 0)
        self.assertFalse(self.truth["full_repository_suite"])
        self.assertFalse(self.truth["independent_reproduction"])
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(self.truth["successor_contacts"], 0)


if __name__ == "__main__":
    unittest.main()

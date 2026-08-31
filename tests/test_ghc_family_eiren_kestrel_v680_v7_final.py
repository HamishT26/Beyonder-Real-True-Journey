from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "eiren-kestrel" / "v680-v7"
FINAL = BASE / "final"
VALIDATION = BASE / "validation"
SOURCE = "2522f0ff596b66f57f187f8073d498c692a85712"
X1 = "e94866a1adf4b5b038479c12bc5354ead6f7c249"
EVIDENCE = "1ee1a87ff80ad3b2813a9b6cfb29b3dff38c4ba1"
BRANCH = "codex/GHC-Family/eiren-kestrel-v680-v7-full-tools"
COUNTS = {
    "bounded_passing_witnesses": 39794,
    "effective_methods": 57852,
    "effective_negatives": 52315,
    "exact_gates": 452,
    "failed_witnesses": 23976,
    "open_gaps": 461,
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


class EirenKestrelV680V7FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.phase = load(FINAL / "phase-truth.json")
        cls.method = load(FINAL / "method-flow-final.json")
        cls.delta = load(VALIDATION / "final-delta-manifest.json")
        cls.owner = load(VALIDATION / "final-owner-manifest.json")

    def test_01_exact_immutable_anchors(self) -> None:
        lifecycle = load(FINAL / "lifecycle-replay.json")
        self.assertEqual(lifecycle["source"], SOURCE)
        self.assertEqual(lifecycle["x1_head"], X1)
        self.assertEqual(lifecycle["evidence_head"], EVIDENCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)

    def test_02_precommit_or_exact_final_transition(self) -> None:
        head = git("rev-parse", "HEAD")
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        if head == EVIDENCE:
            self.assertTrue(FINAL.exists())
        else:
            self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)
            self.assertEqual(int(git("rev-list", "--count", f"{SOURCE}..HEAD")), 3)
            self.assertEqual(int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")), 0)

    def test_03_exact_outcomes_and_vocabulary(self) -> None:
        self.assertEqual(self.phase["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(set(self.phase["outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_04_exact_counts(self) -> None:
        self.assertEqual(self.phase["counts"], COUNTS)
        self.assertEqual(self.method["counts"], COUNTS)

    def test_05_failed_witnesses_are_retained(self) -> None:
        self.assertFalse(self.method["failure_erasure"])
        self.assertFalse(self.method["recoveries_retroactively_promote_failure"])
        self.assertEqual(len(self.method["startup_and_x1_failures"]), 14)
        self.assertEqual([row["failure_id"] for row in self.method["x2_operational_failures"]], ["EK6807-X2-N001", "EK6807-X2-N002", "EK6807-X2-N003"])
        self.assertEqual([row["failure_id"] for row in self.method["closeout_operational_failures"]], ["EK6807-CL-N001", "EK6807-CL-N002", "EK6807-CL-N003"])

    def test_06_open_gap_and_exact_gate_counts(self) -> None:
        self.assertEqual(load(FINAL / "open-gap-register.json")["count"], 461)
        self.assertEqual(load(FINAL / "exact-gate-register.json")["count"], 452)

    def test_07_terminal_verdict(self) -> None:
        self.assertEqual(self.phase["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_08_manifests_replay_normalized_worktree_bytes(self) -> None:
        for manifest in (self.delta, self.owner):
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            for row in manifest["entries"]:
                data = (ROOT / row["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
                self.assertEqual(len(data), row["bytes"], row["path"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_09_manifest_exclusion_arithmetic(self) -> None:
        review = load(VALIDATION / "final-staged-review.json")
        exclusions = set(review["declared_self_exclusions"])
        self.assertEqual(exclusions, set(self.delta["declared_self_exclusions"]))
        self.assertEqual(exclusions, set(self.owner["declared_self_exclusions"]))
        self.assertEqual(review["path_count"], len(review["expected_paths"]))
        self.assertEqual(len(self.delta["entries"]) + len(exclusions), review["path_count"])

    def test_10_content_seal_replays(self) -> None:
        seal = load(BASE / "closeout" / "content-seal.json")
        for row in seal["targets"]:
            data = (ROOT / row["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_11_privacy_and_security(self) -> None:
        privacy = load(VALIDATION / "final-privacy-scan.json")
        security = load(VALIDATION / "final-security-scan.json")
        self.assertEqual(len(privacy["privacy_classes"]), 5)
        self.assertEqual(privacy["confirmed_hits"], [])
        self.assertEqual(security["bounded_findings"], 0)
        self.assertEqual(security["ast_errors"], [])

    def test_12_precommit_receipt_scope(self) -> None:
        receipt = load(VALIDATION / "final-precommit-test-receipt.json")
        self.assertFalse(receipt["canonical_invocation"])
        self.assertIn(receipt["status"], {"PENDING", "PASSED"})
        self.assertIn(receipt["selected_test_count"], {0, 18})

    def test_13_canonical_contract(self) -> None:
        contract = load(FINAL / "canonical-contract.json")
        self.assertEqual(contract["maximum_attributable_invocations"], 1)
        self.assertFalse(contract["post_success_replay_permitted"])
        self.assertFalse(contract["full_repository_suite_authorized"])
        self.assertFalse(contract["complete_repository_suite_assigned"])
        self.assertFalse(contract["complete_repository_suite_run"])
        self.assertFalse(contract["same_owner_is_independent_reproduction"])

    def test_14_route_is_prepared_not_sent(self) -> None:
        text = (BASE / "handoffs" / "elaren-kestrel-v680-v8-activation-candidate.md").read_text(encoding="utf-8")
        self.assertIn("PREPARED_BY_EIREN_KESTREL = true", text)
        self.assertIn("SENT_BY_EIREN_KESTREL = false", text)
        self.assertIn("DELIVERY_STATE = PREPARED_NOT_SENT", text)
        self.assertIn("Eiren Kestrel", text)
        self.assertIn("Elaren Kestrel", text)
        self.assertIn("Neris Solane", text)

    def test_15_sources_and_same_owner_do_not_confer_authority(self) -> None:
        source = load(FINAL / "official-source-boundary.json")
        self.assertFalse(source["authority_conferred"])
        self.assertFalse(source["citations_are_observations"])
        self.assertEqual(source["real_data_rows"], 0)
        self.assertEqual(source["real_world_actions"], 0)
        self.assertFalse(self.phase["same_owner_validation_is_independent_reproduction"])

    def test_16_owner_caps_and_accessibility(self) -> None:
        review = load(VALIDATION / "final-staged-review.json")
        self.assertLess(review["path_count"], 2000)
        self.assertLess(self.owner["entry_count"], 2000)
        self.assertLessEqual(review["max_document_words"], 100000)
        overview = (FINAL / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1500)
        report = (FINAL / "static-report.html").read_text(encoding="utf-8")
        for token in ("<main id=\"main\">", "<caption>", 'scope="col"', "Skip to main content", "Manual browser evaluation: reserved"):
            self.assertIn(token, report)
        wellbeing = load(FINAL / "wellbeing-and-workload.json")
        self.assertTrue(wellbeing["user_control_preserved"])
        self.assertEqual(wellbeing["assessment_type"], "bounded_nonclinical_workload_check")

    def test_17_four_tier_flashcard_deck_remains_bound(self) -> None:
        deck = BASE / "x2" / "flashcards"
        index = load(deck / "deck-index.json")
        manifest = load(deck / "card-manifest.json")
        self.assertEqual(index["card_count"], 67)
        self.assertEqual(index["core_task_outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(load(deck / "baton-index.json")["count"], 13)

    def test_18_isolated_toolchain_remains_bounded(self) -> None:
        receipt = load(BASE / "x2" / "toolchain-install-receipt.json")
        self.assertEqual(receipt["installed_count"], 3)
        self.assertEqual(receipt["smoke_used_count"], 3)
        self.assertTrue(receipt["dependency_check_passed"])
        self.assertFalse(receipt["global_install"])
        self.assertEqual({row["name"] for row in receipt["tools"]}, {"check-jsonschema", "pyupgrade", "codespell"})


if __name__ == "__main__":
    unittest.main()

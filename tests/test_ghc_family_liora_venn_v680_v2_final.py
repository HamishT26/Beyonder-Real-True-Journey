from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "liora-venn" / "v680-v2"
FINAL = BASE / "final"
VALIDATION = BASE / "validation"
SOURCE = "9f030e7f85282ba3de7c378a8fc072c214396dcb"
X1 = "04b3248d8fc62d7f81303eec1d452d6078586db3"
EVIDENCE = "26db158bb8574ab2996ef87bae3ed8e89c2ce9e9"
BRANCH = "codex/GHC-Family/liora-venn-v680-v2-full-tools"
COUNTS = {
    "bounded_passing_witnesses": 36242,
    "effective_methods": 53999,
    "effective_negatives": 50712,
    "exact_gates": 437,
    "failed_witnesses": 22373,
    "open_gaps": 446,
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


class LioraVennV680V2FinalTests(unittest.TestCase):
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
        self.assertEqual(len(self.method["startup_and_x1_failures"]), 13)
        self.assertEqual(
            [row["failure_id"] for row in self.method["x2_operational_failures"]],
            ["LV6802-X2-N001", "LV6802-X2-N002", "LV6802-X2-N003", "LV6802-X2-N004"],
        )

    def test_06_open_gap_and_exact_gate_counts(self) -> None:
        self.assertEqual(load(FINAL / "open-gap-register.json")["count"], 446)
        self.assertEqual(load(FINAL / "exact-gate-register.json")["count"], 437)

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
        self.assertIn(receipt["selected_test_count"], {0, 16})

    def test_13_canonical_contract(self) -> None:
        contract = load(FINAL / "canonical-contract.json")
        self.assertEqual(contract["maximum_attributable_invocations"], 1)
        self.assertFalse(contract["post_success_replay_permitted"])
        self.assertFalse(contract["full_repository_suite_authorized"])
        self.assertTrue(contract["Eiren_only_full_suite"])
        self.assertFalse(contract["same_owner_is_independent_reproduction"])

    def test_14_route_is_prepared_not_sent(self) -> None:
        text = (BASE / "handoffs" / "tamar-vey-v680-v3-activation-candidate.md").read_text(encoding="utf-8")
        self.assertIn("PREPARED_BY_LIORA_VENN = true", text)
        self.assertIn("SENT_BY_LIORA_VENN = false", text)
        self.assertIn("DELIVERY_STATE = PREPARED_NOT_SENT", text)

    def test_15_sources_and_same_owner_do_not_confer_authority(self) -> None:
        source = load(FINAL / "official-source-boundary.json")
        self.assertFalse(source["authority_conferred"])
        self.assertFalse(source["citations_are_observations"])
        self.assertEqual(source["real_data_rows"], 0)
        self.assertEqual(source["real_world_actions"], 0)
        self.assertFalse(self.phase["same_owner_validation_is_independent_reproduction"])

    def test_16_owner_caps(self) -> None:
        review = load(VALIDATION / "final-staged-review.json")
        self.assertLess(review["path_count"], 2000)
        self.assertLessEqual(review["max_document_words"], 100000)


if __name__ == "__main__":
    unittest.main()

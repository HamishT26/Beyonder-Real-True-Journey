from __future__ import annotations

import hashlib
import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v687-v3"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
SOURCE = "71e94d1699eea013c82bef0b7a7e081ac6e43c8c"
X1 = "1a57a093dff78bcb217de33f9c5f282d3ee8bf17"
EVIDENCE = "f08302a468e819a0e89280333d980b8d4ac6a4f7"
BRANCH = "codex/GHC-Family/sable-rook-v687-v3-full-tools"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, encoding="utf-8", capture_output=True).stdout.strip()


def replay_manifest(commit: str, path: str) -> int:
    manifest = json.loads(git("show", f"{commit}:{path}"))
    for entry in manifest["entries"]:
        data = subprocess.run(["git", "show", f"{commit}:{entry['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if len(data) != entry["bytes_normalized_lf"] or hashlib.sha256(data).hexdigest() != entry["sha256_normalized_lf"]:
            raise AssertionError(entry["path"])
    return len(manifest["entries"])


class SableRookV687V3FinalTests(unittest.TestCase):
    def test_01_exact_lifecycle_context(self):
        head = git("rev-parse", "HEAD")
        expected = os.environ.get("SR6873_EXPECTED_FINAL")
        if expected:
            self.assertEqual(head, expected)
            self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)
        else:
            self.assertEqual(head, EVIDENCE)
        self.assertEqual(git("branch", "--show-current"), BRANCH)

    def test_02_phase_truth(self):
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(truth["state"], "FINAL_PREPARED_FOR_CANONICAL")
        self.assertEqual(truth["exact_final"], "PENDING_DIRECT_CHILD_COMMIT")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_03_outcome_counts(self):
        self.assertEqual(load(FINAL / "phase-truth.json")["outcomes"], {"completed": 160, "represented": 20, "open_gap": 10, "exact_gate": 10})

    def test_04_effective_counts(self):
        counts = load(FINAL / "phase-truth.json")["effective_counts"]
        self.assertEqual(counts, {"effective_negatives": 77893, "effective_methods": 93045, "failed_witnesses": 48741, "bounded_passing_witnesses": 77040, "open_gaps": 674, "exact_gates": 659})

    def test_05_retained_negative_layers(self):
        data = load(CLOSEOUT / "retained-negative-register.json")
        self.assertEqual(data["source_repository_negatives"], 76876)
        self.assertEqual(data["source_route_overlay"], 1)
        self.assertTrue(data["source_induction_extra_failure_unaggregated"])
        self.assertEqual(data["sable_x1_operational"], 7)
        self.assertEqual(data["sable_x2_invalid_and_adverse"], 1003)
        self.assertEqual(data["sable_x2_operational"], 1)
        self.assertEqual(data["sable_postevidence_operational"], 1)
        self.assertEqual(data["sable_final_operational"], 4)

    def test_06_gates(self):
        gates = load(CLOSEOUT / "gate-register.json")
        self.assertEqual(gates["open_gaps"], 674)
        self.assertEqual(gates["exact_gates"], 659)
        self.assertEqual(gates["silently_closed"], 0)

    def test_07_promotions(self):
        receipt = load(FINAL / "promotion-receipt.json")
        self.assertTrue(receipt["passed"])
        self.assertEqual(receipt["skill_count"], 10)
        self.assertEqual(receipt["skill_file_count"], 60)
        self.assertEqual(receipt["shared_runner_count"], 5)
        self.assertEqual(receipt["mismatches"], [])

    def test_08_deck(self):
        deck = load(FINAL / "four-tier-deck.json")
        self.assertEqual(deck["card_count"], 208)
        self.assertEqual(deck["tiers"], {"owner": 1, "pillar": 3, "practice": 4, "task": 200})

    def test_09_baton_range_modules_eof(self):
        index = load(HANDOFFS / "baton-index.json")
        self.assertGreaterEqual(index["words"], 10000)
        self.assertLessEqual(index["words"], 100000)
        self.assertEqual(len(index["modules"]), 13)
        text = (HANDOFFS / "future-seat-08-v687-v4-activation-candidate.md").read_text(encoding="utf-8")
        self.assertTrue(text.rstrip().endswith(index["eof"]))

    def test_10_baton_hash(self):
        index = load(HANDOFFS / "baton-index.json")
        data = (HANDOFFS / "future-seat-08-v687-v4-activation-candidate.md").read_bytes()
        self.assertEqual(len(data), index["bytes"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), index["sha256"])

    def test_11_overview_three_pages(self):
        words = len((FINAL / "integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1500)
        self.assertLessEqual(words, 100000)

    def test_12_accessible_report(self):
        text = (FINAL / "accessible-report.html").read_text(encoding="utf-8")
        for token in ["<title>", "<main>", "<h1>", "<caption>", 'scope="col"', 'scope="row"']:
            self.assertIn(token, text)
        self.assertIn("affected-user evaluation remain reserved", text)

    def test_13_environment(self):
        env = load(FINAL / "environment-version-receipt.json")
        self.assertTrue(env["verified_only"])
        for key in ["desktop_update_performed", "elevation", "host_security_changed", "windows_feature_changed", "sandbox_or_hyper_v_activated", "reboot"]:
            self.assertFalse(env[key])

    def test_14_wellbeing_and_identity(self):
        data = load(FINAL / "wellbeing.json")
        self.assertFalse(data["subjective_state_claimed"])
        self.assertTrue(data["corrigibility_preserved"])
        self.assertFalse(data["consciousness_or_personhood_claim"])

    def test_15_complete_incomplete(self):
        data = load(CLOSEOUT / "complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(data["complete"]), 12)
        self.assertGreaterEqual(len(data["incomplete"]), 12)

    def test_16_content_seal(self):
        seal = load(CLOSEOUT / "content-seal.json")
        self.assertEqual(seal["target_count"], 13)
        for entry in seal["targets"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_17_x1_manifest_replay(self):
        self.assertEqual(replay_manifest(X1, "docs/sable-rook/v687-v3/validation/x1-manifest.json"), 62)

    def test_18_x2_manifest_replay(self):
        self.assertEqual(replay_manifest(EVIDENCE, "docs/sable-rook/v687-v3/validation/x2-manifest.json"), 118)

    def test_19_final_delta_manifest_working(self):
        manifest = load(VALIDATION / "final-delta-manifest.json")
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_20_final_owner_manifest_working(self):
        manifest = load(VALIDATION / "final-owner-manifest.json")
        self.assertLess(manifest["owner_file_count"], 2000)
        self.assertEqual(manifest["owner_file_count"], manifest["entry_count"] + len(manifest["self_exclusions"]))
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_21_privacy(self):
        scan = load(VALIDATION / "final-privacy-scan.json")
        self.assertEqual(len(scan["pattern_classes"]), 5)
        self.assertEqual(scan["confirmed_hit_count"], 0)

    def test_22_ast_security(self):
        scan = load(VALIDATION / "final-ast-security.json")
        self.assertEqual(scan["finding_count"], 0)
        self.assertFalse(scan["exhaustive_security"])

    def test_23_all_json_parses(self):
        paths = list(BASE.rglob("*.json"))
        relative = {path.relative_to(BASE).as_posix() for path in paths}
        required = {
            "x1/new-proposals.json",
            "x2/outcome-ledger.json",
            "final/phase-truth.json",
            "closeout/content-seal.json",
            "validation/final-owner-manifest.json",
        }
        self.assertTrue(required.issubset(relative))
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_24_document_caps(self):
        for path in BASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)

    def test_25_route_held(self):
        route = load(CLOSEOUT / "route-readiness.json")
        self.assertEqual(route["state"], "PREPARED_NOT_CREATED")
        self.assertEqual(route["creation_count"], 0)
        self.assertFalse(route["identity_preassigned"])
        self.assertFalse(route["caelen_contacted"])

    def test_26_canonical_budget(self):
        data = load(CLOSEOUT / "final-validation-candidate.json")
        self.assertEqual(data["canonical_invocation_budget"], 1)
        self.assertEqual(data["canonical_successes"], 0)
        self.assertFalse(data["replay_after_success"])
        self.assertFalse(data["full_repository_suite"])

    def test_27_final_method_flow(self):
        receipt = load(FINAL / "method-flow" / "validation.json")
        ledger = load(FINAL / "method-flow" / "ledger.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(len(ledger["methods"]), 5)
        self.assertEqual(sum(row["result"] == "fail" for row in ledger["witnesses"]), 5)
        self.assertEqual(sum(row["result"] == "pass" for row in ledger["witnesses"]), 5)

    def test_28_immutable_x1_x2(self):
        changed = git("diff", "--name-only", EVIDENCE, "--", "docs/sable-rook/v687-v3/x1", "docs/sable-rook/v687-v3/x2", "docs/sable-rook/v687-v3/skills", "docs/sable-rook/v687-v3/method-flow", "docs/sable-rook/v687-v3/workflow-refinement", "docs/sable-rook/v687-v3/reflection-remaster", "docs/sable-rook/v687-v3/tooling")
        self.assertEqual(changed, "")

    def test_29_claim_boundaries(self):
        data = load(FINAL / "claim-boundaries.json")
        self.assertGreaterEqual(len(data["not_established"]), 18)
        self.assertEqual(data["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_30_source_ledger(self):
        data = load(FINAL / "source-ledger.json")
        self.assertEqual(len(data["entries"]), 10)
        self.assertFalse(data["citations_are_observations"])
        self.assertEqual(data["real_rows"], 0)

    def test_31_package_and_execution_truth(self):
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(truth["packages"]["direct"], 3)
        self.assertEqual(truth["skills"], {"built": 10, "validated": 10, "used": 10, "promoted": 10})
        self.assertEqual(truth["runners"], {"built": 10, "used": 10, "shared": 5})

    def test_32_no_route_creation_in_repo(self):
        truth = load(FINAL / "phase-truth.json")
        self.assertFalse(truth["future_seat_created"])
        self.assertFalse(truth["caelen_contacted"])

    def test_33_staged_review_shape(self):
        review = load(VALIDATION / "final-staged-review.json")
        self.assertIn(review["state"], {"PREPARED_NOT_STAGED", "PASS"})

    def test_34_ancestry_plan(self):
        plan = load(CLOSEOUT / "ancestry-plan.json")
        self.assertEqual(plan["required_parent"], EVIDENCE)
        self.assertEqual(plan["required_phase_commits"], 3)
        self.assertEqual(plan["required_merges"], 0)

    def test_35_only_four_labels(self):
        self.assertEqual(set(load(BASE / "x2" / "outcome-ledger.json")["allowed_labels"]), {"completed", "represented", "open_gap", "exact_gate"})


if __name__ == "__main__":
    unittest.main()

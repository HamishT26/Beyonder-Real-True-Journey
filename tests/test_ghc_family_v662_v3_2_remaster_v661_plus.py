"""Lifecycle checks for the additive Neris v661-plus validation-scope recovery."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = Path("docs/neris-solane/v662-v3-2-remaster")
PHASE = ROOT / PHASE_ROOT
SCOPE = PHASE / "scope-recovery"
BRANCH = "codex/GHC-Family/neris-solane-v662-v3-2-remaster"
FIRST_SOURCE = "9d35f2c60bc1d124bbc67d000e7f5a4da6d95410"
X1 = "9b61b218956031d80da66a59924713778b63f31f"
EVIDENCE = "999de05624682c19226c1bd5f57f2682468ff072"
CORRECTION = "f8e9f59b0e16cd11da5b08cd00beafe65e6d7bf6"
PRIOR_FINAL = "681c52c92a5b48f6702d0cd1db6384f76f325ffc"
OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}


def read_json(relative: str) -> dict:
    return json.loads((SCOPE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {completed.stderr[-1000:]}")
    return completed.stdout.strip()


def git_bytes(revision: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if completed.returncode:
        raise AssertionError(f"missing Git blob {revision}:{path}")
    return completed.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def git_batch_bytes(revision: str, paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    request = b"".join(f"{revision}:{path}\n".encode("utf-8") for path in paths)
    stdout, stderr = process.communicate(request, timeout=300)
    if process.returncode:
        raise AssertionError(f"git batch failed: {stderr[-1000:].decode('utf-8', 'replace')}")
    values = {}
    offset = 0
    for path in paths:
        newline = stdout.find(b"\n", offset)
        if newline < 0:
            raise AssertionError(f"missing batch header for {path}")
        header = stdout[offset:newline].split()
        if len(header) != 3 or header[1] != b"blob":
            raise AssertionError(f"unexpected batch header for {path}")
        size = int(header[2])
        start = newline + 1
        end = start + size
        if len(stdout) < end + 1 or stdout[end : end + 1] != b"\n":
            raise AssertionError(f"truncated batch blob for {path}")
        values[path] = stdout[start:end].replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        offset = end + 1
    if offset != len(stdout):
        raise AssertionError("unexpected trailing Git batch output")
    return values


def replay_manifest(revision: str, value: dict) -> list[str]:
    mismatches = []
    blobs = git_batch_bytes(revision, [entry["path"] for entry in value["entries"]])
    for entry in value["entries"]:
        payload = blobs[entry["path"]]
        if len(payload) != entry["bytes"] or hashlib.sha256(payload).hexdigest() != entry["sha256"]:
            mismatches.append(entry["path"])
    return mismatches


class TestV662V3RemasterV661Plus(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = read_json("governance/v661-plus-validation-scope.json")
        cls.overlay = read_json("truth/broad-canonical-redirect-overlay.json")
        cls.truth = read_json("truth/scoped-final-truth.json")
        cls.flow = read_json("method-flow/method-flow-state-v661-plus.json")
        cls.inventory = read_json("validation/scoped-inventory-snapshot.json")
        cls.selection = read_json("validation/scoped-selection-contract.json")
        cls.owner_manifest = read_json("validation/scoped-owner-manifest.json")
        cls.delta_manifest = read_json("validation/scoped-delta-manifest.json")
        cls.privacy = read_json("validation/scoped-privacy-scan.json")
        cls.document = read_json("validation/scoped-document-cap.json")
        cls.staged = read_json("validation/scoped-staged-review.json")
        cls.validation = read_json("validation/scoped-validation.json")
        cls.method_validation = read_json("validation/scoped-method-flow-skill-validation.json")
        cls.route = read_json("routing/route-state-v661-plus.json")

    def test_01_additive_history_is_exact_and_merge_free(self) -> None:
        head = git("rev-parse", "HEAD")
        self.assertEqual(git("rev-parse", "--abbrev-ref", "HEAD"), BRANCH)
        self.assertEqual(git("rev-parse", "HEAD^"), PRIOR_FINAL)
        self.assertEqual(
            git("rev-list", "--first-parent", f"{FIRST_SOURCE}..HEAD").splitlines(),
            [head, PRIOR_FINAL, CORRECTION, EVIDENCE, X1],
        )
        self.assertEqual(git("rev-list", "--merges", f"{FIRST_SOURCE}..HEAD"), "")

    def test_02_prior_exact_final_manifest_remains_immutable(self) -> None:
        manifest_path = f"{PHASE_ROOT.as_posix()}/validation/final-owner-manifest.json"
        value = json.loads(git_bytes(PRIOR_FINAL, manifest_path).decode("utf-8"))
        self.assertEqual(value["entry_count"], 242)
        self.assertEqual(replay_manifest(PRIOR_FINAL, value), [])

    def test_03_live_scope_is_v661_plus_only(self) -> None:
        self.assertEqual(self.policy["state"], "LIVE_USER_AUTHORIZED_V661_PLUS_ONLY")
        self.assertEqual(self.policy["phase_floor"], "v661-v1")
        self.assertEqual(self.policy["numeric_phase_floor"], 661)
        self.assertEqual(self.policy["applies_to_active_main_tasks"], 15)
        self.assertTrue(self.policy["standby_unchanged"])
        self.assertTrue(self.policy["historical_evidence_retained"])
        self.assertEqual(len(self.policy["global_skills_used"]), 6)

    def test_04_inventory_selects_only_parsed_v661_plus_family_modules(self) -> None:
        selected = set(self.inventory["selected_test_files"])
        older = set(self.inventory["below_floor_test_files"])
        unversioned = set(self.inventory["unversioned_test_files"])
        self.assertEqual(self.inventory["phase_floor"], 661)
        self.assertEqual(self.inventory["selected_file_count"], self.inventory["module_count"])
        self.assertEqual(self.inventory["test_count"], self.inventory["unique_test_count"])
        self.assertGreaterEqual(self.inventory["selected_file_count"], 37)
        self.assertGreaterEqual(self.inventory["below_floor_file_count"], 468)
        self.assertGreaterEqual(self.inventory["unversioned_file_count"], 2)
        self.assertTrue(all(value >= 661 for value in self.inventory["selected_versions"].values()))
        self.assertFalse(selected & older)
        self.assertFalse(selected & unversioned)
        self.assertEqual(self.inventory["loader_errors"], [])
        self.assertEqual(self.inventory["duplicate_ids"], 0)
        self.assertEqual(self.inventory["test_bodies_run"], 0)

    def test_05_selection_contract_matches_frozen_inventory(self) -> None:
        self.assertEqual(self.selection["phase_floor"], 661)
        self.assertEqual(self.selection["selected_files"], self.inventory["selected_test_files"])
        self.assertEqual(self.selection["selected_file_count"], self.inventory["selected_file_count"])
        self.assertEqual(self.selection["selected_test_count"], self.inventory["test_count"])
        self.assertFalse(self.selection["replay_after_success"])
        self.assertTrue(self.selection["whole_repository_structural_gates_retained"])

    def test_06_interrupted_broad_attempt_is_retained_at_zero_credit(self) -> None:
        self.assertEqual(self.overlay["failure_count"], 14)
        self.assertEqual(self.overlay["broad_worker_failure_count"], 7)
        self.assertEqual(self.overlay["canonical_success_count"], 0)
        self.assertTrue(self.overlay["all_zero_success_credit"])
        self.assertFalse(self.overlay["replay"])
        self.assertTrue(self.overlay["receipt"]["valid"])
        self.assertEqual(
            self.overlay["receipt"]["sha256"],
            "5f4f90ff5a3ea6b94f9cd208c203b0b9741881c7f6b9b4ab3a9f3238c1cff932",
        )
        identities = [row["negative_id"] for row in self.overlay["rows"]]
        self.assertEqual(len(identities), len(set(identities)))

    def test_07_scoped_truth_preserves_labels_counts_and_terminal_boundary(self) -> None:
        self.assertEqual(self.truth["frozen_proposals"], 3530)
        self.assertEqual(self.truth["outcomes"], OUTCOMES)
        self.assertEqual(self.truth["effective_negatives"], 23058)
        self.assertEqual(self.truth["effective_methods"], 7652)
        self.assertEqual(self.truth["open_gaps"], 150)
        self.assertEqual(self.truth["exact_gates"], 148)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(self.truth["independent_reproduction"])

    def test_08_method_flow_retains_every_scope_failure(self) -> None:
        self.assertEqual(self.flow["method_count"], 67)
        self.assertEqual(self.flow["failed_witness_count"], 227)
        self.assertEqual(self.flow["passing_witness_count"], 60)
        self.assertEqual(self.flow["counts"]["witnesses"], 287)
        self.assertEqual(self.flow["counts"]["state_events"], 120)
        self.assertEqual(self.flow["counts"]["recommendations"], 67)
        self.assertEqual(self.flow["effective_negatives"], 23058)
        self.assertEqual(self.flow["effective_methods"], 7652)
        scoped = [row for row in self.flow["methods"] if row["method_id"].startswith("V6623R-SCOPE-METHOD-")]
        self.assertEqual(len(scoped), 14)
        self.assertEqual(sum(row["recommendation_state"] == "observed" for row in scoped), 7)

    def test_09_family_current_method_flow_skill_accepts_the_ledger(self) -> None:
        self.assertTrue(self.method_validation["valid"])
        self.assertEqual(self.method_validation["issue_count"], 0)
        self.assertEqual(self.method_validation["method_count"], 67)
        self.assertEqual(self.method_validation["witness_count"], 287)

    def test_10_scoped_owner_manifest_replays_current_git_blobs(self) -> None:
        self.assertEqual(replay_manifest("HEAD", self.owner_manifest), [])
        paths = [row["path"] for row in self.owner_manifest["entries"]]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertIn("scripts/ghc_family_v662_v3_2_remaster_canonical_driver.py", paths)
        self.assertIn("tests/test_ghc_family_v662_v3_2_remaster_v661_plus.py", paths)

    def test_11_scoped_delta_manifest_replays_current_git_blobs(self) -> None:
        self.assertEqual(replay_manifest("HEAD", self.delta_manifest), [])
        paths = [row["path"] for row in self.delta_manifest["entries"]]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertIn("scripts/build_ghc_family_v662_v3_2_remaster_v661_plus.py", paths)
        self.assertIn("tests/test_ghc_family_v662_v3_2_remaster_v661_plus.py", paths)

    def test_12_json_privacy_and_document_gates_remain_bounded(self) -> None:
        json_paths = [path for path in PHASE.rglob("*.json")]
        for path in json_paths:
            json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertFalse(self.privacy["privacy_complete"])
        self.assertEqual(len(self.privacy["classes"]), 5)
        self.assertTrue(self.document["valid"])

    def test_13_exact_staged_review_and_validation_are_sealed(self) -> None:
        self.assertEqual(self.staged["state"], "EXACT_STAGED_REVIEW")
        self.assertTrue(self.staged["valid"])
        self.assertEqual(self.staged["missing"], [])
        self.assertEqual(self.staged["unexpected"], [])
        self.assertEqual(self.staged["expected_paths"], self.staged["actual_paths"])
        self.assertTrue(self.validation["valid"])
        self.assertEqual(self.validation["passed"], self.validation["total"])

    def test_14_successor_route_is_prepared_but_unsent(self) -> None:
        self.assertEqual(self.route["next"]["owner"], "Vesper Arlen")
        self.assertEqual(self.route["next"]["phase"], "v662-v4")
        self.assertEqual(self.route["successor_after_vesper"]["owner"], "Lyren Moss")
        self.assertEqual(self.route["successor_after_vesper"]["phase"], "v662-v5")
        self.assertFalse(self.route["message_attempted"])
        self.assertFalse(self.route["sent"])
        self.assertFalse(self.route["acknowledged"])
        self.assertEqual(self.route["delivery_count"], 0)
        self.assertFalse(self.route["substitute_endpoint"])

    def test_15_activation_candidate_preserves_identity_and_claim_boundaries(self) -> None:
        packet = (SCOPE / "routing/vesper-arlen-v662-v4-v661-plus-activation-candidate.md").read_text(encoding="utf-8").lower()
        for phrase in (
            "relational working language only",
            "consciousness",
            "sentience",
            "legal personhood",
            "identity continuity",
            "employment",
            "qualification",
            "independent agency",
            "māori authority",
            "independent reproduction",
            "theory-of-everything",
            "stage 20",
        ):
            self.assertIn(phrase, packet)
        self.assertIn("existing exact-title main task `lyren moss`", packet)
        self.assertIn("task-message acknowledgement", packet)

    def test_16_scope_report_is_substantive_and_accessible(self) -> None:
        report = (SCOPE / "closeout/v661-plus-scope-recovery.md").read_text(encoding="utf-8")
        html = (SCOPE / "reports/scoped-accessible-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(report.split()), 1800)
        self.assertIn("relational working language only", report.lower())
        self.assertIn("Māori authority", report)
        self.assertIn("NOT_READY_FOR_STAGE_20", report)
        self.assertIn('href="#main"', html)
        self.assertIn('id="main"', html)
        self.assertIn("privacy-complete", html)

    def test_17_scoped_canonical_success_is_not_prematurely_claimed(self) -> None:
        self.assertEqual(self.truth["canonical_state"], "NOT_RUN_V661_PLUS_EXACT_FINAL_REQUIRED")
        self.assertEqual(self.truth["canonical_success_count"], 0)
        self.assertFalse(self.truth["message_attempted"])
        self.assertFalse(self.truth["message_sent"])
        self.assertTrue((ROOT / "scripts/ghc_family_v662_v3_2_remaster_canonical_driver.py").is_file())

    def test_18_workload_receipt_preserves_solo_scope(self) -> None:
        workload = read_json("wellbeing/scoped-workload-check.json")
        self.assertTrue(workload["solo"])
        self.assertFalse(workload["delegated"])
        self.assertEqual(workload["subagents"], 0)
        self.assertTrue(workload["broad_attempt_interrupted"])
        self.assertFalse(workload["scoped_aggregate_run"])
        self.assertTrue(workload["pause_redirect_stop_right_preserved"])


if __name__ == "__main__":
    unittest.main()

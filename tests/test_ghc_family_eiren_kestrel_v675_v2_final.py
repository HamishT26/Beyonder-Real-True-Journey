from __future__ import annotations

import hashlib
import json
import shutil
import subprocess  # nosec B404
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "eiren-kestrel" / "v675-v2"
SOURCE_FINAL = "394482bea39831b87a72aefe10a39340543070c7"
X1_COMMIT = "c8d2d107235db9a1e3a42b2d9843596a6f5c1890"
EVIDENCE_COMMIT = "f3bb95c68182c8f7ae1d469ea97443245ce9735b"
X1_MANIFEST = "docs/eiren-kestrel/v675-v2/validation/x1-manifest.json"
EVIDENCE_MANIFEST = "docs/eiren-kestrel/v675-v2/validation/evidence-manifest.json"
DELTA_MANIFEST = "docs/eiren-kestrel/v675-v2/validation/final-delta-manifest.json"
OWNER_MANIFEST = "docs/eiren-kestrel/v675-v2/validation/final-owner-manifest.json"
EXPECTED_FINAL_METHODS = 220
EXPECTED_FINAL_WITNESSES = EXPECTED_FINAL_METHODS * 2
EXPECTED_FINAL_EVENTS = EXPECTED_FINAL_METHODS * 3


def resolve_git_executable() -> str:
    candidate = shutil.which("git")
    if candidate is None:
        raise RuntimeError("git executable is required")
    return candidate


GIT_EXE = resolve_git_executable()


def git(*args: str, check: bool = True) -> bytes:
    return subprocess.run(  # nosec B603
        [GIT_EXE, *args], cwd=ROOT, check=check, capture_output=True
    ).stdout


def git_text(*args: str) -> str:
    return git(*args).decode("utf-8").strip()


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def load(relative: str) -> dict:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def committed_blob(commit: str, path: str) -> bytes:
    return normalized(git("show", f"{commit}:{path}"))


def current_head() -> str:
    return git_text("rev-parse", "HEAD")


def candidate_blob(path: str) -> bytes:
    if current_head() == EVIDENCE_COMMIT:
        return normalized(git("show", f":{path}"))
    return committed_blob(current_head(), path)


def candidate_mode(path: str) -> str:
    if current_head() == EVIDENCE_COMMIT:
        return git_text("ls-files", "-s", "--", path).split()[0]
    return git_text("ls-tree", current_head(), "--", path).split()[0]


def replay_manifest(commit: str, path: str) -> tuple[dict, list[str]]:
    payload = json.loads(committed_blob(commit, path).decode("utf-8"))
    issues = []
    for row in payload["entries"]:
        blob = committed_blob(commit, row["path"])
        mode = git_text("ls-tree", commit, "--", row["path"]).split()[0]
        if len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            issues.append(row["path"])
        if mode != row["mode"]:
            issues.append(f"mode:{row['path']}")
    return payload, issues


def replay_candidate_manifest(path: str) -> tuple[dict, list[str]]:
    payload = json.loads(candidate_blob(path).decode("utf-8"))
    issues = []
    for row in payload["entries"]:
        blob = candidate_blob(row["path"])
        if len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            issues.append(row["path"])
        if candidate_mode(row["path"]) != row["mode"]:
            issues.append(f"mode:{row['path']}")
    return payload, issues


class TestEirenKestrelV675V2Final(unittest.TestCase):
    def test_01_phase_identity_and_lifecycle(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["owner"], "Eiren Kestrel")
        self.assertEqual(truth["phase"], "v675-v2")
        self.assertEqual(truth["source_final"], SOURCE_FINAL)
        self.assertEqual(truth["x1_commit"], X1_COMMIT)
        self.assertEqual(truth["evidence_commit"], EVIDENCE_COMMIT)

    def test_02_outcomes_are_exact(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(
            truth["outcomes"],
            {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        )

    def test_03_proposal_chain_and_rows(self) -> None:
        ledger = load("closeout/proposal-ledger-final.json")
        self.assertEqual(ledger["proposal_chain_before"], 7070)
        self.assertEqual(ledger["proposal_chain_after"], 7110)
        self.assertEqual(len(ledger["rows"]), 40)
        self.assertEqual(len({row["proposal_id"] for row in ledger["rows"]}), 40)

    def test_04_mutations_and_controls_are_bounded(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["mutations"], {"executed": 160, "rejected": 160})
        self.assertEqual(truth["positive_controls"], {"executed": 36, "accepted": 36})
        self.assertEqual(truth["external_actions"], 0)

    def test_05_method_flow_is_complete_and_split(self) -> None:
        flow = load("closeout/method-flow-final.json")
        witness_doc = load("closeout/method-flow-witnesses-final.json")
        self.assertEqual(len(flow["methods"]), EXPECTED_FINAL_METHODS)
        self.assertEqual(len(flow["recommendations"]), EXPECTED_FINAL_METHODS)
        self.assertEqual(len(flow["state_events"]), EXPECTED_FINAL_EVENTS)
        self.assertEqual(flow["witness_count"], EXPECTED_FINAL_WITNESSES)
        self.assertEqual(witness_doc["row_count"], EXPECTED_FINAL_WITNESSES)
        self.assertEqual(
            Counter(row["result"] for row in witness_doc["rows"]),
            Counter({"fail": EXPECTED_FINAL_METHODS, "pass": EXPECTED_FINAL_METHODS}),
        )

    def test_06_negatives_are_retained(self) -> None:
        negatives = load("closeout/retained-negative-register.json")
        self.assertEqual(negatives["row_count"], EXPECTED_FINAL_METHODS)
        self.assertEqual(negatives["failures_rewritten_as_pass"], 0)
        self.assertTrue(all(row["completion_credit"] == 0 for row in negatives["rows"]))

    def test_07_effective_counts_and_gates_are_exact(self) -> None:
        truth = load("closeout/phase-truth.json")
        gates = load("closeout/exact-open-gate-register.json")
        effective = truth["effective_counts"]
        self.assertEqual(effective["effective_negatives"], 40407)
        self.assertEqual(effective["effective_methods"], 28659)
        self.assertEqual(effective["failed_witnesses"], 12068)
        self.assertEqual(effective["bounded_passing_witnesses"], 15942)
        self.assertEqual(gates["effective_open_gaps"], 333)
        self.assertEqual(gates["effective_exact_gates"], 325)

    def test_08_skill_runner_tool_summary_is_bounded(self) -> None:
        summary = load("closeout/skill-runner-tool-summary.json")
        self.assertEqual(summary["skills"]["passed"], 20)
        self.assertEqual(summary["runners"]["passed"], 10)
        self.assertEqual(summary["tools"]["passed"], 3)
        self.assertEqual(summary["global_installations"], 0)
        self.assertEqual(summary["external_actions"], 0)

    def test_09_zero_row_and_real_world_boundaries(self) -> None:
        adapter = load("x2/adapter/nps-tinplate-sheet-metal-zero-row.json")
        truth = load("closeout/phase-truth.json")
        self.assertEqual(adapter["network_calls"], 0)
        self.assertEqual(adapter["rows"], 0)
        self.assertEqual(truth["real_people"], 0)
        self.assertEqual(truth["real_sheet_metal_tinware_or_materials"], 0)
        self.assertEqual(truth["real_fabrication_repairs_or_treatments"], 0)

    def test_10_source_x1_evidence_chain_is_direct(self) -> None:
        self.assertEqual(git_text("rev-parse", f"{X1_COMMIT}^"), SOURCE_FINAL)
        self.assertEqual(git_text("rev-parse", f"{EVIDENCE_COMMIT}^"), X1_COMMIT)
        self.assertEqual(git_text("rev-list", "--count", f"{SOURCE_FINAL}..{EVIDENCE_COMMIT}"), "2")
        self.assertEqual(git_text("rev-list", "--merges", f"{SOURCE_FINAL}..{EVIDENCE_COMMIT}"), "")

    def test_11_final_candidate_history_contract(self) -> None:
        head = current_head()
        if head == EVIDENCE_COMMIT:
            staged = git_text("diff", "--cached", "--name-only", EVIDENCE_COMMIT)
            self.assertTrue(staged)
            self.assertEqual(git_text("rev-list", "--count", f"{SOURCE_FINAL}..{head}"), "2")
        else:
            self.assertEqual(git_text("rev-parse", f"{head}^"), EVIDENCE_COMMIT)
            self.assertEqual(git_text("rev-list", "--count", f"{SOURCE_FINAL}..{head}"), "3")
            self.assertEqual(git_text("rev-list", "--merges", f"{SOURCE_FINAL}..{head}"), "")

    def test_12_x1_manifest_replays(self) -> None:
        payload, issues = replay_manifest(X1_COMMIT, X1_MANIFEST)
        self.assertEqual(payload["entry_count"], len(payload["entries"]))
        self.assertEqual(issues, [])

    def test_13_evidence_manifest_replays(self) -> None:
        payload, issues = replay_manifest(EVIDENCE_COMMIT, EVIDENCE_MANIFEST)
        self.assertEqual(payload["entry_count"], len(payload["entries"]))
        self.assertEqual(issues, [])

    def test_14_final_delta_manifest_replays(self) -> None:
        payload, issues = replay_candidate_manifest(DELTA_MANIFEST)
        self.assertEqual(payload["entry_count"], len(payload["entries"]))
        self.assertEqual(issues, [])

    def test_15_final_owner_manifest_replays_and_covers(self) -> None:
        payload, issues = replay_candidate_manifest(OWNER_MANIFEST)
        declared = {row["path"] for row in payload["entries"]} | set(payload["self_exclusions"])
        if current_head() == EVIDENCE_COMMIT:
            owner_paths = {
                path
                for path in git_text("ls-files", "--cached").splitlines()
                if path.startswith("docs/eiren-kestrel/v675-v2/")
                or "eiren_kestrel_v675_v2" in path
                or Path(path).name
                in {
                    "ghc_family_tinsmith_work_identity.py",
                    "ghc_family_pattern_piece_relations.py",
                    "ghc_family_seam_taxonomy_guard.py",
                    "ghc_family_form_geometry_vacancy.py",
                    "ghc_family_tin_condition_cue.py",
                    "ghc_family_tinsmith_correction_chain.py",
                    "ghc_family_tin_privacy_minimizer.py",
                    "ghc_family_thos_seam_quarantine.py",
                    "ghc_family_freed_id_tinsmith_envelope.py",
                    "ghc_family_cbr_tinsmith_response.py",
                }
            }
            owner_paths.add("docs/eiren-kestrel/v675-v2/validation/final-precommit-test-receipt.json")
        else:
            owner_paths = declared
        self.assertEqual(declared, owner_paths)
        self.assertEqual(issues, [])

    def test_16_privacy_and_staged_review_are_valid(self) -> None:
        privacy = load("validation/final-staged-privacy.json")
        review = load("validation/final-staged-review.json")
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertEqual(privacy["decode_issues"], [])
        self.assertTrue(review["valid"])
        self.assertEqual(review["issues"], [])

    def test_17_validation_receipts_preserve_evidence_truth(self) -> None:
        validation = load("validation/final-validation-receipt.json")
        evidence = load("validation/evidence-validation-receipt.json")
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["json_issues"], [])
        self.assertEqual(validation["word_issues"], [])
        self.assertEqual(validation["python_compile_issues"], [])
        self.assertEqual(evidence["final_evidence_selection"]["passed"], 18)
        self.assertEqual(evidence["final_evidence_selection"]["success_count"], 1)
        self.assertFalse(evidence["final_evidence_selection"]["replayed"])

    def test_18_content_seal_replays(self) -> None:
        seal = load("seal/content-seal.json")
        self.assertEqual(seal["entry_count"], len(seal["entries"]))
        for row in seal["entries"]:
            path = f"docs/eiren-kestrel/v675-v2/{row['path']}"
            blob = candidate_blob(path)
            self.assertEqual(len(blob), row["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"])

    def test_19_canonical_state_is_uninvoked_precommit(self) -> None:
        state = load("final/canonical-invocation-state.json")
        self.assertEqual(state["state"], "NOT_INVOKED_PRECOMMIT")
        self.assertEqual(state["invocation_count"], 0)
        self.assertEqual(state["success_count"], 0)
        self.assertEqual(state["replay_count"], 0)

    def test_20_route_and_baton_are_prepared_not_sent(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        baton = (OWNER_ROOT / "handoffs/elaren-kestrel-v675-v3-activation-candidate.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["sent"])
        self.assertFalse(route["successor_precontacted"])
        self.assertEqual(route["prospective_successor_title"], "Elaren Kestrel")
        self.assertEqual(route["prospective_successor_phase"], "v675-v3")
        self.assertEqual(route["successor_after_successor_title"], "Neris Solane")
        self.assertEqual(route["successor_after_successor_phase"], "v675-v4")
        self.assertGreaterEqual(len(baton.split()), 10000)
        self.assertLessEqual(len(baton.split()), 100000)

    def test_21_accessible_report_has_structural_landmarks(self) -> None:
        html = (OWNER_ROOT / "closeout/accessible-final-report.html").read_text(encoding="utf-8")
        for marker in ("<html lang=", "<header>", "<nav", "<main>", "<section", "<table>", "<caption>", "<footer>"):
            self.assertIn(marker, html)
        self.assertIn("assistive-technology", html)
        self.assertIn("NOT_READY_FOR_STAGE_20", html)

    def test_22_owner_file_and_document_caps(self) -> None:
        owner_files = [path for path in OWNER_ROOT.rglob("*") if path.is_file()]
        if current_head() == EVIDENCE_COMMIT:
            changed = [
                ROOT / path
                for path in git_text("diff", "--cached", "--name-only", EVIDENCE_COMMIT).splitlines()
                if path.startswith(("scripts/", "tests/"))
            ]
        else:
            changed = [
                ROOT / path
                for path in git_text("diff", "--name-only", EVIDENCE_COMMIT, current_head()).splitlines()
                if path.startswith(("scripts/", "tests/"))
            ]
        all_files = owner_files + changed
        self.assertLessEqual(len(all_files), 2000)
        for path in all_files:
            if path.suffix.lower() in {".json", ".md", ".py", ".yaml", ".yml", ".html", ".txt"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)

    def test_23_precommit_receipt_is_conditional_then_required(self) -> None:
        path = OWNER_ROOT / "validation/final-precommit-test-receipt.json"
        if current_head() == EVIDENCE_COMMIT and not path.exists():
            self.assertFalse(path.exists())
        else:
            receipt = load("validation/final-precommit-test-receipt.json")
            self.assertTrue(receipt["valid"])
            self.assertEqual(receipt["passed"], 25)
            self.assertEqual(receipt["tests"], 25)

    def test_24_terminal_and_authority_boundaries_remain(self) -> None:
        truth = load("closeout/phase-truth.json")
        overview = (OWNER_ROOT / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        for marker in ("GMUT", "THOS", "Freed ID", "Māori authority", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(marker, overview)
        self.assertFalse(truth["independent_reproduction"])

    def test_25_closeout_receipt_preserves_history_and_scope(self) -> None:
        receipt = load("closeout/closeout-receipt.json")
        self.assertEqual(receipt["source_final"], SOURCE_FINAL)
        self.assertEqual(receipt["x1_commit"], X1_COMMIT)
        self.assertEqual(receipt["evidence_commit"], EVIDENCE_COMMIT)
        self.assertEqual(receipt["final_parent_required"], EVIDENCE_COMMIT)
        self.assertEqual(receipt["phase_commits_after_final"], 3)
        self.assertEqual(receipt["merges_after_final"], 0)
        self.assertEqual(receipt["full_repository_suite"], "not_run_not_claimed")


if __name__ == "__main__":
    unittest.main()

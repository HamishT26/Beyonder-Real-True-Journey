from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "orin-thale" / "v668-v7"
SOURCE = "8b4c6de2c4ae00c876ffb1342fc6614ef901ab73"
X1 = "95fd7625d1d7ab00816561aa3976441f399bb2d8"
EVIDENCE = "64e5b3f995061e3f7c547a0759e2a5a111dfdbbc"
EXCLUSIONS = {
    "docs/orin-thale/v668-v7/validation/final-owner-manifest.json",
    "docs/orin-thale/v668-v7/validation/final-delta-manifest.json",
    "docs/orin-thale/v668-v7/validation/final-staged-allowlist.json",
}


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True).stdout


class OrinFinalCandidateTests(unittest.TestCase):
    def test_source_x1_evidence_chain_is_exact(self) -> None:
        self.assertEqual(git("rev-parse", f"{X1}^").decode().strip(), SOURCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^").decode().strip(), X1)
        self.assertEqual(git("merge-base", "--is-ancestor", EVIDENCE, "HEAD"), b"")

    def test_closeout_truth_preserves_exact_outcomes_and_terminal_verdict(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(truth["proposal_chain"], 4870)
        self.assertEqual(truth["mutations"], {"preregistered": 160, "executed": 160, "rejected": 160})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_closeout_counts_follow_final_method_flow(self) -> None:
        truth = load("closeout/phase-truth.json")
        flow = load("closeout/method-flow/index.json")
        methods = flow["counts"]["methods"]
        self.assertEqual(flow["counts"]["witness_results"], {"fail": methods, "pass": methods})
        self.assertEqual(truth["effective_negatives"], 29964 + methods + 160)
        self.assertEqual(truth["effective_methods"], 16550 + methods)
        self.assertEqual(truth["failed_witnesses"], 2265 + methods)
        self.assertEqual(truth["bounded_passing_witnesses"], 3092 + methods)

    def test_method_flow_shards_preserve_exact_row_counts(self) -> None:
        index = load("closeout/method-flow/index.json")
        for row in index["shards"]:
            shard = json.loads((ROOT / row["path"]).read_text(encoding="utf-8"))
            self.assertEqual(shard["row_count"], row["row_count"])
            self.assertEqual(len(shard["rows"]), row["row_count"])

    def test_complete_and_incomplete_checklist_keeps_external_gates_open(self) -> None:
        checklist = load("closeout/complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["complete"]), 10)
        self.assertGreaterEqual(len(checklist["incomplete"]), 10)
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_handoff_and_route_are_prepared_not_sent(self) -> None:
        route = load("route/terminal-route-state.json")
        handoff = (PHASE_ROOT / "handoffs" / "liora-venn-v668-v8-activation-candidate.md").read_text(encoding="utf-8")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["successor_title"], "Liora Venn")
        self.assertEqual(route["successor_phase"], "v668-v8")
        self.assertEqual(route["send_count"], 0)
        self.assertIn("SENT_BY_ORIN_THALE = false", handoff)

    def test_canonical_candidate_is_pending_and_not_replayed(self) -> None:
        candidate = load("final/final-validation-candidate.json")
        contract = load("validation/final-canonical-contract.json")
        self.assertEqual(candidate["canonical_invocations"], 0)
        self.assertEqual(candidate["canonical_successes"], 0)
        self.assertTrue(contract["one_attributable_invocation"])
        self.assertFalse(contract["replay_after_success"])
        self.assertFalse(contract["full_repository_suite"])

    def test_final_delta_contains_no_frozen_x1_or_x2_changes(self) -> None:
        paths = git("diff", "--name-only", EVIDENCE).decode().splitlines()
        frozen = [path for path in paths if path.startswith("docs/orin-thale/v668-v7/x1/") or path.startswith("docs/orin-thale/v668-v7/x2/") or path.endswith("v668_v7_x1.py") or path.endswith("v668_v7_x2.py")]
        self.assertEqual(frozen, [])

    def test_final_delta_manifest_matches_allowlist_domain(self) -> None:
        manifest = load("validation/final-delta-manifest.json")
        allowlist = load("validation/final-staged-allowlist.json")
        self.assertEqual({row["path"] for row in manifest["entries"]}, set(allowlist["intended_paths_before_manifests"]))
        self.assertEqual(set(manifest["self_exclusions"]), EXCLUSIONS)
        self.assertEqual(manifest["coverage_count"], manifest["entry_count"] + 3)

    def test_owner_manifest_replays_clean_filter_blobs(self) -> None:
        manifest = load("validation/final-owner-manifest.json")
        self.assertEqual(set(manifest["self_exclusions"]), EXCLUSIONS)
        self.assertEqual(manifest["coverage_count"], manifest["entry_count"] + 3)
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            oid = subprocess.run(
                ["git", "-C", str(ROOT), "hash-object", "-w", f"--path={row['path']}", "--stdin"],
                input=path.read_bytes(), check=True, capture_output=True,
            ).stdout.decode().strip()
            data = git("cat-file", "blob", oid)
            self.assertEqual(oid, row["git_blob_oid"])
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])

    def test_integrated_overview_is_three_page_equivalent_and_bounded(self) -> None:
        text = (PHASE_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\b\w+[\w'-]*\b", text))
        self.assertGreaterEqual(words, 1200)
        self.assertLessEqual(words, 6000)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_accessible_report_reserves_manual_and_affected_user_review(self) -> None:
        text = (PHASE_ROOT / "closeout" / "accessible-static-report.html").read_text(encoding="utf-8")
        self.assertIn("<main", text)
        self.assertIn("<caption>", text)
        self.assertIn("scope='col'", text)
        self.assertIn("Manual keyboard", text)
        self.assertIn("affected-user evaluation remain reserved", text)

    def test_all_phase_json_parses_and_documents_fit_ceiling(self) -> None:
        for path in PHASE_ROOT.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))
        for path in PHASE_ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt", ".html", ".yaml", ".yml"}:
                words = len(re.findall(r"\b\w+[\w'-]*\b", path.read_text(encoding="utf-8")))
                self.assertLessEqual(words, 6000, path.as_posix())

    def test_public_closeout_has_no_raw_private_material(self) -> None:
        patterns = [
            re.compile(r"<codex_delegation>", re.I),
            re.compile(r"source_thread_id\s*[:=]", re.I),
            re.compile(r"\b[A-Z]:\\Users\\[^\s\"']+", re.I),
            re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        ]
        hits = []
        for root_name in ("closeout", "final", "handoffs", "route", "seal", "validation"):
            for path in (PHASE_ROOT / root_name).rglob("*"):
                if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml", ".yml"}:
                    text = path.read_text(encoding="utf-8")
                    if any(pattern.search(text) for pattern in patterns):
                        hits.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(hits, [])

    def test_content_seal_preserves_gates_and_no_sent_claim(self) -> None:
        seal = load("seal/content-seal.json")
        self.assertEqual(seal["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertTrue(seal["no_failure_erased"])
        self.assertEqual(seal["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(seal["route_state"], "PREPARED_NOT_SENT")


if __name__ == "__main__":
    unittest.main()

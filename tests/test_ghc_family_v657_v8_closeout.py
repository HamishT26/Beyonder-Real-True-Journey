from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v657-v8"
SOURCE = "664460f294989f14c8ebcb1c157bdf67f9bf1052"
X1 = "a48c87af28aa55a8bb6aea056e4652906cdb575f"
EVIDENCE = "ea2f0132bd129e38167ab08e255a70bd386d3869"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class V657V8CloseoutTests(unittest.TestCase):
    def test_immutable_anchor_chain(self) -> None:
        subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE, "HEAD"], cwd=ROOT, check=True)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)

    def test_final_truth_candidate(self) -> None:
        truth = load("truth/phase-truth.json")
        self.assertEqual(truth["outcome_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 16491)
        self.assertEqual((truth["effective_open_gaps"], truth["effective_exact_gates"]), (112, 111))
        self.assertEqual(truth["real_rows"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])

    def test_closeout_method_flow_parity(self) -> None:
        flow = load("method-flow/method-flow-state-final-candidate.json")
        self.assertEqual(flow["counts"]["current_methods"], 0)
        self.assertEqual(flow["counts"]["current_witness_results"], {"fail": 0, "pass": 0})
        self.assertEqual(flow["counts"]["effective_methods"], 2765)
        self.assertEqual(flow["counts"]["effective_witness_results"], {"fail": 2765, "pass": 2765})
        self.assertTrue(flow["all_failed_witnesses_retained"])

    def test_prior_manifests_replay(self) -> None:
        replay = load("closeout/prior-manifest-replay.json")
        self.assertTrue(replay["valid"])
        self.assertEqual(replay["x1"]["entry_count"], 40)
        self.assertEqual(replay["evidence"]["entry_count"], 260)
        self.assertEqual(replay["total_entries"], 300)

    def test_route_has_no_successor_authorization(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual(route["state"], "NO_SUCCESSOR_AUTHORIZED_REQUIRES_FRESH_LIVE_ROUTE")
        self.assertIsNone(route["next_exact_title"])
        self.assertIsNone(route["next_phase"])
        self.assertFalse(route["message_sent"])
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["subagent_spawned"])
        self.assertEqual(route["tavian_sol_state"], "ON_STANDBY")

    def test_final_records_do_not_preclaim_postcommit_facts(self) -> None:
        truth = load("truth/phase-truth.json")
        closeout = load("closeout/closeout-receipt.json")
        seal = load("seal/seal-candidate.json")
        prereq = load("final/final-validation-prerequisites.json")
        self.assertEqual(truth["final_commit"], "commit_containing_this_record")
        self.assertEqual(closeout["candidate_final"], "commit_containing_this_receipt")
        self.assertEqual(seal["candidate_final"], "commit_containing_this_receipt")
        self.assertEqual(closeout["canonical_validation_state"], "NOT_RUN_BEFORE_FINAL_COMMIT")
        self.assertTrue(prereq["requires_external_receipt"])
        self.assertTrue(prereq["post_success_replay_forbidden"])

    def test_closeout_artifact_packet_exists(self) -> None:
        required = [
            "deliverables/v657-v8-closeout-summary.md",
            "final-complete-incomplete-checklist.json",
            "closeout/closeout-receipt.json",
            "seal/seal-candidate.json",
            "final/final-validation-prerequisites.json",
            "truth/retained-negative-register-final-candidate.json",
            "truth/exact-open-gate-register-final-candidate.json",
            "tooling/ghc-family-index-final.json",
            "tooling/roster-check-final.json",
            "startup/final-environment-version-receipt.json",
            "wellbeing/final-wellbeing-check.json",
        ]
        self.assertTrue(all((PHASE / path).is_file() for path in required))

    def test_closeout_manifest_contract(self) -> None:
        manifest = load("validation/closeout-content-manifest.json")
        exclusions = {row["path"] for row in manifest["declared_exclusions"]}
        self.assertGreaterEqual(manifest["entry_count"], 270)
        self.assertEqual(manifest["declared_exclusion_count"], 3)
        self.assertIn("docs/tamar-vey/v657-v8/validation/closeout-content-manifest.json", exclusions)
        self.assertEqual(len(manifest["entries"]), manifest["entry_count"])

    def test_summary_preserves_claim_boundaries(self) -> None:
        text = (PHASE / "deliverables/v657-v8-closeout-summary.md").read_text(encoding="utf-8")
        for token in ["NOT_READY_FOR_STAGE_20", "zero rows", "NO_SUCCESSOR_AUTHORIZED", "relational working language"]:
            self.assertIn(token, text)

    def test_phase_documents_parse_and_stay_bounded(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 220)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))
        documents = [
            path for path in PHASE.rglob("*")
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}
        ]
        self.assertLessEqual(max(len(path.read_text(encoding="utf-8").split()) for path in documents), 100000)


if __name__ == "__main__":
    unittest.main()

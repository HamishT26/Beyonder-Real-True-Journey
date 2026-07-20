from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v650-v2"
X1 = "d70cbab27e64e12d634e0d9b94b73f50aa507ad1"


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


class IlyraV650V2EvidenceTests(unittest.TestCase):
    def test_outcomes_and_negative_retention(self) -> None:
        outcomes = load("x2/core-outcome-ledger.json")
        self.assertEqual(outcomes["proposal_count"], 20)
        self.assertEqual(
            outcomes["distribution"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(outcomes["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        negatives = load("x2/retained-negative-register.json")
        self.assertEqual(negatives["inherited_effective"], 5579)
        self.assertEqual(negatives["x1_operational"], 8)
        self.assertEqual(negatives["synthetic_executed_and_rejected"], 100)
        self.assertEqual(negatives["x2_operational"], 3)
        self.assertEqual(negatives["effective_at_evidence"], 5690)
        self.assertFalse(negatives["negative_erased"])

    def test_expanded_portfolios_are_complete(self) -> None:
        self.assertEqual(load("x2/safe-now-results.json")["completed_count"], 40)
        self.assertEqual(load("x2/candidate-results.json")["completed_count"], 30)
        self.assertEqual(load("x2/clean-fix-refine-results.json")["completed_count"], 40)
        skills = load("x2/skill-use-ledger.json")
        self.assertEqual((skills["completed_count"], skills["pending_count"]), (20, 0))
        self.assertFalse(skills["global_installation"])
        self.assertFalse(skills["subagent_forward_test"])
        self.assertTrue(
            all(row["smoke_used"] and row["quick_validate_returncode"] == 0 for row in skills["skills"])
        )
        runners = load("x2/runner-use-ledger.json")
        self.assertEqual((runners["completed_count"], runners["pending_count"]), (10, 0))
        self.assertTrue(
            all(
                row["passing_fixture"] and row["rejecting_fixture"] and row["secondary_library_use"]
                for row in runners["runners"]
            )
        )

    def test_core_artifacts_and_mutations(self) -> None:
        outcomes = load("x2/core-outcome-ledger.json")["outcomes"]
        self.assertEqual(len(outcomes), 20)
        for row in outcomes:
            root = PHASE / row["artifact_root"]
            contract = json.loads((root / "contract.json").read_text(encoding="utf-8"))
            mutation = json.loads((root / "mutation-results.json").read_text(encoding="utf-8"))
            receipt = json.loads((root / "bounded-receipt.json").read_text(encoding="utf-8"))
            self.assertTrue(contract["bounded"])
            self.assertFalse(contract["production"] or contract["authority_credit"] or contract["stage20"])
            self.assertEqual(
                (contract["real_rows"], contract["real_people"], contract["queries"], contract["downloads"]),
                (0, 0, 0, 0),
            )
            self.assertEqual((mutation["count"], mutation["rejected_count"]), (5, 5))
            self.assertTrue(all(item["negative_retained"] for item in mutation["mutations"]))
            self.assertEqual(receipt["outcome"], row["outcome"])
        all_mutations = load("x2/synthetic-mutation-results.json")
        self.assertEqual((all_mutations["count"], all_mutations["rejected_count"]), (100, 100))
        self.assertTrue(all_mutations["all_retained"])

    def test_gates_method_flow_and_route(self) -> None:
        gates = load("x2/gate-register.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (44, 45))
        self.assertEqual(gates["silently_closed"], 0)
        methods = load("method-flow/method-flow-summary-x2.json")
        self.assertEqual(methods["counts"]["methods"], 11)
        self.assertEqual(methods["counts"]["witness_results"], {"fail": 11, "pass": 11})
        state = load("orchestration/phase-state-evidence.json")
        self.assertEqual(state["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(state["subagents"], 0)

    def test_skills_are_phase_local_valid_and_metadata_bound(self) -> None:
        for row in load("x2/skill-use-ledger.json")["skills"]:
            folder = PHASE / "skills" / row["name"]
            skill = (folder / "SKILL.md").read_text(encoding="utf-8")
            metadata = (folder / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertTrue(skill.startswith("---\nname:"))
            self.assertIn(f"${row['name']}", metadata)
            self.assertNotIn("TODO", skill)

    def test_x1_frozen_surface_is_blob_stable(self) -> None:
        manifest = load("validation/x1-staged-manifest.json")
        for row in manifest["entries"]:
            self.assertEqual(git("rev-parse", f"{X1}:{row['path']}"), row["git_blob"])
            self.assertEqual(git("hash-object", f"--path={row['path']}", row["path"]), row["git_blob"])

    def test_documents_and_truth_boundaries(self) -> None:
        documents = load("validation/document-cap-receipt.json")
        self.assertTrue(documents["all_under_20000"])
        self.assertTrue(documents["overview_three_page_equivalent"])
        report = (PHASE / "deliverables" / "v650-v2-bounded-evidence-report.html").read_text(encoding="utf-8")
        self.assertIn("Skip to main content", report)
        self.assertNotIn("<script", report.casefold())
        self.assertIn("affected-user evaluation remain reserved", report)
        truth = load("phase-truth-evidence.json")
        self.assertFalse(truth["full_repository_suite"])
        self.assertFalse(truth["replay_used"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()

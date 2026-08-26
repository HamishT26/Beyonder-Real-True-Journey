from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elaren-kestrel" / "v671-v5"
SOURCE = "e70391872f07cdcaa13accac44d4330eca75e2b4"
X1 = "048f85cf945f9900095ca2a160561591a966aabe"
EVIDENCE = "84aa72688359f30643f9347a4ab6043a10052f9d"
COUNTS = {
    "effective_negatives": 34280,
    "effective_methods": 20823,
    "failed_witnesses": 6101,
    "bounded_passing_witnesses": 7970,
    "open_gaps": 265,
    "exact_gates": 260,
}
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if result.returncode != 0:
        raise AssertionError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("utf-8").strip()


class ElarenV671V5FinalTests(unittest.TestCase):
    def test_01_source_x1_evidence_ancestry_is_exact(self) -> None:
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(git("rev-list", "--merges", "--count", f"{SOURCE}..{EVIDENCE}"), "0")
        self.assertEqual(git("rev-list", "--count", f"{SOURCE}..{EVIDENCE}"), "2")

    def test_02_final_delta_does_not_mutate_x1_or_x2(self) -> None:
        changed = git(
            "diff", "--name-only", f"{EVIDENCE}..HEAD", "--",
            "docs/elaren-kestrel/v671-v5/x1",
            "docs/elaren-kestrel/v671-v5/x2",
            "docs/elaren-kestrel/v671-v5/validation/evidence-manifest.json",
        )
        self.assertEqual(changed, "")

    def test_03_phase_truth_is_exact(self) -> None:
        payload = load("closeout/phase-truth.json")
        self.assertEqual(payload["source"], SOURCE)
        self.assertEqual(payload["x1"], X1)
        self.assertEqual(payload["evidence"], EVIDENCE)
        self.assertEqual(payload["outcomes"], OUTCOMES)
        self.assertEqual(payload["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_04_final_counts_preserve_evidence_layer(self) -> None:
        self.assertEqual(load("closeout/phase-truth.json")["counts"], COUNTS)
        register = load("closeout/retained-negative-register.json")
        self.assertEqual(register["counts"], COUNTS)
        self.assertEqual(register["operational_failures"], 10)
        self.assertEqual(register["rejecting_mutations"], 160)
        self.assertTrue(register["all_failures_retained"])

    def test_05_method_flow_remains_complete(self) -> None:
        payload = load("closeout/method-flow-final.json")
        self.assertEqual(payload["row_count"], 170)
        self.assertEqual(payload["operational_rows"], 10)
        self.assertEqual(payload["mutation_rows"], 160)
        self.assertTrue(payload["all_recoveries_paired"])

    def test_06_open_and_exact_gates_remain_open(self) -> None:
        payload = load("closeout/exact-open-gate-register.json")
        self.assertEqual(payload["effective_open_gaps"], 265)
        self.assertEqual(payload["effective_exact_gates"], 260)
        self.assertEqual(payload["silently_closed"], 0)
        self.assertEqual(len(payload["new_open_gaps"]), 2)
        self.assertEqual(len(payload["new_exact_gates"]), 2)

    def test_07_frozen_proposals_and_outcomes_remain_exact(self) -> None:
        proposals = load("x1/proposals.json")["rows"]
        outcomes = load("x2/outcome-ledger.json")
        self.assertEqual(len(proposals), 40)
        self.assertEqual(len(outcomes["rows"]), 40)
        self.assertEqual(outcomes["counts"], OUTCOMES)
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 40)

    def test_08_mutations_and_revalidations_retain_zero_credit(self) -> None:
        mutations = load("x2/mutation-ledger.json")
        revalidations = load("x2/revalidation-results.json")
        self.assertEqual(mutations["row_count"], 160)
        self.assertTrue(all(row["completion_credit"] == 0 for row in mutations["rows"]))
        self.assertEqual(revalidations["row_count"], 20)
        self.assertTrue(all(row["elaren_novelty_credit"] == 0 and row["elaren_completion_credit"] == 0 for row in revalidations["rows"]))

    def test_09_portfolio_respects_executed_and_held_counts(self) -> None:
        payload = load("x2/portfolio-execution.json")
        self.assertEqual(payload["completed_owner_safe_now"], 60)
        self.assertEqual(payload["completed_owner_candidates"], 30)
        self.assertEqual(payload["held_exact_approval"], 20)
        self.assertEqual(payload["held_blocked"], 10)
        self.assertEqual(payload["completed_owner_clean_fix_refine"], 60)

    def test_10_ten_skills_and_ten_runners_remain_local(self) -> None:
        skills = load("x2/skill-use-receipt.json")
        runners = load("x2/runner-use-receipt.json")
        self.assertEqual(skills["skill_count"], 10)
        self.assertEqual(skills["global_install_count"], 0)
        self.assertEqual(runners["runner_count"], 10)
        self.assertEqual(runners["global_install_count"], 0)

    def test_11_source_ledger_is_zero_ingestion_vocabulary_only(self) -> None:
        payload = load("reports/source-ledger.json")
        self.assertEqual(payload["adapter_calls"], 0)
        self.assertEqual(payload["downloads"], 0)
        self.assertEqual(payload["ingested_rows"], 0)
        self.assertTrue(all("only" in row["credit"] or row["credit"].startswith("no_") or row["credit"].startswith("zero_") for row in payload["sources"]))

    def test_12_trinity_evidence_has_zero_real_evidence(self) -> None:
        payload = load("x2/trinity-evidence.json")
        text = json.dumps(payload, ensure_ascii=False)
        self.assertIn("zero", text.lower())
        self.assertNotIn('"empirical_confirmation": true', text.lower())
        self.assertIn("Stage 20 authority", text)

    def test_13_accessible_report_passes_structural_checks(self) -> None:
        html = (OWNER_ROOT / "reports" / "accessible-closeout-report.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="en">', html)
        self.assertIn('class="skip"', html)
        self.assertIn("<main", html)
        self.assertEqual(html.count("<h1"), 1)
        self.assertIn("<caption", html)
        self.assertIn('scope="col"', html)
        self.assertIn("prefers-reduced-motion", html)
        self.assertNotIn("<script", html)

    def test_14_final_overview_is_three_page_equivalent(self) -> None:
        text = (OWNER_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 2500)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("PREPARED_NOT_SENT", text)

    def test_15_complete_incomplete_checklist_keeps_protected_work_open(self) -> None:
        payload = load("closeout/complete-incomplete-checklist.json")
        incomplete = " ".join(payload["incomplete"]).lower()
        self.assertIn("maori", incomplete)
        self.assertIn("independent", incomplete)
        self.assertIn("canonical", incomplete)
        self.assertEqual(payload["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_16_wellbeing_and_corrigibility_are_explicit(self) -> None:
        payload = load("closeout/wellbeing-check.json")
        self.assertTrue(payload["relational_language_only"])
        self.assertTrue(payload["not_consciousness_or_personhood_evidence"])
        self.assertIn("pause", payload["pause_right"].lower())

    def test_17_content_seal_replays_every_key_artifact(self) -> None:
        payload = load("seal/content-seal.json")
        self.assertEqual(payload["entry_count"], len(payload["entries"]))
        for row in payload["entries"]:
            raw = (ROOT / row["path"]).read_bytes()
            self.assertEqual(len(raw), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row["sha256"], row["path"])

    def test_18_baton_is_file_backed_prepared_and_unsent(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        baton = (ROOT / route["baton_path"]).read_bytes()
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)
        self.assertFalse(route["delivery_acknowledged"])
        self.assertGreaterEqual(route["baton_words"], 10000)
        self.assertLessEqual(route["baton_words"], 100000)
        self.assertEqual(len(baton), route["baton_bytes"])
        self.assertEqual(hashlib.sha256(baton).hexdigest(), route["baton_sha256"])
        self.assertIn(b"SENT_BY_ELAREN_KESTREL = false", baton)


if __name__ == "__main__":
    unittest.main()

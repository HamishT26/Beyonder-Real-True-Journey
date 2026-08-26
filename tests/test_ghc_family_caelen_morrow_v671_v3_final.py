"""Final-candidate and exact-final tests for Caelen Morrow v671-v3."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "caelen-morrow" / "v671-v3"
SOURCE = "33b7c2d6b9f79f931ff98c478f136dab823c4d69"
X1 = "2551c126776ea0538354a32b90414f31f5cec4b3"
EVIDENCE = "46c41e84871edd72544ddad16f038902ec2386f5"
BRANCH = "codex/GHC-Family/caelen-morrow-v671-v3-full-tools"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def run(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        args, cwd=ROOT, check=False, capture_output=True, timeout=120
    )


def git_text(*args: str) -> str:
    result = run("git", *args)
    if result.returncode:
        raise AssertionError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("utf-8", errors="replace").strip()


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def candidate_mode() -> bool:
    return git_text("rev-parse", "HEAD") == EVIDENCE


def blob(path: str) -> bytes:
    spec = f":{path}" if candidate_mode() else f"HEAD:{path}"
    result = run("git", "show", spec)
    if result.returncode:
        raise AssertionError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.replace(b"\r\n", b"\n")


class CaelenMorrowV671V3FinalTests(unittest.TestCase):
    def test_01_exact_branch_and_expected_lifecycle_head(self):
        self.assertEqual(git_text("branch", "--show-current"), BRANCH)
        head = git_text("rev-parse", "HEAD")
        expected = os.environ.get("GHC_CAELEN_V671_V3_EXPECTED_FINAL")
        if expected:
            self.assertEqual(head, expected)
        else:
            self.assertEqual(head, EVIDENCE)

    def test_02_direct_single_parent_zero_merge_history(self):
        head = git_text("rev-parse", "HEAD")
        if head == EVIDENCE:
            self.assertEqual(git_text("rev-parse", "HEAD^"), X1)
            self.assertEqual(
                int(git_text("rev-list", "--count", f"{SOURCE}..HEAD")), 2
            )
        else:
            self.assertEqual(git_text("rev-parse", "HEAD^"), EVIDENCE)
            self.assertEqual(
                int(git_text("rev-list", "--count", f"{SOURCE}..HEAD")), 3
            )
        self.assertEqual(
            int(git_text("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")), 0
        )
        self.assertEqual(git_text("rev-parse", f"{X1}^"), SOURCE)
        self.assertEqual(git_text("rev-parse", f"{EVIDENCE}^"), X1)

    def test_03_final_truth_is_exact_and_bounded(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["proposal_chain"], {"before": 5630, "after": 5670})
        self.assertEqual(
            truth["outcomes"],
            {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        )
        self.assertEqual(truth["effective_negatives"], 33905)
        self.assertEqual(truth["effective_methods"], 20222)
        self.assertEqual(truth["failed_witnesses"], 5726)
        self.assertEqual(truth["passing_witnesses"], 7333)
        self.assertEqual(truth["open_gaps"], 261)
        self.assertEqual(truth["exact_gates"], 256)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["real_world_actions"], 0)
        self.assertEqual(truth["authority_acts"], 0)

    def test_04_frozen_proposals_and_outcomes_remain_exact(self):
        proposals = load("x1/proposals.json")
        outcomes = load("x2/outcome-ledger.json")
        self.assertEqual(len(proposals["rows"]), 40)
        self.assertEqual(len({row["proposal_id"] for row in proposals["rows"]}), 40)
        self.assertEqual(
            {row["expected_disposition"] for row in proposals["rows"]}, LABELS
        )
        self.assertEqual(len(outcomes["rows"]), 40)
        self.assertEqual(outcomes["counts"], proposals["outcomes"])

    def test_05_contracts_remain_synthetic_zero_counter_and_non_authoritative(self):
        contracts = sorted((OWNER_ROOT / "x2/contracts").glob("*.json"))
        self.assertEqual(len(contracts), 40)
        for path in contracts:
            row = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(row["synthetic_only"])
            self.assertFalse(row["authoritative"])
            self.assertTrue(all(value == 0 for value in row["zero_counters"].values()))
            self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
            self.assertIn(row["observed_disposition"], LABELS)

    def test_06_rejecting_mutations_are_all_retained_at_zero_credit(self):
        ledgers = sorted((OWNER_ROOT / "x2/mutations").glob("*.json"))
        rows = [row for path in ledgers for row in json.loads(path.read_text(encoding="utf-8"))["rows"]]
        self.assertEqual(len(rows), 160)
        self.assertEqual(len({row["mutation_id"] for row in rows}), 160)
        self.assertTrue(all(row["attempted"] and not row["accepted"] for row in rows))
        self.assertTrue(
            all(
                row["retained_failed_witness"] and row["completion_credit"] == 0
                for row in rows
            )
        )

    def test_07_retention_method_flow_and_gate_counts_match(self):
        negative = load("closeout/retained-negative-register.json")
        method = load("closeout/method-flow-final.json")
        gates = load("closeout/exact-open-gate-register.json")
        self.assertEqual(negative["effective_negatives"], 33905)
        self.assertEqual(negative["erased"], 0)
        self.assertEqual(method["effective_methods"], 20222)
        self.assertEqual(method["failed_witnesses"], 5726)
        self.assertEqual(method["passing_witnesses"], 7333)
        self.assertEqual(len(method["closeout_operational_failures"]), 3)
        self.assertTrue(method["all_failures_retained"])
        self.assertEqual(method["x2_aggregate_success_credit"], 0)
        self.assertEqual(gates["effective_open_gaps"], 261)
        self.assertEqual(gates["effective_exact_gates"], 256)
        self.assertEqual(gates["erased"], 0)

    def test_08_tool_bank_and_environment_are_bounded(self):
        environment = load("closeout/environment-version-final.json")
        usage = load("tools/bounded-tool-use-ledger.json")
        self.assertEqual(environment["package_count"], 25)
        self.assertTrue(environment["all_versions_present"])
        self.assertTrue(environment["npm_prefix_on_d_drive"])
        self.assertTrue(environment["npm_cache_on_d_drive"])
        self.assertEqual(environment["installations_this_phase"], 0)
        self.assertEqual(environment["updates_this_phase"], 0)
        self.assertEqual(environment["host_security_changes"], 0)
        self.assertEqual(usage["package_rows"], 25)
        self.assertEqual(usage["global_state_mutations"], 0)

    def test_09_main_skills_phase_skills_and_runners_are_visible(self):
        receipt = load("orchestration/skill-runner-use-final.json")
        self.assertEqual(receipt["main_skill_count"], len(receipt["main_skills"]))
        self.assertGreaterEqual(receipt["main_skill_count"], 20)
        self.assertEqual(receipt["phase_local_skills_built_and_smoke_used"], 10)
        self.assertEqual(receipt["family_current_runners_built_and_smoke_used"], 10)
        self.assertEqual(receipt["package_bank_count"], 25)
        self.assertFalse(receipt["independent_authority"])
        self.assertEqual(
            len(list((OWNER_ROOT / "skills").glob("*/SKILL.md"))), 10
        )

    def test_10_invalid_x2_aggregate_and_narrow_recovery_are_not_laundered(self):
        receipt = load("x2/x2-test-composite.json")
        self.assertEqual(receipt["original_aggregate"]["tests_passed"], 15)
        self.assertEqual(
            receipt["original_aggregate"]["aggregate_success_credit"], 0
        )
        self.assertFalse(receipt["original_aggregate"]["replayed"])
        recovery = receipt["isolated_dependency_recovery"]
        self.assertEqual(recovery["tests_run"], 1)
        self.assertEqual(recovery["successful_tests_replayed"], 0)
        self.assertEqual(recovery["covered_lines"], 67)
        self.assertEqual(recovery["statements"], 114)
        self.assertTrue(recovery["passed"])
        self.assertFalse(receipt["canonical_validation"])

    def test_11_source_adapter_and_public_sources_remain_zero_row(self):
        adapter = load("x2/source-adapter-status.json")
        source = load("x1/source-ledger.json")
        self.assertFalse(adapter["enabled"])
        self.assertEqual(
            sum(adapter[key] for key in ("network_calls", "downloads", "rows", "media")),
            0,
        )
        self.assertEqual(source["adapter_calls"], 0)
        self.assertEqual(source["real_rows"], 0)
        self.assertEqual(len(source["sources"]), 5)

    def test_12_accessibility_structure_and_reserved_evaluation_remain_visible(self):
        report = (OWNER_ROOT / "x2/accessible-evidence-report.html").read_text(
            encoding="utf-8"
        )
        for phrase in (
            'lang="en"',
            'href="#main"',
            "<main",
            "<caption>",
            'scope="col"',
            "assistive-technology",
            "affected-user",
            "NOT_READY_FOR_STAGE_20",
        ):
            self.assertIn(phrase, report)
        checklist = load("closeout/complete-incomplete-checklist.json")
        incomplete = " ".join(checklist["incomplete"])
        self.assertIn("manual browser", incomplete)
        self.assertIn("Maori authority", incomplete)

    def test_13_every_owner_json_document_parses(self):
        paths = sorted(OWNER_ROOT.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 180)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_14_final_staged_review_is_exact_and_non_destructive(self):
        review = load("validation/final-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["frozen_x1_or_evidence_mutations"], [])
        self.assertEqual(review["out_of_scope"], [])
        self.assertEqual(review["deleted_paths"], [])

    def test_15_final_delta_and_owner_manifests_replay_exact_blobs(self):
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        self.assertEqual(delta["entry_count"], len(delta["entries"]))
        self.assertEqual(owner["entry_count"], len(owner["entries"]))
        self.assertEqual(delta["hash_domain"], "normalized_lf_exact_staged_git_blob")
        self.assertEqual(owner["hash_domain"], "normalized_lf_exact_git_index_blob")
        for manifest in (delta, owner):
            for entry in manifest["entries"]:
                data = blob(entry["path"])
                self.assertEqual(len(data), entry["bytes"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_16_content_seal_and_handoff_integrity_are_exact(self):
        seal = load("seal/content-seal.json")
        handoff_path = OWNER_ROOT / "handoffs/eiren-kestrel-v671-v4-activation-candidate.md"
        data = handoff_path.read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(len(data), seal["handoff_candidate_bytes_normalized_lf"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), seal["handoff_candidate_sha256_normalized_lf"])
        self.assertEqual(
            len(handoff_path.read_text(encoding="utf-8").split()),
            seal["handoff_candidate_words"],
        )
        self.assertEqual(seal["delivery_state"], "PREPARED_NOT_SENT")
        self.assertEqual(seal["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_17_route_is_prepared_not_sent_and_no_endpoint_was_contacted(self):
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["prospective_existing_task_title"], "Eiren Kestrel")
        self.assertEqual(route["prospective_phase"], "v671-v4")
        self.assertEqual(route["successor_contact_count"], 0)
        self.assertEqual(route["task_creation_count"], 0)
        self.assertEqual(route["fork_count"], 0)
        self.assertEqual(route["standby_contact_count"], 0)
        self.assertTrue(route["requires_terminal_live_refresh"])

    def test_18_complete_incomplete_and_wellbeing_boundaries_are_preserved(self):
        checklist = load("closeout/complete-incomplete-checklist.json")
        wellbeing = load("closeout/wellbeing-check.json")
        self.assertGreaterEqual(len(checklist["complete"]), 6)
        self.assertGreaterEqual(len(checklist["incomplete"]), 6)
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(wellbeing["real_people"], 0)
        self.assertFalse(wellbeing["human_performance_inference"])
        self.assertTrue(wellbeing["pause_and_stop_rights_preserved"])

    def test_19_owner_file_and_document_word_caps_are_respected(self):
        files = [path for path in OWNER_ROOT.rglob("*") if path.is_file()]
        self.assertLessEqual(len(files), 2000)
        for path in files:
            if path.suffix.lower() in {".json", ".md", ".html", ".txt", ".py"}:
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(text.split()), 100000, str(path))

    def test_20_frozen_x1_and_evidence_surfaces_are_unchanged_by_closeout(self):
        paths = [
            "docs/caelen-morrow/v671-v3/x1",
            "docs/caelen-morrow/v671-v3/x2",
            "docs/caelen-morrow/v671-v3/method-flow",
            "docs/caelen-morrow/v671-v3/skills",
            "docs/caelen-morrow/v671-v3/tools",
            "scripts/build_ghc_family_caelen_morrow_v671_v3_x1.py",
            "scripts/build_ghc_family_caelen_morrow_v671_v3_x2.py",
            "scripts/ghc_family_caelen_morrow_v671_v3_letterpress.py",
            "tests/test_ghc_family_caelen_morrow_v671_v3_x1.py",
            "tests/test_ghc_family_caelen_morrow_v671_v3_x2.py",
        ]
        changed = git_text("diff", "--name-only", EVIDENCE, "--", *paths)
        self.assertEqual(changed, "")


if __name__ == "__main__":
    unittest.main()

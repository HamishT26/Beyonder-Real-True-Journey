"""Exact-final owner-scoped tests for Eiren Kestrel v671-v4."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v671-v4"
SOURCE = "37ac80c499d43a90c874876402b262a220a252a1"
X1 = "1c4d262b14cb8528fb9d72aad40a5e4fb7423b26"
EVIDENCE = "000c4c75ccac98794b43a0171f2d330436e6069d"


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git(*args: str, binary: bool = False):
    result = subprocess.run(
        ["git", *args], cwd=REPO, check=True, capture_output=True
    )
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def normalized_final_blob(path: str) -> bytes:
    return git("show", f"HEAD:{path}", binary=True).replace(b"\r\n", b"\n")


class EirenKestrelV671V4FinalTests(unittest.TestCase):
    def test_01_exact_direct_parent_chain_and_zero_merges(self):
        head = git("rev-parse", "HEAD")
        self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        commits = git("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
        self.assertEqual(commits[:2], [X1, EVIDENCE])
        self.assertEqual(commits[-1], head)
        self.assertEqual(len(commits), 3)
        self.assertEqual(git("rev-list", "--merges", f"{SOURCE}..{head}"), "")

    def test_02_phase_truth_preserves_exact_program_and_outcomes(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["proposal_chain"], {"before": 5670, "after": 5710})
        self.assertEqual(truth["proposal_rows"], 40)
        self.assertFalse(truth["universal_novelty_claim"])
        self.assertEqual(
            truth["outcomes"],
            {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        )
        self.assertEqual(
            truth["core_labels"], ["completed", "represented", "open_gap", "exact_gate"]
        )

    def test_03_retained_counts_are_exact_and_additive(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(
            truth["counts"],
            {
                "effective_negatives": 34088,
                "effective_methods": 20405,
                "failed_witnesses": 5909,
                "passing_witnesses": 7552,
                "open_gaps": 263,
                "exact_gates": 258,
            },
        )
        retained = load("closeout/retained-negative-register.json")
        self.assertTrue(retained["all_retained"])
        self.assertEqual(retained["erased"], 0)
        self.assertEqual(retained["x2_operational_failures"], 11)
        self.assertEqual(retained["final_operational_failures"], 3)
        self.assertEqual(retained["rejecting_mutations"], 160)

    def test_04_method_flow_keeps_invalid_aggregate_and_recovery_distinct(self):
        flow = load("closeout/method-flow-final.json")
        self.assertEqual(
            flow["evidence_aggregate_state"],
            "VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_AGGREGATE_SUCCESS_CREDIT",
        )
        self.assertEqual(flow["failed_evidence_junit_sha256"], "e99c7c98818222cd551a1e529dd4abaa4fa4813acf27fe67ed1127f49de68fb1")
        self.assertEqual(flow["dependency_recovery_junit_sha256"], "b5eeb7364508ca094c63652850b77be6d13a8276c6b017c2824d287d106286c1")
        self.assertTrue(flow["all_failures_retained"])

    def test_05_open_and_exact_gates_and_verdict_remain_visible(self):
        gates = load("closeout/exact-open-gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 263)
        self.assertEqual(gates["effective_exact_gates"], 258)
        self.assertEqual(gates["erased"], 0)
        self.assertTrue(gates["Maori_concepts_remain_under_Maori_authority"])
        self.assertEqual(gates["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_06_integrated_overview_exceeds_three_page_floor_and_keeps_boundaries(self):
        overview = (ROOT / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
        normalized = " ".join(overview.split())
        self.assertGreaterEqual(len(overview.split()), 900)
        for phrase in (
            "Freed ID and CBR Heart",
            "GMUT Mind",
            "THOS Body",
            "independent reproduction",
            "Theory-of-Everything proof",
            "Maori authority",
            "NOT_READY_FOR_STAGE_20",
        ):
            self.assertIn(phrase, normalized)

    def test_07_baton_integrity_and_word_bounds_are_exact(self):
        index = load("deck/baton-index.json")
        rel = index["path"]
        blob = git("show", f"HEAD:{rel}", binary=True).replace(b"\r\n", b"\n")
        self.assertEqual(len(blob), index["bytes"])
        self.assertEqual(hashlib.sha256(blob).hexdigest(), index["sha256"])
        text = blob.decode("utf-8")
        self.assertEqual(len(text.split()), index["words"])
        self.assertGreaterEqual(index["words"], 10_000)
        self.assertLessEqual(index["words"], 100_000)

    def test_08_baton_is_prepared_not_sent_and_route_is_single_valued(self):
        route = load("orchestration/route-state-final-candidate.json")
        baton = (ROOT / "handoffs/elaren-kestrel-v671-v5-activation-candidate.md").read_text(encoding="utf-8")
        self.assertEqual(route["prospective_successor_title"], "Elaren Kestrel")
        self.assertEqual(route["prospective_successor_phase"], "v671-v5")
        self.assertFalse(route["successor_contacted"])
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertIn("SENT_BY_EIREN_KESTREL = false", baton)
        self.assertIn("Tavian", baton)

    def test_09_privacy_and_python_security_receipts_are_bounded_and_valid(self):
        privacy = load("validation/final-privacy-scan.json")
        security = load("validation/final-python-security-review.json")
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(security["valid"])
        self.assertEqual(security["finding_count"], 0)

    def test_10_public_source_adapter_and_tool_boundaries_remain_zero_mutation(self):
        sources = load("reports/source-ledger.json")
        tools = load("orchestration/skill-runner-use-final.json")
        self.assertFalse(sources["adapter_enabled"])
        self.assertEqual(sources["network_calls"], 0)
        self.assertEqual(sources["rows_ingested"], 0)
        self.assertEqual(tools["package_bank_count"], 25)
        self.assertEqual(tools["installations_this_phase"], 0)
        self.assertEqual(tools["global_state_mutations"], 0)
        self.assertEqual(tools["global_skill_installations"], 0)

    def test_11_accessible_closeout_structure_and_reserved_evaluation_are_visible(self):
        report = (ROOT / "reports/accessible-closeout-report.html").read_text(encoding="utf-8")
        for phrase in (
            'lang="en"',
            'href="#main"',
            "<main",
            "<caption>",
            'scope="col"',
            "assistive-technology",
            "Maori-language",
            "NOT_READY_FOR_STAGE_20",
        ):
            self.assertIn(phrase, report)

    def test_12_final_staged_review_is_additive_and_preserves_prior_lifecycles(self):
        review = load("validation/final-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertTrue(review["x1_and_evidence_immutable"])
        self.assertEqual(review["out_of_scope"], [])
        self.assertEqual(review["deleted_paths"], [])

    def test_13_final_delta_manifest_replays_exact_final_blobs(self):
        manifest = load("validation/final-delta-manifest.json")
        self.assertEqual(manifest["hash_domain"], "normalized_lf_exact_staged_git_blob")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            blob = normalized_final_blob(entry["path"])
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])

    def test_14_final_owner_manifest_replays_exact_final_blobs(self):
        manifest = load("validation/final-owner-manifest.json")
        self.assertEqual(manifest["hash_domain"], "normalized_lf_exact_final_git_blob")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            blob = normalized_final_blob(entry["path"])
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])

    def test_15_seal_and_validation_prerequisites_remain_fail_closed(self):
        seal = load("seal/content-seal.json")
        prereq = load("final/final-validation-prerequisites.json")
        checklist = load("closeout/complete-incomplete-checklist.json")
        self.assertEqual(seal["evidence"], EVIDENCE)
        self.assertEqual(seal["exact_final"], "bind_from_external_exact_final_canonical_receipt")
        self.assertFalse(seal["content_mutation_after_seal_permitted"])
        self.assertTrue(prereq["one_canonical_invocation_maximum"])
        self.assertFalse(prereq["complete_repository_suite_required"])
        self.assertIn("real evidence and independent reproduction", checklist["incomplete"])
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()

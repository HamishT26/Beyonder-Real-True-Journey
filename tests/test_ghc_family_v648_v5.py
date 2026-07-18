from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v648_v5_definitions as d  # noqa: E402


PHASE = ROOT / "docs" / "sable-rook" / d.PHASE_SLUG
X1_COMMIT = "8ca83ea35ecbc72b1a993e04bde6a1dde096f4b9"


def load(relative: str):
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


class TestGhcFamilyV648V5Evidence(unittest.TestCase):
    def test_exact_ten_core_outcomes_and_noncompensation(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        truth = load("phase-truth-x2.json")
        expected = {
            "completed": 6,
            "represented": 2,
            "open_gap": 1,
            "exact_gate": 1,
        }
        self.assertEqual(ledger["count"], 10)
        self.assertEqual(ledger["outcomes"], expected)
        self.assertEqual(ledger["allowed_outcomes"], d.OUTCOME_CLASSES)
        self.assertEqual(truth["outcomes"], expected)
        self.assertTrue(ledger["noncompensation"])
        self.assertEqual(
            {row["observed_disposition"] for row in ledger["proposals"]},
            set(d.OUTCOME_CLASSES),
        )
        self.assertTrue(all(row["same_owner_only"] for row in ledger["proposals"]))
        self.assertTrue(
            all(not row["independent_reproduction"] for row in ledger["proposals"])
        )

    def test_ten_family_runners_reject_seventy_frozen_mutations(self) -> None:
        runners = load("tooling/x2-runner-ledger.json")
        negatives = load("validation/preregistered-synthetic-negatives.json")
        self.assertEqual(runners["count"], 10)
        self.assertEqual(runners["built_count"], 10)
        self.assertEqual(runners["invoked_count"], 10)
        self.assertEqual(runners["passed_count"], 10)
        self.assertEqual(negatives["count"], 70)
        self.assertEqual(negatives["executed_count"], 70)
        self.assertEqual(negatives["rejected_count"], 70)
        self.assertTrue(all(row["rejected"] for row in negatives["negatives"]))
        self.assertEqual(
            len({row["negative_id"] for row in negatives["negatives"]}), 70
        )
        for runner in runners["runners"]:
            witness = load(runner["witness"])
            self.assertTrue(witness["passed"])
            self.assertEqual(witness["mutation_count"], 7)
            self.assertEqual(witness["rejected_mutation_count"], 7)

    def test_empirical_participant_identity_and_authority_gates_stay_open(self) -> None:
        chandra = load("empirical/chandra-csc21-study-contract.json")["evidence"]
        thos = load("thos/newsroom-handover-contract.json")["evidence"]
        freed = load("freed-id/oauth-issuer-id-profile.json")["evidence"]
        cbr = load("cbr/newsroom-remedy-matrix.json")["evidence"]
        self.assertEqual(chandra["real_rows"], 0)
        self.assertEqual(chandra["likelihood_evaluations"], 0)
        self.assertEqual(chandra["posterior_samples"], 0)
        self.assertFalse(chandra["empirical_confirmation"])
        self.assertEqual(thos["real_publications"], 0)
        self.assertFalse(freed["production_identity"])
        self.assertFalse(cbr["real_editorial_decision"])
        self.assertFalse(cbr["source_disclosure_decision"])
        self.assertFalse(cbr["privacy_remedy_decision"])
        self.assertFalse(cbr["legal_interpretation"])
        self.assertFalse(cbr["cultural_ratification"])
        self.assertFalse(cbr["maori_authority_decision"])

    def test_expanded_portfolios_are_built_used_and_nondestructive(self) -> None:
        safe = load("approval-packets/x2-safe-now-ledger.json")
        candidates = load("prototypes/x2-candidate-ledger.json")
        skills = load("tooling/x2-skill-ledger.json")
        runners = load("tooling/x2-runner-ledger.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((safe["count"], safe["completed_count"]), (30, 30))
        self.assertEqual(
            (candidates["count"], candidates["built_count"], candidates["invoked_count"]),
            (20, 20, 20),
        )
        self.assertEqual(
            (
                skills["count"],
                skills["built_count"],
                skills["validated_count"],
                skills["used_count"],
            ),
            (20, 20, 20, 20),
        )
        self.assertEqual(skills["global_install_count"], 0)
        self.assertEqual(runners["count"], 10)
        self.assertEqual(
            (cleanup["count"], cleanup["completed_count"], cleanup["destructive_action_count"]),
            (30, 30, 0),
        )
        self.assertTrue(all(not row["destructive_action"] for row in cleanup["items"]))

    def test_twenty_phase_local_skills_exist_and_were_smoke_used(self) -> None:
        ledger = load("tooling/x2-skill-ledger.json")
        for row in ledger["skills"]:
            base = PHASE / "skills" / row["name"]
            self.assertTrue((base / "SKILL.md").is_file())
            self.assertTrue((base / "agents" / "openai.yaml").is_file())
            witness = load(row["witness"])
            self.assertTrue(witness["initialized"])
            self.assertTrue(witness["validated"])
            self.assertTrue(witness["smoke_used"])
            self.assertTrue(witness["rejecting_fixture_rejected"])
            self.assertFalse(witness["global_install"])

    def test_x1_tree_is_exactly_immutable(self) -> None:
        receipt = load("validation/x1-immutability-receipt.json")
        manifest = load("validation/x1-staged-manifest.json")
        paths = [row["path"] for row in manifest["entries"]] + manifest["self_exclusions"]
        self.assertEqual(receipt["x1_commit"], X1_COMMIT)
        self.assertEqual(receipt["checked_path_count"], len(paths))
        self.assertEqual(receipt["issues"], [])
        self.assertTrue(receipt["passed"])
        for relative in paths:
            self.assertEqual(
                git("rev-parse", f"{X1_COMMIT}:{relative}"),
                git("hash-object", f"--path={relative}", relative),
                relative,
            )

    def test_negatives_method_flow_and_gates_preserve_every_failure(self) -> None:
        negatives = load("retained-negative-register-x2.json")
        operational = load("validation/x2-operational-negatives.json")
        gates = load("exact-open-gate-register-x2.json")
        flow = load("method-flow/method-flow-ledger-x2.json")
        validation = load("method-flow/method-flow-validation-x2.json")
        self.assertEqual(negatives["inherited"], 4299)
        self.assertEqual(negatives["x1_operational"], 6)
        self.assertEqual(negatives["synthetic_executed_and_rejected"], 70)
        self.assertEqual(negatives["x2_operational"], 2)
        self.assertEqual(negatives["effective_total"], 4377)
        self.assertFalse(negatives["negative_erased"])
        self.assertEqual(operational["count"], 2)
        self.assertEqual(len(flow["methods"]), 8)
        self.assertEqual(len(flow["witnesses"]), 16)
        self.assertEqual(sum(row["result"] == "fail" for row in flow["witnesses"]), 8)
        self.assertEqual(sum(row["result"] == "pass" for row in flow["witnesses"]), 8)
        self.assertTrue(
            all(row["recommendation_state"] == "preferred" for row in flow["methods"])
        )
        self.assertTrue(validation["valid"])
        self.assertEqual(gates["effective_open_gaps"], 31)
        self.assertEqual(gates["effective_exact_gates"], 32)
        self.assertEqual(gates["silently_closed"], 0)

    def test_source_status_and_family_compatibility_remain_explicit(self) -> None:
        sources = load("sources/source-ledger-x2-verification.json")
        callers = load("tooling/caller-compatibility-receipt.json")
        self.assertEqual(
            sources["statuses"], {"current": 7, "stable": 10, "draft": 1, "watch": 1}
        )
        self.assertTrue(sources["official_or_primary_only"])
        self.assertEqual(sources["citations_as_observations"], 0)
        self.assertEqual(len(callers["new_family_current_runners"]), 10)
        self.assertEqual(callers["historical_names_deleted"], [])
        self.assertEqual(callers["historical_names_renamed"], [])
        self.assertFalse(callers["external_caller_completeness_claim"])

    def test_evidence_manifest_privacy_and_exact_review(self) -> None:
        manifest = load("validation/evidence-staged-manifest.json")
        privacy = load("validation/evidence-staged-privacy.json")
        review = load("validation/evidence-staged-review.json")
        self.assertEqual(manifest["hash_domain"], "git_hash_object_path_filtered_blob")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["self_exclusions"]), 3)
        for entry in manifest["entries"]:
            self.assertEqual(
                git("hash-object", f"--path={entry['path']}", entry["path"]),
                entry["git_blob"],
                entry["path"],
            )
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertEqual(len(privacy["pattern_classes"]), 5)
        self.assertEqual(review["x1_modified_paths"], [])
        self.assertEqual(review["out_of_scope_paths"], [])
        self.assertEqual(review["closeout_or_baton_paths"], [])
        self.assertTrue(review["passed"])

    def test_accessible_report_overview_and_document_caps(self) -> None:
        overview = (PHASE / "deliverables/v648-v5-integrated-overview.md").read_text(
            encoding="utf-8"
        )
        report = (PHASE / "deliverables/v648-v5-static-report.html").read_text(
            encoding="utf-8"
        )
        self.assertGreaterEqual(len(overview.split()), 1200)
        self.assertIn('href="#main"', report)
        self.assertIn("<caption>", report)
        self.assertIn('scope="col"', report)
        self.assertIn('scope="row"', report)
        self.assertIn("Manual keyboard", report)
        self.assertIn("affected-user evaluation remain reserved", report)
        for path in list(PHASE.rglob("*.md")) + list(PHASE.rglob("*.html")):
            self.assertLessEqual(
                len(path.read_text(encoding="utf-8").split()), 6000, path.as_posix()
            )

    def test_terminal_hold_and_environment_boundaries(self) -> None:
        truth = load("phase-truth-x2.json")
        receipt = load("evidence-receipt.json")
        wellbeing = load("wellbeing-check-x2.json")
        checklist = load("complete-incomplete-checklist-x2.json")
        self.assertFalse(truth["canonical_successful_pass_used"])
        self.assertFalse(truth["replay_used"])
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(receipt["full_suite_used"])
        self.assertFalse(receipt["replay_used"])
        self.assertEqual(wellbeing["host_changes"], 0)
        self.assertEqual(wellbeing["cross_platform_messages"], 0)
        self.assertEqual(wellbeing["desktop_updates"], 0)
        self.assertIn("final canonical validation", checklist["incomplete"])
        self.assertLess(len(list(PHASE.rglob("*"))), 15000)


if __name__ == "__main__":
    unittest.main()

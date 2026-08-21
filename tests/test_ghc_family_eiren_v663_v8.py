#!/usr/bin/env python3
"""Owner-scoped tests for Eiren Kestrel v663-v8 marquetry evidence."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.ghc_family_marquetry_evidence as evidence


SOURCE = "f60262e3b4b74aebf8ad8f8c5c591eb4e2c93c83"
X1 = "074607aa41bc2ac43782c8b126d8ba2f0330b070"
PHASE_ROOT = Path("docs/eiren-kestrel/v663-v8")
DECLARED_REPOSITORY_DEPENDENCIES = ["scripts/ghc_family_marquetry_evidence.py"]


def git(*args: str) -> str:
    result = subprocess.run(["git", "-C", str(ROOT), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    return result.stdout


def load_json(relative: str) -> dict:
    return json.loads((ROOT / PHASE_ROOT / relative).read_text(encoding="utf-8"))


class TestImmutableX1(unittest.TestCase):
    def test_x1_is_direct_child_of_source(self) -> None:
        self.assertEqual(git("rev-parse", f"{X1}^").strip(), SOURCE)

    def test_x1_contains_planning_only(self) -> None:
        paths = git("diff", "--name-only", SOURCE, X1).splitlines()
        self.assertEqual(len(paths), 13)
        self.assertTrue(all(path.startswith(f"{PHASE_ROOT.as_posix()}/x1/") for path in paths))
        self.assertFalse(any("/x2/" in path or path.startswith("scripts/") or path.startswith("tests/") for path in paths))

    def test_x1_program_counts(self) -> None:
        proposal = load_json("x1/proposal-freeze.json")
        self.assertEqual(proposal["inherited_frozen_baseline"], 3830)
        self.assertEqual(proposal["new_frozen_total"], 3850)
        self.assertEqual(len(proposal["selected_inherited"]), 20)
        self.assertEqual(len(proposal["new_proposals"]), 20)
        self.assertEqual(Counter(row["expected_disposition"] for row in proposal["new_proposals"]), Counter(completed=14, represented=4, open_gap=1, exact_gate=1))


class TestSyntheticFixtureContracts(unittest.TestCase):
    def test_case_identity_and_count(self) -> None:
        cases = evidence.fixture_cases()
        self.assertEqual(len(cases), 20)
        self.assertEqual(len({case["proposal_id"] for case in cases}), 20)
        self.assertEqual({case["validator"] for case in cases}, set(evidence.VALIDATORS))

    def test_all_positive_fixtures(self) -> None:
        for case in evidence.fixture_cases():
            with self.subTest(proposal_id=case["proposal_id"]):
                result = evidence.VALIDATORS[case["validator"]](case["positive"])
                self.assertTrue(result["valid"])
                self.assertEqual(result["proposal_id"], case["proposal_id"])
                self.assertEqual(result["real_world_rows"], 0)

    def test_four_rejecting_mutations_per_fixture(self) -> None:
        for case in evidence.fixture_cases():
            self.assertEqual(len(case["mutations"]), 4)
            validator = evidence.VALIDATORS[case["validator"]]
            for mutation in case["mutations"]:
                with self.subTest(proposal_id=case["proposal_id"], mutation=mutation["path"]):
                    with self.assertRaises((evidence.EvidenceError, KeyError, TypeError, IndexError)):
                        validator(evidence.apply_mutation(case["positive"], mutation))

    def test_mutation_receipt(self) -> None:
        receipt = evidence.mutation_receipt()
        self.assertTrue(receipt["valid"])
        self.assertEqual((receipt["positive_fixture_count"], receipt["mutation_count"], receipt["rejected_count"]), (20, 80, 80))
        self.assertTrue(all(row["failure_credit"] == 0 for row in receipt["records"]))

    def test_ten_runner_profiles(self) -> None:
        self.assertEqual(len(evidence.PROFILES), 10)
        for profile in evidence.PROFILES:
            with self.subTest(profile=profile):
                receipt = evidence.run_profile(profile)
                self.assertTrue(receipt["valid"])
                self.assertEqual(receipt["real_world_rows"], 0)

    def test_geometry_and_identity_boundaries(self) -> None:
        design = evidence.fixture_cases()[0]["positive"]
        self.assertEqual(evidence.validate_design_capsule(design)["proposal_id"], "EK6638-N001")
        graph = evidence.fixture_cases()[4]["positive"]
        self.assertTrue(evidence.validate_cut_path_graph(graph)["valid"])
        freed = evidence.fixture_cases()[13]["positive"]
        self.assertEqual(freed["real_keys"], 0)


class TestPhaseEvidencePacket(unittest.TestCase):
    def test_concrete_artifacts_exist(self) -> None:
        proposals = load_json("x1/proposal-freeze.json")["new_proposals"]
        expected = {(PHASE_ROOT / "x2" / artifact).as_posix() for proposal in proposals for artifact in proposal["concrete_artifacts"]}
        self.assertEqual(len(expected), 55)
        self.assertTrue(all((ROOT / path).is_file() for path in expected))

    def test_outcome_ledger(self) -> None:
        ledger = load_json("x2/outcome-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertEqual(len(ledger["new_outcomes"]), 20)
        self.assertEqual(Counter(row["outcome"] for row in ledger["new_outcomes"]), Counter(completed=14, represented=4, open_gap=1, exact_gate=1))
        self.assertTrue(all(row["real_world_rows"] == 0 for row in ledger["new_outcomes"]))
        self.assertTrue(all(row["automatic_completion_credit"] is False and row["current_completion_credit"] is False for row in ledger["inherited_revalidations"]))

    def test_package_review_is_no_install(self) -> None:
        packet = load_json("x2/package-candidate-review.json")
        self.assertTrue(packet["valid"])
        self.assertEqual({row["package"] for row in packet["candidates"]}, {"jsonschema", "pydantic", "networkx", "sympy"})
        self.assertTrue(all(row["decision"] == "not_installed_no_material_need" for row in packet["candidates"]))
        self.assertEqual(packet["install_actions"], 0)

    def test_sources_are_vocabulary_only(self) -> None:
        ledger = load_json("x2/source-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertGreaterEqual(len(ledger["sources"]), 10)
        self.assertTrue(all(row["use_class"] == "vocabulary_and_constraint_only" for row in ledger["sources"]))
        self.assertTrue(all(row["authority_conferred"] is False for row in ledger["sources"]))

    def test_phase_local_skills(self) -> None:
        skills = sorted((ROOT / PHASE_ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 10)
        for skill in skills:
            content = skill.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---\nname: "))
            self.assertIn("\ndescription: ", content)
            self.assertIn("relational working language", " ".join(content.split()))
            self.assertIn("NOT_READY_FOR_STAGE_20", content)

    def test_runner_profile_receipts(self) -> None:
        receipts = sorted((ROOT / PHASE_ROOT / "x2/runner-profiles").glob("*.json"))
        self.assertEqual(len(receipts), 10)
        for path in receipts:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(payload["valid"])
            self.assertEqual(payload["real_world_rows"], 0)

    def test_report_has_structural_landmarks_and_reservations(self) -> None:
        html = (ROOT / PHASE_ROOT / "x2/report/marquetry-evidence-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', "<main", "<h1", "<table", "<caption", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, html)
        for reservation in ("manual", "browser", "assistive-technology", "cognitive", "Māori-language", "affected-user"):
            self.assertIn(reservation.casefold(), html.casefold())

    def test_operational_method_flow_retains_post_x1_failures(self) -> None:
        flow = load_json("x2/operational-method-flow.json")
        self.assertTrue(flow["valid"])
        self.assertGreaterEqual(len(flow["records"]), 3)
        self.assertTrue(all(row["credit"] == 0 for row in flow["records"]))

    def test_x2_manifest_excludes_itself(self) -> None:
        manifest = load_json("validation/x2-content-manifest.json")
        paths = [row["path"] for row in manifest["entries"]]
        self.assertTrue(manifest["valid"])
        self.assertEqual(len(paths), len(set(paths)))
        self.assertNotIn(f"{PHASE_ROOT.as_posix()}/validation/x2-content-manifest.json", paths)


if __name__ == "__main__":
    unittest.main(verbosity=2)

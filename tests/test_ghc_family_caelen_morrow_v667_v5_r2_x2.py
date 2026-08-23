from __future__ import annotations

import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts.build_ghc_family_caelen_morrow_v667_v5_r2_x2 import PHASE_ROOT, ROOT, validate_contract


SOURCE = "1b1e453cb015aff20af3236bb64a8ec32b376702"
X1 = "5a5cf4859d791faff854292ed22a7a431ae4b620"


def load(relative: str) -> dict:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class CaelenMorrowV667V5R2X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.outcomes = load("x2/proposal-outcomes.json")
        cls.mutations = load("x2/rejecting-mutations.json")
        cls.evidence = load("evidence/immutable-evidence-candidate.json")
        cls.negatives = load("evidence/retained-negative-register.json")
        cls.methods = load("method-flow/x2-method-flow-ledger.json")
        cls.gaps = load("evidence/open-gap-register.json")
        cls.gates = load("evidence/exact-gate-register.json")
        cls.tools = load("x2/tooling/mandatory-tool-use-matrix.json")
        cls.installs = load("x2/tooling/install-integrity-receipt.json")
        cls.registry = load("x2/skill-runner-registry.json")
        cls.flashcards = load("x2/flashcards/execution-receipts.json")

    def test_twenty_positive_contracts_validate(self) -> None:
        self.assertEqual(20, len(self.outcomes["outcomes"]))
        for outcome in self.outcomes["outcomes"]:
            contract = load(f"x2/proposals/{outcome['proposal_id'].casefold()}/contract.json")
            self.assertEqual([], validate_contract(contract), outcome["proposal_id"])
            self.assertTrue(contract["synthetic_only"])
            self.assertEqual(0, contract["external_write_count"])
            self.assertIsNone(contract["authority_claim"])

    def test_rejecting_mutations_and_exact_outcomes(self) -> None:
        self.assertEqual(100, self.mutations["mutation_count"])
        self.assertEqual(0, self.mutations["accepted_mutation_count"])
        self.assertTrue(all(not row["accepted"] and row["validator_failures"] for row in self.mutations["mutations"]))
        expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
        self.assertEqual(expected, self.outcomes["counts"])
        self.assertEqual(expected, dict(Counter(row["final_disposition"] for row in self.outcomes["outcomes"])))
        self.assertEqual("NOT_READY_FOR_STAGE_20", self.outcomes["terminal_verdict"])

    def test_all_twenty_five_tools_have_bounded_witnesses(self) -> None:
        self.assertEqual(25, self.tools["tool_count"])
        self.assertEqual(12, self.tools["inherited_tool_count"])
        self.assertEqual(10, self.tools["new_foundational_count"])
        self.assertEqual(3, self.tools["current_phase_new_count"])
        self.assertTrue(self.tools["all_used"])
        self.assertTrue(all(row["used"] and row["exit_code"] == 0 and row["bounded_witness"] for row in self.tools["rows"]))
        self.assertEqual(25, len({row["name"] for row in self.tools["rows"]}))

    def test_thirteen_exact_packages_are_installed_and_bounded(self) -> None:
        self.assertEqual(13, self.installs["installed_count"])
        self.assertEqual(6, self.installs["python_wheel_sha256_match_count"])
        self.assertEqual(7, self.installs["npm_dist_integrity_match_count"])
        self.assertTrue(self.installs["lifecycle_scripts_disabled"])
        self.assertEqual(0, self.installs["hooks_installed"])
        self.assertEqual(0, self.installs["publishing_events"])
        self.assertEqual(0, self.installs["credential_events"])
        self.assertEqual(0, self.installs["python_direct_audit_known_vulnerabilities"])
        self.assertEqual(0, self.installs["node_exact_fixture_audit_known_vulnerabilities"])

    def test_profiles_and_cli_updates_are_d_first_and_user_scoped(self) -> None:
        profile = load("x2/tooling/profile-migration-receipt.json")
        self.assertEqual("D:", profile["npm_prefix_drive"])
        self.assertEqual("D:", profile["canonical_powershell_profile_drive"])
        self.assertEqual("C:", profile["minimal_bootstrap_drive"])
        self.assertEqual(0, profile["legacy_c_npm_prefix_entries"])
        self.assertTrue(profile["fresh_powershell_7_profile_loaded"])
        self.assertTrue(profile["fresh_windows_powershell_5_profile_loaded"])
        updates = load("x2/tooling/cli-update-receipt.json")
        self.assertEqual(["12.0.2", "7.6.5 side-by-side user-scope", "0.149.0"], [row["after"] for row in updates["updates"]])
        self.assertTrue(all(row["passed"] for row in updates["updates"]))
        self.assertFalse(updates["windows_operating_system_updated"])
        self.assertFalse(updates["codex_desktop_updated"])
        self.assertFalse(updates["elevation_used"])

    def test_advisory_failure_and_narrow_recovery_remain_visible(self) -> None:
        recovery = load("x2/tooling/advisory-recovery-receipt.json")
        self.assertEqual("PYSEC-2026-2132", recovery["advisory"])
        self.assertEqual(0, recovery["failed_attempt_credit"])
        self.assertEqual("click==8.4.2", recovery["verified_current_pin"])
        self.assertEqual(0, recovery["recovery_audit_known_vulnerability_count"])
        self.assertFalse(recovery["broader_tools_replayed"])
        self.assertTrue(recovery["failure_retained"])

    def test_mandatory_skills_phase_skills_and_runners_are_used(self) -> None:
        mandatory = load("x2/mandatory-skill-use-receipt.json")
        self.assertEqual(21, mandatory["required_count"])
        self.assertEqual(21, mandatory["used_count"])
        self.assertTrue(mandatory["all_used"])
        self.assertEqual(10, self.registry["skill_count"])
        self.assertEqual(10, self.registry["runner_count"])
        self.assertEqual(10, self.registry["skill_smoke_passes"])
        self.assertEqual(10, self.registry["runner_smoke_passes"])
        self.assertEqual(0, self.registry["global_skill_install_count"])

    def test_flashcard_packet_and_rejecting_mutations(self) -> None:
        self.assertTrue(all(row["passed"] for row in self.flashcards.values()))
        self.assertGreaterEqual(self.flashcards["build"]["result"]["card_count"], 200)
        self.assertGreaterEqual(self.flashcards["build"]["result"]["section_count"], 10)
        mutation = load("x2/flashcards/mutation-receipt.json")
        self.assertEqual(mutation["mutation_count"], mutation["rejected_count"])
        self.assertTrue(all(row["rejected"] for row in mutation["cases"]))

    def test_method_flow_and_negative_accounting(self) -> None:
        self.assertEqual(329, self.methods["phase_method_count"])
        self.assertEqual(13737, self.methods["effective_method_count"])
        self.assertEqual(189, self.methods["phase_failed_witness_count"])
        self.assertEqual(329, self.methods["phase_bounded_passing_witness_count"])
        self.assertTrue(self.methods["valid"])
        self.assertTrue(all(not row["failure_erased"] for row in self.methods["rows"]))
        self.assertEqual(189, self.negatives["phase_additive_count"])
        self.assertEqual(27905, self.negatives["effective_count"])
        self.assertEqual(0, self.negatives["failure_erased_count"])
        self.assertEqual(196, self.gaps["effective_count"])
        self.assertEqual(194, self.gates["effective_count"])
        self.assertFalse(self.gates["new_rows"][0]["executed"])

    def test_zero_real_world_and_authority_counts(self) -> None:
        for key in ["real_people", "real_organizations", "real_private_packages", "real_production_releases", "credentials", "publishing_events", "automatic_updates", "external_writes"]:
            self.assertEqual(0, self.evidence[key], key)
        self.assertTrue(self.evidence["same_owner_only"])
        self.assertFalse(self.evidence["independent_reproduction"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", self.evidence["terminal_verdict"])

    def test_accessible_report_has_structure_and_reservations(self) -> None:
        report = (PHASE_ROOT / "reports" / "accessible-report.html").read_text(encoding="utf-8")
        for fragment in ["<!doctype html>", '<html lang="en">', "Skip to main content", '<main id="main">', "<caption>", 'scope="col"', "NOT_READY_FOR_STAGE_20"]:
            self.assertIn(fragment, report)
        self.assertIn("assistive-technology", report)
        self.assertIn("Māori-language", report)

    def test_x1_commit_tree_remains_immutable(self) -> None:
        changed = subprocess.check_output(["git", "-C", str(ROOT), "diff", "--name-only", X1, "--", "docs/caelen-morrow/v667-v5-r2/x1"], text=True, encoding="utf-8").strip().splitlines()
        self.assertEqual([], changed)

    def test_phase_json_parses_and_caps_hold(self) -> None:
        files = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
        self.assertLessEqual(len(files), 2000)
        json_files = [path for path in files if path.suffix == ".json"]
        self.assertGreaterEqual(len(json_files), 100)
        for path in json_files:
            json.loads(path.read_text(encoding="utf-8"))
        for path in [p for p in files if p.suffix.lower() in {".md", ".html", ".txt"}]:
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)

    def test_source_and_head_lifecycle_are_exact(self) -> None:
        self.assertEqual(X1, subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip())
        self.assertEqual(SOURCE, subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", f"{X1}^"], text=True).strip())


if __name__ == "__main__":
    unittest.main()

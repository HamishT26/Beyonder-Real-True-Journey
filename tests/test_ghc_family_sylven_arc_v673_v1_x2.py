"""Owner-scoped immutable-evidence tests for Sylven Arc v673-v1 x2."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "docs" / "sylven-arc" / "v673-v1"
X1 = OWNER / "x1"
X2 = OWNER / "x2"
X1_COMMIT = "606f6b7afef6d4368e1b34d128e57fc061629b05"
EXPECTED = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
RUNNERS = [
    "ghc_family_flag_identity.py", "ghc_family_flag_edge_topology.py",
    "ghc_family_flag_seam_relation.py", "ghc_family_flag_attachment_abstention.py",
    "ghc_family_flag_material_vacancy.py", "ghc_family_flag_condition_separation.py",
    "ghc_family_flag_provenance_correction.py", "ghc_family_flag_privacy_access.py",
    "ghc_family_flag_workload_handover.py", "ghc_family_flag_flashcard_projection.py",
]


def load(relative: str):
    return json.loads((X2 / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


class TestSylvenArcV673V1X2(unittest.TestCase):
    def test_01_x2_begins_at_exact_x1(self):
        self.assertEqual(git("rev-parse", "HEAD"), X1_COMMIT)

    def test_02_immutable_x1_has_no_checkout_diff(self):
        self.assertEqual(git("diff", X1_COMMIT, "--", "docs/sylven-arc/v673-v1/x1"), "")

    def test_03_closeout_is_absent(self):
        self.assertFalse((OWNER / "closeout").exists())
        self.assertFalse((OWNER / "final").exists())

    def test_04_exactly_forty_contracts_exist(self):
        contracts = sorted((X2 / "contracts").glob("*.json"))
        self.assertEqual(len(contracts), 40)
        self.assertTrue(all(json.loads(path.read_text(encoding="utf-8"))["synthetic"] for path in contracts))

    def test_05_outcomes_are_exact(self):
        row = load("proposal-outcomes.json")
        self.assertEqual(row["counts"], EXPECTED)
        self.assertEqual(Counter(item["outcome"] for item in row["rows"]), Counter(EXPECTED))

    def test_06_core_vocabulary_is_closed(self):
        self.assertEqual(set(load("proposal-outcomes.json")["counts"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_07_mutations_all_executed_and_rejected(self):
        row = load("rejecting-mutation-ledger.json")
        self.assertEqual((row["planned"], row["executed"], row["rejected"], row["accepted"]), (160, 160, 160, 0))
        self.assertTrue(all(item["rejected"] and not item["accepted"] for item in row["rows"]))

    def test_08_mutation_matrix_is_four_per_proposal(self):
        rows = load("rejecting-mutation-ledger.json")["rows"]
        self.assertEqual(Counter(item["proposal_id"] for item in rows), Counter({f"SA6731-N{i:03d}": 4 for i in range(1, 41)}))

    def test_09_positive_controls_pass_36_of_36(self):
        row = load("positive-control-ledger.json")
        self.assertEqual((row["planned"], row["passed"]), (36, 36))
        self.assertTrue(all(item["accepted"] for item in row["rows"]))

    def test_10_contracts_use_zero_real_rows_and_actions(self):
        for path in (X2 / "contracts").glob("*.json"):
            row = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual((row["real_people"], row["real_objects"], row["observations"], row["measurements"], row["external_actions"], row["network_calls"]), (0, 0, 0, 0, 0, 0))

    def test_11_twenty_skills_have_three_files_each(self):
        skills = sorted(path for path in (X2 / "skills").iterdir() if path.is_dir())
        self.assertEqual(len(skills), 20)
        self.assertTrue(all((root / "SKILL.md").exists() and (root / "agents" / "openai.yaml").exists() and (root / "references" / "contract.md").exists() for root in skills))

    def test_12_skill_frontmatter_names_match_directories(self):
        for root in (X2 / "skills").iterdir():
            if root.is_dir():
                text = (root / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith(f"---\nname: {root.name}\n"), root.name)

    def test_13_skill_positive_and_negative_smokes_pass(self):
        row = load("skills/skill-smoke-receipt.json")
        self.assertEqual((row["skill_count"], row["positive_passes"], row["negative_rejections"]), (20, 20, 20))
        self.assertEqual(row["global_install_count"], 0)

    def test_14_default_codepage_failure_is_retained(self):
        row = load("skills/official-validation-failed-receipt.json")
        self.assertEqual(row["credit"], 0)
        self.assertEqual(row["failure_class"], "WINDOWS_DEFAULT_CODEPAGE_UTF8_DECODE_FAILURE")
        self.assertFalse(row["private_paths_retained"])

    def test_15_official_skill_utf8_recovery_passes_20(self):
        row = load("skills/official-validation-receipt.json")
        self.assertTrue(row["valid"])
        self.assertEqual((row["skill_count"], row["valid_count"]), (20, 20))
        self.assertTrue(all(item["python_utf8_mode"] and item["complete_read"] for item in row["rows"]))

    def test_16_ten_runner_smokes_pass_both_paths(self):
        row = load("tooling/runner-smoke-receipt.json")
        self.assertTrue(row["valid"])
        self.assertEqual(row["runner_count"], 10)
        self.assertTrue(all(item["positive_exit"] == 0 and item["negative_exit"] == 2 for item in row["rows"]))

    def test_17_runner_cli_paths_remain_live(self):
        for name in RUNNERS:
            good = subprocess.run([sys.executable, str(ROOT / "scripts" / name), "--fixture", "valid"], cwd=ROOT, capture_output=True, text=True)
            bad = subprocess.run([sys.executable, str(ROOT / "scripts" / name), "--fixture", "invalid"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual((good.returncode, bad.returncode), (0, 2), name)

    def test_18_three_substantive_tools_pass_both_paths(self):
        row = load("tooling/substantive-tool-receipt.json")
        self.assertEqual(row["tool_count"], 3)
        self.assertTrue(row["valid"])
        self.assertTrue(all(item["positive_valid"] and item["negative_rejected"] for item in row["rows"]))

    def test_19_all_new_python_compiles(self):
        paths = [ROOT / "scripts" / "build_ghc_family_sylven_arc_v673_v1_x2.py"]
        paths.extend(ROOT / "scripts" / name for name in RUNNERS)
        paths.extend(ROOT / "scripts" / name for name in ["ghc_family_flag_contract.py", "ghc_family_flag_flashcards.py", "ghc_family_flag_evidence.py"])
        for path in paths:
            compile(path.read_text(encoding="utf-8"), path.as_posix(), "exec")

    def test_20_flashcard_deck_has_four_tiers_and_13_modules(self):
        row = load("flashcards/deck.json")
        self.assertEqual(row["tier_order"], ["freed_id", "pillar", "practice", "task"])
        self.assertEqual(row["section_count"], 13)
        self.assertEqual(len(row["cards"]), 60)
        self.assertEqual(set(card["tier"] for card in row["cards"]), {"freed_id", "pillar", "practice", "task"})

    def test_21_flashcard_hashes_and_parents_validate(self):
        row = load("flashcards/validation.json")
        self.assertTrue(row["valid"])
        self.assertTrue(row["acyclic_by_tier_order"])
        self.assertEqual(row["issues"], [])

    def test_22_portfolios_respect_execution_and_holds(self):
        row = load("portfolio-completion.json")["completion"]
        self.assertEqual(row["safe_now"]["completed"], 60)
        self.assertEqual(row["candidates"]["completed"], 30)
        self.assertEqual(row["clean_fix_refine"]["completed"], 60)
        self.assertEqual(row["exact_approval"]["completed"], 0)
        self.assertEqual(row["blocked"]["completed"], 0)
        self.assertEqual(row["successor_recommendations_completion_credit"], 0)

    def test_23_zero_call_adapter_stays_open(self):
        row = load("zero-call-adapter.json")
        self.assertFalse(row["enabled"])
        self.assertEqual((row["network_calls"], row["downloads"], row["rows"]), (0, 0, 0))
        self.assertEqual(row["status"], "open_gap")

    def test_24_authority_packet_stays_exact_gated(self):
        row = load("authority-gate.json")
        self.assertEqual(row["status"], "exact_gate")
        self.assertTrue(row["held_unexecuted"])
        self.assertIn("Māori concepts remain under Māori authority", row["boundary"])

    def test_25_method_flow_counts_and_pairs_are_exact(self):
        row = load("method-flow-evidence.json")
        self.assertEqual(row["counts"]["methods"], 208)
        self.assertEqual(row["counts"]["witnesses"], 416)
        self.assertEqual(row["counts"]["witness_results"], {"fail": 208, "pass": 208})
        self.assertEqual(row["counts"]["state_events"], 624)

    def test_26_effective_counts_are_additive(self):
        row = load("evidence-counts.json")
        self.assertEqual(row["activation_baseline"]["effective_negatives"], 36161)
        self.assertEqual(row["counts"], {"proposal_chain": 6270, "effective_negatives": 36369, "effective_methods": 22697, "failed_witnesses": 8030, "bounded_passing_witnesses": 10260, "open_gaps": 293, "exact_gates": 286})
        self.assertFalse(row["source_repository_seal_rewritten"])

    def test_27_evidence_receipt_has_no_external_action(self):
        row = load("evidence-receipt.json")
        self.assertEqual((row["api_calls"], row["external_actions"]), (0, 0))
        self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_28_owner_file_and_document_guards_hold(self):
        files = [path for path in OWNER.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)
        for path in files:
            if path.suffix.lower() in {".json", ".md", ".html", ".txt", ".py", ".yaml"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path.as_posix())

    def test_29_overview_preserves_all_nonpromotion_boundaries(self):
        text = (X2 / "evidence-overview.md").read_text(encoding="utf-8")
        for phrase in ("participant-free proxy", "Māori concepts remain under Māori authority", "not independent reproduction", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(phrase, text)

    def test_30_no_successor_or_real_world_action_is_claimed(self):
        text = (X2 / "evidence-overview.md").read_text(encoding="utf-8")
        self.assertIn("creates no closeout or successor delivery", text)
        self.assertIn("No real person, flag, textile", text)


if __name__ == "__main__":
    unittest.main()

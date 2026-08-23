from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_ghc_family_elaren_kestrel_v667_v7_x1.py"
SPEC = importlib.util.spec_from_file_location("elaren_v667_v7_x1", BUILDER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load Elaren x1 builder")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ElarenV667V7X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not mod.PHASE_ROOT.is_dir():
            raise RuntimeError("run the x1 builder before the x1 test module")
        cls.docs = {path.relative_to(ROOT).as_posix(): json.loads(path.read_text(encoding="utf-8")) for path in mod.PHASE_ROOT.rglob("*.json")}

    def doc(self, relative: str):
        return self.docs[f"{mod.REL_PHASE_ROOT}/{relative}"]

    def test_01_exact_source_constants(self):
        self.assertEqual(mod.SOURCE_SHA, "dc8d91294b7656ad5e9961bba93ff759af20846c")
        self.assertEqual(mod.SOURCE_X1_SHA, "0ff9e3058d4df62d30035b7d9f5d5ce0939f10a2")
        self.assertEqual(mod.SOURCE_EVIDENCE_SHA, "942eda86e745da93ece372d89870e052361b039c")

    def test_02_corpus_reconstructs_4490_occurrences(self):
        corpus, construction = mod.build_corpus()
        self.assertEqual(len(corpus), 4490)
        self.assertTrue(construction)
        self.assertEqual(construction[-1]["ending_count"], 4490)

    def test_03_programme_is_twenty_new_and_twenty_selected(self):
        freeze = self.doc("x1/proposal-freeze.json")
        self.assertEqual(len(freeze["new_proposals"]), 20)
        self.assertEqual(len(freeze["selected_inherited"]), 20)
        self.assertEqual(freeze["new_frozen_total"], 4510)

    def test_04_expected_dispositions_are_exact(self):
        rows = self.doc("x1/proposal-freeze.json")["new_proposals"]
        self.assertEqual(Counter(row["expected_disposition"] for row in rows), Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}))
        self.assertTrue(all(row["expected_disposition"] in mod.ALLOWED_OUTCOMES for row in rows))

    def test_05_proposals_have_complete_preregistration(self):
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "current_official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        rows = self.doc("x1/proposal-freeze.json")["new_proposals"]
        self.assertTrue(all(required <= set(row) for row in rows))
        self.assertTrue(all(len(row["preregistered_mutations"]) == 5 for row in rows))

    def test_06_x1_has_no_observed_outcomes(self):
        freeze = self.doc("x1/proposal-freeze.json")
        self.assertFalse(freeze["outcomes_observed"])
        self.assertEqual(freeze["x2_implementation_count"], 0)
        self.assertTrue(all(not row["outcomes_observed"] for row in freeze["new_proposals"] + freeze["selected_inherited"]))

    def test_07_selected_rows_have_zero_elaren_credit(self):
        rows = self.doc("x1/proposal-freeze.json")["selected_inherited"]
        self.assertTrue(all(row["elaren_novelty_credit"] == 0 and row["elaren_completion_credit"] == 0 and row["automatic_completion_credit"] == 0 for row in rows))

    def test_08_novelty_audit_passes(self):
        novelty = self.doc("x1/novelty-audit.json")
        self.assertTrue(novelty["valid"])
        self.assertEqual(novelty["corpus_row_count"], 4490)
        self.assertEqual(novelty["new_frozen_total"], 4510)
        self.assertEqual(novelty["exact_title_collisions"], [])
        self.assertEqual(novelty["pair_collisions_at_or_above_threshold"], [])

    def test_09_portfolio_counts_are_exact(self):
        portfolio = self.doc("x1/portfolio-freeze.json")
        expected = {"owner_safe_now": 30, "successor_safe_now_recommendations": 20, "owner_candidates": 15, "successor_candidate_recommendations": 15, "owner_skill_ideas": 10, "successor_skill_recommendations": 10, "owner_runner_ideas": 10, "successor_runner_recommendations": 10, "owner_clean_fix_refine": 30, "successor_clean_fix_refine_recommendations": 30, "exact_approval_packets": 10, "blocked_packets": 5}
        self.assertEqual({key: len(portfolio[key]) for key in expected}, expected)

    def test_10_tool_plan_is_three_new_over_41_inherited(self):
        tools = self.doc("x1/toolchain-install-plan.json")
        self.assertEqual(tools["inherited_current_tool_count"], 41)
        self.assertEqual([row["tool"] for row in tools["new_tools"]], ["interrogate", "import-linter", "pyroma"])
        self.assertEqual((tools["x1_download_count"], tools["x1_install_count"], tools["x1_smoke_count"]), (0, 0, 0))

    def test_11_source_ledger_is_public_vocabulary_only(self):
        ledger = self.doc("x1/source-ledger.json")
        self.assertEqual(ledger["source_count"], 18)
        self.assertTrue(ledger["public_vocabulary_only"])
        self.assertFalse(ledger["authority_conferred"])

    def test_12_three_source_truth_layers_remain_distinct(self):
        charter = self.doc("x1/phase-charter.json")
        self.assertEqual(charter["source_repository_evidence_seal"]["effective_negatives"], 28166)
        self.assertEqual(charter["source_committed_final"]["effective_negatives"], 28168)
        self.assertEqual(charter["activation_baseline"]["effective_negatives"], 28175)

    def test_13_startup_failures_are_retained(self):
        flow = self.doc("x1/startup-method-flow.json")
        self.assertEqual(flow["failure_count"], 15)
        self.assertTrue(all(row["credit"] == 0 for row in flow["failures"]))

    def test_14_all_mandatory_skills_are_recorded(self):
        adoption = self.doc("x1/mandatory-skill-adoption.json")
        self.assertEqual(adoption["required_count"], 21)
        self.assertTrue(all(row["entrypoint_read_through_eof"] and row["required_references_read_through_eof"] for row in adoption["skills"]))

    def test_15_later_lifecycle_paths_are_absent(self):
        for name in ("x2", "evidence", "closeout", "seal", "route"):
            self.assertFalse((mod.PHASE_ROOT / name).exists())

    def test_16_overview_is_three_page_planning_context(self):
        content = (mod.PHASE_ROOT / "x1/x1-overview.md").read_text(encoding="utf-8")
        words = content.split()
        self.assertGreaterEqual(len(words), 900)
        self.assertIn("NOT_READY_FOR_STAGE_20", content)

    def test_17_manifest_replays_exact_bytes(self):
        manifest = self.doc("validation/x1-content-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes()
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(mod.hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_18_privacy_scan_has_zero_candidates(self):
        candidates = []
        for path in mod.phase_owned_paths():
            candidates.extend(mod.privacy_candidates(path, path.read_text(encoding="utf-8")))
        self.assertEqual(candidates, [])

    def test_19_source_is_ancestor_and_history_is_merge_free(self):
        ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", mod.SOURCE_SHA, "HEAD"], cwd=ROOT, check=False)
        merges = subprocess.run(["git", "rev-list", "--merges", f"{mod.SOURCE_SHA}..HEAD", "--count"], cwd=ROOT, check=True, capture_output=True, text=True)
        self.assertEqual(ancestor.returncode, 0)
        self.assertEqual(merges.stdout.strip(), "0")

    def test_20_builder_validation_passes(self):
        receipt = mod.validate_tree()
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["privacy_candidates"], 0)
        self.assertEqual(receipt["x2_paths"], 0)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v645-v1"
sys.path.insert(0, str(ROOT / "scripts"))


def load_module(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODEL = load_module("scripts/ghc_family_v645_v1_model.py", "v644_v8_model")
DEFINITIONS = load_module("scripts/ghc_family_v645_v1_x1_definitions.py", "v644_v8_definitions")
LFS = load_module("scripts/ghc_family_git_lfs_boundary.py", "ghc_family_git_lfs_boundary_test")


class TestV644V8Models(unittest.TestCase):
    def test_all_ten_models_have_seven_matched_mutations(self) -> None:
        self.assertEqual(10, len(MODEL.BASE_CASES))
        for proposal in DEFINITIONS.PROPOSALS:
            result = MODEL.proposal_cases(proposal["proposal_id"])
            self.assertEqual(7, result["case_count"])
            self.assertEqual(7, result["matched_count"])

    def test_completed_and_proxy_baselines_pass(self) -> None:
        for proposal_id in {
            "V6451-P01", "V6451-P02", "V6451-P04", "V6451-P05",
            "V6451-P07", "V6451-P08", "V6451-P09", "V6451-P10",
        }:
            self.assertTrue(MODEL.proposal_cases(proposal_id)["baseline_accept"], proposal_id)

    def test_open_and_exact_baselines_do_not_cross_gate(self) -> None:
        self.assertFalse(MODEL.proposal_cases("V6451-P03")["baseline_accept"])
        self.assertFalse(MODEL.proposal_cases("V6451-P06")["baseline_accept"])

    def test_open_gap_cannot_be_promoted_by_single_field(self) -> None:
        row = dict(MODEL.BASE_CASES["V6451-P03"])
        row["official_real_rows"] = 1
        self.assertFalse(MODEL.evaluate("V6451-P03", row))

    def test_exact_gate_cannot_be_promoted_by_single_authority_flag(self) -> None:
        row = dict(MODEL.BASE_CASES["V6451-P06"])
        row["competent_legal_authority"] = True
        self.assertFalse(MODEL.evaluate("V6451-P06", row))

    def test_psyche_conversion_rejected(self) -> None:
        row = dict(MODEL.BASE_CASES["V6451-P09"])
        row["psyche_conversion"] = True
        self.assertFalse(MODEL.evaluate("V6451-P09", row))

    def test_unknown_proposal_rejected(self) -> None:
        with self.assertRaises(KeyError):
            MODEL.proposal_cases("missing")

    def test_lfs_classifier_distinguishes_present_and_missing_objects(self) -> None:
        pointer = f"version {LFS.VERSION}\noid sha256:{'a' * 64}\nsize 42\n".encode()
        present = LFS.classify_bytes(path="fixtures/a.bin", data=pointer, object_present=True)
        missing = LFS.classify_bytes(path="fixtures/a.bin", data=pointer, object_present=False)
        self.assertEqual("valid_lfs_pointer_object_present", present["classification"])
        self.assertEqual("valid_lfs_pointer_object_missing", missing["classification"])
        self.assertTrue(present["accepted"])
        self.assertFalse(missing["accepted"])

    def test_lfs_classifier_rejects_malformed_and_out_of_root(self) -> None:
        pointer = f"version {LFS.VERSION}\noid sha1:{'a' * 40}\nsize 42\n".encode()
        malformed = LFS.classify_bytes(path="fixtures/a.bin", data=pointer, object_present=True)
        outside = LFS.classify_bytes(path="../outside.bin", data=pointer, object_present=True)
        self.assertEqual("malformed_lfs_pointer", malformed["classification"])
        self.assertEqual("rejected_out_of_root", outside["classification"])
        self.assertFalse(malformed["accepted"] or outside["accepted"])

    def test_lfs_classifier_is_network_free_for_ordinary_content(self) -> None:
        row = LFS.classify_bytes(path="README.md", data=b"ordinary content\n")
        self.assertEqual("ordinary_tracked_content", row["classification"])
        self.assertFalse(row["network_fetch_performed"])


class TestV644V8Artifacts(unittest.TestCase):
    def load(self, relative: str):
        return json.loads((PHASE / relative).read_text(encoding="utf-8"))

    def test_x2_distribution_and_cases(self) -> None:
        ledger = self.load("x2-proposal-ledger.json")
        self.assertEqual(
            {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
            ledger["observed_distribution"],
        )
        self.assertEqual(70, ledger["total_case_count"])
        self.assertEqual(70, ledger["total_matched_count"])

    def test_all_deliverables_exist(self) -> None:
        for proposal in DEFINITIONS.PROPOSALS:
            for relative in proposal["deliverables"]:
                self.assertTrue((PHASE / relative).is_file(), relative)

    def test_negative_retention(self) -> None:
        register = self.load("retained-negative-register.json")
        self.assertEqual(1750, register["inherited_effective_count"])
        self.assertEqual(6, register["x1_operational_count"])
        self.assertGreaterEqual(register["x2_operational_count"], 4)
        self.assertEqual(70, register["new_synthetic_count"])
        self.assertEqual(
            register["inherited_effective_count"]
            + register["x1_operational_count"]
            + register["x2_operational_count"]
            + register["new_synthetic_count"],
            register["negative_count"],
        )
        self.assertEqual(register["negative_count"], len(register["negatives"]))
        self.assertEqual([], register["duplicate_negative_ids"])
        self.assertTrue(register["all_retained"])

    def test_gate_counts_remain_open(self) -> None:
        gates = self.load("exact-open-gate-register.json")
        self.assertEqual(5, gates["open_gap_count"])
        self.assertEqual(6, gates["exact_gate_count"])
        self.assertTrue(gates["none_silently_closed"])

    def test_protected_claims_false(self) -> None:
        evidence = self.load("evidence/evidence-ledger.json")
        self.assertTrue(all(value is False for value in evidence["protected_claims"].values()))
        self.assertTrue(all(value == 0 for value in evidence["real_or_external_counts"].values()))
        self.assertEqual("NOT_READY_FOR_STAGE_20", evidence["terminal_verdict"])

    def test_static_report_has_visible_equivalents(self) -> None:
        report = (PHASE / "deliverables/v645-v1-static-report.html").read_text(encoding="utf-8")
        for marker in [
            'href="#main"', '<main id="main"', ":focus-visible", 'role="img"',
            "<figcaption>", 'id="distribution-long"', "Underlying disposition data",
        ]:
            self.assertIn(marker, report)
        self.assertNotIn("::before", report)
        self.assertNotIn("::after", report)

    def test_overview_is_three_page_equivalent(self) -> None:
        words = (PHASE / "deliverables/v645-v1-final-integrated-overview.md").read_text(encoding="utf-8").split()
        self.assertGreaterEqual(len(words), 1200)

    def test_phase_truth_has_no_outbound_action(self) -> None:
        truth = self.load("phase-truth.json")
        self.assertEqual("Freed ID/CBR Heart", truth["primary_focus"])
        self.assertEqual(0, truth["outbound_message_count"])
        self.assertEqual(0, truth["successor_task_count"])
        self.assertEqual("ACTIVE_SOLO; PREPARED_NOT_SENT", truth["route_state"])
        self.assertFalse(truth["full_repository_suite_run"])

    def test_source_status_vocabulary_preserved(self) -> None:
        source = self.load("sources/source-ledger.json")
        self.assertEqual(225, source["effective_source_count"])
        self.assertTrue(set(source["effective_status_counts"]) <= {"current", "stable", "draft", "watch"})

    def test_dispositions_use_only_allowed_vocabulary(self) -> None:
        ledger = self.load("x2-proposal-ledger.json")
        observed = Counter(row["observed_disposition"] for row in ledger["rows"])
        self.assertEqual(Counter(ledger["observed_distribution"]), observed)
        self.assertTrue(set(observed) <= {"completed", "represented", "open_gap", "exact_gate"})

    def test_method_flow_retains_recovery_boundaries(self) -> None:
        method = self.load("method-flow/method-flow-state.json")
        states = {row["method_id"]: row["recommendation_state"] for row in method["methods"]}
        self.assertEqual("preferred", states["v6451-m07"])
        self.assertEqual("preferred", states["v6451-m10"])
        self.assertNotIn("candidate", states.values())

    def test_manifest_is_same_owner_only(self) -> None:
        manifest = self.load("reproduction/evidence-manifest.json")
        self.assertTrue(manifest["same_owner_repeatability_only"])
        self.assertFalse(manifest["independent_team_reproduction"])


if __name__ == "__main__":
    unittest.main()

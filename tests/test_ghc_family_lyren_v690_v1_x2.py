from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/lyren-moss/v690-v1"
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_error_control_cli import run as run_cli
from ghc_family_error_control_x2 import run


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class LyrenV690V1X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = load(BASE / "plan/new-proposals.json")["proposals"][100:]
        cls.results = load(BASE / "x2/results.json")["results"]
        cls.candidates = load(BASE / "x2/candidate-subjects.json")["records"]

    def test_exact_frozen_results(self):
        self.assertEqual(len(self.plan), 100)
        self.assertEqual(len(self.results), 100)
        for proposal, report in zip(self.plan, self.results):
            request = copy.deepcopy(proposal["request"])
            before = copy.deepcopy(request)
            self.assertEqual(run(request), proposal["expected"], proposal["proposal_id"])
            self.assertEqual(request, before, proposal["proposal_id"])
            self.assertEqual(report["observed"], proposal["expected"])
            self.assertTrue(report["passed"])

    def test_all_candidates_are_retained_and_refused(self):
        self.assertEqual(len(self.candidates), 100)
        by_id = {row["proposal_id"]: row for row in self.candidates}
        for proposal in self.plan:
            subject = copy.deepcopy(proposal["candidate_subject"])
            before = copy.deepcopy(subject)
            self.assertEqual(run(subject), proposal["candidate_expected"])
            self.assertEqual(subject, before)
            self.assertEqual(by_id[proposal["proposal_id"]]["original_success_credit"], 0)
            self.assertTrue(by_id[proposal["proposal_id"]]["refusal_check_passed"])

    def test_outcome_distribution_uses_only_core_labels(self):
        counts = Counter(row["outcome"] for row in self.results)
        self.assertEqual(counts, {"completed": 80, "represented": 10, "open_gap": 5, "exact_gate": 5})
        self.assertEqual(set(counts), {"completed", "represented", "open_gap", "exact_gate"})

    def test_crc_append_verify_roundtrip(self):
        for data, polynomial in [("0", "1011"), ("1101", "1011"), ("101010101", "1101")]:
            appended = run({"operation": "crc_append", "payload": {"data": data, "polynomial": polynomial}})
            checked = run({"operation": "crc_verify", "payload": {"codeword": appended["value"]["codeword"], "polynomial": polynomial}})
            self.assertTrue(checked["value"]["valid"])
            self.assertFalse(appended["value"]["cryptographic"])
            self.assertFalse(checked["value"]["repair_performed"])

    def test_interleave_inverse(self):
        for bits, rows in [("0011", 2), ("001101", 2), ("001100110011", 3)]:
            interleaved = run({"operation": "row_interleave", "payload": {"bits": bits, "rows": rows}})
            recovered = run({"operation": "row_deinterleave", "payload": {"codeword": interleaved["value"]["codeword"], "rows": rows}})
            self.assertEqual(recovered["value"]["bits"], bits)

    def test_crc_and_checksum_are_not_cryptographic(self):
        crc = run({"operation": "crc_append", "payload": {"data": "1101", "polynomial": "1011"}})
        checksum = run({"operation": "xor_checksum", "payload": {"bytes": [1, 2, 3]}})
        self.assertFalse(crc["value"]["cryptographic"])
        self.assertFalse(checksum["value"]["cryptographic"])

    def test_erasure_inventory_does_not_repair(self):
        result = run({"operation": "erasure_inventory", "payload": {"values": [1, None, 0, None]}})
        self.assertEqual(result["value"]["erasures"], [1, 3])
        self.assertFalse(result["value"]["repair_performed"])

    def test_sequence_gaps_and_duplicates_remain_distinct(self):
        result = run({"operation": "sequence_gap_map", "payload": {"sequence": [1, 1, 3]}})
        self.assertEqual(result["value"]["missing"], [2])
        self.assertEqual(result["value"]["duplicates"], [1])
        self.assertFalse(result["value"]["strictly_increasing"])

    def test_provenance_digest_does_not_establish_identity(self):
        result = run({"operation": "provenance_digest", "payload": {"record": {"synthetic": True}, "source_sha256": "0" * 64}})
        self.assertFalse(result["value"]["identity_established"])
        self.assertRegex(result["value"]["binding_sha256"], r"^[0-9a-f]{64}$")

    def test_accessibility_and_authority_reservations(self):
        accessible = run({"operation": "accessible_error_summary", "payload": {"detected": 4, "corrected": 2, "uncorrectable": 1, "unknown": 1}})
        self.assertEqual(accessible["outcome"], "represented")
        self.assertEqual(accessible["value"]["manual_evaluation"], "reserved")
        gap = run({"operation": "coding_evidence_reservation", "payload": {"obligation": "real channel evidence", "kind": "scientific_evidence", "evidence": None, "authority": None}})
        gate = run({"operation": "coding_evidence_reservation", "payload": {"obligation": "operational release", "kind": "competent_authority", "evidence": None, "authority": None}})
        self.assertEqual(gap["outcome"], "open_gap")
        self.assertEqual(gate["outcome"], "exact_gate")

    def test_unknown_fields_and_bad_shapes_are_refused(self):
        subjects = [
            {"operation": "xor_checksum", "payload": {"bytes": [1], "authority": True}},
            {"operation": "row_interleave", "payload": {"bits": "101", "rows": 2}},
            {"operation": "crc_append", "payload": {"data": "10", "polynomial": "1010"}},
            {"operation": "erasure_inventory", "payload": {"values": [0, "?"]}},
        ]
        for subject in subjects:
            before = copy.deepcopy(subject)
            result = run(subject)
            self.assertFalse(result["ok"])
            self.assertEqual(result["original_success_credit"], 0)
            self.assertEqual(subject, before)

    def test_combined_cli_preserves_x1_and_x2_compatibility(self):
        x1 = run_cli({"operation": "even_parity_append", "payload": {"bits": "101"}})
        x2 = run_cli({"operation": "xor_checksum", "payload": {"bytes": [1, 2, 3]}})
        self.assertEqual(x1["value"]["codeword"], "1010")
        self.assertEqual(x2["value"]["checksum"], 0)

    def test_refinements_are_lossless_zero_credit(self):
        rows = load(BASE / "x2/refinements.json")["records"]
        self.assertEqual(len(rows), 100)
        self.assertTrue(all(row["lossless"] for row in rows))
        self.assertTrue(all(row["novelty_credit"] == 0 and row["execution_credit"] == 0 for row in rows))
        self.assertTrue(all(not row["host_cleanup"] for row in rows))

    def test_package_comparisons(self):
        receipt = load(BASE / "x2/toolchain/package-comparisons.json")
        self.assertEqual(receipt["count"], 30)
        self.assertTrue(receipt["all_passed"])
        self.assertEqual(Counter(row["package"] for row in receipt["records"]), {"bitstring": 10, "reedsolo": 10, "crccheck": 10})

    def test_skill_and_runner_validation(self):
        self.assertTrue(load(BASE / "x2/skills-validation.json")["all_passed"])
        self.assertTrue(load(BASE / "x2/tooling/runner-smokes.json")["all_passed"])
        self.assertTrue(load(BASE / "x2/global-skills-validation.json")["all_passed"])
        self.assertTrue(load(BASE / "x2/global-runners-validation.json")["all_passed"])
        self.assertEqual(len(list((BASE / "x2/skills").iterdir())), 10)
        self.assertEqual(len(list((BASE / "x2/global-skills").iterdir())), 5)

    def test_method_flow_counts_and_unique_ids(self):
        ledger = load(BASE / "x2/method-flow.json")
        self.assertEqual(ledger["counts"], {"methods": 13, "witnesses": 445, "failed_witnesses": 105, "passing_witnesses": 340, "retained_negatives": 105})
        self.assertEqual(len({row["method_id"] for row in ledger["methods"]}), 13)
        self.assertEqual(len({row["witness_id"] for row in ledger["witnesses"]}), 445)
        self.assertTrue(all(not row["independent_reproduction"] for row in ledger["witnesses"]))

    def test_negative_index_and_counterexamples(self):
        index = load(BASE / "x2/negative-index.json")
        self.assertEqual(index["count"], 105)
        self.assertTrue(index["all_original_success_credit_zero"])
        self.assertTrue(all(row["original_success_credit"] == 0 and row["retained"] for row in index["records"]))
        counterexamples = load(BASE / "x2/research/counterexamples.json")
        self.assertEqual(counterexamples["count"], 2)
        self.assertFalse(counterexamples["new_fundamental_laws_claimed"])

    def test_four_tier_deck_is_content_addressed_and_parented(self):
        index = load(BASE / "x2/deck/deck-index.json")
        self.assertEqual(index["counts"], {"1": 1, "2": 3, "3": 4, "4": 205})
        self.assertEqual(len(index["order"]), 213)
        cards = {path.stem: load(path) for path in (BASE / "x2/deck/cards").glob("*.json")}
        self.assertEqual(set(cards), set(index["order"]))
        for card_id, card in cards.items():
            body = dict(card)
            body.pop("card_id")
            self.assertEqual(card_id, "ghc-card-" + hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()[:24])
            if card["tier"] == 1:
                self.assertEqual(card["parent_ids"], [])
            else:
                self.assertEqual(len(card["parent_ids"]), 1)
                self.assertIn(card["parent_ids"][0], cards)
                self.assertEqual(cards[card["parent_ids"][0]]["tier"], card["tier"] - 1)

    def test_meta_tool_catalogue(self):
        catalogue = load(BASE / "x2/meta-tool-catalogue.json")
        self.assertEqual(catalogue["schema"], "ghc.family.meta-tool-box.catalogue.v2")
        self.assertEqual(catalogue["card_count"], 40)
        self.assertEqual(len({row["card_id"] for row in catalogue["cards"]}), 40)
        self.assertTrue(all(not row["repository_scan"] and not row["cross_lane_scan"] for row in catalogue["cards"]))

    def test_completion_and_cumulative_truth(self):
        ledger = load(BASE / "x2/completion-ledger.json")
        self.assertEqual(ledger["counts"], {"completed": 80, "represented": 10, "open_gap": 5, "exact_gate": 5})
        self.assertEqual(ledger["supplementary_counts"], {"represented": 5})
        truth = load(BASE / "x2/phase-truth.json")
        self.assertEqual(truth["cumulative_before_late_overlays"], {"effective_negatives": 960, "methods": 79, "direct_witnesses": 2453, "failed_witnesses": 671, "passing_witnesses": 1782})
        self.assertEqual(truth["cumulative_after_late_overlay"], {"effective_negatives": 967, "methods": 80, "direct_witnesses": 2467, "failed_witnesses": 678, "passing_witnesses": 1789})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_post_validation_overlay_and_global_promotion(self):
        overlay = load(BASE / "x2/post-validation-overlay.json")
        self.assertEqual(len(overlay["retained_negatives"]), 7)
        self.assertEqual(overlay["effective_counts"], {"methods": 14, "retained_negatives": 112, "witnesses": 459, "failed_witnesses": 112, "passing_witnesses": 347})
        promotion = load(BASE / "x2/tooling/global-promotion.json")
        self.assertTrue(promotion["passed"])
        self.assertTrue(promotion["no_overwrite"])
        self.assertEqual(promotion["counts"], {"skills": 5, "public_runners": 5, "dependency_modules": 2})
        self.assertTrue(all(row["byte_parity"] and row["validated"] for row in promotion["skills"]))
        self.assertTrue(all(row["byte_parity"] and row["positive_passed"] and row["adverse_passed"] for row in promotion["runners"]))

    def test_manifest_raw_bytes(self):
        manifest = load(BASE / "x2/manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            path = ROOT / entry["path"]
            self.assertTrue(path.is_file(), entry["path"])
            self.assertEqual(path.stat().st_size, entry["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry["sha256"])


if __name__ == "__main__":
    unittest.main()

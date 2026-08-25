from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_elowen_cairn_v669_v2_archive as archive
import ghc_family_lutherie_contracts as contracts


class ElowenCairnV669V2X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.phase_root = ROOT / archive.REL_PHASE_ROOT
        cls.proposals = contracts.load_proposals()
        cls.execution = contracts.execute_contracts(cls.proposals)

    def read_json(self, relative: str) -> dict:
        return json.loads((self.phase_root / relative).read_text(encoding="utf-8"))

    def test_01_lifecycle_starts_at_immutable_x1(self) -> None:
        branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        parent = subprocess.check_output(["git", "rev-parse", f"{head}^"], cwd=ROOT, text=True).strip()
        self.assertEqual(branch, archive.BRANCH)
        self.assertEqual(head, archive.FROZEN_X1)
        self.assertEqual(parent, archive.SOURCE_FINAL)

    def test_02_exact_forty_x1_proposals_are_consumed(self) -> None:
        self.assertEqual(len(self.proposals), 40)
        self.assertEqual(len({row["proposal_id"] for row in self.proposals}), 40)
        self.assertTrue(all(row["x1_completion_credit"] == 0 for row in self.proposals))

    def test_03_outcomes_match_preregistration(self) -> None:
        self.assertEqual(
            self.execution["outcome_counts"],
            {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        )
        self.assertEqual(set(self.execution["outcome_counts"]), set(archive.ALLOWED_OUTCOMES))

    def test_04_all_positive_contracts_pass_the_bounded_checker(self) -> None:
        positive = self.execution["positive"]
        self.assertEqual(len(positive), 40)
        self.assertTrue(all(row["result"]["accepted"] for row in positive))

    def test_05_positive_contracts_preserve_zero_real_world_counts(self) -> None:
        for row in self.execution["positive"]:
            fixture = row["fixture"]
            self.assertTrue(fixture["synthetic_only"])
            self.assertTrue(all(value == 0 for value in fixture["counts"].values()))
            self.assertEqual(fixture["external_actions"], [])
            self.assertEqual(fixture["protected_claims"], [])
            self.assertEqual(fixture["authority_status"], "vacant")

    def test_06_completion_credit_tracks_only_completed_disposition(self) -> None:
        for row in self.execution["positive"]:
            fixture = row["fixture"]
            expected = 1 if fixture["declared_outcome"] == "completed" else 0
            self.assertEqual(fixture["bounded_completion_credit"], expected)
            self.assertEqual(row["result"]["completion_credit"], expected)

    def test_07_gmut_surfaces_are_typed_zero_data_obligations(self) -> None:
        rows = [row["fixture"] for row in self.execution["positive"] if "gmut_boundary" in row["fixture"]]
        self.assertGreaterEqual(len(rows), 3)
        for fixture in rows:
            self.assertTrue(fixture["gmut_boundary"]["typed_obligations_only"])
            self.assertEqual(sum(value for key, value in fixture["gmut_boundary"].items() if key != "typed_obligations_only"), 0)

    def test_08_thos_surfaces_remain_zero_participant_proxies(self) -> None:
        rows = [row["fixture"] for row in self.execution["positive"] if "thos_boundary" in row["fixture"]]
        self.assertEqual(len(rows), 2)
        for fixture in rows:
            self.assertTrue(fixture["thos_boundary"]["proxy_only"])
            self.assertEqual(fixture["thos_boundary"]["participants_or_operators"], 0)
            self.assertEqual(fixture["thos_boundary"]["effectiveness_estimates"], 0)

    def test_09_freed_id_surfaces_remain_zero_key_and_nonproduction(self) -> None:
        rows = [row["fixture"] for row in self.execution["positive"] if "freed_id_boundary" in row["fixture"]]
        self.assertEqual(len(rows), 2)
        for fixture in rows:
            self.assertTrue(fixture["freed_id_boundary"]["synthetic_nonproduction"])
            self.assertEqual(fixture["freed_id_boundary"]["keys"], 0)
            self.assertEqual(fixture["freed_id_boundary"]["proofs"], 0)

    def test_10_open_gaps_are_zero_call_or_zero_evaluation(self) -> None:
        by_slug = {row["fixture"]["semantic_slug"]: row["fixture"] for row in self.execution["positive"]}
        adapter = by_slug["loc-instrument-zero-call"]["adapter"]
        evaluation = by_slug["human-evaluation-gap"]["evaluation"]
        self.assertEqual((adapter["network_calls"], adapter["downloads"], adapter["rows"]), (0, 0, 0))
        self.assertEqual((evaluation["participants"], evaluation["professionals"]), (0, 0))

    def test_11_exact_gates_remain_unexecuted_and_stage20_locked(self) -> None:
        by_slug = {row["fixture"]["semantic_slug"]: row["fixture"] for row in self.execution["positive"]}
        gate = by_slug["instrument-authority-gate"]["gate"]
        stage = by_slug["stage20-nonpromotion"]
        self.assertEqual((gate["authorities_present"], gate["decisions"]), (0, 0))
        self.assertTrue(all(value == 0 for value in stage["evidence_vector"].values()))
        self.assertEqual(stage["terminal_verdict"], archive.TERMINAL_VERDICT)

    def test_12_all_160_preregistered_mutations_are_rejected(self) -> None:
        rows = self.execution["mutations"]
        self.assertEqual(len(rows), 160)
        self.assertEqual(Counter(row["observed"] for row in rows), {"reject": 160})
        self.assertTrue(all(row["completion_credit"] == 0 and row["retained_failed_witness"] for row in rows))

    def test_13_each_mutation_has_its_exact_stable_reason(self) -> None:
        for row in self.execution["mutations"]:
            self.assertIn(row["mutation_kind"], row["reasons"])
            self.assertEqual(row["expected"], "reject")

    def test_14_proposal_and_mutation_identifiers_are_unique(self) -> None:
        mutation_ids = [row["mutation_id"] for row in self.execution["mutations"]]
        proposal_ids = [row["proposal_id"] for row in self.proposals]
        self.assertEqual(len(mutation_ids), len(set(mutation_ids)))
        self.assertEqual(len(proposal_ids), len(set(proposal_ids)))

    def test_15_proposal_cards_and_mutation_shards_are_exact(self) -> None:
        self.assertEqual(len(list((self.phase_root / "x2/proposals").glob("*.json"))), 40)
        self.assertEqual(len(list((self.phase_root / "x2/cards").glob("*.json"))), 40)
        shards = sorted((self.phase_root / "x2/mutations").glob("*.json"))
        self.assertEqual(len(shards), 8)
        self.assertEqual(sum(json.loads(path.read_text(encoding="utf-8"))["count"] for path in shards), 160)

    def test_16_portfolio_execution_preserves_exact_counts_and_labels(self) -> None:
        for category, expected in archive.PORTFOLIO_COUNTS.items():
            ledger = self.read_json(f"x2/portfolio-execution/{category}.json")
            self.assertEqual(ledger["count"], expected)
            self.assertTrue(set(ledger["outcome_counts"]) <= set(archive.ALLOWED_OUTCOMES))
            self.assertTrue(all(row["x2_external_actions"] == 0 for row in ledger["rows"]))

    def test_17_exact_and_blocked_portfolios_remain_held(self) -> None:
        for category in ("exact_approval", "blocked"):
            ledger = self.read_json(f"x2/portfolio-execution/{category}.json")
            self.assertEqual(ledger["outcome_counts"], {"exact_gate": ledger["count"]})
            self.assertTrue(all(row["execution_state"] == "held_unexecuted" for row in ledger["rows"]))
            self.assertTrue(all(row["completion_credit"] == 0 for row in ledger["rows"]))

    def test_18_twenty_owner_local_skills_quick_validate_and_smoke_read(self) -> None:
        receipt = self.read_json("tools/skill-smoke-receipt.json")
        self.assertEqual(receipt["count"], 20)
        self.assertTrue(all(row["quick_validation"] == "PASS" for row in receipt["rows"]))
        self.assertTrue(all(row["smoke_use"] == "PASS_OWNER_LOCAL_READ" for row in receipt["rows"]))
        self.assertTrue(all(not row["globally_installed"] for row in receipt["rows"]))

    def test_19_ten_family_runners_smoke_use_without_external_action(self) -> None:
        receipt = self.read_json("tools/runner-smoke-receipt.json")
        self.assertEqual(receipt["count"], 10)
        self.assertTrue(all(row["smoke_status"] == "PASS" and row["return_code"] == 0 for row in receipt["rows"]))
        self.assertTrue(all(row["external_actions"] == 0 and row["network_calls"] == 0 for row in receipt["rows"]))

    def test_20_sixty_clean_fix_refine_checks_complete_boundedly(self) -> None:
        ledger = self.read_json("x2/portfolio-execution/clean_fix_refine.json")
        self.assertEqual(ledger["count"], 60)
        self.assertEqual(ledger["outcome_counts"], {"completed": 60})
        self.assertTrue(all(row["completion_credit"] == 1 for row in ledger["rows"]))

    def test_21_method_flow_pairs_every_operation_and_mutation(self) -> None:
        ledger = self.read_json("method-flow/evidence-ledger.json")
        expected = len(archive.STARTUP_FAILURES) + len(archive.X2_FAILURES) + 160
        self.assertEqual(len(ledger["methods"]), expected)
        self.assertEqual(Counter(row["result"] for row in ledger["witnesses"]), {"fail": expected, "pass": expected})
        witness_ids = {row["witness_id"] for row in ledger["witnesses"]}
        self.assertTrue(all(set(row["failed_witness_ids"] + row["validation_witness_ids"]) <= witness_ids for row in ledger["methods"]))

    def test_22_evidence_truth_arithmetic_and_gate_registers_are_exact(self) -> None:
        truth = self.read_json("x2/phase-truth-evidence.json")
        self.assertEqual(truth["effective_negatives"], 30717)
        self.assertEqual(truth["methods"], 16823)
        self.assertEqual(truth["failed_witnesses"], 2538)
        self.assertEqual(truth["passing_witnesses"], 3615)
        self.assertEqual(truth["open_gaps"], 227)
        self.assertEqual(truth["exact_gates"], 222)
        self.assertEqual(truth["terminal_verdict"], archive.TERMINAL_VERDICT)

    def test_23_evidence_manifests_replay_exact_staged_git_blobs(self) -> None:
        for relative in ("validation/evidence-owner-manifest.json", "validation/evidence-delta-manifest.json"):
            manifest = self.read_json(relative)
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            for row in manifest["entries"]:
                data = subprocess.check_output(["git", "show", ":" + row["path"]], cwd=ROOT)
                oid = subprocess.check_output(["git", "hash-object", "--stdin"], cwd=ROOT, input=data).decode().strip()
                self.assertEqual(len(data), row["bytes"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])
                self.assertEqual(oid, row["git_blob_oid"])

    def test_24_privacy_security_and_ceiling_boundaries_hold(self) -> None:
        owner_files = archive.phase_owner_files()
        self.assertLessEqual(len(owner_files), archive.FILE_CEILING)
        private_patterns = [
            re.compile(r"\b019[0-9a-f]{5}-[0-9a-f-]{20,}\b", re.I),
            re.compile(r"(?i)(?:password|secret|api[_-]?key|bearer|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
            re.compile(r"(?i)(?:task|thread|session|resume)[_-]?id\s*[:=]\s*['\"][^'\"]+"),
            re.compile(r"[A-Za-z]:\\(?:Users|GHC-Archives)\\"),
        ]
        hits = []
        for path in owner_files:
            if path.suffix.lower() in {".json", ".md", ".html", ".txt", ".py"}:
                text = path.read_text(encoding="utf-8")
                hits.extend((path, pattern.pattern) for pattern in private_patterns if pattern.search(text))
                if path.suffix.lower() in {".md", ".html", ".txt"}:
                    self.assertLessEqual(len(re.findall(r"\S+", text)), archive.DOCUMENT_WORD_CEILING)
            if path.suffix == ".py":
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        self.assertFalse(any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords))
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Owner-scoped tests for Lyren Moss v679-v4 x2 evidence."""

from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_lyren_moss_v679_v4_core import (  # noqa: E402
    CHANNELS,
    LABELS,
    MUTATIONS,
    contract_from_proposal,
    mutate,
    privacy_candidates,
    read_json,
    runner_smoke,
    validate_accessibility,
    validate_columns,
    validate_contract,
    validate_correction,
    validate_provenance,
    validate_sequence,
    validate_skill,
)


PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
X1 = PHASE / "x1"
X2 = PHASE / "x2"


class CoreContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.proposals = read_json(X1 / "new-proposal-freeze.json")["proposals"]
        cls.contract = contract_from_proposal(cls.proposals[0])

    def test_positive_contract_accepts(self) -> None:
        self.assertEqual(validate_contract(self.contract), [])

    def test_all_preregistered_mutations_reject(self) -> None:
        for kind in MUTATIONS:
            with self.subTest(kind=kind):
                self.assertTrue(validate_contract(mutate(self.contract, kind)))

    def test_channel_vacancy_accepts(self) -> None:
        result = validate_columns([{"channel": channel, "state": "not_observed", "value": None, "unit": None} for channel in CHANNELS])
        self.assertTrue(result["accepted"])

    def test_numeric_channel_rejects(self) -> None:
        result = validate_columns([{"channel": "temperature", "state": "observed", "value": 20.0, "unit": "degC"}])
        self.assertFalse(result["accepted"])

    def test_sequence_positive_and_gap_negative(self) -> None:
        self.assertTrue(validate_sequence([{"sequence": 1, "record_id": "SYNTH-MONITOR-SEQ-001"}])["accepted"])
        self.assertFalse(validate_sequence([{"sequence": 2, "record_id": "SYNTH-MONITOR-SEQ-001"}])["accepted"])

    def test_correction_preserves_original(self) -> None:
        result = validate_correction(
            {"record_id": "SYNTH-MONITOR-CORR-001"},
            {"record_id": "SYNTH-MONITOR-CORR-002", "supersedes": "SYNTH-MONITOR-CORR-001", "reason": "synthetic correction"},
        )
        self.assertTrue(result["accepted"])
        self.assertEqual(result["records_retained"], 2)

    def test_provenance_refuses_agent_nodes(self) -> None:
        result = validate_provenance([{"id": "SYNTH-PROV-AGENT-001", "type": "Agent"}], [])
        self.assertFalse(result["accepted"])

    def test_accessibility_is_structural_only(self) -> None:
        html = "<main><h1>x</h1><table><caption>x</caption><th scope='col'>x</th></table><details>x</details><style>@media print{}</style></main>"
        result = validate_accessibility(html)
        self.assertTrue(result["accepted"])
        self.assertFalse(result["complete_accessibility_assurance"])

    def test_privacy_fixture_is_clear(self) -> None:
        self.assertEqual(privacy_candidates("SYNTH-MONITOR-LOG-LM6794-N001"), [])

    def test_all_runner_smokes_meet_expectations(self) -> None:
        names = ("contract", "column", "sequence", "correction", "provenance", "accessibility", "privacy", "mutation", "method_flow", "terminal")
        for name in names:
            for invalid in (False, True):
                with self.subTest(name=name, invalid=invalid):
                    self.assertTrue(runner_smoke(name, invalid)["expectation_met"])


class BuiltArtifactTests(unittest.TestCase):
    def test_contract_and_receipt_counts(self) -> None:
        self.assertEqual(len(list((X2 / "contracts").glob("*.json"))), 60)
        self.assertEqual(len(list((X2 / "evidence").glob("*-receipt.json"))), 60)

    def test_contracts_revalidate(self) -> None:
        for path in sorted((X2 / "contracts").glob("*.json")):
            with self.subTest(path=path.name):
                self.assertEqual(validate_contract(read_json(path)), [])

    def test_outcome_labels_and_counts(self) -> None:
        value = read_json(X2 / "proposal-outcomes.json")
        counts = Counter(row["outcome"] for row in value["outcomes"])
        self.assertEqual(set(counts), LABELS)
        self.assertEqual(dict(counts), {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})

    def test_mutation_ledger_is_complete(self) -> None:
        value = read_json(X2 / "mutation-ledger.json")
        self.assertEqual(value["count"], 240)
        self.assertEqual(value["rejected"], 240)
        self.assertEqual(value["completion_credit"], 0)

    def test_positive_controls_are_bounded(self) -> None:
        value = read_json(X2 / "positive-controls.json")
        self.assertEqual(value["count"], 60)
        self.assertEqual(value["passed"], 60)
        self.assertTrue(all(row["broader_credit"] == 0 for row in value["controls"]))

    def test_portfolio_floors_and_gates(self) -> None:
        value = read_json(X2 / "portfolio-execution.json")
        self.assertEqual(value["safe_now"]["executed"], 120)
        self.assertEqual(value["candidates"]["represented_or_executed"], 80)
        self.assertEqual(value["exact_approval"]["count"], 20)
        self.assertEqual(value["blocked"]["count"], 10)
        self.assertIn("unexecuted", value["exact_approval"]["execution_state"])

    def test_clean_fix_refine_counts(self) -> None:
        value = read_json(X2 / "clean-fix-refine-execution.json")
        self.assertEqual(value["owner_completed"], 100)
        self.assertEqual(len(value["successor_recommendations"]), 30)
        self.assertEqual(value["successor_executed_by_lyren"], 0)

    def test_owner_local_skills_validate(self) -> None:
        paths = sorted((X2 / "skills").iterdir())
        self.assertEqual(len(paths), 20)
        for path in paths:
            with self.subTest(path=path.name):
                self.assertTrue(validate_skill(path)["accepted"])

    def test_flashcard_index_is_content_addressed(self) -> None:
        value = read_json(X2 / "flashcards" / "index.json")
        self.assertEqual(value["card_count"], 135)
        self.assertEqual(len(value["entries"]), 135)
        self.assertEqual(len({row["content_sha256"] for row in value["entries"]}), 135)

    def test_toolchain_is_verify_only(self) -> None:
        value = read_json(X2 / "toolchain-verification.json")
        self.assertEqual(value["target_count"], 25)
        self.assertEqual(value["installations"], 0)
        self.assertEqual(value["available"] + value["represented_missing"], 25)

    def test_primary_sources_are_official_or_primary(self) -> None:
        value = read_json(X2 / "source-ledger.json")
        self.assertEqual(value["source_count"], 9)
        self.assertTrue(all(row["url"].startswith("https://") for row in value["sources"]))
        self.assertEqual(value["real_world_rows"], 0)

    def test_privacy_scan_has_no_confirmed_candidates(self) -> None:
        value = read_json(X2 / "privacy-scan.json")
        self.assertEqual(value["classes"], 5)
        self.assertEqual(value["confirmed_candidates"], 0)
        self.assertFalse(value["complete_privacy_assurance"])

    def test_phase_truth_preserves_terminal_boundary(self) -> None:
        value = read_json(X2 / "phase-truth.json")
        self.assertEqual(value["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(value["independent_reproduction"])
        self.assertFalse(value["full_repository_suite"])
        self.assertEqual(value["real_world_rows"], 0)
        self.assertEqual(value["external_actions"], 0)

    def test_route_remains_held(self) -> None:
        value = read_json(X2 / "route-hold.json")
        self.assertEqual(value["current_state"], "HELD_DURING_X2")
        self.assertFalse(value["precontact"])
        self.assertEqual(value["send_count"], 0)

    def test_every_json_parses(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 290)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

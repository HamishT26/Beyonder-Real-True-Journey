from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v681-v3"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_COMMIT = "77bf12d03946985f1dabb22b5c0606a8762f8ed8"
BRANCH = "codex/GHC-Family/lyren-moss-v681-v3-full-tools"
OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class LyrenMossV681V3X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = load(X1 / "new-proposal-freeze.json")
        cls.evidence = load(X2 / "proposal-evidence.json")
        cls.positives = load(X2 / "positive-controls.json")
        cls.mutations = load(X2 / "mutation-results.json")
        cls.truth = load(X2 / "phase-truth.json")

    def test_exact_x1_head_and_branch_before_evidence_commit(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD"), X1_COMMIT)
        self.assertEqual(git("branch", "--show-current"), BRANCH)

    def test_x1_manifest_is_immutable(self) -> None:
        receipt = load(X2 / "x1-immutability-receipt.json")
        self.assertTrue(receipt["head_matches"])
        self.assertTrue(receipt["planning_only"])
        self.assertEqual(receipt["manifest_mismatches"], [])
        self.assertEqual(receipt["entry_count"], 20)

    def test_proposal_identity_and_outcomes(self) -> None:
        frozen_ids = [row["proposal_id"] for row in self.freeze["proposals"]]
        evidence_ids = [row["proposal_id"] for row in self.evidence["outcomes"]]
        self.assertEqual(evidence_ids, frozen_ids)
        counts = Counter(row["outcome"] for row in self.evidence["outcomes"])
        self.assertEqual(counts, Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}))
        self.assertEqual(set(counts), OUTCOMES)

    def test_positive_controls(self) -> None:
        self.assertEqual(self.positives["accepted"], 60)
        self.assertEqual(self.positives["real_rows"], 0)
        self.assertEqual(self.positives["external_actions"], 0)
        self.assertTrue(all(row["result"]["accepted"] for row in self.positives["controls"]))

    def test_mutations_are_all_rejected_and_retained(self) -> None:
        self.assertEqual(self.mutations["executed"], 300)
        self.assertEqual(self.mutations["rejected"], 300)
        self.assertTrue(self.mutations["zero_completion_credit"])
        self.assertFalse(self.mutations["failure_erasure"])
        self.assertTrue(all(row["observed"] == "rejected" for row in self.mutations["mutations"]))
        self.assertTrue(all(row["reasons"] for row in self.mutations["mutations"]))

    def test_five_mutation_types_per_proposal(self) -> None:
        by_proposal = {}
        for row in self.mutations["mutations"]:
            by_proposal.setdefault(row["proposal_id"], set()).add(row["mutation_type"])
        self.assertEqual(len(by_proposal), 60)
        self.assertTrue(all(len(types) == 5 for types in by_proposal.values()))

    def test_toolchain_is_isolated_and_smoke_used(self) -> None:
        receipt = load(X2 / "toolchain-install-receipt.json")
        self.assertFalse(receipt["global_or_shared_prefix_mutated"])
        self.assertEqual(receipt["installation_scope"], "D_isolated_owner_local_nonshared")
        self.assertEqual(
            {row["name"]: row["version"] for row in receipt["direct_tools"]},
            {"bitarray": "3.10.1", "networkx": "3.6.1", "jsonschema": "4.26.0"},
        )
        self.assertEqual(len(receipt["download_artifacts"]), 8)
        self.assertEqual(receipt["smoke"]["invalid_schema_errors"], 2)
        self.assertEqual(receipt["smoke"]["punch_pattern_holes"], 4)
        self.assertTrue(receipt["smoke"]["acyclic_lineage"])
        self.assertEqual(receipt["smoke"]["external_actions"], 0)

    def test_schema_and_sequence_board_are_synthetic(self) -> None:
        board = load(X2 / "sequence-lineage-board.json")
        schema = load(X2 / "punched-card-deck-schema.json")
        self.assertEqual(board["collection_rows"], 0)
        self.assertFalse(board["authority_conferred"])
        self.assertTrue(board["record"]["synthetic"])
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])

    def test_skill_validation_once(self) -> None:
        receipt = load(X2 / "skill-validation-receipts.json")
        self.assertEqual(receipt["passed"], 20)
        self.assertFalse(receipt["global_installation"])
        self.assertFalse(receipt["validator_replayed_after_success"])
        self.assertTrue(all(row["returncode"] == 0 and row["validator_invocations"] == 1 for row in receipt["receipts"]))
        self.assertEqual(len(list((X2 / "skills").glob("*/SKILL.md"))), 20)
        self.assertEqual(len(list((X2 / "skills").glob("*/agents/openai.yaml"))), 20)

    def test_runner_smoke_once(self) -> None:
        receipt = load(X2 / "runner-smoke-receipts.json")
        self.assertEqual(receipt["passed"], 10)
        self.assertFalse(receipt["replayed_after_success"])
        self.assertTrue(all(row["returncode"] == 0 and row["smoke_invocations"] == 1 for row in receipt["receipts"]))
        self.assertTrue(all(row["output"]["external_actions"] == 0 for row in receipt["receipts"]))

    def test_portfolio_execution_and_holds(self) -> None:
        portfolio = load(X2 / "portfolio-results.json")
        self.assertEqual(len(portfolio["safe_now"]), 120)
        self.assertEqual(len(portfolio["owner_candidates"]), 80)
        self.assertEqual(len(portfolio["owner_clean_fix_refine"]), 100)
        self.assertTrue(all(row["state"] == "bounded_owner_local_completed" for row in portfolio["safe_now"]))
        self.assertTrue(all(row["state"] == "bounded_fixture_completed" for row in portfolio["owner_candidates"]))
        self.assertTrue(all(row["state"] == "held_unexecuted" for row in portfolio["exact_approval"] + portfolio["blocked"]))
        self.assertEqual(portfolio["successor_records_executed"], 0)

    def test_flashcard_hierarchy_and_addresses(self) -> None:
        deck = load(X2 / "freed-id-flashcards.json")
        self.assertEqual(deck["card_count"], 80)
        self.assertEqual(len(deck["cards"]), 80)
        self.assertEqual(len({row["content_address"] for row in deck["cards"]}), 80)
        self.assertEqual(Counter(row["tier"] for row in deck["cards"]), Counter({"proposal": 60, "boundary": 13, "practice": 3, "pillar": 3, "owner": 1}))

    def test_pillar_and_authority_boundaries(self) -> None:
        gmut = load(X2 / "gmut-formal-board.json")
        thos = load(X2 / "thos-proxy-board.json")
        freed = load(X2 / "freed-id-profile.json")
        cbr = load(X2 / "cbr-authority-matrix.json")
        self.assertEqual(gmut["empirical_rows"], 0)
        self.assertFalse(gmut["theory_of_everything"])
        self.assertEqual(thos["blind_matched_budget_real_arms"], 0)
        self.assertFalse(freed["production"])
        self.assertEqual(cbr["decisions_made"], 0)

    def test_zero_row_adapter_refuses(self) -> None:
        adapter = load(X2 / "zero-row-adapter.json")
        self.assertEqual(adapter["downloaded_rows"], 0)
        self.assertEqual(adapter["likelihood_calls"], 0)
        self.assertEqual(adapter["terminal_response"], "REFUSED_NO_ROWS")
        self.assertEqual(adapter["status"], "represented")

    def test_accessibility_is_structural_only(self) -> None:
        audit = load(X2 / "accessibility-structural-audit.json")
        html = (X2 / "accessible-report.html").read_text(encoding="utf-8")
        self.assertFalse(audit["wcag_conformance_claimed"])
        self.assertEqual(audit["assistive_technology_evaluation"], "reserved")
        for fragment in ('lang="en-NZ"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"'):
            self.assertIn(fragment, html)

    def test_method_flow_counts_and_retention(self) -> None:
        method = load(X2 / "method-flow-ledger.json")
        negative = load(X2 / "retained-negative-register.json")
        self.assertFalse(method["failure_erasure"])
        self.assertFalse(method["independent_reproduction_claimed"])
        self.assertEqual(len(method["methods"]), 60)
        self.assertEqual(negative["retained_mutations"], 300)
        self.assertEqual(negative["startup_failures"], 5)
        self.assertEqual(negative["x1_postcommit_failures"], 0)
        self.assertEqual(len(negative["x2_operational_failures"]), 2)
        self.assertEqual(negative["x2_operational_failures"][0]["failure_id"], "LM6813-X2-N001")
        self.assertEqual(negative["x2_operational_failures"][1]["failure_id"], "LM6813-X2-N002")
        self.assertEqual(method["counts"], self.truth["counts"])

    def test_truth_counts_and_terminal_verdict(self) -> None:
        self.assertEqual(self.truth["declared_chain"], 9890)
        self.assertEqual(self.truth["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(self.truth["counts"]["effective_negatives"], 53582)
        self.assertEqual(self.truth["counts"]["effective_methods"], 60799)
        self.assertEqual(self.truth["counts"]["failed_witnesses"], 25243)
        self.assertEqual(self.truth["counts"]["bounded_passing_witnesses"], 42621)
        self.assertEqual(self.truth["counts"]["open_gaps"], 473)
        self.assertEqual(self.truth["counts"]["exact_gates"], 464)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_privacy_scan_has_no_confirmed_hits(self) -> None:
        scan = load(VALIDATION / "x2-privacy-scan.json")
        self.assertEqual(scan["confirmed_hits"], [])
        self.assertEqual(len(scan["privacy_classes"]), 5)

    def test_x2_manifest_replays_worktree_bytes(self) -> None:
        manifest = load(VALIDATION / "x2-index-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_staged_review_is_x2_only(self) -> None:
        review = load(VALIDATION / "x2-staged-review.json")
        self.assertEqual(review["lifecycle"], "x2_evidence")
        self.assertTrue(all("/v681-v3/x1/" not in path for path in review["expected_paths"]))
        self.assertEqual(len(review["expected_paths"]), review["path_count"])


if __name__ == "__main__":
    unittest.main()

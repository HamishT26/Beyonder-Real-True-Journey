from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "eiren-kestrel" / "v685-v5"
X1 = BASE / "x1"
X2 = BASE / "x2"
DECK = X2 / "flashcards"
VALIDATION = BASE / "validation"
X1_COMMIT = "167e626c0684ac9ac1cd2d2184a831e1456f43b9"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


class EirenKestrelV685V5X2Tests(unittest.TestCase):
    def test_x2_began_at_exact_x1(self):
        self.assertEqual(git("merge-base", "--is-ancestor", X1_COMMIT, "HEAD").returncode, 0)

    def test_new_proposal_evidence(self):
        evidence = load(X2 / "proposal-evidence.json")
        outcomes = load(X2 / "proposal-outcomes.json")
        self.assertEqual(evidence["proposal_count"], 120)
        self.assertEqual(evidence["positive_pass_count"], 120)
        self.assertEqual(outcomes["outcome_counts"], {"completed": 84, "represented": 24, "open_gap": 6, "exact_gate": 6})
        self.assertEqual(outcomes["unknown_labels"], [])

    def test_rejecting_mutations(self):
        receipt = load(X2 / "rejecting-mutations.json")
        self.assertEqual(receipt["mutation_count"], 600)
        self.assertEqual(receipt["rejected_count"], 600)
        self.assertEqual(receipt["accepted_count"], 0)
        self.assertTrue(all(row["retained_failed_witness"] for row in receipt["mutations"]))

    def test_inherited_revalidation_zero_credit(self):
        receipt = load(X2 / "inherited-revalidation-evidence.json")
        self.assertEqual(receipt["selection_count"], 200)
        self.assertEqual(receipt["positive_pass_count"], 200)
        self.assertEqual(receipt["rejecting_pass_count"], 200)
        self.assertTrue(all(row["eiren_novelty_credit"] == 0 and row["eiren_completion_credit"] == 0 for row in receipt["rows"]))

    def test_portfolio_execution(self):
        receipt = load(X2 / "portfolio-execution.json")
        self.assertEqual(len(receipt["safe_now"]), 200)
        self.assertEqual(len(receipt["owner_candidates"]), 150)
        self.assertEqual(len(receipt["owner_clean_fix_refine"]), 300)
        self.assertEqual(receipt["bounded_completed_count"], 650)
        self.assertEqual(receipt["exact_or_blocked_executed_count"], 0)
        self.assertTrue(all(not row["executed"] for row in receipt["exact_approval"] + receipt["blocked"]))

    def test_skills_initialized_validated_read_and_smoked(self):
        receipt = load(X2 / "skill-initialization-and-smoke-receipt.json")
        self.assertEqual(receipt["skill_count"], 20)
        self.assertEqual(receipt["quick_validated_count"], 20)
        self.assertEqual(receipt["complete_read_count"], 20)
        self.assertEqual(receipt["accepting_smoke_pass_count"], 20)
        self.assertEqual(receipt["rejecting_smoke_pass_count"], 20)
        self.assertTrue(all(row["smoke_pass"] for row in receipt["skills"]))

    def test_runners_accept_and_reject(self):
        receipt = load(X2 / "runner-smoke-receipt.json")
        self.assertEqual(receipt["runner_count"], 10)
        self.assertEqual(receipt["positive_pass_count"], 10)
        self.assertEqual(receipt["invalid_rejection_pass_count"], 10)
        self.assertTrue(all(row["smoke_pass"] for row in receipt["runners"]))

    def test_four_tier_deck_and_manifest(self):
        index = load(DECK / "deck-index.json")
        self.assertEqual(index["card_count"], 128)
        cards = [load(ROOT / path) for path in index["cards"]]
        self.assertEqual({card["tier"] for card in cards}, {1, 2, 3, 4})
        ids = {card["card_id"] for card in cards}
        for card in cards:
            self.assertTrue(all(parent in ids for parent in card["parent_ids"]))
        manifest = load(DECK / "card-manifest.json")
        self.assertTrue(manifest["self_excluded"])
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes()
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_zero_row_and_source_boundaries(self):
        zero = load(X2 / "zero-row-empirical-receipt.json")
        source = load(X2 / "source-use-receipt.json")
        numeric = [value for key, value in zero.items() if key not in {"schema", "owner", "phase"}]
        self.assertTrue(all(value == 0 for value in numeric))
        self.assertEqual(source["network_calls_in_x2"], 0)
        self.assertEqual(source["downloaded_data_rows"], 0)

    def test_method_flow_preserves_failures(self):
        methods = load(X2 / "method-flow-evidence.json")
        self.assertFalse(methods["failure_erasure"])
        self.assertEqual(methods["proposal_mutation_failures"], 600)
        self.assertEqual(methods["inherited_revalidation_failures"], 200)
        self.assertEqual(methods["skill_rejecting_failures"], 20)
        self.assertEqual(methods["runner_rejecting_failures"], 10)
        self.assertGreater(methods["effective_counts"]["bounded_passing_witnesses"], methods["starting_counts"]["bounded_passing_witnesses"])

    def test_all_x2_json_parses(self):
        paths = list(X2.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 140)
        for path in paths:
            load(path)

    def test_accessible_html_structure(self):
        html = (X2 / "accessible-evidence-board.html").read_text(encoding="utf-8")
        for token in ["<html", "<header", "<nav", "<main", "<h1", "<h2"]:
            self.assertIn(token, html)
        self.assertIn("assistive-technology", html)

    def test_x1_tree_immutable(self):
        proc = git("diff", "--name-only", X1_COMMIT, "--", "docs/eiren-kestrel/v685-v5/x1")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.decode().strip(), "")

    def test_staged_manifest_when_present(self):
        path = VALIDATION / "evidence-index-manifest.json"
        if not path.exists():
            self.skipTest("manifest finalized after staging")
        manifest = load(path)
        self.assertGreater(manifest["entry_count"], 150)
        review = load(VALIDATION / "evidence-staged-review.json")
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["x1_mutations"], [])
        self.assertEqual(review["outside_owner_paths"], [])
        privacy = load(VALIDATION / "evidence-privacy-adjudication.json")
        self.assertEqual(privacy["confirmed_hit_count"], 0)


if __name__ == "__main__":
    unittest.main()

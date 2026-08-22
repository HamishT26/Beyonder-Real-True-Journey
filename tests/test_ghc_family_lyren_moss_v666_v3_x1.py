from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v666-v3"
SOURCE = "96509c5b28628a6b62628dea277d1240b945b2ca"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class LyrenV666V3X1Tests(unittest.TestCase):
    def test_source_and_identity_are_exact(self):
        source = load("provenance/source-verification.json")
        identity = load("identity/relational-identity.json")
        self.assertEqual(source["source_sha"], SOURCE)
        self.assertEqual(source["source_to_final_phase_commit_count"], 3)
        self.assertEqual(source["source_to_final_merge_count"], 0)
        self.assertEqual(source["source_manifest_entries_replayed"], 303)
        self.assertTrue(source["four_way_equal"])
        self.assertFalse(source["predecessor_canonical_replayed"])
        self.assertEqual(identity["owner"], "Lyren Moss")
        self.assertIn("relational working language only", identity["boundary"])

    def test_proposals_and_chain_are_frozen_not_observed(self):
        freeze = load("x1/proposal-freeze.json")
        self.assertEqual(freeze["inherited_frozen_baseline"], 4210)
        self.assertEqual(freeze["new_frozen_total"], 4230)
        self.assertEqual(len(freeze["new_proposals"]), 20)
        self.assertEqual(len(freeze["selected_inherited_revalidations"]), 20)
        self.assertEqual(freeze["expected_disposition_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertFalse(freeze["outcomes_observed"])
        self.assertEqual({row["expected_disposition"] for row in freeze["new_proposals"]}, ALLOWED)
        self.assertTrue(all(len(row["preregistered_mutations"]) == 5 for row in freeze["new_proposals"]))
        self.assertTrue(all(row["x1_status"] == "frozen_not_executed" for row in freeze["new_proposals"]))

    def test_novelty_audit_reconstructs_every_inherited_row(self):
        audit = load("x1/novelty-audit.json")
        self.assertEqual(audit["corpus_row_count"], 4210)
        self.assertEqual(audit["new_frozen_total"], 4230)
        self.assertEqual(audit["exact_inherited_collisions"], [])
        self.assertEqual(audit["new_pair_collisions_at_or_above_0_70"], [])
        self.assertTrue(audit["valid"])

    def test_portfolio_minimums_are_exact_and_unexecuted(self):
        portfolio = load("x1/portfolio-freeze.json")
        self.assertTrue(portfolio["minimums_satisfied"])
        self.assertEqual(portfolio["counts"], {"owner_safe_now": 30, "successor_safe_now": 20, "owner_bounded_candidates": 15, "successor_bounded_candidates": 15, "exact_approval_packets": 10, "blocked_packets": 5, "owner_phase_local_skill_plans": 10, "successor_skill_recommendations": 10, "owner_family_current_runner_plans": 10, "successor_runner_recommendations": 10, "owner_clean_fix_refine": 30, "successor_clean_fix_refine": 30})
        self.assertEqual(portfolio["x1_execution_count"], 0)
        for rows in portfolio["portfolios"].values():
            self.assertTrue(all(row["completion_credit"] == 0 for row in rows))

    def test_startup_failures_are_retained(self):
        flow = load("method-flow/startup-method-flow.json")
        self.assertEqual(flow["new_startup_negative_count"], 6)
        self.assertEqual(flow["effective_after_x1_startup_negatives"], 26288)
        self.assertEqual(flow["effective_after_x1_startup_methods"], 10715)
        self.assertEqual(flow["failed_witness_count"], flow["bounded_passing_witness_count"])
        self.assertTrue(all(row["aggregate_credit"] == 0 for row in flow["rows"]))

    def test_sources_and_practice_remain_bounded(self):
        profiles = load("provenance/source-profiles.json")
        self.assertEqual(profiles["profile_count"], 7)
        self.assertEqual(profiles["network_calls_by_phase_software"], 0)
        self.assertEqual(profiles["real_rows_ingested"], 0)
        self.assertTrue(all(row["authority_nonconversion"] for row in profiles["profiles"]))

    def test_x2_and_later_paths_do_not_exist(self):
        for name in ("x2", "evidence", "closeout", "seal", "final", "handoffs"):
            self.assertFalse((PHASE / name).exists(), name)

    def test_x1_artifacts_are_parseable_utf8_lf(self):
        for path in PHASE.rglob("*"):
            if not path.is_file():
                continue
            raw = path.read_bytes()
            self.assertNotIn(b"\r", raw, str(path))
            text = raw.decode("utf-8")
            if path.suffix == ".json":
                json.loads(text)

    def test_x1_manifest_replays_actual_git_index_blobs(self):
        manifest = load("validation/x1-content-manifest.json")
        self.assertEqual(manifest["entry_count"], 18)
        self.assertEqual(len(manifest["entries"]), 18)
        for entry in manifest["entries"]:
            stage_line = subprocess.check_output(
                ["git", "-C", str(ROOT), "ls-files", "--stage", "--", entry["path"]],
                text=True,
            ).strip()
            self.assertIn(entry["git_blob_oid"], stage_line)
            blob = subprocess.check_output(
                ["git", "-C", str(ROOT), "show", f":{entry['path']}"]
            )
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])
            self.assertEqual(len(blob), entry["size_bytes"])

    def test_git_state_still_descends_from_exact_source(self):
        head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
        result = subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", SOURCE, head], check=False)
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()

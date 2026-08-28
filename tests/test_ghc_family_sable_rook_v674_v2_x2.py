#!/usr/bin/env python3
"""Bounded owner-scoped tests for Sable Rook v674-v2 x2 evidence."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


SOURCE = "6f079df9a056f00e80392b7e036abc023db5fa88"
X1 = "81ad6f98f24087777691e96201312e66c37ac844"
ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v674-v2"
X1_ROOT = PHASE / "x1"
X2_ROOT = PHASE / "x2"
VALIDATION = PHASE / "validation"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class SableRookV674V2X2Tests(unittest.TestCase):
    def test_01_exact_x1_context_and_immutable_x1_surface(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD"), X1)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        changed = git("diff", "--name-only", X1, "--", "docs/sable-rook/v674-v2/x1")
        self.assertEqual(changed, "")

    def test_02_exactly_sixty_proposals_have_permitted_outcomes(self) -> None:
        files = sorted((X2_ROOT / "proposals").glob("*.json"))
        self.assertEqual(len(files), 60)
        rows = [load(path) for path in files]
        outcomes = [row["outcome"] for row in rows]
        self.assertEqual(set(outcomes), ALLOWED_OUTCOMES)
        self.assertEqual(
            {label: outcomes.count(label) for label in ALLOWED_OUTCOMES},
            {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        )
        self.assertEqual(len({row["proposal"]["proposal_id"] for row in rows}), 60)

    def test_03_accepting_controls_and_rejecting_mutations_are_exact(self) -> None:
        positive = load(X2_ROOT / "fixtures" / "positive-control-ledger.json")
        rejected = load(X2_ROOT / "fixtures" / "invalid-mutation-ledger.json")
        self.assertEqual((positive["count"], positive["passed"]), (60, 60))
        self.assertEqual((rejected["count"], rejected["rejected"]), (240, 240))
        self.assertEqual(rejected["broader_credit"], 0)
        self.assertEqual({row["observed"] for row in rejected["rows"]}, {"rejected"})
        self.assertEqual({row["completion_credit"] for row in rejected["rows"]}, {0})

    def test_04_practice_artifacts_are_synthetic_and_authority_vacant(self) -> None:
        cue_register = load(X2_ROOT / "practice" / "synthetic-cue-register.json")
        authority = load(X2_ROOT / "practice" / "access-remedy-authority-matrix.json")
        thos = load(X2_ROOT / "practice" / "thos-handover-proxy.json")
        gmut = load(X2_ROOT / "practice" / "gmutt-analogy-firewall.json")
        self.assertEqual(cue_register["real_records"], 0)
        self.assertEqual(cue_register["network_calls"], 0)
        self.assertTrue(all(row["software_decision"] is False for row in authority["rows"]))
        self.assertEqual(thos["real_participants"], 0)
        self.assertFalse(thos["independent_review"])
        self.assertEqual(gmut["real_likelihoods"], 0)
        self.assertFalse(gmut["empirical_confirmation"])
        self.assertFalse(gmut["theory_of_everything"])

    def test_05_owner_portfolios_and_protected_holds_remain_distinct(self) -> None:
        owner = load(X2_ROOT / "portfolios" / "owner-execution.json")
        holds = load(X2_ROOT / "portfolios" / "protected-holds.json")
        successor = load(X2_ROOT / "portfolios" / "successor-recommendations.json")
        self.assertEqual(len(owner["safe_now"]), 120)
        self.assertEqual(len(owner["owner_candidates"]), 80)
        self.assertEqual(len(owner["owner_clean_fix_refine"]), 100)
        self.assertEqual(len(holds["exact_approval"]), 20)
        self.assertEqual(len(holds["blocked"]), 10)
        self.assertEqual(holds["executed"], 0)
        self.assertEqual(successor["sable_completion_credit"], 0)
        self.assertFalse(successor["execution_claimed"])
        self.assertFalse(successor["precontact"])

    def test_06_twenty_phase_local_skills_validate_and_are_smoke_used(self) -> None:
        receipt = load(X2_ROOT / "tools" / "skill-use-receipt.json")
        skill_files = sorted((X2_ROOT / "tools" / "skills").glob("*/SKILL.md"))
        self.assertEqual(receipt["count"], 20)
        self.assertEqual(len(skill_files), 20)
        self.assertTrue(all(row["quick_validate_exit"] == 0 for row in receipt["rows"]))
        self.assertTrue(all(row["smoke_use_exit"] == 0 for row in receipt["rows"]))
        self.assertTrue(all(row["phase_local_only"] is True for row in receipt["rows"]))
        self.assertTrue(all(row["global_installation"] is False for row in receipt["rows"]))
        self.assertTrue(all(row["subagent_forward_test"] == "not_run_solo_rule" for row in receipt["rows"]))

    def test_07_ten_family_current_runners_accept_and_reject_as_declared(self) -> None:
        receipt = load(X2_ROOT / "tools" / "runner-smoke-receipt.json")
        self.assertEqual(receipt["count"], 10)
        self.assertEqual(len(receipt["rows"]), 10)
        self.assertTrue(all(row["accept_exit"] == 0 for row in receipt["rows"]))
        self.assertTrue(all(row["reject_exit"] == 2 for row in receipt["rows"]))
        self.assertTrue(all(row["smoke_used"] is True for row in receipt["rows"]))
        self.assertTrue(all(row["installed_on_path"] is False for row in receipt["rows"]))
        for row in receipt["rows"]:
            self.assertTrue((ROOT / "scripts" / row["runner"]).is_file())

    def test_08_phase_truth_preserves_boundaries_and_terminal_veto(self) -> None:
        truth = load(X2_ROOT / "phase-truth.json")
        self.assertEqual(truth["proposal_chain"], 6670)
        self.assertEqual(
            truth["outcomes"],
            {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        )
        self.assertEqual(truth["real_data_records"], 0)
        self.assertEqual(truth["real_participants"], 0)
        self.assertEqual(truth["real_keys_or_proofs"], 0)
        self.assertEqual(truth["external_actions"], 0)
        self.assertFalse(truth["complete_repository_suite"])
        self.assertFalse(truth["independent_reproduction"])
        self.assertFalse(truth["empirical_confirmation"])
        self.assertFalse(truth["maori_authority"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_09_method_flow_retains_startup_and_mutation_failures(self) -> None:
        ledger = load(X2_ROOT / "method-flow" / "ledger.json")
        self.assertEqual(len(ledger["x1_startup_failures"]), 14)
        self.assertEqual(ledger["components"]["invalid_mutation_guards"], 240)
        counts = ledger["effective_counts"]
        self.assertGreaterEqual(counts["effective_negatives"], 38104 + 14 + 240)
        self.assertGreaterEqual(counts["failed_witnesses"], 9765 + 14 + 240)
        self.assertGreater(counts["bounded_passing_witnesses"], 12654)
        self.assertIn("never erases", ledger["recovery_rule"])

    def test_10_x2_manifest_replays_normalized_lf_worktree_bytes(self) -> None:
        manifest = load(VALIDATION / "x2-evidence-manifest.json")
        self.assertEqual(manifest["hash_domain"], "normalized_lf_worktree_precommit")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["self_exclusions"], ["docs/sable-rook/v674-v2/validation/x2-evidence-manifest.json"])
        for entry in manifest["entries"]:
            data = normalized((ROOT / entry["path"]).read_bytes())
            self.assertEqual(len(data), entry["bytes_normalized_lf"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"], entry["path"])

    def test_11_json_python_and_document_surfaces_are_parseable(self) -> None:
        json_files = sorted(X2_ROOT.rglob("*.json"))
        self.assertGreaterEqual(len(json_files), 80)
        for path in json_files:
            load(path)
        python_files = [ROOT / "scripts" / row["runner"] for row in load(X2_ROOT / "tools" / "runner-smoke-receipt.json")["rows"]]
        python_files.append(ROOT / "scripts" / "build_ghc_family_sable_rook_v674_v2_x2.py")
        python_files.append(ROOT / "tests" / "test_ghc_family_sable_rook_v674_v2_x2.py")
        for path in python_files:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        for path in X2_ROOT.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)

    def test_12_accessible_companion_is_structural_not_complete_conformance(self) -> None:
        html = (X2_ROOT / "practice" / "accessible-companion.html").read_text(encoding="utf-8")
        markdown = (X2_ROOT / "practice" / "accessible-companion.md").read_text(encoding="utf-8")
        self.assertIn('<html lang="en">', html)
        self.assertIn("<main>", html)
        self.assertIn("<caption>Core outcomes</caption>", html)
        self.assertIn("manual", html.lower())
        self.assertIn("affected-user evaluation", markdown)
        self.assertNotIn("complete accessibility conformance", markdown.lower())

    def test_13_owner_generated_file_count_is_below_rotation_ceiling(self) -> None:
        owner_paths = list(PHASE.rglob("*"))
        owner_files = [path for path in owner_paths if path.is_file()]
        owner_files += list(ROOT.glob("scripts/*sable_rook_v674_v2*.py"))
        owner_files += list(ROOT.glob("scripts/ghc_family_caption_*.py"))
        owner_files += list(ROOT.glob("tests/*sable_rook_v674_v2*.py"))
        self.assertLess(len({path.resolve() for path in owner_files}), 2000)

    def test_14_no_private_absolute_path_or_raw_identifier_payload(self) -> None:
        patterns = [
            re.compile(rb"(?:C:\\Users\\|D:\\GHC-Archives)", re.I),
            re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
            re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
        ]
        candidates = []
        for path in sorted(X2_ROOT.rglob("*")):
            if not path.is_file():
                continue
            data = path.read_bytes()
            for pattern in patterns:
                if pattern.search(data):
                    candidates.append(str(path.relative_to(ROOT)))
        self.assertEqual(candidates, [])


if __name__ == "__main__":
    unittest.main()

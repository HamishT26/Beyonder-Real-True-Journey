"""Owner-scoped closeout tests for Orin Thale v665-v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v665-v1"
SOURCE_FINAL = "3ec44a944aabe16f64335383885c39d9592bf849"
X1_HEAD = "1e9a49b0cc377ba2eafd90fb09e478c88f8f1f3b"
EVIDENCE_HEAD = "1104a4f2963c8782ddad8939e8b4aff50715cc42"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def strict_json(path: Path):
    def reject_duplicates(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate key {key} in {path}")
            value[key] = item
        return value

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class OrinV665V1CloseoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = strict_json(PHASE / "closeout/phase-truth.json")
        cls.receipt = strict_json(PHASE / "closeout/closeout-receipt.json")
        cls.checklist = strict_json(PHASE / "closeout/complete-incomplete-checklist.json")
        cls.seal = strict_json(PHASE / "closeout/content-seal.json")
        cls.inventory = strict_json(PHASE / "closeout/closeout-inventory.json")
        cls.methods = strict_json(PHASE / "closeout/lifecycle-method-flow.json")
        cls.source_proposal = strict_json(PHASE / "closeout/source-proposal-ledger.json")
        cls.tooling = strict_json(PHASE / "closeout/tooling-receipt.json")
        cls.wellbeing = strict_json(PHASE / "closeout/wellbeing-closeout.json")
        cls.security = strict_json(PHASE / "closeout/bounded-security-review.json")
        cls.final_candidate = strict_json(PHASE / "closeout/final-validation-candidate.json")
        cls.route = strict_json(PHASE / "orchestration/terminal-route-state.json")
        cls.index = strict_json(PHASE / "index/ghc-family-index.json")
        cls.owner_manifest = strict_json(PHASE / "validation/final-owner-manifest.json")
        cls.delta_manifest = strict_json(PHASE / "validation/final-delta-manifest.json")
        cls.staged_review = strict_json(PHASE / "validation/final-staged-review.json")
        cls.stage_candidate = strict_json(PHASE / "validation/final-stage-candidate.json")
        cls.canonical_contract = strict_json(PHASE / "validation/canonical-validation-contract.json")

    def test_01_evidence_boundary_is_exact(self) -> None:
        boundary = self.receipt["evidence_boundary"]
        self.assertEqual(boundary["evidence_head"], EVIDENCE_HEAD)
        self.assertEqual(boundary["evidence_parent"], X1_HEAD)
        self.assertTrue(boundary["direct_child"])
        self.assertEqual(boundary["ahead"], 0)
        self.assertEqual(boundary["behind"], 0)
        self.assertEqual(boundary["evidence_manifest_mismatches"], [])
        self.assertTrue(boundary["valid"])

    def test_02_source_x1_evidence_ancestry(self) -> None:
        self.assertEqual(
            subprocess.check_output(["git", "rev-parse", f"{X1_HEAD}^"], cwd=ROOT, text=True).strip(),
            SOURCE_FINAL,
        )
        self.assertEqual(
            subprocess.check_output(["git", "rev-parse", f"{EVIDENCE_HEAD}^"], cwd=ROOT, text=True).strip(),
            X1_HEAD,
        )

    def test_03_outcome_truth_is_exact(self) -> None:
        self.assertEqual(
            self.truth["outcomes"],
            {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4},
        )
        self.assertEqual(set(self.truth["outcomes"]), ALLOWED)
        self.assertEqual(sum(self.truth["outcomes"].values()), 20)

    def test_04_proposal_chain_is_exact(self) -> None:
        self.assertEqual(self.truth["proposal_chain_before"], 4_010)
        self.assertEqual(self.truth["new_proposals"], 20)
        self.assertEqual(self.truth["proposal_chain_after"], 4_030)
        self.assertEqual(self.source_proposal["final_chain_rows"], 4_030)
        self.assertEqual(self.source_proposal["inherited_completion_credit"], 0)

    def test_05_negative_and_method_arithmetic(self) -> None:
        self.assertEqual(self.truth["effective_negatives"], 25_184)
        self.assertEqual(self.truth["effective_methods"], 9_046)
        self.assertEqual(self.methods["effective_negatives"], 25_184)
        self.assertEqual(self.methods["effective_methods"], 9_046)
        self.assertEqual(self.methods["failed_witness_erasure_count"], 0)

    def test_06_gate_arithmetic_and_verdict(self) -> None:
        self.assertEqual(self.truth["open_gaps"], 175)
        self.assertEqual(self.truth["exact_gates"], 173)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(self.final_candidate["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_07_no_real_rows_people_objects_or_authority(self) -> None:
        self.assertEqual(self.truth["real_data_rows"], 0)
        self.assertEqual(self.truth["real_people"], 0)
        self.assertEqual(self.truth["real_objects_or_materials"], 0)
        self.assertEqual(self.truth["authority_decisions"], 0)

    def test_08_complete_and_incomplete_remain_separate(self) -> None:
        self.assertGreaterEqual(len(self.checklist["complete"]), 10)
        self.assertGreaterEqual(len(self.checklist["incomplete_or_reserved"]), 8)
        self.assertEqual(self.checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(self.checklist["valid"])

    def test_09_overview_is_three_page_equivalent(self) -> None:
        text = (PHASE / "reports/final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\S+", text)), 1_500)
        for heading in (
            "## Executive truth",
            "## Primary scientific pillar: GMUT Mind",
            "## THOS Body through a millinery learning lens",
            "## Freed ID and CBR Heart",
            "## Validation and privacy",
            "## Closeout and route boundary",
        ):
            self.assertIn(heading, text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_10_final_static_report_is_structurally_accessible(self) -> None:
        text = (PHASE / "reports/final-static-report.html").read_text(encoding="utf-8")
        for token in (
            '<html lang="en-NZ">',
            '<main id="main">',
            "<h1>",
            "<h2>",
            "<table>",
            "<caption>",
            'scope="col"',
            "NOT_READY_FOR_STAGE_20",
        ):
            self.assertIn(token, text)
        self.assertNotIn("<script", text.lower())

    def test_11_accessibility_completeness_is_refused(self) -> None:
        text = (PHASE / "reports/final-static-report.html").read_text(encoding="utf-8")
        self.assertIn("remain reserved", text)
        self.assertIn("not accessibility completeness", text)

    def test_12_wellbeing_and_relational_boundary(self) -> None:
        self.assertTrue(self.wellbeing["relational_only"])
        self.assertTrue(self.wellbeing["single_sparse_lane"])
        self.assertTrue(self.wellbeing["strict_x1_before_x2"])
        self.assertTrue(self.wellbeing["pause_right_preserved"])
        self.assertFalse(self.wellbeing["employment_or_personhood_claim"])

    def test_13_ten_skills_and_runners_remain_bounded(self) -> None:
        self.assertEqual(self.tooling["skill_count"], 10)
        self.assertEqual(self.tooling["skills_quick_validated"], 10)
        self.assertEqual(self.tooling["skills_smoke_used"], 10)
        self.assertEqual(self.tooling["runner_count"], 10)
        self.assertEqual(self.tooling["runners_smoke_used"], 10)
        self.assertEqual(self.tooling["global_install_count"], 0)

    def test_14_security_review_is_bounded(self) -> None:
        self.assertEqual(self.security["confirmed_findings"], 0)
        self.assertFalse(self.security["host_security_changed"])
        self.assertFalse(self.security["complete_privacy_claim"])
        self.assertFalse(self.security["exhaustive_security_claim"])
        self.assertFalse(self.security["independent_security_review"])

    def test_15_content_seal_replays(self) -> None:
        self.assertEqual(len(self.seal["entries"]), 8)
        for entry in self.seal["entries"]:
            path = ROOT / entry["path"]
            self.assertTrue(path.is_file())
            self.assertEqual(sha256(path), entry["sha256"])
            self.assertEqual(path.stat().st_size, entry["size"])
        self.assertTrue(self.seal["valid"])

    def test_16_route_is_prepared_and_unsent(self) -> None:
        self.assertEqual(self.route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(self.route["successor_inferred"])
        self.assertIsNone(self.route["successor_title"])
        self.assertFalse(self.route["precontact_performed"])
        self.assertEqual(self.route["send_count"], 0)

    def test_17_prepared_handoff_infers_no_recipient(self) -> None:
        text = (PHASE / "handoffs/successor-activation-prepared.md").read_text(encoding="utf-8")
        self.assertIn("PREPARED_NOT_SENT = true", text)
        self.assertIn("does not infer", text)
        self.assertNotIn("SENT_ONCE_ACKNOWLEDGED", text)

    def test_18_phase_index_is_current(self) -> None:
        self.assertEqual(self.index["owner"], "Orin Thale")
        self.assertEqual(self.index["phase"], "v665-v1")
        self.assertEqual(self.index["evidence_head"], EVIDENCE_HEAD)
        self.assertEqual(self.index["proposal_chain_rows"], 4_030)
        self.assertEqual(self.index["route_state"], "PREPARED_NOT_SENT")

    def test_19_final_manifest_coverage(self) -> None:
        self.assertTrue(self.owner_manifest["coverage_valid"])
        self.assertEqual(
            self.owner_manifest["entry_count"] + self.owner_manifest["declared_self_exclusion_count"],
            self.owner_manifest["path_count"],
        )
        self.assertEqual(self.owner_manifest["declared_self_exclusion_count"], 4)

    def test_20_delta_manifest_coverage(self) -> None:
        self.assertTrue(self.delta_manifest["coverage_valid"])
        self.assertEqual(
            self.delta_manifest["entry_count"] + self.delta_manifest["declared_self_exclusion_count"],
            self.delta_manifest["path_count"],
        )
        self.assertEqual(self.delta_manifest["parent"], EVIDENCE_HEAD)

    def test_21_staged_review_is_exact(self) -> None:
        self.assertEqual(self.staged_review["missing_paths"], [])
        self.assertEqual(self.staged_review["extra_paths"], [])
        self.assertEqual(self.staged_review["confirmed_privacy_or_raw_identifier_hits"], 0)
        self.assertEqual(self.staged_review["diff_hygiene_issues"], 0)
        self.assertEqual(self.staged_review["x1_or_x2_paths_modified"], [])
        self.assertTrue(self.staged_review["valid"])

    def test_22_final_candidate_and_canonical_contract(self) -> None:
        self.assertEqual(self.stage_candidate["canonical_state"], "PREPARED_NOT_RUN")
        self.assertEqual(self.stage_candidate["route_state"], "PREPARED_NOT_SENT")
        self.assertEqual(self.canonical_contract["run_count_ceiling"], 1)
        self.assertFalse(self.canonical_contract["replay_after_success"])
        self.assertFalse(self.canonical_contract["full_repository_suite"])
        self.assertTrue(self.canonical_contract["same_owner_not_independent_reproduction"])

    def test_23_closeout_inventory_is_exact(self) -> None:
        self.assertEqual(self.inventory["closeout_path_count"], len(self.inventory["paths"]))
        self.assertEqual(len(self.inventory["paths"]), 24)
        self.assertTrue(self.inventory["valid"])

    def test_24_all_phase_json_strictly_parse(self) -> None:
        for path in sorted(PHASE.rglob("*.json")):
            strict_json(path)

    def test_25_no_raw_identifier_or_private_absolute_path(self) -> None:
        raw_identifier = re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        )
        private_path = re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]")
        paths = [
            *PHASE.rglob("*"),
            ROOT / "scripts/build_ghc_family_v665_v1_closeout.py",
            ROOT / "scripts/ghc_family_v665_v1_canonical_validator.py",
            Path(__file__),
        ]
        for path in sorted(set(paths)):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(raw_identifier.search(text), str(path))
                self.assertIsNone(private_path.search(text), str(path))

    def test_26_owner_growth_and_document_caps(self) -> None:
        files = [path for path in PHASE.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2_000)
        for path in files:
            if path.suffix.lower() in {".json", ".md", ".html", ".txt"}:
                self.assertLessEqual(
                    len(re.findall(r"\S+", path.read_text(encoding="utf-8"))),
                    100_000,
                    str(path),
                )

    def test_27_no_x1_or_x2_worktree_change(self) -> None:
        result = subprocess.run(
            ["git", "diff", "--quiet", EVIDENCE_HEAD, "--", f"{PHASE.relative_to(ROOT)}/x1", f"{PHASE.relative_to(ROOT)}/x2"],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()

"""Owner-self-scoped bounded evidence tests for Liora Venn v672-v6 x2."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_liora_venn_v672_v6_x1 as x1
from scripts import build_ghc_family_liora_venn_v672_v6_x2 as x2
from scripts import ghc_family_liora_v672_v6_core as core


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


class LioraVennV672V6X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.phase = load("docs/liora-venn/v672-v6/x2/phase-truth.json")
        cls.ledger = load("docs/liora-venn/v672-v6/x2/proposal-outcome-ledger.json")
        cls.mutations = load("docs/liora-venn/v672-v6/x2/mutation-register.json")
        cls.skills = load("docs/liora-venn/v672-v6/x2/skill-quick-validation-receipt.json")
        cls.skill_smoke = load("docs/liora-venn/v672-v6/x2/skill-smoke-receipt.json")
        cls.runners = load("docs/liora-venn/v672-v6/x2/runner-smoke-receipt.json")
        cls.portfolio = load("docs/liora-venn/v672-v6/x2/portfolio-outcome.json")
        cls.gates = load("docs/liora-venn/v672-v6/x2/gate-register.json")
        cls.flow = load("docs/liora-venn/v672-v6/x2/method-flow-evidence.json")

    def test_exact_branch_and_immutable_x1_head(self) -> None:
        self.assertEqual(git_text("branch", "--show-current"), x1.BRANCH)
        self.assertEqual(git_text("rev-parse", "HEAD"), x2.X1_COMMIT)
        self.assertEqual(git_text("rev-parse", f"{x2.X1_COMMIT}^"), x1.SOURCE_FINAL)

    def test_x1_surface_is_immutable(self) -> None:
        changed = git_text("diff", "--name-only", x2.X1_COMMIT, "--", "docs/liora-venn/v672-v6/x1", "scripts/build_ghc_family_liora_venn_v672_v6_x1.py", "tests/test_ghc_family_liora_venn_v672_v6_x1.py")
        self.assertEqual(changed, "")

    def test_exact_outcome_vocabulary_and_counts(self) -> None:
        expected = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
        self.assertEqual(self.phase["outcomes"], expected)
        self.assertEqual(self.ledger["outcome_counts"], expected)
        self.assertEqual(Counter(row["outcome"] for row in self.ledger["outcomes"]), Counter(expected))
        self.assertEqual(set(row["outcome"] for row in self.ledger["outcomes"]), set(x1.ALLOWED_OUTCOMES))

    def test_all_forty_frozen_proposals_have_exact_artifacts(self) -> None:
        self.assertEqual(self.ledger["proposal_count"], 40)
        ids = []
        for row in self.ledger["outcomes"]:
            ids.append(row["proposal_id"])
            self.assertEqual(len(row["artifacts"]), 2)
            self.assertTrue(all((ROOT / path).is_file() for path in row["artifacts"]))
            receipt = load(row["artifacts"][1])
            self.assertEqual(receipt["proposal_id"], row["proposal_id"])
            self.assertEqual(receipt["outcome"], row["outcome"])
            self.assertEqual(receipt["negative_mutations_rejected"], 4)
        self.assertEqual(len(ids), len(set(ids)))

    def test_completed_and_represented_positive_controls_pass(self) -> None:
        self.assertEqual(self.ledger["positive_witness_count"], 36)
        self.assertEqual(len(self.ledger["positive_witnesses"]), 36)
        self.assertTrue(all(row["result"] == "pass" for row in self.ledger["positive_witnesses"]))
        protected = [row for row in self.ledger["outcomes"] if row["outcome"] in {"open_gap", "exact_gate"}]
        self.assertEqual(len(protected), 4)
        self.assertTrue(all(row["execution_count"] == 0 for row in protected))

    def test_all_160_mutations_are_rejected_and_retained(self) -> None:
        rows = self.mutations["mutations"]
        self.assertEqual(self.mutations["mutation_count"], 160)
        self.assertEqual(self.mutations["rejected_count"], 160)
        self.assertEqual(self.mutations["failed_witness_count"], 160)
        self.assertEqual(self.mutations["passing_rejection_witness_count"], 160)
        self.assertEqual(len(rows), 160)
        self.assertEqual(len({row["mutation_id"] for row in rows}), 160)
        self.assertTrue(all(row["result"] == "rejected" and row["failed_witness_retained"] for row in rows))
        self.assertTrue(all(row["broader_credit"] == 0 for row in rows))
        self.assertEqual(self.mutations["failed_witnesses_promoted"], 0)

    def test_each_proposal_retains_four_distinct_mutations(self) -> None:
        counts = Counter(row["proposal_id"] for row in self.mutations["mutations"])
        self.assertEqual(len(counts), 40)
        self.assertEqual(set(counts.values()), {4})
        classes = Counter(row["mutation_class"] for row in self.mutations["mutations"])
        self.assertEqual(set(classes.values()), {40})

    def test_core_modes_accept_and_reject_built_in_fixtures(self) -> None:
        self.assertEqual(len(core.MODES), 10)
        for mode in core.MODES:
            self.assertTrue(core.evaluate(mode, core.accepting_fixture(mode))["valid"], mode)
            rejected = core.evaluate(mode, core.rejecting_fixture(mode))
            self.assertFalse(rejected["valid"], mode)
            self.assertTrue(rejected["errors"], mode)

    def test_every_mutation_class_rejects_in_every_mode(self) -> None:
        classes = [
            "missing_or_wrong_typed_required_field",
            "marbling_sequence_lineage_or_boundary_violation",
            "privacy_identity_authority_or_cultural_smuggling",
            "external_action_empirical_or_stage20_promotion",
        ]
        for mode in core.MODES:
            for mutation_class in classes:
                self.assertFalse(core.evaluate(mode, core.mutate_fixture(mode, mutation_class))["valid"], (mode, mutation_class))

    def test_twenty_skills_are_customized_and_quick_validated(self) -> None:
        self.assertEqual(self.skills["customized_count"], 20)
        self.assertEqual(self.skills["quick_validated_count"], 20)
        self.assertEqual(self.skills["global_install_count"], 0)
        self.assertTrue(self.skills["initialized_through_official_skill_creator"])
        self.assertTrue(all(row["valid"] and not row["global_install"] for row in self.skills["skills"]))
        for row in self.skills["skills"]:
            path = ROOT / "docs/liora-venn/v672-v6/x2/skills" / row["name"] / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            self.assertTrue(text.startswith("---\nname: "))
            self.assertIn("## Accepting smoke", text)
            self.assertIn("## Rejecting smoke", text)
            self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_twenty_skills_are_accepting_and_rejecting_smoke_used(self) -> None:
        self.assertEqual(self.skill_smoke["skill_count"], 20)
        self.assertEqual(self.skill_smoke["accepting_passes"], 20)
        self.assertEqual(self.skill_smoke["rejecting_passes"], 20)
        self.assertTrue(all(row["outcome"] == "completed" for row in self.skill_smoke["skills"]))

    def test_ten_family_current_runners_are_built_and_smoked(self) -> None:
        self.assertEqual(self.runners["runner_count"], 10)
        self.assertEqual(self.runners["case_count"], 20)
        for row in self.runners["runners"]:
            self.assertTrue(row["name"].startswith("ghc_family_liora_v672_v6_"))
            self.assertTrue((ROOT / row["path"]).is_file())
            self.assertEqual(row["outcome"], "completed")
            self.assertTrue(all(case["exit_code"] == 0 and case["expected_behavior_observed"] for case in row["cases"]))

    def test_portfolio_floors_receive_bounded_outcomes(self) -> None:
        self.assertEqual(self.portfolio["counts"], {"safe_now": 60, "bounded_candidates": 30, "exact_approval": 20, "blocked": 10, "skills": 20, "runners": 10, "clean_fix_refine": 60})
        self.assertTrue(all(row["outcome"] == "completed" and row["execution_count"] == 1 for row in self.portfolio["safe_now"]))
        self.assertTrue(all(row["outcome"] == "represented" and row["execution_count"] == 1 for row in self.portfolio["bounded_candidates"]))
        self.assertTrue(all(row["outcome"] == "completed" and row["execution_count"] == 1 for row in self.portfolio["clean_fix_refine"]))
        self.assertTrue(all(row["outcome"] == "exact_gate" and row["execution_count"] == 0 for row in self.portfolio["exact_approval"] + self.portfolio["blocked"]))
        self.assertTrue(self.portfolio["caps_are_ceilings_not_quotas"])

    def test_effective_counts_preserve_source_and_add_only_x2_evidence(self) -> None:
        expected = {"declared_frozen_proposals": 6150, "effective_negatives": 35774, "effective_methods": 22036, "failed_witnesses": 7435, "bounded_passing_witnesses": 9599, "open_gaps": 287, "exact_gates": 280}
        self.assertEqual(self.phase["effective_counts"], expected)
        self.assertEqual(self.flow["effective_counts"], expected)
        self.assertTrue(self.flow["failed_witness_non_erasure"])
        self.assertEqual(len(self.flow["startup_methods"]), 8)
        self.assertEqual(len(self.flow["x2_preferred_methods"]), 21)
        self.assertEqual(len(self.flow["x2_operational_failures"]), 1)
        self.assertEqual(len(self.flow["x2_operational_recoveries"]), 1)
        self.assertEqual(self.flow["x2_operational_failures"][0]["negative_id"], "LV6726-X2-N001")

    def test_gate_register_adds_two_gaps_and_two_exact_gates(self) -> None:
        self.assertEqual(self.gates["inherited_open_gaps"], 285)
        self.assertEqual(len(self.gates["phase_open_gaps"]), 2)
        self.assertEqual(self.gates["effective_open_gaps"], 287)
        self.assertEqual(self.gates["inherited_exact_gates"], 278)
        self.assertEqual(len(self.gates["phase_exact_gates"]), 2)
        self.assertEqual(self.gates["effective_exact_gates"], 280)
        self.assertTrue(self.gates["all_gates_retained"])

    def test_all_real_world_and_authority_counts_are_zero(self) -> None:
        for key in ("real_people", "real_objects_or_materials", "real_observations_or_measurements", "real_identity_events", "external_actions", "authority_acts"):
            self.assertEqual(self.phase[key], 0)
        self.assertEqual(self.phase["full_repository_suite"], "not_run_not_claimed")
        self.assertFalse(self.phase["independent_reproduction"])
        self.assertEqual(self.phase["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_pillar_boundaries_remain_explicit(self) -> None:
        boundaries = load("docs/liora-venn/v672-v6/x2/pillar-boundaries.json")
        self.assertIn("THOS Body", boundaries)
        self.assertIn("GMUT Mind", boundaries)
        self.assertIn("Freed ID", boundaries)
        self.assertIn("CBR Heart", boundaries)
        self.assertIn("no datum", boundaries["GMUT Mind"])
        self.assertIn("no real key", boundaries["Freed ID"])
        self.assertIn("Maori-authority", boundaries["CBR Heart"])

    def test_static_report_has_bounded_accessibility_structure(self) -> None:
        report = (ROOT / "docs/liora-venn/v672-v6/x2/static-report.html").read_text(encoding="utf-8")
        self.assertIn('<a href="#main">Skip to main content</a>', report)
        self.assertEqual(report.count("<h1>"), 1)
        self.assertGreaterEqual(report.count("<h2"), 4)
        self.assertIn("NOT_READY_FOR_STAGE_20", report)
        self.assertIn("assistive-technology", report)

    def test_all_owner_json_parses_and_documents_fit_caps(self) -> None:
        files = [path for path in (ROOT / "docs/liora-venn/v672-v6").rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)
        for path in files:
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            if path.suffix.lower() in {".md", ".json", ".html", ".yaml", ".yml"}:
                self.assertLessEqual(len(re.findall(r"\S+", path.read_text(encoding="utf-8"))), 100000, path.as_posix())

    def test_public_owner_documents_have_no_private_absolute_paths_or_raw_task_ids(self) -> None:
        patterns = [
            re.compile(r"[A-Za-z]:\\\\"),
            re.compile(r"C:/Users/", re.I),
            re.compile(r"D:/GHC-Archives/", re.I),
            re.compile(r"019[a-f0-9]{5,}-[a-f0-9-]{12,}", re.I),
        ]
        for path in (ROOT / "docs/liora-venn/v672-v6").rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                for pattern in patterns:
                    self.assertIsNone(pattern.search(text), f"{pattern.pattern} in {path}")

    def test_evidence_staged_review_and_manifest_match_exact_index(self) -> None:
        review = load("docs/liora-venn/v672-v6/validation/evidence-staged-review.json")
        manifest = load("docs/liora-venn/v672-v6/validation/evidence-manifest.json")
        staged = set(filter(None, git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()))
        declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
        self.assertTrue(review["valid"])
        self.assertEqual(review["deletions"], [])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["frozen_x1_changes"], [])
        self.assertEqual(staged, declared)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["self_exclusions"]), 2)
        for row in manifest["entries"]:
            data = git("show", f":{row['path']}").stdout
            self.assertEqual(git_text("rev-parse", f":{row['path']}"), row["git_blob_oid"])
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])

    def test_staged_evidence_has_zero_deletions_and_no_frozen_x1(self) -> None:
        self.assertEqual(git_text("diff", "--cached", "--name-only", "--diff-filter=D"), "")
        staged = git_text("diff", "--cached", "--name-only").splitlines()
        self.assertFalse(any(path.startswith("docs/liora-venn/v672-v6/x1/") for path in staged))
        self.assertFalse(any(path.endswith("_x1.py") for path in staged))


if __name__ == "__main__":
    unittest.main()

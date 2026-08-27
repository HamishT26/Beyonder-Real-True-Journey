"""Owner-self-scoped planning-only tests for Liora Venn v672-v6 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_liora_venn_v672_v6_x1 as x1


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


class LioraVennV672V6X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.charter = load("docs/liora-venn/v672-v6/x1/phase-charter.json")
        cls.intake = load("docs/liora-venn/v672-v6/x1/activation-intake.json")
        cls.proposals = load("docs/liora-venn/v672-v6/x1/proposal-freeze.json")
        cls.portfolio = load("docs/liora-venn/v672-v6/x1/portfolio-freeze.json")
        cls.audit = load("docs/liora-venn/v672-v6/x1/semantic-neighbor-audit.json")
        cls.method_flow = load("docs/liora-venn/v672-v6/x1/method-flow-startup.json")
        cls.flashcards = load("docs/liora-venn/v672-v6/x1/flashcards.json")
        cls.source = load("docs/liora-venn/v672-v6/x1/source-revalidation.json")
        cls.sources = load("docs/liora-venn/v672-v6/x1/source-ledger.json")

    def test_exact_branch_and_source_head(self) -> None:
        self.assertEqual(git_text("branch", "--show-current"), x1.BRANCH)
        self.assertEqual(git_text("rev-parse", "HEAD"), x1.SOURCE_FINAL)
        self.assertEqual(self.charter["source_exact_final"], x1.SOURCE_FINAL)

    def test_identity_is_relational_working_language_only(self) -> None:
        identity = load("docs/liora-venn/v672-v6/x1/identity-and-boundary.json")
        self.assertTrue(identity["relational_working_language_only"])
        self.assertEqual(identity["owner"], "Liora Venn")
        self.assertEqual(identity["pronouns"], "she/they")
        for word in ("consciousness", "personhood", "employment", "authority"):
            self.assertIn(word, identity["claims_disallowed"])

    def test_x1_is_planning_only(self) -> None:
        self.assertTrue(self.charter["x1_planning_only"])
        self.assertFalse(self.charter["x2_outcomes_observed"])
        self.assertFalse(self.charter["successor_contacted"])
        self.assertFalse(self.intake["fast_mode_claimed"])
        self.assertEqual(self.charter["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse((ROOT / "docs/liora-venn/v672-v6/x2").exists())

    def test_exact_source_ancestry_and_four_way_equality(self) -> None:
        self.assertEqual(
            self.source["direct_parents"],
            {"x1_parent": x1.SOURCE_PREDECESSOR, "evidence_parent": x1.SOURCE_X1, "final_parent": x1.SOURCE_EVIDENCE},
        )
        self.assertEqual(self.source["phase_commit_count"], 3)
        self.assertEqual(self.source["merge_count"], 0)
        self.assertEqual(self.source["final_parent_count"], 1)
        self.assertTrue(self.source["four_way_equal"])
        self.assertEqual(self.source["typed_divergence"], {"ahead": 0, "behind": 0})

    def test_source_manifests_and_content_seal(self) -> None:
        replay = self.source["manifest_and_seal_replay"]
        self.assertTrue(replay["all_manifests_valid"])
        self.assertEqual([row["entries"] for row in replay["manifests"]], [22, 117, 19, 163])
        self.assertEqual([row["self_exclusions"] for row in replay["manifests"]], [2, 3, 6, 6])
        self.assertTrue(replay["content_seal_valid"])
        self.assertEqual(replay["content_seal_targets"], 10)

    def test_inherited_canonical_is_not_replayed_or_credited(self) -> None:
        self.assertEqual(self.source["external_canonical_receipt_sha256"], x1.SOURCE_CANONICAL_SHA256)
        self.assertEqual(self.source["external_canonical_status"], "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL")
        self.assertEqual(self.source["external_canonical_invocations"], 1)
        self.assertEqual(self.source["external_canonical_successes"], 1)
        self.assertFalse(self.source["external_canonical_replayed_by_liora"])
        self.assertEqual(self.source["full_repository_suite"], "not_run_not_claimed")

    def test_proposal_count_fields_and_outcomes(self) -> None:
        rows = self.proposals["new_proposals"]
        self.assertEqual(len(rows), 40)
        self.assertEqual(self.proposals["new_declared_chain_total"], 6150)
        self.assertEqual(
            Counter(row["expected_disposition"] for row in rows),
            Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}),
        )
        self.assertEqual(self.proposals["expected_outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(sorted(set(row["expected_disposition"] for row in rows)), sorted(x1.ALLOWED_OUTCOMES))
        self.assertFalse(self.proposals["outcomes_observed"])

    def test_every_proposal_has_required_preregistered_fields(self) -> None:
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane",
            "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        ids = []
        for index, row in enumerate(self.proposals["new_proposals"], 1):
            self.assertTrue(required.issubset(row))
            self.assertEqual(row["proposal_id"], f"LV6726-N{index:03d}")
            self.assertTrue(row["x1_planning_only"])
            self.assertEqual(row["x2_execution_count"], 0)
            self.assertEqual(row["completion_credit"], 0)
            self.assertEqual(len(row["concrete_artifacts"]), 2)
            self.assertEqual(len(row["protected_gates"]), len(x1.PROTECTED_GATES))
            ids.append(row["proposal_id"])
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_160_rejecting_mutations_are_preregistered_only(self) -> None:
        mutations = [mutation for row in self.proposals["new_proposals"] for mutation in row["negative_fixtures"]]
        self.assertEqual(len(mutations), 160)
        self.assertEqual(len({row["mutation_id"] for row in mutations}), 160)
        self.assertEqual({row["state"] for row in mutations}, {"preregistered_not_executed"})

    def test_source_bounded_novelty_audit_refuses_universal_claim(self) -> None:
        self.assertEqual(self.audit["declared_chain_rows"], 6110)
        self.assertEqual(self.audit["reachable_proposal_json_paths"], 1667)
        self.assertEqual(self.audit["parsed_documents"], 1667)
        self.assertEqual(self.audit["parse_failures"], [])
        self.assertEqual(self.audit["unique_reachable_proposal_rows"], 2055)
        self.assertFalse(self.audit["universal_novelty_claim"])
        self.assertEqual(self.audit["selected_phrase_matching_file_counts"], {"marbled paper": 0, "paper marbling": 0, "suminagashi": 0})
        self.assertEqual(len(self.audit["candidates"]), 40)
        self.assertTrue(all(not row["exact_title_matches"] for row in self.audit["candidates"]))
        self.assertTrue(all(row["bounded_novelty_disposition"] == "owner_new_after_source_bounded_review" for row in self.audit["candidates"]))

    def test_portfolio_floors_are_frozen_without_credit(self) -> None:
        self.assertEqual(
            self.portfolio["counts"],
            {"safe_now": 60, "bounded_candidates": 30, "exact_approval": 20, "blocked": 10, "skills": 20, "runners": 10, "clean_fix_refine": 60},
        )
        for key in ("safe_now", "bounded_candidates", "exact_approval", "blocked", "skills", "runners", "clean_fix_refine"):
            self.assertTrue(all(row["completion_credit"] == 0 for row in self.portfolio[key]))
        self.assertTrue(self.portfolio["caps_are_ceilings_not_quotas"])

    def test_skills_and_runners_remain_unbuilt_in_x1(self) -> None:
        self.assertEqual({row["state"] for row in self.portfolio["skills"]}, {"planned_not_initialized"})
        self.assertTrue(all(row["global_install"] is False for row in self.portfolio["skills"]))
        self.assertEqual({row["state"] for row in self.portfolio["runners"]}, {"planned_not_built"})
        self.assertTrue(all(row["name"].startswith("ghc_family_liora_v672_v6_") for row in self.portfolio["runners"]))

    def test_method_flow_retains_every_startup_failure(self) -> None:
        self.assertEqual(self.method_flow["counts"]["methods"], 8)
        self.assertEqual(self.method_flow["counts"]["witness_results"], {"fail": 11, "pass": 8})
        failures = [row for row in self.method_flow["witnesses"] if row["result"] == "fail"]
        passes = [row for row in self.method_flow["witnesses"] if row["result"] == "pass"]
        self.assertEqual(len(failures), 11)
        self.assertEqual(len(passes), 8)
        self.assertEqual(
            {negative for row in failures for negative in row["retained_negative_ids"]},
            {row["negative_id"] for row in x1.FAILURES},
        )
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in self.method_flow["methods"]))

    def test_startup_overlay_preserves_repository_sealed_counts(self) -> None:
        overlay = self.method_flow["activation_overlay"]
        self.assertEqual(overlay["repository_sealed_source_counts_unchanged"], x1.ACTIVATION_COUNTS)
        self.assertEqual(
            overlay["effective_after_startup"],
            {"effective_negatives": 35613, "effective_methods": 22015, "failed_witnesses": 7274, "bounded_passing_witnesses": 9322, "open_gaps": 285, "exact_gates": 278},
        )

    def test_flashcards_have_exact_four_tiers_and_thirteen_modules(self) -> None:
        self.assertEqual(self.flashcards["tier_order"], ["identity", "pillar", "practice", "task"])
        self.assertEqual(self.flashcards["module_count"], 13)
        self.assertEqual(self.flashcards["card_count"], 52)
        by_module = Counter(row["module"] for row in self.flashcards["cards"])
        self.assertEqual(set(by_module.values()), {4})
        self.assertTrue(all(row["x1_planning_only"] for row in self.flashcards["cards"]))

    def test_official_sources_are_vocabulary_only(self) -> None:
        self.assertEqual(len(self.sources["sources"]), 7)
        allowed_hosts = {"www.vam.ac.uk", "blog.library.si.edu", "www.osha.gov", "www.w3.org", "www.rfc-editor.org"}
        for row in self.sources["sources"]:
            host = re.match(r"https://([^/]+)/", row["url"]).group(1)
            self.assertIn(host, allowed_hosts)
            self.assertIn("only", row["use"])
        self.assertFalse(self.sources["citations_are_observations"])
        self.assertFalse(self.sources["citations_confer_authority"])

    def test_environment_versions_performed_no_mutation(self) -> None:
        environment = load("docs/liora-venn/v672-v6/x1/environment-versions.json")
        self.assertTrue(environment["python"])
        self.assertIn("git version", environment["git"])
        self.assertTrue(environment["powershell"])
        self.assertEqual(environment["updates_performed"], [])
        self.assertEqual(environment["installs_performed"], [])
        self.assertFalse(environment["elevation"])
        self.assertFalse(environment["windows_features_changed"])
        self.assertFalse(environment["reboot"])

    def test_owner_documents_are_below_word_and_file_ceilings(self) -> None:
        files = [path for path in (ROOT / "docs/liora-venn/v672-v6").rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)
        for path in files:
            if path.suffix.lower() in {".md", ".json", ".html", ".yaml", ".yml"}:
                words = len(re.findall(r"\S+", path.read_text(encoding="utf-8")))
                self.assertLessEqual(words, 100000, path.as_posix())

    def test_public_owner_artifacts_contain_no_private_routes_or_raw_ids(self) -> None:
        forbidden = [
            re.compile(r"[A-Za-z]:\\\\"),
            re.compile(r"C:/Users/", re.I),
            re.compile(r"D:/GHC-Archives/", re.I),
            re.compile(r"019[a-f0-9]{5,}-[a-f0-9-]{12,}", re.I),
            re.compile(r"(?i)(api[_-]?key|access[_-]?token|password)\s*[:=]\s*[^\s\"']+"),
        ]
        paths = [path for path in (ROOT / "docs/liora-venn/v672-v6").rglob("*") if path.is_file()]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for pattern in forbidden:
                self.assertIsNone(pattern.search(text), f"{pattern.pattern} in {path}")

    def test_x1_staged_review_and_git_blob_manifest(self) -> None:
        review = load("docs/liora-venn/v672-v6/validation/x1-staged-review.json")
        manifest = load("docs/liora-venn/v672-v6/validation/x1-manifest.json")
        staged = set(filter(None, git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()))
        declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["forbidden_x2_or_closeout_paths"], [])
        self.assertEqual(review["deletions"], [])
        self.assertEqual(staged, declared)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["self_exclusions"]), 2)
        for row in manifest["entries"]:
            data = git("show", f":{row['path']}").stdout
            self.assertEqual(git_text("rev-parse", f":{row['path']}"), row["git_blob_oid"])
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])

    def test_staged_surface_has_no_deletes_or_x2(self) -> None:
        deleted = git_text("diff", "--cached", "--name-only", "--diff-filter=D")
        staged = git_text("diff", "--cached", "--name-only")
        self.assertEqual(deleted, "")
        self.assertNotIn("/x2/", staged)
        self.assertNotIn("_x2.py", staged)


if __name__ == "__main__":
    unittest.main()

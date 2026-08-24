from __future__ import annotations

import ast
import hashlib
import json
import pathlib
import re
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "orin-thale" / "v668-v7"
X1_HEAD = "95fd7625d1d7ab00816561aa3976441f399bb2d8"
SOURCE = "8b4c6de2c4ae00c876ffb1342fc6614ef901ab73"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True).stdout


class OrinX2EvidenceTests(unittest.TestCase):
    def test_frozen_x1_parent_and_source_remain_ancestral(self) -> None:
        self.assertEqual(git_bytes("rev-parse", f"{X1_HEAD}^").decode().strip(), SOURCE)
        self.assertEqual(git_bytes("merge-base", "--is-ancestor", X1_HEAD, "HEAD"), b"")

    def test_x1_commit_contains_no_x2_path(self) -> None:
        changed = git_bytes("diff-tree", "--no-commit-id", "--name-only", "-r", X1_HEAD).decode().splitlines()
        self.assertFalse(any("/x2/" in path or "/evidence/" in path for path in changed))

    def test_outcome_vocabulary_and_counts_are_exact(self) -> None:
        ledger = load("x2/evidence/outcome-ledger.json")
        self.assertEqual(ledger["counts"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(len(ledger["rows"]), 40)
        self.assertEqual({row["outcome"] for row in ledger["rows"]}, {"completed", "represented", "open_gap", "exact_gate"})

    def test_all_positive_witnesses_accept_without_protected_promotion(self) -> None:
        rows = load("x2/evidence/outcome-ledger.json")["rows"]
        self.assertTrue(all(row["positive_witness"]["accepted"] for row in rows))
        self.assertTrue(all(row["positive_fixture"]["protected_claims"] == [] for row in rows))
        self.assertEqual(sum(row["positive_witness"]["completion_credit"] for row in rows), 28)

    def test_all_160_mutations_executed_and_rejected(self) -> None:
        rows = []
        for path in sorted((PHASE_ROOT / "x2" / "mutations").glob("*.json")):
            rows.extend(json.loads(path.read_text(encoding="utf-8"))["rows"])
        self.assertEqual(len(rows), 160)
        self.assertTrue(all(row["result"] == "rejected" and not row["accepted"] and row["credit"] == 0 for row in rows))
        self.assertEqual(len({row["mutation_id"] for row in rows}), 160)

    def test_gwosc_adapter_is_zero_row_open_gap(self) -> None:
        adapter = load("x2/evidence/GWOSC-zero-row-adapter.json")
        self.assertEqual(adapter["outcome"], "open_gap")
        for field in ("network_requests", "files_downloaded", "real_rows", "strain_samples", "likelihood_evaluations", "posterior_samples", "parameter_constraints"):
            self.assertEqual(adapter[field], 0)

    def test_gmut_board_is_formal_only(self) -> None:
        board = load("x2/evidence/gmut-microlocal-obligation-board.json")
        self.assertEqual(board["outcome"], "completed")
        self.assertEqual(board["symbolic_calculations"], 0)
        self.assertEqual(board["physical_predictions"], 0)
        self.assertEqual(board["observation_firewall"], "closed")

    def test_thos_remains_represented_without_people_or_effect(self) -> None:
        board = load("x2/evidence/thos-binding-workboard.json")
        self.assertEqual(board["outcome"], "represented")
        self.assertEqual(board["real_people"], 0)
        self.assertEqual(board["blind_matched_budget_arms"], 0)
        self.assertEqual(board["effectiveness_estimates"], 0)

    def test_freed_id_and_cbr_have_zero_real_lifecycle_or_authority(self) -> None:
        board = load("x2/evidence/freed-id-cbr-boundary.json")
        for field in ("real_keys", "real_proofs", "live_identity_events", "authority_decisions", "Maori_authority_decisions"):
            self.assertEqual(board[field], 0)

    def test_skills_are_customized_validated_and_smoke_used(self) -> None:
        receipt = load("x2/evidence/skill-receipts.json")
        self.assertEqual(receipt["count"], 20)
        for row in receipt["rows"]:
            self.assertTrue(row["initialized_through_skill_creator"])
            self.assertEqual(row["quick_validation"]["return_code"], 0)
            self.assertEqual(row["accepting_smoke"]["return_code"], 0)
            self.assertEqual(row["rejecting_smoke"]["return_code"], 2)
            skill = PHASE_ROOT / "x2" / "skills" / row["name"] / "SKILL.md"
            text = skill.read_text(encoding="utf-8")
            self.assertNotIn("[TODO", text)
            self.assertIn("## Refusal boundary", text)

    def test_family_current_runners_accept_and_reject(self) -> None:
        receipt = load("x2/evidence/runner-receipts.json")
        self.assertEqual(receipt["count"], 10)
        self.assertTrue(all(row["family_current"] for row in receipt["rows"]))
        self.assertTrue(all(row["accepting_smoke"]["return_code"] == 0 for row in receipt["rows"]))
        self.assertTrue(all(row["rejecting_smoke"]["return_code"] == 2 for row in receipt["rows"]))

    def test_portfolio_execution_and_held_packets_are_exact(self) -> None:
        summary = load("x2/evidence/portfolio-execution-summary.json")
        self.assertEqual(summary["counts"], {"blocked": 10, "candidates": 30, "clean_fix_refine": 60, "exact_approval": 20, "runners": 10, "safe_now": 60, "skills": 20})
        self.assertTrue(summary["under_1000_ceiling"])
        self.assertTrue(summary["exact_and_blocked_unexecuted"])
        for category in ("exact_approval", "blocked"):
            rows = load(f"x2/portfolio/{category}.json")["rows"]
            self.assertTrue(all(row["state"] == "held_unexecuted" and row["completion_credit"] == 0 for row in rows))

    def test_method_flow_preserves_each_failure_and_recovery(self) -> None:
        ledger = load("method-flow/x2-operational.json")
        methods = ledger["counts"]["methods"]
        self.assertGreaterEqual(methods, 12)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": methods, "pass": methods})
        self.assertEqual(ledger["counts"]["states"]["preferred"], methods)

    def test_effective_counts_are_additive_and_terminal_not_ready(self) -> None:
        truth = load("x2/evidence/phase-truth.json")
        methods = load("method-flow/x2-operational.json")["counts"]["methods"]
        self.assertEqual(truth["effective_negatives"], 29964 + methods + 160)
        self.assertEqual(truth["effective_methods"], 16550 + methods)
        self.assertEqual(truth["failed_witnesses"], 2265 + methods)
        self.assertEqual(truth["bounded_passing_witnesses"], 3092 + methods)
        self.assertEqual(truth["open_gaps"], 221)
        self.assertEqual(truth["exact_gates"], 216)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["canonical_validation"], "not_run")

    def test_source_use_is_vocabulary_only_and_zero_observation(self) -> None:
        receipt = load("x2/evidence/source-use-receipt.json")
        self.assertEqual(receipt["real_observation_rows"], 0)
        self.assertEqual(receipt["participant_rows"], 0)
        self.assertEqual(receipt["authority_decisions"], 0)
        self.assertFalse(receipt["independent_review"])

    def test_evidence_manifest_covers_exact_declared_surface(self) -> None:
        manifest = load("x2/evidence/evidence-content-manifest.json")
        allowlist = load("validation/x2-staged-allowlist.json")
        expected = set(allowlist["intended_paths_before_manifest"])
        expected.add("docs/orin-thale/v668-v7/validation/x2-staged-allowlist.json")
        self.assertEqual({row["path"] for row in manifest["entries"]}, expected)
        self.assertEqual(manifest["entry_count"], len(expected))
        self.assertEqual(manifest["self_exclusions"], allowlist["self_exclusions"])
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            oid = subprocess.run(
                ["git", "-C", str(ROOT), "hash-object", "-w", f"--path={row['path']}", "--stdin"],
                input=path.read_bytes(),
                check=True,
                capture_output=True,
            ).stdout.decode().strip()
            data = git_bytes("cat-file", "blob", oid)
            self.assertEqual(oid, row["git_blob_oid"])
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])

    def test_all_json_parses_and_phase_documents_remain_bounded(self) -> None:
        for path in PHASE_ROOT.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))
        for path in PHASE_ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt", ".html"}:
                words = len(re.findall(r"\b\w+[\w'-]*\b", path.read_text(encoding="utf-8")))
                self.assertLessEqual(words, 6000, path.as_posix())

    def test_changed_python_is_ast_parseable_and_has_no_unsafe_shell(self) -> None:
        paths = [ROOT / "scripts" / "ghc_family_orin_thale_v668_v7_x2.py", ROOT / "scripts" / "ghc_family_orin_thale_v668_v7_skill_smoke.py", ROOT / "scripts" / "build_ghc_family_orin_thale_v668_v7_x2.py"]
        paths.extend(ROOT / row["path"] for row in load("x2/evidence/runner-receipts.json")["rows"])
        for path in paths:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    self.assertFalse(any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords))

    def test_public_x2_surface_excludes_private_material(self) -> None:
        patterns = [
            re.compile(r"<codex_delegation>", re.I),
            re.compile(r"source_thread_id\s*[:=]", re.I),
            re.compile(r"\b[A-Z]:\\Users\\[^\s\"']+", re.I),
            re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        ]
        hits = []
        for path in (PHASE_ROOT / "x2").rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}:
                text = path.read_text(encoding="utf-8")
                for pattern in patterns:
                    if pattern.search(text):
                        hits.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()

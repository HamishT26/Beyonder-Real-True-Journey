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


def git(*args: str, text: bool = True) -> str | bytes:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )
    return completed.stdout.strip() if text else completed.stdout


class ElowenCairnV669V2X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.phase_root = ROOT / archive.REL_PHASE_ROOT

    def read_json(self, relative: str) -> dict:
        return json.loads((self.phase_root / relative).read_text(encoding="utf-8"))

    def owner_paths(self) -> list[Path]:
        return archive.phase_owner_files()

    def proposal_rows(self) -> list[dict]:
        freeze = self.read_json("x1/proposal-freeze.json")
        rows: list[dict] = []
        for path in freeze["shards"]:
            rows.extend(json.loads((ROOT / path).read_text(encoding="utf-8"))["rows"])
        return rows

    def test_01_branch_source_and_planning_tree(self) -> None:
        self.assertEqual(git("branch", "--show-current"), archive.BRANCH)
        self.assertEqual(git("rev-parse", "HEAD"), archive.SOURCE_FINAL)
        self.assertTrue(all("/x2/" not in path.relative_to(ROOT).as_posix() for path in self.owner_paths()))

    def test_02_phase_truth_is_planning_only(self) -> None:
        truth = self.read_json("x1/phase-truth.json")
        self.assertEqual(truth["lifecycle"], "X1_PLANNING_CANDIDATE_NOT_COMMITTED")
        self.assertEqual(truth["observed_outcomes"], {label: 0 for label in archive.ALLOWED_OUTCOMES})
        self.assertEqual(truth["canonical_validation"], "not_run")
        self.assertIsNone(truth["x1"])

    def test_03_proposal_freeze_counts_and_labels(self) -> None:
        rows = self.proposal_rows()
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 40)
        self.assertEqual(
            Counter(row["expected_disposition"] for row in rows),
            {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        )
        self.assertEqual(sum(len(row["negative_fixtures"]) for row in rows), 160)

    def test_04_every_proposal_has_complete_preregistration(self) -> None:
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
            "execution_lane", "official_or_primary_source_needs", "concrete_artifacts",
            "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        for row in self.proposal_rows():
            self.assertTrue(required <= set(row), row["proposal_id"])
            self.assertEqual(row["x1_completion_credit"], 0)
            self.assertIsNone(row["observed_disposition"])
            self.assertEqual(len(row["negative_fixtures"]), 4)
            self.assertEqual({item["expected"] for item in row["negative_fixtures"]}, {"reject"})

    def test_05_novelty_inventory_is_honest_and_reproducible(self) -> None:
        audit = self.read_json("x1/semantic-novelty-audit.json")
        self.assertEqual(audit["declared_inherited_frozen_proposals"], 4950)
        self.assertEqual(audit["recovered_rows"], 1380)
        self.assertEqual(audit["recovered_unique_normalized_titles"], 1379)
        self.assertEqual(audit["unrecovered_declared_rows"], 3570)
        self.assertEqual(audit["exact_title_collisions"], 0)
        self.assertEqual(audit["quarantined_proposals"], 0)
        self.assertLess(audit["maximum_neighbor"]["neighbor"]["score"], 0.75)
        self.assertTrue(audit["unavailable_history_is_open_gap"])
        self.assertFalse(audit["universal_novelty_claim"])

    def test_06_portfolio_floors_and_holds(self) -> None:
        actual = {}
        for category, count in archive.PORTFOLIO_COUNTS.items():
            doc = self.read_json(f"x1/portfolios/{category}.json")
            actual[category] = len(doc["rows"])
            self.assertEqual(doc["count"], count)
        self.assertEqual(actual, archive.PORTFOLIO_COUNTS)
        for category in ("exact_approval", "blocked"):
            self.assertTrue(all(row["execution_state"] == "held_unexecuted" for row in self.read_json(f"x1/portfolios/{category}.json")["rows"]))

    def test_07_successor_recommendations_are_zero_credit_seeds(self) -> None:
        doc = self.read_json("x1/successor-recommendations-freeze.json")
        self.assertEqual(doc["counts"], {"candidate": 15, "skill": 10, "runner": 10, "clean_fix_refine": 30})
        for category in doc["counts"]:
            self.assertTrue(all(row["completion_credit"] == 0 for row in doc[category]))
        self.assertIn("no task is created", doc["boundary"])

    def test_08_source_ledger_preserves_credit_boundaries(self) -> None:
        doc = self.read_json("x1/source-ledger.json")
        self.assertEqual(len(doc["sources"]), 11)
        self.assertEqual(len({row["source_id"] for row in doc["sources"]}), 11)
        self.assertTrue(all(row["credit_boundary"] and row["url"].startswith("https://") for row in doc["sources"]))
        self.assertEqual(doc["network_requests_during_x1_source_review"], 3)

    def test_09_method_flow_is_complete_and_append_only(self) -> None:
        ledger = self.read_json("method-flow/x1-ledger.json")
        self.assertEqual(len(ledger["methods"]), len(archive.STARTUP_FAILURES))
        self.assertEqual(
            Counter(row["result"] for row in ledger["witnesses"]),
            {"fail": len(archive.STARTUP_FAILURES), "pass": len(archive.STARTUP_FAILURES)},
        )
        witness_ids = {row["witness_id"] for row in ledger["witnesses"]}
        self.assertTrue(all(set(row["validation_witness_ids"]) <= witness_ids for row in ledger["methods"]))
        self.assertEqual(len(ledger["state_events"]), 4 * len(archive.STARTUP_FAILURES))

    def test_10_overlay_arithmetic_retains_every_failure(self) -> None:
        truth = self.read_json("x1/phase-truth.json")
        for key, expected in archive.ACTIVATION_OVERLAY.items():
            self.assertEqual(truth[key], expected)

    def test_11_route_and_workflow_remain_unexecuted(self) -> None:
        route = self.read_json("x1/route-state.json")
        workflow = self.read_json("x1/workflow-plan-freeze.json")
        self.assertEqual(route["delivery_state"], "NO_ROUTE_ACTION_DURING_X1")
        self.assertFalse(route["successor_contacted"])
        self.assertFalse(route["standby_contacted"])
        self.assertEqual(workflow["plan"][1]["state"], "not_started")
        self.assertTrue(workflow["strict_x1_before_x2"])

    def test_12_git_blob_manifest_replays_exactly(self) -> None:
        manifest = self.read_json("validation/x1-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = git("show", f":{entry['path']}", text=False)
            oid = git("rev-parse", f":{entry['path']}")
            self.assertEqual(oid, entry["git_blob_oid"])
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_13_documents_stay_under_declared_ceilings(self) -> None:
        words = {}
        for path in self.owner_paths():
            if path.suffix.lower() in {".md", ".html", ".txt"}:
                words[path.relative_to(ROOT).as_posix()] = len(re.findall(r"\S+", path.read_text(encoding="utf-8")))
        self.assertTrue(words)
        self.assertLessEqual(max(words.values()), archive.DOCUMENT_WORD_CEILING)
        overview = (archive.REL_PHASE_ROOT / "x1/integrated-overview.md").as_posix()
        self.assertGreaterEqual(words[overview], 1500)
        self.assertLess(len(self.owner_paths()), archive.FILE_CEILING)

    def test_14_no_private_route_or_raw_identifier_payload(self) -> None:
        patterns = [
            re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
            re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
            re.compile(r"(?i)\b[A-Z]:\\(?:Users|Documents and Settings)\\[^\\\s]+"),
            re.compile(r"(?i)(?:source_" + r"thread_id|private_" + r"callable_identifier|codex" + r"Delegation|resume_" + r"value)"),
            re.compile(r"(?i)(?:password|secret|api[_-]?key|bearer|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
        ]
        candidates = []
        for path in self.owner_paths():
            if path.suffix.lower() not in {".json", ".md", ".html", ".yaml", ".yml", ".py", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8")
            candidates.extend((path, match.group(0)) for pattern in patterns for match in pattern.finditer(text))
        self.assertEqual(candidates, [])

    def test_15_changed_python_has_no_high_risk_execution_surface(self) -> None:
        banned = {"requests", "urllib3", "httpx", "socket", "winreg"}
        findings = []
        for path in self.owner_paths():
            if path.suffix != ".py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    findings.extend(alias.name for alias in node.names if alias.name.split(".")[0] in banned)
                if isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] in banned:
                    findings.append(node.module)
                if isinstance(node, ast.Call):
                    for keyword in node.keywords:
                        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                            findings.append("shell_true")
        self.assertEqual(findings, [])

    def test_16_boundaries_and_verdict_are_present(self) -> None:
        overview = (self.phase_root / "x1/integrated-overview.md").read_text(encoding="utf-8")
        for term in ("GMUT", "THOS", "Freed ID", "CBR", "Māori authority", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(term, overview)
        self.assertIn(archive.IDENTITY_BOUNDARY, overview)
        self.assertEqual(self.read_json("x1/phase-truth.json")["terminal_verdict"], archive.TERMINAL_VERDICT)


if __name__ == "__main__":
    unittest.main()

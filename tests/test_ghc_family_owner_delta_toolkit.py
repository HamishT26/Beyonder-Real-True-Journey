from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "ghc_family_owner_delta_toolkit.py"
SPEC = importlib.util.spec_from_file_location("owner_delta_toolkit", MODULE_PATH)
assert SPEC and SPEC.loader
toolkit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(toolkit)


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


class RepoFixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        git(self.root, "init")
        git(self.root, "config", "user.email", "fixture@example.invalid")
        git(self.root, "config", "user.name", "Fixture")
        (self.root / "base.txt").write_text("base\n", encoding="utf-8")
        git(self.root, "add", "base.txt")
        git(self.root, "commit", "-m", "base")
        self.source = git(self.root, "rev-parse", "HEAD")

    def commit_delta(self) -> str:
        (self.root / "docs").mkdir(exist_ok=True)
        (self.root / "scripts").mkdir(exist_ok=True)
        (self.root / "docs" / "record.json").write_text(
            json.dumps({"outcome": "completed"}) + "\n", encoding="utf-8"
        )
        (self.root / "docs" / "note.md").write_text("# Note\n\nBounded evidence.\n", encoding="utf-8")
        (self.root / "scripts" / "ok.py").write_text("VALUE = 1\n", encoding="utf-8")
        git(self.root, "add", "docs", "scripts")
        git(self.root, "commit", "-m", "delta")
        return git(self.root, "rev-parse", "HEAD")

    def close(self) -> None:
        self.temp.cleanup()


class PathContractTests(unittest.TestCase):
    def test_normalize_relative_accepts_literal_path(self) -> None:
        self.assertEqual(toolkit.normalize_relative("docs/a.json"), "docs/a.json")

    def test_normalize_relative_rejects_parent_traversal(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_relative("../secret")

    def test_normalize_relative_rejects_drive_path(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.normalize_relative("C:\\private\\x")

    def test_ensure_unique_rejects_duplicates(self) -> None:
        with self.assertRaises(toolkit.DeltaError):
            toolkit.ensure_unique(["a", "a"], "fixture")


class DeltaFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = RepoFixture()
        self.target = self.fixture.commit_delta()

    def tearDown(self) -> None:
        self.fixture.close()

    def test_resolve_commit_returns_full_id(self) -> None:
        self.assertRegex(toolkit.resolve_commit(self.fixture.root, "HEAD"), r"^[0-9a-f]{40}$")

    def test_delta_rows_are_literal_and_bounded(self) -> None:
        rows = toolkit.delta_rows(self.fixture.root, self.fixture.source, self.target)
        self.assertEqual({row["path"] for row in rows}, {"docs/note.md", "docs/record.json", "scripts/ok.py"})

    def test_manifest_replays_blob_hashes(self) -> None:
        payload = toolkit.manifest_payload(self.fixture.root, self.fixture.source, self.target)
        self.assertEqual(payload["entry_count"], 3)
        self.assertTrue(all(row["sha256"] for row in payload["entries"]))

    def test_json_payload_parses_only_delta_json(self) -> None:
        payload = toolkit.json_payload(self.fixture.root, self.fixture.source, self.target)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["parsed_count"], 1)

    def test_markdown_payload_counts_headings(self) -> None:
        payload = toolkit.markdown_payload(self.fixture.root, self.fixture.source, self.target)
        self.assertEqual(payload["checked_count"], 1)
        self.assertEqual(payload["records"][0]["headings"], 1)

    def test_python_payload_compiles_without_pycache(self) -> None:
        payload = toolkit.python_payload(self.fixture.root, self.fixture.source, self.target)
        self.assertEqual(payload["compiled_count"], 1)
        self.assertFalse((self.fixture.root / "scripts" / "__pycache__").exists())

    def test_privacy_payload_passes_sanitized_fixture(self) -> None:
        payload = toolkit.privacy_payload(self.fixture.root, self.fixture.source, self.target)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["candidate_count"], 0)

    def test_security_payload_passes_bounded_python(self) -> None:
        payload = toolkit.security_payload(self.fixture.root, self.fixture.source, self.target)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["finding_count"], 0)

    def test_file_budget_uses_materialized_files_and_exact_delta(self) -> None:
        payload = toolkit.file_budget_payload(self.fixture.root, self.fixture.source, self.target, 2000)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["owner_delta_file_count"], 3)

    def test_source_must_be_ancestor(self) -> None:
        git(self.fixture.root, "checkout", "--orphan", "unrelated")
        (self.fixture.root / "orphan.txt").write_text("orphan\n", encoding="utf-8")
        git(self.fixture.root, "add", "orphan.txt")
        git(self.fixture.root, "commit", "-m", "orphan")
        unrelated = git(self.fixture.root, "rev-parse", "HEAD")
        with self.assertRaises(toolkit.DeltaError):
            toolkit.delta_rows(self.fixture.root, unrelated, self.target)


class LedgerAndRouteTests(unittest.TestCase):
    def test_data_quality_accepts_only_four_labels(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            path.write_text(
                json.dumps({"records": [{"outcome": label} for label in sorted(toolkit.ALLOWED_OUTCOMES)]}),
                encoding="utf-8",
            )
            payload = toolkit.data_quality_payload([path])
            self.assertTrue(payload["valid"])
            self.assertEqual(sum(payload["outcome_counts"].values()), 4)

    def test_data_quality_rejects_unknown_label(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            path.write_text(json.dumps({"outcome": "done"}), encoding="utf-8")
            payload = toolkit.data_quality_payload([path])
            self.assertFalse(payload["valid"])
            self.assertEqual(payload["unknown_labels"], ["done"])

    def test_skill_hash_payload_sanitizes_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text("---\nname: sample\n---\n", encoding="utf-8")
            payload = toolkit.skill_hash_payload([f"sample-skill={path}"])
            self.assertTrue(payload["paths_sanitized"])
            self.assertNotIn(str(path), json.dumps(payload))

    def test_route_payload_accepts_owner_delta_policy(self) -> None:
        execution = {
            "policy": "owner_self_scoped_delta",
            "current_owner_executor": "Neris Solane",
        }
        active = [
            "Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen",
            "Lyren Moss", "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash",
            "Orin Thale", "Liora Venn", "Tamar Vey", "Elowen Cairn", "Sylven Arc",
            "Caelen Morrow",
        ]
        roster = {
            "active_main_tasks": active,
            "standby_members": [{"relational_name": "Tavian Sol"}],
            "live_route_override": {"repeat_cycle": active},
            "validation_scope": {"execution_authority": execution},
            "current_route": {"current": {"owner": "Neris Solane"}, "next": {"owner": "Vesper Arlen"}},
        }
        auth = {"validation_scope": {"execution_authority": execution}}
        with tempfile.TemporaryDirectory() as directory:
            roster_path = Path(directory) / "roster.json"
            auth_path = Path(directory) / "auth.json"
            roster_path.write_text(json.dumps(roster), encoding="utf-8")
            auth_path.write_text(json.dumps(auth), encoding="utf-8")
            payload = toolkit.route_payload(roster_path, auth_path)
            self.assertTrue(payload["valid"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

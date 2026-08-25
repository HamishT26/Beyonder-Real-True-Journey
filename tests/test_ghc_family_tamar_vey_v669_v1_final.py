#!/usr/bin/env python3
"""Owner-scoped tests for the Tamar Vey v669-v1 final candidate."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_tamar_vey_v669_v1_final as builder  # noqa: E402
import ghc_family_tamar_vey_v669_v1_archive as archive  # noqa: E402


def git(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=not binary)
    return result.stdout if binary else result.stdout.strip()


class TamarV669V1FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        commits = str(git("rev-list", "--reverse", f"{builder.EVIDENCE_HEAD}..HEAD")).splitlines()
        cls.final_commit = commits[0] if commits else None

    @classmethod
    def read_bytes(cls, relative: str) -> bytes:
        if cls.final_commit:
            return git("show", f"{cls.final_commit}:{relative}", binary=True)  # type: ignore[return-value]
        return (ROOT / relative).read_bytes()

    @classmethod
    def read_json(cls, relative: str) -> dict:
        return json.loads(cls.read_bytes(relative).decode("utf-8"))

    @classmethod
    def phase_json(cls, relative: str) -> dict:
        return cls.read_json(f"{archive.REL_PHASE_ROOT}/{relative}")

    def test_01_direct_parent_lifecycle_and_commit_ceiling(self) -> None:
        self.assertEqual(git("branch", "--show-current"), archive.BRANCH)
        self.assertEqual(git("rev-parse", f"{builder.X1_HEAD}^"), archive.SOURCE_FINAL)
        self.assertEqual(git("rev-parse", f"{builder.EVIDENCE_HEAD}^"), builder.X1_HEAD)
        if self.final_commit:
            self.assertEqual(git("rev-parse", f"{self.final_commit}^"), builder.EVIDENCE_HEAD)
            self.assertEqual(git("rev-list", "--count", f"{archive.SOURCE_FINAL}..{self.final_commit}"), "3")
            self.assertEqual(git("rev-list", "--merges", f"{archive.SOURCE_FINAL}..{self.final_commit}"), "")
            self.assertEqual(len(str(git("rev-list", "--parents", "-n", "1", self.final_commit)).split()), 2)
        else:
            self.assertEqual(git("rev-parse", "HEAD"), builder.EVIDENCE_HEAD)

    def test_02_final_truth_and_counts_are_exact(self) -> None:
        truth = self.phase_json("closeout/phase-truth.json")
        self.assertEqual(truth["source_final"], archive.SOURCE_FINAL)
        self.assertEqual(truth["x1"], builder.X1_HEAD)
        self.assertEqual(truth["evidence"], builder.EVIDENCE_HEAD)
        self.assertEqual(truth["proposal_chain_after"], 4950)
        self.assertEqual(truth["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(truth["mutations"], {"preregistered": 160, "executed": 160, "rejected": 160, "accepted": 0})
        evidence = self.phase_json("x2/evidence/phase-truth.json")
        count = len(builder.FINAL_FAILURES)
        expected = {
            "effective_negatives": evidence["effective_negatives"] + count,
            "methods": evidence["methods"] + count,
            "failed_witnesses": evidence["failed_witnesses"] + count,
            "passing_witnesses": evidence["passing_witnesses"] + count,
            "open_gaps": evidence["open_gaps"],
            "exact_gates": evidence["exact_gates"],
        }
        self.assertEqual({key: truth[key] for key in expected}, expected)
        self.assertEqual(truth["terminal_verdict"], archive.TERMINAL_VERDICT)

    def test_03_source_canonical_and_seal_are_preserved_as_inherited_evidence(self) -> None:
        truth = self.phase_json("closeout/phase-truth.json")
        self.assertEqual(truth["source_terminal_status"], archive.SOURCE_TERMINAL_STATUS)
        self.assertEqual(truth["source_canonical_receipt_sha256"], archive.SOURCE_CANONICAL_RECEIPT_SHA256)
        self.assertEqual(truth["source_canonical_payload_sha256"], archive.SOURCE_CANONICAL_PAYLOAD_SHA256)
        retained = self.phase_json("closeout/retained-negative-register.json")
        self.assertEqual(retained["source_repository_seal"], 30342)
        self.assertTrue(retained["no_failure_erased"])

    def test_04_open_gaps_and_exact_gates_remain_visible(self) -> None:
        register = self.phase_json("closeout/open-exact-gate-register.json")
        evidence = self.phase_json("x2/evidence/phase-truth.json")
        self.assertEqual((register["open_gaps"], register["exact_gates"]), (evidence["open_gaps"], evidence["exact_gates"]))
        self.assertEqual(set(register["new_open_gap_ids"]), {"TV6691-N037", "TV6691-N038"})
        self.assertEqual(set(register["new_exact_gate_ids"]), {"TV6691-N039", "TV6691-N040"})
        self.assertTrue(register["Maori_concepts_remain_under_Maori_authority"])

    def test_05_route_and_handoff_are_prepared_not_sent(self) -> None:
        route = self.phase_json("route/terminal-route-state.json")
        handoff = self.read_bytes(f"{archive.REL_PHASE_ROOT}/handoffs/elowen-cairn-v669-v2-activation-candidate.md").decode("utf-8")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["successor_title"], "Elowen Cairn")
        self.assertEqual(route["successor_phase"], "v669-v2")
        self.assertEqual(route["send_count"], 0)
        self.assertFalse(route["successor_contacted"] or route["successor_precontacted"] or route["successor_task_created"] or route["delivery_acknowledged"])
        self.assertIn("PREPARED_BY_TAMAR_VEY = true", handoff)
        self.assertIn("SENT_BY_TAMAR_VEY = false", handoff)
        self.assertIn("Elowen Cairn", handoff)

    def test_06_canonical_contract_is_pending_once_only(self) -> None:
        contract = self.phase_json("validation/final-canonical-contract.json")
        self.assertEqual(contract["expected_owner_tests"], 49)
        self.assertEqual(contract["canonical_invocations"], 0)
        self.assertEqual(contract["canonical_successes"], 0)
        self.assertFalse(contract["success_replay_allowed"])
        self.assertFalse(contract["full_repository_suite"])
        self.assertEqual(contract["execution_gate"], "only_after_clean_pushed_fresh_live_equal_final")

    def test_07_content_seal_replays_exact_working_or_committed_bytes(self) -> None:
        seal = self.phase_json("seal/content-seal.json")
        self.assertEqual(seal["entry_count"], len(seal["entries"]))
        for row in seal["entries"]:
            data = self.read_bytes(row["path"])
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])
        self.assertEqual(seal["route_state"], "PREPARED_NOT_SENT")
        self.assertEqual(seal["terminal_verdict"], archive.TERMINAL_VERDICT)

    def test_08_final_delta_manifest_matches_exact_allowlist(self) -> None:
        manifest_path = f"{archive.REL_PHASE_ROOT}/validation/final-delta-manifest.json"
        manifest = self.read_json(manifest_path)
        allowlist = self.phase_json("validation/final-staged-allowlist.json")
        self.assertEqual(set(manifest["self_exclusions"]), set(builder.MANIFEST_EXCLUSIONS))
        self.assertEqual(set(allowlist["manifest_exclusions"]), set(builder.MANIFEST_EXCLUSIONS))
        self.assertEqual(set(allowlist["paths"]), {row["path"] for row in manifest["entries"]} | set(builder.MANIFEST_EXCLUSIONS))
        self.assertEqual(manifest["coverage_count"], manifest["entry_count"] + 3)

    def test_09_owner_and_delta_manifests_replay_exact_git_blobs(self) -> None:
        for relative in ("validation/final-owner-manifest.json", "validation/final-delta-manifest.json"):
            manifest = self.phase_json(relative)
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            for row in manifest["entries"]:
                blob = git("cat-file", "blob", row["git_blob_oid"], binary=True)
                self.assertEqual(len(blob), row["bytes"], row["path"])
                self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"], row["path"])
                if self.final_commit:
                    self.assertEqual(git("rev-parse", f"{self.final_commit}:{row['path']}"), row["git_blob_oid"], row["path"])
                else:
                    result = subprocess.run(["git", "-C", str(ROOT), "hash-object", f"--path={row['path']}", "--stdin"], input=(ROOT / row["path"]).read_bytes(), check=True, capture_output=True)
                    self.assertEqual(result.stdout.decode("ascii").strip(), row["git_blob_oid"], row["path"])

    def test_10_final_delta_does_not_rewrite_x1_or_x2(self) -> None:
        manifest = self.phase_json("validation/final-delta-manifest.json")
        for row in manifest["entries"]:
            self.assertNotIn(f"{archive.REL_PHASE_ROOT}/x1/", row["path"])
            self.assertNotIn(f"{archive.REL_PHASE_ROOT}/x2/", row["path"])
            self.assertFalse(row["path"].startswith("docs/liora-venn/"))

    def test_11_all_owner_documents_parse_and_stay_under_ceiling(self) -> None:
        manifest = self.phase_json("validation/final-owner-manifest.json")
        for row in manifest["entries"]:
            path = row["path"]
            suffix = Path(path).suffix.casefold()
            data = self.read_bytes(path)
            if suffix == ".json":
                json.loads(data.decode("utf-8"))
            if path.startswith(f"{archive.REL_PHASE_ROOT}/") and suffix in {".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
                self.assertLessEqual(len(re.findall(r"\b\w+[\w'-]*\b", data.decode("utf-8"))), 6000, path)
        self.assertLess(manifest["coverage_count"], 2000)

    def test_12_owner_python_parses_and_has_no_network_or_shell_surface(self) -> None:
        manifest = self.phase_json("validation/final-owner-manifest.json")
        python_rows = [row for row in manifest["entries"] if row["path"].endswith(".py")]
        self.assertGreaterEqual(len(python_rows), 20)
        for row in python_rows:
            tree = ast.parse(self.read_bytes(row["path"]).decode("utf-8"), filename=row["path"])
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                    self.assertFalse(any(name.split(".")[0] in {"requests", "socket", "urllib", "http", "ftplib"} for name in names), row["path"])
                if isinstance(node, ast.Call):
                    self.assertFalse(any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords), row["path"])

    def test_13_no_private_route_or_raw_identifier_payload(self) -> None:
        manifest = self.phase_json("validation/final-owner-manifest.json")
        text = "\n".join(self.read_bytes(row["path"]).decode("utf-8") for row in manifest["entries"] if Path(row["path"]).suffix.casefold() in {".json", ".md", ".html", ".yaml", ".yml", ".py"})
        tokens = ["<" + "codex" + "_delegation", "source" + "_thread" + "_id", "session" + "_meta.payload.id", "response" + "_item"]
        self.assertTrue(all(token.casefold() not in text.casefold() for token in tokens))
        self.assertNotIn("C:" + chr(92), text)
        self.assertNotIn("D:" + chr(92), text)
        self.assertIsNone(re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", text, re.IGNORECASE))

    def test_14_terminal_checklist_reserves_post_push_gates(self) -> None:
        checklist = self.phase_json("closeout/terminal-checklist.json")
        self.assertIn("one_exact_final_canonical_aggregate", checklist["pending_after_final_commit"])
        self.assertFalse(checklist["successor_contacted"])
        self.assertEqual(checklist["terminal_verdict"], archive.TERMINAL_VERDICT)

    def test_15_overview_preserves_all_pillar_and_authority_boundaries(self) -> None:
        overview = self.read_bytes(f"{archive.REL_PHASE_ROOT}/closeout/final-integrated-overview.md").decode("utf-8")
        for token in ("THOS Body", "Freed ID and CBR Heart", "GMUT Mind", "Māori authority", "same-owner", "not independent reproduction", archive.TERMINAL_VERDICT, "PREPARED_NOT_SENT"):
            self.assertIn(token, overview)


if __name__ == "__main__":
    unittest.main()

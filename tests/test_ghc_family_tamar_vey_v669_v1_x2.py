#!/usr/bin/env python3
"""Owner-scoped tests for Tamar Vey v669-v1 bounded x2 evidence."""

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

import build_ghc_family_tamar_vey_v669_v1_x2 as builder  # noqa: E402
import ghc_family_tamar_vey_v669_v1_archive as archive  # noqa: E402
import ghc_family_tamar_vey_v669_v1_x2 as controls  # noqa: E402


def git(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=not binary)
    return result.stdout if binary else result.stdout.strip()


class TamarV669V1X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        commits = str(git("rev-list", "--reverse", f"{builder.X1_HEAD}..HEAD")).splitlines()
        cls.evidence_commit = commits[0] if commits else None

    @classmethod
    def read_bytes(cls, relative: str) -> bytes:
        if cls.evidence_commit:
            return git("show", f"{cls.evidence_commit}:{relative}", binary=True)  # type: ignore[return-value]
        return (ROOT / relative).read_bytes()

    @classmethod
    def read_json(cls, relative: str) -> dict:
        return json.loads(cls.read_bytes(relative).decode("utf-8"))

    @classmethod
    def x2_paths(cls) -> list[str]:
        if cls.evidence_commit:
            changed = str(git("diff-tree", "--no-commit-id", "--name-only", "-r", cls.evidence_commit)).splitlines()
            return sorted(changed)
        allowlist = cls.read_json(f"{archive.REL_PHASE_ROOT}/validation/x2-staged-allowlist.json")
        return sorted(allowlist["paths"])

    @classmethod
    def outcome_rows(cls) -> list[dict]:
        return cls.read_json(f"{archive.REL_PHASE_ROOT}/x2/evidence/outcome-ledger.json")["rows"]

    def test_01_lifecycle_starts_after_immutable_x1(self) -> None:
        self.assertEqual(git("branch", "--show-current"), archive.BRANCH)
        self.assertEqual(git("rev-parse", f"{builder.X1_HEAD}^"), archive.SOURCE_FINAL)
        if self.evidence_commit:
            self.assertEqual(git("rev-parse", f"{self.evidence_commit}^"), builder.X1_HEAD)
            self.assertEqual(git("rev-list", "--merges", f"{builder.X1_HEAD}..{self.evidence_commit}"), "")
        else:
            self.assertEqual(git("rev-parse", "HEAD"), builder.X1_HEAD)
        self.assertEqual(git("ls-tree", "-r", "--name-only", builder.X1_HEAD, "--", f"{archive.REL_PHASE_ROOT}/x2"), "")

    def test_02_outcomes_use_only_four_labels(self) -> None:
        rows = self.outcome_rows()
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 40)
        counts = Counter(row["outcome"] for row in rows)
        self.assertEqual(counts, Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}))
        self.assertEqual(set(counts), set(archive.ALLOWED_OUTCOMES))
        self.assertEqual(sum(row["positive_witness"]["completion_credit"] for row in rows), 28)
        self.assertEqual(sum(row["positive_witness"]["representation_credit"] for row in rows), 8)
        self.assertEqual(sum(row["positive_witness"]["open_gap_held"] for row in rows), 2)
        self.assertEqual(sum(row["positive_witness"]["exact_gate_held"] for row in rows), 2)

    def test_03_all_positive_fixtures_are_bounded(self) -> None:
        for row in self.outcome_rows():
            fixture = row["positive_fixture"]
            self.assertEqual(fixture["evidence_class"], "owner_local_synthetic")
            self.assertEqual((fixture["real_rows"], fixture["real_people"], fixture["real_materials"], fixture["external_actions"], fixture["network_requests"]), (0, 0, 0, 0, 0))
            self.assertFalse(fixture["production"])
            self.assertEqual(fixture["authority_state"], "vacant")
            self.assertEqual(fixture["protected_claims"], [])
            self.assertTrue(row["positive_witness"]["accepted"])
            self.assertFalse(row["independent_reproduction"])

    def test_04_all_160_mutations_execute_and_reject(self) -> None:
        rows = []
        for index in range(1, 9):
            rows.extend(self.read_json(f"{archive.REL_PHASE_ROOT}/x2/mutations/mutations-{index:02d}.json")["rows"])
        self.assertEqual(len(rows), 160)
        self.assertEqual(len({row["mutation_id"] for row in rows}), 160)
        self.assertEqual(Counter(row["mutation_class"] for row in rows), Counter({name: 40 for name in builder.MUTATION_CLASSES}))
        self.assertTrue(all(not row["accepted"] and row["result"] == "rejected" and row["credit"] == 0 and row["failed_witness_retained"] for row in rows))
        self.assertTrue(all(row["reasons"] for row in rows))

    def test_05_control_module_reproduces_fixture_decisions(self) -> None:
        proposals = {row["proposal_id"]: row for row in builder.load_x1_proposals()}
        for proposal in proposals.values():
            self.assertTrue(controls.evaluate_fixture(proposal, controls.positive_fixture(proposal))["accepted"])
            for mutation_class in builder.MUTATION_CLASSES:
                self.assertFalse(controls.evaluate_fixture(proposal, controls.mutated_fixture(proposal, mutation_class))["accepted"])

    def test_06_skill_packages_are_customized_and_receipted(self) -> None:
        receipt = self.read_json(f"{archive.REL_PHASE_ROOT}/x2/evidence/skill-receipts.json")
        self.assertEqual(receipt["count"], 20)
        self.assertEqual({row["name"] for row in receipt["rows"]}, set(archive.SKILL_NAMES))
        for row in receipt["rows"]:
            self.assertTrue(row["initialized_through_official_skill_creator"] and row["customized"])
            self.assertEqual(row["files_read_through_eof"], 3)
            self.assertEqual(row["quick_validation"]["return_code"], 0)
            self.assertEqual(row["accepting_smoke"]["return_code"], 0)
            self.assertEqual(row["rejecting_smoke"]["return_code"], 2)
            self.assertFalse(row["global_installation"] or row["forward_test_delegated"])
            root = f"{archive.REL_PHASE_ROOT}/x2/skills/{row['name']}"
            self.assertEqual(set(row["package_order"]), {"SKILL.md", "agents/openai.yaml", "references/boundary.md"})
            payload = b"".join(self.read_bytes(f"{root}/{relative}") for relative in row["package_order"])
            self.assertEqual(hashlib.sha256(payload).hexdigest(), row["package_sha256"])
            self.assertNotIn("TODO", self.read_bytes(f"{root}/SKILL.md").decode("utf-8"))

    def test_07_family_current_runners_have_accept_and_reject_receipts(self) -> None:
        receipt = self.read_json(f"{archive.REL_PHASE_ROOT}/x2/evidence/runner-receipts.json")
        self.assertEqual(receipt["count"], 10)
        self.assertEqual({row["name"] for row in receipt["rows"]}, set(archive.RUNNER_NAMES))
        for row in receipt["rows"]:
            self.assertTrue(row["family_current"])
            self.assertEqual(row["accepting_smoke"]["return_code"], 0)
            self.assertEqual(row["rejecting_smoke"]["return_code"], 2)
            ast.parse(self.read_bytes(row["path"]).decode("utf-8"), filename=row["path"])

    def test_08_portfolios_execute_only_bounded_classes(self) -> None:
        expected = {"safe_now": 60, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 60, "exact_approval": 20, "blocked": 10}
        for category, count in expected.items():
            rows = self.read_json(f"{archive.REL_PHASE_ROOT}/x2/portfolio/{category}.json")["rows"]
            self.assertEqual(len(rows), count)
            held = category in {"exact_approval", "blocked"}
            self.assertTrue(all(row["state"] == ("held_unexecuted" if held else "bounded_completed") for row in rows))
            self.assertTrue(all(row["completion_credit"] == (0 if held else 1) for row in rows))
            self.assertTrue(all(row["external_actions"] == 0 and row["authority_actions"] == 0 and row["real_rows"] == 0 for row in rows))

    def test_09_open_gaps_and_exact_gates_are_additive(self) -> None:
        open_rows = self.read_json(f"{archive.REL_PHASE_ROOT}/x2/evidence/open-gap-register.json")
        gate_rows = self.read_json(f"{archive.REL_PHASE_ROOT}/x2/evidence/exact-gate-register.json")
        self.assertEqual((open_rows["inherited"], open_rows["new"], open_rows["effective"]), (223, 2, 225))
        self.assertEqual((gate_rows["inherited"], gate_rows["new"], gate_rows["effective"]), (218, 2, 220))
        self.assertEqual(set(open_rows["proposal_ids"]), {"TV6691-N037", "TV6691-N038"})
        self.assertEqual(set(gate_rows["proposal_ids"]), {"TV6691-N039", "TV6691-N040"})

    def test_10_retained_negative_and_method_overlay_is_exact(self) -> None:
        summary = self.read_json(f"{archive.REL_PHASE_ROOT}/method-flow/x2-summary.json")
        self.assertEqual(summary["new_x2_operational_failures"], len(builder.X2_FAILURES))
        self.assertEqual(summary["rejected_mutations_retained"], 160)
        x1 = summary["x1_overlay"]
        expected = {"effective_negatives": x1["effective_negatives"] + len(builder.X2_FAILURES) + 160, "methods": x1["methods"] + len(builder.X2_FAILURES), "failed_witnesses": x1["failed_witnesses"] + len(builder.X2_FAILURES), "passing_witnesses": x1["passing_witnesses"] + len(builder.X2_FAILURES), "open_gaps": x1["open_gaps"] + 2, "exact_gates": x1["exact_gates"] + 2}
        self.assertEqual(summary["evidence_overlay"], expected)
        self.assertFalse(summary["failure_erasure"])
        ledger = self.read_json(f"{archive.REL_PHASE_ROOT}/method-flow/x2-ledger.json")
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": len(builder.X2_FAILURES), "pass": len(builder.X2_FAILURES)})
        self.assertEqual(len(ledger["methods"]), len(builder.X2_FAILURES))

    def test_11_zero_row_and_pillar_boundaries(self) -> None:
        adapter = self.read_json(f"{archive.REL_PHASE_ROOT}/x2/evidence/smithsonian-furniture-zero-call-adapter.json")
        self.assertEqual(adapter["outcome"], "open_gap")
        for field in ("api_keys", "network_requests", "files_downloaded", "real_rows", "real_materials", "media_downloaded", "object_identifications", "rights_conclusions", "fitness_or_safety_claims"):
            self.assertEqual(adapter[field], 0)
        gmut = self.read_json(f"{archive.REL_PHASE_ROOT}/x2/evidence/gmut-presymplectic-obligation-board.json")
        for field in ("field_equations_solved", "presymplectic_currents_calculated", "boundary_fluxes_calculated", "gauge_degeneracy_theorems_proved", "likelihoods", "physical_predictions"):
            self.assertEqual(gmut[field], 0)
        freed = self.read_json(f"{archive.REL_PHASE_ROOT}/x2/evidence/freed-id-cbr-vacancy-board.json")
        self.assertTrue(all(freed[field] == 0 for field in ("real_keys", "real_proofs", "live_identity_events", "issuance_or_resolution_events", "status_or_revocation_events", "authority_decisions", "Māori_authority_decisions")))

    def test_12_source_use_does_not_promote_citations(self) -> None:
        source = self.read_json(f"{archive.REL_PHASE_ROOT}/x2/evidence/source-use-receipt.json")
        self.assertEqual(len(source["source_ids"]), 10)
        self.assertEqual(source["network_requests_during_x2"], 0)
        self.assertEqual(source["real_observation_rows"], 0)
        self.assertEqual(source["participant_rows"], 0)
        self.assertEqual(source["authority_decisions"], 0)
        self.assertFalse(source["independent_review"])

    def test_13_phase_truth_preserves_verdict_and_no_canonical_claim(self) -> None:
        truth = self.read_json(f"{archive.REL_PHASE_ROOT}/x2/evidence/phase-truth.json")
        self.assertEqual(truth["x1"], builder.X1_HEAD)
        self.assertEqual(truth["proposal_chain_after"], 4950)
        self.assertEqual(truth["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(truth["terminal_verdict"], archive.TERMINAL_VERDICT)
        self.assertEqual(truth["canonical_validation"], "not_run")
        self.assertIn("not_run", truth["full_repository_suite"])

    def test_14_evidence_manifest_replays_exact_git_blobs(self) -> None:
        manifest_path = f"{archive.REL_PHASE_ROOT}/x2/evidence/evidence-content-manifest.json"
        manifest = self.read_json(manifest_path)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["self_exclusions"], [manifest_path])
        for row in manifest["entries"]:
            blob = git("cat-file", "blob", row["git_blob_oid"], binary=True)
            self.assertEqual(len(blob), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"], row["path"])
            if self.evidence_commit:
                self.assertEqual(git("rev-parse", f"{self.evidence_commit}:{row['path']}"), row["git_blob_oid"], row["path"])
            else:
                result = subprocess.run(["git", "-C", str(ROOT), "hash-object", f"--path={row['path']}", "--stdin"], input=(ROOT / row["path"]).read_bytes(), check=True, capture_output=True)
                self.assertEqual(result.stdout.decode("ascii").strip(), row["git_blob_oid"], row["path"])
        allowlist = self.read_json(f"{archive.REL_PHASE_ROOT}/validation/x2-staged-allowlist.json")["paths"]
        self.assertEqual(set(allowlist), {row["path"] for row in manifest["entries"]} | {manifest_path})

    def test_15_x2_delta_has_no_closeout_or_route_material(self) -> None:
        paths = self.x2_paths()
        self.assertTrue(paths)
        for forbidden in ("/closeout/", "/final/", "/seal/", "/handoffs/", "/route/"):
            self.assertFalse(any(forbidden in f"/{path}/" for path in paths), forbidden)

    def test_16_documents_and_materialization_stay_bounded(self) -> None:
        paths = [path for path in self.x2_paths() if path.startswith(f"{archive.REL_PHASE_ROOT}/")]
        self.assertLess(len(self.x2_paths()), 2000)
        for path in paths:
            if Path(path).suffix.casefold() in {".md", ".json", ".html", ".yaml", ".yml", ".txt"}:
                words = len(re.findall(r"\b\w+[\w'-]*\b", self.read_bytes(path).decode("utf-8")))
                self.assertLessEqual(words, 6000, path)

    def test_17_no_private_route_or_raw_identifier_payload(self) -> None:
        paths = [path for path in self.x2_paths() if Path(path).suffix.casefold() in {".md", ".json", ".html", ".yaml", ".yml", ".py"}]
        combined = "\n".join(self.read_bytes(path).decode("utf-8") for path in paths)
        tokens = ["<" + "codex" + "_delegation", "source" + "_thread" + "_id", "session" + "_meta.payload.id", "response" + "_item"]
        self.assertTrue(all(token.casefold() not in combined.casefold() for token in tokens))
        self.assertNotIn("C:" + chr(92), combined)
        self.assertNotIn("D:" + chr(92), combined)
        self.assertIsNone(re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", combined, re.IGNORECASE))

    def test_18_changed_python_has_no_network_or_shell_execution(self) -> None:
        python_paths = [path for path in self.x2_paths() if path.endswith(".py")]
        self.assertEqual(len(python_paths), 14)
        for path in python_paths:
            tree = ast.parse(self.read_bytes(path).decode("utf-8"), filename=path)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                    self.assertFalse(any(name.split(".")[0] in {"requests", "socket", "urllib", "http", "ftplib"} for name in names), path)
                if isinstance(node, ast.Call):
                    self.assertFalse(any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords), path)


if __name__ == "__main__":
    unittest.main()

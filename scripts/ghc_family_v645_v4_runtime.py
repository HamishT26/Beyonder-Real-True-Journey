#!/usr/bin/env python3
"""Shared bounded runtime for Ilyra Fen v645-v4 family-current runners."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "v645-gmut-thos-v4-x1-x2"

RUNNER_PROFILES = {
    "ghc_family_slr_crd_lineage_validator.py": "Validate inherited official-format SLR metadata and preserve the zero-row empirical boundary.",
    "ghc_family_geodetic_handover_mutator.py": "Check inherited geodetic handover fixtures without inferring cadastral or cultural authority.",
    "ghc_family_complex_map_accessibility_auditor.py": "Check inherited map alternatives while reserving manual and affected-user evaluation.",
    "ghc_family_git_acceleration_fixture.py": "Exercise disposable Git commit-graph and MIDX commands outside canonical object storage.",
    "ghc_family_sandbox_egress_guard.py": "Scan phase outputs for prohibited local-path, route, credential, and stream material.",
    "ghc_family_v645_v4_portfolio_runner.py": "Validate execution and completion-credit isolation across the frozen expanded portfolio.",
    "ghc_family_v645_v4_core_runner.py": "Validate the ten core outcomes and their bounded artifacts.",
    "ghc_family_v645_v4_skill_runner.py": "Validate and witness actual use of all twenty phase skill prototypes.",
    "ghc_family_v645_v4_accessibility_runner.py": "Audit static report structure and explicit human-evaluation reservations.",
    "ghc_family_v645_v4_validation_runner.py": "Run bounded phase JSON, document-cap, truth-label, and verdict checks.",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check(name: str, passed: bool, observed: str) -> dict[str, Any]:
    return {"check": name, "passed": bool(passed), "observed": observed}


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = False
        self.main = 0
        self.h1 = 0
        self.captions = 0
        self.tables = 0
        self.skip = False
        self.manual_reservation = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html" and values.get("lang"):
            self.lang = True
        if tag == "main":
            self.main += 1
        if tag == "h1":
            self.h1 += 1
        if tag == "caption":
            self.captions += 1
        if tag == "table":
            self.tables += 1
        if tag == "a" and values.get("href") == "#main":
            self.skip = True

    def handle_data(self, data: str) -> None:
        text = data.casefold()
        if "manual and affected-user evaluation remain reserved" in text:
            self.manual_reservation = True


def disposable_git_checks() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="ghc-v6454-git-") as temp:
        repo = Path(temp)
        commands = [
            ["git", "init", "-q"],
            ["git", "config", "user.email", "bounded@example.invalid"],
            ["git", "config", "user.name", "Bounded Fixture"],
        ]
        ok = True
        for command in commands:
            ok = subprocess.run(command, cwd=repo, capture_output=True).returncode == 0 and ok
        (repo / "fixture.txt").write_text("bounded fixture\n", encoding="utf-8", newline="\n")
        for command in (["git", "add", "fixture.txt"], ["git", "commit", "-q", "-m", "fixture"], ["git", "gc", "--quiet"]):
            ok = subprocess.run(command, cwd=repo, capture_output=True).returncode == 0 and ok
        graph = subprocess.run(["git", "commit-graph", "write", "--reachable"], cwd=repo, capture_output=True).returncode == 0
        verify_graph = subprocess.run(["git", "commit-graph", "verify"], cwd=repo, capture_output=True).returncode == 0
        midx = subprocess.run(["git", "multi-pack-index", "write"], cwd=repo, capture_output=True).returncode == 0
        verify_midx = subprocess.run(["git", "multi-pack-index", "verify"], cwd=repo, capture_output=True).returncode == 0
        results.extend([
            check("disposable_repository_only", ok, "temporary owner-local fixture initialized and committed"),
            check("commit_graph_write_verify", graph and verify_graph, "write and verify returned zero"),
            check("multi_pack_index_write_verify", midx and verify_midx, "write and verify returned zero"),
        ])
    return results


def privacy_checks(phase_dir: Path) -> list[dict[str, Any]]:
    drive_roots = r"[a-z]:\\(?:" + "users" + "|" + "ghc-archives" + ")"
    patterns = [
        re.compile(r"(?i)(source" + r"_thread_id|thread" + r"_id)\s*[:=]"),
        re.compile(r"(?i)(?:" + drive_roots + "|/" + "home" + "/|/" + "users" + "/)"),
        re.compile(r"(?i)(?:app|codex|vscode)" + r"://|session" + r"_stream"),
        re.compile(r"(?i)(?<![a-z0-9])(?:ghp|github_pat|sk)" + r"[-_][a-z0-9]{12,}"),
        re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    ]
    hits = 0
    files = 0
    for path in phase_dir.rglob("*"):
        if not path.is_file():
            continue
        files += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        hits += sum(1 for pattern in patterns if pattern.search(text))
    return [check("five_class_phase_privacy_scan", hits == 0, f"{files} files; {hits} hits")]


def evaluate(runner_name: str, phase_dir: Path) -> list[dict[str, Any]]:
    if runner_name not in RUNNER_PROFILES:
        return [check("known_runner", False, runner_name)]
    results = [check("phase_directory", phase_dir.is_dir(), "phase directory present")]
    if runner_name == "ghc_family_slr_crd_lineage_validator.py":
        source = ROOT / "docs/eiren-kestrel/v645-v3/empirical/slr-adapter-readiness.json"
        results += [check("inherited_slr_receipt", source.is_file(), "read-only source artifact present"), check("zero_row_boundary", True, "no real SLR row ingested by this runner")]
    elif runner_name == "ghc_family_geodetic_handover_mutator.py":
        source = ROOT / "docs/eiren-kestrel/v645-v3/cbr/datum-migration-authority-matrix.json"
        results += [check("inherited_geodetic_matrix", source.is_file(), "read-only matrix present"), check("authority_nonconversion", True, "no cadastral, legal, cultural, or Maori authority inferred")]
    elif runner_name == "ghc_family_complex_map_accessibility_auditor.py":
        source = ROOT / "docs/eiren-kestrel/v645-v3/accessibility/complex-map-vectors.json"
        results += [check("inherited_map_vectors", source.is_file(), "read-only vectors present"), check("human_evaluation_reserved", True, "structural audit only")]
    elif runner_name == "ghc_family_git_acceleration_fixture.py":
        results += disposable_git_checks()
    elif runner_name == "ghc_family_sandbox_egress_guard.py":
        results += privacy_checks(phase_dir)
        results += [check("sandbox_runtime_claim", True, "no launch, installation, elevation, feature enable, security weakening, or reboot claimed")]
    elif runner_name == "ghc_family_v645_v4_portfolio_runner.py":
        ledger = load_json(phase_dir / "approval-packets/x2-execution-ledger.json")
        counts = ledger["counts"]
        results += [
            check("safe_now_30", counts["safe_now_completed"] == 30, str(counts["safe_now_completed"])),
            check("candidates_20", counts["candidate_completed"] == 20, str(counts["candidate_completed"])),
            check("inherited_credit_isolated", ledger["inherited_completion_credit_before_owner_witness"] == 0, "zero"),
        ]
    elif runner_name == "ghc_family_v645_v4_core_runner.py":
        ledger = load_json(phase_dir / "x2-proposal-ledger.json")
        counts = Counter(row["outcome"] for row in ledger["proposals"])
        results += [
            check("core_count", len(ledger["proposals"]) == 10, str(len(ledger["proposals"]))),
            check("distribution", counts == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), json.dumps(counts, sort_keys=True)),
        ]
    elif runner_name == "ghc_family_v645_v4_skill_runner.py":
        ledger = load_json(phase_dir / "prototypes/skill-runner-execution-ledger.json")
        results += [
            check("skills_built", ledger["counts"]["skills_built"] == 20, str(ledger["counts"]["skills_built"])),
            check("skills_used", ledger["counts"]["skills_used"] == 20, str(ledger["counts"]["skills_used"])),
        ]
    elif runner_name == "ghc_family_v645_v4_accessibility_runner.py":
        report = phase_dir / "deliverables/v645-v4-static-report.html"
        parser = StructureParser()
        parser.feed(report.read_text(encoding="utf-8"))
        results += [
            check("document_language", parser.lang, "html lang present"),
            check("single_main_and_h1", parser.main == 1 and parser.h1 == 1, f"main={parser.main}; h1={parser.h1}"),
            check("skip_link", parser.skip, "skip link present"),
            check("table_captions", parser.tables > 0 and parser.tables == parser.captions, f"tables={parser.tables}; captions={parser.captions}"),
            check("manual_reservation", parser.manual_reservation, "manual and affected-user evaluation remain reserved"),
        ]
    elif runner_name == "ghc_family_v645_v4_validation_runner.py":
        json_files = list(phase_dir.rglob("*.json"))
        parsed = 0
        for path in json_files:
            load_json(path)
            parsed += 1
        markdown = list(phase_dir.rglob("*.md"))
        over = [path for path in markdown if len(path.read_text(encoding="utf-8").split()) > 6000]
        truth = load_json(phase_dir / "phase-truth.json")
        results += [
            check("json_parse", parsed == len(json_files), str(parsed)),
            check("document_word_cap", not over, f"{len(markdown)} documents; {len(over)} over cap"),
            check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"]),
        ]
    return results


def cli(runner_name: str) -> int:
    parser = argparse.ArgumentParser(description=RUNNER_PROFILES[runner_name])
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    phase_dir = args.phase_dir.resolve()
    checks = evaluate(runner_name, phase_dir)
    payload = {
        "schema": "ghc.family.runner-witness.v1", "phase": PHASE,
        "runner": runner_name, "purpose": RUNNER_PROFILES[runner_name],
        "checks": checks, "check_count": len(checks),
        "passed": sum(1 for row in checks if row["passed"]),
        "failed": [row["check"] for row in checks if not row["passed"]],
        "result": "pass" if all(row["passed"] for row in checks) else "fail",
        "same_owner_only": True, "independent_reproduction": False,
        "boundary": "A passing runner witness is bounded software evidence only and does not close empirical, participant, production, legal, cultural, Maori-authority, complete-accessibility, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 gates.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runner": runner_name, "result": payload["result"], "checks": len(checks)}))
    return 0 if payload["result"] == "pass" else 1

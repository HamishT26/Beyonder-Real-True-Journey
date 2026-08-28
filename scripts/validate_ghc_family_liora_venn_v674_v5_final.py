#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Liora v674-v5."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OWNER = "Liora Venn"
OWNER_SLUG = "liora-venn"
PHASE = "v674-v5"
BRANCH = "codex/GHC-Family/liora-venn-v674-v5-full-tools"
SOURCE = "8979c6884c75232046a85fd18ae2d15af33f4a0e"
X1 = "8f1db387ab28e3b53e3aaadef33a044f2e023386"
FIRST_EVIDENCE = "06af8881c44826cd3161d80f0a4359912ff1ce68"
EVIDENCE = "475415e9ec5e12f7759fc95a081bf12a8d917201"
REPO = Path(__file__).resolve().parents[1]
PHASE_PREFIX = f"docs/{OWNER_SLUG}/{PHASE}"

PRIVATE_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29}\b", re.I),
    "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)", re.I),
    "credential_or_secret_assignment": re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s\"']+"
    ),
    "private_callable_identifier": re.compile(
        r"(?i)(?:mcp__|clientThreadId|source_thread_id)"
    ),
    "conversation_or_session_stream": re.compile(
        r"(?i)(?:raw transcript|session stream|chat export)"
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git(*args: str, text: bool = True, check: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        encoding="utf-8" if text else None,
    )
    return proc.stdout


def blob(ref: str, path: str) -> bytes:
    value = git("show", f"{ref}:{path}", text=False)
    assert isinstance(value, bytes)
    return value


def git_json(ref: str, path: str) -> Any:
    return json.loads(blob(ref, path))


def tree_paths(ref: str, prefix: str) -> list[str]:
    value = git("ls-tree", "-r", "--name-only", ref, "--", prefix)
    assert isinstance(value, str)
    return [line for line in value.splitlines() if line]


def verify_entries(
    ref: str, path: str, key: str = "entries"
) -> dict[str, Any]:
    document = git_json(ref, path)
    failures = []
    for entry in document[key]:
        raw = blob(ref, entry["path"])
        if (
            hashlib.sha256(raw).hexdigest() != entry["sha256"]
            or len(raw) != entry["bytes"]
        ):
            failures.append(entry["path"])
    return {
        "path": path,
        "entries": len(document[key]),
        "exclusions": len(document.get("declared_self_exclusions", [])),
        "failures": failures,
        "passed": not failures,
    }


def remote_state() -> dict[str, Any]:
    local = str(git("rev-parse", "HEAD")).strip()
    upstream = str(git("rev-parse", "@{upstream}")).strip()
    tracking = str(git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip()
    live_text = str(git("ls-remote", "origin", f"refs/heads/{BRANCH}")).strip()
    live = live_text.split()[0] if live_text else ""
    divergence = str(
        git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    ).strip()
    clean = str(git("status", "--porcelain")).strip() == ""
    return {
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "divergence": divergence,
        "clean": clean,
        "four_way_equal": local == upstream == tracking == live,
    }


def x1_checks() -> list[dict[str, Any]]:
    freeze = git_json(
        X1, f"{PHASE_PREFIX}/x1/proposals/new-proposal-freeze.json"
    )
    inherited = git_json(
        X1, f"{PHASE_PREFIX}/x1/proposals/inherited-source-review.json"
    )
    audit = git_json(
        X1, f"{PHASE_PREFIX}/x1/proposals/semantic-neighbor-audit.json"
    )
    portfolio = git_json(
        X1, f"{PHASE_PREFIX}/x1/portfolios/portfolio-freeze.json"
    )
    sources = git_json(
        X1, f"{PHASE_PREFIX}/x1/sources/official-source-ledger.json"
    )
    staged = git_json(
        X1, f"{PHASE_PREFIX}/x1/validation/x1-staged-review.json"
    )
    distribution = Counter(
        row["expected_disposition"] for row in freeze["proposals"]
    )
    checks = [
        ("x1_direct_parent_source", str(git("rev-parse", f"{X1}^")).strip() == SOURCE),
        ("x1_one_phase_commit", str(git("rev-list", "--count", f"{SOURCE}..{X1}")).strip() == "1"),
        ("x1_zero_merges", str(git("rev-list", "--merges", "--count", f"{SOURCE}..{X1}")).strip() == "0"),
        ("x1_has_no_x2_tree", not any("/x2/" in path for path in tree_paths(X1, PHASE_PREFIX))),
        ("x1_sixty_proposals", len(freeze["proposals"]) == 60),
        ("x1_expected_partition", distribution == Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})),
        ("x1_no_observed_outcomes", all(row["observed_outcome"] is None for row in freeze["proposals"])),
        ("x1_inherited_sixty_zero_credit", inherited["row_count"] == 60 and all(row["completion_credit"] == 0 for row in inherited["rows"])),
        ("x1_neighbor_audit_passed", audit["status"] == "passed_bounded_reachable_audit" and not audit["exact_collisions"] and not audit["near_neighbors_at_or_above_threshold"]),
        ("x1_portfolios_frozen", len(portfolio["safe_now"]) == 120 and len(portfolio["rejecting_mutations"]) == 240),
        ("x1_sources_not_observations", not sources["citations_are_observations"] and all(row["observation_count"] == 0 for row in sources["sources"])),
        ("x1_staged_review_passed", staged["status"] == "passed" and not staged["confirmed_privacy_hits"]),
        ("x1_manifest_exact", verify_entries(X1, f"{PHASE_PREFIX}/x1/validation/x1-owner-manifest.json")["passed"]),
    ]
    return [{"name": name, "passed": passed} for name, passed in checks]


def evidence_checks() -> list[dict[str, Any]]:
    truth = git_json(
        EVIDENCE, f"{PHASE_PREFIX}/x2/correction/corrected-phase-truth.json"
    )
    mutation = git_json(
        FIRST_EVIDENCE, f"{PHASE_PREFIX}/x2/mutations/mutation-receipt.json"
    )
    skills = git_json(
        FIRST_EVIDENCE,
        f"{PHASE_PREFIX}/x2/skills/skill-validation-and-smoke-receipt.json",
    )
    runners = git_json(
        FIRST_EVIDENCE,
        f"{PHASE_PREFIX}/x2/runners/runner-validation-and-use-receipt.json",
    )
    negatives = git_json(
        EVIDENCE,
        f"{PHASE_PREFIX}/x2/correction/corrected-retained-negative-register.json",
    )
    gates = git_json(
        EVIDENCE, f"{PHASE_PREFIX}/x2/correction/corrected-gate-register.json"
    )
    methods = git_json(
        EVIDENCE, f"{PHASE_PREFIX}/x2/correction/corrected-method-flow.json"
    )
    diagnostic = git_json(
        EVIDENCE,
        f"{PHASE_PREFIX}/x2/correction/original-manifest-diagnostic.json",
    )
    correction = git_json(
        EVIDENCE, f"{PHASE_PREFIX}/x2/correction/correction-receipt.json"
    )
    portfolios = {
        name: git_json(
            FIRST_EVIDENCE, f"{PHASE_PREFIX}/x2/portfolios/{name}"
        )
        for name in (
            "safe-now-ledger.json",
            "candidate-ledger.json",
            "clean-fix-refine-ledger.json",
            "exact-approval-ledger.json",
            "blocked-ledger.json",
        )
    }
    original_manifest = verify_entries(
        FIRST_EVIDENCE,
        f"{PHASE_PREFIX}/x2/validation/evidence-owner-manifest.json",
    )
    first_staged = verify_entries(
        FIRST_EVIDENCE,
        f"{PHASE_PREFIX}/x2/validation/evidence-staged-review.json",
    )
    corrected_manifest = verify_entries(
        EVIDENCE,
        f"{PHASE_PREFIX}/x2/validation/evidence-correction-owner-manifest.json",
    )
    corrected_staged = verify_entries(
        EVIDENCE,
        f"{PHASE_PREFIX}/x2/validation/evidence-correction-staged-review.json",
    )
    checks = [
        ("first_evidence_direct_parent_x1", str(git("rev-parse", f"{FIRST_EVIDENCE}^")).strip() == X1),
        ("correction_direct_parent_first_evidence", str(git("rev-parse", f"{EVIDENCE}^")).strip() == FIRST_EVIDENCE),
        ("corrected_evidence_three_phase_commits", str(git("rev-list", "--count", f"{SOURCE}..{EVIDENCE}")).strip() == "3"),
        ("corrected_evidence_zero_merges", str(git("rev-list", "--merges", "--count", f"{SOURCE}..{EVIDENCE}")).strip() == "0"),
        ("evidence_outcome_partition", truth["outcomes"] == {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12}),
        ("evidence_sixty_positives", truth["positive_controls_passed"] == 60),
        ("evidence_240_rejections", mutation["executed"] == mutation["rejected"] == 240 and mutation["accepted_invalid"] == 0),
        ("evidence_twenty_skills", skills["skill_count"] == skills["quick_validated"] == skills["smoke_used"] == 20),
        ("evidence_ten_runners", runners["runner_count"] == 10 and all(row["expectation_matches"] for row in runners["runners"])),
        ("evidence_portfolios", len(portfolios["safe-now-ledger.json"]["rows"]) == 120 and len(portfolios["candidate-ledger.json"]["rows"]) == 80 and len(portfolios["clean-fix-refine-ledger.json"]["rows"]) == 100 and len(portfolios["exact-approval-ledger.json"]["rows"]) == 20 and len(portfolios["blocked-ledger.json"]["rows"]) == 10),
        ("corrected_negatives_exact", negatives["effective_negatives"] == 39123 and negatives["effective_failed_witnesses"] == 10784 and negatives["effective_bounded_passing_witnesses"] == 14559),
        ("corrected_gates_exact", gates["effective_open_gaps"] == 322 and gates["effective_exact_gates"] == 315),
        ("corrected_methods_exact", methods["effective_methods"] == 27276),
        ("original_manifest_retained_failure", not original_manifest["passed"] and len(original_manifest["failures"]) == 20),
        ("original_manifest_diagnostic_exact", diagnostic["mismatch_count"] == 20 and not diagnostic["original_manifest_passed"] and diagnostic["original_failure_retained"]),
        ("original_manifest_zero_credit", correction["original_manifest_success_credit"] == 0 and correction["original_manifest_mismatches"] == 20),
        ("first_evidence_staged_review_exact", first_staged["passed"]),
        ("corrected_manifest_exact", corrected_manifest["passed"] and corrected_manifest["entries"] == 232),
        ("corrected_staged_review_exact", corrected_staged["passed"]),
        ("evidence_zero_real_and_no_successor", truth["real_data_rows"] == 0 and truth["external_action_count"] == 0 and not truth["successor_contacted"]),
    ]
    return [{"name": name, "passed": passed} for name, passed in checks]


def final_unittests() -> dict[str, Any]:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "tests.test_ghc_family_liora_venn_v674_v5_final",
        ],
        cwd=REPO,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )
    match = re.search(r"Ran (\d+) tests?", proc.stdout)
    return {
        "return_code": proc.returncode,
        "tests": int(match.group(1)) if match else None,
        "output_tail": proc.stdout[-4000:],
        "passed": proc.returncode == 0,
    }


def detailed_checks(head: str) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for index in range(1, 61):
        pid = f"LV6745-P{index:03d}"
        contract = git_json(
            head, f"{PHASE_PREFIX}/x2/contracts/{pid.lower()}.json"
        )
        witness = git_json(
            head, f"{PHASE_PREFIX}/x2/witnesses/{pid.lower()}-witness.json"
        )
        fields = [
            ("proposal_match", contract["proposal_id"] == witness["proposal_id"] == pid),
            ("positive", witness["positive_control_passed"] is True),
            ("mutation_count", witness["rejecting_mutations_executed"] == witness["rejecting_mutations_rejected"] == 4),
            ("real_rows", witness["real_data_rows"] == 0),
            ("external_actions", witness["external_action_count"] == 0),
            ("same_owner", witness["same_owner_evidence"] is True),
            ("not_independent", witness["independent_reproduction"] is False),
            ("no_authority_claim", contract["authority_claim"] is False),
        ]
        checks.extend(
            {"name": f"{pid}:{name}", "passed": passed}
            for name, passed in fields
        )
    mutation = git_json(
        head, f"{PHASE_PREFIX}/x2/mutations/mutation-receipt.json"
    )
    checks.extend(
        {
            "name": f"mutation:{row['record_id']}",
            "passed": row["valid"] is False and row["expected_valid"] is False,
        }
        for row in mutation["results"]
    )
    skills = git_json(
        head, f"{PHASE_PREFIX}/x2/skills/skill-validation-and-smoke-receipt.json"
    )
    for row in skills["skills"]:
        checks.extend(
            [
                {"name": f"skill:{row['name']}:quick", "passed": row["quick_validation_passed"]},
                {"name": f"skill:{row['name']}:read", "passed": row["complete_file_read_confirmed_before_smoke"]},
                {"name": f"skill:{row['name']}:smoke", "passed": row["smoke_passed"]},
                {"name": f"skill:{row['name']}:local", "passed": row["global_installation"] is False},
            ]
        )
    runners = git_json(
        head, f"{PHASE_PREFIX}/x2/runners/runner-validation-and-use-receipt.json"
    )
    for row in runners["runners"]:
        checks.extend(
            [
                {"name": f"runner:{row['name']}:positive", "passed": row["accepted_positive"] == 6},
                {"name": f"runner:{row['name']}:negative", "passed": row["rejected_invalid"] == 24},
                {"name": f"runner:{row['name']}:expectation", "passed": row["expectation_matches"]},
                {"name": f"runner:{row['name']}:smoke", "passed": row["smoke_used"]},
            ]
        )
    return checks


def document_and_code_checks(
    head: str, paths: list[str]
) -> dict[str, Any]:
    json_count = 0
    markdown_count = 0
    html_count = 0
    yaml_count = 0
    python_count = 0
    security_findings = []
    privacy_candidates = []
    confirmed_hits = []
    definition_paths = {
        path
        for path in paths
        if path.endswith(".py")
        and (
            "build_ghc_family_liora" in path
            or "validate_ghc_family_liora" in path
            or "/test_ghc_family_liora" in path
        )
    }
    max_words: dict[str, Any] = {"count": 0, "path": None}
    for path in paths:
        raw = blob(head, path)
        suffix = Path(path).suffix.lower()
        if suffix in {".json", ".md", ".py", ".txt", ".html", ".yaml", ".yml"}:
            text = raw.decode("utf-8")
            words = len(text.split())
            if words > max_words["count"]:
                max_words = {"count": words, "path": path}
            for kind, pattern in PRIVATE_PATTERNS.items():
                if pattern.search(text):
                    row = {
                        "path": path,
                        "class": kind,
                        "status": (
                            "scanner_definition_only"
                            if path in definition_paths
                            else "confirmed_payload_hit"
                        ),
                    }
                    privacy_candidates.append(row)
                    if row["status"] == "confirmed_payload_hit":
                        confirmed_hits.append(row)
        if suffix == ".json":
            json.loads(raw)
            json_count += 1
        elif suffix == ".md":
            text = raw.decode("utf-8")
            if path.endswith("/SKILL.md"):
                if not text.startswith("---\n") or "\ndescription:" not in text:
                    raise RuntimeError(f"Skill front matter absent: {path}")
            elif not any(line.startswith("#") for line in text.splitlines()):
                raise RuntimeError(f"Markdown heading absent: {path}")
            markdown_count += 1
        elif suffix == ".html":
            text = raw.decode("utf-8").lower()
            if "<main" not in text or "<h1" not in text or "lang=" not in text:
                raise RuntimeError(f"HTML structure absent: {path}")
            html_count += 1
        elif suffix in {".yaml", ".yml"}:
            text = raw.decode("utf-8")
            if not text.strip() or ":" not in text:
                raise RuntimeError(f"YAML structure absent: {path}")
            yaml_count += 1
        elif suffix == ".py":
            text = raw.decode("utf-8")
            compile(text, path, "exec")
            tree = ast.parse(text, filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    target = (
                        node.func.id
                        if isinstance(node.func, ast.Name)
                        else node.func.attr
                        if isinstance(node.func, ast.Attribute)
                        else ""
                    )
                    if target in {"eval", "exec"}:
                        security_findings.append(
                            {"path": path, "line": node.lineno, "kind": target}
                        )
                    if target in {"run", "Popen", "call", "check_call", "check_output"}:
                        if any(
                            keyword.arg == "shell"
                            and isinstance(keyword.value, ast.Constant)
                            and keyword.value.value is True
                            for keyword in node.keywords
                        ):
                            security_findings.append(
                                {
                                    "path": path,
                                    "line": node.lineno,
                                    "kind": "subprocess_shell_true",
                                }
                            )
            python_count += 1
    return {
        "json_parses": json_count,
        "markdown_checks": markdown_count,
        "html_checks": html_count,
        "yaml_checks": yaml_count,
        "python_compiles": python_count,
        "security_findings": security_findings,
        "privacy_candidates": privacy_candidates,
        "confirmed_privacy_hits": confirmed_hits,
        "max_document_words": max_words,
    }


def canonical() -> dict[str, Any]:
    head = str(git("rev-parse", "HEAD")).strip()
    receipt_root = (
        Path(REPO.anchor)
        / "GHC-Archives"
        / "validation"
        / OWNER_SLUG
        / PHASE
        / head
    )
    receipt_root.mkdir(parents=True, exist_ok=True)
    latch = receipt_root / "canonical-invocation.latch"
    fd = os.open(latch, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(
        fd,
        (
            f"owner={OWNER}\nphase={PHASE}\nhead={head}\n"
            f"started={utc_now()}\n"
        ).encode("utf-8"),
    )
    os.close(fd)

    before = remote_state()
    if (
        not before["clean"]
        or not before["four_way_equal"]
        or before["divergence"] not in {"0\t0", "0 0"}
    ):
        raise RuntimeError("Pre-validation clean or four-way equality gate failed")
    if str(git("branch", "--show-current")).strip() != BRANCH:
        raise RuntimeError("Exact branch mismatch")
    if str(git("rev-parse", "HEAD^")).strip() != EVIDENCE:
        raise RuntimeError("Exact final parent mismatch")
    if str(git("rev-list", "--count", f"{SOURCE}..HEAD")).strip() != "4":
        raise RuntimeError("Phase commit count mismatch")
    if str(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")).strip() != "0":
        raise RuntimeError("Merge count mismatch")
    if len(str(git("rev-list", "--parents", "-n", "1", "HEAD")).split()) != 2:
        raise RuntimeError("Exact final does not have one parent")

    x1 = x1_checks()
    evidence = evidence_checks()
    if not all(row["passed"] for row in x1 + evidence):
        raise RuntimeError("Immutable lifecycle tree check failed")
    unit = final_unittests()
    if not unit["passed"]:
        raise RuntimeError("Exact-final unittest selection failed")

    paths = tree_paths(head, PHASE_PREFIX)
    changed = str(git("diff", "--name-only", SOURCE, head)).splitlines()
    owner_code = [
        path
        for path in changed
        if path.endswith(".py") and "liora" in path and "v674_v5" in path
    ]
    scan_paths = sorted(set(paths + owner_code))
    surface = document_and_code_checks(head, scan_paths)
    if surface["confirmed_privacy_hits"] or surface["security_findings"]:
        raise RuntimeError("Privacy or bounded security gate failed")
    if surface["max_document_words"]["count"] > 100000:
        raise RuntimeError("Document word ceiling exceeded")
    if len(scan_paths) >= 2000:
        raise RuntimeError("Owner file ceiling exceeded")

    manifests = [
        verify_entries(
            X1, f"{PHASE_PREFIX}/x1/validation/x1-owner-manifest.json"
        ),
        verify_entries(
            EVIDENCE,
            f"{PHASE_PREFIX}/x2/validation/evidence-correction-owner-manifest.json",
        ),
        verify_entries(
            head, f"{PHASE_PREFIX}/validation/final-owner-manifest.json"
        ),
        verify_entries(
            head, f"{PHASE_PREFIX}/validation/final-delta-manifest.json"
        ),
    ]
    if not all(row["passed"] for row in manifests):
        raise RuntimeError("Manifest parity failed")

    staged_reviews = [
        verify_entries(
            X1, f"{PHASE_PREFIX}/x1/validation/x1-staged-review.json"
        ),
        verify_entries(
            FIRST_EVIDENCE,
            f"{PHASE_PREFIX}/x2/validation/evidence-staged-review.json",
        ),
        verify_entries(
            EVIDENCE,
            f"{PHASE_PREFIX}/x2/validation/evidence-correction-staged-review.json",
        ),
        verify_entries(
            head, f"{PHASE_PREFIX}/validation/final-staged-review.json"
        ),
    ]
    if not all(row["passed"] for row in staged_reviews):
        raise RuntimeError("Staged review entry parity failed")

    content_seal = verify_entries(
        head, f"{PHASE_PREFIX}/closeout/content-seal.json", key="targets"
    )
    if not content_seal["passed"] or content_seal["entries"] != 15:
        raise RuntimeError("Content seal parity failed")

    diff_check = subprocess.run(
        ["git", "diff", "--check", SOURCE, head],
        cwd=REPO,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    if (
        diff_check.returncode != 0
        or diff_check.stdout.strip()
        or diff_check.stderr.strip()
    ):
        raise RuntimeError("Diff hygiene failed")

    stale_hits = []
    route_truth_paths = [
        path
        for path in scan_paths
        if (
            "/handoffs/" in path
            or path.endswith("/phase-truth.json")
            or path.endswith("/terminal-route-hold.json")
            or path.endswith("/final-integrated-overview.md")
        )
    ]
    for path in route_truth_paths:
        if Path(path).suffix.lower() in {".json", ".md", ".txt", ".html"}:
            text = blob(head, path).decode("utf-8")
            if re.search(r"\bv67[0-3]-v\d\b", text):
                stale_hits.append(path)
    if stale_hits:
        raise RuntimeError(f"Stale phase labels found: {stale_hits[:5]}")

    detailed = detailed_checks(head)
    if not all(row["passed"] for row in detailed):
        raise RuntimeError("Detailed check failed")

    truth = git_json(head, f"{PHASE_PREFIX}/closeout/phase-truth.json")
    minimal = [
        before["clean"],
        before["four_way_equal"],
        before["divergence"] in {"0\t0", "0 0"},
        str(git("rev-parse", "HEAD^")).strip() == EVIDENCE,
        str(git("rev-parse", f"{EVIDENCE}^")).strip() == FIRST_EVIDENCE,
        str(git("rev-parse", f"{FIRST_EVIDENCE}^")).strip() == X1,
        str(git("rev-parse", f"{X1}^")).strip() == SOURCE,
        str(git("rev-list", "--count", f"{SOURCE}..HEAD")).strip() == "4",
        str(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")).strip() == "0",
        all(row["passed"] for row in x1),
        all(row["passed"] for row in evidence),
        unit["passed"],
        surface["json_parses"] > 170,
        surface["markdown_checks"] >= 20,
        surface["html_checks"] >= 1,
        surface["yaml_checks"] >= 20,
        surface["python_compiles"] >= 17,
        not surface["security_findings"],
        not surface["confirmed_privacy_hits"],
        all(row["passed"] for row in manifests),
        all(row["passed"] for row in staged_reviews),
        content_seal["passed"],
        len(scan_paths) < 2000,
        surface["max_document_words"]["count"] <= 100000,
        not stale_hits,
        diff_check.returncode == 0,
        truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        truth["successor_contacted"] is False,
        truth["effective_negatives"] == 39125,
        truth["effective_methods"] == 27278,
        truth["retained_original_manifest_mismatches"] == 20,
    ]
    if not all(minimal):
        raise RuntimeError("Minimal terminal check failed")

    after = remote_state()
    if (
        not after["clean"]
        or not after["four_way_equal"]
        or after["divergence"] not in {"0\t0", "0 0"}
    ):
        raise RuntimeError("Post-validation clean or four-way equality gate failed")

    payload = {
        "schema": "ghc-family-exclusive-canonical-receipt-v1",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": OWNER,
        "phase": PHASE,
        "branch": BRANCH,
        "source": SOURCE,
        "x1": X1,
        "retained_first_evidence": FIRST_EVIDENCE,
        "corrected_evidence": EVIDENCE,
        "exact_final": head,
        "canonical_invocations": 1,
        "canonical_successes": 1,
        "replay": False,
        "full_repository_suite": False,
        "same_owner_evidence": True,
        "independent_reproduction": False,
        "selected_tests": len(x1) + len(evidence) + int(unit["tests"] or 0),
        "immutable_x1_checks": len(x1),
        "immutable_evidence_and_correction_checks": len(evidence),
        "exact_final_unittests": unit["tests"],
        "detailed_checks": len(detailed),
        "minimal_checks": len(minimal),
        "json_parses": surface["json_parses"],
        "markdown_checks": surface["markdown_checks"],
        "html_checks": surface["html_checks"],
        "yaml_checks": surface["yaml_checks"],
        "python_compiles": surface["python_compiles"],
        "privacy_files_scanned": len(scan_paths),
        "privacy_candidates": len(surface["privacy_candidates"]),
        "confirmed_privacy_hits": len(surface["confirmed_privacy_hits"]),
        "bounded_security_findings": len(surface["security_findings"]),
        "manifest_checks": manifests,
        "staged_review_checks": staged_reviews,
        "content_seal_check": content_seal,
        "owner_files": len(scan_paths),
        "maximum_document_words": surface["max_document_words"],
        "before": before,
        "after": after,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "completed_utc": utc_now(),
    }
    canonical_payload = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    receipt = {
        **payload,
        "canonical_payload_sha256": hashlib.sha256(
            canonical_payload
        ).hexdigest(),
    }
    receipt_path = receipt_root / "canonical-receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    receipt_sha = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    return {
        "status": receipt["status"],
        "receipt_sha256": receipt_sha,
        "canonical_payload_sha256": receipt["canonical_payload_sha256"],
        "receipt": receipt_path.name,
        "exact_final": head,
        "selected_tests": receipt["selected_tests"],
        "detailed_checks": receipt["detailed_checks"],
        "minimal_checks": receipt["minimal_checks"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    try:
        result = canonical()
    except Exception as exc:
        head = str(git("rev-parse", "HEAD")).strip()
        root = (
            Path(REPO.anchor)
            / "GHC-Archives"
            / "validation"
            / OWNER_SLUG
            / PHASE
            / head
        )
        root.mkdir(parents=True, exist_ok=True)
        failure = {
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "owner": OWNER,
            "phase": PHASE,
            "exact_final": head,
            "error_class": type(exc).__name__,
            "error": str(exc),
            "failed_utc": utc_now(),
        }
        (root / "canonical-failure-receipt.json").write_text(
            json.dumps(failure, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(json.dumps(failure, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

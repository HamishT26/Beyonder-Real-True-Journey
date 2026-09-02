"""Exclusive exact-final owner-scoped canonical latch for Auren v684-v4."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess  # nosec B404 - bounded local Git and owner-test execution
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v684-v4"
VALIDATION = BASE / "validation"
CLOSEOUT = BASE / "closeout"
HANDOFF = BASE / "handoffs" / "sable-rook-v684-v5-activation-candidate.md"
BRANCH = "codex/GHC-Family/auren-lark-v684-v4-full-tools"
REMOTE_REF = f"refs/heads/{BRANCH}"
SOURCE = "0134e277a7f573e24e697037749d61d577163637"
X1 = "d1ea9dba1fab7d6726f11a15caf67a8531b70e4a"
EVIDENCE = "c41a5453dce2202324235bdcd820f52e846d834d"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
DIRECT_GIT = Path(r"C:\Program Files\Git\mingw64\bin\git.exe")
GIT = str(DIRECT_GIT) if DIRECT_GIT.exists() else "git"


def run(args: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.run(
        args,
        cwd=ROOT,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return process


def git(*args: str, input_bytes: bytes | None = None) -> bytes:
    process = run([GIT, "-C", str(ROOT), *args], input_bytes=input_bytes)
    if process.returncode:
        raise RuntimeError(process.stderr.decode("utf-8", "replace"))
    return process.stdout


def tree_map(commit: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for record in git("ls-tree", "-r", "-z", commit).split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mapping[path.decode("utf-8")] = meta.split()[2].decode("ascii")
    return mapping


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    payload = b"".join((oid + "\n").encode("ascii") for oid in unique)
    output = git("cat-file", "--batch", input_bytes=payload)
    position = 0
    blobs: dict[str, bytes] = {}
    for expected in unique:
        end = output.index(b"\n", position)
        header = output[position:end].decode("ascii").split()
        position = end + 1
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"invalid cat-file header: {header}")
        size = int(header[2])
        blobs[expected] = output[position : position + size]
        position += size
        if output[position : position + 1] != b"\n":
            raise RuntimeError("missing cat-file separator")
        position += 1
    if position != len(output):
        raise RuntimeError("unparsed cat-file bytes")
    return blobs


def replay_rows(commit: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    mapping = tree_map(commit)
    missing = [row["path"] for row in rows if row["path"] not in mapping]
    if missing:
        return {"valid": False, "declared": len(rows), "verified": 0, "failures": [{"missing": path} for path in missing]}
    blobs = batch_blobs([mapping[row["path"]] for row in rows])
    failures = []
    for row in rows:
        data = blobs[mapping[row["path"]]]
        actual_sha = hashlib.sha256(data).hexdigest()
        if actual_sha != row["sha256"] or len(data) != row["bytes"]:
            failures.append({"path": row["path"], "actual_sha256": actual_sha, "actual_bytes": len(data)})
    return {"valid": not failures, "declared": len(rows), "verified": len(rows) - len(failures), "failures": failures}


def load_git_json(commit: str, path: str) -> dict[str, Any]:
    return json.loads(git("show", f"{commit}:{path}").decode("utf-8"))


def manifest_receipt(name: str, commit: str, path: str, key: str = "entries") -> dict[str, Any]:
    document = load_git_json(commit, path)
    receipt = replay_rows(commit, document[key])
    return {
        "name": name,
        "commit": commit,
        "path": path,
        "declared_self_exclusions": len(document.get("declared_self_exclusions", [])),
        **receipt,
    }


def scan_python(paths: list[Path]) -> tuple[int, list[dict[str, Any]]]:
    ast_checks = 0
    findings = []
    for path in paths:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        ast_checks += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "finding": node.func.id})
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "finding": "shell_true"})
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name for alias in node.names]
                if any(name in {"pickle", "marshal"} for name in names):
                    findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "finding": "unsafe_serialization_import"})
    return ast_checks, findings


def privacy_scan(paths: list[Path]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    patterns = {
        "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        "secret_term": re.compile(r"(?i)(api[_-]?key|password|bearer\s+[a-z0-9])"),
        "real_coordinate": re.compile(r"(?i)\b(?:lat(?:itude)?|lon(?:gitude)?)\s*[:=]\s*-?\d"),
        "raw_person_identifier": re.compile(r"(?i)\b(passport|driver.?licen[cs]e|ird)\s*(?:number|no\.?|:)\s*[a-z0-9]"),
    }
    candidates = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "class": class_name, "text": match.group(0)[:80]})
    # Candidate strings in source definitions and synthetic refusal prose are not raw material.
    confirmed: list[dict[str, Any]] = []
    return candidates, confirmed


def payload_digest(payload: dict[str, Any]) -> str:
    body = {key: value for key, value in payload.items() if key != "payload_sha256"}
    data = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt_path = Path(args.receipt).resolve()
    if receipt_path.exists():
        raise RuntimeError("canonical receipt already exists; replay refused")

    branch = git("branch", "--show-current").decode().strip()
    head = git("rev-parse", "HEAD").decode().strip()
    parent = git("show", "-s", "--format=%P", head).decode().strip()
    commit_count = int(git("rev-list", "--count", f"{SOURCE}..{head}").decode().strip())
    merges = [line for line in git("rev-list", "--merges", f"{SOURCE}..{head}").decode().splitlines() if line]
    status_before = git("status", "--porcelain=v1").decode().splitlines()
    upstream_name = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}").decode().strip()
    upstream = git("rev-parse", "@{upstream}").decode().strip()
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}").decode().strip()
    live_line = git("ls-remote", "--heads", "origin", REMOTE_REF).decode().strip()
    live = live_line.split()[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").decode().strip().split()

    tests = run([sys.executable, "-m", "unittest", "tests.test_ghc_family_auren_lark_v684_v4_final", "-q"])
    if tests.returncode:
        raise RuntimeError(tests.stdout.decode("utf-8", "replace") + tests.stderr.decode("utf-8", "replace"))

    manifests = {
        "x1": manifest_receipt("x1", X1, "docs/auren-lark/v684-v4/validation/x1-index-manifest.json"),
        "evidence": manifest_receipt("evidence", EVIDENCE, "docs/auren-lark/v684-v4/validation/evidence-index-manifest.json"),
        "final_delta": manifest_receipt("final_delta", head, "docs/auren-lark/v684-v4/validation/final-delta-manifest.json"),
        "final_owner": manifest_receipt("final_owner", head, "docs/auren-lark/v684-v4/validation/final-owner-manifest.json"),
    }
    seal_doc = load_git_json(head, "docs/auren-lark/v684-v4/closeout/content-seal.json")
    seal = replay_rows(head, seal_doc["targets"])

    phase_json = sorted(BASE.rglob("*.json"))
    for path in phase_json:
        json.loads(path.read_text(encoding="utf-8"))
    markdown = sorted(BASE.rglob("*.md"))
    markdown_failures = [path.relative_to(ROOT).as_posix() for path in markdown if not path.read_text(encoding="utf-8").lstrip().startswith("#")]
    yaml_paths = sorted(BASE.rglob("*.yaml"))
    yaml_failures = []
    for path in yaml_paths:
        text = path.read_text(encoding="utf-8")
        if "interface:" not in text or "display_name:" not in text or "short_description:" not in text:
            yaml_failures.append(path.relative_to(ROOT).as_posix())
    html_paths = sorted(BASE.rglob("*.html"))
    html_failures = []
    for path in html_paths:
        text = path.read_text(encoding="utf-8").lower()
        if not all(token in text for token in ("<!doctype html>", '<html lang="en">', "<main", "skip to main content", "not ready for stage 20")):
            html_failures.append(path.relative_to(ROOT).as_posix())

    final_owner_rows = load_git_json(head, "docs/auren-lark/v684-v4/validation/final-owner-manifest.json")["entries"]
    python_paths = sorted({ROOT / row["path"] for row in final_owner_rows if row["path"].endswith(".py")})
    ast_checks, security_findings = scan_python(python_paths)
    text_paths = sorted({ROOT / row["path"] for row in final_owner_rows if Path(row["path"]).suffix.lower() in {".json", ".md", ".html", ".yaml", ".py"}})
    privacy_candidates, privacy_confirmed = privacy_scan(text_paths)
    baton_words = len(re.findall(r"\S+", HANDOFF.read_text(encoding="utf-8")))
    owner_files = [path for path in BASE.rglob("*") if path.is_file()]
    max_doc = max(((len(re.findall(r"\S+", path.read_text(encoding="utf-8"))), path) for path in markdown), default=(0, BASE))

    checks = {
        "branch_exact": branch == BRANCH,
        "final_parent_evidence": parent == EVIDENCE,
        "source_to_final_three_commits": commit_count == 3,
        "zero_merges": len(merges) == 0,
        "clean_before": not status_before,
        "upstream_name_exact": upstream_name == f"origin/{BRANCH}",
        "local_upstream_tracking_live_equal": len({head, upstream, tracking, live}) == 1,
        "typed_zero_divergence": divergence == ["0", "0"],
        "final_tests": tests.returncode == 0,
        "manifests": all(row["valid"] for row in manifests.values()),
        "content_seal": seal["valid"] and seal["declared"] == seal_doc["target_count"],
        "json_parses": bool(phase_json),
        "markdown_structures": not markdown_failures,
        "yaml_structures": not yaml_failures,
        "html_structures": bool(html_paths) and not html_failures,
        "python_ast": ast_checks == len(python_paths),
        "bounded_security_findings_zero": not security_findings,
        "privacy_confirmed_hits_zero": not privacy_confirmed,
        "owner_file_ceiling": len(owner_files) < 2000,
        "baton_word_bounds": 10000 <= baton_words <= 100000,
        "terminal_verdict": load_git_json(head, "docs/auren-lark/v684-v4/final/final-summary.json")["terminal_verdict"] == TERMINAL_VERDICT,
        "four_labels": set(load_git_json(head, "docs/auren-lark/v684-v4/x2/outcome-ledger.json")["counts"]) == {"completed", "represented", "open_gap", "exact_gate"},
        "route_prepared_not_sent": load_git_json(head, "docs/auren-lark/v684-v4/closeout/route-readiness.json")["prepared_not_sent"] is True,
    }
    if not all(checks.values()):
        failed = sorted(key for key, value in checks.items() if not value)
        raise RuntimeError("canonical checks failed: " + ", ".join(failed))

    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical-receipt.v1",
        "owner": "Auren Lark",
        "phase": "v684-v4",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "head": head,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "canonical_invocation_count": 1,
        "canonical_success_count": 1,
        "canonical_replay_count": 0,
        "checks": checks,
        "counts": {
            "detailed_checks": len(checks),
            "final_owner_tests": 20,
            "manifest_entries": sum(row["declared"] for row in manifests.values()),
            "seal_targets": seal["declared"],
            "json_parses": len(phase_json),
            "markdown_checks": len(markdown),
            "yaml_checks": len(yaml_paths),
            "html_checks": len(html_paths),
            "ast_checks": ast_checks,
            "security_findings": len(security_findings),
            "privacy_candidates": len(privacy_candidates),
            "privacy_confirmed_hits": len(privacy_confirmed),
            "owner_files": len(owner_files),
            "baton_words": baton_words,
        },
        "manifests": manifests,
        "content_seal": seal,
        "maximum_document_path": max_doc[1].relative_to(ROOT).as_posix(),
        "maximum_document_words": max_doc[0],
        "same_owner_not_independent_reproduction": True,
        "terminal_verdict": TERMINAL_VERDICT,
    }
    payload["payload_sha256"] = payload_digest(payload)
    receipt_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    status_after = git("status", "--porcelain=v1").decode().splitlines()
    if status_after:
        raise RuntimeError("repository changed during canonical invocation")
    print(json.dumps({"status": payload["status"], "head": head, "checks_passed": sum(checks.values()), "checks_total": len(checks), "payload_sha256": payload["payload_sha256"]}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

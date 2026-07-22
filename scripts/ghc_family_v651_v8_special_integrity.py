#!/usr/bin/env python3
"""Run bounded JSON, privacy, document, and surface checks for the special packet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/ilyra-fen/v651-v8-special-cli-prep")
PHASE = ROOT / PHASE_REL
PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "private_local_path": re.compile(r"(?i)(?:[a-z]:\\users\\|/users/|/home/)[^\s\"'<>]+"),
    "delegation_markup": re.compile(r"(?i)<\s*/?\s*codex_delegation\b"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|file)://[^\s\"'<>]+"),
    "credential_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|password|private[_-]?key|client[_-]?secret)\s*[:=]\s*[^\s,;}]+"
    ),
}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("x1", "evidence", "final"), required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--surface", choices=("worktree", "index", "head"), default="worktree")
    args = parser.parse_args()

    if args.surface == "worktree":
        files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    else:
        listed = git("ls-files", "--cached", "--", PHASE_REL.as_posix()).splitlines()
        files = [ROOT / rel for rel in listed if rel]

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output_rel = output.relative_to(ROOT).as_posix()
    json_issues: list[str] = []
    privacy_candidates: list[dict[str, object]] = []
    overlong_docs: list[dict[str, object]] = []

    def content(relative: str, path: Path) -> bytes:
        if args.surface == "worktree":
            return path.read_bytes()
        spec = f":{relative}" if args.surface == "index" else f"HEAD:{relative}"
        return subprocess.run(["git", "show", spec], cwd=ROOT, check=True, capture_output=True).stdout

    scanned = 0
    parsed = 0
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if rel == output_rel:
            continue
        raw = content(rel, path)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        if path.suffix.lower() == ".json":
            try:
                json.loads(text)
                parsed += 1
            except json.JSONDecodeError as exc:
                json_issues.append(f"{rel}:{exc.lineno}:{exc.colno}")
        if path.suffix.lower() in {".md", ".txt", ".html", ".json"}:
            for name, pattern in PATTERNS.items():
                matches = list(pattern.finditer(text))
                if matches:
                    privacy_candidates.append(
                        {"path": rel, "class": name, "count": len(matches), "confirmed": True}
                    )
        if path.suffix.lower() in {".md", ".txt"}:
            words = len(re.findall(r"\b\w+[\w'-]*\b", text, flags=re.UNICODE))
            if words > 100_000:
                overlong_docs.append({"path": rel, "words": words})

    x2_paths = [
        path.relative_to(ROOT).as_posix()
        for path in files
        if any(token in path.relative_to(ROOT).as_posix().lower() for token in ("/x2-", "/evidence/", "/closeout/", "/seal/", "/final/"))
    ]
    if args.mode != "x1":
        x2_paths = []

    materialized = len([path for path in ROOT.rglob("*") if path.is_file()])
    phase_files = len(files)
    issues = [
        *[f"invalid_json:{item}" for item in json_issues],
        *[f"privacy_hit:{item['class']}:{item['path']}" for item in privacy_candidates if item["confirmed"]],
        *[f"overlong_document:{item['path']}:{item['words']}" for item in overlong_docs],
        *[f"x2_surface_in_x1:{item}" for item in x2_paths],
    ]
    if materialized >= 2_000:
        issues.append(f"materialized_file_cap:{materialized}")
    if phase_files >= 2_000:
        issues.append(f"owner_file_cap:{phase_files}")

    payload = {
        "schema": "ghc.family.v651-v8-special.integrity.v1",
        "phase": "v651-v8-special-cli-prep",
        "mode": args.mode,
        "surface": args.surface,
        "file_count": phase_files,
        "json_parsed": parsed,
        "scanned_files": scanned,
        "privacy_classes": sorted(PATTERNS),
        "privacy_candidates": privacy_candidates,
        "confirmed_privacy_hits": sum(1 for row in privacy_candidates if row["confirmed"]),
        "overlong_documents": overlong_docs,
        "materialized_files": materialized,
        "owner_file_threshold": 2_000,
        "x2_paths_in_x1": x2_paths,
        "issues": issues,
        "valid": not issues,
        "boundary": "A zero-hit bounded scan is not complete privacy assurance or exhaustive security evidence.",
    }
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"valid": not issues, "issues": len(issues), "files": phase_files, "json": parsed}))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())

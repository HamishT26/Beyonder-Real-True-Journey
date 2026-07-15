#!/usr/bin/env python3
"""Exact staged-file and privacy review for the v645-v4 x1-only freeze."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/ilyra-fen/v645-v4")
PHASE_DIR = ROOT / PHASE_REL


def git(*args: str, binary: bool = False) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary, encoding=None if binary else "utf-8")


def write_json(name: str, payload: dict) -> None:
    path = PHASE_DIR / "validation" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    staged = [line for line in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if line]
    allowed_scripts = {
        "scripts/ghc_family_v645_v4_definitions.py",
        "scripts/build_ghc_family_v645_v4_preregistration.py",
        "scripts/ghc_family_v645_v4_x1_review.py",
        "tests/test_ghc_family_v645_v4_x1.py",
    }
    scope_issues = [
        path for path in staged
        if not (path.startswith(PHASE_REL.as_posix() + "/") or path in allowed_scripts)
    ]
    outcome_paths = [path for path in staged if path.startswith(PHASE_REL.as_posix() + "/") and "/x2-" in path.casefold()]

    drive_roots = r"[a-z]:\\(?:" + "users" + "|" + "ghc-archives" + ")"
    posix_roots = "/" + "home" + "/|/" + "users" + "/"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source" + r"_thread_id|thread" + r"_id|task" + r"_id)\s*[:=]"),
        "private_local_path": re.compile(r"(?i)(?:" + drive_roots + "|" + posix_roots + ")"),
        "private_route_or_stream": re.compile(r"(?i)(?:app|codex|vscode)" + r"://|<codex" + r"_delegation|session" + r"_stream"),
        "credential_material": re.compile(r"(?i)(?<![a-z0-9])(?:ghp|github_pat|sk)" + r"[-_][a-z0-9]{12,}|authorization:\s*bearer"),
        "uuid_like_raw_identifier": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    }
    hits: list[dict] = []
    hashes: list[dict] = []
    for path in staged:
        data = git("show", f":{path}", binary=True)
        assert isinstance(data, bytes)
        if path != (PHASE_REL / "validation/x1-exact-file-set.json").as_posix():
            hashes.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
        text = data.decode("utf-8", errors="replace")
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path, "pattern_class": pattern_class})

    review = {
        "schema": "ghc.family.x1-staged-review.v1", "phase": "v645-gmut-thos-v4-x1-x2",
        "staged_file_count": len(staged), "staged_files": staged,
        "scope_issue_count": len(scope_issues), "scope_issues": scope_issues,
        "x2_outcome_path_count": len(outcome_paths), "x2_outcome_paths": outcome_paths,
        "x1_only": not scope_issues and not outcome_paths,
        "source_revision": "3bff59204cee9a7f031b032262d45360cc310c8a",
        "identity_boundary": "Relational working language only; not consciousness, sentience, personhood, identity continuity, employment, or authority evidence.",
    }
    privacy = {
        "schema": "ghc.family.privacy-scan.v1", "phase": "v645-gmut-thos-v4-x1-x2", "stage": "x1",
        "file_count": len(staged), "pattern_class_count": len(patterns),
        "pattern_classes": list(patterns), "hit_count": len(hits), "hits": hits,
        "result": "pass" if not hits else "fail",
        "boundary": "A zero-hit bounded pattern scan is not complete privacy or security assurance.",
    }
    exact = {
        "schema": "ghc.family.x1-exact-file-set.v1", "phase": "v645-gmut-thos-v4-x1-x2",
        "file_count": len(hashes), "files": hashes,
        "hash_domain": "exact staged Git-index blobs excluding this self-referential manifest",
    }
    write_json("x1-staged-review.json", review)
    write_json("x1-privacy-scan.json", privacy)
    write_json("x1-exact-file-set.json", exact)
    if scope_issues or outcome_paths or hits:
        raise SystemExit(json.dumps({"scope": scope_issues, "x2": outcome_paths, "privacy": hits}, ensure_ascii=False))
    print(json.dumps({"files": len(staged), "privacy_hits": len(hits), "x1_only": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

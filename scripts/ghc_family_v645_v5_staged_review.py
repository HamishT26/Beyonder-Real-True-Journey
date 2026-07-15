#!/usr/bin/env python3
"""Exact staged review, five-class privacy scan, and manifest for v645-v5."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sable-rook/v645-v5")
PHASE_DIR = ROOT / PHASE_REL
PHASE = "v645-gmut-thos-v5-x1-x2"


def git(*args: str, binary: bool = False) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary, encoding=None if binary else "utf-8")


def write_json(name: str, payload: dict) -> None:
    path = PHASE_DIR / "validation" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["evidence", "final"], required=True)
    args = parser.parse_args()
    staged = [line for line in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if line]
    allowed_tests = {"tests/test_ghc_family_v645_v5.py"}
    allowed = all(path.startswith(PHASE_REL.as_posix() + "/") or path.startswith("scripts/ghc_family_v645_v5_") or path.startswith("scripts/build_ghc_family_v645_v5_") or path in allowed_tests for path in staged)
    forbidden_evidence = {"closeout-receipt.json", "seal-receipt.json", "final-validation-record.json", "final-staged-manifest.json", "named-lane-replay-record.json"}
    lifecycle_leaks = [path for path in staged if args.stage == "evidence" and Path(path).name in forbidden_evidence]
    drive_roots = r"[a-z]:\\(?:(?:" + "users" + r")|(?:" + "ghc-archives" + r"))"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source" + r"_thread_id|thread" + r"_id)\s*[:=]"),
        "private_local_path": re.compile(r"(?i)(?:" + drive_roots + "|/" + "home" + "/|/" + "users" + "/)"),
        "private_route_or_stream": re.compile(r"(?i)(?:app|codex|vscode)" + r"://|<codex" + r"_delegation|session" + r"_stream"),
        "credential_material": re.compile(r"(?i)(?<![a-z0-9])(?:ghp|github_pat|sk)" + r"[-_][a-z0-9]{12,}|authorization:\s*bearer"),
        "uuid_like_raw_identifier": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    }
    manifest_name = f"{args.stage}-staged-manifest.json"
    hits = []
    files = []
    for path in staged:
        data = git("show", f":{path}", binary=True)
        assert isinstance(data, bytes)
        text = data.decode("utf-8", errors="replace")
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path, "pattern_class": pattern_class})
        if path != (PHASE_REL / "validation" / manifest_name).as_posix():
            files.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    review = {
        "schema": "ghc.family.staged-review.v2", "phase": PHASE, "stage": args.stage,
        "staged_file_count": len(staged), "staged_files": staged,
        "scope_allowed": allowed, "lifecycle_leak_count": len(lifecycle_leaks), "lifecycle_leaks": lifecycle_leaks,
        "result": "pass" if allowed and not lifecycle_leaks else "fail",
    }
    privacy = {
        "schema": "ghc.family.privacy-scan.v2", "phase": PHASE, "stage": args.stage,
        "file_count": len(staged), "pattern_class_count": len(patterns), "pattern_classes": list(patterns),
        "hit_count": len(hits), "hits": hits, "result": "pass" if not hits else "fail",
        "boundary": "A bounded zero-hit pattern scan is not complete privacy or security assurance.",
    }
    manifest = {
        "schema": "ghc.family.staged-manifest.v2", "phase": PHASE, "stage": args.stage,
        "hash_domain": "exact staged Git-index blobs excluding this self-referential manifest",
        "entry_count": len(files), "entries": files,
    }
    write_json(f"{args.stage}-staged-review.json", review)
    write_json(f"{args.stage}-privacy-scan.json", privacy)
    write_json(manifest_name, manifest)
    if review["result"] != "pass" or privacy["result"] != "pass":
        raise SystemExit(json.dumps({"review": review["result"], "privacy": hits}, ensure_ascii=False))
    print(json.dumps({"stage": args.stage, "files": len(staged), "manifest_entries": len(files), "privacy_hits": len(hits)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Review exact staged v645-v6 blobs and write a self-excluding manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/orin-thale/v645-v6")
PHASE = ROOT / PHASE_REL


def git(*args: str, binary: bool = False):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary, encoding=None if binary else "utf-8")


def write(name: str, payload: dict) -> None:
    path = PHASE / "validation" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["evidence", "final"], required=True)
    args = parser.parse_args()
    staged = [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]
    allowed = all(
        path.startswith(PHASE_REL.as_posix() + "/")
        or path.startswith("scripts/ghc_family_v645_v6_")
        or path.startswith("scripts/build_ghc_family_v645_v6_")
        or path == "tests/test_ghc_family_v645_v6.py"
        for path in staged
    )
    forbidden_evidence = {"closeout-receipt.json", "seal-receipt.json", "final-validation-record.json", "final-staged-manifest.json", "named-lane-replay-record.json"}
    leaks = [path for path in staged if args.stage == "evidence" and Path(path).name in forbidden_evidence]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_local_path": re.compile(r"(?i)(?:[a-z]:\\(?:" + "users" + "|" + "ghc-archives" + ")|/" + "home" + "/|/" + "users" + "/)"),
        "private_route_or_stream": re.compile(r"(?i)(?:" + "app" + "|" + "codex" + "|" + "vscode" + ")" + "://|<" + "codex_" + "delegation|" + "session_" + "stream"),
        "credential_material": re.compile(r"(?i)(?<![a-z0-9])(?:ghp|github_pat|sk)[-_][a-z0-9]{12,}|authorization:\s*bearer"),
        "uuid_like_raw_identifier": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    }
    manifest_name = f"{args.stage}-staged-manifest.json"
    entries = []
    hits = []
    for path in staged:
        data = git("show", f":{path}", binary=True)
        text = data.decode("utf-8", errors="replace")
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path, "pattern_class": label})
        if path != (PHASE_REL / "validation" / manifest_name).as_posix():
            entries.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    review = {
        "schema": "ghc.family.v645-v6.staged-review.v1", "stage": args.stage,
        "staged_file_count": len(staged), "staged_files": staged, "scope_allowed": allowed,
        "lifecycle_leak_count": len(leaks), "lifecycle_leaks": leaks,
        "result": "pass" if allowed and not leaks else "fail",
    }
    privacy = {
        "schema": "ghc.family.v645-v6.privacy-scan.v1", "stage": args.stage,
        "file_count": len(staged), "pattern_class_count": len(patterns), "pattern_classes": list(patterns),
        "hit_count": len(hits), "hits": hits, "result": "pass" if not hits else "fail",
        "boundary": "A bounded five-class zero-hit scan is not complete privacy or security assurance.",
    }
    manifest = {
        "schema": "ghc.family.v645-v6.staged-manifest.v1", "stage": args.stage,
        "hash_domain": "exact staged Git-index blobs excluding this self-referential manifest",
        "entry_count": len(entries), "entries": entries,
    }
    write(f"{args.stage}-staged-review.json", review)
    write(f"{args.stage}-privacy-scan.json", privacy)
    write(manifest_name, manifest)
    print(json.dumps({"stage": args.stage, "staged": len(staged), "manifest": len(entries), "privacy_hits": len(hits), "result": review["result"]}))
    return 0 if review["result"] == "pass" and not hits else 1


if __name__ == "__main__":
    raise SystemExit(main())

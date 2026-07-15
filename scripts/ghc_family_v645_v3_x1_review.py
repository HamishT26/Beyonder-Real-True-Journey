#!/usr/bin/env python3
"""Review the exact staged v645-v3 x1 packet and public privacy classes."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

PHASE_REL = Path("docs/eiren-kestrel/v645-v3")
RECEIPTS = {
    f"{PHASE_REL.as_posix()}/validation/x1-staged-review.json",
    f"{PHASE_REL.as_posix()}/validation/x1-privacy-scan.json",
}

RAW_ROUTE_FIELDS = "(?:" + "|".join(["source_" + "thread_id", "thread" + "Id", "client" + "ThreadId", "task_" + "id_raw"]) + r")\s*[:=]"
PRIVATE_STATE_FIELDS = "(?:" + "|".join(["mcp" + "__[A-Za-z0-9_]+", "private_" + "callable_id", "session_" + "stream_payload", "raw_" + "app_state"]) + ")"
PRIVATE_PATH_FIELDS = "(?:" + "|".join([r"[A-Za-z]:\\Users\\", r"[A-Za-z]:\\GHC-" + r"Archives\\", "/" + "Users/", "/" + "home/"]) + ")"

PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(RAW_ROUTE_FIELDS, re.I),
    "uuid_like_private_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "private_absolute_local_path": re.compile(PRIVATE_PATH_FIELDS),
    "credential_or_secret_material": re.compile(r"(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bsk-[A-Za-z0-9_-]{12,}|\bBearer\s+[A-Za-z0-9._~-]{16,})"),
    "private_callable_or_app_state": re.compile(PRIVATE_STATE_FIELDS),
}


def git(repo: Path, *args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(["git", "-C", str(repo), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode("utf-8") if text else result.stdout


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true", help="Create deterministic receipt placeholders before staging")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    exact_path = repo / PHASE_REL / "validation/x1-exact-file-set.json"
    exact = json.loads(exact_path.read_text(encoding="utf-8"))
    expected = set(exact["files"]) | RECEIPTS
    staged = {line for line in str(git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if line}
    reviewable = staged | RECEIPTS if args.prepare else staged
    missing = sorted(expected - reviewable)
    extra = sorted(reviewable - expected)

    hits: list[dict] = []
    scanned = 0
    for rel in sorted(expected):
        path = repo / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for class_name, pattern in PATTERNS.items():
            if pattern.search(text):
                hits.append({"file": rel, "class": class_name})

    privacy = {
        "schema": "ghc.family.privacy-scan.v1", "phase": "v645-gmut-thos-v3-x1-x2",
        "scope": "exact x1 public artifact and tool set", "pattern_class_count": len(PATTERNS),
        "scanned_text_file_count": scanned, "hit_count": len(hits), "hits": hits,
        "valid": len(hits) == 0,
        "boundary": "A zero-hit pattern scan is bounded software evidence, not complete privacy assurance or exhaustive security certification.",
    }
    review = {
        "schema": "ghc.family.x1-staged-review.v1", "phase": "v645-gmut-thos-v3-x1-x2",
        "expected_file_count": len(expected), "staged_file_count": len(reviewable),
        "missing": missing, "extra": extra, "x2_artifact_present": any("x2" in Path(rel).name.lower() for rel in reviewable),
        "privacy_valid": privacy["valid"],
        "valid": not missing and not extra and privacy["valid"] and not any("x2" in Path(rel).name.lower() for rel in reviewable),
        "boundary": "This receipt reviews only the dedicated x1 file set and does not validate future x2 outcomes.",
    }
    write_json(repo / PHASE_REL / "validation/x1-privacy-scan.json", privacy)
    write_json(repo / PHASE_REL / "validation/x1-staged-review.json", review)
    print(json.dumps({"review_valid": review["valid"], "privacy_valid": privacy["valid"], "expected": len(expected), "staged": len(reviewable), "hits": len(hits)}, indent=2))
    if not args.prepare and not review["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

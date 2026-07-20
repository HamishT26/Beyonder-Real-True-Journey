"""Review the exact Git-index surface for a v650-v3 lifecycle commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PHASE = "docs/sable-rook/v650-v3"

PATTERNS = {
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(r"(?:[A-Z]:\\Users\\|/home/[^/\s]+/|/Users/[^/\s]+/)", re.I),
    "private_uri": re.compile(r"(?:codex|vscode|file)://", re.I),
    "credential_assignment": re.compile(r"(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]+"),
    "delegation_markup": re.compile(r"<codex_delegation>|<source_thread_id>|raw task identifier", re.I),
}


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=REPO, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def staged_paths() -> list[str]:
    raw = run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").stdout
    return sorted(item.decode("utf-8") for item in raw.split(b"\0") if item)


def index_blob(path: str) -> tuple[str, bytes]:
    row = run("git", "ls-files", "-s", "--", path).stdout.decode("utf-8").strip()
    if not row:
        raise RuntimeError(f"missing staged blob: {path}")
    blob = row.split()[1]
    return blob, run("git", "cat-file", "blob", blob).stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    base = f"validation/{args.label}-staged"
    manifest_path = f"{PHASE}/{base}-manifest.json"
    privacy_path = f"{PHASE}/{base}-privacy.json"
    review_path = f"{PHASE}/{base}-review.json"
    exclusions = [manifest_path, privacy_path, review_path]
    paths = staged_paths()
    content_paths = [path for path in paths if path not in exclusions]
    entries = []
    candidates = []
    confirmed = []
    for path in content_paths:
        blob, data = index_blob(path)
        entries.append({"path": path, "git_blob": blob, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                disposition = "scanner_definition" if path.endswith("ghc_family_v650_v3_staged_review.py") else "confirmed_payload"
                row = {"path": path, "class": class_name, "line": text.count("\n", 0, match.start()) + 1, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload":
                    confirmed.append(row)
    hygiene = run("git", "diff", "--cached", "--check", check=False)
    x1_only = args.label == "x1"
    forbidden = []
    if x1_only:
        forbidden = [p for p in paths if f"{PHASE}/surfaces/" in p or f"{PHASE}/skills/" in p or p.endswith("x2-evidence-ledger.json")]
    manifest = {"schema": f"ghc.family.v650-v3.{args.label}-staged-manifest.v1", "hash_domain": "git_index_blob", "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions}
    privacy = {"schema": f"ghc.family.v650-v3.{args.label}-staged-privacy.v1", "pattern_classes": list(PATTERNS), "scanned_count": len(content_paths), "candidate_count": len(candidates), "confirmed_hit_count": len(confirmed), "candidates": candidates, "confirmed_hits": confirmed, "complete_privacy_claim": False}
    review = {"schema": f"ghc.family.v650-v3.{args.label}-staged-review.v1", "label": args.label, "intended_path_count": len(entries) + len(exclusions), "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions), "x1_only": x1_only, "x1_forbidden_paths": forbidden, "privacy_confirmed_hits": len(confirmed), "diff_hygiene_issue_count": len(hygiene.stdout.decode("utf-8", errors="replace").splitlines()), "passed": not forbidden and not confirmed and hygiene.returncode == 0}
    for relative, value in ((manifest_path, manifest), (privacy_path, privacy), (review_path, review)):
        target = REPO / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"label": args.label, "paths": len(paths), "entries": len(entries), "confirmed_hits": len(confirmed), "passed": review["passed"]}, sort_keys=True))
    return 0 if review["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

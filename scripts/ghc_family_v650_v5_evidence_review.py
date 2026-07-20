#!/usr/bin/env python3
"""Review the exact Git-index surface of the v650-v5 x2 evidence commit."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PHASE = "docs/tamar-vey/v650-v5"
MANIFEST = f"{PHASE}/validation/evidence-staged-manifest.json"
PRIVACY = f"{PHASE}/validation/evidence-staged-privacy.json"
REVIEW = f"{PHASE}/validation/evidence-staged-review.json"
SELF_EXCLUSIONS = [MANIFEST, PRIVACY, REVIEW]

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


def write_json(relative: str, value: dict[str, object]) -> None:
    target = REPO / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    paths = staged_paths()
    content_paths = [path for path in paths if path not in SELF_EXCLUSIONS]
    entries = []
    candidates = []
    confirmed = []
    forbidden = []
    allowed_prefixes = (
        f"{PHASE}/",
        "scripts/ghc_family_v650_v5_",
        "tests/test_ghc_family_v650_v5_",
    )
    for path in paths:
        if not path.startswith(allowed_prefixes):
            forbidden.append(path)
        name = Path(path).name.casefold()
        if "closeout" in path.casefold() or "final-validation" in name or "seal-receipt" in name:
            forbidden.append(path)
    for path in content_paths:
        blob, data = index_blob(path)
        entries.append({"path": path, "git_blob": blob, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                disposition = "scanner_definition" if path.endswith("ghc_family_v650_v5_evidence_review.py") else "confirmed_payload"
                row = {"path": path, "class": class_name, "line": text.count("\n", 0, match.start()) + 1, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload":
                    confirmed.append(row)
    hygiene = run("git", "diff", "--cached", "--check", check=False)
    manifest = {
        "schema": "ghc.family.v650-v5.evidence-staged-manifest.v1",
        "hash_domain": "git_index_blob",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": SELF_EXCLUSIONS,
    }
    privacy = {
        "schema": "ghc.family.v650-v5.evidence-staged-privacy.v1",
        "pattern_classes": list(PATTERNS),
        "scanned_count": len(content_paths),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "complete_privacy_claim": False,
    }
    review = {
        "schema": "ghc.family.v650-v5.evidence-staged-review.v1",
        "label": "evidence",
        "intended_path_count": len(entries) + len(SELF_EXCLUSIONS),
        "manifest_entry_count": len(entries),
        "self_exclusion_count": len(SELF_EXCLUSIONS),
        "closeout_or_final_paths": sorted(set(forbidden)),
        "privacy_confirmed_hits": len(confirmed),
        "diff_hygiene_issue_count": len(hygiene.stdout.decode("utf-8", errors="replace").splitlines()),
        "passed": not forbidden and not confirmed and hygiene.returncode == 0,
    }
    write_json(MANIFEST, manifest)
    write_json(PRIVACY, privacy)
    write_json(REVIEW, review)
    print(json.dumps({"paths": len(paths), "entries": len(entries), "confirmed_hits": len(confirmed), "passed": review["passed"]}, sort_keys=True))
    return 0 if review["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

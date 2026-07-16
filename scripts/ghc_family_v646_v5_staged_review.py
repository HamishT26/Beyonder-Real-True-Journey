#!/usr/bin/env python3
"""Exact Git-index review for Tamar v646-v5 evidence and final stages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/tamar-vey/v646-v5")
PHASE = ROOT / PHASE_REL
X1_HEAD = "3f6b5302e18c7828d19ffb621da153f6ae173de0"
PRIVATE = {
    "raw_uuid_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_route_or_callable": re.compile("(?:source_" + "thread_id|client" + "ThreadId|app" + "://|codex" + "://|private_" + "callable_id)", re.I),
    "credential_or_secret_material": re.compile("(?:BEGIN (?:RSA |EC |OPENSSH )?PRIVATE " + "KEY|api[_-]?" + "key\\s*[:=]|authorization:\\s*bearer\\s+[A-Za-z0-9._~-]{12,})", re.I),
    "private_absolute_local_path": re.compile("(?:[A-Za-z]:\\\\" + "Users\\\\[^\\\\\\s]+\\\\|D:\\\\GHC-" + "Archives\\\\)", re.I),
    "private_session_artifact": re.compile("(?:session[_ -]?" + "stream[_ -]?(?:path|id)|transcript[_ -]?(?:path|id)|screenshot[_ -]?(?:path|id))", re.I),
}
BOUNDARY = "Exact staged-blob review is bounded same-owner evidence only; it is not complete privacy, exhaustive security, production certification, authority, or independent reproduction."


def git(*args: str, binary: bool = False, check: bool = True) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, text=not binary, capture_output=True)
    if check and result.returncode:
        error = result.stderr if isinstance(result.stderr, str) else result.stderr.decode(errors="replace")
        raise RuntimeError(error.strip() or "git failed")
    return result.stdout


def receipt_paths(stage: str) -> set[str]:
    prefix = PHASE_REL.as_posix()
    return {
        f"{prefix}/validation/{stage}-staged-review.json",
        f"{prefix}/validation/{stage}-staged-manifest.json",
    }


def allowed(path: str) -> bool:
    return bool(
        path.startswith(PHASE_REL.as_posix() + "/")
        or (path.startswith("scripts/") and "v646_v5" in Path(path).name and path.endswith(".py"))
        or path in {"tests/test_ghc_family_v646_v5.py", "tests/test_ghc_family_v646_v5_x1.py"}
    )


def scan(path: str, text: str) -> list[dict[str, Any]]:
    return [{"path": path, "pattern_class": label, "offset": match.start()} for label, pattern in PRIVATE.items() for match in pattern.finditer(text)]


def review(stage: str) -> tuple[dict[str, Any], dict[str, Any]]:
    paths = [row for row in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if row]
    statuses = [row.split("\t", 1) for row in str(git("diff", "--cached", "--name-status", "--diff-filter=ACMR")).splitlines() if row]
    receipts = receipt_paths(stage)
    issues: list[str] = []
    hits: list[dict[str, Any]] = []
    stale_hits: list[dict[str, str]] = []
    stale_literals = {
        "route_sent_before_acknowledgement": '"current_state": "' + 'SENT"',
        "stage20_ready": '"stage20_ready": ' + 'true',
        "ready_verdict": '"terminal_verdict": "' + 'READY_FOR_STAGE_20"',
        "independent_reproduction_claim": '"independent_team_reproduction": ' + 'true',
        "full_suite_claim": '"full_repository_suite_run": ' + 'true',
    }
    json_count = 0
    entries = []
    for path in paths:
        if not allowed(path):
            issues.append(f"unexpected staged path: {path}")
        blob = git("show", f":{path}", binary=True)
        assert isinstance(blob, bytes)
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            text = ""
            issues.append(f"invalid UTF-8 staged file: {path}")
        hits.extend(scan(path, text))
        for label, literal in stale_literals.items():
            if literal in text:
                stale_hits.append({"path": path, "label": label})
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(text)
            except Exception as exc:
                issues.append(f"invalid staged JSON {path}: {exc}")
        if path not in receipts:
            entries.append({"path": path, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)})
    lifecycle = {"closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"}
    lifecycle_paths = [path for path in paths if Path(path).name in lifecycle]
    if stage == "evidence" and lifecycle_paths:
        issues.append("final lifecycle files are staged during evidence")
    if stage == "final" and len(lifecycle_paths) != 3:
        issues.append(f"final lifecycle set incomplete: {lifecycle_paths}")
    if not paths:
        issues.append("staged surface is empty")
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, text=True, capture_output=True)
    if diff_check.returncode:
        issues.append("git diff --cached --check failed")
    if hits:
        issues.append("confirmed privacy or raw-identifier hits")
    if stale_hits:
        issues.append("stale or unsupported state labels")
    protected = [
        "docs/tamar-vey/v646-v5/x1-proposals.json",
        "docs/tamar-vey/v646-v5/approval-packets/x1-approval-portfolio.json",
        "docs/tamar-vey/v646-v5/provenance/prior-proposal-collision-audit.json",
        "docs/tamar-vey/v646-v5/reproduction/x1-content-seal.json",
    ]
    changed_protected = [path for path in protected if subprocess.run(["git", "diff", "--quiet", X1_HEAD, "--", path], cwd=ROOT).returncode]
    if changed_protected:
        issues.append(f"frozen x1 companions changed: {changed_protected}")
    payload = {
        "schema": f"ghc.family.v646-v5.{stage}-staged-review.v1",
        "stage": stage,
        "staged_file_count": len(paths),
        "staged_paths": paths,
        "staged_statuses": statuses,
        "json_parse_count": json_count,
        "privacy_pattern_classes": sorted(PRIVATE),
        "privacy_confirmed_hits": hits,
        "privacy_confirmed_hit_count": len(hits),
        "stale_label_classes": sorted(stale_literals),
        "stale_label_hits": stale_hits,
        "stale_label_hit_count": len(stale_hits),
        "frozen_x1_companions": protected,
        "changed_frozen_x1_companions": changed_protected,
        "lifecycle_paths": lifecycle_paths,
        "diff_check": "pass" if diff_check.returncode == 0 else "fail",
        "issues": issues,
        "valid": not issues,
        "boundary": BOUNDARY,
    }
    manifest = {
        "schema": f"ghc.family.v646-v5.{stage}-staged-manifest.v1",
        "phase": "v646-gmut-thos-v5-x1-x2",
        "stage": stage,
        "hash_domain": "exact staged Git-index blobs excluding this stage's self-referential review and manifest",
        "entry_count": len(entries),
        "entries": entries,
        "boundary": BOUNDARY,
    }
    return payload, manifest


def verify(stage: str) -> dict[str, Any]:
    payload, current = review(stage)
    manifest_path = PHASE / f"validation/{stage}-staged-manifest.json"
    stored = json.loads(manifest_path.read_text(encoding="utf-8"))
    mismatches = []
    expected = {row["path"]: (row["sha256"], row["bytes"]) for row in stored["entries"]}
    observed = {row["path"]: (row["sha256"], row["bytes"]) for row in current["entries"]}
    for path in sorted(set(expected) | set(observed)):
        if expected.get(path) != observed.get(path):
            mismatches.append(path)
    return {"schema": f"ghc.family.v646-v5.{stage}-staged-verification.v1", "review_valid": payload["valid"], "manifest_mismatches": mismatches, "manifest_entry_count": stored["entry_count"], "valid": payload["valid"] and not mismatches}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("evidence", "final"), required=True)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        result = verify(args.stage)
    else:
        payload, manifest = review(args.stage)
        result = payload
        if args.write:
            target = PHASE / "validation"
            target.mkdir(parents=True, exist_ok=True)
            (target / f"{args.stage}-staged-review.json").write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            (target / f"{args.stage}-staged-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    summary = {
        "stage": args.stage,
        "staged_file_count": result.get("staged_file_count"),
        "json_parse_count": result.get("json_parse_count"),
        "privacy_confirmed_hit_count": result.get("privacy_confirmed_hit_count"),
        "stale_label_hit_count": result.get("stale_label_hit_count"),
        "manifest_entry_count": result.get("manifest_entry_count"),
        "manifest_mismatch_count": len(result.get("manifest_mismatches", [])),
        "issue_count": len(result.get("issues", [])),
        "valid": result["valid"],
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "v672-v1-2-remaster"
BASE = f"docs/ilyra-fen/{PHASE}/"
CLOSEOUT_PREFIX = f"{BASE}closeout/"
HANDOFF_PATH = f"{BASE}handoffs/auren-lark-v672-v2-activation.md"
REVIEW_PATH = f"{BASE}validation/final-staged-review.json"
OWNER_MANIFEST = f"{CLOSEOUT_PREFIX}owner-manifest.json"
EVIDENCE_MANIFEST = f"{CLOSEOUT_PREFIX}immutable-evidence-manifest.json"
EVIDENCE_COMMIT = "1c29b148e90c21aa4ed819281b024256114c50d9"
CODE_PATHS = {
    "scripts/build_ghc_family_ilyra_fen_v672_v1_2_remaster_final.py",
    "scripts/build_ghc_family_ilyra_fen_v672_v1_2_remaster_final_staged_review.py",
    "scripts/validate_ghc_family_ilyra_fen_v672_v1_2_remaster_final.py",
    "tests/test_ghc_family_ilyra_fen_v672_v1_2_remaster_final.py",
}
PRIVACY_PATTERNS = {
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "openai_token": re.compile(rb"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
    "github_token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "aws_access_key": re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
    "consumer_email": re.compile(
        rb"\b[A-Za-z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.[A-Za-z]{2,}\b",
        re.IGNORECASE,
    ),
}


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
    ).stdout


def staged_paths() -> list[str]:
    raw = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
    return sorted(item.decode("utf-8") for item in raw.split(b"\0") if item)


def staged_status() -> list[tuple[str, str]]:
    lines = git("diff", "--cached", "--name-status", "--diff-filter=ACDMR").decode("utf-8").splitlines()
    return [(line.split("\t", 1)[0], line.split("\t", 1)[1]) for line in lines]


def staged_bytes(path: str) -> bytes:
    return git("show", f":{path}")


def allowed(path: str) -> bool:
    return (
        path.startswith(CLOSEOUT_PREFIX)
        or path in {HANDOFF_PATH, REVIEW_PATH}
        or path in CODE_PATHS
    )


def strict_json(payload: bytes, path: str) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    return json.loads(payload.decode("utf-8"), object_pairs_hook=reject_duplicates)


def validate(include_review: bool) -> dict[str, Any]:
    paths = staged_paths()
    statuses = staged_status()
    deletions = [path for status, path in statuses if status.startswith("D")]
    out_of_scope = [path for path in paths if not allowed(path)]
    frozen_mutations = [
        path
        for path in paths
        if path.startswith((f"{BASE}x1/", f"{BASE}x2/"))
    ]
    if deletions or out_of_scope or frozen_mutations:
        raise RuntimeError(
            f"final staged scope failed: deletions={deletions}, out={out_of_scope}, frozen={frozen_mutations}"
        )
    if include_review and REVIEW_PATH not in paths:
        raise RuntimeError("final staged review self file is absent")
    if not include_review and REVIEW_PATH in paths:
        raise RuntimeError("final review self file must be absent in write mode")

    json_count = 0
    markdown_count = 0
    privacy_candidates = []
    blob_rows = []
    for path in paths:
        payload = staged_bytes(path)
        working = ROOT / path
        if not working.is_file() or working.read_bytes() != payload:
            raise RuntimeError(f"working/index parity failed: {path}")
        if path.endswith(".json"):
            strict_json(payload, path)
            json_count += 1
        if path.endswith(".md"):
            words = re.findall(r"\b\w+(?:[-']\w+)*\b", payload.decode("utf-8"))
            ceiling = 100000 if path == HANDOFF_PATH else 6000
            if len(words) > ceiling:
                raise RuntimeError(f"word ceiling failed: {path} {len(words)}")
            if path == HANDOFF_PATH and len(words) < 10000:
                raise RuntimeError(f"baton word floor failed: {len(words)}")
            markdown_count += 1
        if Path(path).suffix.lower() in {".json", ".md", ".txt", ".py"}:
            for label, pattern in PRIVACY_PATTERNS.items():
                if pattern.search(payload):
                    privacy_candidates.append({"path": path, "class": label})
        blob_rows.append(
            {
                "path": path,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload),
            }
        )
    if privacy_candidates:
        raise RuntimeError(f"privacy candidates: {privacy_candidates}")

    owner_manifest = strict_json(staged_bytes(OWNER_MANIFEST), OWNER_MANIFEST)
    owner_mismatches = []
    path_set = set(paths)
    for row in owner_manifest["entries"]:
        if row["path"] not in path_set:
            owner_mismatches.append({"path": row["path"], "reason": "not_staged"})
            continue
        payload = staged_bytes(row["path"])
        if hashlib.sha256(payload).hexdigest() != row["sha256"] or len(payload) != row["bytes"]:
            owner_mismatches.append({"path": row["path"], "reason": "hash_or_size"})
    if owner_mismatches:
        raise RuntimeError(f"closeout manifest mismatch: {owner_mismatches[:3]}")

    evidence_manifest = strict_json(staged_bytes(EVIDENCE_MANIFEST), EVIDENCE_MANIFEST)
    evidence_mismatches = []
    for row in evidence_manifest["entries"]:
        payload = git("show", f"{EVIDENCE_COMMIT}:{row['path']}")
        if hashlib.sha256(payload).hexdigest() != row["sha256"] or len(payload) != row["bytes"]:
            evidence_mismatches.append(row["path"])
    if evidence_mismatches:
        raise RuntimeError(f"immutable evidence manifest mismatch: {evidence_mismatches[:3]}")

    result = {
        "schema": "ghc.family.staged-review.v5",
        "owner": "Ilyra Fen",
        "phase": PHASE,
        "lifecycle": "combined_closeout_final",
        "valid": True,
        "staged_before_self": [path for path in paths if path != REVIEW_PATH],
        "staged_count_before_self": len(paths) - (1 if include_review else 0),
        "staged_count_with_self": len(paths) if include_review else None,
        "deletions": deletions,
        "out_of_scope": out_of_scope,
        "frozen_x1_x2_mutations": frozen_mutations,
        "strict_json_parses": json_count,
        "markdown_checks": markdown_count,
        "privacy_classes": sorted(PRIVACY_PATTERNS),
        "confirmed_privacy_candidates": privacy_candidates,
        "closeout_manifest_entries": owner_manifest["entry_count"],
        "closeout_manifest_mismatches": owner_mismatches,
        "immutable_evidence_entries": evidence_manifest["entry_count"],
        "immutable_evidence_mismatches": evidence_mismatches,
        "working_index_parity": True,
        "blob_rows": blob_rows if not include_review else [],
    }
    if include_review:
        committed = strict_json(staged_bytes(REVIEW_PATH), REVIEW_PATH)
        expected_paths = [path for path in paths if path != REVIEW_PATH]
        if committed["staged_before_self"] != expected_paths:
            raise RuntimeError("committed final staged inventory drifted")
        if committed["staged_count_before_self"] != len(expected_paths):
            raise RuntimeError("committed final staged count drifted")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.write == args.verify:
        parser.error("choose exactly one of --write or --verify")
    result = validate(include_review=args.verify)
    if args.write:
        path = ROOT / REVIEW_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(
        json.dumps(
            {
                "valid": result["valid"],
                "staged_count_before_self": result["staged_count_before_self"],
                "strict_json_parses": result["strict_json_parses"],
                "closeout_manifest_entries": result["closeout_manifest_entries"],
                "immutable_evidence_entries": result["immutable_evidence_entries"],
                "privacy_candidates": len(result["confirmed_privacy_candidates"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

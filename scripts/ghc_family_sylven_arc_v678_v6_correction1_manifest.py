#!/usr/bin/env python3
"""Build and replay Sylven Arc v678-v6 correction1 manifests and seal."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


BASE = "ea27f954b8636f167c83b964c0ba5ad15301ea1e"
DELTA = "docs/sylven-arc/v678-v6/validation/correction1-delta-manifest.json"
OWNER = "docs/sylven-arc/v678-v6/validation/correction1-owner-manifest.json"
REVIEW = "docs/sylven-arc/v678-v6/validation/correction1-staged-review.json"
SEAL = "docs/sylven-arc/v678-v6/correction1/correction1-content-seal.json"
DELTA_EXCLUSIONS = [DELTA, OWNER, SEAL]
OWNER_EXCLUSIONS = [OWNER, SEAL]
ALLOWED = (
    "docs/sylven-arc/v678-v6/correction1/",
    "docs/sylven-arc/v678-v6/validation/correction1-",
    "scripts/build_ghc_family_sylven_arc_v678_v6_correction1.py",
    "scripts/ghc_family_sylven_arc_v678_v6_correction1_manifest.py",
    "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py",
    "tests/test_ghc_family_sylven_arc_v678_v6_correction1.py",
)
PRIVACY = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(terminal transcript|session stream|screenshot payload)"),
}


def call(repo: Path, args: list[str]) -> bytes:
    result = subprocess.run(args, cwd=repo, check=False, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stderr.decode("utf-8", errors="replace").strip() or "command failed")
    return result.stdout


def git(repo: Path, *args: str) -> str:
    return call(repo, ["git", *args]).decode("utf-8").strip()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))


def normalized(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def is_owner(path: str) -> bool:
    return (
        path.startswith("docs/sylven-arc/v678-v6/")
        or (path.startswith("scripts/") and "sylven_arc_v678_v6" in path)
        or (path.startswith("tests/") and "sylven_arc_v678_v6" in path)
    )


def current_paths(repo: Path) -> list[str]:
    tracked = call(repo, ["git", "ls-files", "-z"]).decode("utf-8")
    untracked = call(repo, ["git", "ls-files", "--others", "--exclude-standard", "-z"]).decode("utf-8")
    return sorted(set(path.replace("\\", "/") for path in (tracked + untracked).split("\0") if path))


def delta_paths(repo: Path) -> list[str]:
    untracked = call(repo, ["git", "ls-files", "--others", "--exclude-standard", "-z"]).decode("utf-8")
    changed = call(repo, ["git", "diff", "--name-only", "-z", BASE]).decode("utf-8")
    return sorted(set(path.replace("\\", "/") for path in (untracked + changed).split("\0") if path))


def manifest_entries(repo: Path, paths: list[str]) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(paths):
        value = normalized((repo / path).read_bytes())
        rows.append({"path": path, "bytes_normalized_lf": len(value), "sha256_normalized_lf": digest(value)})
    return rows


def privacy_review(repo: Path, paths: list[str]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    candidates = []
    confirmed = []
    definitions = {
        "scripts/ghc_family_sylven_arc_v678_v6_core.py",
        "scripts/ghc_family_sylven_arc_v678_v6_flashcards.py",
        "scripts/ghc_family_sylven_arc_v678_v6_x1_manifest.py",
        "scripts/ghc_family_sylven_arc_v678_v6_evidence_manifest.py",
        "scripts/ghc_family_sylven_arc_v678_v6_final_manifest.py",
        "scripts/ghc_family_sylven_arc_v678_v6_correction1_manifest.py",
        "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py",
        "tests/test_ghc_family_sylven_arc_v678_v6_x1.py",
        "tests/test_ghc_family_sylven_arc_v678_v6_x2.py",
        "tests/test_ghc_family_sylven_arc_v678_v6_final.py",
        "docs/sylven-arc/v678-v6/validation/evidence-staged-review.json",
        "docs/sylven-arc/v678-v6/validation/final-staged-review.json",
        "docs/sylven-arc/v678-v6/validation/final-manifest-preflight-recovery.json",
        REVIEW,
    }
    for path in paths:
        file_path = repo / path
        if not file_path.is_file() or file_path.suffix.lower() not in {".json", ".md", ".html", ".py", ".yaml", ".yml", ".txt"}:
            continue
        value = file_path.read_text(encoding="utf-8")
        for kind, pattern in PRIVACY.items():
            if pattern.search(value):
                item = {"path": path, "class": kind}
                if path in definitions:
                    item["adjudication"] = "scanner_definition_or_adjudication_metadata"
                    candidates.append(item)
                else:
                    item["adjudication"] = "confirmed_or_unresolved_payload"
                    confirmed.append(item)
    return candidates, confirmed


def build(repo: Path) -> dict[str, Any]:
    if git(repo, "rev-parse", "HEAD") != BASE:
        raise SystemExit("correction1 manifests require the immutable first final as HEAD")
    delta = delta_paths(repo)
    rejected = [path for path in delta if not any(path.startswith(prefix) for prefix in ALLOWED)]
    if rejected:
        raise SystemExit("unexpected correction1 paths: " + json.dumps(rejected))
    owner_paths = [path for path in current_paths(repo) if is_owner(path) and (repo / path).is_file()]
    candidates, confirmed = privacy_review(repo, owner_paths)
    if confirmed:
        raise SystemExit("confirmed privacy payload candidates: " + json.dumps(confirmed))
    write_json(repo / REVIEW, {
        "schema": "ghc-family-correction-staged-review/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "base": BASE, "unexpected_paths": [], "deletions": [], "renames": [],
        "privacy_classes": sorted(PRIVACY), "scanner_or_adjudication_candidates": candidates,
        "confirmed_privacy_or_raw_identifier_hits": 0, "canonical_invocation_count": 0,
        "first_final_history_rewritten": False, "correction_scope": "validator self-audit and lifecycle-correct manifests only",
    })
    delta = [path for path in delta_paths(repo) if path not in DELTA_EXCLUSIONS]
    write_json(repo / DELTA, {
        "schema": "ghc-family-normalized-lf-manifest/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "lifecycle": "correction1_delta", "base": BASE, "algorithm": "sha256-normalized-lf",
        "self_exclusions": DELTA_EXCLUSIONS, "entry_count": len(delta), "entries": manifest_entries(repo, delta),
    })
    owner_paths = [path for path in current_paths(repo) if is_owner(path) and (repo / path).is_file() and path not in OWNER_EXCLUSIONS]
    write_json(repo / OWNER, {
        "schema": "ghc-family-normalized-lf-manifest/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "lifecycle": "correction1_owner", "base": BASE, "algorithm": "sha256-normalized-lf",
        "self_exclusions": OWNER_EXCLUSIONS, "entry_count": len(owner_paths), "entries": manifest_entries(repo, owner_paths),
    })
    targets = [
        "docs/sylven-arc/v678-v6/correction1/correction-truth.json",
        "docs/sylven-arc/v678-v6/correction1/method-flow-overlay.json",
        "docs/sylven-arc/v678-v6/correction1/canonical-preflight-state.json",
        "docs/sylven-arc/v678-v6/correction1/receipt-contract-correction.md",
        "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py", DELTA, OWNER,
    ]
    write_json(repo / SEAL, {
        "schema": "ghc-family-content-seal/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "lifecycle": "correction1", "base": BASE, "corrected_final": "BOUND_AT_COMMIT",
        "algorithm": "sha256-exact-bytes",
        "entries": [{"path": path, "bytes": (repo / path).stat().st_size, "sha256": digest((repo / path).read_bytes())} for path in targets],
        "canonical_status": "PENDING_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "route_status": "PREPARED_NOT_SENT",
    })
    return {"status": "BUILT", "delta_entries": len(delta), "owner_entries": len(owner_paths), "seal_entries": len(targets), "privacy_candidates": len(candidates), "confirmed_hits": 0}


def ref_blob(repo: Path, ref: str, path: str) -> bytes:
    return call(repo, ["git", "show", f":{path}" if ref == "INDEX" else f"{ref}:{path}"])


def verify_one(repo: Path, ref: str, manifest_path: str, expected: list[str]) -> dict[str, Any]:
    manifest = json.loads(ref_blob(repo, ref, manifest_path).decode("utf-8"))
    mismatches = []
    if sorted(entry["path"] for entry in manifest["entries"]) != sorted(expected):
        mismatches.append("__path_set__")
    for entry in manifest["entries"]:
        value = normalized(ref_blob(repo, ref, entry["path"]))
        if len(value) != entry["bytes_normalized_lf"] or digest(value) != entry["sha256_normalized_lf"]:
            mismatches.append(entry["path"])
    return {"entries": len(manifest["entries"]), "mismatches": mismatches}


def verify(repo: Path, ref: str) -> dict[str, Any]:
    if ref == "INDEX":
        delta_actual = [path for path in git(repo, "diff", "--cached", "--name-only", BASE).splitlines() if path not in DELTA_EXCLUSIONS]
        all_paths = git(repo, "ls-files").splitlines()
    else:
        delta_actual = [path for path in git(repo, "diff", "--name-only", BASE, ref).splitlines() if path not in DELTA_EXCLUSIONS]
        all_paths = git(repo, "ls-tree", "-r", "--name-only", ref).splitlines()
    owner_actual = [path for path in all_paths if is_owner(path) and path not in OWNER_EXCLUSIONS]
    delta_result = verify_one(repo, ref, DELTA, delta_actual)
    owner_result = verify_one(repo, ref, OWNER, owner_actual)
    seal = json.loads(ref_blob(repo, ref, SEAL).decode("utf-8"))
    seal_mismatches = []
    for entry in seal["entries"]:
        value = ref_blob(repo, ref, entry["path"])
        if len(value) != entry["bytes"] or digest(value) != entry["sha256"]:
            seal_mismatches.append(entry["path"])
    mismatches = delta_result["mismatches"] + owner_result["mismatches"] + seal_mismatches
    result = {"status": "PASS" if not mismatches else "FAIL", "ref": ref, "delta_entries": delta_result["entries"], "owner_entries": owner_result["entries"], "seal_entries": len(seal["entries"]), "mismatches": mismatches}
    if mismatches:
        raise SystemExit(json.dumps(result, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--ref", default="INDEX")
    args = parser.parse_args()
    repo = args.repo.resolve()
    result = build(repo) if args.command == "build" else verify(repo, args.ref)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build and replay the Sylven Arc v678-v6 immutable x2 evidence manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


X1 = "22d310c7ae4fdbd45959d388d15642039d748da0"
MANIFEST = "docs/sylven-arc/v678-v6/validation/evidence-manifest.json"
REVIEW = "docs/sylven-arc/v678-v6/validation/evidence-staged-review.json"
ALLOWED_PREFIXES = (
    "docs/sylven-arc/v678-v6/x2/",
    "docs/sylven-arc/v678-v6/validation/x2-",
    "docs/sylven-arc/v678-v6/validation/flashcard-",
    "docs/sylven-arc/v678-v6/validation/evidence-",
    "scripts/ghc_family_sylven_arc_v678_v6_",
    "scripts/build_ghc_family_sylven_arc_v678_v6_",
    "tests/test_ghc_family_sylven_arc_v678_v6_x2.py",
)
PRIVACY = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(terminal transcript|session stream|screenshot payload)"),
}


def run(repo: Path, args: list[str], *, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(args, cwd=repo, input=input_bytes, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stderr.decode("utf-8", errors="replace").strip() or "command failed")
    return result.stdout


def git(repo: Path, *args: str) -> str:
    return run(repo, ["git", *args]).decode("utf-8").strip()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))


def normalized(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def status_paths(repo: Path) -> list[str]:
    untracked = run(repo, ["git", "ls-files", "--others", "--exclude-standard", "-z"]).decode("utf-8")
    changed = run(repo, ["git", "diff", "--name-only", "-z", X1]).decode("utf-8")
    paths = [path.replace("\\", "/") for path in (untracked + changed).split("\0") if path]
    return sorted(set(paths))


def allowed(path: str) -> bool:
    return path == REVIEW or path == MANIFEST or any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def candidate_paths(repo: Path) -> list[str]:
    paths = [path for path in status_paths(repo) if path not in {MANIFEST}]
    rejected = [path for path in paths if not allowed(path)]
    if rejected:
        raise SystemExit("unexpected owner-delta paths: " + json.dumps(rejected))
    material = [path for path in paths if (repo / path).is_file()]
    if not material:
        raise SystemExit("no x2 evidence paths discovered")
    return sorted(material)


def privacy_review(repo: Path, paths: list[str]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    candidates = []
    confirmed = []
    for path in paths:
        file_path = repo / path
        if file_path.suffix.lower() not in {".json", ".md", ".html", ".py", ".yaml", ".yml"}:
            continue
        value = file_path.read_text(encoding="utf-8")
        for kind, pattern in PRIVACY.items():
            if not pattern.search(value):
                continue
            if path.endswith((
                "ghc_family_sylven_arc_v678_v6_core.py",
                "ghc_family_sylven_arc_v678_v6_flashcards.py",
                "ghc_family_sylven_arc_v678_v6_evidence_manifest.py",
                "test_ghc_family_sylven_arc_v678_v6_x2.py",
            )):
                candidates.append({"path": path, "class": kind, "adjudication": "scanner_definition_or_synthetic_test_metadata"})
            else:
                confirmed.append({"path": path, "class": kind, "adjudication": "unresolved_payload_candidate"})
    return candidates, confirmed


def build(repo: Path) -> dict[str, Any]:
    if git(repo, "rev-parse", "HEAD") != X1:
        raise SystemExit("evidence manifest must be built from exact x1")
    paths = candidate_paths(repo)
    candidates, confirmed = privacy_review(repo, paths)
    if confirmed:
        raise SystemExit("confirmed or unresolved privacy candidates: " + json.dumps(confirmed))
    review = {
        "schema": "ghc-family-sylven-v678-v6-evidence-staged-review/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "base": X1, "allowed_path_count_before_manifest": len(paths), "unexpected_paths": [],
        "privacy_classes": sorted(PRIVACY), "scanner_definition_candidates": candidates,
        "confirmed_privacy_or_raw_identifier_hits": 0, "x1_history_mutated": False,
        "real_world_rows": 0, "external_actions": 0, "full_repository_suite_run": False,
    }
    write_json(repo / REVIEW, review)
    paths = candidate_paths(repo)
    entries = []
    for path in paths:
        value = normalized((repo / path).read_bytes())
        entries.append({"path": path, "bytes_normalized_lf": len(value), "sha256_normalized_lf": sha(value)})
    manifest = {
        "schema": "ghc-family-normalized-lf-manifest/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "lifecycle": "immutable_x2_evidence", "base": X1, "algorithm": "sha256-normalized-lf",
        "self_exclusions": [MANIFEST], "entry_count": len(entries), "entries": entries,
    }
    write_json(repo / MANIFEST, manifest)
    return {"status": "BUILT", "entries": len(entries), "privacy_candidates": len(candidates), "confirmed_hits": 0}


def read_ref(repo: Path, ref: str, path: str) -> bytes:
    if ref == "INDEX":
        return run(repo, ["git", "show", f":{path}"])
    return run(repo, ["git", "show", f"{ref}:{path}"])


def verify(repo: Path, ref: str) -> dict[str, Any]:
    if ref == "WORKTREE":
        manifest = json.loads((repo / MANIFEST).read_text(encoding="utf-8"))
    else:
        manifest = json.loads(read_ref(repo, ref, MANIFEST).decode("utf-8"))
    mismatches = []
    for entry in manifest["entries"]:
        path = entry["path"]
        value = normalized((repo / path).read_bytes()) if ref == "WORKTREE" else normalized(read_ref(repo, ref, path))
        if len(value) != entry["bytes_normalized_lf"] or sha(value) != entry["sha256_normalized_lf"]:
            mismatches.append(path)
    if ref == "INDEX":
        actual = sorted(path for path in git(repo, "diff", "--cached", "--name-only", X1).splitlines() if path != MANIFEST)
        expected = sorted(entry["path"] for entry in manifest["entries"])
        if actual != expected:
            mismatches.append("__index_path_set__")
    result = {"status": "PASS" if not mismatches else "FAIL", "ref": ref, "entries": len(manifest["entries"]), "mismatches": mismatches}
    if mismatches:
        raise SystemExit(json.dumps(result, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--ref", default="WORKTREE")
    args = parser.parse_args()
    repo = args.repo.resolve()
    result = build(repo) if args.command == "build" else verify(repo, args.ref)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()

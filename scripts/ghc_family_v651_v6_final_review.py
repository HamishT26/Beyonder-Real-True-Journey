#!/usr/bin/env python3
"""Review and bind the exact staged Elaren v651-v6 combined final tree."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/elaren-kestrel/v651-v6"
PHASE = REPO / PHASE_ROOT
EVIDENCE = "94b9afc4f8289e8fdf1a304c90c0765e3beb055f"
ALLOWED_EXTERNAL = {
    "scripts/build_ghc_family_v651_v6_closeout.py",
    "scripts/ghc_family_v651_v6_final_review.py",
    "scripts/ghc_family_v651_v6_canonical_validation.py",
    "tests/test_ghc_family_v651_v6_closeout.py",
}
OUTPUTS = {
    f"{PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{PHASE_ROOT}/validation/final-owner-manifest.json",
    f"{PHASE_ROOT}/validation/final-staged-privacy.json",
    f"{PHASE_ROOT}/validation/final-staged-review.json",
}
PATTERNS = {
    "raw_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|file|vscode|app|thread)://", re.I),
    "delegation_markup": re.compile(rb"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential_assignment": re.compile(rb"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
}


def git(*args: str, binary: bool = False, check: bool = True) -> str | bytes:
    proc = subprocess.run(["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout if binary else proc.stdout.decode("utf-8").strip()


def write_json(relative: str, payload: object) -> None:
    path = REPO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def index_oid(path: str) -> str:
    line = str(git("ls-files", "-s", "--", path))
    if not line:
        raise RuntimeError(f"path is not in the Git index: {path}")
    return line.split()[1]


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input="".join(oid + "\n" for oid in unique).encode("ascii"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    stream = io.BytesIO(proc.stdout)
    result: dict[str, bytes] = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode("ascii").split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header: {header}")
        size = int(header[2])
        result[expected] = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing cat-file batch terminator")
    return result


def tree_paths(commit: str, prefix: str) -> set[str]:
    raw = bytes(git("ls-tree", "-r", "-z", commit, "--", prefix, binary=True))
    paths: set[str] = set()
    for record in raw.split(b"\0"):
        if record:
            _meta, path = record.split(b"\t", 1)
            paths.add(path.decode("utf-8"))
    return paths


def manifest(paths: set[str], exclusions: set[str], blobs: dict[str, bytes]) -> dict:
    rows = []
    for path in sorted(paths - exclusions):
        oid = index_oid(path)
        data = blobs[oid]
        rows.append({"path": path, "git_blob": oid, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return {
        "hash_domain": "exact Git index blob identity and SHA-256 of indexed blob bytes",
        "entry_count": len(rows),
        "covered_path_count": len(paths),
        "entries": rows,
        "self_exclusions": sorted(exclusions),
    }


def main() -> None:
    if str(git("rev-parse", "HEAD")) != EVIDENCE:
        raise SystemExit("final review must run from the immutable evidence head before the combined final commit")
    staged = set(filter(None, str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines()))
    final_paths = staged | OUTPUTS
    unexpected = sorted(path for path in final_paths if not path.startswith(PHASE_ROOT + "/") and path not in ALLOWED_EXTERNAL)
    frozen_changes = sorted(path for path in staged if subprocess.run(["git", "cat-file", "-e", f"{EVIDENCE}:{path}"], cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0)
    if not staged:
        raise SystemExit("no staged final candidate")

    owner_paths = tree_paths(EVIDENCE, PHASE_ROOT) | {path for path in final_paths if path.startswith(PHASE_ROOT + "/")}
    oid_paths = (final_paths | owner_paths) - OUTPUTS
    oid_map = {path: index_oid(path) for path in oid_paths}
    blob_map = batch_blobs(list(oid_map.values()))

    delta_payload = {
        "schema": "ghc.family.v651-v6.final-delta-manifest.v1",
        "evidence_commit": EVIDENCE,
        **manifest(final_paths, OUTPUTS, blob_map),
        "boundary": "Exact final delta except four declared lifecycle self-exclusions; committed parity is rechecked once at the exact final head.",
    }
    owner_payload = {
        "schema": "ghc.family.v651-v6.final-owner-manifest.v1",
        **manifest(owner_paths, OUTPUTS, blob_map),
        "boundary": "Complete Elaren v651-v6 owner tree except four declared lifecycle self-exclusions; committed parity is rechecked once at the exact final head.",
    }
    write_json(f"{PHASE_ROOT}/validation/final-delta-manifest.json", delta_payload)
    write_json(f"{PHASE_ROOT}/validation/final-owner-manifest.json", owner_payload)

    privacy_hits = []
    json_issues = []
    json_count = 0
    document_issues = []
    for path in sorted(owner_paths):
        if path in OUTPUTS:
            if not (REPO / path).exists():
                continue
            data = (REPO / path).read_bytes()
        else:
            data = blob_map[oid_map[path]]
        if path.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
                json_count += 1
            except Exception as exc:
                json_issues.append({"path": path, "error": type(exc).__name__})
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                privacy_hits.append({"path": path, "class": name, "offset": match.start()})
        if path.endswith((".md", ".html", ".txt")):
            count = len(re.findall(r"\b[\w'-]+\b", data.decode("utf-8", errors="replace")))
            if count > 100000:
                document_issues.append({"path": path, "words": count})

    privacy_payload = {
        "schema": "ghc.family.v651-v6.final-staged-privacy.v1",
        "files_scanned": len(owner_paths),
        "pattern_classes": sorted(PATTERNS),
        "confirmed_hits": privacy_hits,
        "zero_confirmed_hits": not privacy_hits,
        "boundary": "Five-class content scan; zero regex hits is not complete privacy assurance.",
    }
    write_json(f"{PHASE_ROOT}/validation/final-staged-privacy.json", privacy_payload)
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
    baton = (PHASE / "handoffs/vesper-arlen-v651-v7-activation.md").read_text(encoding="utf-8")
    overview = (PHASE / "overview/final-integrated-overview.md").read_text(encoding="utf-8")
    baton_words = len(re.findall(r"\b[\w'-]+\b", baton))
    overview_words = len(re.findall(r"\b[\w'-]+\b", overview))
    valid = not unexpected and not frozen_changes and not privacy_hits and not json_issues and not document_issues and diff_check.returncode == 0 and 10000 <= baton_words <= 100000 and overview_words >= 3000
    review = {
        "schema": "ghc.family.v651-v6.final-staged-review.v1",
        "valid": valid,
        "predicted_final_delta_paths": len(final_paths),
        "owner_paths": len(owner_paths),
        "delta_manifest_entries": delta_payload["entry_count"],
        "owner_manifest_entries": owner_payload["entry_count"],
        "self_exclusion_count": len(OUTPUTS),
        "unexpected_paths": unexpected,
        "frozen_evidence_changes": frozen_changes,
        "json_parses": json_count,
        "json_issues": json_issues,
        "privacy_zero_confirmed_hits": not privacy_hits,
        "document_issues": document_issues,
        "baton_words": baton_words,
        "overview_words": overview_words,
        "diff_hygiene": "pass" if diff_check.returncode == 0 else diff_check.stdout.strip(),
        "route_state": "PREPARED_NOT_SENT",
        "canonical_successful_passes_before_commit": 0,
        "full_repository_suite_run": False,
        "boundary": "Exact staged same-owner review only; terminal credit requires one post-push scoped canonical pass.",
    }
    write_json(f"{PHASE_ROOT}/validation/final-staged-review.json", review)
    print(json.dumps({"valid": valid, "delta_paths": len(final_paths), "owner_paths": len(owner_paths), "json": json_count, "privacy_hits": len(privacy_hits), "baton_words": baton_words, "overview_words": overview_words}))
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()

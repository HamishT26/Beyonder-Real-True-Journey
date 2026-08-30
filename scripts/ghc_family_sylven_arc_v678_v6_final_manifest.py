#!/usr/bin/env python3
"""Build and replay Sylven Arc v678-v6 final delta and owner manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


EVIDENCE = "7b747952b6a6916c3881066865ff7021aeabea3c"
DELTA = "docs/sylven-arc/v678-v6/validation/final-delta-manifest.json"
OWNER = "docs/sylven-arc/v678-v6/validation/final-owner-manifest.json"
REVIEW = "docs/sylven-arc/v678-v6/validation/final-staged-review.json"
SEAL = "docs/sylven-arc/v678-v6/seal/content-seal.json"
DELTA_EXCLUSIONS = [DELTA, OWNER, SEAL]
OWNER_EXCLUSIONS = [OWNER, SEAL]
ALLOWED_FINAL_PREFIXES = (
    "docs/sylven-arc/v678-v6/closeout/",
    "docs/sylven-arc/v678-v6/handoffs/",
    "docs/sylven-arc/v678-v6/seal/",
    "docs/sylven-arc/v678-v6/validation/closeout-",
    "docs/sylven-arc/v678-v6/validation/final-",
    "scripts/build_ghc_family_sylven_arc_v678_v6_final.py",
    "scripts/ghc_family_sylven_arc_v678_v6_final_manifest.py",
    "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py",
    "tests/test_ghc_family_sylven_arc_v678_v6_final.py",
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


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def changed_paths(repo: Path) -> list[str]:
    untracked = call(repo, ["git", "ls-files", "--others", "--exclude-standard", "-z"]).decode("utf-8")
    changed = call(repo, ["git", "diff", "--name-only", "-z", EVIDENCE]).decode("utf-8")
    return sorted(set(path.replace("\\", "/") for path in (untracked + changed).split("\0") if path))


def allowed_final(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in ALLOWED_FINAL_PREFIXES)


def is_owner(path: str) -> bool:
    return (
        path.startswith("docs/sylven-arc/v678-v6/")
        or (path.startswith("scripts/") and "sylven_arc_v678_v6" in path)
        or (path.startswith("tests/") and "sylven_arc_v678_v6" in path)
    )


def privacy_review(repo: Path, paths: list[str]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    candidates = []
    confirmed = []
    definition_files = {
        "scripts/ghc_family_sylven_arc_v678_v6_core.py",
        "scripts/ghc_family_sylven_arc_v678_v6_flashcards.py",
        "scripts/ghc_family_sylven_arc_v678_v6_evidence_manifest.py",
        "scripts/ghc_family_sylven_arc_v678_v6_final_manifest.py",
        "scripts/ghc_family_sylven_arc_v678_v6_x1_manifest.py",
        "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py",
        "tests/test_ghc_family_sylven_arc_v678_v6_x1.py",
        "tests/test_ghc_family_sylven_arc_v678_v6_x2.py",
        "tests/test_ghc_family_sylven_arc_v678_v6_final.py",
        "docs/sylven-arc/v678-v6/validation/evidence-staged-review.json",
        "docs/sylven-arc/v678-v6/validation/final-manifest-preflight-recovery.json",
        REVIEW,
    }
    for path in paths:
        file_path = repo / path
        if not file_path.is_file() or file_path.suffix.lower() not in {".json", ".md", ".html", ".py", ".yaml", ".yml"}:
            continue
        value = file_path.read_text(encoding="utf-8")
        for kind, pattern in PRIVACY.items():
            if pattern.search(value):
                item = {"path": path, "class": kind}
                if path in definition_files or path.endswith(("final-staged-review.json", "evidence-staged-review.json")):
                    item["adjudication"] = "scanner_definition_or_adjudication_metadata"
                    candidates.append(item)
                else:
                    item["adjudication"] = "unresolved_payload_candidate"
                    confirmed.append(item)
    return candidates, confirmed


def entries(repo: Path, paths: list[str]) -> list[dict[str, Any]]:
    result = []
    for path in sorted(paths):
        value = normalized((repo / path).read_bytes())
        result.append({"path": path, "bytes_normalized_lf": len(value), "sha256_normalized_lf": sha(value)})
    return result


def owner_paths_from_worktree(repo: Path) -> list[str]:
    tracked = call(repo, ["git", "ls-files", "-z"]).decode("utf-8")
    untracked = call(repo, ["git", "ls-files", "--others", "--exclude-standard", "-z"]).decode("utf-8")
    paths = sorted(set(path.replace("\\", "/") for path in (tracked + untracked).split("\0") if path and is_owner(path)))
    return [path for path in paths if (repo / path).is_file()]


def build(repo: Path) -> dict[str, Any]:
    if git(repo, "rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final manifests must be built above exact evidence")
    delta_paths = changed_paths(repo)
    rejected = [path for path in delta_paths if not allowed_final(path)]
    if rejected:
        raise SystemExit("unexpected final-delta paths: " + json.dumps(rejected))
    scan_paths = sorted(set(owner_paths_from_worktree(repo)))
    privacy_candidates, confirmed = privacy_review(repo, scan_paths)
    if confirmed:
        raise SystemExit("confirmed or unresolved privacy payload candidates: " + json.dumps(confirmed))
    review = {
        "schema": "ghc-family-sylven-v678-v6-final-staged-review/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "base": EVIDENCE, "final_delta_paths_before_manifests": len(delta_paths), "unexpected_paths": [],
        "privacy_classes": sorted(PRIVACY), "scanner_or_adjudication_candidates": privacy_candidates,
        "confirmed_privacy_or_raw_identifier_hits": 0, "deletions": [], "renames": [], "merges_planned": 0,
        "real_world_rows": 0, "external_actions": 0, "canonical_invocation_count": 0,
    }
    write_json(repo / REVIEW, review)
    delta_paths = [path for path in changed_paths(repo) if path not in DELTA_EXCLUSIONS]
    delta_manifest = {
        "schema": "ghc-family-normalized-lf-manifest/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "lifecycle": "final_delta", "base": EVIDENCE, "algorithm": "sha256-normalized-lf",
        "self_exclusions": DELTA_EXCLUSIONS, "entry_count": len(delta_paths), "entries": entries(repo, delta_paths),
    }
    write_json(repo / DELTA, delta_manifest)
    owner_paths = [path for path in owner_paths_from_worktree(repo) if path not in OWNER_EXCLUSIONS]
    owner_manifest = {
        "schema": "ghc-family-normalized-lf-manifest/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "lifecycle": "final_owner", "base": EVIDENCE, "algorithm": "sha256-normalized-lf",
        "self_exclusions": OWNER_EXCLUSIONS, "entry_count": len(owner_paths), "entries": entries(repo, owner_paths),
    }
    write_json(repo / OWNER, owner_manifest)
    seal_targets = [
        "docs/sylven-arc/v678-v6/closeout/phase-truth.json",
        "docs/sylven-arc/v678-v6/closeout/method-flow-final.json",
        "docs/sylven-arc/v678-v6/closeout/retained-negative-register.json",
        "docs/sylven-arc/v678-v6/closeout/open-exact-gate-register.json",
        "docs/sylven-arc/v678-v6/closeout/final-integrated-overview.md",
        "docs/sylven-arc/v678-v6/closeout/route-receipt.json",
        "docs/sylven-arc/v678-v6/handoffs/caelen-morrow-v678-v7-activation-candidate.md",
        DELTA, OWNER,
    ]
    seal = {
        "schema": "ghc-family-content-seal/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "source": "d7a2e3d1851d8a9eb6a8707968a47354b44e824a", "x1": "22d310c7ae4fdbd45959d388d15642039d748da0",
        "evidence": EVIDENCE, "exact_final": "BOUND_AT_COMMIT", "algorithm": "sha256-exact-bytes",
        "entries": [{"path": path, "bytes": (repo / path).stat().st_size, "sha256": sha((repo / path).read_bytes())} for path in seal_targets],
        "canonical_status": "PENDING_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "route_status": "PREPARED_NOT_SENT",
    }
    write_json(repo / SEAL, seal)
    return {
        "status": "BUILT", "delta_entries": len(delta_paths), "owner_entries": len(owner_paths),
        "seal_entries": len(seal_targets), "privacy_candidates": len(privacy_candidates), "confirmed_hits": 0,
    }


def read_ref(repo: Path, ref: str, path: str) -> bytes:
    return call(repo, ["git", "show", f":{path}" if ref == "INDEX" else f"{ref}:{path}"])


def path_set(repo: Path, ref: str, owner: bool) -> list[str]:
    if ref == "INDEX":
        paths = call(repo, ["git", "ls-files", "-z"]).decode("utf-8").split("\0")
    else:
        paths = git(repo, "ls-tree", "-r", "--name-only", ref).splitlines()
    paths = [path.replace("\\", "/") for path in paths if path]
    if owner:
        return sorted(path for path in paths if is_owner(path) and path not in OWNER_EXCLUSIONS)
    return sorted(path for path in paths if path not in DELTA_EXCLUSIONS and path in set(git(repo, "diff", "--name-only", EVIDENCE, ref if ref != "INDEX" else "--cached").splitlines()))


def verify_manifest(repo: Path, ref: str, manifest_path: str, expected_paths: list[str]) -> dict[str, Any]:
    manifest = json.loads(read_ref(repo, ref, manifest_path).decode("utf-8"))
    mismatches = []
    actual_manifest_paths = sorted(entry["path"] for entry in manifest["entries"])
    if actual_manifest_paths != sorted(expected_paths):
        mismatches.append("__path_set__")
    for entry in manifest["entries"]:
        value = normalized(read_ref(repo, ref, entry["path"]))
        if len(value) != entry["bytes_normalized_lf"] or sha(value) != entry["sha256_normalized_lf"]:
            mismatches.append(entry["path"])
    return {"manifest": manifest_path, "entries": len(manifest["entries"]), "mismatches": mismatches}


def verify(repo: Path, ref: str) -> dict[str, Any]:
    if ref == "INDEX":
        delta_actual = sorted(path for path in git(repo, "diff", "--cached", "--name-only", EVIDENCE).splitlines() if path not in DELTA_EXCLUSIONS)
        owner_actual = path_set(repo, ref, True)
    else:
        delta_actual = sorted(path for path in git(repo, "diff", "--name-only", EVIDENCE, ref).splitlines() if path not in DELTA_EXCLUSIONS)
        owner_actual = path_set(repo, ref, True)
    delta_result = verify_manifest(repo, ref, DELTA, delta_actual)
    owner_result = verify_manifest(repo, ref, OWNER, owner_actual)
    seal = json.loads(read_ref(repo, ref, SEAL).decode("utf-8"))
    seal_mismatches = []
    for entry in seal["entries"]:
        value = read_ref(repo, ref, entry["path"])
        if len(value) != entry["bytes"] or sha(value) != entry["sha256"]:
            seal_mismatches.append(entry["path"])
    mismatches = delta_result["mismatches"] + owner_result["mismatches"] + seal_mismatches
    result = {
        "status": "PASS" if not mismatches else "FAIL", "ref": ref,
        "delta_entries": delta_result["entries"], "owner_entries": owner_result["entries"],
        "seal_entries": len(seal["entries"]), "mismatches": mismatches,
    }
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

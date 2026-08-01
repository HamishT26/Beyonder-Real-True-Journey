#!/usr/bin/env python3
"""Build and review Liora Venn v657-v7 evidence lifecycle receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v657_v7_phase_data as d
import ghc_family_v657_v7_x2_config as c


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
PHASE_PREFIX = f"{d.PHASE_ROOT}/"
MANIFEST_RELATIVE = f"{d.PHASE_ROOT}/validation/evidence-content-manifest.json"
PRIVACY_RELATIVE = f"{d.PHASE_ROOT}/validation/evidence-privacy-scan.json"
REVIEW_RELATIVE = f"{d.PHASE_ROOT}/validation/evidence-staged-review.json"
DECLARED_MANIFEST_EXCLUSIONS = {
    "validation/evidence-content-manifest.json": "self_hash_impossible_inside_same_blob",
    "validation/evidence-privacy-scan.json": "regenerated_after_manifest_for_final_staged_privacy_state",
    "validation/evidence-staged-review.json": "generated_after_candidate_is_staged",
    "validation/evidence-validation.json": "regenerated_after_manifest_for_final_validation_counts",
    "validation/evidence-minimal-validation.json": "regenerated_after_manifest_for_final_validation counts",
}
PRIVACY_PATTERNS = {
    "raw_uuid": re.compile(
        r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"
    ),
    "private_absolute_path": re.compile(
        r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/][^\s\"']+"
    ),
    "credential_or_secret": re.compile(
        r"(?i)\b(?:sk-[a-z0-9_-]{20,}|bearer\s+[a-z0-9._-]{20,}|password\s*[:=]\s*[^\s\"']{8,})"
    ),
    "private_route_value": re.compile(
        r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"
    ),
    "private_callable_value": re.compile(
        r"(?i)\bprivate_callable_(?:id|identifier)\s*[:=]\s*[a-z0-9_-]{8,}"
    ),
}


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def repository_relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def wrapper_paths() -> set[str]:
    return {f"scripts/{filename}" for filename, _ in d.RUNNER_SPECS}


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path
        for path in (ROOT / "scripts").glob("*v657_v7*.py")
        if path.is_file()
    )
    paths.extend(ROOT / path for path in wrapper_paths())
    for relative in [
        "tests/test_ghc_family_v657_v7_x1.py",
        "tests/test_ghc_family_v657_v7.py",
    ]:
        path = ROOT / relative
        if path.is_file():
            paths.append(path)
    return sorted({path.resolve() for path in paths})


def phase_relative(path: Path) -> str | None:
    try:
        return path.relative_to(PHASE).as_posix()
    except ValueError:
        return None


def clean_blob(path: Path) -> tuple[str, int]:
    relative = repository_relative(path)
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    size = int(git("cat-file", "-s", oid))
    return oid, size


def scan_text(path: str, text: str) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for label, pattern in PRIVACY_PATTERNS.items():
        count = len(pattern.findall(text))
        if count:
            hits.append({"path": path, "pattern_class": label, "count": count})
    return hits


def current_privacy_scan() -> dict[str, Any]:
    paths = [
        path
        for path in owner_paths()
        if repository_relative(path) != PRIVACY_RELATIVE
    ]
    hits: list[dict[str, Any]] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        hits.extend(scan_text(repository_relative(path), text))
    return {
        "schema": "ghc.family.v657-v7.evidence-privacy-scan.v1",
        "file_count": len(paths),
        "pattern_class_count": len(PRIVACY_PATTERNS),
        "pattern_classes": sorted(PRIVACY_PATTERNS),
        "confirmed_hits": hits,
        "hit_count": sum(row["count"] for row in hits),
        "self_exclusion": PRIVACY_RELATIVE,
        "valid": not hits,
        "boundary": "Five-class bounded text scan only; not exhaustive security or privacy-complete assurance.",
    }


def build_manifest() -> dict[str, Any]:
    entries = []
    expected_paths = []
    for path in owner_paths():
        relative = repository_relative(path)
        local = phase_relative(path)
        if local in DECLARED_MANIFEST_EXCLUSIONS:
            continue
        oid, size = clean_blob(path)
        entries.append(
            {
                "path": relative,
                "git_blob": oid,
                "git_clean_bytes": size,
            }
        )
        expected_paths.append(relative)
    return {
        "schema": "ghc.family.v657-v7.evidence-content-manifest.v1",
        "hash_domain": "Git filtered prospective blob identity",
        "entry_count": len(entries),
        "entries": entries,
        "declared_exclusions": [
            {
                "path": f"{PHASE_PREFIX}{relative}",
                "reason": reason,
            }
            for relative, reason in sorted(DECLARED_MANIFEST_EXCLUSIONS.items())
        ],
        "declared_exclusion_count": len(DECLARED_MANIFEST_EXCLUSIONS),
        "exact_path_set_sha256": hashlib.sha256(
            ("\n".join(expected_paths) + "\n").encode("utf-8")
        ).hexdigest(),
        "x1_commit": c.X1_COMMIT,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Exact Git-clean candidate content with declared lifecycle self-exclusions.",
    }


def build_receipts() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != c.X1_COMMIT:
        raise RuntimeError("evidence receipts require the exact frozen x1 head")
    privacy = current_privacy_scan()
    if not privacy["valid"]:
        raise RuntimeError(f"privacy candidate hits: {privacy['confirmed_hits']}")
    write_json("validation/evidence-privacy-scan.json", privacy)

    documents = [
        path
        for path in PHASE.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}
    ]
    document_rows = [
        {
            "path": path.relative_to(PHASE).as_posix(),
            "words": len(path.read_text(encoding="utf-8").split()),
        }
        for path in sorted(documents)
    ]
    write_json(
        "validation/evidence-document-cap.json",
        {
            "schema": "ghc.family.v657-v7.evidence-document-cap.v1",
            "document_count": len(document_rows),
            "maximum_words": max(row["words"] for row in document_rows),
            "limit": 100000,
            "all_within_limit": all(
                row["words"] <= 100000 for row in document_rows
            ),
            "documents": document_rows,
        },
    )
    owner_count = len(owner_paths())
    write_json(
        "validation/evidence-owner-file-cap.json",
        {
            "schema": "ghc.family.v657-v7.evidence-owner-file-cap.v1",
            "owner_file_count": owner_count,
            "limit": 2000,
            "within_limit": owner_count < 2000,
            "inherited_repository_baseline_counted": False,
        },
    )
    manifest = build_manifest()
    write_json("validation/evidence-content-manifest.json", manifest)
    return {
        "manifest_entries": manifest["entry_count"],
        "privacy_files": privacy["file_count"],
        "owner_files": owner_count,
        "maximum_words": max(row["words"] for row in document_rows),
    }


def frozen_x1_paths() -> set[str]:
    return {
        row
        for row in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            c.X1_COMMIT,
        ).splitlines()
        if row
    }


def index_blob(relative: str) -> str:
    return git("rev-parse", f":{relative}")


def staged_text(relative: str) -> str:
    data = subprocess.run(
        ["git", "show", f":{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return data.decode("utf-8")


def allowed_path(relative: str) -> bool:
    return (
        relative.startswith(PHASE_PREFIX)
        or (
            relative.startswith("scripts/")
            and "v657_v7" in Path(relative).name
            and relative.endswith(".py")
        )
        or relative in wrapper_paths()
        or relative == "tests/test_ghc_family_v657_v7.py"
    )


def review_staged() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != c.X1_COMMIT:
        raise RuntimeError("evidence staged review requires the exact frozen x1 head")
    staged_paths = sorted(
        row
        for row in git(
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMR",
            c.X1_COMMIT,
        ).splitlines()
        if row
    )
    reviewed_paths = [path for path in staged_paths if path != REVIEW_RELATIVE]
    deleted_paths = [
        row
        for row in git(
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=D",
            c.X1_COMMIT,
        ).splitlines()
        if row
    ]
    out_of_scope = [path for path in staged_paths if not allowed_path(path)]
    frozen_changes = sorted(set(staged_paths) & frozen_x1_paths())
    unstaged = [
        row for row in git("diff", "--name-only").splitlines() if row
    ]
    untracked = [
        row
        for row in git("ls-files", "--others", "--exclude-standard").splitlines()
        if row and row != REVIEW_RELATIVE
    ]
    diff_check = run("git", "diff", "--cached", "--check", check=False)

    staged_privacy_hits: list[dict[str, Any]] = []
    for relative in reviewed_paths:
        staged_privacy_hits.extend(scan_text(relative, staged_text(relative)))

    manifest = json.loads(
        (PHASE / "validation/evidence-content-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    manifest_mismatches = []
    for entry in manifest["entries"]:
        observed = index_blob(entry["path"])
        if observed != entry["git_blob"]:
            manifest_mismatches.append(
                {
                    "path": entry["path"],
                    "expected": entry["git_blob"],
                    "observed": observed,
                }
            )
    exclusions = {row["path"] for row in manifest["declared_exclusions"]}
    expected_manifest_paths = {
        repository_relative(path)
        for path in owner_paths()
        if repository_relative(path) not in exclusions
    }
    actual_manifest_paths = {row["path"] for row in manifest["entries"]}
    manifest_path_issues = sorted(
        expected_manifest_paths.symmetric_difference(actual_manifest_paths)
    )

    name_hash = hashlib.sha256(
        ("\n".join(reviewed_paths) + "\n").encode("utf-8")
    ).hexdigest()
    valid = not any(
        [
            deleted_paths,
            out_of_scope,
            frozen_changes,
            unstaged,
            untracked,
            diff_check.returncode,
            staged_privacy_hits,
            manifest_mismatches,
            manifest_path_issues,
        ]
    )
    payload = {
        "schema": "ghc.family.v657-v7.evidence-staged-review.v1",
        "valid": valid,
        "x1_commit": c.X1_COMMIT,
        "staged_path_count": len(staged_paths),
        "reviewed_path_count": len(reviewed_paths),
        "reviewed_name_list_sha256": name_hash,
        "self_exclusion": REVIEW_RELATIVE,
        "deleted_paths": deleted_paths,
        "out_of_scope_paths": out_of_scope,
        "x1_frozen_changes": frozen_changes,
        "unstaged_paths": unstaged,
        "untracked_paths_other_than_self": untracked,
        "diff_check_returncode": diff_check.returncode,
        "staged_privacy_pattern_class_count": len(PRIVACY_PATTERNS),
        "staged_privacy_hits": staged_privacy_hits,
        "manifest_entry_count": manifest["entry_count"],
        "manifest_mismatches": manifest_mismatches,
        "manifest_path_issues": manifest_path_issues,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Exact staged candidate review with the review blob declared as its sole self-exclusion.",
    }
    write_json("validation/evidence-staged-review.json", payload)
    if not valid:
        raise RuntimeError(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "review"])
    args = parser.parse_args()
    payload = build_receipts() if args.mode == "build" else review_staged()
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()

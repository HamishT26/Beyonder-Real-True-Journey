#!/usr/bin/env python3
"""Build and review Neris v656-v7 final candidate receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import build_ghc_family_v656_v7_evidence_receipts as e
import ghc_family_v656_v7_final_config as c
import ghc_family_v656_v7_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
PHASE_PREFIX = f"{d.PHASE_ROOT}/"
MANIFEST_RELATIVE = f"{d.PHASE_ROOT}/validation/final-owner-manifest.json"
PRIVACY_RELATIVE = f"{d.PHASE_ROOT}/validation/final-privacy-precommit.json"
REVIEW_RELATIVE = f"{d.PHASE_ROOT}/validation/final-staged-review.json"
EXCLUSIONS = {
    MANIFEST_RELATIVE: "self_hash_impossible_inside_same_blob",
    PRIVACY_RELATIVE: "regenerated_after_manifest_for_final_candidate_privacy_state",
    REVIEW_RELATIVE: "generated_after_final_candidate_is_staged",
}


def git(*args: str) -> str:
    return e.git(*args)


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


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path
        for path in (ROOT / "scripts").glob("*v656_v7*.py")
        if path.is_file()
    )
    paths.extend(ROOT / relative for relative in e.wrapper_paths())
    paths.extend(
        path
        for path in (ROOT / "tests").glob("test_ghc_family_v656_v7*.py")
        if path.is_file()
    )
    return sorted({path.resolve() for path in paths})


def clean_blob(path: Path) -> tuple[str, int]:
    relative = repository_relative(path)
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    return oid, int(git("cat-file", "-s", oid))


def privacy_scan() -> dict[str, Any]:
    paths = [
        path
        for path in owner_paths()
        if repository_relative(path) != PRIVACY_RELATIVE
    ]
    hits = []
    for path in paths:
        hits.extend(
            e.scan_text(
                repository_relative(path), path.read_text(encoding="utf-8")
            )
        )
    return {
        "schema": "ghc.family.v656-v7.final-privacy-precommit.v1",
        "file_count": len(paths),
        "pattern_class_count": len(e.PRIVACY_PATTERNS),
        "pattern_classes": sorted(e.PRIVACY_PATTERNS),
        "confirmed_hits": hits,
        "hit_count": sum(row["count"] for row in hits),
        "self_exclusion": PRIVACY_RELATIVE,
        "valid": not hits,
        "boundary": "Five-class bounded precommit scan only; not exhaustive security or privacy-complete assurance.",
    }


def manifest() -> dict[str, Any]:
    entries = []
    for path in owner_paths():
        relative = repository_relative(path)
        if relative in EXCLUSIONS:
            continue
        oid, size = clean_blob(path)
        entries.append(
            {
                "path": relative,
                "git_blob": oid,
                "git_clean_bytes": size,
            }
        )
    paths = [entry["path"] for entry in entries]
    return {
        "schema": "ghc.family.v656-v7.final-owner-manifest.v1",
        "hash_domain": "Git filtered prospective blob identity",
        "entry_count": len(entries),
        "entries": entries,
        "declared_exclusions": [
            {"path": path, "reason": reason}
            for path, reason in sorted(EXCLUSIONS.items())
        ],
        "declared_exclusion_count": len(EXCLUSIONS),
        "exact_path_set_sha256": hashlib.sha256(
            ("\n".join(paths) + "\n").encode("utf-8")
        ).hexdigest(),
        "closeout_commit": c.CLOSEOUT_COMMIT,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Exact Git-clean final owner tree with declared lifecycle self-exclusions.",
    }


def build() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != c.CLOSEOUT_COMMIT:
        raise RuntimeError("final receipts require the exact closeout head")
    privacy = privacy_scan()
    if not privacy["valid"]:
        raise RuntimeError(f"final privacy hits: {privacy['confirmed_hits']}")
    write_json("validation/final-privacy-precommit.json", privacy)
    documents = [
        path
        for path in PHASE.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}
    ]
    rows = [
        {
            "path": path.relative_to(PHASE).as_posix(),
            "words": len(path.read_text(encoding="utf-8").split()),
        }
        for path in sorted(documents)
    ]
    write_json(
        "validation/final-document-cap.json",
        {
            "schema": "ghc.family.v656-v7.final-document-cap.v1",
            "document_count": len(rows),
            "maximum_words": max(row["words"] for row in rows),
            "limit": 100000,
            "all_within_limit": all(row["words"] <= 100000 for row in rows),
            "documents": rows,
        },
    )
    count = len(owner_paths())
    write_json(
        "validation/final-owner-file-cap.json",
        {
            "schema": "ghc.family.v656-v7.final-owner-file-cap.v1",
            "owner_file_count": count,
            "limit": 2000,
            "within_limit": count < 2000,
            "inherited_repository_baseline_counted": False,
        },
    )
    payload = manifest()
    write_json("validation/final-owner-manifest.json", payload)
    return {
        "manifest_entries": payload["entry_count"],
        "privacy_files": privacy["file_count"],
        "owner_files": count,
        "maximum_words": max(row["words"] for row in rows),
    }


def prior_phase_paths() -> set[str]:
    return {
        row
        for row in git(
            "diff",
            "--name-only",
            c.SOURCE_COMMIT,
            c.CLOSEOUT_COMMIT,
        ).splitlines()
        if row
    }


def allowed(relative: str) -> bool:
    return (
        relative.startswith(PHASE_PREFIX)
        or (
            relative.startswith("scripts/")
            and "v656_v7" in Path(relative).name
            and relative.endswith(".py")
        )
        or relative in e.wrapper_paths()
        or (
            relative.startswith("tests/test_ghc_family_v656_v7")
            and relative.endswith(".py")
        )
    )


def review() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != c.CLOSEOUT_COMMIT:
        raise RuntimeError("final review requires the exact closeout head")
    staged = sorted(
        row
        for row in git(
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMR",
            c.CLOSEOUT_COMMIT,
        ).splitlines()
        if row
    )
    reviewed = [path for path in staged if path != REVIEW_RELATIVE]
    deleted = [
        row
        for row in git(
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=D",
            c.CLOSEOUT_COMMIT,
        ).splitlines()
        if row
    ]
    out_of_scope = [path for path in staged if not allowed(path)]
    frozen_changes = sorted(set(staged) & prior_phase_paths())
    unstaged = [row for row in git("diff", "--name-only").splitlines() if row]
    untracked = [
        row
        for row in git("ls-files", "--others", "--exclude-standard").splitlines()
        if row and row != REVIEW_RELATIVE
    ]
    diff_check = e.run("git", "diff", "--cached", "--check", check=False)
    privacy_hits = []
    for relative in reviewed:
        privacy_hits.extend(e.scan_text(relative, e.staged_text(relative)))
    content = json.loads(
        (PHASE / "validation/final-owner-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    mismatches = []
    for entry in content["entries"]:
        observed = git("rev-parse", f":{entry['path']}")
        if observed != entry["git_blob"]:
            mismatches.append(
                {
                    "path": entry["path"],
                    "expected": entry["git_blob"],
                    "observed": observed,
                }
            )
    excluded = {row["path"] for row in content["declared_exclusions"]}
    expected_paths = {
        repository_relative(path)
        for path in owner_paths()
        if repository_relative(path) not in excluded
    }
    actual_paths = {row["path"] for row in content["entries"]}
    path_issues = sorted(expected_paths.symmetric_difference(actual_paths))
    name_hash = hashlib.sha256(
        ("\n".join(reviewed) + "\n").encode("utf-8")
    ).hexdigest()
    valid = not any(
        [
            deleted,
            out_of_scope,
            frozen_changes,
            unstaged,
            untracked,
            diff_check.returncode,
            privacy_hits,
            mismatches,
            path_issues,
        ]
    )
    payload = {
        "schema": "ghc.family.v656-v7.final-staged-review.v1",
        "valid": valid,
        "closeout_commit": c.CLOSEOUT_COMMIT,
        "staged_path_count": len(staged),
        "reviewed_path_count": len(reviewed),
        "reviewed_name_list_sha256": name_hash,
        "self_exclusion": REVIEW_RELATIVE,
        "deleted_paths": deleted,
        "out_of_scope_paths": out_of_scope,
        "prior_phase_frozen_changes": frozen_changes,
        "unstaged_paths": unstaged,
        "untracked_paths_other_than_self": untracked,
        "diff_check_returncode": diff_check.returncode,
        "staged_privacy_hits": privacy_hits,
        "staged_privacy_pattern_class_count": len(e.PRIVACY_PATTERNS),
        "manifest_entry_count": content["entry_count"],
        "manifest_mismatches": mismatches,
        "manifest_path_issues": path_issues,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Exact final delta review with the review blob declared as its sole self-exclusion.",
    }
    write_json("validation/final-staged-review.json", payload)
    if not valid:
        raise RuntimeError(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "review"])
    args = parser.parse_args()
    payload = build() if args.mode == "build" else review()
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()

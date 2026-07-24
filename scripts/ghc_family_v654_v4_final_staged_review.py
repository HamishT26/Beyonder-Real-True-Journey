#!/usr/bin/env python3
"""Review the exact staged Caelen v654-v4 content seal and build manifests."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/caelen-morrow/v654-v4"
X1 = "4af17107d0042eb6b41ef17a9b32aebd6eabdc2a"
EVIDENCE = "47746b3b52c02e97ee5c4e66632f7584a2834fca"
ROUTE_STATE = "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
SELF_EXCLUSIONS = {
    "docs/caelen-morrow/v654-v4/validation/final-delta-manifest.json",
    "docs/caelen-morrow/v654-v4/validation/final-owner-manifest.json",
    "docs/caelen-morrow/v654-v4/validation/final-staged-privacy.json",
    "docs/caelen-morrow/v654-v4/validation/final-staged-review.json",
    "docs/caelen-morrow/v654-v4/validation/final-diff-hygiene.json",
}
RUNNER_PATHS = {
    "scripts/ghc_family_accessible_garment_audit.py",
    "scripts/ghc_family_freed_id_garment_profiles.py",
    "scripts/ghc_family_garment_compatibility_refusal.py",
    "scripts/ghc_family_garment_hazard_boards.py",
    "scripts/ghc_family_garment_intake_ledger.py",
    "scripts/ghc_family_garment_notice_quarantine.py",
    "scripts/ghc_family_gmut_textile_fields.py",
    "scripts/ghc_family_thos_garment_proxy.py",
}
PHASE_SCRIPT_PATHS = {
    "scripts/ghc_family_v654_v4_phase_data.py",
    "scripts/ghc_family_v654_v4_x2_data.py",
    "scripts/ghc_family_v654_v4_core.py",
    "scripts/build_ghc_family_v654_v4_method_flow.py",
    "scripts/build_ghc_family_v654_v4_preregistration.py",
    "scripts/ghc_family_v654_v4_x1_validate.py",
    "scripts/build_ghc_family_v654_v4_x2_method_flow.py",
    "scripts/build_ghc_family_v654_v4_evidence.py",
    "scripts/ghc_family_v654_v4_evidence_validate.py",
    "scripts/ghc_family_v654_v4_detailed_validator.py",
    "scripts/ghc_family_v654_v4_bounded_suite.py",
    "scripts/build_ghc_family_v654_v4_closeout.py",
    "scripts/ghc_family_v654_v4_final_staged_review.py",
    "scripts/ghc_family_v654_v4_final_validate.py",
}
PHASE_TEST_PATHS = {
    "tests/test_ghc_family_v654_v4_x1.py",
    "tests/test_ghc_family_v654_v4.py",
    "tests/test_ghc_family_v654_v4_closeout.py",
}
ALLOWED_NON_DOC_PATHS = RUNNER_PATHS | PHASE_SCRIPT_PATHS | PHASE_TEST_PATHS


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=check,
    )
    return result.stdout.strip()


def write(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def index_oid(relative: str) -> str:
    return git("rev-parse", f":{relative}")


def index_blob(relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "cat-file", "blob", index_oid(relative)], cwd=REPO
    )


def hash_index_entry(relative: str) -> dict[str, Any]:
    blob = index_blob(relative)
    return {
        "path": relative,
        "git_blob": index_oid(relative),
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }


def staged_paths() -> list[str]:
    return sorted(
        path.replace("\\", "/")
        for path in git(
            "diff", "--cached", "--name-only", "--diff-filter=ACMR"
        ).splitlines()
        if path
    )


def all_index_paths() -> list[str]:
    rows = git("ls-files", "--stage").splitlines()
    paths = []
    for row in rows:
        if "\t" not in row:
            continue
        meta, path = row.split("\t", 1)
        if meta.split()[-1] == "0":
            paths.append(path.replace("\\", "/"))
    return sorted(set(paths))


def owner_path(relative: str) -> bool:
    return (
        relative.startswith("docs/caelen-morrow/v654-v4/")
        or relative in ALLOWED_NON_DOC_PATHS
    )


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)[A-Z]:\\Users\\[^\s\"']+"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(?:(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*"
            r"[\"']?[A-Za-z0-9._-]{8,}|bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|"
            r"browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    candidates: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    scanned = 0
    for relative in paths:
        try:
            content = index_blob(relative).decode("utf-8")
        except (UnicodeDecodeError, subprocess.CalledProcessError):
            continue
        scanned += 1
        is_definition = (
            relative.endswith("_validate.py")
            or relative.endswith("_staged_review.py")
            or relative.endswith("-privacy.json")
            or relative == "scripts/build_ghc_family_v654_v4_preregistration.py"
        )
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = (
                    "scanner_definition" if is_definition else "confirmed_payload_hit"
                )
                row = {
                    "path": relative,
                    "pattern_class": pattern_class,
                    "disposition": disposition,
                }
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v654-v4.final-staged-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with scanner-definition quarantine; zero "
            "confirmed hits is not complete privacy assurance."
        ),
    }


def replay_manifest(anchor: str, relative: str) -> tuple[int, list[dict[str, Any]]]:
    manifest = json.loads(git("show", f"{anchor}:{relative}"))
    mismatches = []
    for row in manifest["entries"]:
        observed = git("rev-parse", f"{anchor}:{row['path']}", check=False)
        if observed != row["git_blob"]:
            mismatches.append(
                {
                    "path": row["path"],
                    "expected": row["git_blob"],
                    "observed": observed or None,
                }
            )
    return len(manifest["entries"]), mismatches


def main() -> None:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    staged = staged_paths()
    check("staged_nonempty", bool(staged), len(staged))
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/caelen-morrow/v654-v4/")
        and path not in ALLOWED_NON_DOC_PATHS
    ]
    check("staged_scope", not out_of_scope, out_of_scope)
    check(
        "no_sibling_docs",
        not any(path.startswith("docs/") and not path.startswith(
            "docs/caelen-morrow/v654-v4/"
        ) for path in staged),
        [path for path in staged if path.startswith("docs/") and not path.startswith(
            "docs/caelen-morrow/v654-v4/"
        )],
    )
    check(
        "x1_paths_immutable",
        not any(
            path.startswith(
                (
                    "docs/caelen-morrow/v654-v4/preregistration/",
                    "docs/caelen-morrow/v654-v4/approval/",
                    "docs/caelen-morrow/v654-v4/sources/",
                )
            )
            for path in staged
        ),
        "no frozen x1 document path changed",
    )
    check(
        "evidence_paths_immutable",
        not any(
            path.startswith(
                (
                    "docs/caelen-morrow/v654-v4/evidence/",
                    "docs/caelen-morrow/v654-v4/surfaces/",
                    "docs/caelen-morrow/v654-v4/skills/",
                    "docs/caelen-morrow/v654-v4/tools/",
                )
            )
            for path in staged
        ),
        "no committed evidence artifact changed",
    )

    whitespace = subprocess.run(
        ["git", "diff", "--cached", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    check("diff_whitespace", whitespace.returncode == 0, whitespace.stdout + whitespace.stderr)

    x1_count, x1_mismatch = replay_manifest(
        X1,
        "docs/caelen-morrow/v654-v4/validation/x1-staged-manifest.json",
    )
    evidence_count, evidence_mismatch = replay_manifest(
        EVIDENCE,
        "docs/caelen-morrow/v654-v4/validation/evidence-manifest.json",
    )
    check(
        "immutable_x1_manifest",
        not x1_mismatch and x1_count == 92,
        {"entries": x1_count, "mismatches": x1_mismatch},
    )
    check(
        "immutable_evidence_manifest",
        not evidence_mismatch and evidence_count == 179,
        {"entries": evidence_count, "mismatches": evidence_mismatch},
    )

    delta_paths = [
        path
        for path in staged
        if path not in SELF_EXCLUSIONS and "__pycache__" not in path
    ]
    delta_entries = [hash_index_entry(path) for path in delta_paths]
    owner_paths = [
        path
        for path in all_index_paths()
        if owner_path(path)
        and path not in SELF_EXCLUSIONS
        and "__pycache__" not in path
    ]
    owner_entries = [hash_index_entry(path) for path in owner_paths]
    privacy = privacy_scan(owner_paths)
    check("privacy", privacy["confirmed_hit_count"] == 0, privacy["confirmed_hits"])
    check("owner_file_cap", len(owner_paths) + len(SELF_EXCLUSIONS) <= 2000, len(owner_paths))

    route = json.loads(
        index_blob(
            "docs/caelen-morrow/v654-v4/route/terminal-existing-task-baton.json"
        ).decode("utf-8")
    )
    check(
        "route_prepared_not_sent",
        route["state"] == ROUTE_STATE
        and route["recipient_title"] == "Eiren Kestrel"
        and route["existing_task_only"]
        and route["task_created_count"] == 0
        and route["task_contacted_count"] == 0
        and route["message_limit"] == 1,
        route,
    )

    baton = index_blob(
        "docs/caelen-morrow/v654-v4/handoffs/eiren-kestrel-v654-v5-activation.md"
    ).decode("utf-8")
    baton_words = len(baton.split())
    check("baton_word_cap", 10000 <= baton_words <= 100000, baton_words)
    check(
        "baton_sanitized_route",
        "Eiren Kestrel" in baton
        and "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED" in baton
        and "new user-visible main task" not in baton.casefold()
        and "source_thread_id" not in baton.casefold(),
        "exact existing-title prepared baton",
    )

    write(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.v654-v4.final-delta-manifest.v1",
            "hash_domain": "exact_staged_git_index_blob",
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "self_exclusions": sorted(SELF_EXCLUSIONS),
            "coverage_boundary": (
                "Every staged final content-seal path except five declared "
                "self-referential manifest, privacy, and review receipts."
            ),
        },
    )
    write(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v654-v4.final-owner-manifest.v1",
            "hash_domain": "exact_staged_git_index_blob",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusions": sorted(SELF_EXCLUSIONS),
            "owner_interpretation": (
                "All Caelen v654-v4 docs plus phase-local v654-v4 scripts, "
                "family-current garment/textile runners, and v654-v4 tests."
            ),
        },
    )
    write("validation/final-staged-privacy.json", privacy)
    write(
        "validation/final-diff-hygiene.json",
        {
            "schema": "ghc.family.v654-v4.final-diff-hygiene.v1",
            "staged_path_count": len(staged),
            "delta_manifest_entry_count": len(delta_entries),
            "self_exclusion_count": len(SELF_EXCLUSIONS),
            "out_of_scope_paths": out_of_scope,
            "sibling_document_paths": [
                path
                for path in staged
                if path.startswith("docs/")
                and not path.startswith("docs/caelen-morrow/v654-v4/")
            ],
            "x1_document_paths_changed": [
                path
                for path in staged
                if path.startswith(
                    (
                        "docs/caelen-morrow/v654-v4/preregistration/",
                        "docs/caelen-morrow/v654-v4/approval/",
                        "docs/caelen-morrow/v654-v4/sources/",
                    )
                )
            ],
            "evidence_artifact_paths_changed": [
                path
                for path in staged
                if path.startswith(
                    (
                        "docs/caelen-morrow/v654-v4/evidence/",
                        "docs/caelen-morrow/v654-v4/surfaces/",
                        "docs/caelen-morrow/v654-v4/skills/",
                        "docs/caelen-morrow/v654-v4/tools/",
                    )
                )
            ],
            "whitespace_check_returncode": whitespace.returncode,
            "valid": all(row["passed"] for row in checks),
        },
    )

    passed = sum(row["passed"] for row in checks)
    receipt = {
        "schema": "ghc.family.v654-v4.final-staged-review.v1",
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "valid": passed == len(checks),
        "staged_path_count": len(staged),
        "delta_manifest_entry_count": len(delta_entries),
        "owner_manifest_entry_count": len(owner_entries),
        "self_exclusion_count": len(SELF_EXCLUSIONS),
        "x1_manifest_entries_replayed": x1_count,
        "evidence_manifest_entries_replayed": evidence_count,
        "privacy_confirmed_hit_count": privacy["confirmed_hit_count"],
        "activation_baton_words": baton_words,
        "route_state": ROUTE_STATE,
        "full_repository_suite_run": False,
        "canonical_final_pass_run": False,
        "boundary": (
            "Precommit staged review only; not pushed-final equality, canonical "
            "success, independent reproduction, authority, delivery, or Stage 20."
        ),
    }
    write("validation/final-staged-review.json", receipt)
    print(
        json.dumps(
            {
                "passed": passed,
                "total": len(checks),
                "valid": receipt["valid"],
                "delta_entries": len(delta_entries),
                "owner_entries": len(owner_entries),
                "privacy_hits": privacy["confirmed_hit_count"],
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if receipt["valid"] else 1)


if __name__ == "__main__":
    main()

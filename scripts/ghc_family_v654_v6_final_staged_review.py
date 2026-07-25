#!/usr/bin/env python3
"""Review the exact staged Tavian v654-v6 content seal and build manifests."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tavian-sol/v654-v6"
X1 = "731c783c923fc46bd369a5bd2365b5dcddddaaeb"
EVIDENCE = "006f60277001726c07fd038e1645efcf62fdeb56"
ROUTE_STATE = "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
SELF_EXCLUSIONS = {
    "docs/tavian-sol/v654-v6/validation/final-delta-manifest.json",
    "docs/tavian-sol/v654-v6/validation/final-owner-manifest.json",
    "docs/tavian-sol/v654-v6/validation/final-staged-privacy.json",
    "docs/tavian-sol/v654-v6/validation/final-staged-review.json",
    "docs/tavian-sol/v654-v6/validation/final-diff-hygiene.json",
}
RUNNER_PATHS = {
    "scripts/ghc_family_bagit_validity_firewall.py",
    "scripts/ghc_family_fixity_mismatch_quarantine.py",
    "scripts/ghc_family_format_risk_reservation.py",
    "scripts/ghc_family_gmut_preservation_fields.py",
    "scripts/ghc_family_migration_event_lineage.py",
    "scripts/ghc_family_preservation_metadata_crosswalk.py",
    "scripts/ghc_family_preservation_package_integrity.py",
    "scripts/ghc_family_replica_scrub_reservation.py",
    "scripts/ghc_family_thos_preservation_proxy.py",
}
PHASE_SCRIPT_PATHS = {
    "scripts/ghc_family_v654_v6_phase_data.py",
    "scripts/ghc_family_v654_v6_x2_data.py",
    "scripts/ghc_family_v654_v6_core.py",
    "scripts/build_ghc_family_v654_v6_method_flow.py",
    "scripts/build_ghc_family_v654_v6_preregistration.py",
    "scripts/ghc_family_v654_v6_x1_validate.py",
    "scripts/build_ghc_family_v654_v6_x2_method_flow.py",
    "scripts/build_ghc_family_v654_v6_evidence.py",
    "scripts/ghc_family_v654_v6_evidence_validate.py",
    "scripts/ghc_family_v654_v6_detailed_validator.py",
    "scripts/ghc_family_v654_v6_bounded_suite.py",
    "scripts/build_ghc_family_v654_v6_closeout.py",
    "scripts/ghc_family_v654_v6_final_staged_review.py",
    "scripts/ghc_family_v654_v6_final_validate.py",
}
PHASE_TEST_PATHS = {
    "tests/test_ghc_family_v654_v6_x1.py",
    "tests/test_ghc_family_v654_v6.py",
    "tests/test_ghc_family_v654_v6_closeout.py",
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


@lru_cache(maxsize=1)
def index_entries() -> dict[str, str]:
    raw = subprocess.check_output(
        ["git", "ls-files", "--stage", "-z"], cwd=REPO
    )
    result: dict[str, str] = {}
    for record in raw.split(b"\0"):
        if not record or b"\t" not in record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode, oid, stage = metadata.decode("ascii").split()
        if stage == "0":
            result[path.decode("utf-8")] = oid
    return result


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
        if (
            len(header) != 3
            or header[0] != expected
            or header[1] != "blob"
        ):
            raise RuntimeError(f"unexpected blob header: {header}")
        size = int(header[2])
        result[expected] = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch frame terminator")
    if stream.read():
        raise RuntimeError("unexpected trailing batch output")
    return result


INDEX_BLOB_CACHE: dict[str, bytes] = {}


def prime_index_blob_cache(paths: list[str]) -> None:
    entries = index_entries()
    missing_paths = [path for path in paths if path not in INDEX_BLOB_CACHE]
    missing_from_index = [
        path for path in missing_paths if path not in entries
    ]
    if missing_from_index:
        raise RuntimeError(
            f"paths missing from staged index: {missing_from_index}"
        )
    blobs = batch_blobs([entries[path] for path in missing_paths])
    for path in missing_paths:
        INDEX_BLOB_CACHE[path] = blobs[entries[path]]


def index_oid(relative: str) -> str:
    return index_entries()[relative]


def index_blob(relative: str) -> bytes:
    if relative not in INDEX_BLOB_CACHE:
        prime_index_blob_cache([relative])
    return INDEX_BLOB_CACHE[relative]


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
    return sorted(index_entries())


def owner_path(relative: str) -> bool:
    return (
        relative.startswith("docs/tavian-sol/v654-v6/")
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
            or relative == "scripts/build_ghc_family_v654_v6_preregistration.py"
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
        "schema": "ghc.family.v654-v6.final-staged-privacy.v1",
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
    tree = {}
    for line in git("ls-tree", "-r", anchor).splitlines():
        if "\t" not in line:
            continue
        metadata, path = line.split("\t", 1)
        fields = metadata.split()
        if len(fields) == 3 and fields[1] == "blob":
            tree[path] = fields[2]
    mismatches = []
    for row in manifest["entries"]:
        observed = tree.get(row["path"])
        if observed != row["git_blob"]:
            mismatches.append(
                {
                    "path": row["path"],
                    "expected": row["git_blob"],
                    "observed": observed,
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
        if not path.startswith("docs/tavian-sol/v654-v6/")
        and path not in ALLOWED_NON_DOC_PATHS
    ]
    check("staged_scope", not out_of_scope, out_of_scope)
    check(
        "no_sibling_docs",
        not any(path.startswith("docs/") and not path.startswith(
            "docs/tavian-sol/v654-v6/"
        ) for path in staged),
        [path for path in staged if path.startswith("docs/") and not path.startswith(
            "docs/tavian-sol/v654-v6/"
        )],
    )
    check(
        "x1_paths_immutable",
        not any(
            path.startswith(
                (
                    "docs/tavian-sol/v654-v6/preregistration/",
                    "docs/tavian-sol/v654-v6/approval/",
                    "docs/tavian-sol/v654-v6/sources/",
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
                    "docs/tavian-sol/v654-v6/evidence/",
                    "docs/tavian-sol/v654-v6/surfaces/",
                    "docs/tavian-sol/v654-v6/skills/",
                    "docs/tavian-sol/v654-v6/tools/",
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
        "docs/tavian-sol/v654-v6/validation/x1-staged-manifest.json",
    )
    evidence_count, evidence_mismatch = replay_manifest(
        EVIDENCE,
        "docs/tavian-sol/v654-v6/validation/evidence-manifest.json",
    )
    check(
        "immutable_x1_manifest",
        not x1_mismatch and x1_count == 82,
        {"entries": x1_count, "mismatches": x1_mismatch},
    )
    check(
        "immutable_evidence_manifest",
        not evidence_mismatch and evidence_count == 200,
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
    prime_index_blob_cache(sorted(set(delta_paths) | set(owner_paths)))
    owner_entries = [hash_index_entry(path) for path in owner_paths]
    privacy = privacy_scan(owner_paths)
    check("privacy", privacy["confirmed_hit_count"] == 0, privacy["confirmed_hits"])
    check("owner_file_cap", len(owner_paths) + len(SELF_EXCLUSIONS) <= 2000, len(owner_paths))

    route = json.loads(
        index_blob(
            "docs/tavian-sol/v654-v6/route/terminal-existing-task-baton.json"
        ).decode("utf-8")
    )
    check(
        "route_prepared_not_sent",
        route["state"] == ROUTE_STATE
        and route["recipient_title"] == "Elaren Kestrel"
        and route["successor_phase"] == "v654-v7"
        and route["target_type"] == "main_task"
        and route["existing_task_only"]
        and route["task_created_count"] == 0
        and route["task_contacted_count"] == 0
        and route["message_limit"] == 1
        and route["direct_and_fallback_mutually_exclusive"],
        route,
    )

    baton = index_blob(
        "docs/tavian-sol/v654-v6/handoffs/elaren-kestrel-v654-v7-main-task-activation.md"
    ).decode("utf-8")
    baton_words = len(baton.split())
    check("baton_word_cap", 10000 <= baton_words <= 100000, baton_words)
    check(
        "baton_sanitized_route",
        "Tavian Sol" in baton
        and "Elaren Kestrel" in baton
        and ROUTE_STATE in baton
        and "new user-visible main task" not in baton.casefold()
        and "source_thread_id" not in baton.casefold(),
        "terminal-gated Elaren continuity packet",
    )

    write(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.v654-v6.final-delta-manifest.v1",
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
            "schema": "ghc.family.v654-v6.final-owner-manifest.v1",
            "hash_domain": "exact_staged_git_index_blob",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusions": sorted(SELF_EXCLUSIONS),
            "owner_interpretation": (
                "All Tavian v654-v6 docs plus phase-local v654-v6 scripts, "
                "family-current preservation runners, and v654-v6 tests."
            ),
        },
    )
    write("validation/final-staged-privacy.json", privacy)
    write(
        "validation/final-diff-hygiene.json",
        {
            "schema": "ghc.family.v654-v6.final-diff-hygiene.v1",
            "staged_path_count": len(staged),
            "delta_manifest_entry_count": len(delta_entries),
            "self_exclusion_count": len(SELF_EXCLUSIONS),
            "out_of_scope_paths": out_of_scope,
            "sibling_document_paths": [
                path
                for path in staged
                if path.startswith("docs/")
                and not path.startswith("docs/tavian-sol/v654-v6/")
            ],
            "x1_document_paths_changed": [
                path
                for path in staged
                if path.startswith(
                    (
                        "docs/tavian-sol/v654-v6/preregistration/",
                        "docs/tavian-sol/v654-v6/approval/",
                        "docs/tavian-sol/v654-v6/sources/",
                    )
                )
            ],
            "evidence_artifact_paths_changed": [
                path
                for path in staged
                if path.startswith(
                    (
                        "docs/tavian-sol/v654-v6/evidence/",
                        "docs/tavian-sol/v654-v6/surfaces/",
                        "docs/tavian-sol/v654-v6/skills/",
                        "docs/tavian-sol/v654-v6/tools/",
                    )
                )
            ],
            "whitespace_check_returncode": whitespace.returncode,
            "valid": all(row["passed"] for row in checks),
        },
    )

    passed = sum(row["passed"] for row in checks)
    receipt = {
        "schema": "ghc.family.v654-v6.final-staged-review.v1",
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
        "continuity_packet_words": baton_words,
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

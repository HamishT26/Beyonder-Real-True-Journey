#!/usr/bin/env python3
"""Build v474 THOS v5 x1 checksum/source-reference manifest artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v5-x1"
NEXT_PHASE = "v474-thos-v5-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

SOURCE_ARTIFACTS = [
    "docs/trinity-live-traces/v474-thos-v3-x2-publication-guard-v1.json",
    "docs/trinity-live-traces/v474-thos-v3-x2-publication-guard-v1.md",
    "docs/trinity-live-traces/v474-thos-v4-x1-staged-allowlist-validator-v1.json",
    "docs/trinity-live-traces/v474-thos-v4-x1-staged-allowlist-validator-v1.md",
    "docs/trinity-live-traces/v474-thos-v4-x2-combined-preflight-synthesis-v1.json",
    "docs/trinity-live-traces/v474-thos-v4-x2-combined-preflight-synthesis-v1.md",
]

BLOCKED_PATH_FRAGMENTS = [
    "raw-",
    "session",
    "screenshot",
    "plugin-cache",
    ".codex",
    "tmp/",
    "temp/",
]

APP_CHECKSUM_ADVISORIES = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "checksums bind curated artifact sets to preflight records only",
            "do not hash or publish raw lane output, temp files, session material, visual captures, credentials, external plugin-cache bodies, or unrelated dirty files",
            "unrelated dirty files should not be staged or hashed into publication evidence",
            "checksums do not grant publication authority or validate GMUT",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "checksums strengthen traceability but do not make content safe to expose",
            "privacy and marker-review holds dominate checksum presence",
            "manifest should support waiting and open-gap-carried states",
            "source references state artifact identity, not truth of claims",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "use sha256 with lowercase fixed-length hex",
            "each artifact row needs source references and current-phase/source-phase scope",
            "missing, malformed, mismatched, duplicate, wrong-phase, or raw-text rows are blockers",
            "manifest refs should be bound to allowlist/candidate sets, not broad discovery",
        ],
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_ref(path_text: str) -> dict[str, Any]:
    normalized = path_text.replace("\\", "/")
    path = REPO_ROOT / normalized
    blocked_fragment = next((item for item in BLOCKED_PATH_FRAGMENTS if item.lower() in normalized.lower()), None)
    if blocked_fragment:
        return {
            "path": normalized,
            "reason": f"blocked path fragment {blocked_fragment}",
            "status": "FAIL_BLOCKER",
        }
    if not path.exists():
        return {
            "path": normalized,
            "reason": "source artifact is missing",
            "status": "OPEN_GAP_MISSING_SOURCE",
        }
    if path.is_dir():
        return {
            "path": normalized,
            "reason": "source reference is a directory, not an exact artifact",
            "status": "FAIL_BLOCKER",
        }
    return {
        "bytes": path.stat().st_size,
        "claim_ceiling": "traceability_only_no_publication_authority_no_gmut_validation",
        "path": normalized,
        "privacy_status": "curated_repo_artifact_only_raw_runtime_material_not_included",
        "reason": "source artifact hash recorded",
        "review_status": "repo_published_source_reference",
        "sha256": sha256_file(path),
        "status": "PASS_SHAPE_ONLY",
    }


def fixture(case_id: str, path_text: str, expected: str) -> dict[str, Any]:
    observed = source_ref(path_text)["status"]
    return {
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "status": "EXPECTED_CONFIRMED" if observed == expected else "EXPECTED_FAIL_MISMATCH",
    }


def build_fixtures() -> list[dict[str, Any]]:
    return [
        fixture("known_source_hashes", SOURCE_ARTIFACTS[0], "PASS_SHAPE_ONLY"),
        fixture("missing_source_open_gap", "docs/trinity-live-traces/v474-thos-v5-x1-missing-source-v1.json", "OPEN_GAP_MISSING_SOURCE"),
        fixture("raw_source_blocked", "docs/trinity-live-traces/raw-lane-output.txt", "FAIL_BLOCKER"),
        fixture("plugin_cache_source_blocked", "plugin-cache/some-skill/SKILL.md", "FAIL_BLOCKER"),
        fixture("broad_directory_blocked", "docs/trinity-live-traces", "FAIL_BLOCKER"),
    ]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate_status(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    source_refs = [source_ref(path) for path in SOURCE_ARTIFACTS]
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    script_ref = source_ref(rel_path(Path(__file__).resolve()))
    source_rows = [
        row(
            "source_hashes",
            aggregate_status([{"status": item["status"]} for item in source_refs]),
            "Source artifact checksum references were recorded for the guard/preflight chain.",
            {"source_count": len(source_refs)},
        ),
        row(
            "script_hash",
            script_ref["status"],
            "The current manifest generator script hash was recorded.",
            {"script_path": script_ref["path"]},
        ),
        row(
            "fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_BLOCKER",
            "Expected source-reference fixtures were evaluated.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "app_checksum_advisories",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were folded into the checksum manifest.",
            {"advisory_count": len(APP_CHECKSUM_ADVISORIES)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Checksum references support THOS traceability only; GMUT gates remain open.",
        ),
    ]
    manifest = {
        "aggregate_status": aggregate_status(source_rows),
        "app_checksum_advisories": APP_CHECKSUM_ADVISORIES,
        "blocked_path_fragments": BLOCKED_PATH_FRAGMENTS,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "hash_algorithm": "sha256",
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": source_rows,
        "script_reference": script_ref,
        "source_references": source_refs,
        "traceability_ceiling": "repo-published source artifacts only; no raw lane text, temp files, external cache files, or publication authority claim",
        "required_row_fields": [
            "path",
            "sha256",
            "bytes",
            "status",
            "privacy_status",
            "review_status",
            "claim_ceiling",
        ],
    }
    run_status = {
        "aggregate_status": manifest["aggregate_status"],
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": source_rows,
    }

    written: list[Path] = []
    manifest_json = ARTIFACT_ROOT / f"{PHASE}-checksum-source-manifest-v1.json"
    write_json(manifest_json, manifest)
    written.append(manifest_json)
    manifest_md = ARTIFACT_ROOT / f"{PHASE}-checksum-source-manifest-v1.md"
    write_md(
        manifest_md,
        f"""
# v474 THOS v5 x1 Checksum Source Manifest

Generated UTC: `{generated_at}`

Status: `{manifest['aggregate_status']}`

Recorded SHA-256 references for `{len(source_refs)}` repo-published guard/preflight source artifacts plus the manifest generator script. Raw lane text, temp files, external plugin-cache material, unrelated dirty files, and broad directory references are excluded from durable checksum evidence.

Fixture results: `{len(fixtures) - len(fixture_mismatches)}` confirmed, `{len(fixture_mismatches)}` mismatched.

All six GMUT gates remain open.
""",
    )
    written.append(manifest_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v5 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v5 x1 adds checksum/source-reference traceability for the publication preflight chain without publishing raw lane output or overriding marker-review holds.

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def main() -> int:
    for path in build_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

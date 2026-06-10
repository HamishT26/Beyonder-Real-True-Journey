#!/usr/bin/env python3
"""Generate a non-mutating THOS phase artifact manifest.

The manifest records file identity, checksum, and lightweight JSON metadata for
a phase artifact set. It does not stage, commit, upload, delete, or mutate
anything except the optional local output file explicitly requested by --output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {"PASS_SHAPE_ONLY", "FAIL_BLOCKER", "OPEN_GAP", "NOT_RUN"}


def sha256_hex(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def line_count(path: Path) -> int:
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf"}:
        return 0
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text:
        return 0
    return len(text.splitlines())


def collect_statuses(value: Any) -> list[str]:
    statuses: list[str] = []
    if isinstance(value, dict):
        for key in ["status", "aggregate_status", "phase_result"]:
            current = value.get(key)
            if isinstance(current, str):
                statuses.append(current)
        for nested in value.values():
            if isinstance(nested, (dict, list)):
                statuses.extend(collect_statuses(nested))
    elif isinstance(value, list):
        for nested in value:
            statuses.extend(collect_statuses(nested))
    return statuses


def json_summary(path: Path) -> dict[str, Any]:
    if path.suffix.lower() != ".json":
        return {"json_parse": "not_json"}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"json_parse": "FAIL_BLOCKER", "json_error": str(exc)}
    rows = parsed.get("rows") if isinstance(parsed, dict) else None
    statuses = collect_statuses(parsed)
    invalid = sorted({status for status in statuses if status.isupper() and status not in ALLOWED_STATUSES})
    return {
        "json_parse": "PASS_SHAPE_ONLY",
        "artifact_id": parsed.get("artifact_id") if isinstance(parsed, dict) else None,
        "aggregate_status": parsed.get("aggregate_status") if isinstance(parsed, dict) else None,
        "row_count": len(rows) if isinstance(rows, list) else None,
        "gmUT_gate_effect": parsed.get("gmUT_gate_effect") if isinstance(parsed, dict) else None,
        "invalid_upper_status_values": invalid,
    }


def artifact_family(path: Path) -> str:
    name = path.name
    for marker in [
        "source-refresh",
        "supervisor-export",
        "regression-execution",
        "unreconciled-exception-export",
        "data-driven-visualization",
        "sibling-synthesis",
        "handoff",
        "run-status",
    ]:
        if marker in name:
            return marker
    return "other"


def build_manifest(phase_slug: str, artifact_root: Path) -> dict[str, Any]:
    files = sorted(artifact_root.glob(f"{phase_slug}-*"))
    artifacts = []
    for path in files:
        rel = path.as_posix()
        artifacts.append(
            {
                "path": rel,
                "family": artifact_family(path),
                "suffix": path.suffix.lower(),
                "bytes": path.stat().st_size,
                "line_count": line_count(path),
                "sha256": sha256_hex(path),
                **json_summary(path),
            }
        )
    family_counts: dict[str, int] = {}
    for artifact in artifacts:
        family_counts[artifact["family"]] = family_counts.get(artifact["family"], 0) + 1
    aggregate_status = "PASS_SHAPE_ONLY"
    if not artifacts:
        aggregate_status = "FAIL_BLOCKER"
    elif any(artifact.get("json_parse") == "FAIL_BLOCKER" for artifact in artifacts):
        aggregate_status = "FAIL_BLOCKER"
    return {
        "validator_mode": "local_non_mutating_phase_manifest",
        "manifested_phase_slug": phase_slug,
        "artifact_root": artifact_root.as_posix(),
        "aggregate_status": aggregate_status,
        "mutation_performed": False,
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        "artifact_count": len(artifacts),
        "family_counts": family_counts,
        "artifacts": artifacts,
    }


def verify_manifest(manifest_path: Path) -> dict[str, Any]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "validator_mode": "local_non_mutating_phase_manifest_verify",
            "manifest_file": manifest_path.as_posix(),
            "aggregate_status": "FAIL_BLOCKER",
            "mutation_performed": False,
            "connector_write_performed": False,
            "gmUT_gate_effect": "none_open_not_tested",
            "rows": [
                {
                    "row_id": "manifest_parse",
                    "status": "FAIL_BLOCKER",
                    "reason_code": "manifest_parse_failed",
                    "evidence": str(exc),
                }
            ],
        }

    rows: list[dict[str, Any]] = []
    artifacts = manifest.get("artifacts", [])
    if not isinstance(artifacts, list):
        rows.append(
            {
                "row_id": "manifest_artifacts",
                "status": "FAIL_BLOCKER",
                "reason_code": "artifacts_not_list",
                "path": None,
            }
        )
    for idx, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            rows.append(
                {
                    "row_id": f"artifact_{idx}",
                    "status": "FAIL_BLOCKER",
                    "reason_code": "artifact_not_object",
                    "path": None,
                }
            )
            continue
        artifact_path = artifact.get("path")
        expected_sha256 = artifact.get("sha256")
        if not isinstance(artifact_path, str) or not isinstance(expected_sha256, str):
            rows.append(
                {
                    "row_id": f"artifact_{idx}",
                    "status": "FAIL_BLOCKER",
                    "reason_code": "missing_path_or_sha256",
                    "path": artifact_path,
                }
            )
            continue
        path = Path(artifact_path)
        if not path.exists():
            rows.append(
                {
                    "row_id": artifact_path,
                    "status": "FAIL_BLOCKER",
                    "reason_code": "artifact_missing",
                    "path": artifact_path,
                    "expected_sha256": expected_sha256,
                    "actual_sha256": None,
                }
            )
            continue
        actual_sha256 = sha256_hex(path)
        status = "PASS_SHAPE_ONLY" if actual_sha256 == expected_sha256 else "FAIL_BLOCKER"
        reason = "checksum_matched" if status == "PASS_SHAPE_ONLY" else "checksum_mismatch"
        rows.append(
            {
                "row_id": artifact_path,
                "status": status,
                "reason_code": reason,
                "path": artifact_path,
                "expected_sha256": expected_sha256,
                "actual_sha256": actual_sha256,
            }
        )
    aggregate_status = "FAIL_BLOCKER" if not rows or any(row["status"] == "FAIL_BLOCKER" for row in rows) else "PASS_SHAPE_ONLY"
    return {
        "validator_mode": "local_non_mutating_phase_manifest_verify",
        "manifest_file": manifest_path.as_posix(),
        "manifested_phase_slug": manifest.get("manifested_phase_slug"),
        "aggregate_status": aggregate_status,
        "mutation_performed": False,
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        "artifact_count": len(artifacts) if isinstance(artifacts, list) else 0,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a local THOS phase artifact manifest.")
    parser.add_argument("--phase-slug", help="Phase slug to manifest")
    parser.add_argument(
        "--artifact-root",
        default="docs/trinity-live-traces",
        help="Directory containing phase artifacts",
    )
    parser.add_argument("--output", help="Optional JSON manifest path to write")
    parser.add_argument("--verify-manifest", help="Verify paths and checksums from an existing manifest")
    args = parser.parse_args()

    if args.verify_manifest:
        report = verify_manifest(Path(args.verify_manifest))
    else:
        if not args.phase_slug:
            raise SystemExit("--phase-slug is required unless --verify-manifest is used")
        report = build_manifest(args.phase_slug, Path(args.artifact_root))
    output = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if report["aggregate_status"] == "FAIL_BLOCKER" else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Tempdir-only regression harness for THOS assertion manifests.

The harness materializes synthetic artifacts in temporary directories, invokes
the real publication guard, and emits a curated summary report. It does not
write connector outputs, mutate repo fixtures, or preserve raw temp payloads.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_PHASE_SLUG = "v470-thos-v7-x5-regression"
DEFAULT_COVERAGE_TOKEN = "happy-path"
GUARD_SCRIPT = Path(__file__).resolve().with_name("thos_publication_guard.py")


@dataclass
class Case:
    case_id: str
    expected_decision: str
    expected_status: str
    expected_fragments: list[str]
    materialize_valid_assertion: bool = True
    materialize_stray_assertion: bool = False
    manifest_override: dict[str, Any] | None = None
    manifest_bytes: str | None = None
    path_list_override: dict[str, Any] | None = None
    omit_manifest_flag: bool = False
    required_coverage_tokens: list[str] = field(default_factory=lambda: [DEFAULT_COVERAGE_TOKEN])


def assertion_payload(*, status: str = "PASS_SHAPE_ONLY", connector_write: bool = False) -> dict[str, Any]:
    failures = [] if status == "PASS_SHAPE_ONLY" else ["boundary:local_non_mutating"]
    return {
        "aggregate_status": status,
        "assertion_failures": failures,
        "assertion_status": status,
        "connector_write_performed": connector_write,
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "observed_report_status": "FAIL_BLOCKER",
        "report_input": "synthetic://manifest-regression",
        "report_mode": "local_non_mutating",
        "rows": [],
        "validator_mode": "local_non_mutating_visualization_report_assertion",
    }


def base_manifest(phase_slug: str, assertion_path: str, negative_assertion_path: str | None = None) -> dict[str, Any]:
    refs = [
        {
            "artifact_id": "happy-positive-v1",
            "coverage_tokens": [DEFAULT_COVERAGE_TOKEN],
            "expectation": "positive",
            "expected_status": "PASS_SHAPE_ONLY",
            "path": assertion_path,
            "report_input": "synthetic://manifest-regression",
            "variant_id": "tempdir-positive",
        }
    ]
    if negative_assertion_path is not None:
        refs.append(
            {
                "artifact_id": "happy-expected-negative-v1",
                "coverage_tokens": ["negative-boundary"],
                "expectation": "expected_negative",
                "expected_failure_tokens": ["boundary:local_non_mutating"],
                "expected_status": "FAIL_BLOCKER",
                "path": negative_assertion_path,
                "report_input": "synthetic://manifest-regression-negative",
                "variant_id": "tempdir-expected-negative",
            }
        )
    return {
        "artifact_refs": [
            *refs
        ],
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        "manifest_schema": "thos_assertion_artifact_manifest_v1",
        "mutation_performed": False,
        "phase_slug": phase_slug,
        "published_claim_boundary": "local_manifest_regression_only",
        "validator_mode": "local_non_mutating",
    }


def base_path_list(phase_slug: str, assertion_path: str, negative_assertion_path: str | None = None) -> dict[str, Any]:
    paths = [assertion_path]
    if negative_assertion_path is not None:
        paths.append(negative_assertion_path)
    return {
        "connector_write_performed": False,
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "path_list_schema": "thos_assertion_path_list_v1",
        "paths": paths,
        "phase_slug": phase_slug,
        "validator_mode": "local_non_mutating",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_guard(
    *,
    cwd: Path,
    phase_slug: str,
    manifest_path: Path | None,
    path_list_path: Path,
    required_coverage_tokens: list[str],
) -> tuple[int, dict[str, Any]]:
    cmd = [
        sys.executable,
        str(GUARD_SCRIPT),
        "--phase-slug",
        phase_slug,
        "--artifact-root",
        "artifacts",
        "--require-assertion-artifacts",
        "--require-assertion-manifest",
        "--assertion-path-list",
        path_list_path.as_posix(),
        "--skip-git-drift",
    ]
    if manifest_path is not None:
        cmd.extend(["--assertion-manifest", manifest_path.as_posix()])
    for token in required_coverage_tokens:
        cmd.extend(["--require-assertion-coverage", token])

    result = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        payload = json.loads(result.stdout)
    except Exception:
        payload = {
            "aggregate_status": "FAIL_BLOCKER",
            "rows": [
                {
                    "row_id": "harness_guard_json_parse",
                    "status": "FAIL_BLOCKER",
                    "message": "guard stdout was not JSON",
                    "evidence": result.stderr.strip(),
                }
            ],
        }
    return result.returncode, payload


def row_blob(payload: dict[str, Any]) -> str:
    return json.dumps(payload.get("rows", []), sort_keys=True)


def case_decision(returncode: int, payload: dict[str, Any]) -> str:
    if returncode == 0 and payload.get("aggregate_status") == "PASS_SHAPE_ONLY":
        return "allow"
    return "deny"


def run_case(case: Case, phase_slug: str) -> dict[str, Any]:
    root_ref = "tempdir_case_root"
    with tempfile.TemporaryDirectory(prefix=f"{case.case_id}-") as tmp:
        tmp_path = Path(tmp)
        artifact_root = tmp_path / "artifacts"
        assertion_rel = f"artifacts/{phase_slug}-assert-{case.case_id}-v1.json"
        assertion_path = tmp_path / assertion_rel
        negative_rel = f"artifacts/{phase_slug}-assert-negative-{case.case_id}-v1.json"
        negative_path = tmp_path / negative_rel
        manifest_rel = f"artifacts/{phase_slug}-assertion-manifest-{case.case_id}-v1.json"
        manifest_path = tmp_path / manifest_rel
        path_list_rel = f"artifacts/{phase_slug}-assertion-path-list-{case.case_id}-v1.json"
        path_list_path = tmp_path / path_list_rel

        if case.materialize_valid_assertion:
            payload = assertion_payload()
            if case.case_id == "expectation_status_mismatch":
                payload = assertion_payload(status="FAIL_BLOCKER")
            if case.case_id == "boundary_drift_rejected":
                payload = assertion_payload(connector_write=True)
            write_json(assertion_path, payload)
            negative_payload = assertion_payload(status="FAIL_BLOCKER")
            negative_payload["report_input"] = "synthetic://manifest-regression-negative"
            write_json(negative_path, negative_payload)

        if case.materialize_stray_assertion:
            stray = artifact_root / f"{phase_slug}-assert-stray-v1.json"
            write_json(stray, assertion_payload())

        manifest_payload = (
            case.manifest_override
            if case.manifest_override is not None
            else base_manifest(phase_slug, assertion_rel, negative_rel)
        )
        path_list_payload = (
            case.path_list_override
            if case.path_list_override is not None
            else base_path_list(phase_slug, assertion_rel, negative_rel)
        )

        if case.manifest_bytes is not None:
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(case.manifest_bytes, encoding="utf-8")
        elif not case.omit_manifest_flag:
            write_json(manifest_path, manifest_payload)
        write_json(path_list_path, path_list_payload)

        manifest_arg = None if case.omit_manifest_flag else Path(manifest_rel)
        returncode, guard_payload = run_guard(
            cwd=tmp_path,
            phase_slug=phase_slug,
            manifest_path=manifest_arg,
            path_list_path=Path(path_list_rel),
            required_coverage_tokens=case.required_coverage_tokens,
        )
        blob = row_blob(guard_payload)
        matched = [fragment for fragment in case.expected_fragments if fragment in blob]
        observed_decision = case_decision(returncode, guard_payload)
        temp_fixture_count = len(list(artifact_root.glob("*"))) if artifact_root.exists() else 0

    cleanup_verified = not tmp_path.exists()
    matches = (
        observed_decision == case.expected_decision
        and guard_payload.get("aggregate_status") == case.expected_status
        and len(matched) == len(case.expected_fragments)
        and cleanup_verified
    )
    return {
        "case_id": case.case_id,
        "cleanup_verified": cleanup_verified,
        "curated_temp_fixture_count": 0,
        "expected_decision": case.expected_decision,
        "expected_fragments": case.expected_fragments,
        "expected_status": case.expected_status,
        "guard_aggregate_status": guard_payload.get("aggregate_status"),
        "guard_decision": observed_decision,
        "guard_returncode": returncode,
        "matched_fragments": matched,
        "matches_expected": matches,
        "mutation_performed": False,
        "root_ref": root_ref,
        "temp_fixture_count": temp_fixture_count,
    }


def build_cases(phase_slug: str) -> list[Case]:
    assertion_rel = f"artifacts/{phase_slug}-assert-happy-v1.json"
    negative_rel = f"artifacts/{phase_slug}-assert-negative-happy-v1.json"
    happy_manifest = base_manifest(phase_slug, assertion_rel, negative_rel)
    return [
        Case("happy_manifest_allows", "allow", "PASS_SHAPE_ONLY", ["assertion artifacts passed contract"]),
        Case("missing_manifest_required", "deny", "FAIL_BLOCKER", ["explicit assertion manifest is required"], omit_manifest_flag=True),
        Case("malformed_manifest_json", "deny", "FAIL_BLOCKER", ["manifest JSON unreadable"], manifest_bytes="{"),
        Case(
            "path_list_mismatch",
            "deny",
            "FAIL_BLOCKER",
            ["paths do not match manifest"],
            path_list_override=base_path_list(phase_slug, f"artifacts/{phase_slug}-assert-other-v1.json", negative_rel),
        ),
        Case(
            "absolute_path_rejected",
            "deny",
            "FAIL_BLOCKER",
            ["absolute paths are not allowed"],
            manifest_override={
                **happy_manifest,
                "artifact_refs": [{**happy_manifest["artifact_refs"][0], "path": "C:/escape.json"}],
            },
        ),
        Case(
            "traversal_path_rejected",
            "deny",
            "FAIL_BLOCKER",
            ["path traversal or empty path segment is not allowed"],
            manifest_override={
                **happy_manifest,
                "artifact_refs": [{**happy_manifest["artifact_refs"][0], "path": f"artifacts/../{phase_slug}-assert-escape-v1.json"}],
            },
        ),
        Case("missing_artifact_rejected", "deny", "FAIL_BLOCKER", ["manifest-listed assertion artifact is not in phase artifact set"], materialize_valid_assertion=False),
        Case("expectation_status_mismatch", "deny", "FAIL_BLOCKER", ["did not match manifest expected_status"]),
        Case("boundary_drift_rejected", "deny", "FAIL_BLOCKER", ["assertion boundary fields are not local/non-mutating"]),
        Case("coverage_gap_rejected", "deny", "FAIL_BLOCKER", ["missing assertion coverage tokens"], required_coverage_tokens=["missing-token"]),
        Case("stray_assertion_rejected", "deny", "FAIL_BLOCKER", ["closed-world contract"], materialize_stray_assertion=True),
        Case(
            "duplicate_artifact_id_rejected",
            "deny",
            "FAIL_BLOCKER",
            ["duplicate artifact_id"],
            manifest_override={
                **happy_manifest,
                "artifact_refs": [happy_manifest["artifact_refs"][0], happy_manifest["artifact_refs"][0]],
            },
        ),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run tempdir-only THOS assertion-manifest regressions.")
    parser.add_argument("--phase-slug", default=DEFAULT_PHASE_SLUG)
    parser.add_argument("--output", help="Optional JSON report path")
    args = parser.parse_args()

    cases = [run_case(case, args.phase_slug) for case in build_cases(args.phase_slug)]
    failures = [case for case in cases if not case["matches_expected"]]
    report = {
        "aggregate_status": "FAIL_BLOCKER" if failures else "PASS_SHAPE_ONLY",
        "case_count": len(cases),
        "cases": cases,
        "connector_write_performed": False,
        "curated_summary_only": True,
        "curated_temp_fixture_count": 0,
        "gmUT_gate_effect": "none_open_not_tested",
        "harness_scope": "tempdir_only",
        "mutation_performed": False,
        "phase_slug": args.phase_slug,
        "regression_report_id": "thos_assertion_manifest_regression_v1",
        "started_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "temp_fixture_leakage": False,
        "validator_mode": "local_non_mutating_tempdir_regression",
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

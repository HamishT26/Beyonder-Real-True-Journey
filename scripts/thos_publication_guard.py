#!/usr/bin/env python3
"""Non-mutating THOS publication guard.

This checker is intentionally narrow: it validates a named phase artifact set
and reports blockers without staging, deleting, uploading, or modifying files.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


ALLOWED_STATUSES = {"FAIL_BLOCKER", "OPEN_GAP", "NOT_RUN", "PASS_SHAPE_ONLY"}
FORBIDDEN_PATH_RE = re.compile(
    r"(session.*jsonl|jsonl|screenshot|raw[-_ ]?log|credential|secret|token)",
    re.IGNORECASE,
)
SECRET_RE = re.compile(
    r"(sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|"
    r"gh[pousr]_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|"
    r"(api[_-]?key|access[_-]?token|password)\s*[:=]\s*[^\s\"']{8,})",
    re.IGNORECASE,
)
FORBIDDEN_CLAIM_RE = re.compile(
    r"(GMUT\s+validated|GMUT\s+validation\s+complete|"
    r"all\s+six\s+GMUT\s+gates\s+(?:closed|passed)|all\s+gates\s+closed|"
    r"final\s+physics\s+(?:complete|validated|solved)|consciousness\s+solved|"
    r"solved\s+consciousness\s+(?:achieved|complete|validated)|"
    r"empirical\s+spiritual\s+proof\s+achieved|fifth[- ]force\s+safety\s+confirmed|"
    r"canon\s+promoted|cleanup\s+completed\s+successfully|"
    r"connector\s+write\s+completed\s+successfully|cloud\s+mutation\s+completed\s+successfully)",
    re.IGNORECASE,
)


@dataclass
class Row:
    row_id: str
    status: str
    message: str
    evidence: str | None = None


@dataclass
class Report:
    phase_slug: str
    artifact_glob: str
    rows: list[Row] = field(default_factory=list)
    checked_files: list[str] = field(default_factory=list)
    staged_files: list[str] = field(default_factory=list)

    def add(self, row_id: str, status: str, message: str, evidence: str | None = None) -> None:
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"invalid status {status}")
        self.rows.append(Row(row_id, status, message, evidence))

    @property
    def aggregate_status(self) -> str:
        statuses = [row.status for row in self.rows]
        if "FAIL_BLOCKER" in statuses:
            return "FAIL_BLOCKER"
        if "OPEN_GAP" in statuses:
            return "OPEN_GAP"
        if statuses and all(status == "NOT_RUN" for status in statuses):
            return "NOT_RUN"
        return "PASS_SHAPE_ONLY"

    def as_json(self) -> dict:
        return {
            "phase_slug": self.phase_slug,
            "artifact_glob": self.artifact_glob,
            "validator_mode": "local_non_mutating",
            "aggregate_status": self.aggregate_status,
            "gmUT_gate_effect": "none_open_not_tested",
            "mutation_performed": False,
            "connector_write_performed": False,
            "checked_files": self.checked_files,
            "staged_files": self.staged_files,
            "rows": [row.__dict__ for row in self.rows],
        }


def git_lines(args: list[str]) -> list[str]:
    try:
        output = subprocess.check_output(["git", *args], text=True, stderr=subprocess.STDOUT)
    except Exception as exc:  # pragma: no cover - depends on local git availability
        return [f"UNREADABLE: {exc}"]
    return [line for line in output.splitlines() if line.strip()]


def iter_row_status_values(value: object) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        rows = value.get("rows")
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict):
                    status = row.get("status") or row.get("checker_status")
                    if isinstance(status, str):
                        found.append(status)
        for nested in value.values():
            if isinstance(nested, (dict, list)):
                found.extend(iter_row_status_values(nested))
    elif isinstance(value, list):
        for nested in value:
            found.extend(iter_row_status_values(nested))
    return found


def check_assertion_artifacts(files: list[Path], coverage_tokens: list[str]) -> tuple[str, str, str | None]:
    assertion_files = [path for path in files if path.suffix == ".json" and "-assert-" in path.name]
    if not assertion_files:
        return "FAIL_BLOCKER", "no assertion artifacts found", None

    positive_count = 0
    expected_negative_count = 0
    failures: list[str] = []
    covered = {token: False for token in coverage_tokens}

    for path in assertion_files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{path.as_posix()}: assertion JSON unreadable: {exc}")
            continue

        name = path.name
        for token in covered:
            if token in name:
                covered[token] = True

        expected_negative = "-assert-negative-" in name or "pre-fix" in name
        status = payload.get("assertion_status") or payload.get("aggregate_status")
        assertion_failures = payload.get("assertion_failures")
        boundary_ok = (
            payload.get("report_mode") == "local_non_mutating"
            and payload.get("connector_write_performed") is False
            and payload.get("mutation_performed") is False
            and payload.get("gmUT_gate_effect") == "none_open_not_tested"
        )
        if not boundary_ok:
            failures.append(f"{path.as_posix()}: assertion boundary fields are not local/non-mutating")
        if expected_negative:
            expected_negative_count += 1
            if status != "FAIL_BLOCKER" or not assertion_failures:
                failures.append(f"{path.as_posix()}: expected-negative assertion did not fail with reasons")
        else:
            positive_count += 1
            if status != "PASS_SHAPE_ONLY" or assertion_failures:
                failures.append(f"{path.as_posix()}: positive assertion did not pass cleanly")

    missing_coverage = [token for token, present in covered.items() if not present]
    if missing_coverage:
        failures.append(f"missing assertion coverage tokens: {missing_coverage}")
    if positive_count == 0:
        failures.append("no positive assertion artifacts found")
    if expected_negative_count == 0:
        failures.append("no expected-negative assertion artifacts found")
    if failures:
        return "FAIL_BLOCKER", "assertion artifacts failed contract", json.dumps(failures)
    return (
        "PASS_SHAPE_ONLY",
        f"assertion artifacts passed contract: {positive_count} positive, {expected_negative_count} expected-negative",
        json.dumps({"coverage_tokens": coverage_tokens}),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a non-mutating THOS publication guard.")
    parser.add_argument("--phase-slug", required=True, help="Phase slug, for example v470-thos-v3-x2")
    parser.add_argument(
        "--artifact-root",
        default="docs/trinity-live-traces",
        help="Artifact root containing phase files",
    )
    parser.add_argument(
        "--staged-only",
        action="store_true",
        help="Also check currently staged paths against the phase allowlist",
    )
    parser.add_argument(
        "--allow-staged",
        action="append",
        default=[],
        help="Additional exact staged path allowed for this phase, repeatable",
    )
    parser.add_argument(
        "--require-assertion-artifacts",
        action="store_true",
        help="Require local THOS assertion artifacts for visualization/report phases",
    )
    parser.add_argument(
        "--require-assertion-coverage",
        action="append",
        default=[],
        help="Require an assertion artifact filename to contain this coverage token, repeatable",
    )
    args = parser.parse_args()

    root = Path(args.artifact_root)
    artifact_glob = f"{args.phase_slug}-*"
    report = Report(phase_slug=args.phase_slug, artifact_glob=str(root / artifact_glob))

    files = sorted(root.glob(artifact_glob))
    report.checked_files = [path.as_posix() for path in files]
    if not files:
        report.add("artifact_presence", "FAIL_BLOCKER", "no artifacts matched phase slug")
    else:
        report.add("artifact_presence", "PASS_SHAPE_ONLY", f"found {len(files)} artifacts")

    for path in files:
        path_text = path.as_posix()
        if FORBIDDEN_PATH_RE.search(path_text):
            report.add("path_guard", "FAIL_BLOCKER", "forbidden path token", path_text)
        text = path.read_text(encoding="utf-8", errors="replace")
        if SECRET_RE.search(text):
            report.add("credential_guard", "FAIL_BLOCKER", "secret-like pattern in artifact", path_text)
        if FORBIDDEN_CLAIM_RE.search(text):
            report.add("forbidden_claim_guard", "FAIL_BLOCKER", "forbidden claim wording", path_text)
        if path.suffix == ".json":
            try:
                parsed = json.loads(text)
            except Exception as exc:
                report.add("json_parse", "FAIL_BLOCKER", f"JSON parse failed: {exc}", path_text)
            else:
                invalid_statuses = [status for status in iter_row_status_values(parsed) if status not in ALLOWED_STATUSES]
                if invalid_statuses:
                    report.add(
                        "status_enum",
                        "FAIL_BLOCKER",
                        f"invalid status values: {sorted(set(invalid_statuses))}",
                        path_text,
                    )
        for idx, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                report.add("trailing_whitespace", "FAIL_BLOCKER", "trailing whitespace", f"{path_text}:{idx}")

    if not any(row.row_id == "path_guard" for row in report.rows):
        report.add("path_guard", "PASS_SHAPE_ONLY", "no forbidden path tokens found")
    if not any(row.row_id == "credential_guard" for row in report.rows):
        report.add("credential_guard", "PASS_SHAPE_ONLY", "no secret-like content patterns found")
    if not any(row.row_id == "forbidden_claim_guard" for row in report.rows):
        report.add("forbidden_claim_guard", "PASS_SHAPE_ONLY", "no forbidden claim wording found")
    if not any(row.row_id == "json_parse" for row in report.rows):
        report.add("json_parse", "PASS_SHAPE_ONLY", "JSON artifacts parsed")
    if not any(row.row_id == "status_enum" for row in report.rows):
        report.add("status_enum", "PASS_SHAPE_ONLY", "status enum values are constrained")
    if not any(row.row_id == "trailing_whitespace" for row in report.rows):
        report.add("trailing_whitespace", "PASS_SHAPE_ONLY", "no trailing whitespace found")

    if args.require_assertion_artifacts:
        status, message, evidence = check_assertion_artifacts(files, args.require_assertion_coverage)
        report.add("assertion_artifact_contract", status, message, evidence)
    else:
        report.add("assertion_artifact_contract", "NOT_RUN", "assertion artifact contract not requested")

    if args.staged_only:
        staged = git_lines(["diff", "--cached", "--name-only"])
        report.staged_files = staged
        extra_allowed = set(args.allow_staged)
        unexpected = [
            name
            for name in staged
            if not name.startswith(f"{args.artifact_root}/{args.phase_slug}-") and name not in extra_allowed
        ]
        if unexpected:
            report.add("staged_allowlist", "FAIL_BLOCKER", "staged paths outside phase allowlist", json.dumps(unexpected))
        else:
            report.add("staged_allowlist", "PASS_SHAPE_ONLY", "staged paths match phase allowlist")
    else:
        report.add("staged_allowlist", "NOT_RUN", "staged-only check not requested")

    drift = git_lines(["rev-list", "--left-right", "--count", "HEAD...@{upstream}"])
    if drift and drift[0].startswith("UNREADABLE"):
        report.add("git_drift", "OPEN_GAP", "git drift unreadable", drift[0])
    else:
        report.add("git_drift", "PASS_SHAPE_ONLY", "git drift recorded", drift[0] if drift else "no output")

    print(json.dumps(report.as_json(), indent=2, sort_keys=True))
    return 1 if report.aggregate_status == "FAIL_BLOCKER" else 0


if __name__ == "__main__":
    sys.exit(main())

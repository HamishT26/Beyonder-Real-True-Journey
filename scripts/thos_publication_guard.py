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
from pathlib import Path, PurePosixPath, PureWindowsPath


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


def normalize_repo_path(path_text: str) -> tuple[str | None, str | None]:
    if not isinstance(path_text, str) or not path_text.strip():
        return None, "path is empty or not a string"
    normalized = path_text.replace("\\", "/")
    if PureWindowsPath(path_text).is_absolute() or PurePosixPath(normalized).is_absolute():
        return None, "absolute paths are not allowed"
    if normalized.startswith("//"):
        return None, "UNC-like paths are not allowed"
    parts = PurePosixPath(normalized).parts
    if any(part in {"..", ""} for part in parts):
        return None, "path traversal or empty path segment is not allowed"
    return PurePosixPath(normalized).as_posix(), None


def load_json_object(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object")
    return payload


def read_path_list(path_list_path: Path, phase_slug: str) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    try:
        payload = load_json_object(path_list_path)
    except Exception as exc:
        return [], [f"{path_list_path.as_posix()}: path-list JSON unreadable: {exc}"]
    if payload.get("phase_slug") != phase_slug:
        failures.append(f"{path_list_path.as_posix()}: phase_slug mismatch")
    raw_paths = payload.get("paths")
    if not isinstance(raw_paths, list):
        return [], failures + [f"{path_list_path.as_posix()}: paths must be a list"]
    normalized_paths: list[str] = []
    for raw_path in raw_paths:
        normalized, error = normalize_repo_path(raw_path)
        if error:
            failures.append(f"{path_list_path.as_posix()}: {raw_path!r}: {error}")
            continue
        normalized_paths.append(normalized or "")
    return normalized_paths, failures


def read_assertion_manifest(
    manifest_path: Path,
    path_list_path: Path | None,
    artifact_root: str,
    phase_slug: str,
) -> tuple[list[dict], list[str]]:
    failures: list[str] = []
    try:
        payload = load_json_object(manifest_path)
    except Exception as exc:
        return [], [f"{manifest_path.as_posix()}: manifest JSON unreadable: {exc}"]

    if payload.get("phase_slug") != phase_slug:
        failures.append(f"{manifest_path.as_posix()}: phase_slug mismatch")
    if payload.get("validator_mode") != "local_non_mutating":
        failures.append(f"{manifest_path.as_posix()}: validator_mode must be local_non_mutating")
    if payload.get("connector_write_performed") is not False:
        failures.append(f"{manifest_path.as_posix()}: connector_write_performed must be false")
    if payload.get("mutation_performed") is not False:
        failures.append(f"{manifest_path.as_posix()}: mutation_performed must be false")
    gate_effect = payload.get("gmUT_gate_effect", payload.get("gmut_gate_effect"))
    if gate_effect != "none_open_not_tested":
        failures.append(f"{manifest_path.as_posix()}: gmUT_gate_effect must be none_open_not_tested")

    refs = payload.get("artifact_refs")
    if not isinstance(refs, list) or not refs:
        return [], failures + [f"{manifest_path.as_posix()}: artifact_refs must be a non-empty list"]

    phase_prefix = f"{artifact_root.replace(chr(92), '/')}/{phase_slug}-"
    seen_paths: set[str] = set()
    seen_ids: set[str] = set()
    casefold_paths: set[str] = set()
    normalized_refs: list[dict] = []
    for index, ref in enumerate(refs):
        if not isinstance(ref, dict):
            failures.append(f"{manifest_path.as_posix()}: artifact_refs[{index}] must be an object")
            continue
        artifact_id = ref.get("artifact_id")
        if not isinstance(artifact_id, str) or not artifact_id.strip():
            failures.append(f"{manifest_path.as_posix()}: artifact_refs[{index}] missing artifact_id")
        elif artifact_id in seen_ids:
            failures.append(f"{manifest_path.as_posix()}: duplicate artifact_id {artifact_id}")
        else:
            seen_ids.add(artifact_id)
        path_value = ref.get("path") or ref.get("artifact_path")
        normalized, error = normalize_repo_path(path_value)
        if error:
            failures.append(f"{manifest_path.as_posix()}: artifact_refs[{index}] path error: {error}")
            continue
        assert normalized is not None
        if not normalized.startswith(phase_prefix):
            failures.append(f"{manifest_path.as_posix()}: {normalized} is outside current phase artifact root")
        if normalized in seen_paths:
            failures.append(f"{manifest_path.as_posix()}: duplicate path {normalized}")
        seen_paths.add(normalized)
        lowered = normalized.casefold()
        if lowered in casefold_paths:
            failures.append(f"{manifest_path.as_posix()}: case-colliding path {normalized}")
        casefold_paths.add(lowered)
        if Path(normalized).suffix != ".json":
            failures.append(f"{manifest_path.as_posix()}: {normalized} must be a JSON assertion artifact")
        expectation = ref.get("expectation")
        if expectation not in {"positive", "expected_negative"}:
            failures.append(f"{manifest_path.as_posix()}: {normalized} has invalid expectation {expectation!r}")
        expected_status = ref.get("expected_status")
        if expected_status not in {"PASS_SHAPE_ONLY", "FAIL_BLOCKER"}:
            failures.append(f"{manifest_path.as_posix()}: {normalized} has invalid expected_status {expected_status!r}")
        if expectation == "positive" and expected_status != "PASS_SHAPE_ONLY":
            failures.append(f"{manifest_path.as_posix()}: {normalized} positive entry must expect PASS_SHAPE_ONLY")
        if expectation == "expected_negative" and expected_status != "FAIL_BLOCKER":
            failures.append(f"{manifest_path.as_posix()}: {normalized} expected-negative entry must expect FAIL_BLOCKER")
        coverage = ref.get("coverage_tokens")
        if not isinstance(coverage, list) or not all(isinstance(item, str) and item for item in coverage):
            failures.append(f"{manifest_path.as_posix()}: {normalized} coverage_tokens must be non-empty strings")
        normalized_ref = dict(ref)
        normalized_ref["path"] = normalized
        normalized_refs.append(normalized_ref)

    if path_list_path is not None:
        path_list, path_list_failures = read_path_list(path_list_path, phase_slug)
        failures.extend(path_list_failures)
        if sorted(path_list) != sorted(seen_paths):
            failures.append(
                f"{path_list_path.as_posix()}: paths do not match manifest artifact_refs"
            )
    return normalized_refs, failures


def check_assertion_artifacts(
    files: list[Path],
    coverage_tokens: list[str],
    manifest_path: Path | None = None,
    path_list_path: Path | None = None,
    artifact_root: str = "docs/trinity-live-traces",
    phase_slug: str = "",
    require_manifest: bool = False,
) -> tuple[str, str, str | None]:
    file_map = {path.as_posix(): path for path in files}
    manifest_refs: list[dict] = []
    manifest_failures: list[str] = []
    if manifest_path is not None:
        manifest_refs, manifest_failures = read_assertion_manifest(
            manifest_path, path_list_path, artifact_root, phase_slug
        )
    elif require_manifest:
        manifest_failures.append("explicit assertion manifest is required")

    if manifest_failures:
        return "FAIL_BLOCKER", "assertion manifest failed contract", json.dumps(manifest_failures)

    if manifest_refs:
        assertion_files = [Path(ref["path"]) for ref in manifest_refs if "path" in ref]
        manifest_path_set = {path.as_posix() for path in assertion_files}
        stray = [
            path.as_posix()
            for path in files
            if path.suffix == ".json" and "-assert-" in path.name and path.as_posix() not in manifest_path_set
        ]
        if stray:
            return "FAIL_BLOCKER", "assertion manifest failed closed-world contract", json.dumps(stray)
    else:
        assertion_files = [path for path in files if path.suffix == ".json" and "-assert-" in path.name]

    if not assertion_files:
        return "FAIL_BLOCKER", "no assertion artifacts found", None

    positive_count = 0
    expected_negative_count = 0
    failures: list[str] = []
    covered = {token: False for token in coverage_tokens}

    for index, path in enumerate(assertion_files):
        try:
            repo_path = path.as_posix()
            if repo_path not in file_map:
                failures.append(f"{repo_path}: manifest-listed assertion artifact is not in phase artifact set")
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{path.as_posix()}: assertion JSON unreadable: {exc}")
            continue

        name = path.name
        manifest_ref = manifest_refs[index] if manifest_refs else {}
        manifest_tokens = manifest_ref.get("coverage_tokens", [])
        for token in covered:
            if token in name or token in manifest_tokens:
                covered[token] = True

        expected_negative = (
            manifest_ref.get("expectation") == "expected_negative"
            if manifest_ref
            else "-assert-negative-" in name or "pre-fix" in name
        )
        status = payload.get("assertion_status") or payload.get("aggregate_status")
        assertion_failures = payload.get("assertion_failures")
        boundary_ok = (
            payload.get("report_mode") == "local_non_mutating"
            and payload.get("connector_write_performed") is False
            and payload.get("mutation_performed") is False
            and payload.get("external_mutations_performed", False) is False
            and payload.get("gmUT_gate_effect", payload.get("gmut_gate_effect")) == "none_open_not_tested"
        )
        if not boundary_ok:
            failures.append(f"{path.as_posix()}: assertion boundary fields are not local/non-mutating")
        expected_status = manifest_ref.get("expected_status") if manifest_ref else None
        if expected_status and status != expected_status:
            failures.append(f"{path.as_posix()}: status {status!r} did not match manifest expected_status {expected_status!r}")
        expected_report_input = manifest_ref.get("report_input") if manifest_ref else None
        if expected_report_input and payload.get("report_input") != expected_report_input:
            failures.append(f"{path.as_posix()}: report_input did not match manifest")
        if expected_negative:
            expected_negative_count += 1
            if status != "FAIL_BLOCKER" or not assertion_failures:
                failures.append(f"{path.as_posix()}: expected-negative assertion did not fail with reasons")
            for token in manifest_ref.get("expected_failure_tokens", []):
                if token not in " ".join(assertion_failures or []):
                    failures.append(f"{path.as_posix()}: expected failure token {token!r} not found")
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
    parser.add_argument(
        "--assertion-manifest",
        help="Explicit assertion artifact manifest JSON for closed-world assertion checking",
    )
    parser.add_argument(
        "--assertion-path-list",
        help="Optional assertion path-list JSON that must match the assertion manifest paths",
    )
    parser.add_argument(
        "--require-assertion-manifest",
        action="store_true",
        help="Fail closed unless --assertion-manifest is provided when assertion artifacts are required",
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
        status, message, evidence = check_assertion_artifacts(
            files,
            args.require_assertion_coverage,
            manifest_path=Path(args.assertion_manifest) if args.assertion_manifest else None,
            path_list_path=Path(args.assertion_path_list) if args.assertion_path_list else None,
            artifact_root=args.artifact_root,
            phase_slug=args.phase_slug,
            require_manifest=args.require_assertion_manifest,
        )
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

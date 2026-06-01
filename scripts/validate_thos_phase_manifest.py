#!/usr/bin/env python3
"""Validate a THOS phase manifest before publication."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "phase_id",
    "phase_type",
    "start_time_nz",
    "live_local_head",
    "live_upstream_head",
    "drift",
    "current_phase_artifact_list",
    "blocked_actions",
    "validation_chain",
    "thos_gmut_boundary",
}

ALLOWED_PHASE_TYPES = {"GMUT", "THOS", "GMUT_THOS"}

FORBIDDEN_CLAIM_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bGMUT validated\b",
        r"\bvalidates GMUT\b",
        r"\bvalidated GMUT\b",
        r"\bGMUT is validated\b",
        r"\bfinal physics\b",
        r"\bsolved consciousness\b",
        r"\bempirical spiritual proof\b",
        r"\bfifth-force safety\b",
        r"\bGMUT gate closed\b",
        r"\bgates are closed\b",
        r"\bDrive mutation approved\b",
        r"\bcleanup approved\b",
        r"\bdelete approved\b",
    )
]


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing manifest: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("manifest must be a JSON object")
    return payload


def _expect_non_empty_string(payload: dict[str, Any], key: str) -> None:
    if not isinstance(payload.get(key), str) or not payload[key].strip():
        raise SystemExit(f"manifest.{key} must be a non-empty string")


def _expect_string_list(payload: dict[str, Any], key: str, *, min_items: int = 1) -> None:
    value = payload.get(key)
    if not isinstance(value, list) or len(value) < min_items:
        raise SystemExit(f"manifest.{key} must be a list with at least {min_items} item(s)")
    for index, item in enumerate(value, start=1):
        if not isinstance(item, str) or not item.strip():
            raise SystemExit(f"manifest.{key}[{index}] must be a non-empty string")


def _check_required_fields(payload: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_FIELDS - set(payload))
    if missing:
        raise SystemExit(f"manifest missing required fields: {', '.join(missing)}")


def _check_head_fields(payload: dict[str, Any]) -> None:
    head_pattern = re.compile(r"^[0-9a-f]{40}$")
    for key in ("live_local_head", "live_upstream_head"):
        _expect_non_empty_string(payload, key)
        if not head_pattern.fullmatch(payload[key]):
            raise SystemExit(f"manifest.{key} must be a 40-character git hash")
    if payload["live_local_head"] != payload["live_upstream_head"]:
        raise SystemExit("manifest live heads differ")
    _expect_non_empty_string(payload, "drift")
    if payload["drift"].replace("\t", " ").strip() != "0 0":
        raise SystemExit("manifest.drift must be 0 0")


def _check_phase_fields(payload: dict[str, Any]) -> None:
    _expect_non_empty_string(payload, "phase_id")
    _expect_non_empty_string(payload, "phase_type")
    _expect_non_empty_string(payload, "start_time_nz")
    if payload["phase_type"] not in ALLOWED_PHASE_TYPES:
        raise SystemExit(f"manifest.phase_type must be one of: {', '.join(sorted(ALLOWED_PHASE_TYPES))}")


def _check_lists(payload: dict[str, Any]) -> None:
    _expect_string_list(payload, "current_phase_artifact_list")
    _expect_string_list(payload, "blocked_actions")
    _expect_string_list(payload, "validation_chain")
    if not any("GMUT" in action for action in payload["blocked_actions"]):
        raise SystemExit("manifest.blocked_actions must include the GMUT validation boundary")
    if not any("remote equality" in step.lower() for step in payload["validation_chain"]):
        raise SystemExit("manifest.validation_chain must include remote equality verification")


def _check_boundary(payload: dict[str, Any]) -> None:
    boundary = payload.get("thos_gmut_boundary")
    if not isinstance(boundary, dict):
        raise SystemExit("manifest.thos_gmut_boundary must be an object")
    if boundary.get("gmut_gates") != "open":
        raise SystemExit("manifest.thos_gmut_boundary.gmut_gates must be open")
    if boundary.get("thos_claim") != "operational_scaffold_only":
        raise SystemExit("manifest.thos_gmut_boundary.thos_claim must be operational_scaffold_only")


def _check_forbidden_claims(payload: dict[str, Any]) -> None:
    text = json.dumps(payload, sort_keys=True)
    hits = [pattern.pattern for pattern in FORBIDDEN_CLAIM_PATTERNS if pattern.search(text)]
    if hits:
        raise SystemExit(f"manifest contains forbidden claim pattern(s): {', '.join(hits)}")


def _repo_path(repo_root: Path, raw_path: str) -> Path:
    root = repo_root.resolve()
    target = (root / raw_path).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise SystemExit(f"manifest artifact path escapes repo root: {raw_path}") from exc
    return target


def _check_artifact_paths(payload: dict[str, Any], repo_root: Path) -> None:
    missing: list[str] = []
    for raw_path in payload["current_phase_artifact_list"]:
        target = _repo_path(repo_root, raw_path)
        if not target.exists():
            missing.append(raw_path)
    if missing:
        raise SystemExit(f"manifest artifact path(s) missing: {', '.join(missing)}")


def _git_rev_parse(ref: str, repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", ref],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise SystemExit(f"git rev-parse failed for {ref}: {detail}")
    return result.stdout.strip()


def _check_live_git_heads(payload: dict[str, Any], repo_root: Path, upstream_ref: str) -> None:
    local_head = _git_rev_parse("HEAD", repo_root)
    upstream_head = _git_rev_parse(upstream_ref, repo_root)
    if payload["live_local_head"] != local_head:
        raise SystemExit("manifest.live_local_head does not match live HEAD")
    if payload["live_upstream_head"] != upstream_head:
        raise SystemExit("manifest.live_upstream_head does not match live upstream")


def _write_report(path: Path, manifest: Path, checks: list[dict[str, str]]) -> None:
    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "manifest": manifest.as_posix(),
        "status": "PASS",
        "checks": checks,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def validate(path: Path) -> dict[str, Any]:
    payload = _load_json(path)
    _check_required_fields(payload)
    _check_phase_fields(payload)
    _check_head_fields(payload)
    _check_lists(payload)
    _check_boundary(payload)
    _check_forbidden_claims(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a THOS phase manifest JSON file.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--check-artifacts", action="store_true")
    parser.add_argument("--check-live-git", action="store_true")
    parser.add_argument("--upstream-ref", default="origin/codex/GHC-Family/beyonder-shared-omega-line")
    parser.add_argument("--report-json", type=Path)
    args = parser.parse_args()
    checks = [{"name": "base_manifest", "status": "PASS", "detail": "required fields and claim guard passed"}]
    payload = validate(args.manifest)
    repo_root = args.repo_root.resolve()
    if args.check_artifacts:
        _check_artifact_paths(payload, repo_root)
        checks.append({"name": "artifact_paths", "status": "PASS", "detail": "all manifest artifact paths exist"})
    if args.check_live_git:
        _check_live_git_heads(payload, repo_root, args.upstream_ref)
        checks.append({"name": "live_git_heads", "status": "PASS", "detail": "manifest heads match live git refs"})
    if args.report_json:
        _write_report(args.report_json, args.manifest, checks)
        checks.append({"name": "report_json", "status": "PASS", "detail": args.report_json.as_posix()})
    print(f"THOS_PHASE_MANIFEST_OK {args.manifest.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

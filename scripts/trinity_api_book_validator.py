#!/usr/bin/env python3
"""Validate the Trinity API book and usage ledger."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BOOK_PATH = ROOT / "docs" / "trinity-api-book-v6.json"
LEDGER_PATH = ROOT / "docs" / "trinity-api-usage-ledger.jsonl"
OUTPUT_JSON = ROOT / "docs" / "trinity-api-book-validation-latest.json"
OUTPUT_MD = ROOT / "docs" / "trinity-api-book-validation-latest.md"

REQUIRED_FIELDS = {
    "api_id",
    "surface",
    "purpose",
    "trust_class",
    "auth_posture",
    "mode",
    "usage_pattern",
    "source_of_truth",
    "quick_call",
    "wrapper_type",
    "wrapper_target",
    "expected_artifacts",
    "fallback_behavior",
    "notes",
    "cache_requirement",
    "official_source_tier",
    "fallback_class",
    "surface_kind",
    "cache_ttl_class",
    "operator_gate",
    "codex_support_level",
    "model_support_class",
    "delegation_surface",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Trinity API book.")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    if not BOOK_PATH.exists():
        failures.append("api book missing")
        book = {}
    else:
        book = load_json(BOOK_PATH)

    if not LEDGER_PATH.exists():
        failures.append("api usage ledger missing")

    apis = book.get("apis", []) if isinstance(book, dict) else []
    if not isinstance(apis, list):
        failures.append("apis must be a list")
        apis = []
    if len(apis) < 54:
        failures.append(f"expected at least 54 api entries, found {len(apis)}")

    seen: set[str] = set()
    for index, row in enumerate(apis):
        label = f"apis[{index}]"
        if not isinstance(row, dict):
            failures.append(f"{label} must be an object")
            continue
        missing = sorted(REQUIRED_FIELDS - set(row.keys()))
        if missing:
            failures.append(f"{label} missing fields: {missing}")
        api_id = str(row.get("api_id") or "").strip()
        if not api_id:
            failures.append(f"{label} api_id empty")
        elif api_id in seen:
            failures.append(f"duplicate api_id: {api_id}")
        else:
            seen.add(api_id)
        source = str(row.get("source_of_truth") or "").strip()
        if source.startswith("docs/"):
            source_path = ROOT / source
            if not source_path.exists():
                failures.append(f"{api_id or label} missing source_of_truth: {source}")
        wrapper_type = str(row.get("wrapper_type") or "").strip()
        wrapper_target = str(row.get("wrapper_target") or "").strip()
        if wrapper_type not in {"script", "command", "policy", "mcp", "url"}:
            failures.append(f"{api_id or label} invalid wrapper_type")
        if not wrapper_target:
            failures.append(f"{api_id or label} wrapper_target empty")
        elif wrapper_type in {"script", "policy"}:
            target_parts = wrapper_target.split()
            target_path = target_parts[0]
            if target_path.startswith("scripts/") or target_path.startswith("docs/"):
                if not (ROOT / target_path).exists():
                    failures.append(f"{api_id or label} missing wrapper_target: {target_path}")
        expected_artifacts = row.get("expected_artifacts")
        if not isinstance(expected_artifacts, list) or not expected_artifacts:
            failures.append(f"{api_id or label} expected_artifacts must be a non-empty list")
        else:
            for artifact in expected_artifacts:
                artifact_path = str(artifact or "").strip()
                if artifact_path.startswith("docs/") and not (ROOT / artifact_path).exists():
                    failures.append(f"{api_id or label} missing expected_artifact: {artifact_path}")
        if not str(row.get("purpose") or "").strip():
            failures.append(f"{api_id or label} purpose empty")
        if not str(row.get("auth_posture") or "").strip():
            failures.append(f"{api_id or label} auth_posture empty")
        if not str(row.get("fallback_behavior") or "").strip():
            failures.append(f"{api_id or label} fallback_behavior empty")
        trust_class = str(row.get("trust_class") or "")
        mode = str(row.get("mode") or "")
        if trust_class == "operator_hold" and mode != "deferred":
            failures.append(f"{api_id or label} operator_hold entries must use deferred mode")
        if trust_class == "bounded_working_mirror" and mode not in {"bounded_working_mirror", "mirror_only"}:
            failures.append(f"{api_id or label} bounded_working_mirror entries must use bounded_working_mirror or mirror_only mode")

    if LEDGER_PATH.exists():
        for index, line in enumerate(LEDGER_PATH.read_text(encoding="utf-8").splitlines()):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                failures.append(f"ledger[{index}] invalid json: {exc}")
                continue
            for field in ("timestamp", "api_id", "mode", "result"):
                if field not in payload:
                    failures.append(f"ledger[{index}] missing {field}")

    status = "PASS"
    if failures:
        status = "FAIL"
    elif warnings:
        status = "WARN"

    payload = {
        "generated_utc": now_iso(),
        "overall_status": status,
        "error_count": len(failures),
        "warning_count": len(warnings),
        "failures": failures,
        "warnings": warnings,
        "book": BOOK_PATH.relative_to(ROOT).as_posix(),
        "ledger": LEDGER_PATH.relative_to(ROOT).as_posix(),
    }
    write_json(OUTPUT_JSON, payload)
    write_text(
        OUTPUT_MD,
        "# Trinity API Book Validation\n\n"
        f"- overall_status: `{status}`\n"
        f"- errors: `{len(failures)}`\n"
        f"- warnings: `{len(warnings)}`\n"
        + ("\n".join(f"- error: `{item}`" for item in failures) + "\n" if failures else "")
        + ("\n".join(f"- warning: `{item}`" for item in warnings) + "\n" if warnings else ""),
    )
    if status == "FAIL":
        return 1
    if status == "WARN" and args.fail_on_warn:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

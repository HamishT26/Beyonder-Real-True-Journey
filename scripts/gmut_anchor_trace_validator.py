#!/usr/bin/env python3
"""
Validate checksum-linked extraction trace snapshots for canonical GMUT anchors.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class CheckResult:
    check: str
    status: str
    detail: str


def _pass(check: str, detail: str) -> CheckResult:
    return CheckResult(check=check, status="PASS", detail=detail)


def _warn(check: str, detail: str) -> CheckResult:
    return CheckResult(check=check, status="WARN", detail=detail)


def _read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _as_float(value: object) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def _close(a: float, b: float, *, rel_tol: float, abs_tol: float) -> bool:
    delta = abs(a - b)
    return delta <= max(abs_tol, rel_tol * max(abs(a), abs(b)))


def _validate(
    canonical_payload: Dict[str, object],
    manifest_payload: Dict[str, object],
    *,
    rel_tol: float,
    abs_tol: float,
) -> Tuple[List[CheckResult], List[Dict[str, object]]]:
    checks: List[CheckResult] = []
    rows: List[Dict[str, object]] = []

    anchors = canonical_payload.get("anchors", [])
    if not isinstance(anchors, list):
        return [_warn("canonical_anchors", "canonical anchors payload missing list")], rows
    checks.append(_pass("canonical_anchors", f"anchors={len(anchors)}"))

    manifest_traces = manifest_payload.get("traces", [])
    if not isinstance(manifest_traces, list):
        return [_warn("manifest_traces", "manifest trace list missing")], rows
    checks.append(_pass("manifest_traces", f"traces={len(manifest_traces)}"))

    trace_by_id: Dict[str, Dict[str, object]] = {}
    duplicate_trace_ids: List[str] = []
    for entry in manifest_traces:
        if not isinstance(entry, dict):
            continue
        trace_id = str(entry.get("trace_id", "")).strip()
        if not trace_id:
            continue
        if trace_id in trace_by_id:
            duplicate_trace_ids.append(trace_id)
        trace_by_id[trace_id] = entry
    if duplicate_trace_ids:
        checks.append(_warn("manifest_unique_trace_ids", f"duplicates={sorted(set(duplicate_trace_ids))}"))
    else:
        checks.append(_pass("manifest_unique_trace_ids", f"unique_ids={len(trace_by_id)}"))

    missing_manifest = 0
    checksum_mismatches = 0
    numeric_mismatches = 0
    snapshot_missing = 0

    for anchor in anchors:
        if not isinstance(anchor, dict):
            continue
        claim_id = str(anchor.get("claim_id", ""))
        anchor_id = str(anchor.get("anchor_id", ""))
        trace_id = str(anchor.get("extraction_trace_id", "")).strip()
        row_status = "PASS"
        issues: List[str] = []

        if not trace_id:
            row_status = "WARN"
            issues.append("missing extraction_trace_id")
            missing_manifest += 1
            rows.append(
                {
                    "claim_id": claim_id,
                    "anchor_id": anchor_id,
                    "trace_id": trace_id,
                    "status": row_status,
                    "issues": issues,
                }
            )
            continue

        trace_entry = trace_by_id.get(trace_id)
        if trace_entry is None:
            row_status = "WARN"
            issues.append("trace_id not found in manifest")
            missing_manifest += 1
            rows.append(
                {
                    "claim_id": claim_id,
                    "anchor_id": anchor_id,
                    "trace_id": trace_id,
                    "status": row_status,
                    "issues": issues,
                }
            )
            continue

        manifest_anchor_id = str(trace_entry.get("anchor_id", "")).strip()
        if manifest_anchor_id and manifest_anchor_id != anchor_id:
            row_status = "WARN"
            issues.append(f"manifest anchor mismatch: manifest={manifest_anchor_id} canonical={anchor_id}")

        snapshot_rel = str(trace_entry.get("snapshot_path", "")).strip()
        snapshot_path = ROOT / snapshot_rel
        snapshot_sha_expected = str(trace_entry.get("snapshot_sha256", "")).strip().lower()

        snapshot_payload: Dict[str, object] = {}
        snapshot_sha_actual = ""
        if not snapshot_rel or not snapshot_path.exists():
            row_status = "WARN"
            issues.append(f"missing snapshot path: {snapshot_rel or '(empty)'}")
            snapshot_missing += 1
        else:
            snapshot_sha_actual = _sha256(snapshot_path)
            if snapshot_sha_expected and snapshot_sha_expected != "tbd" and snapshot_sha_expected != snapshot_sha_actual:
                row_status = "WARN"
                issues.append("snapshot checksum mismatch")
                checksum_mismatches += 1
            try:
                parsed = _read_json(snapshot_path)
                if isinstance(parsed, dict):
                    snapshot_payload = parsed
            except json.JSONDecodeError:
                row_status = "WARN"
                issues.append("snapshot JSON malformed")

        snapshot_trace_id = str(snapshot_payload.get("trace_id", "")).strip()
        if snapshot_trace_id and snapshot_trace_id != trace_id:
            row_status = "WARN"
            issues.append(f"snapshot trace mismatch: snapshot={snapshot_trace_id} expected={trace_id}")

        canonical_value = _as_float(anchor.get("external_upper_bound"))
        manifest_value = _as_float(trace_entry.get("extracted_numeric_value"))
        snapshot_value = _as_float(snapshot_payload.get("extracted_numeric_value"))
        value_triplet = [item for item in [canonical_value, manifest_value, snapshot_value] if item is not None]
        if len(value_triplet) == 3:
            max_val = max(value_triplet)
            min_val = min(value_triplet)
            if not _close(max_val, min_val, rel_tol=rel_tol, abs_tol=abs_tol):
                row_status = "WARN"
                issues.append(
                    f"numeric mismatch: canonical={canonical_value} manifest={manifest_value} snapshot={snapshot_value}"
                )
                numeric_mismatches += 1
        else:
            row_status = "WARN"
            issues.append("missing numeric value in canonical/manifest/snapshot")
            numeric_mismatches += 1

        rows.append(
            {
                "claim_id": claim_id,
                "anchor_id": anchor_id,
                "trace_id": trace_id,
                "status": row_status,
                "snapshot_path": snapshot_rel,
                "snapshot_sha256_expected": snapshot_sha_expected,
                "snapshot_sha256_actual": snapshot_sha_actual,
                "issues": issues,
            }
        )

    checks.append(_pass("anchor_rows_scanned", f"rows={len(rows)}"))
    if missing_manifest == 0:
        checks.append(_pass("trace_ids_mapped", "all canonical trace IDs mapped in manifest"))
    else:
        checks.append(_warn("trace_ids_mapped", f"missing_trace_mappings={missing_manifest}"))

    if snapshot_missing == 0:
        checks.append(_pass("snapshot_paths_exist", "all snapshot files present"))
    else:
        checks.append(_warn("snapshot_paths_exist", f"missing_snapshots={snapshot_missing}"))

    if checksum_mismatches == 0:
        checks.append(_pass("snapshot_checksums", "all checksums match manifest"))
    else:
        checks.append(_warn("snapshot_checksums", f"checksum_mismatches={checksum_mismatches}"))

    if numeric_mismatches == 0:
        checks.append(_pass("numeric_consistency", "canonical/manifest/snapshot values align"))
    else:
        checks.append(_warn("numeric_consistency", f"numeric_mismatches={numeric_mismatches}"))
    return checks, rows


def _build_markdown(
    generated_utc: str,
    overall_status: str,
    checks: List[CheckResult],
    rows: List[Dict[str, object]],
    rel_tol: float,
    abs_tol: float,
) -> str:
    lines = [
        "# GMUT External-Anchor Trace Validation Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        f"- overall_status: **{overall_status}**",
        f"- relative_tolerance: `{rel_tol}`",
        f"- absolute_tolerance: `{abs_tol}`",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for item in checks:
        lines.append(f"| {item.check} | {item.status} | {item.detail} |")

    lines.extend(
        [
            "",
            "## Anchor trace status",
            "| claim_id | anchor_id | trace_id | status | issues |",
            "|---|---|---|---|---|",
        ]
    )
    for row in rows:
        issues = ", ".join(str(issue) for issue in row.get("issues", [])) if row.get("issues") else "-"
        lines.append(
            f"| {row.get('claim_id', '')} | {row.get('anchor_id', '')} | {row.get('trace_id', '')} | "
            f"{row.get('status', '')} | {issues} |"
        )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate checksum-linked GMUT anchor extraction traces.")
    parser.add_argument("--canonical-input", default="docs/mind-track-external-anchor-canonical-inputs-v1.json")
    parser.add_argument("--trace-manifest", default="docs/mind-track-external-anchor-trace-manifest-v1.json")
    parser.add_argument("--reports-dir", default="docs/mind-track-runs")
    parser.add_argument("--latest-json", default="docs/mind-track-gmut-trace-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/mind-track-gmut-trace-validation-latest.md")
    parser.add_argument("--relative-tolerance", type=float, default=1e-9)
    parser.add_argument("--absolute-tolerance", type=float, default=0.0)
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    canonical_path = ROOT / args.canonical_input
    manifest_path = ROOT / args.trace_manifest

    checks: List[CheckResult] = []
    rows: List[Dict[str, object]] = []

    if not canonical_path.exists():
        checks.append(_warn("canonical_input_exists", f"missing canonical input: {args.canonical_input}"))
    else:
        checks.append(_pass("canonical_input_exists", args.canonical_input))
    if not manifest_path.exists():
        checks.append(_warn("trace_manifest_exists", f"missing trace manifest: {args.trace_manifest}"))
    else:
        checks.append(_pass("trace_manifest_exists", args.trace_manifest))

    if canonical_path.exists() and manifest_path.exists():
        canonical_payload = _read_json(canonical_path)
        manifest_payload = _read_json(manifest_path)
        core_checks, rows = _validate(
            canonical_payload,
            manifest_payload,
            rel_tol=max(0.0, args.relative_tolerance),
            abs_tol=max(0.0, args.absolute_tolerance),
        )
        checks.extend(core_checks)

    overall_status = "PASS" if all(item.status == "PASS" for item in checks) else "WARN"
    payload = {
        "generated_utc": generated_utc,
        "overall_status": overall_status,
        "canonical_input": args.canonical_input,
        "trace_manifest": args.trace_manifest,
        "relative_tolerance": max(0.0, args.relative_tolerance),
        "absolute_tolerance": max(0.0, args.absolute_tolerance),
        "checks": [asdict(item) for item in checks],
        "anchors": rows,
    }
    markdown = _build_markdown(
        generated_utc,
        overall_status,
        checks,
        rows,
        rel_tol=max(0.0, args.relative_tolerance),
        abs_tol=max(0.0, args.absolute_tolerance),
    )

    reports_dir = ROOT / args.reports_dir
    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_json = ROOT / args.latest_json
    latest_md = ROOT / args.latest_md
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    timestamped_json = reports_dir / f"{stamp}-gmut-anchor-trace-validation.json"
    timestamped_md = reports_dir / f"{stamp}-gmut-anchor-trace-validation.md"

    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={overall_status}")
    print(f"timestamped_json={timestamped_json.relative_to(ROOT)}")
    print(f"timestamped_md={timestamped_md.relative_to(ROOT)}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    if args.fail_on_warn and overall_status != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

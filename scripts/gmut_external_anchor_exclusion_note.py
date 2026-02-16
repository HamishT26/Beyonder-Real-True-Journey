#!/usr/bin/env python3
"""
Generate a GMUT external-anchor numeric exclusion note.

Important: this stage is a structured comparison scaffold. It does not claim
external empirical confirmation by itself.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def _read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _markdown(generated_utc: str, payload: Dict[str, object]) -> str:
    lines = [
        "# GMUT External-Anchor Numeric Exclusion Note",
        "",
        f"- generated_utc: `{generated_utc}`",
        f"- overall_status: **{payload['overall_status']}**",
        f"- comparator_status: `{payload['comparator_status']}`",
        f"- comparator_max_abs_deviation: `{payload['comparator_max_abs_deviation']}`",
        f"- required_canonical_fields_present: `{payload['required_canonical_fields_present']}`",
        f"- anchors_with_missing_required_fields: `{payload['anchors_with_missing_required_fields']}`",
        "",
        "## Anchor comparisons",
        "| claim_id | anchor_id | source_tier | confidence | ext_bound | ext_uncertainty | conservative_bound | gmut_working_bound | overhang_factor | ingestion_status | interpretation |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in payload["anchors"]:
        lines.append(
            "| {claim_id} | {anchor_id} | {source_tier} | {confidence_level:.3f} | {external_upper_bound:.6e} | "
            "{external_uncertainty_abs:.6e} | {conservative_external_upper_bound:.6e} | {gmut_working_bound:.6e} | "
            "{overhang_factor:.3e} | {ingestion_status} | {interpretation} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Governance note",
            "These comparisons are **parameter-screening signals**. Any anchor flagged as provisional,",
            "secondary-tier, or pending canonical ingestion remains an open evidence gap.",
            "Promotion requires primary-source ingestion with explicit confidence/uncertainty metadata.",
            "",
        ]
    )
    return "\n".join(lines)


def _evaluate(input_payload: Dict[str, object], comparator_payload: Dict[str, object]) -> Dict[str, object]:
    anchors = input_payload.get("anchors", [])
    if not isinstance(anchors, list) or not anchors:
        raise SystemExit("No anchors found in input payload.")

    rows: List[Dict[str, object]] = []
    warn = False
    required_fields = input_payload.get("required_canonical_ingestion_fields", [])
    required_fields_list = [str(field) for field in required_fields] if isinstance(required_fields, list) else []
    required_fields_present = bool(required_fields_list)
    anchors_with_missing_required_fields = 0
    for anchor in anchors:
        if not isinstance(anchor, dict):
            continue
        external_upper_bound = float(anchor.get("external_upper_bound", 0.0))
        external_uncertainty_abs = abs(float(anchor.get("external_uncertainty_abs", 0.0)))
        gmut_working_bound = float(anchor.get("gmut_working_bound", 0.0))
        confidence_level = float(anchor.get("confidence_level", 0.0))
        conservative_upper_bound = external_upper_bound + external_uncertainty_abs
        if conservative_upper_bound <= 0:
            overhang = float("inf")
            interpretation = "invalid_external_bound"
            warn = True
        else:
            overhang = gmut_working_bound / conservative_upper_bound
            if overhang <= 1.0:
                interpretation = "within_anchor_bound"
            else:
                interpretation = "requires_tighter_parameter_fit"
                warn = True
        ingestion_status = str(anchor.get("ingestion_status", "unknown"))
        source_tier = str(anchor.get("source_tier", "unknown"))
        provisional = bool(anchor.get("provisional", False))
        if provisional:
            warn = True
        if source_tier != "primary":
            warn = True
        if ingestion_status != "ingested_primary_source":
            warn = True
            if interpretation == "within_anchor_bound":
                interpretation = "provisionally_within_bound_pending_ingestion"
        if confidence_level <= 0.0 or confidence_level > 1.0:
            warn = True
        missing_required_fields = [
            field for field in required_fields_list if not str(anchor.get(field, "")).strip()
        ]
        if missing_required_fields:
            warn = True
            anchors_with_missing_required_fields += 1

        rows.append(
            {
                "claim_id": str(anchor.get("claim_id", "unknown")),
                "anchor_id": str(anchor.get("anchor_id", "unknown")),
                "source_kind": str(anchor.get("source_kind", "unknown")),
                "source_tier": source_tier,
                "confidence_level": confidence_level,
                "external_upper_bound": external_upper_bound,
                "external_uncertainty_abs": external_uncertainty_abs,
                "conservative_external_upper_bound": conservative_upper_bound,
                "gmut_working_bound": gmut_working_bound,
                "overhang_factor": overhang,
                "interpretation": interpretation,
                "source_label": str(anchor.get("source_label", "")),
                "source_url": str(anchor.get("source_url", "")),
                "source_citation": str(anchor.get("source_citation", "")),
                "dataset_version_or_release": str(anchor.get("dataset_version_or_release", "")),
                "bound_units": str(anchor.get("bound_units", "")),
                "signal_mapping_note": str(anchor.get("signal_mapping_note", "")),
                "ingestion_status": ingestion_status,
                "missing_required_fields": missing_required_fields,
                "provisional": provisional,
            }
        )

    status = "WARN" if warn else "PASS"
    return {
        "overall_status": status,
        "comparator_status": str(comparator_payload.get("status", "unknown")),
        "comparator_max_abs_deviation": float(comparator_payload.get("max_abs_deviation", 0.0)),
        "required_canonical_fields_present": required_fields_present,
        "required_canonical_ingestion_fields": required_fields_list if required_fields_present else [],
        "anchors_with_missing_required_fields": anchors_with_missing_required_fields,
        "anchors": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate external-anchor numeric exclusion note for GMUT.")
    parser.add_argument(
        "--anchor-input",
        default="docs/mind-track-external-anchor-canonical-inputs-v1.json",
        help="Input JSON describing external anchor numeric bounds.",
    )
    parser.add_argument(
        "--comparator-json",
        default="docs/mind-track-gmut-comparator-latest.json",
        help="Latest internal comparator metrics JSON.",
    )
    parser.add_argument("--reports-dir", default="docs/mind-track-runs")
    parser.add_argument("--latest-json", default="docs/mind-track-gmut-anchor-exclusion-latest.json")
    parser.add_argument("--latest-md", default="docs/mind-track-gmut-anchor-exclusion-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    anchor_input = Path(args.anchor_input)
    comparator_json = Path(args.comparator_json)
    if not anchor_input.exists():
        raise SystemExit(f"Missing anchor input: {anchor_input}")
    if not comparator_json.exists():
        raise SystemExit(f"Missing comparator JSON: {comparator_json}")

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    payload = _evaluate(_read_json(anchor_input), _read_json(comparator_json))
    payload["generated_utc"] = generated_utc
    markdown = _markdown(generated_utc, payload)

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json = reports_dir / f"{stamp}-gmut-anchor-exclusion-note.json"
    timestamped_md = reports_dir / f"{stamp}-gmut-anchor-exclusion-note.md"
    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={payload['overall_status']}")
    print(f"timestamped_json={timestamped_json}")
    print(f"timestamped_md={timestamped_md}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")

    if args.fail_on_warn and payload["overall_status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

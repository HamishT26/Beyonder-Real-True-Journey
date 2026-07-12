#!/usr/bin/env python3
"""Validate read-only empirical adapter manifests for the GMUT research kernel.

The module validates metadata and parameter-to-observable mappings. It never
downloads datasets, runs a cosmological likelihood, or claims a model fit.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


REQUIRED_FIELDS = {
    "dataset_id",
    "release",
    "authority",
    "source_url",
    "citation",
    "license_or_terms",
    "baseline",
    "parameter_map",
    "expected_products",
    "status",
}
ALLOWED_STATUSES = {"manifest_only", "baseline_pending", "adapter_ready", "fit_complete"}


@dataclass(frozen=True)
class AdapterIssue:
    path: str
    code: str
    message: str


def _is_https(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate_adapter_manifest(adapters: Iterable[dict[str, Any]]) -> tuple[AdapterIssue, ...]:
    issues: list[AdapterIssue] = []
    seen: set[str] = set()
    for index, adapter in enumerate(adapters):
        path = f"adapters[{index}]"
        missing = sorted(field for field in REQUIRED_FIELDS if not adapter.get(field))
        if missing:
            issues.append(AdapterIssue(path, "missing_fields", ", ".join(missing)))
            continue
        dataset_id = str(adapter["dataset_id"])
        if dataset_id in seen:
            issues.append(AdapterIssue(path, "duplicate_dataset_id", dataset_id))
        seen.add(dataset_id)
        if not _is_https(str(adapter["source_url"])):
            issues.append(AdapterIssue(path, "non_https_source", str(adapter["source_url"])))
        if adapter["status"] not in ALLOWED_STATUSES:
            issues.append(AdapterIssue(path, "invalid_status", str(adapter["status"])))
        if not isinstance(adapter["parameter_map"], list) or not adapter["parameter_map"]:
            issues.append(AdapterIssue(path, "empty_parameter_map", "at least one mapping is required"))
        if adapter["status"] == "fit_complete" and not adapter.get("fit_receipt"):
            issues.append(AdapterIssue(path, "missing_fit_receipt", "fit_complete requires fit_receipt"))
        serialized = json.dumps(adapter, ensure_ascii=False)
        if ":\\" in serialized or serialized.startswith("/"):
            issues.append(AdapterIssue(path, "local_path_leak", "manifest must be portable"))
    return tuple(issues)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    adapters = payload["adapters"] if isinstance(payload, dict) else payload
    issues = validate_adapter_manifest(adapters)
    report = {
        "schema": "ghc.family.empirical-adapter-validation.v1",
        "valid": not issues,
        "adapter_count": len(adapters),
        "issues": [asdict(issue) for issue in issues],
        "boundary": "metadata_validation_only_no_download_no_likelihood_no_empirical_confirmation",
    }
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

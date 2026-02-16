"""
freed_id_minimum_disclosure_adversarial_verifier.py
---------------------------------------------------

Adversarial verification harness for GOV-002 minimum-disclosure controls.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set

from freed_id_minimum_disclosure import (
    DEFAULT_SENSITIVE_FIELDS,
    MinimumDisclosurePolicy,
    build_minimum_disclosure_presentation,
    validate_minimum_disclosure_presentation,
)


@dataclass
class CheckResult:
    check: str
    status: str
    detail: str


def _build_markdown(generated_utc: str, overall_status: str, checks: List[CheckResult]) -> str:
    lines = [
        "# Freed ID Minimum-Disclosure Adversarial Verification Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        f"- control: `GOV-002`",
        f"- overall_status: **{overall_status}**",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for check in checks:
        lines.append(f"| {check.check} | {check.status} | {check.detail} |")
    return "\n".join(lines).strip() + "\n"


def _vector_check(
    vector: Dict[str, object],
    sensitive_fields: Set[str],
) -> List[CheckResult]:
    checks: List[CheckResult] = []
    vector_id = str(vector.get("vector_id", "unknown"))
    claims = vector.get("claims", {})
    requested_fields = vector.get("requested_fields", [])
    allowed_sensitive_fields = set(vector.get("allowed_sensitive_fields", []))
    expect_disclosed_fields = set(vector.get("expect_disclosed_fields", []))
    expect_denied_sensitive_fields = set(vector.get("expect_denied_sensitive_fields", []))

    if not isinstance(claims, dict) or not isinstance(requested_fields, list):
        checks.append(CheckResult(f"{vector_id}:input_shape", "FAIL", "claims/requested_fields shape invalid"))
        return checks

    policy = MinimumDisclosurePolicy(
        sensitive_fields=set(sensitive_fields),
        allowed_sensitive_fields=set(str(field) for field in allowed_sensitive_fields),
    )
    presentation = build_minimum_disclosure_presentation(
        subject_did="did:freed:adversarial",
        credential_id=f"did:freed:adversarial#{vector_id}",
        claims=claims,
        requested_fields=[str(field) for field in requested_fields],
        policy=policy,
    )

    valid, detail = validate_minimum_disclosure_presentation(presentation, policy)
    checks.append(
        CheckResult(f"{vector_id}:schema_validation", "PASS" if valid else "FAIL", detail)
    )

    disclosed_fields = set(str(key) for key in presentation["disclosed_claims"].keys())
    denied_sensitive_fields = set(str(field) for field in presentation["denied_sensitive_fields"])
    requested_set = set(str(field) for field in requested_fields)

    if disclosed_fields == expect_disclosed_fields:
        checks.append(
            CheckResult(
                f"{vector_id}:expected_disclosed_fields",
                "PASS",
                f"disclosed={sorted(disclosed_fields)}",
            )
        )
    else:
        checks.append(
            CheckResult(
                f"{vector_id}:expected_disclosed_fields",
                "FAIL",
                f"expected={sorted(expect_disclosed_fields)} observed={sorted(disclosed_fields)}",
            )
        )

    if denied_sensitive_fields == expect_denied_sensitive_fields:
        checks.append(
            CheckResult(
                f"{vector_id}:expected_denied_sensitive_fields",
                "PASS",
                f"denied={sorted(denied_sensitive_fields)}",
            )
        )
    else:
        checks.append(
            CheckResult(
                f"{vector_id}:expected_denied_sensitive_fields",
                "FAIL",
                f"expected={sorted(expect_denied_sensitive_fields)} observed={sorted(denied_sensitive_fields)}",
            )
        )

    leaked_unrequested = sorted(disclosed_fields - requested_set)
    if leaked_unrequested:
        checks.append(
            CheckResult(
                f"{vector_id}:no_unrequested_leak",
                "FAIL",
                f"leaked_unrequested={leaked_unrequested}",
            )
        )
    else:
        checks.append(CheckResult(f"{vector_id}:no_unrequested_leak", "PASS", "none"))

    leaked_sensitive = sorted(
        field
        for field in disclosed_fields
        if field in sensitive_fields and field not in allowed_sensitive_fields
    )
    if leaked_sensitive:
        checks.append(
            CheckResult(
                f"{vector_id}:no_disallowed_sensitive_leak",
                "FAIL",
                f"leaked_sensitive={leaked_sensitive}",
            )
        )
    else:
        checks.append(
            CheckResult(f"{vector_id}:no_disallowed_sensitive_leak", "PASS", "none")
        )

    return checks


def _run_verification(vectors_path: Path) -> List[CheckResult]:
    checks: List[CheckResult] = []
    if not vectors_path.exists():
        return [CheckResult("vectors_file_exists", "FAIL", f"missing {vectors_path}")]

    checks.append(CheckResult("vectors_file_exists", "PASS", str(vectors_path)))
    payload = json.loads(vectors_path.read_text(encoding="utf-8"))
    vectors = payload.get("vectors", [])
    if not isinstance(vectors, list) or not vectors:
        checks.append(CheckResult("vectors_loaded", "FAIL", "no vectors available"))
        return checks
    checks.append(CheckResult("vectors_loaded", "PASS", f"count={len(vectors)}"))

    sensitive_fields = set(DEFAULT_SENSITIVE_FIELDS)
    for vector in vectors:
        if not isinstance(vector, dict):
            checks.append(CheckResult("vector_shape", "FAIL", "vector entry is not object"))
            continue
        checks.extend(_vector_check(vector, sensitive_fields))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Run GOV-002 adversarial minimum-disclosure verification.")
    parser.add_argument(
        "--vectors",
        default="docs/freed-id-minimum-disclosure-adversarial-vectors-v0.json",
        help="Path to adversarial vectors JSON.",
    )
    parser.add_argument("--reports-dir", default="docs/heart-track-runs", help="Directory for timestamped outputs.")
    parser.add_argument(
        "--latest-json",
        default="docs/heart-track-min-disclosure-adversarial-latest.json",
        help="Latest JSON output path.",
    )
    parser.add_argument(
        "--latest-md",
        default="docs/heart-track-min-disclosure-adversarial-latest.md",
        help="Latest markdown output path.",
    )
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    checks = _run_verification(Path(args.vectors))
    overall_status = "PASS" if all(check.status == "PASS" for check in checks) else "FAIL"

    payload = {
        "generated_utc": generated_utc,
        "control_id": "GOV-002",
        "mode": "adversarial",
        "overall_status": overall_status,
        "checks": [asdict(check) for check in checks],
    }
    markdown = _build_markdown(generated_utc, overall_status, checks)

    timestamped_json = reports_dir / f"{stamp}-freedid-min-disclosure-adversarial-check.json"
    timestamped_md = reports_dir / f"{stamp}-freedid-min-disclosure-adversarial-check.md"
    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={overall_status}")
    print(f"timestamped_json={timestamped_json}")
    print(f"timestamped_md={timestamped_md}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
